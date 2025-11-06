import os
import copy
import inspect

# /afs/cern.ch/user/n/ntrevisa/work/latinos/Run3/PlotsConfigurationsRun3/WH_chargeAsymmetry/UL/Full2017_v9/WH3l

configurations = os.path.realpath(inspect.getfile(inspect.currentframe())) # this file
configurations = os.path.dirname(configurations) # WH3l
configurations = os.path.dirname(configurations) # Full2017_v9
configurations = os.path.dirname(configurations) # UL

aliases = {}
aliases = OrderedDict()

mc     = [skey for skey in samples if skey not in ('Fake', 'DATA')]


# LepCut2l__ele_mvaFall17V2Iso_WP90__mu_cut_Tight_HWWW_tthmva_80
eleWP = 'mvaFall17V2Iso_WP90'
muWP  = 'cut_Tight_HWWW'

aliases['LepWPCut'] = {
    'expr'    : 'LepCut3l__ele_mvaFall17V2Iso_WP90__mu_cut_Tight_HWWW*\
     ( ((abs(Lepton_pdgId[0])==13 && Muon_mvaTTH[Lepton_muonIdx[0]]>0.82) || (abs(Lepton_pdgId[0])==11 && Lepton_mvaTTH_UL[0]>0.90)) \
    && ((abs(Lepton_pdgId[1])==13 && Muon_mvaTTH[Lepton_muonIdx[1]]>0.82) || (abs(Lepton_pdgId[1])==11 && Lepton_mvaTTH_UL[1]>0.90)) \
    && ((abs(Lepton_pdgId[2])==13 && Muon_mvaTTH[Lepton_muonIdx[2]]>0.82) || (abs(Lepton_pdgId[2])==11 && Lepton_mvaTTH_UL[2]>0.90)) )',
    'samples' : mc + ['DATA']
}

# Lepton SF (not considering the ttHMVA discriminant)
aliases['LepWPSF'] = {
    'expr'    : 'LepSF3l__ele_'+eleWP+'__mu_'+muWP,
    'samples' : mc
}

# ttHMVA SFs and uncertainties
aliases['LepWPttHMVASF'] = {
    'linesToAdd'     : [f'#include "{configurations}/macros/ttHMVASF_class.cc"'],
    'linesToProcess' : ["ROOT.gInterpreter.Declare('ttHMVASF ttH = ttHMVASF(\"2017\", 3, \"all\", \"nominal\");')"],
    'expr'           : 'ttH(Lepton_pt, Lepton_eta, Lepton_pdgId)',
    'samples'        : mc
}

aliases['LepWPttHMVASFEleUp'] = {
    'linesToAdd'     : [f'#include "{configurations}/macros/ttHMVASF_class.cc"'],
    'linesToProcess' : ["ROOT.gInterpreter.Declare('ttHMVASF ttH_EleUp = ttHMVASF(\"2017\", 3, \"all\", \"eleUp\");')"],
    'expr'           : 'ttH_EleUp(Lepton_pt, Lepton_eta, Lepton_pdgId)',
    'samples'        : mc
}
aliases['LepWPttHMVASFEleDown'] = {
    'linesToAdd'     : [f'#include "{configurations}/macros/ttHMVASF_class.cc"'],
    'linesToProcess' : ["ROOT.gInterpreter.Declare('ttHMVASF ttH_EleDown = ttHMVASF(\"2017\", 3, \"all\", \"eleDown\");')"],
    'expr'           : 'ttH_EleDown(Lepton_pt, Lepton_eta, Lepton_pdgId)',
    'samples'        : mc
}

