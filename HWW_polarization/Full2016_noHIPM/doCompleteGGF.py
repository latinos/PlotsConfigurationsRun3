#!/usr/bin/env python
import sys

import ROOT
import uproot

import optparse
import collections
import os.path
import shutil


ROOT.gROOT.SetBatch(True)

argv = sys.argv
sys.argv = argv[:1]

global cuts, plot
from mkShapesRDF.shapeAnalysis.ConfigLib import ConfigLib
configsFolder = "configs"
ConfigLib.loadLatestPickle(os.path.abspath(configsFolder), globals())
print(dir())
print(globals().keys())


cuts = cuts["cuts"]
inputFile = outputFolder + "/" + outputFile

ROOT.TH1.SetDefaultSumw2(True)

import mkShapesRDF.shapeAnalysis.latinos.LatinosUtils as utils

subsamplesmap = utils.flatten_samples(samples)
categoriesmap = utils.flatten_cuts(cuts)

outputFile = "/eos/user/s/sblancof/MC/rootFiles/mkShapes__WW_2016_postVFP_complete.root"


print("Start computation")

df2 = uproot.open("/eos/user/s/sblancof/MC/rootFiles/mkShapes__WW_2016_postVFP__ALL__ggH_gWW_Int.root")
print("\n")
print("Get new interference histograms")
print("\n")
for cutName in cuts:
    print(cutName)
    for varName in variables:

        #print(varName)
        
        inFile = ROOT.TFile("/eos/user/s/sblancof/MC/rootFiles/mkShapes__WW_2016_postVFP__ALL__ggH_gWW_Int.root")
        outFile = ROOT.TFile(outputFile, "UPDATE")
        outFile.cd(cutName+"/"+varName)

        sampleName = "ggH_gWW_Int"
        new_hist_in = inFile.Get(cutName+"/"+varName+"/histo_"+sampleName)
        new_hist_in.Clone("histo_"+sampleName).Write()

        fileKeys = df2[cutName+"/"+varName].keys()
        
        for nuisanceName in nuisances:
        
            if nuisances[nuisanceName]["type"]!="shape":
                continue

            if "ggH_gWW_Int" not in nuisances[nuisanceName]["samples"]:
                continue

            if "histo_"+sampleName+"_"+nuisances[nuisanceName]["name"]+"Up;1" not in fileKeys:
                continue

            #print(nuisanceName)
            #print(cutName+"/"+varName+"/histo_"+sampleName+"_"+nuisances[nuisanceName]["name"]+"Up")

            new_hist_up = inFile.Get(cutName+"/"+varName+"/histo_"+sampleName+"_"+nuisances[nuisanceName]["name"]+"Up")
            new_hist_do = inFile.Get(cutName+"/"+varName+"/histo_"+sampleName+"_"+nuisances[nuisanceName]["name"]+"Down")

            new_hist_up.Clone("histo_"+sampleName+"_"+nuisances[nuisanceName]["name"]+"Up").Write()
            new_hist_do.Clone("histo_"+sampleName+"_"+nuisances[nuisanceName]["name"]+"Down").Write()

            del new_hist_up
            del new_hist_do

        del new_hist_in
        
        inFile.Close()
        outFile.Close()

print("\n")
print("\n")

df2.close()

df = uproot.open(outputFile)

print("JER and MET not correctly transmitted to TOP and DYTT!!!!!!!!")
variableNames = ["events", "Ctot"]
for cutName in ["hww2l2v_13TeV_top_0j","hww2l2v_13TeV_top_1j","hww2l2v_13TeV_top_2j",
                "hww2l2v_13TeV_dytt_0j","hww2l2v_13TeV_dytt_1j","hww2l2v_13TeV_dytt_2j",
                "hww2l2v_13TeV_ss_Inc","hww2l2v_13TeV_ss_0j","hww2l2v_13TeV_ss_1j","hww2l2v_13TeV_ss_2j",
                "hww2l2v_13TeV_sr_0j_pt2lt20","hww2l2v_13TeV_sr_0j_pt2gt20","hww2l2v_13TeV_sr_1j_pt2lt20","hww2l2v_13TeV_sr_1j_pt2gt20","hww2l2v_13TeV_sr_2j","hww2l2v_13TeV_sr_2j_vbf"]:
    for varName in variables:
        print(varName)
        inFile = ROOT.TFile(outputFile, "UPDATE")
        inFile.cd(cutName+"/"+varName)
        for sampleName in samples:
            if sampleName in ["DATA", "Fake"]:
                continue
            
            #print(sampleName)
            for nuisanceName in nuisances:
                if ("JER"!=nuisanceName and "met"!=nuisanceName):
                    continue

                #print("histo_"+sampleName+"_"+nuisances[nuisanceName]["name"]+"Up;1")
                if "histo_"+sampleName+"_"+nuisances[nuisanceName]["name"]+"Up;1" in df[cutName+"/"+varName].keys():
                    #print("skipped!")
                    continue
                
                hist = inFile.Get(cutName+"/"+varName+"/histo_"+sampleName)
                new_hist = hist
                
                new_hist.Clone("histo_"+sampleName+"_"+nuisances[nuisanceName]["name"]+"Up").Write()
                new_hist.Clone("histo_"+sampleName+"_"+nuisances[nuisanceName]["name"]+"Down").Write()
                
                del new_hist
                del hist
        inFile.Close()
                        
