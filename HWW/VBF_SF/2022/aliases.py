import os
import copy
import inspect

print('\n\n\n')
print('Configs:\n\n\n')
configurations = os.path.realpath(inspect.getfile(inspect.currentframe())) 
configurations = os.path.dirname(configurations) + '/'
print(configurations)
print('\n\n\n')


aliases = {}
aliases = OrderedDict()

mc     = [skey for skey in samples if skey not in ('Fake', 'DATA', 'Dyemb', 'DATA_EG', 'DATA_Mu', 'DATA_EMu', 'Fake_EG', 'Fake_Mu', 'Fake_EMu')]
mc_emb = [skey for skey in samples if skey not in ('Fake', 'DATA', 'DATA_Mu', 'DATA_EMu', 'Fake_EG', 'Fake_Mu', 'Fake_EMu')]


# LepCut2l__ele_cutBased_LooseID_tthMVA_Run3__mu_cut_TightID_pfIsoTight_HWW_tthmva_67
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

Tag = 'ele_'+eleWP+'_mu_'+muWP

aliases['fakeW'] = {
    'linesToAdd' : [f'#include "{configurations}macros/fake_rate_reader_class.cc"'],
    'linesToProcess':[f"ROOT.gInterpreter.Declare('fake_rate_reader fr_reader = fake_rate_reader(\"2022\", \"{eleWP}\", \"{muWP}\", 0.90, 0.80, \"nominal\", 2, \"std\", \"{configurations}\");')"],
    'expr': f'fr_reader(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_{muWP}, Lepton_isTightElectron_{eleWP}, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'    : ['Fake']
}

#aliases["fakeWEleUp"] = {
#    "expr": f"fakeW_{Tag}_2l0jElUp*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)<30.0) + fakeW_{Tag}_2l1jElUp*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)>30.0 && Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)<30.0) + fakeW_{Tag}_2l2jElUp*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)>30.0)",
#    'samples':['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
#}
#aliases["fakeWEleDown"] = {
#    "expr": f"fakeW_{Tag}_2l0jElDown*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)<30.0) + fakeW_{Tag}_2l1jElDown*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)>30.0 && Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)<30.0) + fakeW_{Tag}_2l2jElDown*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)>30.0)",
#    'samples':['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
#}
#aliases["fakeWMuUp"] = {
#    "expr": f"fakeW_{Tag}_2l0jMuUp*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)<30.0) + fakeW_{Tag}_2l1jMuUp*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)>30.0 && Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)<30.0) + fakeW_{Tag}_2l2jMuUp*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)>30.0)",
#    'samples':['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
#}
#aliases["fakeWMuDown"] = {
#    "expr": f"fakeW_{Tag}_2l0jMuDown*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)<30.0) + fakeW_{Tag}_2l1jMuDown*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)>30.0 && Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)<30.0) + fakeW_{Tag}_2l2jMuDown*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)>30.0)",
#    'samples':['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
#}
#aliases["fakeWStatEleUp"] = {
#    "expr": f"fakeW_{Tag}_2l0jstatElUp*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)<30.0) + fakeW_{Tag}_2l1jstatElUp*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)>30.0 && Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)<30.0) + fakeW_{Tag}_2l2jstatElUp*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)>30.0)",
#    'samples':['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
#}
#aliases["fakeWStatEleDown"] = {
#    "expr": f"fakeW_{Tag}_2l0jstatElDown*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)<30.0) + fakeW_{Tag}_2l1jstatElDown*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)>30.0 && Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)<30.0) + fakeW_{Tag}_2l2jstatElDown*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)>30.0)",
#    'samples':['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
#}
#aliases["fakeWStatMuUp"] = {
#    "expr": f"fakeW_{Tag}_2l0jstatMuUp*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)<30.0) + fakeW_{Tag}_2l1jstatMuUp*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)>30.0 && Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)<30.0) + fakeW_{Tag}_2l2jstatMuUp*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)>30.0)",
#    'samples':['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
#}
#aliases["fakeWStatMuDown"] = {
#    "expr": f"fakeW_{Tag}_2l0jstatMuDown*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)<30.0) + fakeW_{Tag}_2l1jstatMuDown*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)>30.0 && Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)<30.0) + fakeW_{Tag}_2l2jstatMuDown*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)>30.0)",
#    'samples':['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
#}


