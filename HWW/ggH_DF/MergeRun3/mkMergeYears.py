#!/usr/bin/env python
import subprocess
import os
import sys
import ROOT
import uproot
import numpy as np
from sys import argv
import argparse
import copy
import shutil
from textwrap import dedent
from mkShapesRDF.shapeAnalysis.ConfigLib import ConfigLib
import mkShapesRDF.shapeAnalysis.latinos.LatinosUtils as utils
from concurrent.futures import ProcessPoolExecutor, as_completed
ROOT.gROOT.SetBatch(True)
ROOT.TH1.SetDefaultSumw2(True)

"""
--------- mkMergeYears.py
Script to merge the histograms of different years (e.g. Run 2, Run 3, ...) into a single root file, 
summing the histograms of the different years and properly handling the nuisances.

- To run the code locally, merging all cuts and variables in one go:
    python mkMergeYears.py --inDir rootFiles/ --outDir rootFiles/ --nJobs X (where X is the number of parallel jobs to run, e.g. 10)

- To run the code locally, merging only a specific cut and variable:
    python mkMergeYears.py --inDir rootFiles/ --outDir rootFiles/ --onlyCut cutName --onlyVar varName

- To submit the code to condor, merging only a specific cut and variable:
    python mkMergeYears.py --inDir rootFiles/ --outDir rootFiles/ --onlyCut cutName --onlyVar varName --doSubmit

If last option is used, remember to do hadd of the temporary files at the end, with:
    hadd -fk rootFiles/histos_tag.root rootFiles/histos_tag__ALL__*.root
"""

def defaultParser():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument(
        "-o",
        "--outDir",
        type=str,
        help="Output directory",
        required=False,
        default=f"rootFiles/",
    )

    parser.add_argument(
        "-i",
        "--inDir",
        type=str,
        help="Input directory",
        required=False,
        default=f"rootFiles/",
    )

    parser.add_argument(
        "-j",
        "--nJobs",
        type=int,
        help="Number of jobs",
        required=False,
        default=10,
    )

    parser.add_argument(
        "-c",
        "--onlyCut",
        type=str,
        help="Cut to merge (if not specified, merge all cuts)",
        required=False,
        default=None,
    )

    parser.add_argument(
        "-v",
        "--onlyVar",
        type=str,
        help="Variable to merge (if not specified, merge all variables)",
        required=False,
        default=None,
    )

    parser.add_argument(
        "-sub",
        "--doSubmit",
        action='store_true',
        help="Submit jobs to condor",
        default=False,
    )

    parser.add_argument(
        "--configurationFile",
        dest="pycfg",
        help="input configuration file",
        default="merge_configuration.py",
    )
    
    return parser

#
# load configurations into the parser, according to configuration.py
#
def loadDefaultOptions(parser, pycfg=None, quiet=False):

    if pycfg != None and os.path.exists(pycfg):
        # print ("loadDefaultOptions: pycfg = ", pycfg)
        handle = open(pycfg,'r')
        variables = {}
        exec(handle.read(),variables)
        handle.close()
        # clean the dictionary to remove globals due to "exec" funcionality
        variables = {k: v for k, v in variables.items() if not (k.startswith('__') and k.endswith('__'))}

        print ("loadDefaultOptions: variables = ", variables.items())
        for opt_name, opt_value in variables.items():
          parser.add_argument('--' + opt_name, default=opt_value)
        return
    else:
        return


