#!/usr/bin/env python
import ROOT
import uproot
import pandas as pd
import numpy as np
import awkward as ak
import os
import subprocess

import argparse
import sys
import time
import json
from pathlib import Path

ROOT.gROOT.SetBatch(True)
ROOT.TH1.SetDefaultSumw2(True)

samples = {
    "2016UL": {
        "signals" : [
            "GluGluHToWWTo2L2Nu_M125",
            "VBFHToWWTo2L2Nu_M125",
        ],
        "bkg": [
            "WWTo2L2Nu",
            "DYJetsToTT_MuEle_M-50",
            "TTTo2L2Nu",
        ],
        "path": '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer20UL16_106x_nAODv9_HIPM_Full2016v9/MCl1loose2016v9__MCCorr2016v9NoJERInHorn__l2tightOR2016v9',
        "melaPath": '/eos/user/s/sblancof/MC/Summer20UL16_106x_nAODv9_HIPM_Full2016v9/MCl1loose2016v9__MCCorr2016v9NoJERInHorn__l2tightOR2016v9__melaWeights',
    },
    "2016UL_noHIPM": {
        "signals" : [
            "GluGluHToWWTo2L2Nu_M125",
            "VBFHToWWTo2L2Nu_M125",
        ],
        "bkg": [
            "WWTo2L2Nu",
            "DYJetsToTT_MuEle_M-50",
            "TTTo2L2Nu",
        ],
        "path": '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer20UL16_106x_nAODv9_noHIPM_Full2016v9/MCl1loose2016v9__MCCorr2016v9NoJERInHorn__l2tightOR2016v9',
        "melaPath": '/eos/user/s/sblancof/MC/Summer20UL16_106x_nAODv9_noHIPM_Full2016v9/MCl1loose2016v9__MCCorr2016v9NoJERInHorn__l2tightOR2016v9__melaWeights',
    },
    "2017UL": {
        "signals" : [
            "GluGluHToWWTo2L2Nu_M125",
            "VBFHToWWTo2L2Nu_M125",
        ],
        "bkg": [
            "WWTo2L2Nu",
            "DYJetsToTT_MuEle_M-50",
            "TTTo2L2Nu",
        ],
        "path": '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer20UL17_106x_nAODv9_Full2017v9/MCl1loose2017v9__MCCorr2017v9NoJERInHorn__l2tightOR2017v9',
        "melaPath": '/eos/user/s/sblancof/MC/Summer20UL17_106x_nAODv9_Full2017v9/MCl1loose2017v9__MCCorr2017v9NoJERInHorn__l2tightOR2017v9__melaWeights',
    },
    "2018UL": {
        "signals" : [
            "GluGluHToWWTo2L2Nu_M125",
            "VBFHToWWTo2L2Nu_M125",
        ],
        "bkg": [
            "WWTo2L2Nu",
            "DYJetsToTT_MuEle_M-50",
            "TTTo2L2Nu",
        ],
        "path": '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer20UL18_106x_nAODv9_Full2018v9/MCl1loose2018v9__MCCorr2018v9NoJERInHorn__l2tightOR2018v9',
        "melaPath": '/eos/user/s/sblancof/MC/Summer20UL18_106x_nAODv9_Full2018v9/MCl1loose2018v9__MCCorr2018v9NoJERInHorn__l2tightOR2018v9__melaWeights',
    },
    "2022": {
        "signals" : [
            "GluGluHToWWTo2L2Nu_M125",
            "VBFHToWWTo2L2Nu_M125",
        ],
        "bkg": [
            "WWTo2L2Nu",
            "DYto2L-2Jets_MLL-50",
            "TTTo2L2Nu",
        ],
        "path": '/eos/cms/store/group/phys_higgs/cmshww/calderon/HWWNano/Summer22_130x_nAODv12_Full2022v12/MCl2loose2022v12__MCCorr2022v12JetScaling__sblancof__l2tight',
        "melaPath": '/eos/cms/store/group/phys_higgs/cmshww/calderon/HWWNano/Summer22_130x_nAODv12_Full2022v12/MCl2loose2022v12__MCCorr2022v12JetScaling__sblancof__l2tight__melaWeights',
    },
    "2022EE": {
        "signals" : [
            "GluGluHToWWTo2L2Nu_M125",
            "VBFHToWWTo2L2Nu_M125",
        ],
        "bkg": [
            "WWTo2L2Nu",
            "DYto2L-2Jets_MLL-50",
            "TTTo2L2Nu",
        ],
        "path": '/eos/cms/store/group/phys_higgs/cmshww/calderon/HWWNano/Summer22EE_130x_nAODv12_Full2022v12/MCl2loose2022EEv12__MCCorr2022EEv12JetScaling__sblancof__l2tight',
        "melaPath": '/eos/user/s/sblancof/MC/Summer22EE_130x_nAODv12_Full2022v12/MCl2loose2022EEv12__MCCorr2022EEv12JetScaling__sblancof__l2tight__melaWeights',
    },
    "2023": {
        "signals" : [
            "GluGluHToWWTo2L2Nu_M125",
            "VBFHToWWTo2L2Nu_M125",
        ],
        "bkg": [
            "WWTo2L2Nu",
            "DYto2L-2Jets_MLL-50",
            "TTTo2L2Nu",
        ],
        "path": '/eos/cms/store/group/phys_higgs/cmshww/calderon/HWWNano/Summer23_130x_nAODv12_Full2023v12/MCl2loose2023v12__MCCorr2023v12JetScaling__sblancof__l2tight',
        "melaPath": '/eos/user/s/sblancof/MC/Summer23_130x_nAODv12_Full2023v12/MCl2loose2023v12__MCCorr2023v12JetScaling__sblancof__l2tight__melaWeights',
    },
    "2023BPix": {
        "signals" : [
            "GluGluHToWWTo2L2Nu_M125",
            "VBFHToWWTo2L2Nu_M125",
        ],
        "bkg": [
            "WWTo2L2Nu",
            "DYto2L-2Jets_MLL-50",
            "TTTo2L2Nu",
        ],
        "path": '/eos/cms/store/group/phys_higgs/cmshww/calderon/HWWNano/Summer23BPix_130x_nAODv12_Full2023BPixv12/MCl2loose2023BPixv12__MCCorr2023BPixv12JetScaling__sblancof__l2tight',
        "melaPath": '/eos/user/s/sblancof/MC/Summer23BPix_130x_nAODv12_Full2023BPixv12/MCl2loose2023BPixv12__MCCorr2023BPixv12JetScaling__sblancof__l2tight__melaWeights',
    },
    "2024": {
        "signals" : [
            "GluGluHToWWTo2L2Nu_M125",
            "VBFHToWWTo2L2Nu_M125",
        ],
        "bkg": [
            "WWTo2L2Nu",
            "DYto2L-2Jets_MLL-50",
            "TTTo2L2Nu",
        ],
        "path": '/eos/cms/store/group/phys_higgs/cmshww/calderon/HWWNano/Summer24_150x_nAODv15_Full2024v15/MCl2loose2024v15__MCCorr2024v15__JERFrom23BPix__l2tight',
        "melaPath": '/eos/user/s/sblancof/MC/Summer24_150x_nAODv15_Full2024v15/MCl2loose2024v15__MCCorr2024v15__JERFrom23BPix__l2tight__melaWeights',
    },
}

