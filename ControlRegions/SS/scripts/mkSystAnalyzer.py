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

def syst_analyzer(input_file_name, cut, variable, sample, systematic, output_directory):

    # Open input file
    input_file = TFile.Open(opt.inputFile)

    # Read histograms
    directory_name = f'{cut}/{variable}'

    histo_nominal = input_file.Get(f'{directory_name}/histo_{sample}')
    histo_up      = input_file.Get(f'{directory_name}/histo_{sample}_{systematic}Up')
    histo_down    = input_file.Get(f'{directory_name}/histo_{sample}_{systematic}Down')

    # Plot nominal histogram, together with the up and down variations 
    ROOT.gStyle.SetOptStat(0)
    
    # Choose colors for the histograms
    histo_nominal.SetLineColor(ROOT.kBlue)
    histo_up.SetLineColor(ROOT.kGreen+1)
    histo_down.SetLineColor(ROOT.kRed+1)

    # Find the maximum to use for y-axis range
    y_axis_max = 1.5 * max(histo_nominal.GetMaximum(),max(histo_up.GetMaximum(),histo_down.GetMaximum()))

    # Create overall canvas
    c1 = ROOT.TCanvas('c1', 'c1', 600, 600)
    c1.cd()

    # Plot hisograms on main pad
    pad1 = ROOT.TPad('pad1', 'pad1', 0.0, 0.3, 1.0, 1.0)
    pad1.Draw()
    pad1.cd()
    histo_nominal.SetTitle(f"histo_{sample}_{systematic}")
    histo_nominal.GetYaxis().SetRangeUser(0.0,y_axis_max)
    histo_nominal.Draw()
    histo_up.Draw("same")
    histo_down.Draw("same")

    # Prepare ratio histograms
    histo_ratio_nominal = histo_nominal.Clone()
    histo_ratio_nominal.Divide(histo_nominal)
    histo_ratio_nominal.SetLineColor(ROOT.kBlue+1)

    histo_ratio_up = histo_up.Clone()
    histo_ratio_up.Divide(histo_nominal)
    histo_ratio_up.SetLineColor(ROOT.kGreen+1)
    
    histo_ratio_down = histo_down.Clone()
    histo_ratio_down.Divide(histo_nominal)
    histo_ratio_down.SetLineColor(ROOT.kRed+1)

    # Create smaller pad for ratio plots
    c1.cd()    
    pad2 = ROOT.TPad('pad2', 'pad2', 0.0, 0.0, 1.0, 0.3)
    pad2.SetTopMargin(0.0)
    pad2.SetBottomMargin(0.4)
    pad2.Draw()
    pad2.cd()
    histo_ratio_up.SetTitle("")
    histo_ratio_up.GetYaxis().SetRangeUser(0,2)
    histo_ratio_up.GetYaxis().SetLabelSize(0.06)
    histo_ratio_up.GetXaxis().SetLabelSize(0.08)
    histo_ratio_up.GetXaxis().SetTitle(variable)
    histo_ratio_up.GetXaxis().SetTitleSize(0.10)
    histo_ratio_up.Draw()
    histo_ratio_down.Draw("same")
    histo_ratio_nominal.Draw("hist p,same")

    # Create legend and plot it on the main pad
    pad1.cd()
    leg = ROOT.TLegend(0.15, 0.70, 0.80, 0.85)
    leg.SetLineColor(0)
    leg.AddEntry(histo_nominal,"Nominal","l");
    leg.AddEntry(histo_up,     "Syst. Up","l");
    leg.AddEntry(histo_down,   "Syst. Down","l");
    leg.Draw('same')
    
    output_file_name = opt.outputDir + "/" + sample + "_" + cut + "_" + variable + "_" + systematic 
    print("Output file complete path = {}".format(output_file_name))

    c1.Print(f"{output_file_name}.png")
    # c1.Print(f"{output_file_name}.pdf")

    c1.Close()
    
    del c1
    del pad1
    del pad2

