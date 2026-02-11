import os
import copy
import inspect

# /afs/cern.ch/user/n/ntrevisa/work/latinos/Run3/PlotsConfigurationsRun3/ControlRegions/WZ/2023_v12
configurations = os.path.realpath(inspect.getfile(inspect.currentframe())) # this file
configurations = os.path.dirname(configurations) # 2023_v12
configurations = os.path.dirname(configurations) # WZ
configurations = os.path.dirname(configurations) # ControlRegions
configurations = os.path.dirname(configurations) # PlotsConfigurationsRun3

aliases = {}
aliases = OrderedDict()

mc     = [skey for skey in samples if skey not in ('Fake', 'DATA', 'Dyemb', 'DATA_EG', 'DATA_Mu', 'DATA_EMu', 'Fake_EG', 'Fake_Mu', 'Fake_EMu')]
mc_emb = [skey for skey in samples if skey not in ('Fake', 'DATA', 'DATA_Mu', 'DATA_EMu', 'Fake_EG', 'Fake_Mu', 'Fake_EMu')]

# LepCut3l__ele_wp90iso__mu_cut_TightID_POG
eleWP = 'wp90iso'
muWP = 'cut_Tight_HWW'
#muWP  = 'cut_TightID_POG'

aliases['LepWPCut'] = {
    'expr': 'LepCut3l__ele_'+eleWP+'__mu_'+muWP,
    'samples': mc + ['DATA'],
}

aliases['LepWPSF'] = {
    'expr': 'LepSF3l__ele_'+eleWP+'__mu_'+muWP,
    'samples': mc
}

# gen-matching to prompt only (GenLepMatch3l matches to *any* gen lepton)
aliases['PromptGenLepMatch3l'] = {
    'expr': 'Alt(Lepton_promptgenmatched, 0, 0) * Alt(Lepton_promptgenmatched, 1, 0) * Alt(Lepton_promptgenmatched, 2, 0)',
    'samples': mc
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
    'expr' : 'Sum(CleanJet_pt > 30 && CleanJet_pt < 50 && abs(CleanJet_eta) > 2.6 && abs(CleanJet_eta) < 3.1) == 0',
}

########################################################################
# B-Tagging WP: https://btv-wiki.docs.cern.ch/ScaleFactors/Run3Summer23/
########################################################################

# Algo / WP / WP cut
btagging_WPs = {
    "DeepFlavB" : {
        "loose"    : "0.0479",
        "medium"   : "0.2431",
        "tight"    : "0.6553",
        "xtight"   : "0.7667",
        "xxtight"  : "0.9459",
    },
    "RobustParTAK4B" : {
        "loose"    : "0.0358",
        "medium"   : "0.1917",
        "tight"    : "0.6172",
        "xtight"   : "0.7515",
        "xxtight"  : "0.9659",
    },
    "PNetB" : {
        "loose"    : "0.0681",
        "medium"   : "0.3487",
        "tight"    : "0.7969",    
        "xtight"   : "0.8882",
        "xxtight"  : "0.9883",
    }
}

# Algo / SF name
btagging_SFs = {
    "DeepFlavB"      : "deepjet",
    "RobustParTAK4B" : "partTransformer",
    "PNetB"          : "deepjet",
}

# Algorithm and WP selection
bAlgo = 'DeepFlavB' # ['DeepFlavB','RobustParTAK4B','PNetB'] 
WP    = 'loose'     # ['loose','medium','tight','xtight','xxtight']

# Access information from dictionaries
bWP   = btagging_WPs[bAlgo][WP]
bSF   = btagging_SFs[bAlgo]

# B tagging selections and scale factors
aliases['bVeto'] = {
    'expr': f'Sum(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{bAlgo}, CleanJet_jetIdx) > {bWP}) == 0'
}

aliases['bVetoSF'] = {
    'expr': 'TMath::Exp(Sum(LogVec((CleanJet_pt>20 && abs(CleanJet_eta)<2.5)*Take(Jet_btagSF_{}_shape, CleanJet_jetIdx)+1*(CleanJet_pt<20 || abs(CleanJet_eta)>2.5))))'.format(bSF),
    'samples': mc
}

