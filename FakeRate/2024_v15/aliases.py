import os
import copy
import inspect

configurations = os.path.realpath(inspect.getfile(inspect.currentframe()))
configurations = os.path.dirname(configurations)
configurations = os.path.dirname(configurations) 

aliases = {}
aliases = OrderedDict()

mc = [skey for skey in samples if skey not in ('Fake', 'DATA')]

# LepCut2l__ele_cutBased_LooseID_tthMVA_Run3__mu_cut_TightID_pfIsoTight_HWW_tthmva_67
eleWP = 'cutBased_LooseID_tthMVA_Run3'
muWP  = 'cut_TightID_pfIsoTight_HWW_tthmva_67'

aliases['LepWPCut2l'] = {
    'expr': 'LepCut2l__ele_'+eleWP+'__mu_'+muWP,
    'samples': mc + ['DATA','DATA_unprescaled']
}

aliases['LepWPCut1l'] = {
    'expr': '(abs(Lepton_pdgId[0])==11 && Lepton_isTightElectron_'+eleWP+'[0]>0.5) \
          || (abs(Lepton_pdgId[0])==13 && Lepton_isTightMuon_'+muWP+'[0]>0.5)',
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

aliases['noJetInHorn'] = {
    'expr' : 'Sum(CleanJet_pt > 30 && CleanJet_pt < 50 && abs(CleanJet_eta) > 2.5 && abs(CleanJet_eta) < 3.0) == 0',
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

    # aliases[f'drlj_{jet_pt_threshold}'] = {
    #     'linesToAdd'     : [f'#include "{configurations}/macros/away_jet_class.cc"'],
    #     'linesToProcess' : [f"ROOT.gInterpreter.Declare('away_jet away_jet_{jet_pt_threshold} = away_jet();')"],
    #     'expr'           : f'away_jet_{jet_pt_threshold}({jet_pt_threshold},nLepton,nCleanJet,Lepton_pt,Lepton_eta,Lepton_phi,CleanJet_pt,CleanJet_eta,CleanJet_phi)',
    # 'samples': mc + ['DATA']
    # }


# DeltaR (l1,j1)
aliases['dRl1j1'] = {
    'expr': 'CleanJet_pt[0] >= 10 ? TMath::Sqrt(dphilep1jet1*dphilep1jet1 + (Lepton_eta[0]-CleanJet_eta[0])*(Lepton_eta[0]-CleanJet_eta[0])) : -9999',
}

aliases['Lepton_conept'] = {
    'expr': 'LeptonConePt(Lepton_pt, Lepton_pdgId, Lepton_electronIdx, Lepton_muonIdx, Electron_jetRelIso, Muon_jetRelIso)',
    'linesToAdd': [f'#include "{configurations}/../utils/macros/LeptonConePt_class.cc"'],
    'samples': mc + ['DATA', 'DATA_unprescaled']
}