if __name__ == '__main__':

    sys.argv = argv

    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    
    parser.add_option('--inputFile',  dest='inputFile',  help='input file with histograms',  default='DEFAULT')
    # parser.add_option('--cut',        dest='cut',        help='cut to inspect',              default='DEFAULT')
    # parser.add_option('--variable',   dest='variable',   help='variable to inspect',         default='DEFAULT')
    # parser.add_option('--sample',     dest='sample',     help='sample to inspect',           default='DEFAULT')
    parser.add_option('--outputDir',  dest='outputDir',  help='output directory',            default='DEFAULT')
 
    # read default parsing options as well
    (opt, args) = parser.parse_args()

    sys.argv.append( '-b' )
    ROOT.gROOT.SetBatch()

    print("Input file       = {}".format(opt.inputFile))
    # print("Cut              = {}".format(opt.cut))
    # print("Variable         = {}".format(opt.variable))
    # print("Sample           = {}".format(opt.sample))
    print("Output directory = {}".format(opt.outputDir))

    # Exceptions
    if opt.inputFile == 'DEFAULT' :
        raise ValueError("Please insert input file with histograms")
    inputFile = opt.inputFile
    
    # if opt.cut == 'DEFAULT' :
    #     raise ValueError("Please insert cut to inspect")
    # cut = opt.cut
    
    # if opt.variable == 'DEFAULT' :
    #     raise ValueError("Please insert variable to inspect")
    # variable = opt.variable

    # if opt.sample == 'DEFAULT' :
    #     raise ValueError("Please insert sample to inspect")
    # variable = opt.variable
    
    if opt.outputDir == 'DEFAULT' :
        raise ValueError("Please insert output directory")
    outputDir = opt.outputDir
    os.system(f'mkdir -p {outputDir}')
    
    cuts        = [
        'hww2l2v_13TeV_WH_SS_mm_2j_SS_CR_plus_pt2ge20',
        'hww2l2v_13TeV_WH_SS_mm_2j_SS_CR_minus_pt2ge20',
        'hww2l2v_13TeV_WH_SS_em_2j_SS_CR_plus_pt2ge20',
        'hww2l2v_13TeV_WH_SS_em_2j_SS_CR_minus_pt2ge20',
        'hww2l2v_13TeV_WH_SS_ee_2j_SS_CR_plus_pt2ge20',
        'hww2l2v_13TeV_WH_SS_ee_2j_SS_CR_minus_pt2ge20',
        'hww2l2v_13TeV_WH_SS_mm_1j_SS_CR_plus_pt2ge20',
        'hww2l2v_13TeV_WH_SS_mm_1j_SS_CR_minus_pt2ge20',
        'hww2l2v_13TeV_WH_SS_em_1j_SS_CR_plus_pt2ge20',
        'hww2l2v_13TeV_WH_SS_em_1j_SS_CR_minus_pt2ge20',
        'hww2l2v_13TeV_WH_SS_ee_1j_SS_CR_plus_pt2ge20',
        'hww2l2v_13TeV_WH_SS_ee_1j_SS_CR_minus_pt2ge20',
    ]
    variables   = ['pt1','pt2','mll','mlljj20'] # ,'eta1','jetpt1','jeteta1','jetpt2','jeteta2','puppimet']
    samples     = ['Fake_em', 'Fake_ee', 'Fake_mm']
    systematics = ['CMS_WH_hww_fake_e_2018','CMS_WH_hww_fake_m_2018','CMS_WH_hww_fake_stat_m_2018','CMS_WH_hww_fake_reweight_mm_2018','CMS_WH_hww_fake_reweight_em_2018','CMS_WH_hww_fake_reweight_ee_2018']
    
    for cut in cuts:
        for variable in variables:
            for sample in samples:
                for syst in systematics:
                    # Skip some meaningless combinations
                    if 'e_2018' in syst and 'mm' in sample: continue 
                    if 'm_2018' in syst and 'ee' in sample: continue
                    if 'ee' in cut and ('mm' in sample or 'em' in sample): continue
                    if 'em' in cut and ('mm' in sample or 'ee' in sample): continue
                    if 'mm' in cut and ('ee' in sample or 'em' in sample): continue
                    if 'ee' in sample and ('mm' in syst or 'em' in syst): continue
                    if 'em' in sample and ('mm' in syst or 'ee' in syst): continue
                    if 'mm' in sample and ('ee' in syst or 'em' in syst): continue
                    # Run the macro
                    print(f"Running on: {cut}, {variable}, {sample}, {syst}")
                    syst_analyzer(inputFile, cut, variable, sample, syst, outputDir)
