#!/usr/bin/env python

import os, sys
argv = sys.argv
sys.argv = argv[:1]

import optparse
import math

import ROOT

if __name__ == '__main__':

    sys.argv = argv

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    
    parser.add_option('--inputFile',   dest='inputFile',  help='input file with histograms',         default='DEFAULT')
    parser.add_option('--outputFile',  dest='outputFile', help='output where histograms are stored', default='DEFAULT')

    # read default parsing options as well
    (opt, args) = parser.parse_args()

    sys.argv.append( '-b' )
    ROOT.gROOT.SetBatch()

    print("Input file  = {}".format(opt.inputFile))

    # Exceptions
    if opt.inputFile == 'DEFAULT' :
        raise ValueError("Please insert input file name")
    inputFile = opt.inputFile

    if opt.outputFile == 'DEFAULT' :
        raise ValueError("Please insert output file name")
    outputFile = opt.outputFile
    

    # Open input file
    infile = ROOT.TFile(inputFile)
    
    # Create output file
    outfile = ROOT.TFile(outputFile,"recreate")
    outfile.cd()

    # Hard-coded input variables. TO BE MOVED TO INPUT ARGUMENTS!
    jet_pt   = 25
    flavor   = "muon"
    variable = "pt1_eta1"
    
    # Dictionary with histograms names
    histograms = {
        # DATA
        "DATA_QCD_loose"   : f"QCD_loose_jet_pt_{jet_pt}_{flavor}/{variable}/histo_DATA",
        "DATA_QCD_tight"   : f"QCD_tight_jet_pt_{jet_pt}_{flavor}/{variable}/histo_DATA",
        "DATA_Zpeak_loose" : f"Zpeak_loose_jet_pt_{jet_pt}_{flavor}/{variable}/histo_DATA",
        "DATA_Zpeak_tight" : f"Zpeak_tight_jet_pt_{jet_pt}_{flavor}/{variable}/histo_DATA",
        # DY QCD region
        "DY_QCD_loose_high_pt" : f"QCD_loose_jet_pt_{jet_pt}_{flavor}/{variable}/histo_DY_muon_high_pt",
        "DY_QCD_loose_low_pt"  : f"QCD_loose_jet_pt_{jet_pt}_{flavor}/{variable}/histo_DY_muon_low_pt",
        "DY_QCD_tight_high_pt" : f"QCD_tight_jet_pt_{jet_pt}_{flavor}/{variable}/histo_DY_muon_high_pt",
        "DY_QCD_tight_low_pt"  : f"QCD_tight_jet_pt_{jet_pt}_{flavor}/{variable}/histo_DY_muon_low_pt",
        # DY Z-peak region
        "DY_Zpeak_loose_high_pt" : f"Zpeak_loose_jet_pt_{jet_pt}_{flavor}/{variable}/histo_DY_muon_high_pt",
        "DY_Zpeak_loose_low_pt"  : f"Zpeak_loose_jet_pt_{jet_pt}_{flavor}/{variable}/histo_DY_muon_low_pt",
        "DY_Zpeak_tight_high_pt" : f"Zpeak_tight_jet_pt_{jet_pt}_{flavor}/{variable}/histo_DY_muon_high_pt",
        "DY_Zpeak_tight_low_pt"  : f"Zpeak_tight_jet_pt_{jet_pt}_{flavor}/{variable}/histo_DY_muon_low_pt",
        # WJets QCD region
        "WJets_QCD_loose_high_pt" : f"QCD_loose_jet_pt_{jet_pt}_{flavor}/{variable}/histo_WJets_muon_high_pt",
        "WJets_QCD_loose_low_pt"  : f"QCD_loose_jet_pt_{jet_pt}_{flavor}/{variable}/histo_WJets_muon_low_pt",
        "WJets_QCD_tight_high_pt" : f"QCD_tight_jet_pt_{jet_pt}_{flavor}/{variable}/histo_WJets_muon_high_pt",
        "WJets_QCD_tight_low_pt"  : f"QCD_tight_jet_pt_{jet_pt}_{flavor}/{variable}/histo_WJets_muon_low_pt",
    }
    
    # Get relevant histograms from input file

    ###################
    # Data histograms #
    ###################

    # QCD region: used for fake rate estimation
    histo_DATA_QCD_loose = infile.Get(histograms["DATA_QCD_loose"])
    histo_DATA_QCD_tight = infile.Get(histograms["DATA_QCD_tight"])
    
    # Zpeak region: used for prompt rate estimation and EWK processes normalization
    histo_DATA_Zpeak_loose = infile.Get(histograms["DATA_Zpeak_loose"])
    histo_DATA_Zpeak_tight = infile.Get(histograms["DATA_Zpeak_tight"])
    
    #################
    # DY histograms #
    #################
    
    # QCD region: used for fake rate estimation
    histo_DY_QCD_loose        = infile.Get(histograms["DY_QCD_loose_high_pt"])
    histo_DY_QCD_loose_low_pt = infile.Get(histograms["DY_QCD_loose_low_pt"])
    histo_DY_QCD_loose.Add(histo_DY_QCD_loose_low_pt)
    
    histo_DY_QCD_tight        = infile.Get(histograms["DY_QCD_tight_high_pt"])
    histo_DY_QCD_tight_low_pt = infile.Get(histograms["DY_QCD_tight_low_pt"])
    histo_DY_QCD_tight.Add(histo_DY_QCD_tight_low_pt)

    # Zpeak region: used for prompt rate estimation and EWK processes normalization
    histo_DY_Zpeak_loose        = infile.Get(histograms["DY_Zpeak_loose_high_pt"])
    histo_DY_Zpeak_loose_low_pt = infile.Get(histograms["DY_Zpeak_loose_low_pt"])
    histo_DY_Zpeak_loose.Add(histo_DY_Zpeak_loose_low_pt)

    histo_DY_Zpeak_tight        = infile.Get(histograms["DY_Zpeak_tight_high_pt"])
    histo_DY_Zpeak_tight_low_pt = infile.Get(histograms["DY_Zpeak_tight_low_pt"])
    histo_DY_Zpeak_tight.Add(histo_DY_Zpeak_tight_low_pt)

    ####################
    # WJets histograms #
    ####################
    
    # QCD region: used for fake rate estimation
    histo_WJets_QCD_loose        = infile.Get(histograms["WJets_QCD_loose_high_pt"])
    histo_WJets_QCD_loose_low_pt = infile.Get(histograms["WJets_QCD_loose_low_pt"])
    histo_WJets_QCD_loose.Add(histo_WJets_QCD_loose_low_pt)

    histo_WJets_QCD_tight        = infile.Get(histograms["WJets_QCD_tight_high_pt"])
    histo_WJets_QCD_tight_low_pt = infile.Get(histograms["WJets_QCD_tight_low_pt"])
    histo_WJets_QCD_tight.Add(histo_WJets_QCD_tight_low_pt)

    # Prepare histograms with EWK subtraction applied
    histo_DATA_QCD_loose_EWKsub = histo_DATA_QCD_loose.Clone()
    histo_DATA_QCD_loose_EWKsub.Add(histo_DY_QCD_loose,    -1)
    histo_DATA_QCD_loose_EWKsub.Add(histo_WJets_QCD_loose, -1)
    
    histo_DATA_QCD_tight_EWKsub = histo_DATA_QCD_tight.Clone()
    histo_DATA_QCD_tight_EWKsub.Add(histo_DY_QCD_tight,    -1)
    histo_DATA_QCD_tight_EWKsub.Add(histo_WJets_QCD_tight, -1)
    
    # Bins structure:
    # pt bins  = 8: [10, 15, 20, 25, 30, 35, 40, 45, 50]
    # eta bins = 5: [0, 0.5, 1.0, 1.5, 2.0, 2.5]
    # variable: Lepton_pt[0]:abs(Lepton_eta[0]) --> Need to loop over abs(eta) and then on pT
    eta_bins = 5
    eta_binning = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 100]
    pt_bins  = 8
    pt_binning = [10, 15, 20, 25, 30, 35, 40, 45, 50, 1000]
    
    
    for eta_bin in range(0,eta_bins):
        for pt_bin in range(1,pt_bins+1):
            print(f"Eta bin: {eta_bin} - pT bin: {pt_bin} - Total bin: {pt_bin + pt_bins*eta_bin}")
            loose_yields_DATA = histo_DATA_QCD_loose.GetBinContent(pt_bin + pt_bins*eta_bin)
            tight_yields_DATA = histo_DATA_QCD_tight.GetBinContent(pt_bin + pt_bins*eta_bin)

            loose_yields_DATA_EWKsub = histo_DATA_QCD_loose_EWKsub.GetBinContent(pt_bin + pt_bins*eta_bin)
            tight_yields_DATA_EWKsub = histo_DATA_QCD_tight_EWKsub.GetBinContent(pt_bin + pt_bins*eta_bin)
            
            # Ensure we are not dividing by 0
            fake_rate = 0
            if loose_yields_DATA > 0:
                fake_rate = tight_yields_DATA / loose_yields_DATA
            fake_rate_EWKsub = 0
            if loose_yields_DATA_EWKsub > 0:
                fake_rate_EWKsub = tight_yields_DATA_EWKsub / loose_yields_DATA_EWKsub

                
            # Printout - for debugging
            print(f"Number of tight events: {tight_yields_DATA} - Number of loose events: {loose_yields_DATA}")
            print(f"Fake rate in bin (pT,abs(eta)) = ({pt_binning[pt_bin-1]}-{pt_binning[pt_bin]},{eta_binning[eta_bin]}-{eta_binning[eta_bin+1]}) = {fake_rate}")

            print(f"Fake rate with EWK subtraction in bin (pT,abs(eta)) = ({pt_binning[pt_bin-1]}-{pt_binning[pt_bin]},{eta_binning[eta_bin]}-{eta_binning[eta_bin+1]}) = {fake_rate_EWKsub}")
            
