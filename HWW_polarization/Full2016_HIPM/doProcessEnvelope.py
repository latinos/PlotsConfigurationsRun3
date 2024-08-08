#!/usr/bin/env python                                                                                                                                                                                                                                                           

import sys
import optparse
import copy
import collections
import os.path
import math
import logging
import tempfile
import subprocess
import fileinput
import argparse
from sys import argv
import ROOT

######
######
######

filename = "/eos/user/s/sblancof/MC/rootFiles/mkShapes__WW_2016_complete.root"

######
######
######

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

from mkShapesRDF.shapeAnalysis.histo_utils import postProcessNuisances

postProcessNuisances(filename, samples, aliases, variables, cuts, nuisances)


