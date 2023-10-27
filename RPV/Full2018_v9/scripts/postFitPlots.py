#!/bin/python

import sys
import os
import ROOT
import root_numpy as rnp

variable = "sb_mass"
directory = "/afs/cern.ch/work/l/lviliani/LatinosFramework13TeV_FullRun2/CMSSW_10_6_4/src/PlotsConfigurations/Configurations/RPVRegression_analysis/datacardsTEST_RPV/hww2l2v_13TeV_top_1j/"+variable
mass = sys.argv[1]

os.chdir(directory)

COMBINE_OPTIONS="--cminDefaultMinimizerStrategy 0 --cminApproxPreFitTolerance=100  --cminFallbackAlgo Minuit2,Migrad,0:0.1 --cminDefaultMinimizerTolerance 0.1 --X-rtd MINIMIZER_MaxCalls=9999999  --X-rtd MINIMIZER_analytic --X-rtd FAST_VERTICAL_MORPH  --X-rtd MINIMIZER_freezeDisassociatedParams  --X-rtd OPTIMIZE_BOUNDS=0"

command = "combine -M FitDiagnostics datacard_forfit.root --toysFile higgsCombineRPV_sb700_chi400_sl350.GenerateOnly.mH120.123456.root -t 1 --setParameters MH=%s,alpha=1 --freezeParameter MH --setParameterRanges sigma=1,100:n=0.1,40:alpha=0,5:r=0,20000 --redefineSignalPOI r %s --saveShapes -n .M%s --skipBOnlyFit" % (mass, COMBINE_OPTIONS, mass)

filename="fitDiagnostics.M"+mass+".root"
if not os.path.exists(filename): os.system(command)

f = ROOT.TFile(filename)

data = f.Get("shapes_fit_s/hww2l2v_13TeV_top_1j/data")
total_bkg = f.Get("shapes_fit_s/hww2l2v_13TeV_top_1j/total_background")
total_sig = f.Get("shapes_fit_s/hww2l2v_13TeV_top_1j/total_signal")

total_bkg.SetLineColor(ROOT.kBlue)
total_bkg.SetFillColor(ROOT.kBlue)
total_sig.SetLineColor(ROOT.kRed)
total_sig.SetFillColor(ROOT.kRed)

sta = ROOT.THStack()
sta.Add(total_bkg)
sta.Add(total_sig)

data.SetMarkerStyle(20)

c1 = ROOT.TCanvas()
c1.cd()
sta.Draw()
data.Draw("Psame")
total_sig.Draw("same")


c2 = ROOT.TCanvas()
c2.cd()

graph_bkg = rnp.hist2array(total_bkg, copy=True)

data_diff = ROOT.TGraphAsymmErrors()

for iBin in range(0, data.GetN()):
  data_diff.SetPoint     (iBin, data.GetPointX(iBin), data.GetPointY(iBin) - graph_bkg[iBin]   )
  #data_diff.SetPointError(iBin, 0, 

data_diff.SetMarkerStyle(20)
data_diff.Draw("PA")
total_sig.Draw("Csame")

a=raw_input()

