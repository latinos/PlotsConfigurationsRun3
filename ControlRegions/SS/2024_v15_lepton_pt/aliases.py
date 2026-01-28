import os
import copy
import inspect
import ROOT

ROOT.gSystem.Load("libGpad.so")
ROOT.gSystem.Load("libGraf.so")

configurations = os.path.realpath(inspect.getfile(inspect.currentframe())) # This file
configurations = os.path.dirname(configurations)                           # /afs/cern.ch/user/n/ntrevisa/work/latinos/Run3_WH/PlotsConfigurationsRun3/ControlRegions/SS/2024_v15_lepton_pt
configurations = os.path.dirname(configurations)                           # /afs/cern.ch/user/n/ntrevisa/work/latinos/Run3_WH/PlotsConfigurationsRun3/ControlRegions/SS/
print(configurations)

aliases = {}
aliases = OrderedDict()

mc     = [skey for skey in samples if skey not in ('Fake', 'DATA')]
mc_emb = [skey for skey in samples if skey not in ('Fake', 'DATA')]

# LepSF2l__ele_cutBased_LooseID_tthMVA_Run3__mu_cut_TightID_pfIsoTight_HWW_tthmva_67
eleWP = 'cutBased_LooseID_tthMVA_Run3'
muWP  = 'cut_TightID_pfIsoTight_HWW_tthmva_67'

aliases['LepWPCut'] = {
    'expr': 'LepCut2l__ele_'+eleWP+'__mu_'+muWP,
    'samples': mc + ['DATA'],
}

aliases['LepWPSF'] = {
    'expr': 'LepSF2l__ele_'+eleWP+'__mu_'+muWP,
    'samples': mc
}

# gen-matching to prompt only (GenLepMatch2l matches to *any* gen lepton)
aliases['PromptGenLepMatch2l'] = {
    'expr': 'Alt(Lepton_promptgenmatched, 0, 0) * Alt(Lepton_promptgenmatched, 1, 0)',
    'samples': mc
}

# Conept
aliases['Lepton_conept'] = {
    'expr': 'LeptonConePt(Lepton_pt, Lepton_pdgId, Lepton_electronIdx, Lepton_muonIdx, Electron_jetRelIso, Muon_jetRelIso)',
    'linesToAdd': [f'#include "{configurations}/2024_v15/macros/LeptonConePt_class.cc"'],
    'samples': mc + ['Fake', 'DATA']
}