aliases['LepWPttHMVASFMuUp'] = {
    'linesToAdd'     : [f'#include "{configurations}/macros/ttHMVASF_class.cc"'],
    'linesToProcess' : ["ROOT.gInterpreter.Declare('ttHMVASF ttH_MuUp = ttHMVASF(\"2017\", 3, \"all\", \"muUp\");')"],
    'expr'           : 'ttH_MuUp(Lepton_pt, Lepton_eta, Lepton_pdgId)',
    'samples'        : mc
}
aliases['LepWPttHMVASFMuDown'] = {
    'linesToAdd'     : [f'#include "{configurations}/macros/ttHMVASF_class.cc"'],
    'linesToProcess' : ["ROOT.gInterpreter.Declare('ttHMVASF ttH_MuDown = ttHMVASF(\"2017\", 3, \"all\", \"muDown\");')"],
    'expr'           : 'ttH_MuDown(Lepton_pt, Lepton_eta, Lepton_pdgId)',
    'samples'        : mc
}


# Conept
aliases['Lepton_conept'] = {
    'expr': 'LeptonConePt(Lepton_pt, Lepton_pdgId, Lepton_electronIdx, Lepton_muonIdx, Electron_jetRelIso, Muon_jetRelIso)',
    'linesToAdd': [f'#include "{configurations}/macros/LeptonConePt_class.cc"'],
    'samples': mc + ['Fake', 'DATA', 'DATA_unprescaled']
}

