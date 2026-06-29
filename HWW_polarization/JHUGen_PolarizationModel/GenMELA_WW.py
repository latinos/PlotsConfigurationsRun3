
import ROOT
import uproot
import numpy as np
import pandas as pd
import mplhep as hep
import matplotlib.pyplot as plt
import subprocess

import argparse
import sys
import os
import time
import json
from pathlib import Path

ROOT.gROOT.SetBatch(True)
ROOT.TH1.SetDefaultSumw2(True)
ROOT.DisableImplicitMT()

def defaultParser():
    parser = argparse.ArgumentParser(add_help=False)

    def list_of_strings(arg):
        return arg.split(',')

    parser.add_argument(
        "-i",
        "--inDir",
        type=str,
        help="prefix for the job input",
        required=False,
        default="",
    )

    return parser

def createInputBranches(inFile):

    ####################
    #################### Code to test the gen. level polarized ME reweight with JHUGen / MELA
    ####################
    
    inTree = "Events"
    outFile = os.environ["TMPDIR"] + "/" + inFile.split("/")[-1]
    
    ROOT.gSystem.Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/MELACalc/JHUGen-v757.3/JHUGenMELA/MELA/data/el9_amd64_gcc12/libmcfm_711.so","", ROOT.kTRUE)
    ROOT.gSystem.Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/MELACalc/JHUGen-v757.3/JHUGenMELA/MELA/data/el9_amd64_gcc12/libJHUGenMELAMELA.so","", ROOT.kTRUE)
    ROOT.gSystem.Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/IvyFramework/IvyDataTools/lib/libIvyFrameworkIvyDataTools.so","", ROOT.kTRUE)
    ROOT.gSystem.Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/IvyFramework/IvyAutoMELA/lib/libIvyFrameworkIvyAutoMELA.so","", ROOT.kTRUE)
    ROOT.gSystem.Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/MelaAnalytics/GenericMEComputer/lib/libMelaAnalyticsGenericMEComputer.so","", ROOT.kTRUE)
    ROOT.gSystem.Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/MelaAnalytics/EventContainer/lib/libMelaAnalyticsEventContainer.so","", ROOT.kTRUE)
    ROOT.gSystem.Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/MelaAnalytics/CandidateLOCaster/lib/libMelaAnalyticsCandidateLOCaster.so","", ROOT.kTRUE)
    
    # Compile
    
    #gSystem->Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/MELACalc/JHUGen-v757.3/JHUGenMELA/MELA/data/el9_amd64_gcc12/libmcfm_711.so", "", true);
    #gSystem->Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/MELACalc/JHUGen-v757.3/JHUGenMELA/MELA/data/el9_amd64_gcc12/libJHUGenMELAMELA.so", "", true);
    #gSystem->Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/IvyFramework/IvyDataTools/lib/libIvyFrameworkIvyDataTools.so", "", true);
    #gSystem->Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/IvyFramework/IvyAutoMELA/lib/libIvyFrameworkIvyAutoMELA.so", "", true);
    #gSystem->Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/MelaAnalytics/GenericMEComputer/lib/libMelaAnalyticsGenericMEComputer.so", "", true);
    #gSystem->Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/MelaAnalytics/EventContainer/lib/libMelaAnalyticsEventContainer.so", "", true);
    #gSystem->Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/MelaAnalytics/CandidateLOCaster/lib/libMelaAnalyticsCandidateLOCaster.so", "", true);
    
    # -----
    
    ROOT.gSystem.Load("/afs/cern.ch/work/s/sblancof/private/Run2Analysis/sendEOSJobs/JHUGen_PolarizationModel/GenMELA_WW_cc.so","", ROOT.kTRUE)
    #ROOT.gSystem.Load("/afs/cern.ch/work/s/sblancof/private/Run2Analysis/sendEOSJobs/JHUGen_PolarizationModel/GenMELA_WW_2016_cc.so","", ROOT.kTRUE)
    
    ROOT.gInterpreter.Declare("GEN_POLARIZATION b(1);")
    #ROOT.gInterpreter.Declare("GEN_POLARIZATION_2016 b(1);")
    
    df = ROOT.RDataFrame(inTree, inFile)
    df = df.Define(
        "MELAOutput",
        "b(nLHEPart,LHEPart_pt,LHEPart_eta,LHEPart_phi,LHEPart_mass,LHEPart_incomingpz,LHEPart_pdgId,LHEPart_status,LHEPart_spin,GenPart_genPartIdxMother,GenPart_pdgId,GenPart_status,GenPart_pt,GenPart_eta,GenPart_phi,GenPart_mass,Generator_x1,Generator_x2,Generator_id1,Generator_id2)"
    )
    
    df = df.Define("LHEDaughterId", "MELAOutput[0]")
    df = df.Define("LHEDaughterPt", "MELAOutput[1]")
    df = df.Define("LHEDaughterEta", "MELAOutput[2]")
    df = df.Define("LHEDaughterPhi", "MELAOutput[3]")
    df = df.Define("LHEDaughterMass", "MELAOutput[4]")
    df = df.Define("LHEAssociatedParticlePt", "MELAOutput[5]")
    df = df.Define("LHEAssociatedParticleEta", "MELAOutput[6]")
    df = df.Define("LHEAssociatedParticlePhi", "MELAOutput[7]")
    df = df.Define("LHEAssociatedParticleMass", "MELAOutput[8]")
    df = df.Define("LHEAssociatedParticleId", "MELAOutput[9]")
    df = df.Define("LHEMotherId", "MELAOutput[10]")
    df = df.Define("LHEMotherPz", "MELAOutput[11]")
    df = df.Define("LHEMotherE", "MELAOutput[12]")
    
    df = df.Define("otherVars", "MELAOutput[13]")
    
    df = df.Define("qH", "otherVars[0]")
    df = df.Define("mV1", "otherVars[1]")
    df = df.Define("mV2", "otherVars[2]") 
    df = df.Define("costheta1", "otherVars[3]")
    df = df.Define("costheta2", "otherVars[4]")
    df = df.Define("Phi", "otherVars[5]")
    df = df.Define("costhetastar", "otherVars[6]")
    df = df.Define("Phi1", "otherVars[7]")
    df = df.Define("genMass", "otherVars[8]")
    
    columnsToStore = [
        "LHEDaughterId",
        "LHEDaughterPt",
        "LHEDaughterEta",
        "LHEDaughterPhi",
        "LHEDaughterMass",
        "LHEAssociatedParticlePt",
        "LHEAssociatedParticleEta",
        "LHEAssociatedParticlePhi",
        "LHEAssociatedParticleMass",
        "LHEAssociatedParticleId",
        "LHEMotherId",
        "LHEMotherPz",
        "LHEMotherE",
        "qH",
        "mV1",
        "mV2",
        "costheta1",
        "costheta2",
        "Phi",
        "costhetastar",
        "Phi1",
        "genMass",
        #"mll",
        #"dphill",
        #"XSWeight"
    ]
    
    print("Making a snapshot")

    opts = ROOT.RDF.RSnapshotOptions()
    #opts.fLazy = True
    opts.fMode = "UPDATE"
    opts.fOverwriteIfExists = True
    opts.fCompressionAlgorithm = ROOT.ROOT.kLZMA
    opts.fCompressionLevel = 9
    
    df.Snapshot("Events", outFile, columnsToStore, opts) # RECREATE
    print("DONE.")