def defaultParser():
    parser = argparse.ArgumentParser(add_help=False)

    def list_of_strings(arg):
        return arg.split(',')
    
    parser.add_argument(
        "-P",
        "--prefix",
        type=str,
        help="prefix for the job output",
	required=False,
	default="",
    )
    
    parser.add_argument(
        "-i",
        "--inDir",
        type=str,
        help="prefix for the job input",
        required=False,
        default="",
    )

    parser.add_argument(
        "-T",
        "--sample",
        type=str,
        help="sample Name",
        required=False,
        default="",
    )

    parser.add_argument(
        "-all",
        "--allYears",
        help="Do all years from joblist.txt",
        required=False,
        action='store_true',
        default=False,
    )

    return parser


def search_files(dataset):
    """
    Look for input files
    """
    redirector = "root://cms-xrd-global.cern.ch/"
    def findFilesInDAS(path):
        procString = f'dasgoclient --query="file dataset={path}"'
        proc = subprocess.Popen(
            procString,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = proc.communicate()
        out = out.decode("utf-8")
        out = out.split("\n")
        files = [redirector + item for item in list(filter(lambda k: k.strip() != "", out))]
        
        err = err.decode("utf-8")
        if len(err) != 0:
            print("There were some errors in retrieving file:")
            print(err)
            sys.exit()

        return files

    def findFilesInEOS(path):
        cmd = "find {} -wholename '*/*.root'".format(path)
        fnames = subprocess.check_output(cmd, shell=True).strip().split(b'\n')
        files = [fname.decode('ascii') for fname in fnames]
        return files
    
    total_files = []
    if dataset.startswith("/eos"):
        total_files += findFilesInEOS(dataset)
    else:
        total_files += findFilesInDAS(dataset)

    print(total_files)
    return total_files


def build_condor_submit(inDir="", sampleName="", prefix="", label=""):
    mypath = os.path.abspath(os.getcwd())
    fSh = ""
    with open("/afs/cern.ch/work/s/sblancof/private/Run2Analysis/sendEOSJobs/start.sh") as file:
        for i in file.readlines():
            fSh += i

    #fSh += "cd " + mypath + " \n"
    fSh += f"cd {os.environ['TMPDIR']} \n"
    fSh += "cp " + mypath + "/RecoRandomForest.py .\n"
    
    #fSh += "cp -r /eos/user/s/sblancof/Run2Analysis/mkShapesRDF/JHUGenMELA/MELA/data/Pdfdata .\n"
    #fSh += "cp /eos/user/s/sblancof/Run2Analysis/mkShapesRDF/JHUGenMELA/MELA/data/input.DAT .\n"
    #fSh += "cp /eos/user/s/sblancof/Run2Analysis/mkShapesRDF/JHUGenMELA/MELA/data/process.DAT .\n"
    #fSh += "cp /eos/user/s/sblancof/Run2Analysis/mkShapesRDF/JHUGenMELA/MELA/data/br.sm1 .\n"
    #fSh += "cp /eos/user/s/sblancof/Run2Analysis/mkShapesRDF/JHUGenMELA/MELA/data/br.sm2 .\n"
    #fSh += "pushd /eos/user/s/sblancof/Run2Analysis/mkShapesRDF/MELACalc/JHUGen-v757.3/JHUGenMELA \n"
    #fSh += "./setup.sh \n"
    #fSh += "eval $(./setup.sh env) \n"
    #fSh += "popd \n"

    #fSh += "cp -r /eos/user/s/sblancof/Run2Analysis/mkShapesRDF/JHUGenMELA/MELA/data/Pdfdata .\n"
    #fSh += "cp /eos/user/s/sblancof/Run2Analysis/mkShapesRDF/JHUGenMELA/MELA/data/input.DAT .\n"
    #fSh += "cp /eos/user/s/sblancof/Run2Analysis/mkShapesRDF/JHUGenMELA/MELA/data/process.DAT .\n"
    #fSh += "cp /eos/user/s/sblancof/Run2Analysis/mkShapesRDF/JHUGenMELA/MELA/data/br.sm1 .\n"
    #fSh += "cp /eos/user/s/sblancof/Run2Analysis/mkShapesRDF/JHUGenMELA/MELA/data/br.sm2 .\n"
    fSh += "pushd /eos/user/s/sblancof/Run2Analysis/mkShapesRDF/JHUGenMELA\n"
    fSh += "./setup.sh\n"
    fSh += "eval $(./setup.sh env)\n"
    fSh += "popd\n"
    
    #fSh += "cp -r /eos/user/s/sblancof/Run2Analysis/mkShapesRDF/JHUGenMELA/MELA/data/Pdfdata .\n"
    
    fSh += "export X509_USER_PROXY=/afs/cern.ch/user/s/sblancof/.proxy \n"
    
    condorDir = mypath + "/condor"
    Path(condorDir).mkdir(parents=True, exist_ok=True)

    datasetName = inDir + "nanoLatino_" + sampleName + "__part*.root"
    files_2018 = search_files(datasetName)
    min_length = len(files_2018)

    fSub = f"""
universe = vanilla
executable = condor/$(Folder)/run.sh

arguments = $(Folder)

output = condor/$(Folder)/out.txt
error  = condor/$(Folder)/err.txt
log    = condor/$(Folder)/log.txt

request_cpus   = 1
request_memory = 12GB
request_disk   = 10GB
requirements = (OpSysAndVer =?= "AlmaLinux9")
+JobFlavour = "workday"

queue 1 Folder in ALLTAGS
"""

    allTags = []
    for i in range(min_length):
        folder_tag = files_2018[i].split("/nanoLatino_")[-1].split(".root")[0]
        #folder_tag = label+"job_"+str(i)
        jobDir = condorDir + "/" + folder_tag
        Path(jobDir).mkdir(parents=True, exist_ok=True)
        job_fSh = fSh
        job_fSh = job_fSh + "\n"
        job_fSh = job_fSh + f"python RecoRandomForest.py -i {files_2018[i]} -o {prefix} \n"

        with open(jobDir + "/run.sh", "w") as file:
            file.write(job_fSh)

        os.system("chmod +x " + jobDir + "/run.sh")
        allTags.append(folder_tag)

    fSub = fSub.replace("ALLTAGS", " ".join(allTags))
    with open("condor_submit.jdl", "w") as file:
        file.write(fSub)

    if label!="":
        return allTags        

def main():
    parser = defaultParser()
    args = parser.parse_args()
    
    prefix = args.prefix
    inDir = args.inDir
    sample = args.sample
    doAll = args.allYears
    
    print("Run job builder -------")
    
    if doAll:
        allTags2 = []
        with open('joblist.txt') as file:
            lines = [line.rstrip() for line in file]
            for line in lines:
                inputs = line.split(",")
                print(f"build_condor_submit({inputs[0]}, {inputs[2]}, {inputs[1]}, {inputs[3]+'_'})")
                allTags2 += build_condor_submit(inputs[0], inputs[2], inputs[1], inputs[3]+"_")

                fSub = f"""
universe = vanilla
executable = condor/$(Folder)/run.sh 
      
arguments = $(Folder) 
    
output = condor/$(Folder)/out.txt 
error  = condor/$(Folder)/err.txt
log    = condor/$(Folder)/log.txt
   
request_cpus   = 1 
request_memory = 12GB
request_disk   = 10GB
requirements = (OpSysAndVer =?= "AlmaLinux9") 
+JobFlavour = "workday"
    
queue 1 Folder in ALLTAGS   
"""

                fSub = fSub.replace("ALLTAGS", " ".join(allTags2))
                with open("condor_submit.jdl", "w") as file:
                    file.write(fSub)
                
    else:
        build_condor_submit(inDir,sample,prefix)


if __name__ == '__main__':
    main()
    print("DONE!")