# ----------------------------------------------------- Merge Years: e.g. Run 2, Run 3, ... --------------------------------------
class MergerFactory:
    # _logger = logging.getLogger('MergerFactory')

    # _____________________________________________________________________________
    def __init__(self, tag, inDir, outDir, foldersToMerge):

        ### Prepare the output keys, output file, and inputs        
        self.inDir = inDir
        self.outDir = outDir
        self._fileOut = outDir + '/histos_' + tag + '.root'
        self._filesIn = {}
        self.all_nuisances = {}
        self.all_years = ["2016", "2017", "2018", "2022EE", "2022", "2023BPix", "2023", "2024", "2025", "2026"] # The order is important

        for folderHR, folder in foldersToMerge.items():
            # Look inside the exact directory specified in your merge_configuration file, 
            # fallback to the global outDir if it's missing.
            source_dir = folder.get("outDir", outDir)
            
            old_root_file_name = os.path.join(source_dir, "mkShapes__" + folder["tag"] + ".root")
            new_root_file_name = os.path.join(outDir, "year_" + folderHR + "_histos_" + folder["tag"] + ".root")
            
            print(f" Partial: old_root_file_name = {old_root_file_name}")
            os.system(f"cp {old_root_file_name} {new_root_file_name}")

            self._filesIn[folderHR] = new_root_file_name

    def extract_dict(self, filename, var_name, samples_input={}):
            import os
            import sys
            
            namespace = {
                'samples': samples_input,
                'os': os,
                'sys': sys,
                'cuts': globals().get('cuts', {}),
                'categories': globals().get('categories', {}),
                'nuisances': {},
                'aliases': {}
            }
            
            try:
                with open(filename, 'r') as f:
                    exec(f.read(), namespace, namespace)
                
                # If the dict object we want wasn't found or is evaluated to None, fallback to empty dict
                result = namespace.get(var_name)
                return result if result is not None else {}
                
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                return {}  # Return an empty dictionary instead of None to prevent 'NoneType' crashes
        
    def getVariedHistos(self, folderHR, folder_name, rootFileIn, sampleName, nuisanceName, nuisance, yearKeys, extra="CMS_") :
        
        nameTemp     = 'histo_' + str(sampleName)
        nameTempUp   = 'histo_' + str(sampleName) + '_' + (nuisance['name']) + 'Up'
        nameTempDown = 'histo_' + str(sampleName) + '_' + (nuisance['name']) + 'Down'

        usedExtra = False
        nameExtraTempUp   = 'histo_' + str(sampleName) + '_' + extra + (nuisance['name']) + 'Up'
        nameExtraTempDown = 'histo_' + str(sampleName) + '_' + extra + (nuisance['name']) + 'Down'

        #
        # If the histogram up and down are present in the input root files, add the histograms up/down
        # No matter if then the nuisance is not a shape nuisance but lnN ... still, you add the histograms!
        # eh perbacco, the histogram exists, then you add it, you might change idea later on
        #
        # print ("All the histograms names is [histograms[", folderHR, "][", folder_name, "]]: ", histograms[folderHR][folder_name].keys())
        # print ("I'm looking for: ", nameTempUp, " and ", nameTempDown)
        if nameTempUp in yearKeys and nameTempDown in yearKeys :
            
            # print (" I found: ", nameTempUp, " and ", nameTempDown)
            histo_up_to_be_summed = rootFileIn.Get(folder_name + "/" + nameTempUp)
            histo_down_to_be_summed = rootFileIn.Get(folder_name + "/" + nameTempDown)
            histo_up_to_be_summed_weights = 1.0
            histo_down_to_be_summed_weights = 1.0

        elif nameExtraTempUp in yearKeys and nameExtraTempDown in yearKeys :
            
            # In some cases, the histograms might be named with the "CMS_" prefix, e.g. "histo_sample_CMS_nuisanceUp" instead of "histo_sample_nuisanceUp". 
            # In this case, we should look for the histograms with the "CMS_" prefix and add them if they are present.

            # print (" I found extra-named: ", nameExtraTempUp, " and ", nameExtraTempDown)
            histo_up_to_be_summed = rootFileIn.Get(folder_name + "/" + nameExtraTempUp)
            histo_down_to_be_summed = rootFileIn.Get(folder_name + "/" + nameExtraTempDown)
            histo_up_to_be_summed_weights = 1.0
            histo_down_to_be_summed_weights = 1.0

            usedExtra = True

        else :

            #
            # it might be that for that particular sample
            # or for a specific year in the combination
            # the nuisance is not defined or missing.
            # In this case, ok, nothing to be done: the up/down variation should be taken as the nominal
            #
            # The nuisance might have been a lnN ... this has to be handled properly
            #

            if nuisanceName in self.all_nuisances[folderHR].keys() :
                if self.all_nuisances[folderHR][nuisanceName]['type'] == 'lnN' and  sampleName in self.all_nuisances[folderHR][nuisanceName]['samples'].keys() :
                    #
                    #    lnN nuisances:
                    #    the up/down could be given separately:   '1.03/0.99'
                    #    or unique :                              '1.02'
                    #
                    histo_up_to_be_summed = rootFileIn.Get(folder_name + "/" + nameTemp )
                    histo_down_to_be_summed = rootFileIn.Get(folder_name + "/" + nameTemp )

                    if "/" not in self.all_nuisances[folderHR][nuisanceName]['samples'][sampleName]:
                      # print (" I'm using the weight [", folderHR, "][", nuisanceName, "] =  ", float(all_nuisances[folderHR][nuisanceName]['samples'][sampleName]))
                      histo_up_to_be_summed_weights =  float(self.all_nuisances[folderHR][nuisanceName]['samples'][sampleName])
                      histo_down_to_be_summed_weights = 1. / float(self.all_nuisances[folderHR][nuisanceName]['samples'][sampleName])
                    else :
                        # print ("all_nuisances[", folderHR, "][", nuisanceName, "]['samples'][", sampleName, "] = ", all_nuisances[folderHR][nuisanceName]['samples'][sampleName])
                        val_up, val_down = self.all_nuisances[folderHR][nuisanceName]['samples'][sampleName].split("/")
                        histo_up_to_be_summed_weights = val_up
                        histo_down_to_be_summed_weights = val_down

                else:
                    # Take nominal value if the nuisance is not defined for that sample, or if the nuisance is not a lnN nor shape
                    histo_up_to_be_summed = rootFileIn.Get(folder_name + "/" + nameTemp )
                    histo_down_to_be_summed = rootFileIn.Get(folder_name + "/" + nameTemp )
                    histo_up_to_be_summed_weights = 1.0
                    histo_down_to_be_summed_weights = 1.0

            else:
                ### To keep the (un)correlation of nuisances, one need to define new nuisances. For example:
                # lumi_Uncorrelated exists in all the nuisances.py, but it needs to be uncorrelated across years
                # therefore, in the global nuisances.py is defined a new nuisance, e.g. lumi_Uncorrelated_2018, lumi_Uncorrelated_2017, etc.
                matched = False
                for year in self.all_years :
                    if year in nuisanceName and year in folderHR :
                        oldNuisanceName = nuisanceName.split("_"+year)[0]
                        if oldNuisanceName in self.all_nuisances[folderHR].keys() :
                            matched = True
                            histo_up_to_be_summed, histo_down_to_be_summed, histo_up_to_be_summed_weights, histo_down_to_be_summed_weights, nameTempUp, nameTempDown = self.getVariedHistos(folderHR, folder_name, rootFileIn, sampleName, oldNuisanceName, nuisance, yearKeys, extra="CMS_")

                if not matched :
                    # print(f"Taking nominal value for {nuisanceName} in {folderHR}!")
                    histo_up_to_be_summed = rootFileIn.Get(folder_name + "/" + nameTemp )
                    histo_down_to_be_summed = rootFileIn.Get(folder_name + "/" + nameTemp )
                    histo_up_to_be_summed_weights = 1.0
                    histo_down_to_be_summed_weights = 1.0

        if usedExtra :
            return histo_up_to_be_summed, histo_down_to_be_summed, histo_up_to_be_summed_weights, histo_down_to_be_summed_weights, nameExtraTempUp, nameExtraTempDown
        else :
            return histo_up_to_be_summed, histo_down_to_be_summed, histo_up_to_be_summed_weights, histo_down_to_be_summed_weights, nameTempUp, nameTempDown

    #### Be memory efficient to work with large number of samples and nuisances
    # 
    # Avoid copying everything in memory, and instead read the histograms from the root files on the fly, and merge them directly into the output file.
    # Do it per cut, per sample and per variable, and store the output in each iteration. Open and close the output file at each iteration to avoid keeping everything in memory.
    #
    def process_cut_variable(self, cutName, variableName, samples, new_list_of_nuisances):

        print ("process_cut_variable:: cutName = ", cutName, " variableName = ", variableName)
        folder_name = cutName + "/" + variableName
        # print (" while adding nominals folder_name = ", folder_name)

        ## Store all keys using uproot
        allKeys = {}
        for folderHR in self._filesIn.keys() :
            fileIn = self._filesIn[folderHR]
            with uproot.open(fileIn) as f:
                allKeys[folderHR] = np.unique([ key.split(";")[0] for key in f[folder_name].keys() ])
                # print(f"Number of keys for {folderHR} in {folder_name}: {len(allKeys[folderHR])}")   

        rootIn = {}
        # loop over years and copy nominals
        for folderHR in self._filesIn.keys():
            fileIn = self._filesIn[folderHR]
            # print("Openning file: ", fileIn)
            rootIn[folderHR] = ROOT.TFile.Open(fileIn, "READ")
        
        # Open output file
        tmpFile = self._fileOut.replace(".root", "__ALL__" + cutName + "_" + variableName + ".root")
        outFile = ROOT.TFile(tmpFile, "RECREATE")
        # create the folder if it does not exist
        outFile.mkdir(folder_name)
        outFile.cd(folder_name)

        # loop over samples
        for sampleName, sample in samples.items():

            print("        sample: ", sampleName)                 

            histos_to_be_summed = []
            #rootIn = {}
            ## loop over years and copy nominals
            for folderHR in self._filesIn.keys():
                histos_to_be_summed.append( rootIn[folderHR].Get(folder_name + "/histo_" + sampleName) )

            # print (" start adding ... ")
            # Clean the list to make sure we only look at valid ROOT objects
            histos_to_be_summed = [h for h in histos_to_be_summed if h and h.GetName()]

            if not histos_to_be_summed:
                print(f"Warning: No valid histograms found to sum for this combination. Skipping...")
                return None # Or whatever default value process_cut_variable is expected to return

            summed_histo = histos_to_be_summed[0].Clone()

            # print ("type = ", type(summed_histo))
            # print (" the [0] is : ", summed_histo.GetName())
            
            for hh in histos_to_be_summed[1:] :  # skip first one
                summed_histo.Add(hh)

            # print (" now write: ", summed_histo.GetName())
            summed_histo.Write()

            #
            # Now let's handle the nuisances
            #

            # loop over nuisances
            for nuisanceName, nuisance in new_list_of_nuisances.items():

                histos_up_to_be_summed = []
                histos_down_to_be_summed = []

                histos_up_to_be_summed_weights = []
                histos_down_to_be_summed_weights = []

                #
                # if the combined nuisance type is lnN, don't touch anything, nothing to be done on histograms level
                #
                if nuisance['type'] == 'lnN' :
                    continue

                if nuisanceName == "stat":
                    continue
        
                if "type" in nuisance.keys() and (nuisance["type"] == "rateParam" or nuisance["type"] == "lnU"):
                    continue

                if 'name' in nuisance.keys() :

                    if "samples" in nuisance.keys() and sampleName not in nuisance["samples"].keys() :
                        continue

                    nameTemp     = 'histo_' + str(sampleName)
                    nameTempUp   = 'histo_' + str(sampleName) + '_' + (nuisance['name']) + 'Up'
                    nameTempDown = 'histo_' + str(sampleName) + '_' + (nuisance['name']) + 'Down'

                    # print ("nuisanceName = ", nuisanceName)
                    #print ("   --> nuisance = ", nuisance)

                    for folderHR in self._filesIn.keys():
                        
                        histo_up, histo_do, histoW_up, histoW_do, nameTempUp, nameTempDown = self.getVariedHistos(folderHR, folder_name, rootIn[folderHR], sampleName, nuisanceName, nuisance, allKeys[folderHR], extra="CMS_")
                        histos_up_to_be_summed.append(histo_up)
                        histos_down_to_be_summed.append(histo_do)
                        histos_up_to_be_summed_weights.append(histoW_up)
                        histos_down_to_be_summed_weights.append(histoW_do)
                else:
                    # print("nuisance ", nuisanceName, " has no name key, skipping it for histograms merging")
                    continue

                #
                # if the nuisance has NO effect on a sample, the histograms are not even created, thus it's not possible to merge them
                #                