aliases['bReq'] = { 
    'expr': f'Sum(CleanJet_pt > 30. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{bAlgo}, CleanJet_jetIdx) > {bWP}) >= 1'
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

# Systematic uncertainty variations
for shift in ['jes','lf','hf','lfstats1','lfstats2','hfstats1','hfstats2','cferr1','cferr2']:

    for targ in ['bVeto', 'bReq']:
        alias = aliases['%sSF%sup' % (targ, shift)] = copy.deepcopy(aliases['%sSF' % targ])
        alias['expr'] = alias['expr'].replace('btagSF_deepjet_shape', 'btagSF_deepjet_shape_up_%s' % shift)

        alias = aliases['%sSF%sdown' % (targ, shift)] = copy.deepcopy(aliases['%sSF' % targ])
        alias['expr'] = alias['expr'].replace('btagSF_deepjet_shape', 'btagSF_deepjet_shape_down_%s' % shift)

    aliases['btagSF%sup' % shift] = {
        'expr': aliases['btagSF']['expr'].replace('SF', 'SF' + shift + 'up'),
        'samples': mc
    }

    aliases['btagSF%sdown' % shift] = {
        'expr': aliases['btagSF']['expr'].replace('SF', 'SF' + shift + 'down'),
        'samples': mc
    }

##########################################################################
# End of b tagging
##########################################################################

# Data/MC scale factors and systematic uncertainties
aliases['SFweight'] = {
    'expr': ' * '.join(['SFweight3l', 'LepWPCut', 'LepWPSF','btagSF']),
    'samples': mc
}

aliases['SFweightEleUp'] = {
    'expr': 'LepSF3l__ele_'+eleWP+'__Up',
    'samples': mc
}
aliases['SFweightEleDown'] = {
    'expr': 'LepSF3l__ele_'+eleWP+'__Down',
    'samples': mc
}
aliases['SFweightMuUp'] = {
    'expr': 'LepSF3l__mu_'+muWP+'__Up',
    'samples': mc
}
aliases['SFweightMuDown'] = {
    'expr': 'LepSF3l__mu_'+muWP+'__Down',
    'samples': mc
}

# # WH3l_mOSll for data
# aliases['WH3l_mOSll'] = {
#     'linesToAdd' : [f'#include "{configurations}/ControlRegions/WZ/macros/mOS_ll.cc"'],
#     'class'      : 'mOS_ll',
#     'args'       : 'nLepton,Lepton_pt,Lepton_eta,Lepton_phi,Lepton_pdgId',
#     'samples'    : ['DATA'],
# }

# # WH3l_mlll for data
# aliases['WH3l_mlll'] = {
#     'linesToAdd' : [f'#include "{configurations}/ControlRegions/WZ/macros/m_lll.cc"'],
#     'class'      : 'm_lll',
#     'args'       : 'nLepton,Lepton_pt,Lepton_eta,Lepton_phi,Lepton_pdgId',
#     'samples'    : ['DATA'],
# }

# # WH3l_ZVeto for data
# aliases['WH3l_ZVeto'] = {
#     'linesToAdd' : [f'#include "{configurations}/ControlRegions/WZ/macros/z_veto.cc"'],
#     'class'      : 'z_veto',
#     'args'       : 'nLepton,Lepton_pt,Lepton_eta,Lepton_phi,Lepton_pdgId',
#     'samples'    : ['DATA'],
# }

# # WH3l_flagOSSF for data
# aliases['WH3l_flagOSSF'] = {
#     'linesToAdd' : [f'#include "{configurations}/ControlRegions/WZ/macros/flag_ossf.cc"'],
#     'class'      : 'flag_ossf',
#     'args'       : 'nLepton,Lepton_pt,Lepton_eta,Lepton_phi,Lepton_pdgId',
#     'samples'    : ['DATA'],
# }

# # WH3l_flagOSSF for data
# aliases['WH3l_chlll'] = {
#     'linesToAdd' : [f'#include "{configurations}/ControlRegions/WZ/macros/ch_lll.cc"'],
#     'class'      : 'ch_lll',
#     'args'       : 'nLepton,Lepton_pt,Lepton_eta,Lepton_phi,Lepton_pdgId',
#     'samples'    : ['DATA'],
# }