def main():
    parser = defaultParser()
    args = parser.parse_args()

    inFile = args.inDir

    print("Run MELA variable builder -------")

    createInputBranches(inFile)


if __name__ == '__main__':
    main()
    print("DONE!")
    
"""
df = df.Define("weight", "XSWeight * 137.54")
df = df.Define("polWeight", "MELAOutput[0] * weight")
df = df.Define("qH", "MELAOutput[1]")
df = df.Define("mV1", "MELAOutput[2]")
df = df.Define("mV2", "MELAOutput[3]")
df = df.Define("costheta1", "MELAOutput[4]")
df = df.Define("costheta2", "MELAOutput[5]")
df = df.Define("Phi", "MELAOutput[6]")
df = df.Define("costhetastar", "MELAOutput[7]")
df = df.Define("Phi1", "MELAOutput[8]")
df = df.Define("genMass", "MELAOutput[9]")

h_mV1 = df.Histo1D(("hist_mV1", "hist_mV1", 64, 70., 130.), "mV1", "weight")
h_mV1_pol = df.Histo1D(("hist_mV1_pol", "hist_mV1_pol", 64, 70., 130.), "mV1", "polWeight")

h_mV2 = df.Histo1D(("hist_mV2", "hist_mV2", 64, 0., 70.), "mV2", "weight")
h_mV2_pol = df.Histo1D(("hist_mV2_pol", "hist_mV2_pol", 64, 0., 70.), "mV2", "polWeight")

h_genMass = df.Histo1D(("hist_genMass", "hist_genMass", 64, 90., 200.), "genMass", "weight")
h_genMass_pol = df.Histo1D(("hist_genMass_pol", "hist_genMass_pol", 64, 90., 200.), "genMass", "polWeight")

h_costheta1 = df.Histo1D(("hist_costheta1", "hist_costheta1", 64, -1., 1.), "costheta1", "weight")
h_costheta1_pol = df.Histo1D(("hist_costheta1_pol", "hist_costheta1_pol", 64, -1., 1.), "costheta1", "polWeight")

h_costheta2 = df.Histo1D(("hist_costheta2", "hist_costheta2", 64, -1., 1.), "costheta2", "weight")
h_costheta2_pol = df.Histo1D(("hist_costheta2_pol", "hist_costheta2_pol", 64, -1., 1.), "costheta2", "polWeight")

h_costhetastar = df.Histo1D(("hist_costhetastar", "hist_costhetastar", 64, -1., 1.), "costhetastar", "weight")
h_costhetastar_pol = df.Histo1D(("hist_costhetastar_pol", "hist_costhetastar_pol", 64, -1., 1.), "costhetastar", "polWeight")

h_Phi = df.Histo1D(("hist_Phi", "hist_Phi", 64, -3.14, 3.14), "Phi", "weight")
h_Phi_pol = df.Histo1D(("hist_Phi_pol", "hist_Phi_pol", 64, -3.14, 3.14), "Phi", "polWeight")

tfile = ROOT.TFile.Open("JHUGen_reweight_histograms.root", "RECREATE")
tfile.cd()
h_mV1.Clone().Write()
h_mV1_pol.Clone().Write()
h_mV2.Clone().Write()
h_mV2_pol.Clone().Write()
h_genMass.Clone().Write()
h_genMass_pol.Clone().Write()
h_costheta1.Clone().Write()
h_costheta1_pol.Clone().Write()
h_costheta2.Clone().Write()
h_costheta2_pol.Clone().Write()
h_costhetastar.Clone().Write()
h_costhetastar_pol.Clone().Write()
h_Phi.Clone().Write()
h_Phi_pol.Clone().Write()
tfile.Close()
"""

