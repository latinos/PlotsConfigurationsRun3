import os
import copy
import inspect

# /afs/cern.ch/user/n/ntrevisa/work/latinos/Run3/PlotsConfigurationsRun3/ControlRegions/WZ/2022EE_v12
configurations = os.path.realpath(inspect.getfile(inspect.currentframe())) # this file
configurations = os.path.dirname(configurations) # 2022EE_v12
configurations = os.path.dirname(configurations) # WZ
configurations = os.path.dirname(configurations) # ControlRegions
configurations = os.path.dirname(configurations) # PlotsConfigurationsRun3

aliases = {}
aliases = OrderedDict()

mc     = [skey for skey in samples if skey not in ('Fake', 'DATA', 'Dyemb', 'DATA_EG', 'DATA_Mu', 'DATA_EMu', 'Fake_EG', 'Fake_Mu', 'Fake_EMu')]
mc_emb = [skey for skey in samples if skey not in ('Fake', 'DATA', 'DATA_Mu', 'DATA_EMu', 'Fake_EG', 'Fake_Mu', 'Fake_EMu')]

# LepCut3l__ele_wp90iso__mu_cut_TightID_POG

eleWP = 'wp90iso'
muWP  = 'cut_Tight_HWW'

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

##########################################################################
# B-Tagging WP: https://btv-wiki.docs.cern.ch/ScaleFactors/Run3Summer22EE/
##########################################################################

# Algo / WP / WP cut
btagging_WPs = {
    "DeepFlavB" : {
        "loose"    : "0.0614",
        "medium"   : "0.3196",
        "tight"    : "0.7300",
        "xtight"   : "0.8184",
        "xxtight"  : "0.9542",
    },
    "RobustParTAK4B" : {
        "loose"    : "0.0897",
        "medium"   : "0.4510",
        "tight"    : "0.8604",
        "xtight"   : "0.9234",
        "xxtight"  : "0.9893",
    },
    "PNetB" : {
        "loose"    : "0.0499",
        "medium"   : "0.2605",
        "tight"    : "0.6915",    
        "xtight"   : "0.8033",
        "xxtight"  : "0.9664",
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
    'expr': ' * '.join(['SFweight2l', 'LepWPCut', 'LepWPSF','btagSF']),
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