# Ensure we only keep valid ROOT histograms and track their corresponding weights
                valid_up_data = [
                    (h, w) for h, w in zip(histos_up_to_be_summed, histos_up_to_be_summed_weights)
                    if h and hasattr(h, "GetName") and h.GetName()
                ]
                valid_down_data = [
                    (h, w) for h, w in zip(histos_down_to_be_summed, histos_down_to_be_summed_weights)
                    if h and hasattr(h, "GetName") and h.GetName()
                ]

                if len(valid_up_data) >= 1 and len(valid_down_data) >= 1:

                    # Process UP variations
                    summed_up_histo = valid_up_data[0][0].Clone()
                    summed_up_histo.Scale(valid_up_data[0][1])
                    
                    for hh, weight in valid_up_data[1:]:
                        summed_up_histo.Add(hh, weight)
                        
                    summed_up_histo.SetName(nameTempUp)
                    summed_up_histo.Write()

                    # Process DOWN variations
                    summed_down_histo = valid_down_data[0][0].Clone()
                    summed_down_histo.Scale(valid_down_data[0][1])
                    
                    for hh, weight in valid_down_data[1:]:
                        summed_down_histo.Add(hh, weight)
                        
                    summed_down_histo.SetName(nameTempDown)
                    summed_down_histo.Write()
                else:
                    print(f"Warning: Nuisance {nuisanceName} missing valid histograms for sample {sampleName}. Skipping...")

        outFile.Close()
        for key in rootIn.keys() :
            rootIn[key].Close()

        return True

    # _____________________________________________________________________________
    def merge(
        self,
        tag,
        variables,
        cuts,
        samples,
        nuisances,
        foldersToMerge,
        foldersToMergeNuisancesFiles,
        nJobs=10,
        onlyCut=None,
        onlyVar=None,
        doSubmit=False
    ):
        
        print ("merge:: variables = ", variables)

        #
        # expand cuts, unrolling the categories
        #
        new_cuts = {}
        for k, j in cuts.items():
          if isinstance(cuts[k], dict) and "categories" in cuts[k].keys():
              for cat in cuts[k]['categories']:
                # cuts.append(k+'_'+cat)
                new_cuts[k+'_'+cat] = {}
          else :
            new_cuts[k] = {}
        print ("cuts = ", cuts)
        print ("new_cuts = ", new_cuts)
        cuts = new_cuts     
        new_list_of_nuisances = nuisances

        #
        # Get all the samples from all the years. This is needed for the definition of the nuisances
        #
        foldersToMergeSamplesFiles = {
           k : os.path.join(p["folder"], 'samples.py') for k, p in foldersToMerge.items()
        }
        print ("foldersToMergeSamplesFiles   = ", foldersToMergeSamplesFiles)

        #
        # get all the niusances from all the years
        #

        for folderHR, year_nuisances in foldersToMergeNuisancesFiles.items() :
            year_samples = foldersToMergeSamplesFiles[folderHR]
            # print ("year_samples = ", year_samples)
            temp_samples = self.extract_dict(year_samples, "samples")
            # print ("temp_samples = ", temp_samples)
            # print ("year_nuisances = ", year_nuisances)
            nuisances = self.extract_dict(year_nuisances, "nuisances", temp_samples)
            self.all_nuisances[folderHR] = nuisances

        # print ("all_nuisances = ", self.all_nuisances)

        doMerge = False
        if doSubmit:

            fSh = ""
            with open(os.environ['STARTPATH']) as file:
                for i in file.readlines():
                    fSh += i
            fSh += f"cd {os.environ['PWD']} \n"
            fSh += f"cp {os.path.abspath(__file__)} . \n"

            fSub = f"""
universe = vanilla  
executable = condor/mergeTask/$(Folder)/run.sh  
   
arguments = $(Folder) 
    
output = condor/mergeTask/$(Folder)/out.txt   
error  = condor/mergeTask/$(Folder)/err.txt  
log    = condor/mergeTask/$(Folder)/log.txt 
   
request_cpus   = 1  
request_memory = 12GB
request_disk   = 10GB 
requirements = (OpSysAndVer =?= "AlmaLinux9") 
+JobFlavour = "longlunch"

queue 1 Folder in ALLTAGS
"""
            
            allTags = []
            for cutName in cuts:
                for varName, var in variables.items():
                    folder_tag = f"{cutName}_{varName}"
                    folder_path = f"condor/mergeTask/{folder_tag}"
                    os.makedirs(folder_path, exist_ok=True)

                    cmd = f"python mkMergeYears.py --inDir {self.inDir} --outDir {self.outDir} --onlyCut {cutName} --onlyVar {varName} \n"

                    job_fSh = fSh
                    job_fSh = job_fSh + "\n"
                    job_fSh = job_fSh + cmd

                    with open(folder_path + "/run.sh", "w") as file:
                        file.write(job_fSh)

                    os.system("chmod +x " + folder_path + "/run.sh")
                    allTags.append(folder_tag)

            fSub = fSub.replace("ALLTAGS", " ".join(allTags))
            with open("condor_submit.jdl", "w") as file:
                file.write(fSub)

            print("Submit the condor jobs with: \n")
            print("condor_submit condor_submit.jdl")

        elif onlyCut is not None and onlyVar is not None:            
            self.process_cut_variable(onlyCut, onlyVar, samples, new_list_of_nuisances)
        elif nJobs == 1:
            doMerge = True
            for cutName in cuts:
                for varName, var in variables.items():
                    self.process_cut_variable(cutName, varName, samples, new_list_of_nuisances)
        elif nJobs > 1:
            doMerge = True
            with ProcessPoolExecutor(max_workers=nJobs) as executor:
                futures = {
                    executor.submit(self.process_cut_variable, cutName, varName, samples, new_list_of_nuisances): (cutName, varName)
                    for cutName in cuts
                    for varName, var in variables.items()
                }
                for f in as_completed(futures):
                    cutName, varName = futures[f]
                    f.result()  # re-raises exceptions

        if doMerge:
            # Final merge:
            print (" Now merging all the temporary files into the final output file: ", self._fileOut)
            proc = subprocess.Popen(f"hadd -fk {self._fileOut} {self._fileOut.replace('.root', '__ALL__*')}", shell=True)
            proc.wait()
            # Remove temporary files
            if os.path.exists(self._fileOut):
                proc = subprocess.Popen(f"rm {self._fileOut.replace('.root', '__ALL__*')}", shell=True)
                proc.wait()

        return True


