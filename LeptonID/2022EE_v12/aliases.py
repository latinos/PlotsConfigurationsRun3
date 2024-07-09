import os
import copy
import inspect

configurations = os.path.realpath(inspect.getfile(inspect.currentframe())) # this file

aliases = {}
aliases = OrderedDict()

mc     = [skey for skey in samples if skey not in ('Fake', 'DATA', 'Dyemb', 'DATA_EG', 'DATA_Mu', 'DATA_EMu', 'Fake_EG', 'Fake_Mu', 'Fake_EMu')]
mc_emb = [skey for skey in samples if skey not in ('Fake', 'DATA', 'DATA_Mu', 'DATA_EMu', 'Fake_EG', 'Fake_Mu', 'Fake_EMu')]


###############################
# Define different lepton IDs #
###############################

# LepCut2l__ele_wp90iso__mu_cut_TightID_POG
eleWP = 'wp90iso'
muWP  = 'cut_TightID_POG'

aliases['LepWPCut__ele_wp90iso__mu_cut_TightID_POG'] = {
    'expr': 'LepCut2l__ele_' + eleWP + '__mu_' + muWP,
    'samples': mc,
}

# LepCut2l__ele_wp90iso__mu_cut_TightID_POG + muon_ttHMVA_80
aliases['LepWPCut__ele_wp90iso__mu_cut_TightID_POG_tthmva_80'] = {
    'expr': 'LepCut2l__ele_' + eleWP + '__mu_' + muWP + \
            '( ((abs(Lepton_pdgId[0])==13 && Muon_mvaTTH[Lepton_muonIdx[0]]>0.80) || (abs(Lepton_pdgId[0])==11)) \
            && ((abs(Lepton_pdgId[1])==13 && Muon_mvaTTH[Lepton_muonIdx[1]]>0.80) || (abs(Lepton_pdgId[1])==11)) )',
    'samples': mc,
}


# LepCut2l__ele_mvaWinter22V2Iso_WP90__mu_cut_Tight_HWW
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'cut_Tight_HWW'

aliases['LepWPCut__ele_mvaWinter22V2Iso_WP90__mu_cut_Tight_HWW'] = {
    'expr': 'LepCut2l__ele_' + eleWP + '__mu_' + muWP,
    'samples': mc,
}

# LepCut2l__ele_mvaWinter22V2Iso_WP90__mu_cut_Tight_HWW + muon_ttHMVA_80
aliases['LepWPCut__ele_mvaWinter22V2Iso_WP90__mu_cut_Tight_HWW_tthmva_80'] = {
    'expr': 'LepCut2l__ele_'+eleWP+'__mu_'+muWP + \
            '( ((abs(Lepton_pdgId[0])==13 && Muon_mvaTTH[Lepton_muonIdx[0]]>0.80) || (abs(Lepton_pdgId[0])==11)) \
            && ((abs(Lepton_pdgId[1])==13 && Muon_mvaTTH[Lepton_muonIdx[1]]>0.80) || (abs(Lepton_pdgId[1])==11)) )',
    'samples': mc,
}


# LepCut2l__ele_mvaWinter22V2Iso_WP90__mu_cut_TightMiniIso_HWW 
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'cut_TightMiniIso_HWW '

aliases['LepWPCut__ele_mvaWinter22V2Iso_WP90__mu_cut_TightMiniIso_HWW'] = {
    'expr': 'LepCut2l__ele_' + eleWP + '__mu_' + muWP,
    'samples': mc,
}

# LepCut2l__ele_mvaWinter22V2Iso_WP90__mu_cut_TightMiniIso_HWW + muon_ttHMVA_80
aliases['LepWPCut__ele_mvaWinter22V2Iso_WP90__mu_cut_TightMiniIso_HWW_tthmva_80'] = {
    'expr': 'LepCut2l__ele_' + eleWP + '__mu_' + muWP + \
            '( ((abs(Lepton_pdgId[0])==13 && Muon_mvaTTH[Lepton_muonIdx[0]]>0.80) || (abs(Lepton_pdgId[0])==11)) \
            && ((abs(Lepton_pdgId[1])==13 && Muon_mvaTTH[Lepton_muonIdx[1]]>0.80) || (abs(Lepton_pdgId[1])==11)) )',
    'samples': mc,
}


