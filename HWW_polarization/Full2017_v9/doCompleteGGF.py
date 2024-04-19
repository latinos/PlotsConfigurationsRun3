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


outputFile = "/eos/user/s/sblancof/MC/rootFiles/mkShapes__WW_2018_complete.root"

#inFile = ROOT.TFile(outputFile, "UPDATE")
#outFile = ROOT.TFile(outputFile, "RECREATE")

### example 
### hww2l2v_13TeV_WW_2j/detall/histo_ZZ_CMS_scale_m_2017Up
### nuisance: CMS_scale_m_2017

print("Start computation")

#print(nuisances)

#{'name': 'THU_qqH_PTH25', 'skipCMS': 1, 'kind': 'weight', 'type': 'shape', 'samples': {'qqH_hww': ['qqH_PTH25', '2.-qqH_PTH25'], 'qqH_HWLWL': ['qqH_PTH25', '2.-qqH_PTH25'], 'qqH_HWTWT': ['qqH_PTH25', '2.-qqH_PTH25'], 'qqH_HWW_Int': ['qqH_PTH25', '2.-qqH_PTH25'], 'qqH_HWW_TTInt': ['qqH_PTH25', '2.-qqH_PTH25']}}

## Do merge for ggH_hww  /  qqH_hww  /  ggWW  / ggH_gWW_Int  /  qqH_qqWW_Int  / WWewk

#new_histos = {}

#hww2l2v_13TeV_sr_0j
#hww2l2v_13TeV_sr_1j
#hww2l2v_13TeV_sr_2j
#hww2l2v_13TeV_sr_2j_vbf

#hww2l2v_13TeV_sr_BDT95_0j
#hww2l2v_13TeV_sr_BDT95_1j
#hww2l2v_13TeV_sr_BDT95_2j

#hww2l2v_13TeV_sr_BDT95_2j_vbf

#hww2l2v_13TeV_sr_BDT90_0j
#hww2l2v_13TeV_sr_BDT90_1j
#hww2l2v_13TeV_sr_BDT90_2j
#hww2l2v_13TeV_sr_BDT90_2j_vbf

#hww2l2v_13TeV_sr_BDT80_0j
#hww2l2v_13TeV_sr_BDT80_1j
#hww2l2v_13TeV_sr_BDT80_2j
#hww2l2v_13TeV_sr_BDT80_2j_vbf

#hww2l2v_13TeV_sr_RF_bkg_0j
#hww2l2v_13TeV_sr_RF_bkg_1j
#hww2l2v_13TeV_sr_RF_bkg_2j
#hww2l2v_13TeV_sr_RF_bkg_2j_vbf

#hww2l2v_13TeV_sr_RF_Signal_0j
#hww2l2v_13TeV_sr_RF_Signal_1j
#hww2l2v_13TeV_sr_RF_Signal_2j
#hww2l2v_13TeV_sr_RF_Signal_2j_vbf

#hww2l2v_13TeV_top_0j
#hww2l2v_13TeV_top_1j
#hww2l2v_13TeV_top_2j

#hww2l2v_13TeV_dytt_0j
#hww2l2v_13TeV_dytt_1j
#hww2l2v_13TeV_dytt_2j

#hww2l2v_13TeV_WW_0j
#hww2l2v_13TeV_WW_1j
#hww2l2v_13TeV_WW_2j


