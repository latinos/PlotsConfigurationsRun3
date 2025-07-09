import uproot
import numpy as np
import pandas as pd
import ROOT
import json
import sys
import os

ROOT.EnableImplicitMT(1)

#/eos/cms/store/group/phys_higgs/cmshww/calderon/HWWNano/Run2022EE_Prompt_nAODv12_Full2022v12/DATAl1loose2022EFGv12__fakeW/nanoLatino_MuonEG_Run2022E-Prompt-v1__part

from mkShapesRDF.lib.search_files import SearchFiles

headersPath = "/afs/cern.ch/work/s/sblancof/private/Run3Analysis/mkShapesRDF/mkShapesRDF/include/headers.hh"
ROOT.gInterpreter.Declare(f'#include "{headersPath}"')

searchFiles = SearchFiles()

_files = searchFiles.searchFiles("/eos/cms/store/group/phys_higgs/cmshww/calderon/HWWNano/Run2022EE_Prompt_nAODv12_Full2022v12/DATAl1loose2022EFGv12__fakeW/", "MuonEG_Run2022E-Prompt-v1")
_files = _files + searchFiles.searchFiles("/eos/cms/store/group/phys_higgs/cmshww/calderon/HWWNano/Run2022EE_Prompt_nAODv12_Full2022v12/DATAl1loose2022EFGv12__fakeW/", "MuonEG_Run2022F-Prompt-v1")
_files = _files	+ searchFiles.searchFiles("/eos/cms/store/group/phys_higgs/cmshww/calderon/HWWNano/Run2022EE_Prompt_nAODv12_Full2022v12/DATAl1loose2022EFGv12__fakeW/", "MuonEG_Run2022G-Prompt-v1")

_files = _files + searchFiles.searchFiles("/eos/cms/store/group/phys_higgs/cmshww/calderon/HWWNano/Run2022_ReReco_nAODv12_Full2022v12/DATAl1loose2022v12__fakeW/", "MuonEG_Run2022C-ReReco-v1")
_files = _files + searchFiles.searchFiles("/eos/cms/store/group/phys_higgs/cmshww/calderon/HWWNano/Run2022_ReReco_nAODv12_Full2022v12/DATAl1loose2022v12__fakeW/", "MuonEG_Run2022D-ReReco-v1")

#_files2 = searchFiles.searchFiles("/eos/cms/store/group/phys_higgs/cmshww/calderon/HWWNano/Run2022EE_Prompt_nAODv12_Full2022v12/DATAl1loose2022EFGv12__fakeW/", "Muon_Run2022E-Prompt-v1")
#_files2 = _files2 + searchFiles.searchFiles("/eos/cms/store/group/phys_higgs/cmshww/calderon/HWWNano/Run2022EE_Prompt_nAODv12_Full2022v12/DATAl1loose2022EFGv12__fakeW/", "Muon_Run2022F-Prompt-v1")
#_files2 = _files2 + searchFiles.searchFiles("/eos/cms/store/group/phys_higgs/cmshww/calderon/HWWNano/Run2022EE_Prompt_nAODv12_Full2022v12/DATAl1loose2022EFGv12__fakeW/", "Muon_Run2022G-Prompt-v1")

#_files2 = _files2 + searchFiles.searchFiles("/eos/cms/store/group/phys_higgs/cmshww/calderon/HWWNano/Run2022_ReReco_nAODv12_Full2022v12/DATAl1loose2022v12__fakeW/", "Muon_Run2022C-ReReco-v1")
#_files2 = _files2 + searchFiles.searchFiles("/eos/cms/store/group/phys_higgs/cmshww/calderon/HWWNano/Run2022_ReReco_nAODv12_Full2022v12/DATAl1loose2022v12__fakeW/", "Muon_Run2022D-ReReco-v1")

#print(_files)

events = []
first = True

df = ROOT.RDataFrame("Events", _files)
#df2 = ROOT.RDataFrame("Events", _files2)
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'cut_Tight_HWW'

bWP_loose_deepFlavB  = '0.0583'
bWP_medium_deepFlavB = '0.3086'
bWP_tight_deepFlavB  = '0.7183'
bAlgo = 'DeepFlavB'   
bWP   = bWP_loose_deepFlavB
bSF   = 'deepjet'

df = df.Define(
    "LepCut2",
    "_2lepOk ? (Lepton_isTightElectron_" + eleWP + "[0]>0.5 && Lepton_isTightMuon_" + muWP + "[0]>0.5) && (Lepton_isTightElectron_" + eleWP + "[1]>0.5 && Lepton_isTightMuon_" + muWP + "[1]>0.5) : false"
)

df = df.Define(
    "bVeto",
    f'Sum(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{bAlgo}, CleanJet_jetIdx) > {bWP}) == 0'
)

df = df.Filter('(Lepton_pt[0]>25 && Lepton_pt[1]>20 && Lepton_pdgId[0] * Lepton_pdgId[1] == -11*13 && Alt(Lepton_pt, 2, 0)<10.0 && mll>85 && bVeto)*(HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ)*LepCut2')

print("Check number of events in the signal region")
print("Only MuonEG dataset!!!")
print("Events -> " + str(df.Count().GetValue()))

'''
df2 = df2.Filter('(Lepton_pt[0]>25 && Lepton_pt[1]>20 && Lepton_pdgId[0] * Lepton_pdgId[1] == -11*13)*(LepCut2l__ele_'+eleWP+'__mu_'+muWP+')*!(HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ)*LepCut2l__ele_'+eleWP+'__mu_'+muWP)

results = df.AsNumpy(["event"])
results2 = df2.AsNumpy(["event"])

events = np.array(results["event"])
events2 = np.array(results2["event"])

events = np.concatenate((events, events2), axis=0)

#for ff in _files:
#    print(ff)
#    df = uproot.open(ff)
#    if first:
#        events = list(df["Events"]["event"].array())
#        first = False
#    else:
#        events = events + (list(df["Events"]["event"].array()))

array, counts = np.unique(events, return_counts=True)

#print(array)

print("--------------------------")

print(array[counts>1])
print(counts[counts>1])
print("------")
print("Summary-------")
print("Length event array: " + str(len(array)))
print("Number of events double counted: " + str(len(array[counts>1])))
print("Excess -> " + str(np.sum(counts[counts>1])))
'''