print("Fixed!!!")


print("Now create ggToWW and qqToWW")

for cutName in cuts:
    print(cutName + "<------")
    for variableName in variables:
        print("    -->" + variableName)

        inFile = ROOT.TFile(outputFile, "UPDATE")
        inFile.cd(cutName+"/"+variableName)
        
        #### Nominals
        hist_ggH = inFile.Get(cutName+"/"+variableName+"/histo_ggH_hww")
        hist_ggWW = inFile.Get(cutName+"/"+variableName+"/histo_ggWW")
        hist_ggInt = inFile.Get(cutName+"/"+variableName+"/histo_ggH_gWW_Int")
        
        new_hist_gg = hist_ggH + hist_ggWW + hist_ggInt
        new_hist_ggWW = hist_ggWW + hist_ggInt
        
        hist_qqH = inFile.Get(cutName+"/"+variableName+"/histo_qqH_hww")
        hist_qqWW = inFile.Get(cutName+"/"+variableName+"/histo_WWewk")
        hist_qqInt = inFile.Get(cutName+"/"+variableName+"/histo_qqH_qqWW_Int")
        
        new_hist_qq = hist_qqH + hist_qqWW + hist_qqInt
        new_hist_qqWW = hist_qqWW + hist_qqInt
        
        new_hist_gg.Clone("histo_ggToWW").Write()
        new_hist_qq.Clone("histo_qqToWW").Write()

        new_hist_ggWW.Clone("histo_ggWW_si").Write()
        new_hist_qqWW.Clone("histo_WWewk_si").Write()
        
        for nuisanceName in nuisances:

            skipNuisance = False
            #if ("event" in variableName) and ("hww2l2v_13TeV_top" in cutName or "hww2l2v_13TeV_dytt" in cutName) and ("JER"==nuisanceName or "met"==nuisanceName):
            #    skipNuisance = True
            #
            #if ("event" in variableName) and ("hww2l2v_13TeV_dytt" in cutName) and ("JES" in nuisanceName):
            #    skipNuisance = True
            
            if skipNuisance:
                
                new_hist_gg_up = new_hist_gg
                new_hist_gg_do = new_hist_gg

                new_hist_gg_up.Clone("histo_ggToWW_"+nuisances[nuisanceName]["name"]+"Up").Write()
                new_hist_gg_do.Clone("histo_ggToWW_"+nuisances[nuisanceName]["name"]+"Down").Write()

                new_hist_qq_up = new_hist_qq
                new_hist_qq_do = new_hist_qq
                
                new_hist_qq_up.Clone("histo_qqToWW_"+nuisances[nuisanceName]["name"]+"Up").Write()
                new_hist_qq_do.Clone("histo_qqToWW_"+nuisances[nuisanceName]["name"]+"Down").Write()

                continue
                
            #print(nuisanceName)
            #print(nuisances[nuisanceName])
            
            doggH = False
            doggWW = False
            doggInt = False
            
            doqqH = False
            doqqWW = False
            doqqInt = False
            
            if nuisances[nuisanceName]["type"]!="shape":
                continue
            
            if "ggH_hww" in nuisances[nuisanceName]["samples"]:
                doggH = True
                
            if "qqH_hww" in nuisances[nuisanceName]["samples"]:
                doqqH = True
                
            if "ggWW" in nuisances[nuisanceName]["samples"]:
                doggWW = True

            if "ggH_gWW_Int" in nuisances[nuisanceName]["samples"]:
                doggInt = True

            if "WWewk" in nuisances[nuisanceName]["samples"]:
                doqqWW = True

            if "qqH_qqWW_Int" in nuisances[nuisanceName]["samples"]:
                doqqInt = True

                
            if (doggH and doggWW and doggInt and not skipNuisance):
                hist_ggH_up = inFile.Get(cutName+"/"+variableName+"/histo_ggH_hww_"+nuisances[nuisanceName]["name"]+"Up")
                hist_ggH_do = inFile.Get(cutName+"/"+variableName+"/histo_ggH_hww_"+nuisances[nuisanceName]["name"]+"Down")
                
                hist_ggWW_up = inFile.Get(cutName+"/"+variableName+"/histo_ggWW_"+nuisances[nuisanceName]["name"]+"Up")
                hist_ggWW_do = inFile.Get(cutName+"/"+variableName+"/histo_ggWW_"+nuisances[nuisanceName]["name"]+"Down")

                hist_ggInt_up = inFile.Get(cutName+"/"+variableName+"/histo_ggH_gWW_Int_"+nuisances[nuisanceName]["name"]+"Up")
                hist_ggInt_do = inFile.Get(cutName+"/"+variableName+"/histo_ggH_gWW_Int_"+nuisances[nuisanceName]["name"]+"Down")

                new_hist_gg_up = hist_ggH_up.Clone() + hist_ggWW_up.Clone() + hist_ggInt_up.Clone()
                new_hist_gg_do = hist_ggH_do.Clone() + hist_ggWW_do.Clone() + hist_ggInt_do.Clone()

                new_hist_ggWW_up = hist_ggWW_up + hist_ggInt
                new_hist_ggWW_do = hist_ggWW_do + hist_ggInt

                new_hist_gg_up.Clone("histo_ggToWW_"+nuisances[nuisanceName]["name"]+"Up").Write()
                new_hist_gg_do.Clone("histo_ggToWW_"+nuisances[nuisanceName]["name"]+"Down").Write()

                new_hist_ggWW_up.Clone("histo_ggWW_si_"+nuisances[nuisanceName]["name"]+"Up").Write()
                new_hist_ggWW_do.Clone("histo_ggWW_si_"+nuisances[nuisanceName]["name"]+"Down").Write()

                del new_hist_gg_up
                del new_hist_gg_do
                del new_hist_ggWW_up
                del new_hist_ggWW_do
                
            elif (doggH and doggWW and not skipNuisance):

                hist_ggH_up = inFile.Get(cutName+"/"+variableName+"/histo_ggH_hww_"+nuisances[nuisanceName]["name"]+"Up")
                hist_ggH_do = inFile.Get(cutName+"/"+variableName+"/histo_ggH_hww_"+nuisances[nuisanceName]["name"]+"Down")

                hist_ggWW_up = inFile.Get(cutName+"/"+variableName+"/histo_ggWW_"+nuisances[nuisanceName]["name"]+"Up")
                hist_ggWW_do = inFile.Get(cutName+"/"+variableName+"/histo_ggWW_"+nuisances[nuisanceName]["name"]+"Down")

                new_hist_gg_up = hist_ggH_up.Clone() + hist_ggWW_up.Clone() + hist_ggInt.Clone()
                new_hist_gg_do = hist_ggH_do.Clone() + hist_ggWW_do.Clone() + hist_ggInt.Clone()

                new_hist_gg_up.Clone("histo_ggToWW_"+nuisances[nuisanceName]["name"]+"Up").Write()
                new_hist_gg_do.Clone("histo_ggToWW_"+nuisances[nuisanceName]["name"]+"Down").Write()

                new_hist_ggWW_up = hist_ggWW_up + hist_ggInt
                new_hist_ggWW_do = hist_ggWW_do + hist_ggInt

                new_hist_ggWW_up.Clone("histo_ggWW_si_"+nuisances[nuisanceName]["name"]+"Up").Write()
                new_hist_ggWW_do.Clone("histo_ggWW_si_"+nuisances[nuisanceName]["name"]+"Down").Write()

                del new_hist_ggWW_up
                del new_hist_ggWW_do

                del new_hist_gg_up
                del new_hist_gg_do
                
            elif (doggH and not skipNuisance):

                hist_ggH_up = inFile.Get(cutName+"/"+variableName+"/histo_ggH_hww_"+nuisances[nuisanceName]["name"]+"Up")
                hist_ggH_do = inFile.Get(cutName+"/"+variableName+"/histo_ggH_hww_"+nuisances[nuisanceName]["name"]+"Down")

                new_hist_gg_up = hist_ggH_up.Clone() + hist_ggWW.Clone() + hist_ggInt.Clone()
                new_hist_gg_do = hist_ggH_do.Clone() + hist_ggWW.Clone() + hist_ggInt.Clone()

                new_hist_gg_up.Clone("histo_ggToWW_"+nuisances[nuisanceName]["name"]+"Up").Write()
                new_hist_gg_do.Clone("histo_ggToWW_"+nuisances[nuisanceName]["name"]+"Down").Write()

                del new_hist_gg_up
                del new_hist_gg_do
                
            elif (doggWW and not skipNuisance):

                hist_ggWW_up = inFile.Get(cutName+"/"+variableName+"/histo_ggWW_"+nuisances[nuisanceName]["name"]+"Up")
                hist_ggWW_do = inFile.Get(cutName+"/"+variableName+"/histo_ggWW_"+nuisances[nuisanceName]["name"]+"Down")

                new_hist_gg_up = hist_ggH.Clone() + hist_ggWW_up.Clone() + hist_ggInt.Clone()
                new_hist_gg_do = hist_ggH.Clone() + hist_ggWW_do.Clone() + hist_ggInt.Clone()

                new_hist_gg_up.Clone("histo_ggToWW_"+nuisances[nuisanceName]["name"]+"Up").Write()
                new_hist_gg_do.Clone("histo_ggToWW_"+nuisances[nuisanceName]["name"]+"Down").Write()

                new_hist_ggWW_up = hist_ggWW_up + hist_ggInt
                new_hist_ggWW_do = hist_ggWW_do + hist_ggInt

                new_hist_ggWW_up.Clone("histo_ggWW_si_"+nuisances[nuisanceName]["name"]+"Up").Write()
                new_hist_ggWW_do.Clone("histo_ggWW_si_"+nuisances[nuisanceName]["name"]+"Down").Write()

                del new_hist_ggWW_up
                del new_hist_ggWW_do

                del new_hist_gg_up
                del new_hist_gg_do
                
            ##### qqH VBF ------------------------
                
            if (doqqH and doqqWW and doqqInt):
                hist_qqH_up = inFile.Get(cutName+"/"+variableName+"/histo_qqH_hww_"+nuisances[nuisanceName]["name"]+"Up")
                hist_qqH_do = inFile.Get(cutName+"/"+variableName+"/histo_qqH_hww_"+nuisances[nuisanceName]["name"]+"Down")

                hist_qqWW_up = inFile.Get(cutName+"/"+variableName+"/histo_WWewk_"+nuisances[nuisanceName]["name"]+"Up")
                hist_qqWW_do = inFile.Get(cutName+"/"+variableName+"/histo_WWewk_"+nuisances[nuisanceName]["name"]+"Down")

                hist_qqInt_up = inFile.Get(cutName+"/"+variableName+"/histo_qqH_qqWW_Int_"+nuisances[nuisanceName]["name"]+"Up")
                hist_qqInt_do = inFile.Get(cutName+"/"+variableName+"/histo_qqH_qqWW_Int_"+nuisances[nuisanceName]["name"]+"Down")

                new_hist_qq_up = hist_qqH_up.Clone() + hist_qqWW_up.Clone() + hist_qqInt_up.Clone()
                new_hist_qq_do = hist_qqH_do.Clone() + hist_qqWW_do.Clone() + hist_qqInt_do.Clone()

                new_hist_qq_up.Clone("histo_qqToWW_"+nuisances[nuisanceName]["name"]+"Up").Write()
                new_hist_qq_do.Clone("histo_qqToWW_"+nuisances[nuisanceName]["name"]+"Down").Write()

                new_hist_qqWW_up = hist_qqWW_up + hist_qqInt
                new_hist_qqWW_do = hist_qqWW_do + hist_qqInt

                new_hist_qqWW_up.Clone("histo_WWewk_si_"+nuisances[nuisanceName]["name"]+"Up").Write()
                new_hist_qqWW_do.Clone("histo_WWewk_si_"+nuisances[nuisanceName]["name"]+"Down").Write()

                del new_hist_qqWW_up
                del new_hist_qqWW_do

                del new_hist_qq_up
                del new_hist_qq_do
                
            elif (doqqH and doqqWW):

                hist_qqH_up = inFile.Get(cutName+"/"+variableName+"/histo_qqH_hww_"+nuisances[nuisanceName]["name"]+"Up")
                hist_qqH_do = inFile.Get(cutName+"/"+variableName+"/histo_qqH_hww_"+nuisances[nuisanceName]["name"]+"Down")

                hist_qqWW_up = inFile.Get(cutName+"/"+variableName+"/histo_WWewk_"+nuisances[nuisanceName]["name"]+"Up")
                hist_qqWW_do = inFile.Get(cutName+"/"+variableName+"/histo_WWewk_"+nuisances[nuisanceName]["name"]+"Down")

                new_hist_qq_up = hist_qqH_up.Clone() + hist_qqWW_up.Clone() + hist_qqInt.Clone()
                new_hist_qq_do = hist_qqH_do.Clone() + hist_qqWW_do.Clone() + hist_qqInt.Clone()

                new_hist_qq_up.Clone("histo_qqToWW_"+nuisances[nuisanceName]["name"]+"Up").Write()
                new_hist_qq_do.Clone("histo_qqToWW_"+nuisances[nuisanceName]["name"]+"Down").Write()

                new_hist_qqWW_up = hist_qqWW_up + hist_qqInt
                new_hist_qqWW_do = hist_qqWW_do + hist_qqInt

                new_hist_qqWW_up.Clone("histo_WWewk_si_"+nuisances[nuisanceName]["name"]+"Up").Write()
                new_hist_qqWW_do.Clone("histo_WWewk_si_"+nuisances[nuisanceName]["name"]+"Down").Write()

                del new_hist_qqWW_up
                del new_hist_qqWW_do
                
                del new_hist_qq_up
                del new_hist_qq_do
                
            elif (doqqH):

                hist_qqH_up = inFile.Get(cutName+"/"+variableName+"/histo_qqH_hww_"+nuisances[nuisanceName]["name"]+"Up")
                hist_qqH_do = inFile.Get(cutName+"/"+variableName+"/histo_qqH_hww_"+nuisances[nuisanceName]["name"]+"Down")

                new_hist_qq_up = hist_qqH_up.Clone() + hist_qqWW.Clone() + hist_qqInt.Clone()
                new_hist_qq_do = hist_qqH_do.Clone() + hist_qqWW.Clone() + hist_qqInt.Clone()

                new_hist_qq_up.Clone("histo_qqToWW_"+nuisances[nuisanceName]["name"]+"Up").Write()
                new_hist_qq_do.Clone("histo_qqToWW_"+nuisances[nuisanceName]["name"]+"Down").Write()

                del new_hist_qq_up
                del new_hist_qq_do
                
            elif (doqqWW):

                hist_qqWW_up = inFile.Get(cutName+"/"+variableName+"/histo_WWewk_"+nuisances[nuisanceName]["name"]+"Up")
                hist_qqWW_do = inFile.Get(cutName+"/"+variableName+"/histo_WWewk_"+nuisances[nuisanceName]["name"]+"Down")

                new_hist_qq_up = hist_qqH.Clone() + hist_qqWW_up.Clone() + hist_qqInt.Clone()
                new_hist_qq_do = hist_qqH.Clone() + hist_qqWW_do.Clone() + hist_qqInt.Clone()

                new_hist_qq_up.Clone("histo_qqToWW_"+nuisances[nuisanceName]["name"]+"Up").Write()
                new_hist_qq_do.Clone("histo_qqToWW_"+nuisances[nuisanceName]["name"]+"Down").Write()

                new_hist_qqWW_up = hist_qqWW_up + hist_qqInt
                new_hist_qqWW_do = hist_qqWW_do + hist_qqInt

                new_hist_qqWW_up.Clone("histo_WWewk_si_"+nuisances[nuisanceName]["name"]+"Up").Write()
                new_hist_qqWW_do.Clone("histo_WWewk_si_"+nuisances[nuisanceName]["name"]+"Down").Write()

                del new_hist_qqWW_up
                del new_hist_qqWW_do
                
                del new_hist_qq_up
                del new_hist_qq_do

        del new_hist_gg
        del new_hist_qq
        inFile.Close()
        
print("Finished first loop: Definition of histograms")
#print(new_histos)
#print("Start saving")

#inFile.cd()

#for new_name in new_histos:
#    print(new_name)
#    new_histos[new_name].Clone(new_name).Write()


