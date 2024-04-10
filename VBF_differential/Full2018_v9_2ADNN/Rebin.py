#!/usr/bin/env python

import CombineHarvester.CombineTools.ch as ch
import ROOT 
import sys

args = sys.argv[1:]
assert (len(args) >= 1)

DATACARD = args[0]
# VAR  = args[1]
# THRESHOLD = args[2]


THRESHOLD = 0.3
VAR = 'adnn_VBFvsGGH'

CUTS = ['hww2l2v_13TeV_of2j_dphijj_4bins_0', 'hww2l2v_13TeV_of2j_dphijj_4bins_1', 'hww2l2v_13TeV_of2j_dphijj_4bins_2', 'hww2l2v_13TeV_of2j_dphijj_4bins_3']


for BIN in CUTS:

    cmb = ch.CombineHarvester()
    cmb.SetFlag('check-negative-bins-on-import', 0)

    print (BIN)
    cmb.ParseDatacard(DATACARD+"/"+BIN+"/"+VAR+"/datacard.txt")

# Rebin Mode 1 : Starts from bin with lowest content which fails the condition. Tries moving left and right merging bins until threshold is met.
# Chooses from left and right to minimise number of bins lost
# Repeats with new lowest bin until all bins pass threshold
# SetBinUncertFraction : The threshold on the bin uncertainty fraction for which we consider merging bins

    rebin = ch.AutoRebin()
    rebin.SetBinThreshold(0.0)
    rebin.SetBinUncertFraction(float(THRESHOLD))
    rebin.SetRebinMode(1)
    rebin.SetPerformRebin(True) 

    rebin.SetVerbosity(0)
    rebin.Rebin(cmb, cmb)

    writer = ch.CardWriter(DATACARD+'_opt/'+BIN+'/'+VAR+'/datacard.txt',
                        DATACARD+'_opt/'+BIN+'/'+VAR+'/shapes/histos_'+BIN+'.root')

    writer.WriteCards('', cmb)


