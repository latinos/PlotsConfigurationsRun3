import os
import copy
import inspect

# /afs/cern.ch/user/n/ntrevisa/work/latinos/Run3/PlotsConfigurationsRun3/FakeRate/2016noHIPM_v9

configurations = os.path.realpath(inspect.getfile(inspect.currentframe())) # this file
configurations = os.path.dirname(configurations) # 2016noHIPM_v9
configurations = os.path.dirname(configurations) # FakeRate

aliases = {}
aliases = OrderedDict()

mc = [skey for skey in samples if skey not in ('Fake', 'DATA')]


# Evaluate BDT discriminant
aliases['Lepton_mvaTTH_UL'] = {
    'linesToAdd'     : [f'#include "{configurations}/macros/ttH_MVA_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('ttH_MVA_reader ttHMVA = ttH_MVA_reader(\"BDTG\",\"{configurations}/data/UL20_el_TTH-like_2016_BDTG.weights.xml\",\"BDTG\",\"{configurations}/data/UL20_mu_TTH-like_2016_BDTG.weights.xml\");')"],
    'expr'           : 'ttHMVA(nLepton,Lepton_pdgId,Lepton_electronIdx,Electron_jetIdx,event,Electron_mvaTTH,Electron_mvaFall17V2noIso_WPL,Electron_lostHits,Electron_pt,Electron_eta,Electron_pfRelIso03_all,Electron_miniPFRelIso_chg,Electron_miniPFRelIso_all,Electron_jetNDauCharged,Electron_jetPtRelv2,Electron_jetRelIso,Jet_btagDeepFlavB,Electron_sip3d,Electron_dxy,Electron_dz,Electron_mvaFall17V2noIso,Lepton_muonIdx,Muon_jetIdx,Muon_mvaTTH,Muon_looseId,Muon_isGlobal,Muon_isTracker,Muon_isPFcand,Muon_mediumId,Muon_pt,Muon_eta,Muon_pfRelIso03_all,Muon_miniPFRelIso_chg,Muon_miniPFRelIso_all,Muon_jetNDauCharged,Muon_jetPtRelv2,Muon_jetRelIso,Muon_sip3d,Muon_dxy,Muon_dz,Muon_segmentComp)',
    'samples': ['DATA','DATA_unprescaled'],
}

# LepCut2l__ele_mvaFall17V2Iso_WP90__mu_cut_Tight80x
eleWP = 'mvaFall17V2Iso_WP90'
muWP  = 'cut_Tight80x'

aliases['LepWPCut2l'] = {
    # 'expr': 'LepCut2l__ele_' + eleWP + '__mu_' + muWP,
    'expr': 'LepCut2l__ele_mvaFall17V2Iso_WP90__mu_cut_Tight80x*\
     ( ((abs(Lepton_pdgId[0])==13 && Muon_mvaTTH[Lepton_muonIdx[0]]>0.82) || (abs(Lepton_pdgId[0])==11 && Lepton_mvaTTH_UL[0]>0.90)) \
    && ((abs(Lepton_pdgId[1])==13 && Muon_mvaTTH[Lepton_muonIdx[1]]>0.82) || (abs(Lepton_pdgId[1])==11 && Lepton_mvaTTH_UL[1]>0.90)) )',
    'samples': mc + ['DATA','DATA_unprescaled']
}

aliases['LepWPCut1l'] = {
    'expr': '(abs(Lepton_pdgId[0])==11 && Lepton_isTightElectron_'+eleWP+'[0]>0.5 && Lepton_mvaTTH_UL[0]>0.90) \
          || (abs(Lepton_pdgId[0])==13 && Lepton_isTightMuon_'+muWP+'[0]>0.5 && Muon_mvaTTH[Lepton_muonIdx[0]]>0.82)',
    'samples': mc + ['DATA','DATA_unprescaled']
}

# No jet with pt > 30 GeV
aliases['zeroJet'] = {
    'expr': 'Alt(CleanJet_pt, 0, 0) < 30.'
}

aliases['oneJet'] = {
    'expr': 'Alt(CleanJet_pt, 0, 0) > 30. && Alt(CleanJet_pt, 1, 0) < 30.'
}

aliases['multiJet'] = {
    'expr': 'Alt(CleanJet_pt, 1, 0) > 30.'
}

jet_pt_thrs = [10, 15, 20, 25, 30, 35, 40, 45]

for jet_pt_threshold in jet_pt_thrs:

    # DeltaR(lep,jet)
    aliases[f'drlj_{jet_pt_threshold}'] = {
        'linesToAdd': [f'#include "{configurations}/macros/away_jet.cc"'],
        'class': 'drlj',
        'args' : f'{jet_pt_threshold},nLepton,nCleanJet,Lepton_pt,Lepton_eta,Lepton_phi,CleanJet_pt,CleanJet_eta,CleanJet_phi',
        'samples': mc + ['DATA','DATA_unprescaled']
}

# DeltaR (l1,j1)
aliases['dRl1j1'] = {
    'expr': 'CleanJet_pt[0] >= 10 ? TMath::Sqrt(dphilep1jet1*dphilep1jet1 + (Lepton_eta[0]-CleanJet_eta[0])*(Lepton_eta[0]-CleanJet_eta[0])) : -9999',
}

# Cone pt 
aliases['Lepton_conept'] = {
    'expr': 'LeptonConePt(Lepton_pt, Lepton_pdgId, Lepton_electronIdx, Lepton_muonIdx, Electron_jetRelIso, Muon_jetRelIso)',
    'linesToAdd': [f'#include "{configurations}/../utils/macros/LeptonConePt_class.cc"'],
    'samples': mc + ['DATA', 'DATA_unprescaled']
}