# Fake leptons transfer factor
aliases['fakeW'] = {
    'linesToAdd'     : [f'#include "{configurations}/macros/fake_rate_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader = fake_rate_reader(\"2017\", \"90\", \"82\", 0.90, 0.82, \"nominal\", 3, \"std\", \"{configurations}\");')"],
    'expr'           : 'fr_reader(Lepton_pdgId, Lepton_conept, Lepton_eta, Lepton_isTightMuon_cut_Tight_HWWW, Lepton_isTightElectron_mvaFall17V2Iso_WP90, Lepton_mvaTTH_UL, Muon_mvaTTH, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}

# And variations - already divided by central values in formulas !
aliases['fakeWEleUp'] = {
    'linesToAdd'     : [f'#include "{configurations}/macros/fake_rate_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_EleUp = fake_rate_reader(\"2017\", \"90\", \"82\", 0.90, 0.82, \"EleUp\", 3, \"std\", \"{configurations}\");')"],
    'expr'           : 'fr_reader_EleUp(Lepton_pdgId, Lepton_conept, Lepton_eta, Lepton_isTightMuon_cut_Tight_HWWW, Lepton_isTightElectron_mvaFall17V2Iso_WP90, Lepton_mvaTTH_UL, Muon_mvaTTH, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}
aliases['fakeWEleDown'] = {
    'linesToAdd'     : [f'#include "{configurations}/macros/fake_rate_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_EleDown = fake_rate_reader(\"2017\", \"90\", \"82\", 0.90, 0.82, \"EleDown\", 3, \"std\", \"{configurations}\");')"],
    'expr'           : 'fr_reader_EleDown(Lepton_pdgId, Lepton_conept, Lepton_eta, Lepton_isTightMuon_cut_Tight_HWWW, Lepton_isTightElectron_mvaFall17V2Iso_WP90, Lepton_mvaTTH_UL, Muon_mvaTTH, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}

aliases['fakeWMuUp'] = {
    'linesToAdd'     : [f'#include "{configurations}/macros/fake_rate_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_MuUp = fake_rate_reader(\"2017\", \"90\", \"82\", 0.90, 0.82, \"MuUp\", 3, \"std\", \"{configurations}\");')"],
    'expr'           : 'fr_reader_MuUp(Lepton_pdgId, Lepton_conept, Lepton_eta, Lepton_isTightMuon_cut_Tight_HWWW, Lepton_isTightElectron_mvaFall17V2Iso_WP90, Lepton_mvaTTH_UL, Muon_mvaTTH, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}
aliases['fakeWMuDown'] = {
    'linesToAdd'     : [f'#include "{configurations}/macros/fake_rate_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_MuDown = fake_rate_reader(\"2017\", \"90\", \"82\", 0.90, 0.82, \"MuDown\", 3, \"std\", \"{configurations}\");')"],
    'expr'           : 'fr_reader_MuDown(Lepton_pdgId, Lepton_conept, Lepton_eta, Lepton_isTightMuon_cut_Tight_HWWW, Lepton_isTightElectron_mvaFall17V2Iso_WP90, Lepton_mvaTTH_UL, Muon_mvaTTH, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}

aliases['fakeWStatEleUp'] = {
    'linesToAdd'     : [f'#include "{configurations}/macros/fake_rate_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_StatEleUp = fake_rate_reader(\"2017\", \"90\", \"82\", 0.90, 0.82, \"StatEleUp\", 3, \"std\", \"{configurations}\");')"],
    'expr'           : 'fr_reader_StatEleUp(Lepton_pdgId, Lepton_conept, Lepton_eta, Lepton_isTightMuon_cut_Tight_HWWW, Lepton_isTightElectron_mvaFall17V2Iso_WP90, Lepton_mvaTTH_UL, Muon_mvaTTH, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}
aliases['fakeWStatEleDown'] = {
    'linesToAdd'     : [f'#include "{configurations}/macros/fake_rate_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_StatEleDown = fake_rate_reader(\"2017\", \"90\", \"82\", 0.90, 0.82, \"StatEleDown\", 3, \"std\", \"{configurations}\");')"],
    'expr'           : 'fr_reader_StatEleDown(Lepton_pdgId, Lepton_conept, Lepton_eta, Lepton_isTightMuon_cut_Tight_HWWW, Lepton_isTightElectron_mvaFall17V2Iso_WP90, Lepton_mvaTTH_UL, Muon_mvaTTH, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}

aliases['fakeWStatMuUp'] = {
    'linesToAdd'     : [f'#include "{configurations}/macros/fake_rate_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_StatMuUp = fake_rate_reader(\"2017\", \"90\", \"82\", 0.90, 0.82, \"StatMuUp\", 3, \"std\", \"{configurations}\");')"],
    'expr'           : 'fr_reader_StatMuUp(Lepton_pdgId, Lepton_conept, Lepton_eta, Lepton_isTightMuon_cut_Tight_HWWW, Lepton_isTightElectron_mvaFall17V2Iso_WP90, Lepton_mvaTTH_UL, Muon_mvaTTH, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}
aliases['fakeWStatMuDown'] = {
    'linesToAdd'     : [f'#include "{configurations}/macros/fake_rate_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_StatMuDown = fake_rate_reader(\"2017\", \"90\", \"82\", 0.90, 0.82, \"StatMuDown\", 3, \"std\", \"{configurations}\");')"],
    'expr'           : 'fr_reader_StatMuDown(Lepton_pdgId, Lepton_conept, Lepton_eta, Lepton_isTightMuon_cut_Tight_HWWW, Lepton_isTightElectron_mvaFall17V2Iso_WP90, Lepton_mvaTTH_UL, Muon_mvaTTH, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}

aliases['fakeWEWKEleUp'] = {
    'linesToAdd'     : [f'#include "{configurations}/macros/fake_rate_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_EWKEleUp = fake_rate_reader(\"2017\", \"90\", \"82\", 0.90, 0.82, \"EWKEleUp\", 3, \"std\", \"{configurations}\");')"],
    'expr'           : 'fr_reader_EWKEleUp(Lepton_pdgId, Lepton_conept, Lepton_eta, Lepton_isTightMuon_cut_Tight_HWWW, Lepton_isTightElectron_mvaFall17V2Iso_WP90, Lepton_mvaTTH_UL, Muon_mvaTTH, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}
aliases['fakeWEWKEleDown'] = {
    'linesToAdd'     : [f'#include "{configurations}/macros/fake_rate_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_EWKEleDown = fake_rate_reader(\"2017\", \"90\", \"82\", 0.90, 0.82, \"EWKEleDown\", 3, \"std\", \"{configurations}\");')"],
    'expr'           : 'fr_reader_EWKEleDown(Lepton_pdgId, Lepton_conept, Lepton_eta, Lepton_isTightMuon_cut_Tight_HWWW, Lepton_isTightElectron_mvaFall17V2Iso_WP90, Lepton_mvaTTH_UL, Muon_mvaTTH, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}

aliases['fakeWEWKMuUp'] = {
    'linesToAdd'     : [f'#include "{configurations}/macros/fake_rate_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_EWKMuUp = fake_rate_reader(\"2017\", \"90\", \"82\", 0.90, 0.82, \"EWKMuUp\", 3, \"std\", \"{configurations}\");')"],
    'expr'           : 'fr_reader_EWKMuUp(Lepton_pdgId, Lepton_conept, Lepton_eta, Lepton_isTightMuon_cut_Tight_HWWW, Lepton_isTightElectron_mvaFall17V2Iso_WP90, Lepton_mvaTTH_UL, Muon_mvaTTH, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}
aliases['fakeWEWKMuDown'] = {
    'linesToAdd'     : [f'#include "{configurations}/macros/fake_rate_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_EWKMuDown = fake_rate_reader(\"2017\", \"90\", \"82\", 0.90, 0.82, \"EWKMuDown\", 3, \"std\", \"{configurations}\");')"],
    'expr'           : 'fr_reader_EWKMuDown(Lepton_pdgId, Lepton_conept, Lepton_eta, Lepton_isTightMuon_cut_Tight_HWWW, Lepton_isTightElectron_mvaFall17V2Iso_WP90, Lepton_mvaTTH_UL, Muon_mvaTTH, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}

# No jet with pt > 30 GeV
aliases['zeroJet'] = {
    'expr' : 'Alt(CleanJet_pt, 0, 0) < 30.'
}

aliases['oneJet'] = {
    'expr' : 'Alt(CleanJet_pt, 0, 0) > 30. && Alt(CleanJet_pt, 1, 0) < 30.'
}

aliases['multiJet'] = {
    'expr' : 'Alt(CleanJet_pt, 1, 0) > 30.'
}

####################################################################################
# b tagging WPs: https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL17
####################################################################################

# DeepB = DeepCSV
bWP_loose_deepB  = '0.1355'
bWP_medium_deepB = '0.4506' 
bWP_tight_deepB  = '0.7738'

# DeepFlavB = DeepJet
bWP_loose_deepFlavB  = '0.0532'
bWP_medium_deepFlavB = '0.3040'
bWP_tight_deepFlavB  = '0.7476'

# Actual algo and WP definition. BE CONSISTENT!!
bAlgo = 'DeepB'          # ['DeepB',        'DeepFlavB'         ]
bWP   = bWP_medium_deepB # [bWP_loose_deepB, bWP_loose_deepFlavB]
bSF   = 'deepcsv'        # ['deepcsv',      'deepjet'           ]

# b veto
aliases['bVeto'] = {
    'expr': 'Sum(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{}, CleanJet_jetIdx) > {}) == 0'.format(bAlgo, bWP)
}

aliases['bVetoSF'] = {
    'expr': 'TMath::Exp(Sum(LogVec((CleanJet_pt>20 && abs(CleanJet_eta)<2.5)*Take(Jet_btagSF_{}_shape, CleanJet_jetIdx)+1*(CleanJet_pt<20 || abs(CleanJet_eta)>2.5))))'.format(bSF),
    'samples': mc
}

# At least one b-tagged jet
aliases['bReq'] = {
    'expr': 'Sum(CleanJet_pt > 30. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{}, CleanJet_jetIdx) > {}) >= 1'.format(bAlgo, bWP)
}

aliases['bReqSF'] = {
    'expr': 'TMath::Exp(Sum(LogVec((CleanJet_pt>30 && abs(CleanJet_eta)<2.5)*Take(Jet_btagSF_{}_shape, CleanJet_jetIdx)+1*(CleanJet_pt<30 || abs(CleanJet_eta)>2.5))))'.format(bSF),
    'samples': mc
}

# Top control region
aliases['topcr'] = {
    'expr': 'mtw2>30 && mll>50 && ((zeroJet && !bVeto) || bReq)'
}

# WW control region
aliases['wwcr'] = {
    'expr': 'mth>60 && mtw2>30 && mll>100 && bVeto'
}

# Overall b tag SF
aliases['btagSF'] = {
    'expr': '(bVeto || (topcr && zeroJet))*bVetoSF + (topcr && !zeroJet)*bReqSF',
    'samples': mc
}

for shift in ['jesAbsolute', 'jesAbsolute_2017', 'jesBBEC1', 'jesBBEC1_2017', 'jesEC2',
        'jesEC2_2017', 'jesFlavorQCD', 'jesHF', 'jesHF_2017', 'jesRelativeBal',
        'jesRelativeSample_2017']:
    for var in ['up','down']:
        aliases[f'Jet_btagSF_{bSF}_shape_{shift.replace("jes","JES")}{var[:2]}'] = {
                'expr' : f'Jet_btagSF_{bSF}_shape_{var}_{shift}',
                'samples' : mc
        }

for shift in ['jesAbsolute', 'jesAbsolute_2017', 'jesBBEC1', 'jesBBEC1_2017', 'jesEC2',
              'jesEC2_2017', 'jesFlavorQCD', 'jesHF', 'jesHF_2017', 'jesRelativeBal',
              'jesRelativeSample_2017', 'lf', 'hf', 'lfstats1', 'lfstats2',
              'hfstats1', 'hfstats2', 'cferr1', 'cferr2']:
    
    for targ in ['bVeto', 'bReq']:
        alias = aliases['%sSF%sup' % (targ, shift)] = copy.deepcopy(aliases['%sSF' % targ])
        alias['expr'] = alias['expr'].replace('btagSF_{}_shape'.format(bSF), 'btagSF_{}_shape_up_{}'.format(bSF, shift))

        alias = aliases['%sSF%sdown' % (targ, shift)] = copy.deepcopy(aliases['%sSF' % targ])
        alias['expr'] = alias['expr'].replace('btagSF_{}_shape'.format(bSF), 'btagSF_{}_shape_down_{}'.format(bSF, shift))

    aliases['btagSF%sup' % shift] = {
        'expr': aliases['btagSF']['expr'].replace('SF', 'SF' + shift + 'up'),
        'samples': mc
    }

    aliases['btagSF%sdown' % shift] = {
        'expr': aliases['btagSF']['expr'].replace('SF', 'SF' + shift + 'down'),
        'samples': mc
    }

####################################################################################
# End of b tagging pippone
####################################################################################

aliases['gstarLow'] = {
    'expr': 'Gen_ZGstar_mass > 0 && Gen_ZGstar_mass < 4',
    'samples': 'VgS'
}

aliases['gstarHigh'] = {
    'expr': 'Gen_ZGstar_mass < 0 || Gen_ZGstar_mass > 4',
    'samples': 'WZ'
}

# gen-matching to prompt only (GenLepMatch3l matches to *any* gen lepton)
aliases['PromptGenLepMatch3l'] = {
    'expr': 'Alt(Lepton_promptgenmatched, 0, 0) * Alt(Lepton_promptgenmatched, 1, 0) * Alt(Lepton_promptgenmatched, 2, 0)',
    'samples': mc
}

# Need to redefine PUID scale factors, so that they are double and not vectors
aliases['Jet_PUIDSF'] = {
  'expr' : 'TMath::Exp(Sum((Jet_jetId>=2)*LogVec(Jet_PUIDSF_loose)))',
  'samples': mc
}

aliases['Jet_PUIDSF_up'] = {
  'expr' : 'TMath::Exp(Sum((Jet_jetId>=2)*LogVec(Jet_PUIDSF_loose_up)))',
  'samples': mc
}

aliases['Jet_PUIDSF_down'] = {
  'expr' : 'TMath::Exp(Sum((Jet_jetId>=2)*LogVec(Jet_PUIDSF_loose_down)))',
  'samples': mc
}


aliases['Top_pTrw'] = {
    'expr': '(topGenPt * antitopGenPt > 0.) * (TMath::Sqrt(TMath::Exp(0.0615 - 0.0005 * topGenPt) * TMath::Exp(0.0615 - 0.0005 * antitopGenPt))) + (topGenPt * antitopGenPt <= 0.)',
    'samples': ['top']
}

# data/MC scale factors
aliases['SFweight'] = {
    # 'expr': ' * '.join(['SFweight3l', 'LepWPCut', 'LepWPSF','Jet_PUIDSF_loose', 'btagSF', 'LepWPttHMVASF']),
    'expr': ' * '.join(['SFweight3l', 'LepWPCut', 'LepWPSF', 'Jet_PUIDSF', 'btagSF', 'LepWPttHMVASF']),
    'samples': mc
}

# variations
aliases['SFweightEleUp'] = {
    'expr': 'LepSF3l__ele_'+eleWP+'__Up',
    'samples': mc
}
aliases['SFweightEleDown'] = {
    'expr': 'LepSF3l__ele_'+eleWP+'__Do',
    'samples': mc
}

aliases['SFweightMuUp'] = {
    'expr': 'LepSF3l__mu_'+muWP+'__Up',
    'samples': mc
}
aliases['SFweightMuDown'] = {
    'expr': 'LepSF3l__mu_'+muWP+'__Do',
    'samples': mc
}

# TriggerSFWeight_3l:TriggerSFWeight_3l_u:TriggerSFWeight_3l_d
aliases['SFtriggUp'] = {
    'expr': 'TriggerSFWeight_3l_u/TriggerSFWeight_3l',
    'samples': mc
}
aliases['SFtriggDown'] = {
    'expr': 'TriggerSFWeight_3l_d/TriggerSFWeight_3l',
    'samples': mc
}

# Evaluate BDT discriminants
aliases['BDT_WH3l_OSSF_new_v9'] = {
    'linesToAdd'     : [f'#include "{configurations}/macros/BDT_WH3l_OSSF_v9_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('BDT_WH3l_OSSF_v9 BDT_WH3l_OSSF = BDT_WH3l_OSSF_v9(\"BDTG4C3\",\"{configurations}/data/BDT/2017/WH3l/OSSF/weights/TMVAClassification_BDTG4C3.weights.xml\");')"],
    'expr'           : 'BDT_WH3l_OSSF(WH3l_dphilllmet,WH3l_mOSll,WH3l_ptOSll,WH3l_drOSll,WH3l_ZVeto,WH3l_mtlmet,WH3l_dphilmet,WH3l_ptWWW,PuppiMET_pt,Lepton_pt)',
    'samples'        : mc + ['DATA','Fake'],
}
    
aliases['BDT_WH3l_SSSF_new_v9'] = {
    'linesToAdd'     : [f'#include "{configurations}/macros/BDT_WH3l_SSSF_v9_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('BDT_WH3l_SSSF_v9 BDT_WH3l_SSSF = BDT_WH3l_SSSF_v9(\"BDTG4C3\",\"{configurations}/data/BDT/2017/WH3l/SSSF/weights/TMVAClassification_BDTG4SK01_05shrinkage.weights.xml\");')"],
    'expr'           : 'BDT_WH3l_SSSF(WH3l_dphilllmet,WH3l_mOSll,WH3l_ptOSll,WH3l_drOSll,WH3l_dphilmet,WH3l_ptWWW,PuppiMET_pt,Lepton_pt)',
    'samples'        : mc + ['DATA','Fake'],
}

aliases['BDT_WHSS_TopSemileptonic_v9'] = {
    'linesToAdd'     : [f'#include "{configurations}/macros/BDT_WHSS_TopSemileptonic_v9_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('BDT_WHSS_TopSemileptonic_v9 BDT_WHSS = BDT_WHSS_TopSemileptonic_v9(\"BDTG_6\",\"{configurations}/data/BDT/2017/WHSS/weights/TMVAClassification_BDTG_6.weights.xml\");')"],
    'expr'           : 'BDT_WHSS(mll,mjj,mtw1,mtw2,ptll,mlljj20_whss,PuppiMET_pt,dphill,dphijj,dphillmet,dphilmet2,dphijet1met,CleanJet_pt,Jet_btagDeepB,CleanJet_jetIdx)',
    'samples'        : mc + ['DATA','Fake'],
}
