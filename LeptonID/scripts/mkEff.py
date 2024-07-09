#!/usr/bin/env python

import os, sys
argv = sys.argv
sys.argv = argv[:1]

import optparse
import math

import ROOT
from ROOT import TCanvas, TPad, TFile, TPaveText, TLegend
from ROOT import TH1D, TH1F, TF1, TGraphErrors, TMultiGraph

import importlib.util

if __name__ == '__main__':

    sys.argv = argv

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    
    parser.add_option('--inputFile',   dest='inputFile',   help='input file with histograms',                   default='DEFAULT')
    parser.add_option('--signals',     dest='signals',     help='comma-separated list of signal processes',     default='DEFAULT')
    parser.add_option('--backgrounds', dest='backgrounds', help='comma-separated list of background processes', default='DEFAULT')
    parser.add_option('--cuts',        dest='cuts',        help='list of cuts names to analyze as in cuts.py',  default='DEFAULT')
    parser.add_option('--presel',      dest='presel',      help='preselection to analyze as in cuts.py',        default='DEFAULT')
    parser.add_option('--year',        dest='year',        help='year',                                         default='DEFAULT')
    parser.add_option('--outputDir',   dest='outputDir',   help='output directory',                             default='eff_plots')
    parser.add_option('--variable',    dest='variable',    help='variable to inspect',                          default='events')

    
    # read default parsing options as well
    (opt, args) = parser.parse_args()

    sys.argv.append( '-b' )
    ROOT.gROOT.SetBatch()

    print("Input file  = {}".format(opt.inputFile))
    print("Signals     = {}".format(opt.signals))
    print("Backgrounds = {}".format(opt.backgrounds))
    print("Cuts        = {}".format(opt.cuts))
    print("Presel      = {}".format(opt.presel))
    print("Year        = {}".format(opt.year))
    print("Output dir  = {}".format(opt.outputDir))
    print("Variable    = {}".format(opt.variable))

    # Exceptions
    if opt.inputFile == 'DEFAULT' :
        raise ValueError("Please insert input file name")
    inputFile = opt.inputFile
    
    if opt.signals == 'DEFAULT' :
        raise ValueError("Please insert the list of signal processes")

    if opt.backgrounds == 'DEFAULT' :
        raise ValueError("Please insert the list of background processes")

    if opt.year == 'DEFAULT' :
        raise ValueError("Please insert the year to analyze")
    year = opt.year

    if opt.cuts == 'DEFAULT' :
        raise ValueError("Please insert the cuts to analyze")
    cuts = opt.cuts

    if opt.presel == 'DEFAULT' :
        raise ValueError("Please insert the preselection to analyze")
    presel = opt.presel


    outputDir = opt.outputDir
    variable  = opt.variable
    
    # Transform 'signals' and 'backgrounds' into a list
    signals     = opt.signals.split(',')
    backgrounds = opt.backgrounds.split(',')

    # outputFile = f'{cut}__{opt.signals}__VS__{opt.backgrounds}'
    
    # output_file_name = outputDir + "/" + outputFile
    # print("Output file complete path = {}".format(output_file_name))

    infile = ROOT.TFile(inputFile)
    
    output_root_file = ROOT.TFile(f"{outputDir}/efficiencies.root","update")
    output_root_file.cd()
    
    # Loop over cuts
    cuts = opt.cuts.split(',')

    for cut in cuts:

        print(f"Current cut: {cut}")
        
        # Histograms definitions
        h_sig = ROOT.TH1F("h_sig","h_sig",999,0,2)
        h_bkg = ROOT.TH1F("h_bkg","h_bkg",999,0,2)
        
        h_sig_preselection = ROOT.TH1F("h_sig_presel","h_sig_presel",999,0,2)
        h_bkg_preselection = ROOT.TH1F("h_bkg_presel","h_bkg_presel",999,0,2)
        
        print("numer of bins = ".format(h_sig.GetNbinsX()))
    
        # Filling histograms
        for signal in signals:
            print(f"Current signal: {signal}")
            h_name = f"{cut}/{variable}/histo_{signal}"
            h_tmp  = infile.Get(h_name)
            print(f"Current histo integral: {h_tmp.Integral()}")
            if (h_sig.GetNbinsX() == 999):
                h_sig = h_tmp.Clone("h_sig")
            else:
                h_sig.Add(h_tmp)
    
            h_name_presel = f"{presel}/{variable}/histo_{signal}"
            h_tmp_presel  = infile.Get(h_name_presel)
            if (h_sig_preselection.GetNbinsX() == 999):
                h_sig_preselection = h_tmp_presel.Clone("h_sig_presel")
            else:
                h_sig.Add(h_tmp_presel)
    
        print(f"Total signal integral: {h_sig.Integral()}")
        print(f"Total signal presel integral: {h_sig_preselection.Integral()}")
            
        for background in backgrounds:
            print(f"Current background: {background}")
            h_name = f"{cut}/{variable}/histo_{background}"
            h_tmp  = infile.Get(h_name)
            print(f"Current histo integral: {h_tmp.Integral()}")
            if (h_bkg.GetNbinsX() == 999):
                h_bkg = h_tmp.Clone("h_bkg")
            else:
                h_bkg.Add(h_tmp)
    
            h_name_presel = f"{presel}/{variable}/histo_{background}"
            h_tmp_presel  = infile.Get(h_name_presel)
            if (h_bkg_preselection.GetNbinsX() == 999):
                h_bkg_preselection = h_tmp_presel.Clone("h_bkg_presel")
            else:
                h_bkg.Add(h_tmp_presel)
    
        print(f"Total background integral: {h_bkg.Integral()}")
        print(f"Total background presel integral: {h_bkg_preselection.Integral()}")
    
        # Getting efficiencies
        sig_eff = h_sig.Integral()/h_sig_preselection.Integral()
        print(f"Signal efficiency: {sig_eff}")
    
        bkg_eff = h_bkg.Integral()/h_bkg_preselection.Integral()
        print(f"Background efficiency: {bkg_eff}")
        
        # Preparing output
        os.system(f"mkdir -p {outputDir}/")
    
        with open(f"{outputDir}/efficiencies.csv", "a") as outfile:
            outfile.write(f"{signals} ; {backgrounds} ; {cut} ; {sig_eff} ; {bkg_eff}\n")

        # histo_eff = ROOT.TH2F(f"{signal}_{background}_{cut}","{signal}_{background}_{cut}",1000,0,1,1000,0,1)
        g_eff = ROOT.TGraph()
        g_eff.SetTitle(f"{signal}_{background}_{cut}")
        g_eff.SetName(f"{signal}_{background}_{cut}")
        g_eff.GetXaxis().SetTitle("1 - bkg eff")
        g_eff.GetYaxis().SetTitle("sig eff")
        g_eff.GetXaxis().SetRangeUser(0,1)
        g_eff.GetYaxis().SetRangeUser(0,1)
        g_eff.SetPoint(0,1-bkg_eff,sig_eff)

        g_eff.Write()
        
        del h_sig
        del h_bkg
        del h_sig_preselection
        del h_bkg_preselection
        del g_eff
        
        print("################ \n")
        print("\n")

    output_root_file.Close()
    