aliases['Top_pTrw'] = {
    'expr': '(topGenPt * antitopGenPt > 0.) * (TMath::Sqrt((0.103*TMath::Exp(-0.0118*topGenPt) - 0.000134*topGenPt + 0.973) * (0.103*TMath::Exp(-0.0118*antitopGenPt) - 0.000134*antitopGenPt + 0.973))) + (topGenPt * antitopGenPt <= 0.)',
    'samples': ['top']
}


##########################################################################
# B-Tagging WP: https://btv-wiki.docs.cern.ch/ScaleFactors/Run3Summer22/
##########################################################################

# Algo / WP / WP cut
btagging_WPs = {
    "DeepFlavB" : {
        "loose"    : "0.0583",
        "medium"   : "0.3086",
        "tight"    : "0.7183",
        "xtight"   : "0.8111",
        "xxtight"  : "0.9512",
    },
    "RobustParTAK4B" : {
        "loose"    : "0.0849",
        "medium"   : "0.4319",
        "tight"    : "0.8482",
        "xtight"   : "0.9151",
        "xxtight"  : "0.9874",
    },
    "PNetB" : {
        "loose"    : "0.0470",
        "medium"   : "0.2450",
        "tight"    : "0.6734",    
        "xtight"   : "0.7862",
        "xxtight"  : "0.9610",
    }
}

# Algo / SF name
btagging_SFs = {
    "DeepFlavB"      : "deepjet",
    "RobustParTAK4B" : "partTransformer",
    "PNetB"          : "partNet",
}

# Algorithm and WP selection
bAlgo = 'DeepFlavB' # ['DeepFlavB','RobustParTAK4B','PNetB'] 
WP    = 'loose'     # ['loose','medium','tight','xtight','xxtight']

# Access information from dictionaries
bWP   = btagging_WPs[bAlgo][WP]
bSF   = btagging_SFs[bAlgo]

WP_eval = 'L' # ['L', 'M', 'T', 'XT', 'XXT']
tagger = 'deepJet' # ['deepJet', 'particleNet', 'robustParticleTransformer']

#################
### B-tagging ###
#################

# Fixed BTV wp

# btagging MC efficiencies and SFs are read through the btagSF{flavour} object:
# - the first argument is the MC btagging efficiency root file
# - the second argument is the year from which SFs are retrieved from the POG/BTV json-pog correctionlib directory; 
#   allowed options are = ['2022_Summer22', '2022_Summer22EE', '2023_Summer23', '2023_Summer23BPix']
# The btagSF{flavour}_{shift} constructor executes the actual computation
# In this you specify the WP for the computation and the tagger using the WP_eval and tagger strings.

# We assume that you heve the efficiency maps root files in your configuration, as well as the evaluation macros
# If this is not the case, swap configurations with the proper path

# path = "your/path"

eff_map_year = '2022' # ['2022', '20222', '2023', '20232']
year = '2022_Summer22'

for flavour in ['bc', 'light']:
    for shift in ['central', 'up_uncorrelated', 'down_uncorrelated', 'up_correlated', 'down_correlated']:
        btagsf = 'btagSF' + flavour
        if shift != 'central':
            btagsf += '_' + shift
        aliases[btagsf] = {
            'linesToAdd': [f'#include "{configurations}macros/evaluate_btagSF{flavour}.cc"'],
            'linesToProcess': [f"ROOT.gInterpreter.Declare('btagSF{flavour} btagSF{flavour}_{shift} = btagSF{flavour}(\"{configurations}fixedWP/bTagEff_{eff_map_year}_ttbar_{bAlgo}_loose.root\", \"{year}\");')"],
            'expr': f'btagSF{flavour}_{shift}(CleanJet_pt, CleanJet_eta, CleanJet_jetIdx, nCleanJet, Jet_hadronFlavour, Jet_btag{bAlgo}, "{WP_eval}", "{shift}", "{tagger}")',
            'samples' : mc,
        }


# B tagging selections and scale factors
aliases['bVeto'] = {
    'expr': f'Sum(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{bAlgo}, CleanJet_jetIdx) > {bWP}) == 0'
}

aliases['bReq'] = { 
    'expr': f'Sum(CleanJet_pt > 30. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{bAlgo}, CleanJet_jetIdx) > {bWP}) >= 1'
}