# LepCut2l__ele_wp90iso__mu_mvaMuID_WP_medium
eleWP = 'wp90iso'
muWP  = 'mvaMuID_WP_medium'

aliases['LepCut2l__ele_'+eleWP+'__mu_'+muWP] = {
    'expr' : 'nLepton > 1 ? \
              ( ( (abs(Lepton_pdgId[0]) == 13 && abs(Lepton_eta[0]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[0]]) < 0.1 && Muon_pfRelIso04_all[Lepton_muonIdx[0]] < 0.15 && ((Lepton_pt[0] <= 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.01) || (Lepton_pt[0] > 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[0]] >= 1) || (abs(Lepton_pdgId[0]) == 11 && Lepton_isTightElectron_'+eleWP+'[0]>0.5) ) && \
              ( ( (abs(Lepton_pdgId[1]) == 13 && abs(Lepton_eta[1]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[1]]) < 0.1 && Muon_pfRelIso04_all[Lepton_muonIdx[1]] < 0.15 && ((Lepton_pt[1] <= 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.01) || (Lepton_pt[1] > 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[1]] >= 1) || (abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_'+eleWP+'[1]>0.5) ) ) ) : 0',
    'samples' : mc,
}

# LepCut2l__ele_wp90iso__mu_mvaMuID_WP_medium + muon_ttHMVA_80
aliases['LepCut2l__ele_'+eleWP+'__mu_'+muWP+'_tthmva_80'] = {
    'expr' : 'LepCut2l__ele_' + eleWP + '__mu_' + muWP + \
            '( ((abs(Lepton_pdgId[0])==13 && Muon_mvaTTH[Lepton_muonIdx[0]]>0.80) || (abs(Lepton_pdgId[0])==11)) \
            && ((abs(Lepton_pdgId[1])==13 && Muon_mvaTTH[Lepton_muonIdx[1]]>0.80) || (abs(Lepton_pdgId[1])==11)) )',
    'samples' : mc,
}


# LepCut2l__ele_wp90iso__mu_mvaMuID_WP_tight
eleWP = 'wp90iso'
muWP  = 'mvaMuID_WP_tight'

aliases['LepCut2l__ele_'+eleWP+'__mu_'+muWP] = {
    'expr' : 'nLepton > 1 ? \
              ( ( (abs(Lepton_pdgId[0]) == 13 && abs(Lepton_eta[0]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[0]]) < 0.1 && Muon_pfRelIso04_all[Lepton_muonIdx[0]] < 0.15 && ((Lepton_pt[0] <= 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.01) || (Lepton_pt[0] > 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[0]] == 2) || (abs(Lepton_pdgId[0]) == 11 && Lepton_isTightElectron_'+eleWP+'[0]>0.5) ) && \
              ( ( (abs(Lepton_pdgId[1]) == 13 && abs(Lepton_eta[1]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[1]]) < 0.1 && Muon_pfRelIso04_all[Lepton_muonIdx[1]] < 0.15 && ((Lepton_pt[1] <= 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.01) || (Lepton_pt[1] > 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[1]] == 2) || (abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_'+eleWP+'[1]>0.5) ) ) ) : 0',
    'samples' : mc,
}

# LepCut2l__ele_wp90iso__mu_mvaMuID_WP_tight + muon_ttHMVA_80
aliases['LepCut2l__ele_'+eleWP+'__mu_'+muWP] = {
    'expr' : 'LepCut2l__ele_' + eleWP + '__mu_' + muWP + \
            '( ((abs(Lepton_pdgId[0])==13 && Muon_mvaTTH[Lepton_muonIdx[0]]>0.80) || (abs(Lepton_pdgId[0])==11)) \
            && ((abs(Lepton_pdgId[1])==13 && Muon_mvaTTH[Lepton_muonIdx[1]]>0.80) || (abs(Lepton_pdgId[1])==11)) )',
    'samples' : mc,
}


# Current list of Lepton IDs inspected:
# LepCut2l__ele_mvaWinter22V2Iso_WP90__mu_cut_TightID_POG
# LepCut2l__ele_wp90iso__mu_cut_Tight_HWW
# LepCut2l__ele_wp90iso__mu_cut_TightMiniIso_HWW
# LepCut2l__ele_mvaWinter22V2Iso_WP90__mu_mvaMuID_WP_medium
# LepCut2l__ele_mvaWinter22V2Iso_WP90__mu_mvaMuID_WP_tight


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
