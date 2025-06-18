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


outputFile = "/eos/user/s/sblancof/MC/rootFiles/mkShapes__WW_2017_complete.root"

print("Start computation")

df = uproot.open(outputFile)

for cutName in cuts:
    for varName in variables:
        print(varName)
        inFile = ROOT.TFile(outputFile, "UPDATE")
        inFile.cd(cutName+"/"+varName)

        baseHist = inFile.Get(cutName+"/"+varName+"/histo_Dyemb")
        
        hist = inFile.Get(cutName+"/"+varName+"/histo_Dyveto")
        new_hist_up = 0.1*hist + baseHist
        new_hist_do = -0.1*hist + baseHist
        
        new_hist_up.Clone("histo_Dyemb_CMS_embed_veto_2017Up").Write()
        new_hist_do.Clone("histo_Dyemb_CMS_embed_veto_2017Down").Write()

        del baseHist
        del hist
        del new_hist_up
        del new_hist_do

        inFile.Close()
                        
print("Fixed!!!")



