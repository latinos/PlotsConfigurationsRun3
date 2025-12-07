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


outputFile = "/eos/user/s/sblancof/MC/rootFiles/mkShapes__WW_2016_complete.root"

OldNuises = ["CMS_eff_ttHMVA_e_2016", "CMS_eff_e_2016"]
NewNuises = ["CMS_eff_ttHMVA_e", "CMS_eff_e"]

df = uproot.open(outputFile)

for cutName in cuts:
    print(cutName)
    for varName in variables:
        print(varName)
        inFile = ROOT.TFile(outputFile, "UPDATE")
        inFile.cd(cutName+"/"+varName)
        for sampleName in samples:
            if sampleName in ["DATA", "Fake"]:
                continue
            
            for i in range(len(OldNuises)):

                OldNuis = OldNuises[i]
                NewNuis = NewNuises[i]

                if "histo_"+sampleName+"_"+OldNuis+"Up;1" not in df[cutName+"/"+varName].keys():
                    continue
                
                histUp = inFile.Get(cutName+"/"+varName+"/histo_"+sampleName+"_"+OldNuis+"Up")
                histDown = inFile.Get(cutName+"/"+varName+"/histo_"+sampleName+"_"+OldNuis+"Down")
                
                new_histUp = histUp
                new_histDown = histDown
                
                new_histUp.Clone("histo_"+sampleName+"_"+NewNuis+"Up").Write()
                new_histDown.Clone("histo_"+sampleName+"_"+NewNuis+"Down").Write()
                
                del new_histUp
                del new_histDown
                del histUp
                del histDown
        inFile.Close()
