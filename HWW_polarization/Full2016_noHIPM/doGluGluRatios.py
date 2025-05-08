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

print("DEBUG!!!!")
print("Now check ggH and ggWW in ggToWW")

df = uproot.open(outputFile)

'''
nuisances['QCDscale_ggVV_sr_0j'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.272*(1.15-1.0))
    },
    'cuts' : [cut for cut in cuts0j if 'Signal_0j' in cut],
}
'''

nuisances = """"""

for cutName in cuts:
    variableName = "events"
    print(cutName + "<------")
    print("    -->" + variableName)
    
    ggH = df[cutName+"/"+variableName+"/histo_ggH_hww"].values()[0]
    ggWW = df[cutName+"/"+variableName+"/histo_ggWW"].values()[0]

    print("ggH : " + str(ggH/(ggH+ggWW)))
    print("ggWW : " + str(ggWW/(ggH+ggWW)))

    nuisances += """
nuisances['QCDscale_ggVV_"""+cutName+"""'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+"""+str(ggWW/(ggH+ggWW))+"""*(1.15-1.0))
    },
    'cuts' : [cut for cut in total_cuts if cut=='"""+cutName+"""'],
}"""

print("Finished!")
print("\n")
print("\n")
print(nuisances)
