import ROOT
import pandas as pd
import numpy as np
import uproot
import subprocess
import matplotlib.pyplot as plt
import awkward as ak

ROOT.EnableImplicitMT()

year = '2017'

#path_2016 = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer20UL16_106x_nAODv9_HIPM_Full2016v9/MCl1loose2016v9__MCCorr2016v9NoJERInHorn__l2tightOR2016v9/nanoLatino_TTTo2L2Nu__part*.root"
#path_2016 = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer20UL16_106x_nAODv9_noHIPM_Full2016v9/MCl1loose2016v9__MCCorr2016v9NoJERInHorn__l2tightOR2016v9/nanoLatino_TTTo2L2Nu__part*.root"
path_2017 = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer20UL17_106x_nAODv9_Full2017v9/MCl1loose2017v9__MCCorr2017v9NoJERInHorn__l2tightOR2017v9/nanoLatino_TTTo2L2Nu__part*.root"
#path_2018 = "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer20UL18_106x_nAODv9_Full2018v9/MCl1loose2018v9__MCCorr2018v9NoJERInHorn__l2tightOR2018v9/nanoLatino_TTTo2L2Nu__part*.root"

cmd = "find {}".format(path_2017)
fnames = subprocess.check_output(cmd, shell=True).strip().split(b'\n')
files = [fname.decode('ascii') for fname in fnames]

ROOT.gInterpreter.Declare('#include "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/mkShapesRDF/mkShapesRDF/include/headers.hh"')

df = ROOT.RDataFrame("Events", files[0:50])

_tmp = [
    'Lepton_pt[0] > 25.',
    'Lepton_pt[1] > 10.',
    '(abs(Lepton_pdgId[1]) == 13 || Lepton_pt[1] > 13.)',
    '(nLepton >= 2 && Alt(Lepton_pt,2, 0) < 10.)',
    'ptll>15',
    'mll > 12',
    'mth>40 && PuppiMET_pt>20 && mll > 12 && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13'
]

basic_sel = ' && '.join(_tmp)
df = df.Filter(basic_sel)

df = df.Define("MyCleanJet_pt", "CleanJet_pt[CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5]")
df = df.Define("MyCleanJet_eta", "CleanJet_eta[CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5]")
df = df.Define("MyCleanJet_jetIdx", "CleanJet_jetIdx[CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5]")
df = df.Define("MyCleanJet_btagDeepFlavB", "Take(Jet_btagDeepFlavB, MyCleanJet_jetIdx)")
df = df.Define("MyCleanJet_hadronFlavour", "Take(Jet_hadronFlavour, MyCleanJet_jetIdx)")

mydict = df.AsNumpy(["MyCleanJet_pt", "MyCleanJet_eta", "MyCleanJet_btagDeepFlavB", "MyCleanJet_hadronFlavour"])

branches = ["MyCleanJet_pt", "MyCleanJet_eta", "MyCleanJet_btagDeepFlavB", "MyCleanJet_hadronFlavour"]

def getBranchFlatten(events, branch):
    ak_array = [ak.Array(v) for v in events[branch]]
    np_array = ak.to_numpy(ak.flatten(ak_array))
    return np_array

df_np = {}
for key in branches:
    df_np[key] = getBranchFlatten(mydict, key)
df_ak = pd.DataFrame(df_np)

print("Save CSV file")
df_ak.to_csv("ttbar_2017_cleanjet.csv")
print("Saved!!")

pt_edges = np.array([   0.,   30.,   50.,   70.,  100.,  140.,  200.,  300.,  600., 1000.])
eta_edges = np.array([-2.5       , -1.47899997,  1.47899997,  2.5       ])

bjet_den = ROOT.TH2D("bjet_den", "bjet_den", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)
bjet_num = ROOT.TH2D("bjet_num", "bjet_num", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)
bjet_eff = ROOT.TH2D("bjet_eff", "bjet_eff", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)

cjet_den = ROOT.TH2D("cjet_den", "cjet_den", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)
cjet_num = ROOT.TH2D("cjet_num", "cjet_num", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)
cjet_eff = ROOT.TH2D("cjet_eff", "cjet_eff", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)

ljet_den = ROOT.TH2D("ljet_den", "ljet_den", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)
ljet_num = ROOT.TH2D("ljet_num", "ljet_num", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)
ljet_eff = ROOT.TH2D("ljet_eff", "ljet_eff", len(pt_edges)-1, pt_edges, len(eta_edges)-1, eta_edges)

wp = {
    '2016': 0.0508,
    '2016_postVFP': 0.0480,
    '2017': 0.0532,
    '2018': 0.0490,
}

total = len(df_ak)
for i in range(total):
    
    if (i%100000 == 0):
        print("Progress ---> " + str(100*i/total) + "%")
    
    jet_pt            = df_ak.loc[i].MyCleanJet_pt
    jet_eta           = df_ak.loc[i].MyCleanJet_eta
    jet_btagDeepFlavB = df_ak.loc[i].MyCleanJet_btagDeepFlavB
    jet_hadronFlavour = df_ak.loc[i].MyCleanJet_hadronFlavour
    
    if jet_hadronFlavour == 5:
        
        bjet_den.Fill(jet_pt, jet_eta)
        if jet_btagDeepFlavB > wp[year]:
            bjet_num.Fill(jet_pt, jet_eta)
        
    elif jet_hadronFlavour == 4:
        
        cjet_den.Fill(jet_pt, jet_eta)
        if jet_btagDeepFlavB > wp[year]:
            cjet_num.Fill(jet_pt, jet_eta)
            
    else:
        
        ljet_den.Fill(jet_pt, jet_eta)
        if jet_btagDeepFlavB > wp[year]:
            ljet_num.Fill(jet_pt, jet_eta)

            
bjet_eff = bjet_num.Clone()
bjet_eff.Divide(bjet_den)

cjet_eff = cjet_num.Clone()
cjet_eff.Divide(cjet_den)

ljet_eff = ljet_num.Clone()
ljet_eff.Divide(ljet_den)


file = ROOT.TFile(f"bTagEff_{year}_ttbar_DeepFlavB_loose.root", "RECREATE")
file.cd()

bjet_den.Clone().Write("bjet_den")
bjet_num.Clone().Write("bjet_num")
bjet_eff.Clone().Write("bjet_eff")

cjet_den.Clone().Write("cjet_den")
cjet_num.Clone().Write("cjet_num")
cjet_eff.Clone().Write("cjet_eff")

ljet_den.Clone().Write("ljet_den")
ljet_num.Clone().Write("ljet_num")
ljet_eff.Clone().Write("ljet_eff")

file.Close()
            
            