for cutName in cuts:
    #for cutName in ["hww2l2v_13TeV_sr_BDT95_0j"]:
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
        
        hist_qqH = inFile.Get(cutName+"/"+variableName+"/histo_qqH_hww")
        hist_qqWW = inFile.Get(cutName+"/"+variableName+"/histo_WWewk")
        hist_qqInt = inFile.Get(cutName+"/"+variableName+"/histo_qqH_qqWW_Int")
        
        new_hist_qq = hist_qqH + hist_qqWW + hist_qqInt
        
        #new_histos[cutName+"/"+variableName+"/histo_ggToWW"] = new_hist_gg
        #new_histos[cutName+"/"+variableName+"/histo_qqToWW"] = new_hist_qq
        
        new_hist_gg.Clone("histo_ggToWW").Write()
        new_hist_qq.Clone("histo_qqToWW").Write()
        
        for nuisanceName in nuisances:
            
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

                
            if (doggH and doggWW and doggInt):
                hist_ggH_up = inFile.Get(cutName+"/"+variableName+"/histo_ggH_hww_"+nuisances[nuisanceName]["name"]+"Up")
                hist_ggH_do = inFile.Get(cutName+"/"+variableName+"/histo_ggH_hww_"+nuisances[nuisanceName]["name"]+"Down")
                
                hist_ggWW_up = inFile.Get(cutName+"/"+variableName+"/histo_ggWW_"+nuisances[nuisanceName]["name"]+"Up")
                hist_ggWW_do = inFile.Get(cutName+"/"+variableName+"/histo_ggWW_"+nuisances[nuisanceName]["name"]+"Down")

                hist_ggInt_up = inFile.Get(cutName+"/"+variableName+"/histo_ggH_gWW_Int_"+nuisances[nuisanceName]["name"]+"Up")
                hist_ggInt_do = inFile.Get(cutName+"/"+variableName+"/histo_ggH_gWW_Int_"+nuisances[nuisanceName]["name"]+"Down")

                #print(hist_ggH_up)
                #print(hist_ggH_do)
                #print(hist_ggWW_up)
                #print(hist_ggWW_do)
                #print(hist_ggInt_up)
                #print(hist_ggInt_do)
                
                new_hist_gg_up = hist_ggH_up.Clone() + hist_ggWW_up.Clone() + hist_ggInt_up.Clone()
                new_hist_gg_do = hist_ggH_do.Clone() + hist_ggWW_do.Clone() + hist_ggInt_do.Clone()

                #new_histos[cutName+"/"+variableName+"/histo_ggToWW_"+nuisances[nuisanceName]["name"]+"Up"] = new_hist_gg_up
                #new_histos[cutName+"/"+variableName+"/histo_ggToWW_"+nuisances[nuisanceName]["name"]+"Down"] = new_hist_gg_do

                new_hist_gg_up.Clone("histo_ggToWW_"+nuisances[nuisanceName]["name"]+"Up").Write()
                new_hist_gg_do.Clone("histo_ggToWW_"+nuisances[nuisanceName]["name"]+"Down").Write()

                del new_hist_gg_up
                del new_hist_gg_do
                
            elif (doggH and doggWW):

                hist_ggH_up = inFile.Get(cutName+"/"+variableName+"/histo_ggH_hww_"+nuisances[nuisanceName]["name"]+"Up")
                hist_ggH_do = inFile.Get(cutName+"/"+variableName+"/histo_ggH_hww_"+nuisances[nuisanceName]["name"]+"Down")

                hist_ggWW_up = inFile.Get(cutName+"/"+variableName+"/histo_ggWW_"+nuisances[nuisanceName]["name"]+"Up")
                hist_ggWW_do = inFile.Get(cutName+"/"+variableName+"/histo_ggWW_"+nuisances[nuisanceName]["name"]+"Down")

                new_hist_gg_up = hist_ggH_up.Clone() + hist_ggWW_up.Clone() + hist_ggInt.Clone()
                new_hist_gg_do = hist_ggH_do.Clone() + hist_ggWW_do.Clone() + hist_ggInt.Clone()

                #new_histos[cutName+"/"+variableName+"/histo_ggToWW_"+nuisances[nuisanceName]["name"]+"Up"] = new_hist_gg_up
                #new_histos[cutName+"/"+variableName+"/histo_ggToWW_"+nuisances[nuisanceName]["name"]+"Down"] = new_hist_gg_do

                new_hist_gg_up.Clone("histo_ggToWW_"+nuisances[nuisanceName]["name"]+"Up").Write()
                new_hist_gg_do.Clone("histo_ggToWW_"+nuisances[nuisanceName]["name"]+"Down").Write()

                del new_hist_gg_up
                del new_hist_gg_do
                
            elif (doggH):

                hist_ggH_up = inFile.Get(cutName+"/"+variableName+"/histo_ggH_hww_"+nuisances[nuisanceName]["name"]+"Up")
                hist_ggH_do = inFile.Get(cutName+"/"+variableName+"/histo_ggH_hww_"+nuisances[nuisanceName]["name"]+"Down")

                new_hist_gg_up = hist_ggH_up.Clone() + hist_ggWW.Clone() + hist_ggInt.Clone()
                new_hist_gg_do = hist_ggH_do.Clone() + hist_ggWW.Clone() + hist_ggInt.Clone()

                #new_histos[cutName+"/"+variableName+"/histo_ggToWW_"+nuisances[nuisanceName]["name"]+"Up"] = new_hist_gg_up
                #new_histos[cutName+"/"+variableName+"/histo_ggToWW_"+nuisances[nuisanceName]["name"]+"Down"] = new_hist_gg_do

                new_hist_gg_up.Clone("histo_ggToWW_"+nuisances[nuisanceName]["name"]+"Up").Write()
                new_hist_gg_do.Clone("histo_ggToWW_"+nuisances[nuisanceName]["name"]+"Down").Write()

                del new_hist_gg_up
                del new_hist_gg_do
                
            elif (doggWW):

                hist_ggWW_up = inFile.Get(cutName+"/"+variableName+"/histo_ggWW_"+nuisances[nuisanceName]["name"]+"Up")
                hist_ggWW_do = inFile.Get(cutName+"/"+variableName+"/histo_ggWW_"+nuisances[nuisanceName]["name"]+"Down")

                new_hist_gg_up = hist_ggH.Clone() + hist_ggWW_up.Clone() + hist_ggInt.Clone()
                new_hist_gg_do = hist_ggH.Clone() + hist_ggWW_do.Clone() + hist_ggInt.Clone()

                #new_histos[cutName+"/"+variableName+"/histo_ggToWW_"+nuisances[nuisanceName]["name"]+"Up"] = new_hist_gg_up
                #new_histos[cutName+"/"+variableName+"/histo_ggToWW_"+nuisances[nuisanceName]["name"]+"Down"] = new_hist_gg_do

                new_hist_gg_up.Clone("histo_ggToWW_"+nuisances[nuisanceName]["name"]+"Up").Write()
                new_hist_gg_do.Clone("histo_ggToWW_"+nuisances[nuisanceName]["name"]+"Down").Write()

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

                #new_histos[cutName+"/"+variableName+"/histo_qqToWW_"+nuisances[nuisanceName]["name"]+"Up"] = new_hist_qq_up
                #new_histos[cutName+"/"+variableName+"/histo_qqToWW_"+nuisances[nuisanceName]["name"]+"Down"] = new_hist_qq_do

                new_hist_qq_up.Clone("histo_qqToWW_"+nuisances[nuisanceName]["name"]+"Up").Write()
                new_hist_qq_do.Clone("histo_qqToWW_"+nuisances[nuisanceName]["name"]+"Down").Write()

                del new_hist_qq_up
                del new_hist_qq_do
                
            elif (doqqH and doqqWW):

                hist_qqH_up = inFile.Get(cutName+"/"+variableName+"/histo_qqH_hww_"+nuisances[nuisanceName]["name"]+"Up")
                hist_qqH_do = inFile.Get(cutName+"/"+variableName+"/histo_qqH_hww_"+nuisances[nuisanceName]["name"]+"Down")

                hist_qqWW_up = inFile.Get(cutName+"/"+variableName+"/histo_WWewk_"+nuisances[nuisanceName]["name"]+"Up")
                hist_qqWW_do = inFile.Get(cutName+"/"+variableName+"/histo_WWewk_"+nuisances[nuisanceName]["name"]+"Down")

                new_hist_qq_up = hist_qqH_up.Clone() + hist_qqWW_up.Clone() + hist_qqInt.Clone()
                new_hist_qq_do = hist_qqH_do.Clone() + hist_qqWW_do.Clone() + hist_qqInt.Clone()

                #new_histos[cutName+"/"+variableName+"/histo_qqToWW_"+nuisances[nuisanceName]["name"]+"Up"] = new_hist_qq_up
                #new_histos[cutName+"/"+variableName+"/histo_qqToWW_"+nuisances[nuisanceName]["name"]+"Down"] = new_hist_qq_do

                new_hist_qq_up.Clone("histo_qqToWW_"+nuisances[nuisanceName]["name"]+"Up").Write()
                new_hist_qq_do.Clone("histo_qqToWW_"+nuisances[nuisanceName]["name"]+"Down").Write()

                del new_hist_qq_up
                del new_hist_qq_do
                
            elif (doqqH):

                hist_qqH_up = inFile.Get(cutName+"/"+variableName+"/histo_qqH_hww_"+nuisances[nuisanceName]["name"]+"Up")
                hist_qqH_do = inFile.Get(cutName+"/"+variableName+"/histo_qqH_hww_"+nuisances[nuisanceName]["name"]+"Down")

                new_hist_qq_up = hist_qqH_up.Clone() + hist_qqWW.Clone() + hist_qqInt.Clone()
                new_hist_qq_do = hist_qqH_do.Clone() + hist_qqWW.Clone() + hist_qqInt.Clone()

                #new_histos[cutName+"/"+variableName+"/histo_qqToWW_"+nuisances[nuisanceName]["name"]+"Up"] = new_hist_qq_up
                #new_histos[cutName+"/"+variableName+"/histo_qqToWW_"+nuisances[nuisanceName]["name"]+"Down"] = new_hist_qq_do

                new_hist_qq_up.Clone("histo_qqToWW_"+nuisances[nuisanceName]["name"]+"Up").Write()
                new_hist_qq_do.Clone("histo_qqToWW_"+nuisances[nuisanceName]["name"]+"Down").Write()

                del new_hist_qq_up
                del new_hist_qq_do
                
            elif (doqqWW):

                hist_qqWW_up = inFile.Get(cutName+"/"+variableName+"/histo_WWewk_"+nuisances[nuisanceName]["name"]+"Up")
                hist_qqWW_do = inFile.Get(cutName+"/"+variableName+"/histo_WWewk_"+nuisances[nuisanceName]["name"]+"Down")

                new_hist_qq_up = hist_qqH.Clone() + hist_qqWW_up.Clone() + hist_qqInt.Clone()
                new_hist_qq_do = hist_qqH.Clone() + hist_qqWW_do.Clone() + hist_qqInt.Clone()

                #new_histos[cutName+"/"+variableName+"/histo_qqToWW_"+nuisances[nuisanceName]["name"]+"Up"] = new_hist_qq_up
                #new_histos[cutName+"/"+variableName+"/histo_qqToWW_"+nuisances[nuisanceName]["name"]+"Down"] = new_hist_qq_do

                new_hist_qq_up.Clone("histo_qqToWW_"+nuisances[nuisanceName]["name"]+"Up").Write()
                new_hist_qq_do.Clone("histo_qqToWW_"+nuisances[nuisanceName]["name"]+"Down").Write()

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