# Fake leptons transfer factor
aliases['fakeW'] = {
    'linesToAdd'     : [f'#include "{configurations}/2024_v15/macros/fake_rate_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader = fake_rate_reader(\"{eleWP}\", \"{muWP}\", \"nominal\", 2, \"std\", \"~/work/latinos/Run3_WH/PlotsConfigurationsRun3/FakeRate/2024_v15/FakeRate_pt/2024_v15_pt/\");')"],
    'expr'           : f'fr_reader(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_{muWP}, Lepton_isTightElectron_{eleWP}, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}

aliases['gstarLow'] = {
    'expr': 'Gen_ZGstar_mass > 0 && Gen_ZGstar_mass < 4',
    'samples': ['WZ', 'VgS', 'Vg']
}
aliases['gstarHigh'] = {
    'expr': 'Gen_ZGstar_mass < 0 || Gen_ZGstar_mass > 4',
    'samples': ['WZ', 'VgS', 'Vg'],
}

aliases['Top_pTrw'] = {
    'expr': '(topGenPt * antitopGenPt > 0.) * (TMath::Sqrt((0.103*TMath::Exp(-0.0118*topGenPt) - 0.000134*topGenPt + 0.973) * (0.103*TMath::Exp(-0.0118*antitopGenPt) - 0.000134*antitopGenPt + 0.973))) + (topGenPt * antitopGenPt <= 0.)',
    'samples': ['top']
}

# Jet bins
# using Alt(CleanJet_pt, n, 0) instead of Sum(CleanJet_pt >= 30) because jet pt ordering is not strictly followed in JES-varied samples

# No jet with pt > 30 GeV
aliases['zeroJet'] = {
    'expr': 'Alt(CleanJet_pt, 0, 0) < 30.'
}

aliases['oneJet'] = {
    'expr': 'Alt(CleanJet_pt, 0, 0) > 30.'
}

aliases['multiJet'] = {
    'expr': 'Alt(CleanJet_pt, 1, 0) > 30.'
}

aliases['noJetInHorn'] = {
    'expr' : 'Sum(CleanJet_pt > 30 && CleanJet_pt < 50 && abs(CleanJet_eta) > 2.5 && abs(CleanJet_eta) < 3.0) == 0',
}

########################################################################
# B-Tagging WP: https://btv-wiki.docs.cern.ch/ScaleFactors/Run3Summer23/
########################################################################

# Algo / WP / WP cut
btagging_WPs = {
    "UParTAK4B" : {"loose" : "0.0246", "medium" : "0.1272", "tight" : "0.4648", "xtight" : "0.6298", "xxtight" : "0.9739"},
}

# Algo / SF name
btagging_SFs = {
    "UParTAK4B"      : "upart",
}

# Algorithm and WP selection
bAlgo = 'UParTAK4B'
WP    = 'loose'     # ['loose','medium','tight','xtight','xxtight']

WP_eval = 'L' # ['L', 'M', 'T', 'XT', 'XXT']
tagger = 'UParTAK4'

# Access information from dictionaries
bWP   = btagging_WPs[bAlgo][WP]

# B tagging selections and scale factors
aliases['bVeto'] = {
    'expr': f'Sum(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{bAlgo}, CleanJet_jetIdx) > {bWP}) == 0'
}

aliases['bReq'] = { 
    'expr': f'Sum(CleanJet_pt > 30. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{bAlgo}, CleanJet_jetIdx) > {bWP}) >= 1'
}

##########################################################################
# End of b tagging
##########################################################################

# CR definition
aliases['topcr'] = {
    'expr': 'mll > 50 && ((zeroJet && !bVeto) || bReq) && mtw2 > 30'
}
aliases['dycr'] = {
    'expr': 'mth < 60 && mll > 40 && mll < 80 && bVeto && mtw2 > 30'
}
aliases['wwcr'] = {
    'expr': 'mth > 60 && mtw2 > 30 && mll > 100 && bVeto'
}


# SR definition
aliases['sr'] = {
    'expr': 'mth > 60 && mtw2 > 30 && bVeto'
}

eff_map_year = '2024' # ['2022', '2022EE', '2023BPix', '2023BPixBPix']
year = 'Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15' # ['Run3-22CDSep23-Summer22-NanoAODv12', 'Run3-22EFGSep23-Summer22EE-NanoAODv12, 'Run3-23CSep23-Summer23-NanoAODv12', 'Run3-23DSep23-Summer23BPix-NanoAODv12', 'Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15']

shifts_per_flavour = {
    'bc': ['central', 'down', 'down_fsrdef', 'down_hdamp', 'down_isrdef', 'down_jer', 'down_jes', 'down_mass', 'down_statistic', 'down_tune', 'up', 'up_fsrdef', 'up_hdamp', 'up_isrdef', 'up_jer', 'up_jes', 'up_mass', 'up_statistic', 'up_tune'],
    'light': ['central', 'down', 'down_correlated', 'down_uncorrelated', 'up', 'up_correlated', 'up_uncorrelated'],
}

for flavour in ['bc', 'light']:
    for shift in shifts_per_flavour[flavour]:
        btagsf = 'btagSF' + flavour
        if shift != 'central':
            btagsf += '_' + shift
        aliases[btagsf] = {
            'linesToAdd': [f'#include "{configurations}/macros/evaluate_btagSF{flavour}.cc"'],
            'linesToProcess': [f"ROOT.gInterpreter.Declare('btagSF{flavour} btagSF{flavour}_{shift} = btagSF{flavour}(\"{configurations}/../../../utils/data/btag/{eff_map_year}/bTagEff_{eff_map_year}_ttbar_{bAlgo}_loose.root\", \"{year}\");')"],
            'expr': f'btagSF{flavour}_{shift}(CleanJet_pt, CleanJet_eta, CleanJet_jetIdx, nCleanJet, Jet_hadronFlavour, Jet_btag{bAlgo}, "{WP_eval}", "{shift}", "{tagger}","{eff_map_year}")',
            'samples' : mc,
        }

# Number of hard (= gen-matched) jets                                                                                                                                                                      
aliases['nHardJets'] = {
    'expr'    :  'Sum(Take(Jet_genJetIdx,CleanJet_jetIdx) >= 0 && Take(GenJet_pt,Take(Jet_genJetIdx,CleanJet_jetIdx)) > 25)',
    'samples' : mc
}

# Data/MC scale factors and systematic uncertainties
aliases['SFweight'] = {
    'expr': ' * '.join(['SFweight2l', 'LepWPCut', 'LepWPSF', 'btagSFbc', ' btagSFlight']),
    #'expr': ' * '.join(['SFweight2l', 'LepWPCut', 'LepWPSF']),
    'samples': mc
}

aliases['SFweightEleUp'] = {
    'expr': 'LepSF2l__ele_'+eleWP+'__Up',
    'samples': mc
}
aliases['SFweightEleDown'] = {
    'expr': 'LepSF2l__ele_'+eleWP+'__Down',
    'samples': mc
}
aliases['SFweightMuUp'] = {
    'expr': 'LepSF2l__mu_'+muWP+'__Up',
    'samples': mc
}
aliases['SFweightMuDown'] = {
    'expr': 'LepSF2l__mu_'+muWP+'__Down',
    'samples': mc
}
