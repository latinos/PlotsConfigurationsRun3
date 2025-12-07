# Features to implement:
# - Normalization of EWK contamination using control region.
# - Anything else I am missing now.

#!/usr/bin/env python

import os, sys
argv = sys.argv
sys.argv = argv[:1]

import optparse
import math
from array import array
import math

import ROOT

if __name__ == '__main__':

    sys.argv = argv

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    
    parser.add_option('--inputFile',        dest='inputFile',        help='input file with histograms',                     default='DEFAULT')
    parser.add_option('--outputFolder',     dest='outputFolder',     help='folder where output file is stored',             default='DEFAULT')
    parser.add_option('--outputFileName',   dest='outputFileName',   help='output where histograms are stored',             default='DEFAULT')
    parser.add_option('--jet_pt',           dest='jet_pt',           help='pt threshold of the recoling jet',               default='DEFAULT')
    parser.add_option('--flavor',           dest='flavor',           help='flavor to inspect (electron or muon)',           default='DEFAULT')
    parser.add_option('--variable',         dest='variable',         help='variable to use',                                default='DEFAULT')
    parser.add_option('--do_prompt_rate',   dest='do_prompt_rate',   help='flag to produce also prompt rate',               default='False')
    parser.add_option('--outputFileNamePR', dest='outputFileNamePR', help='output where prompt rate histograms are stored', default='DEFAULT')

    # jet_pt   = 25
    # flavor   = "muon"
    # variable = "pt1_eta1"
    
    # read default parsing options as well
    (opt, args) = parser.parse_args()

    sys.argv.append( '-b' )
    ROOT.gROOT.SetBatch()

    print("Input file  = {}".format(opt.inputFile))

    # Exceptions
    if opt.inputFile == 'DEFAULT' :
        raise ValueError("Please insert input file name")
    inputFile = opt.inputFile

    if opt.outputFolder == 'DEFAULT' :
        raise ValueError("Please insert output directory")
    outputFolder = opt.outputFolder

    if opt.outputFileName == 'DEFAULT' :
        raise ValueError("Please insert output file name")
    outputFileName = opt.outputFileName

    if opt.jet_pt == 'DEFAULT' :
        raise ValueError("Please insert a valid jet pt threshold")
    jet_pt = opt.jet_pt

    if opt.flavor == 'DEFAULT' :
        raise ValueError("Please insert a valid lepton flavor to inspect")
    flavor = opt.flavor

    if opt.variable == 'DEFAULT' :
        raise ValueError("Please insert a variable to use")
    variable = opt.variable

    if opt.do_prompt_rate != 'False' and opt.do_prompt_rate != 'True' :
        raise ValueError("Please insert a valid value for the 'do prompt rate' flag: True or False")
    do_prompt_rate = opt.do_prompt_rate

    if opt.do_prompt_rate == 'True' and opt.outputFileNamePR == 'DEFAULT':
        raise ValueError("Please insert a valid output name for the PR output file")
    outputFileNamePR = opt.outputFileNamePR
    

    # Open input file
    infile = ROOT.TFile(inputFile)
    
    # Create output folder
    os.system(f'mkdir -p {outputFolder}')
    
    # Create output file
    outputFile = f'{outputFolder}/{outputFileName}'
    outfile = ROOT.TFile(outputFile,"recreate")
    outfile.cd()

    # Dictionary with histograms names
    histograms = {
        # DATA
        "DATA_QCD_loose"      : f"QCD_loose_jet_pt_{jet_pt}_{flavor}/{variable}/histo_DATA",
        "DATA_QCD_tight"      : f"QCD_tight_jet_pt_{jet_pt}_{flavor}/{variable}/histo_DATA",
        "DATA_Zpeak_loose"    : f"Zpeak_loose_jet_pt_{jet_pt}_{flavor}/{variable}/histo_DATA",
        "DATA_Zpeak_tight"    : f"Zpeak_tight_jet_pt_{jet_pt}_{flavor}/{variable}/histo_DATA",
        # Unprescaled DATA in Z-peak region: used for prompt rate estimation
        "DATA_Zpeak_PR_loose" : f"Zpeak_PR_loose_{flavor}/{variable}/histo_DATA_unprescaled",
        "DATA_Zpeak_PR_tight" : f"Zpeak_PR_tight_{flavor}/{variable}/histo_DATA_unprescaled",
        # DY QCD region
        "DY_QCD_loose_high_pt" : f"QCD_loose_jet_pt_{jet_pt}_{flavor}/{variable}/histo_DY_{flavor}_high_pt",
        "DY_QCD_loose_low_pt"  : f"QCD_loose_jet_pt_{jet_pt}_{flavor}/{variable}/histo_DY_{flavor}_low_pt",
        "DY_QCD_tight_high_pt" : f"QCD_tight_jet_pt_{jet_pt}_{flavor}/{variable}/histo_DY_{flavor}_high_pt",
        "DY_QCD_tight_low_pt"  : f"QCD_tight_jet_pt_{jet_pt}_{flavor}/{variable}/histo_DY_{flavor}_low_pt",
        # DY Z-peak region
        "DY_Zpeak_loose_high_pt" : f"Zpeak_loose_jet_pt_{jet_pt}_{flavor}/{variable}/histo_DY_{flavor}_high_pt",
        "DY_Zpeak_loose_low_pt"  : f"Zpeak_loose_jet_pt_{jet_pt}_{flavor}/{variable}/histo_DY_{flavor}_low_pt",
        "DY_Zpeak_tight_high_pt" : f"Zpeak_tight_jet_pt_{jet_pt}_{flavor}/{variable}/histo_DY_{flavor}_high_pt",
        "DY_Zpeak_tight_low_pt"  : f"Zpeak_tight_jet_pt_{jet_pt}_{flavor}/{variable}/histo_DY_{flavor}_low_pt",
        # DY Z-peak region for PR measurement        
        # "DY_Zpeak_PR_loose_high_pt" : f"Zpeak_PR_loose_{flavor}/{variable}/histo_DY_{flavor}_high_pt",
        # "DY_Zpeak_PR_loose_low_pt"  : f"Zpeak_PR_loose_{flavor}/{variable}/histo_DY_{flavor}_low_pt",
        # "DY_Zpeak_PR_tight_high_pt" : f"Zpeak_PR_tight_{flavor}/{variable}/histo_DY_{flavor}_high_pt",
        # "DY_Zpeak_PR_tight_low_pt"  : f"Zpeak_PR_tight_{flavor}/{variable}/histo_DY_{flavor}_low_pt",
        # Unprescaled DY in Z-peak region: used for prompt rate estimation
        "DY_Zpeak_PR_loose"  : f"Zpeak_PR_loose_{flavor}/{variable}/histo_DY_unprescaled",
        "DY_Zpeak_PR_tight"  : f"Zpeak_PR_tight_{flavor}/{variable}/histo_DY_unprescaled",
        # WJets QCD region
        "WJets_QCD_loose_high_pt" : f"QCD_loose_jet_pt_{jet_pt}_{flavor}/{variable}/histo_WJets_{flavor}_high_pt",
        "WJets_QCD_loose_low_pt"  : f"QCD_loose_jet_pt_{jet_pt}_{flavor}/{variable}/histo_WJets_{flavor}_low_pt",
        "WJets_QCD_tight_high_pt" : f"QCD_tight_jet_pt_{jet_pt}_{flavor}/{variable}/histo_WJets_{flavor}_high_pt",
        "WJets_QCD_tight_low_pt"  : f"QCD_tight_jet_pt_{jet_pt}_{flavor}/{variable}/histo_WJets_{flavor}_low_pt",
    }
    
    # Get relevant histograms from input file

    ###################
    # Data histograms #
    ###################

    # QCD region: used for fake rate estimation
    histo_DATA_QCD_loose = infile.Get(histograms["DATA_QCD_loose"])
    histo_DATA_QCD_tight = infile.Get(histograms["DATA_QCD_tight"])
    
    # Zpeak region: used for EWK processes normalization
    histo_DATA_Zpeak_loose = infile.Get(histograms["DATA_Zpeak_loose"])
    histo_DATA_Zpeak_tight = infile.Get(histograms["DATA_Zpeak_tight"])

    # Unprescaled Zpeak PR region: used for prompt rate measurement
    histo_DATA_PR_Zpeak_loose = infile.Get(histograms["DATA_Zpeak_PR_loose"])
    histo_DATA_PR_Zpeak_tight = infile.Get(histograms["DATA_Zpeak_PR_tight"])
    
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

    # Zpeak region: used for EWK processes normalization
    histo_DY_Zpeak_loose        = infile.Get(histograms["DY_Zpeak_loose_high_pt"])
    histo_DY_Zpeak_loose_low_pt = infile.Get(histograms["DY_Zpeak_loose_low_pt"])
    histo_DY_Zpeak_loose.Add(histo_DY_Zpeak_loose_low_pt)

    histo_DY_Zpeak_tight        = infile.Get(histograms["DY_Zpeak_tight_high_pt"])
    histo_DY_Zpeak_tight_low_pt = infile.Get(histograms["DY_Zpeak_tight_low_pt"])
    histo_DY_Zpeak_tight.Add(histo_DY_Zpeak_tight_low_pt)

    # Unprescaled Zpeak PR region: used for prompt rate measurement
    histo_DY_Zpeak_PR_loose = infile.Get(histograms["DY_Zpeak_PR_loose"])
    # histo_DY_Zpeak_PR_loose_low_pt = infile.Get(histograms["DY_Zpeak_PR_loose_low_pt"])
    # histo_DY_Zpeak_PR_loose.Add(histo_DY_Zpeak_PR_loose_low_pt)

    histo_DY_Zpeak_PR_tight = infile.Get(histograms["DY_Zpeak_PR_tight"])
    # histo_DY_Zpeak_PR_tight_low_pt = infile.Get(histograms["DY_Zpeak_PR_tight_low_pt"])
    # histo_DY_Zpeak_PR_tight.Add(histo_DY_Zpeak_PR_tight_low_pt)


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
    
    # EWK 10% variation to consider systematic on EWK subtraction
    ewk_rel_unc = 0.10

    def make_scaled_ewk_sub(loose_data, tight_data, loose_dy, tight_dy, loose_wj, tight_wj, scale):
        lo = loose_data.Clone()
        ti = tight_data.Clone()
        lo.Add(loose_dy, -scale)
        lo.Add(loose_wj, -scale)
        ti.Add(tight_dy, -scale)
        ti.Add(tight_wj, -scale)
        return lo, ti

    h_lo_up, h_ti_up = make_scaled_ewk_sub(
        histo_DATA_QCD_loose,  histo_DATA_QCD_tight,
        histo_DY_QCD_loose,    histo_DY_QCD_tight,
        histo_WJets_QCD_loose, histo_WJets_QCD_tight,
        1.0 + ewk_rel_unc
    )
    h_lo_dn, h_ti_dn = make_scaled_ewk_sub(
        histo_DATA_QCD_loose,  histo_DATA_QCD_tight,
        histo_DY_QCD_loose,    histo_DY_QCD_tight,
        histo_WJets_QCD_loose, histo_WJets_QCD_tight,
        1.0 - ewk_rel_unc
    )
    
    # Bins structure:
    # pt bins  = 8: [10, 15, 20, 25, 30, 35, 40, 45, 50]
    # eta bins = 5: [0, 0.5, 1.0, 1.5, 2.0, 2.5]
    # variable: Lepton_pt[0]:abs(Lepton_eta[0]) --> Need to loop over abs(eta) and then on pT
    # eta_bins = 5
    # eta_binning = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 100]
    eta_bins = 2
    eta_binning = [0, 1.479, 2.5, 100]  # For electrons, we use barrel and endcap regions
    pt_bins  = 8
    pt_binning = [10, 15, 20, 25, 30, 35, 40, 45, 50, 1000]
    
    # Output 2D histograms - fake rate
    fake_rate_histo_numerator   = ROOT.TH2F("FR_pT_eta_numerator",  "FR_pT_eta_numerator",   pt_bins, array('f',pt_binning), eta_bins, array('f',eta_binning))
    fake_rate_histo_denominator = ROOT.TH2F("FR_pT_eta_denominator","FR_pT_eta_denominator", pt_bins, array('f',pt_binning), eta_bins, array('f',eta_binning))

    fake_rate_histo_EWKcorr_numerator   = ROOT.TH2F("FR_pT_eta_EWKcorr_numerator",  "FR_pT_eta_EWKcorr_numerator",   pt_bins, array('f',pt_binning), eta_bins, array('f',eta_binning))
    fake_rate_histo_EWKcorr_denominator = ROOT.TH2F("FR_pT_eta_EWKcorr_denominator","FR_pT_eta_EWKcorr_denominator", pt_bins, array('f',pt_binning), eta_bins, array('f',eta_binning))

    fake_rate_histo         = ROOT.TH2F("FR_pT_eta",        "FR_pT_eta",         pt_bins, array('f',pt_binning), eta_bins, array('f',eta_binning))
    fake_rate_histo_EWKcorr = ROOT.TH2F("FR_pT_eta_EWKcorr","FR_pT_eta_EWKcorr", pt_bins, array('f',pt_binning), eta_bins, array('f',eta_binning))

    
    fake_rate_histo_EWKcorr_up   = ROOT.TH2F("FR_pT_eta_EWKcorr_EWK5Up",   "FR_pT_eta_EWKcorr_EWK5Up",   pt_bins, array('f',pt_binning), eta_bins, array('f',eta_binning))
    fake_rate_histo_EWKcorr_down = ROOT.TH2F("FR_pT_eta_EWKcorr_EWK5Down", "FR_pT_eta_EWKcorr_EWK5Down", pt_bins, array('f',pt_binning), eta_bins, array('f',eta_binning))
    
    def safe_ratio(n, d):
        return (n/d) if (d > 0 and n >= 0) else 0.0


    # Fake rate loop
    for eta_bin in range(0,eta_bins):
        for pt_bin in range(1,pt_bins+1):
            print(f"Eta bin: {eta_bin} - pT bin: {pt_bin} - Total bin: {pt_bin + pt_bins*eta_bin}")
            loose_yields_DATA = histo_DATA_QCD_loose.GetBinContent(pt_bin + pt_bins*eta_bin)
            tight_yields_DATA = histo_DATA_QCD_tight.GetBinContent(pt_bin + pt_bins*eta_bin)

            loose_yields_DATA_EWKsub = histo_DATA_QCD_loose_EWKsub.GetBinContent(pt_bin + pt_bins*eta_bin)
            tight_yields_DATA_EWKsub = histo_DATA_QCD_tight_EWKsub.GetBinContent(pt_bin + pt_bins*eta_bin)
            
            # Ensure we are not dividing by 0
            fake_rate = 0
            fake_rate_error = 0
            if loose_yields_DATA > 0:
                fake_rate = tight_yields_DATA / loose_yields_DATA
                if tight_yields_DATA > 0:
                    fake_rate_error = fake_rate * math.sqrt(1/tight_yields_DATA + 1/loose_yields_DATA)
                    
            fake_rate_EWKsub = 0
            fake_rate_EWKsub_error = 0
            if loose_yields_DATA_EWKsub > 0:
                fake_rate_EWKsub = tight_yields_DATA_EWKsub / loose_yields_DATA_EWKsub
                if tight_yields_DATA_EWKsub > 0:
                    fake_rate_EWKsub_error = fake_rate_EWKsub * math.sqrt(1/tight_yields_DATA_EWKsub + 1/loose_yields_DATA_EWKsub)

            # Output histogram filling
            fake_rate_histo_numerator.SetBinContent(pt_bin,eta_bin+1,tight_yields_DATA)
            fake_rate_histo_denominator.SetBinContent(pt_bin,eta_bin+1,loose_yields_DATA)

            fake_rate_histo_EWKcorr_numerator.SetBinContent(pt_bin,eta_bin+1,tight_yields_DATA_EWKsub)
            fake_rate_histo_EWKcorr_denominator.SetBinContent(pt_bin,eta_bin+1,loose_yields_DATA_EWKsub)

            fake_rate_histo.SetBinContent(pt_bin,eta_bin+1,fake_rate)
            fake_rate_histo.SetBinError(pt_bin,eta_bin+1,fake_rate_error)
            fake_rate_histo_EWKcorr.SetBinContent(pt_bin,eta_bin+1,fake_rate_EWKsub)
            fake_rate_histo_EWKcorr.SetBinError(pt_bin,eta_bin+1,fake_rate_EWKsub_error)
            
            # Histograms for EWK subtraction uncertainty estimation
            ibin = pt_bin + pt_bins*eta_bin
            N_up = h_ti_up.GetBinContent(ibin)
            D_up = h_lo_up.GetBinContent(ibin)
            N_dn = h_ti_dn.GetBinContent(ibin)
            D_dn = h_lo_dn.GetBinContent(ibin)

            fr_up = safe_ratio(N_up, D_up) if (D_up > 0) else fake_rate_EWKsub
            fr_dn = safe_ratio(N_dn, D_dn) if (D_dn > 0) else fake_rate_EWKsub

            fake_rate_histo_EWKcorr_up  .SetBinContent(pt_bin, eta_bin+1, fr_up)
            fake_rate_histo_EWKcorr_down.SetBinContent(pt_bin, eta_bin+1, fr_dn)
            # Leave errors = 0 for pure systematic templates
                
            # Printout - for debugging
            print(f"Number of tight events: {tight_yields_DATA} - Number of loose events: {loose_yields_DATA}")
            print(f"Fake rate in bin (pT,abs(eta)) = ({pt_binning[pt_bin-1]}-{pt_binning[pt_bin]},{eta_binning[eta_bin]}-{eta_binning[eta_bin+1]}) = {fake_rate}")

            print(f"Fake rate with EWK subtraction in bin (pT,abs(eta)) = ({pt_binning[pt_bin-1]}-{pt_binning[pt_bin]},{eta_binning[eta_bin]}-{eta_binning[eta_bin+1]}) = {fake_rate_EWKsub}")
            print(f"   EWK5Up = {fr_up} | EWK5Down = {fr_dn}")
            
    fake_rate_histo_numerator.Write()
    fake_rate_histo_denominator.Write()

    fake_rate_histo_EWKcorr_numerator.Write()
    fake_rate_histo_EWKcorr_denominator.Write()

    fake_rate_histo.Write()
    fake_rate_histo_EWKcorr.Write()
    fake_rate_histo_EWKcorr_up.Write()
    fake_rate_histo_EWKcorr_down.Write()


    outfile.Close()    


    if do_prompt_rate == 'True':
    
        # Create output file
        outputFilePR = f'{outputFolder}/{outputFileNamePR}'
        outfile_PR   = ROOT.TFile(outputFilePR,"recreate")
        outfile_PR.cd()

        # Output 2D histograms - prompt rate
        PR_histo_name = ""
        if flavor == 'muon': PR_histo_name = "h_Muon_signal_pt_eta_bin"
        if flavor == 'ele':  PR_histo_name = "h_Ele_signal_pt_eta_bin"
                
        prompt_rate_histo    = ROOT.TH2F(PR_histo_name,        PR_histo_name,       pt_bins, array('f',pt_binning), eta_bins, array('f',eta_binning))
        prompt_rate_histo_MC = ROOT.TH2F(PR_histo_name+"_MC",  PR_histo_name+"_MC", pt_bins, array('f',pt_binning), eta_bins, array('f',eta_binning))
        
        # Prompt rate loop. We separate it to avoid ocmputing both when you only want fake rate
        for eta_bin in range(0,eta_bins):
            for pt_bin in range(1,pt_bins+1):
                print(f"Eta bin: {eta_bin} - pT bin: {pt_bin} - Total bin: {pt_bin + pt_bins*eta_bin}")

                loose_yields_Zpeak_DY = histo_DY_Zpeak_PR_loose.GetBinContent(pt_bin + pt_bins*eta_bin)
                tight_yields_Zpeak_DY = histo_DY_Zpeak_PR_tight.GetBinContent(pt_bin + pt_bins*eta_bin)
                
                loose_yields_Zpeak_DATA = histo_DATA_PR_Zpeak_loose.GetBinContent(pt_bin + pt_bins*eta_bin)
                tight_yields_Zpeak_DATA = histo_DATA_PR_Zpeak_tight.GetBinContent(pt_bin + pt_bins*eta_bin)
            
                # Ensure we are not dividing by 0
                prompt_rate = 0
                prompt_rate_error = 0
                if loose_yields_Zpeak_DATA > 0:
                    prompt_rate = tight_yields_Zpeak_DATA / loose_yields_Zpeak_DATA
                    if tight_yields_Zpeak_DATA > 0:
                        prompt_rate_error = prompt_rate * math.sqrt(1/tight_yields_Zpeak_DATA + 1/loose_yields_Zpeak_DATA)

                prompt_rate_MC = 0
                prompt_rate_MC_error = 0
                if loose_yields_Zpeak_DY > 0:
                    prompt_rate_MC = tight_yields_Zpeak_DY / loose_yields_Zpeak_DY
                    if tight_yields_Zpeak_DY > 0:
                        prompt_rate_MC_error = prompt_rate_MC * math.sqrt(1/tight_yields_Zpeak_DY + 1/loose_yields_Zpeak_DY)

                # Output histogram filling
                prompt_rate_histo   .SetBinContent(pt_bin,eta_bin+1,prompt_rate)
                prompt_rate_histo   .SetBinError(pt_bin,eta_bin+1,prompt_rate_error)
                prompt_rate_histo_MC.SetBinContent(pt_bin,eta_bin+1,prompt_rate_MC)
                prompt_rate_histo_MC.SetBinError(pt_bin,eta_bin+1,prompt_rate_MC_error)
                
                
                # Printout - for debugging
                print(f"Number of tight events in data: {tight_yields_Zpeak_DATA} - Number of loose events in data: {loose_yields_Zpeak_DATA}")
                print(f"Prompt rate in bin (pT,abs(eta)) = ({pt_binning[pt_bin-1]}-{pt_binning[pt_bin]},{eta_binning[eta_bin]}-{eta_binning[eta_bin+1]}) = {prompt_rate}")

                print(f"Number of tight events in DY MC: {tight_yields_Zpeak_DY} - Number of loose events in data: {loose_yields_Zpeak_DY}")
                print(f"Prompt rate in bin (pT,abs(eta)) = ({pt_binning[pt_bin-1]}-{pt_binning[pt_bin]},{eta_binning[eta_bin]}-{eta_binning[eta_bin+1]}) = {prompt_rate_MC}")
            
        prompt_rate_histo.Write()
        prompt_rate_histo_MC.Write()

        outfile_PR.Close()