def main():
    
    header = """
    ----------------------------------------------------------------------------------------
                                                                                           .
           __  __                      __   __                                             .
          |  \/  | ___ _ __ __ _  ___  \ \ / /__  __ _ _ __ ___                            .
          | |\/| |/ _ \ '__/ _` |/ _ \  \ V / _ \/ _` | '__/ __|                           .
          | |  | |  __/ | | (_| |  __/   | |  __/ (_| | |  \__ \                           .
          |_|  |_|\___|_|  \__, |\___|   |_|\___|\__,_|_|  |___/                           .
                           |___/                                                           .
                                                                                           .
    ----------------------------------------------------------------------------------------
    """
    header = dedent(header)
    print(header)

    parser = defaultParser()
    args = parser.parse_args()
    print ("opt.pycfg    = ", args.pycfg)
    loadDefaultOptions(parser, args.pycfg)
    opt = parser.parse_args()

    global cuts, plot
    configsFolder = "configs"
    ConfigLib.loadLatestPickle(os.path.abspath(configsFolder), globals())
    print(dir())
    print(globals().keys())
    cuts = cuts["cuts"]
    subsamplesmap = utils.flatten_samples(samples)
    categoriesmap = utils.flatten_cuts(cuts)
    outDir = args.outDir
    inDir = args.inDir
    nJobs = args.nJobs
    onlyCut = args.onlyCut
    onlyVar = args.onlyVar
    doSubmit = args.doSubmit
    
    print ("args.tag              = ", tag)
    print ("args.foldersToMerge   = ", opt.foldersToMerge)     

    foldersToMergeNuisancesFiles = {
        k : os.path.join(p["folder"], 'nuisances.py') for k, p in opt.foldersToMerge.items()
    }
    print ("foldersToMergeNuisancesFiles   = ", foldersToMergeNuisancesFiles)

    factory = MergerFactory(tag, inDir, outDir, opt.foldersToMerge)
    factory.merge(
       tag,
       variables,
       cuts,
       samples,
       nuisances,
       opt.foldersToMerge,
       foldersToMergeNuisancesFiles,
       nJobs,
       onlyCut,
       onlyVar,
       doSubmit
    )       

    exit()

if __name__ == "__main__":
    main()