aliases['bVetoSF'] = {
    'expr': f'TMath::Exp(Sum(LogVec((CleanJet_pt>20 && abs(CleanJet_eta)<2.5)*Take(Jet_btagSF_{bSF}_shape, CleanJet_jetIdx)+1*(CleanJet_pt<20 || abs(CleanJet_eta)>2.5))))',
    'samples': mc
}

aliases['bReqSF'] = {
    'expr': f'TMath::Exp(Sum(LogVec((CleanJet_pt> 30 && abs(CleanJet_eta)<2.5)*Take(Jet_btagSF_{bSF}_shape, CleanJet_jetIdx)+1*(CleanJet_pt< 30 || abs(CleanJet_eta)>2.5))))',
    'samples': mc
}

# CR definition
aliases['topcr'] = {
    'expr': 'mll > 100 && ((zeroJet && !bVeto) || bReq) && mtw2 > 30 && mth > 65 && mth < 150'
}

aliases['wwcr'] = {
    'expr': 'mth > 60 && mtw2 > 30 && mll > 100 && bVeto'
}


# SR definition
aliases['sr'] = {
    'expr': 'mll < 60 && mth > 65 && mth < 150 && bVeto'
}

# Overall b tag SF

aliases['btagSF'] = {
    'expr': '(bVeto || (topcr && zeroJet))*bVetoSF + (topcr && !zeroJet)*bReqSF',
    'samples': mc
}


# Systematic uncertainty variations standard B-tagger


#for shift in ['jes','lf','hf','lfstats1','lfstats2','hfstats1','hfstats2','cferr1','cferr2']:
#
#    for targ in ['bVeto', 'bReq']:
#        alias = aliases['%sSF%sup' % (targ, shift)] = copy.deepcopy(aliases['%sSF' % targ])
#        #alias['expr'] = alias['expr'].replace('btagSF_deepjet_shape', 'btagSF_deepjet_shape_up_%s' % shift)
#        alias['expr'] = alias['expr'].replace(f"btagSF_{bSF}_shape", f"btagSF_{bSF}_shape_up_{shift}")
#
#        alias = aliases['%sSF%sdown' % (targ, shift)] = copy.deepcopy(aliases['%sSF' % targ])
#        #alias['expr'] = alias['expr'].replace('btagSF_deepjet_shape', 'btagSF_deepjet_shape_down_%s' % shift)
#        alias['expr'] = alias['expr'].replace(f"btagSF_{bSF}_shape", f"btagSF_{bSF}_shape_down_{shift}")
#
#    aliases['btagSF%sup' % shift] = {
#        'expr': aliases['btagSF']['expr'].replace('SF', 'SF' + shift + 'up'),
#        'samples': mc
#    }
#
#    aliases['btagSF%sdown' % shift] = {
#        'expr': aliases['btagSF']['expr'].replace('SF', 'SF' + shift + 'down'),
#        'samples': mc
#    }


########################
### End of b tagging ###
########################

# data/MC scale factors

# Use this for the usual SF
aliases['SFweight'] = {
    'expr': ' * '.join(['SFweight2l', 'LepWPCut', 'LepWPSF', 'btagSFbc', 'btagSFlight']),
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

aliases['dymva'] = {
    'linesToAdd': [f'#include "{configurations}macros/dymva.cc"'],
    'class': 'dymva',
    'args': 'PuppiMET_pt, TkMET_pt, projtkmet, PuppiMET_pt/PuppiMET_sumEt, \
            Alt(CleanJet_eta, 0, -99) - 9999.9*(CleanJet_pt[0]<30), Alt(CleanJet_eta, 1, -99) - 9999.9*(CleanJet_pt[1]<30), \
            Alt(CleanJet_pt, 0, -99) - 9999.9*(CleanJet_pt[0]<30), Alt(CleanJet_pt, 1, -99) - 9999.9*(CleanJet_pt[1]<30), \
            mth, dphillmet, ptll, mjj, mll, mtw2, pTWW, dphijjmet, dphil1tkmet, dphil2tkmet, dphill, \
            Lepton_pt[0], Lepton_pt[1], Lepton_eta[0], Lepton_eta[1]',
    'afterNuis': True
}