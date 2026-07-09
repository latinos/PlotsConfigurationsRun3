
import ROOT
import uproot
import numpy as np
import pandas as pd
import mplhep as hep
import awkward
import matplotlib.pyplot as plt
import subprocess

import argparse
import sys
import os
import time
import json
from pathlib import Path

from mkShapesRDF.lib.parse_cpp import ParseCpp
from mkShapesRDF.processor.framework.mRDF import mRDF
from mkShapesRDF.processor.modules.Snapshot import *

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

    parser.add_argument(
        "-o",
        "--outDir",
        type=str,
        help="prefix for the job output",
        required=False,
        default="",
    )
    
    return parser

def index_sub(string, sub):
    try:
        return string.index(sub)
    except ValueError:
        return -10000

def createInputBranches(inFile, outDir):

    ####################
    #################### Code to test the gen. level polarized ME reweight with JHUGen / MELA
    ####################
    
    inTree = "Events"
    values = []

    # ElepTup
    # ElepTdo
    # ElepTup_suffix
    # ElepTdo_suffix

    # ElepTup
    # ElepTdo
    # EmbElepTup_suffix
    # EmbElepTdo_suffix

    # MupTup
    # MupTdo
    # MupTup_suffix
    # MupTdo_suffix

    # MupTup
    # MupTdo
    # EmbMupTup_suffix
    # EmbMupTdo_suffix

    # jes_systs    = ['JESAbsolute','JESAbsolute_2017','JESBBEC1','JESBBEC1_2017','JESEC2','JESEC2_2017','JESFlavorQCD','JESHF','JESHF_2017','JESRelativeBal','JESRelativeSample_2017']
    # RDF__JESup_suffix
    # RDF__JESdo_suffix

    # JERup
    # JERdo
    # JERup_suffix
    # JERdo_suffix

    # METup
    # METdo
    # METup_suffix
    # METdo_suffix

    ROOT.gInterpreter.Declare('#include "/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/mkShapesRDF/include/headers.hh"')
    
    ROOT.gSystem.Load("/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/JHUGenMELA/MELA/data/slc7_amd64_gcc920/libmcfm_705.so","", ROOT.kTRUE)
    ROOT.gSystem.Load("/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/JHUGenMELA/MELA/data/slc7_amd64_gcc920/libJHUGenMELAMELA.so","", ROOT.kTRUE)
    ROOT.gSystem.Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/RecoMELA_VBF_cc.so","", ROOT.kTRUE)
    ROOT.gInterpreter.Declare("RECOMELA_VBF a;")

    ROOT.gSystem.Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/lib/libmomemta.so","", ROOT.kTRUE)
    ROOT.gSystem.Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/RecoMoMEMta_VBF_cc.so","", ROOT.kTRUE)
    ROOT.gInterpreter.Declare("RecoMoMEMta_VBF EvMoMEMta;")

    baseFolder = inFile.split("/nanoLatino")[0]
    fileName = inFile.split("/")[-1]
    
    ROOT.gSystem.Load("/eos/user/s/sblancof/Run3Analysis/mkShapesRDF/examples/extended/evaluate_RF_polarization_cc.so","", ROOT.kTRUE)
    if "2022EE" in baseFolder.split("/")[-1]:
        ROOT.gInterpreter.Declare('EvaluateRF rf_evaluator("2022EE");')
    elif "2022" in baseFolder.split("/")[-1]:
        ROOT.gInterpreter.Declare('EvaluateRF rf_evaluator("2022");')
    elif "2023BPix" in baseFolder.split("/")[-1]:
        ROOT.gInterpreter.Declare('EvaluateRF rf_evaluator("2023BPix");')
    elif "2023" in baseFolder.split("/")[-1]:
        ROOT.gInterpreter.Declare('EvaluateRF rf_evaluator("2023");')
    elif "2024" in baseFolder.split("/")[-1]:
        ROOT.gInterpreter.Declare('EvaluateRF rf_evaluator("2024");')


    folders = [
        "leptonResolution", "leptonScale",
        "jer",
        "unclustEn",
        "jesRegroed_FlavorQCD", "jesRegroed_HF_YEAR", "jesRegroed_HF", "jesRegroed_Absolute_YEAR",
        "jesRegroed_RelativeBal", "jesRegroed_Absolute", "jesRegroed_RelativeSample_YEAR",
        "jesRegroed_BBEC1_YEAR", "jesRegroed_BBEC1", "jesRegroed_EC2_YEAR", "jesRegroed_EC2"
    ]

    ###### Exceptions
    exceptFolders = []
    excepts = []    

    ####### Copy input files
    print("Copy input files...")
    proc = subprocess.Popen(f"cp {inFile} {os.environ['TMPDIR']}", shell=True)
    proc.wait()

    for folder in folders:
        
        if folder in exceptFolders:
            continue

        file_up = baseFolder + "__" + folder + "up_suffix/" + fileName
        file_do = baseFolder + "__" + folder + "do_suffix/" + fileName

        name_up = fileName.split(".root")[0] + "__" + folder + "up_suffix.root"
        name_do = fileName.split(".root")[0] + "__" + folder + "do_suffix.root"

        proc = subprocess.Popen(f"cp {file_up} {os.environ['TMPDIR']}/{name_up}", shell=True)
        proc.wait()

        proc = subprocess.Popen(f"cp {file_do} {os.environ['TMPDIR']}/{name_do}", shell=True)
        proc.wait()

    print("All copied!")
    #############    
    
    tnom = ROOT.TChain("Events")

    #tnom.Add(inFile)
    tnom.Add(os.environ['TMPDIR']+"/"+fileName)

    print("---- [DEBUG] -----")
    print(baseFolder)
    print(fileName)
    
    for folder in folders:

        if folder.startswith("jes") and "YEAR" in folder:
            if "2022EE" in baseFolder.split("/")[-1]:
                folder = folder.replace("YEAR", "2022EE")
            elif "2022" in baseFolder.split("/")[-1]:
                folder = folder.replace("YEAR", "2022")
            elif "2023BPix" in baseFolder.split("/")[-1]:
                folder = folder.replace("YEAR", "2023BPix")
            elif "2023" in baseFolder.split("/")[-1]:
                folder = folder.replace("YEAR", "2023")
            elif "2024" in baseFolder.split("/")[-1]:
                folder = folder.replace("YEAR", "2024")
        
        if folder in exceptFolders:
            continue
        
        tfriend_up = ROOT.TChain("Events")
        tfriend_do = ROOT.TChain("Events")
        
        #file_up = baseFolder + "__" + folder + "up_suffix/" + fileName
        #file_do = baseFolder + "__" + folder + "do_suffix/" + fileName        

        file_up = os.environ['TMPDIR']+"/"+fileName.split(".root")[0] + "__" + folder + "up_suffix.root"
        file_do = os.environ['TMPDIR']+"/"+fileName.split(".root")[0] + "__" + folder + "do_suffix.root"
        
        tfriend_up.Add(file_up)
        tfriend_do.Add(file_do)

        tnom.AddFriend(tfriend_up)
        tnom.AddFriend(tfriend_do)
        
    #df = ROOT.RDataFrame(tnom)
    df = mRDF()
    df = df.readRDF(tnom)

    usedVars = [
        "mll",
        "mth",
        "mtw1",
        "mtw2",
        "mjj",
        "mcollWW",
        "ptll",
        "Ctot",
        "dphilmet1",
        "dphilmet2",
        "dphill",
        "detall",
        "dphijj",
        "detajj",
        "dphilep1jet1",
        "dphilep2jet1",
        "dphilep1jet2",
        "dphilep2jet2",
        "btagDeepFlavB",
        "btagDeepFlavB_1",
        "drll",
        "mpmet",
        "mTi",
        "Jet_btagDeepFlavB"
    ]
    
    columnNames = [str(col) for col in df.GetColumnNames()]
    print("Number of input branches: " + str(len(columnNames)))
    print(columnNames[0:20])

    print("[DEBUG] Varied ElepT columns")
    for col in columnNames:
        if "Lepton_pt" in col:
            print(col)

    ###### Systematic variations
    for syst in folders:        
        
        if syst.startswith("jes") and "YEAR" in syst:
            if "2022EE" in baseFolder.split("/")[-1]:
                syst = syst.replace("YEAR", "2022EE")
            elif "2022" in baseFolder.split("/")[-1]:
                syst = syst.replace("YEAR", "2022")
            elif "2023BPix" in baseFolder.split("/")[-1]:
                syst = syst.replace("YEAR", "2023BPix")
            elif "2023" in baseFolder.split("/")[-1]:
                syst = syst.replace("YEAR", "2023")
            elif "2024" in baseFolder.split("/")[-1]:
                syst = syst.replace("YEAR", "2024")

        variation = syst + "do"
        separator = "_"

        if syst in excepts:
            continue
        
        variedCols = list(
            filter(lambda k: k.endswith(variation), columnNames)
        )
        
        if len(variedCols) == 0:
            print(f"No varied columns for {variation}")
            sys.exit()
            
        baseCols = list(
            map(
                lambda k: (
                    k[
                        index_sub(k, "Events.")
                        + len("Events.") : -len(
                            separator + variation
                        )
                    ]
                    if "Events" in k
                    else k[: -len(separator + variation)]
                ),
                variedCols,
            )
        )
        for baseCol in baseCols:

            if not (baseCol.startswith("Lepton") or baseCol.startswith("CleanJet") or baseCol.startswith("PuppiMET") or (baseCol in usedVars)):
                continue            

            # Example: mjj_jesRegroed_Absoluteup
            varNameDown = baseCol + separator + syst + "do"
            varNameUp = baseCol + separator + syst + "up"
            _type = df.df.GetColumnType(baseCol)

            expr = (
                ParseCpp.RVecExpression(_type)
                + "{"
                + f"{varNameUp}, {varNameDown}"
                + "}"
            )            
            print(f"df = df.Vary({baseCol},{expr},['up', 'do'],{syst})")
            df = df.Vary(
                baseCol,
                expr,
                ["up", "do"],
                syst,
            )            

    df = df.Define(
        "zeroJet",
        "Alt(CleanJet_pt,0, 0) < 30."
    )
    df = df.Define(
        "oneJet",
        "Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0"
    )
    df = df.Define(
        "multiJet",
        "Alt(CleanJet_pt,1, 0) > 30."
    )
    
    df = df.Define(
        "D_ME",
        "a(nCleanJet, nLepton, PuppiMET_pt, PuppiMET_phi, Lepton_pt, Lepton_phi, Lepton_eta, CleanJet_pt, CleanJet_phi, CleanJet_eta, Lepton_pdgId)"
    )
    df = df.Define(
        "D_VBF_QCD",
        "D_ME[0]"
    )
    df = df.Define(
        "D_VBF_VH",
        "D_ME[1]"
    )    
    df = df.Define(
        "D_QCD_VH",
        "D_ME[2]"
    )
    df.DropColumns("D_ME")
    
    df = df.Define(
        "D_VBF_DY",
        "EvMoMEMta(nCleanJet, nLepton, PuppiMET_pt, PuppiMET_phi, Lepton_pt[0], Lepton_pt[1], Lepton_phi[0], Lepton_phi[1], Lepton_eta[0], Lepton_eta[1], CleanJet_pt[0], CleanJet_pt[1], CleanJet_phi[0], CleanJet_phi[1], CleanJet_eta[0], CleanJet_eta[1], Lepton_pdgId[0], Lepton_pdgId[1])"
    )

    df = df.Define(
        "Ctot", 
        "detajj!=0 ? log((abs(2 * Lepton_eta[0] - CleanJet_eta[0] - CleanJet_eta[1]) + abs(2 * Lepton_eta[1] - CleanJet_eta[0] - CleanJet_eta[1])) / detajj) : -1.0"
    )

    df = df.Define(
        "btagDeepFlavB",
        "Alt(Jet_btagDeepFlavB, Alt(CleanJet_jetIdx, 0, -1), -2.0)"
    )
    df = df.Define(
        "btagDeepFlavB_1",
        "Alt(Jet_btagDeepFlavB, Alt(CleanJet_jetIdx, 1, -1), -2.0)"
    )

    df.DropColumns("btagDeepFlavB")
    df.DropColumns("btagDeepFlavB_1")
    
    df = df.Define(
        "RandomForest_evaluator",
        "rf_evaluator(mll,mth,mtw1,mtw2,mjj,mcollWW,ptll,Ctot,Lepton_pt,Lepton_eta,Lepton_phi,dphilmet1,dphilmet2,dphill,detall,dphijj,detajj,dphilep1jet1,dphilep2jet1,dphilep1jet2,dphilep2jet2,btagDeepFlavB,btagDeepFlavB_1,drll,mpmet,PuppiMET_pt,PuppiMET_phi,D_VBF_QCD,D_VBF_VH,D_QCD_VH,D_VBF_DY,mTi,zeroJet,oneJet,multiJet)"
    )

    df.DropColumns("RandomForest_evaluator")

    df = df.Define(
        "RF_score_0J_LL",
        "RandomForest_evaluator[0][0]"
    )
    df = df.Define(
        "RF_score_0J_TT",
        "RandomForest_evaluator[0][1]"
    )
    df = df.Define(
        "RF_score_0J_Bkg",
        "RandomForest_evaluator[0][2]"
    )
    df = df.Define(
        "RF_score_1J_LL",
        "RandomForest_evaluator[1][0]"
    )
    df = df.Define(
        "RF_score_1J_TT",
        "RandomForest_evaluator[1][1]"
    )
    df = df.Define(
        "RF_score_1J_Bkg",
        "RandomForest_evaluator[1][2]"
    )
    df = df.Define(
        "RF_score_2J_LL",
        "RandomForest_evaluator[2][0]"
    )
    df = df.Define(
        "RF_score_2J_TT",
        "RandomForest_evaluator[2][1]"
    )
    df = df.Define(
        "RF_score_2J_Bkg",
        "RandomForest_evaluator[2][2]"
    )
    df = df.Define(
        "RF_score_VBF_LL",
        "RandomForest_evaluator[3][0]"
    )
    df = df.Define(
        "RF_score_VBF_TT",
        "RandomForest_evaluator[3][1]"
    )
    df = df.Define(
        "RF_score_VBF_Bkg",
        "RandomForest_evaluator[3][2]"
    )
    
    columnsToStore = [
        "D_VBF_QCD",
        "D_VBF_VH",
        "D_QCD_VH",
        "D_VBF_DY",
        "Ctot",
        "RF_score_0J_LL",
        "RF_score_0J_TT",
        "RF_score_0J_Bkg",
        "RF_score_1J_LL",
        "RF_score_1J_TT",
        "RF_score_1J_Bkg",
        "RF_score_2J_LL",
        "RF_score_2J_TT",
        "RF_score_2J_Bkg",
        "RF_score_VBF_LL",
        "RF_score_VBF_TT",
        "RF_score_VBF_Bkg"
    ]

    print(columnsToStore)

    allColumnNames = map(lambda k: str(k), df.GetColumnNames())
    filteredColumnNames = []
    for col in allColumnNames:
        for key in columnsToStore:
            if key in col:
                filteredColumnNames.append(col)                

                
    print("Making a snapshot")
    print("------> Branches to store:")
    print(filteredColumnNames)

    
    opts = ROOT.RDF.RSnapshotOptions()
    #opts.fLazy = True
    opts.fMode = "UPDATE"
    opts.fOverwriteIfExists = True
    opts.fCompressionAlgorithm = ROOT.ROOT.kLZMA
    opts.fCompressionLevel = 9

    tmpFile = os.environ['TMPDIR']+'/output.root'
    outFile = outDir + "/" + inFile.split("/")[-1]
    
    df.Snapshot("Events", tmpFile, filteredColumnNames, opts) # RECREATE

    proc = subprocess.Popen(f"mkdir -p {outDir}", shell=True)
    proc.wait()
    
    proc = subprocess.Popen(f"cp {tmpFile} {outFile}", shell=True)
    proc.wait()
    
    """
    snapshot = lambda : Snapshot(
        tmpOutputFilename=os.environ['TMPDIR']+'/'+fileName,
        columns=filteredColumnNames,
        #columns=["*"],
        eosPath=outDir,
        outputFilename=fileName,
        includeVariations=True,
        splitVariations=False,
        storeNominals=True
    )
    module = snapshot()
    df = module.run(df, values)
    
    snapshots = []
    snapshot_destinations = []

    print(values)
    
    for val in values:
        if "snapshot" == val[0]:
            snapshots.append(val[1])
            snapshot_destinations.append(val[2])

    for snapshot in snapshots:
        snapshot(df.df)

    finalFiles = []
    for destination in snapshot_destinations:
        copyFromInputFiles = destination[1]
        outputFilename = destination[0]
        
        if copyFromInputFiles:
            Snapshot.CopyFromInputFiles(outputFilename, files)

        outputFolderPath = destination[2]
        outputFilenameEOS = destination[3]

        # Create output folder
        proc = subprocess.Popen(f"mkdir -p {outputFolderPath}", shell=True)
        proc.wait()
        
        # Copy output file in output folder
        proc = subprocess.Popen(f"cp {outputFilename} {outputFolderPath}/{outputFilenameEOS}", shell=True)
        proc.wait()
        finalFiles.append(f'{outputFolderPath}/{outputFilenameEOS}')
        
        # Remove the output file from local
        proc = subprocess.Popen(f"rm {outputFilename}", shell=True)
        proc.wait()
    """
    print("DONE.")
    

def main():
    parser = defaultParser()
    args = parser.parse_args()

    inFile = args.inDir
    outDir = args.outDir

    print("Run MELA and RandomForest variable builder -------")

    createInputBranches(inFile, outDir)


if __name__ == '__main__':
    main()
    print("DONE!")
    
