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


# LepCut2l__ele_wp90iso__mu_cut_TightID_POG
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

#aliases['Lepton_mvaIso_0'] = {
#    'expr': "abs(Lepton_pdgId[0])==11 ? Electron_mvaIso[Lepton_electronIdx[0]] : -2.0"
#}

#aliases['Lepton_mvaIso_1'] = {
#    'expr': "abs(Lepton_pdgId[1])==11 ? Electron_mvaIso[Lepton_electronIdx[1]] : -2.0"
#}

Tag = 'ele_'+eleWP+'_mu_'+muWP

aliases["fakeW"] = {
    "expr": f"fakeW_{Tag}_2l0j*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)<30.0) + fakeW_{Tag}_2l1j*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)>30.0 && Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)<30.0) + fakeW_{Tag}_2l2j*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)>30.0)",
    'samples': ['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
}
aliases["fakeWEleUp"] = {
    "expr": f"fakeW_{Tag}_2l0jElUp*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)<30.0) + fakeW_{Tag}_2l1jElUp*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)>30.0 && Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)<30.0) + fakeW_{Tag}_2l2jElUp*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)>30.0)",
    'samples':['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
}
aliases["fakeWEleDown"] = {
    "expr": f"fakeW_{Tag}_2l0jElDown*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)<30.0) + fakeW_{Tag}_2l1jElDown*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)>30.0 && Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)<30.0) + fakeW_{Tag}_2l2jElDown*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)>30.0)",
    'samples':['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
}
aliases["fakeWMuUp"] = {
    "expr": f"fakeW_{Tag}_2l0jMuUp*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)<30.0) + fakeW_{Tag}_2l1jMuUp*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)>30.0 && Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)<30.0) + fakeW_{Tag}_2l2jMuUp*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)>30.0)",
    'samples':['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
}
aliases["fakeWMuDown"] = {
    "expr": f"fakeW_{Tag}_2l0jMuDown*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)<30.0) + fakeW_{Tag}_2l1jMuDown*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)>30.0 && Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)<30.0) + fakeW_{Tag}_2l2jMuDown*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)>30.0)",
    'samples':['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
}
aliases["fakeWStatEleUp"] = {
    "expr": f"fakeW_{Tag}_2l0jstatElUp*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)<30.0) + fakeW_{Tag}_2l1jstatElUp*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)>30.0 && Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)<30.0) + fakeW_{Tag}_2l2jstatElUp*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)>30.0)",
    'samples':['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
}
aliases["fakeWStatEleDown"] = {
    "expr": f"fakeW_{Tag}_2l0jstatElDown*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)<30.0) + fakeW_{Tag}_2l1jstatElDown*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)>30.0 && Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)<30.0) + fakeW_{Tag}_2l2jstatElDown*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)>30.0)",
    'samples':['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
}
aliases["fakeWStatMuUp"] = {
    "expr": f"fakeW_{Tag}_2l0jstatMuUp*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)<30.0) + fakeW_{Tag}_2l1jstatMuUp*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)>30.0 && Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)<30.0) + fakeW_{Tag}_2l2jstatMuUp*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)>30.0)",
    'samples':['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
}
aliases["fakeWStatMuDown"] = {
    "expr": f"fakeW_{Tag}_2l0jstatMuDown*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)<30.0) + fakeW_{Tag}_2l1jstatMuDown*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 0, 0)>30.0 && Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)<30.0) + fakeW_{Tag}_2l2jstatMuDown*(Alt(CleanJet_pt[abs(CleanJet_eta)<=2.5], 1, 0)>30.0)",
    'samples':['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
}


aliases['Top_pTrw'] = {
    'expr': '(topGenPt * antitopGenPt > 0.) * (TMath::Sqrt((0.103*TMath::Exp(-0.0118*topGenPt) - 0.000134*topGenPt + 0.973) * (0.103*TMath::Exp(-0.0118*antitopGenPt) - 0.000134*antitopGenPt + 0.973))) + (topGenPt * antitopGenPt <= 0.)',
    'samples': ['top']
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
    "PNetB"          : "partNet",
}

# Algorithm and WP selection
bAlgo = 'RobustParTAK4B' # ['DeepFlavB','RobustParTAK4B','PNetB'] 
WP    = 'loose'     # ['loose','medium','tight','xtight','xxtight']

# Access information from dictionaries
bWP   = btagging_WPs[bAlgo][WP]
bSF   = btagging_SFs[bAlgo]

#################
### B-tagging ###
#################

# Fixed BTV wp

# btagging MC efficiencies and SFs are read through the btagSF{flavour} object:
# - the first argument is the MC btagging efficiency root file
# - the second argument is the year from which SFs are retrieved from the POG/BTV json-pog correctionlib directory; 
#   allowed options are = ["2022_Summer22", "2022_Summer22EE", "2023_Summer23", "2023_Summer23BPix"]
# The btagSF{flavour}_{shift} constructor executes the actual computation

# btv_path variable must be updated with the proper year
# replace it with the proper path if you move b-tagging efficiency root files somewhere else

#year = "2022_Summer22EE" # allowed options are = ["2022_Summer22", "2022_Summer22EE", "2023_Summer23", "2023_Summer23BPix"]

btv_path = "/afs/cern.ch/user/s/squinto/mkShapesRDF/mkShapesRDF/processor/data/jsonpog-integration/POG/BTV/2022_Summer22EE"

for flavour in ['bc', 'light']:
    for shift in ['central', 'up_uncorrelated', 'down_uncorrelated', 'up_correlated', 'down_correlated']:
        btagsf = 'btagSF' + flavour
        if shift != 'central':
            btagsf += '_' + shift
        aliases[btagsf] = {
            'linesToAdd': [f'#include "{configurations}evaluate_btagSF{flavour}.cc"'],
            'linesToProcess': [f"ROOT.gInterpreter.Declare('btagSF{flavour} btagSF{flavour}_{shift} = btagSF{flavour}(\"{configurations}bTagEff_20222_ttbar_RobustParTAK4B_loose.root\");')"],
            'expr': f'btagSF{flavour}_{shift}(CleanJet_pt, CleanJet_eta, CleanJet_jetIdx, nCleanJet, Jet_hadronFlavour, Jet_btagDeepFlavB, "L", "{shift}")',
            'samples' : mc,
        }

# B tagging selections and scale factors
aliases['bVeto'] = {
    'expr': f'Sum(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{bAlgo}, CleanJet_jetIdx) > {bWP}) == 0'
}

aliases['bReq'] = { 
    'expr': f'Sum(CleanJet_pt > 30. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{bAlgo}, CleanJet_jetIdx) > {bWP}) >= 1'
}
'''
aliases['bVetoSF'] = {
    'expr': 'TMath::Exp(Sum(LogVec((CleanJet_pt>20 && abs(CleanJet_eta)<2.5)*Take(Jet_btagSF_{}_shape, CleanJet_jetIdx)+1*(CleanJet_pt<20 || abs(CleanJet_eta)>2.5))))'.format(bSF),
    'samples': mc
}

aliases['bReqSF'] = {
    'expr': 'TMath::Exp(Sum(LogVec((CleanJet_pt> 30 && abs(CleanJet_eta)<2.5)*Take(Jet_btagSF_{}_shape, CleanJet_jetIdx)+1*(CleanJet_pt< 30 || abs(CleanJet_eta)>2.5))))'.format(bSF),
    'samples': mc
}
# Overall b tag SF

aliases['btagSF'] = {
    'expr': '(bVeto || (topcr && zeroJet))*bVetoSF + (topcr && !zeroJet)*bReqSF',
    'samples': mc
}

# Systematic uncertainty variations standard B-tagger

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
'''
########################
### End of b tagging ###
########################


# CR definition
aliases['topcr'] = {
    'expr': 'mtw2 > 30 && mll > 50 && ((zeroJet && !bVeto) || bReq)'
}
aliases['dycr'] = {
    'expr': 'mth < 60 && mll > 40 && mll < 80 && bVeto'
}
aliases['wwcr'] = {
    'expr': 'mth > 60 && mtw2 > 30 && mll > 100 && bVeto'
}


# SR definition
aliases['sr'] = {
    'expr': 'mth > 60 && mtw2 > 30 && bVeto'
}

# data/MC scale factors

# Use this for the usual SF
aliases['SFweight'] = {
    'expr': ' * '.join(['SFweight2l', 'LepWPCut', 'LepWPSF', 'btagSFbc', 'btagSFlight']),
    #'expr': ' * '.join(['SFweight2l', 'LepWPCut', 'LepWPSF','btagSF']),
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

"""
#####################################
####### 2D Histogram mllvsmth ####### 
#####################################     
bin_mll = ['12.', '17.', '25.', '30.', '35.', '40.', '45.', '65.', '200.']
bin_mth = ['60.', '95.', '110.', '135.', '200.']
mllmt2D = ''
for i in range(len(bin_mth)-1):
  for j in range(len(bin_mll)-1):
    if i+j != len(bin_mth)+len(bin_mll)-4: 
      mllmt2D+='('+bin_mth[i]+'<mth)*(mth<'+bin_mth[i+1]+')*(('+str((len(bin_mll)-1)*i)+')+('+str(j+1)+'))*('+bin_mll[j]+'<mll)*(mll<'+bin_mll[j+1]+')+'
    else: 
      mllmt2D+='('+bin_mth[i]+'<mth)*(mth<'+bin_mth[i+1]+')*(('+str((len(bin_mll)-1)*i)+')+('+str(j+1)+'))*('+bin_mll[j]+'<mll)*(mll<'+bin_mll[j+1]+')'

aliases['mllVSmth_optim'] = {
    'expr' : mllmt2D,
    'afterNuis' : True
}


aliases['adnn_SigVSBkg'] = {
  'linesToAdd': ['#include "%s/adnn_jer_sigVSbkg.cc"' % configurations],
  'class': 'adnn_SigVSBkg',
  'args': ' PV_npvsGood, mll, mth, ptll, drll, dphill, \
            Alt(Take(Jet_btagDeepFlavB, CleanJet_jetIdx), 0, -99), TkMET_pt, PuppiMET_pt, \
            Alt(CleanJet_pt, 0, 0)*(CleanJet_pt[0]>30), Alt(CleanJet_pt, 1, 0)*(CleanJet_pt[1]>30), \
            Alt(CleanJet_eta, 0, -99)*(Alt(CleanJet_pt, 0, 0)>30)-99*(Alt(CleanJet_pt,0,0)<30), \
            Alt(CleanJet_eta, 1, -99)*(Alt(CleanJet_pt, 1, 0)>30)-99*(Alt(CleanJet_pt,1,0)<30), \
            Lepton_pt[0], Lepton_pt[1], Lepton_eta[0], Lepton_eta[1], Lepton_phi[0], Lepton_phi[1], \
            Sum(CleanJet_pt>30)',
    'afterNuis' : True
  #'samples': mc
}

aliases['snn_SigVSBkg_0j'] = {
  # 'linesToAdd': ['#include "%s/snn_sigVSbkg.cc"' % configurations],
  'linesToAdd': ['#include "/afs/cern.ch/user/s/squinto/private/work/PlotsConfigurationsRun3/HWW/macros/snn0j_sigVSbkg.cc"'],
  'class': 'snn0j_SigVSBkg',
  'args': ' PV_npvsGood, mll, mth, ptll, drll, dphill, \
            Alt(Take(Jet_btagDeepFlavB, CleanJet_jetIdx), 0, -99), TkMET_pt, PuppiMET_pt, \
            Alt(CleanJet_pt, 0, 0)*(CleanJet_pt[0]>30), Alt(CleanJet_pt, 1, 0)*(CleanJet_pt[1]>30), \
            Alt(CleanJet_eta, 0, -99)*(Alt(CleanJet_pt, 0, 0)>30)-99*(Alt(CleanJet_pt,0,0)<30), \
            Alt(CleanJet_eta, 1, -99)*(Alt(CleanJet_pt, 1, 0)>30)-99*(Alt(CleanJet_pt,1,0)<30), \
            Lepton_pt[0], Lepton_pt[1], Lepton_eta[0], Lepton_eta[1], Lepton_phi[0], Lepton_phi[1], \
            Sum(CleanJet_pt>30)',
    'afterNuis' : True
  #'samples': mc
}

aliases['snn_SigVSBkg_1j'] = {
  # 'linesToAdd': ['#include "%s/snn_sigVSbkg.cc"' % configurations],
  'linesToAdd': ['#include "/afs/cern.ch/user/s/squinto/private/work/PlotsConfigurationsRun3/HWW/macros/snn1j_sigVSbkg.cc"'],
  'class': 'snn1j_SigVSBkg',
  'args': ' PV_npvsGood, mll, mth, ptll, drll, dphill, \
            Alt(Take(Jet_btagDeepFlavB, CleanJet_jetIdx), 0, -99), TkMET_pt, PuppiMET_pt, \
            Alt(CleanJet_pt, 0, 0)*(CleanJet_pt[0]>30), Alt(CleanJet_pt, 1, 0)*(CleanJet_pt[1]>30), \
            Alt(CleanJet_eta, 0, -99)*(Alt(CleanJet_pt, 0, 0)>30)-99*(Alt(CleanJet_pt,0,0)<30), \
            Alt(CleanJet_eta, 1, -99)*(Alt(CleanJet_pt, 1, 0)>30)-99*(Alt(CleanJet_pt,1,0)<30), \
            Lepton_pt[0], Lepton_pt[1], Lepton_eta[0], Lepton_eta[1], Lepton_phi[0], Lepton_phi[1], \
            Sum(CleanJet_pt>30)',
    'afterNuis' : True
  #'samples': mc
}

aliases['snn_SigVSBkg_2j'] = {
  # 'linesToAdd': ['#include "%s/snn_sigVSbkg.cc"' % configurations],
  'linesToAdd': ['#include "/afs/cern.ch/user/s/squinto/private/work/PlotsConfigurationsRun3/HWW/macros/snn2j_sigVSbkg.cc"'],
  'class': 'snn2j_SigVSBkg',
  'args': ' PV_npvsGood, mll, mth, ptll, drll, dphill, \
            Alt(Take(Jet_btagDeepFlavB, CleanJet_jetIdx), 0, -99), TkMET_pt, PuppiMET_pt, \
            Alt(CleanJet_pt, 0, 0)*(CleanJet_pt[0]>30), Alt(CleanJet_pt, 1, 0)*(CleanJet_pt[1]>30), \
            Alt(CleanJet_eta, 0, -99)*(Alt(CleanJet_pt, 0, 0)>30)-99*(Alt(CleanJet_pt,0,0)<30), \
            Alt(CleanJet_eta, 1, -99)*(Alt(CleanJet_pt, 1, 0)>30)-99*(Alt(CleanJet_pt,1,0)<30), \
            Lepton_pt[0], Lepton_pt[1], Lepton_eta[0], Lepton_eta[1], Lepton_phi[0], Lepton_phi[1], \
            Sum(CleanJet_pt>30)',
    'afterNuis' : True
  #'samples': mc
}

aliases['dbnn_SigVSBkg_0j'] = {
  'linesToAdd': ['#include "/afs/cern.ch/user/s/squinto/private/work/PlotsConfigurationsRun3/HWW/macros/dbnn0j_sigVSbkg.cc"'],
  'class': 'dbnn0j_SigVSBkg',
  'args': ' PV_npvsGood, mll, mth, ptll, drll, dphill, \
            Alt(Take(Jet_btagDeepFlavB, CleanJet_jetIdx), 0, -99), TkMET_pt, PuppiMET_pt, \
            Alt(CleanJet_pt, 0, 0)*(CleanJet_pt[0]>30), Alt(CleanJet_pt, 1, 0)*(CleanJet_pt[1]>30), \
            Alt(CleanJet_eta, 0, -99)*(Alt(CleanJet_pt, 0, 0)>30)-99*(Alt(CleanJet_pt,0,0)<30), \
            Alt(CleanJet_eta, 1, -99)*(Alt(CleanJet_pt, 1, 0)>30)-99*(Alt(CleanJet_pt,1,0)<30), \
            Lepton_pt[0], Lepton_pt[1], Lepton_eta[0], Lepton_eta[1], Lepton_phi[0], Lepton_phi[1], \
            Sum(CleanJet_pt>30)',
    'afterNuis' : True
  #'samples': mc
}

aliases['dbnn_SigVSBkg_1j'] = {
  'linesToAdd': ['#include "/afs/cern.ch/user/s/squinto/private/work/PlotsConfigurationsRun3/HWW/macros/dbnn1j_sigVSbkg.cc"'],
  'class': 'dbnn1j_SigVSBkg',
  'args': ' PV_npvsGood, mll, mth, ptll, drll, dphill, \
            Alt(Take(Jet_btagDeepFlavB, CleanJet_jetIdx), 0, -99), TkMET_pt, PuppiMET_pt, \
            Alt(CleanJet_pt, 0, 0)*(CleanJet_pt[0]>30), Alt(CleanJet_pt, 1, 0)*(CleanJet_pt[1]>30), \
            Alt(CleanJet_eta, 0, -99)*(Alt(CleanJet_pt, 0, 0)>30)-99*(Alt(CleanJet_pt,0,0)<30), \
            Alt(CleanJet_eta, 1, -99)*(Alt(CleanJet_pt, 1, 0)>30)-99*(Alt(CleanJet_pt,1,0)<30), \
            Lepton_pt[0], Lepton_pt[1], Lepton_eta[0], Lepton_eta[1], Lepton_phi[0], Lepton_phi[1], \
            Sum(CleanJet_pt>30)',
    'afterNuis' : True
  #'samples': mc
}

aliases['dbnn_SigVSBkg_2j'] = {
  'linesToAdd': ['#include "/afs/cern.ch/user/s/squinto/private/work/PlotsConfigurationsRun3/HWW/macros/dbnn2j_sigVSbkg.cc"'],
  'class': 'dbnn2j_SigVSBkg',
  'args': ' PV_npvsGood, mll, mth, ptll, drll, dphill, \
            Alt(Take(Jet_btagDeepFlavB, CleanJet_jetIdx), 0, -99), TkMET_pt, PuppiMET_pt, \
            Alt(CleanJet_pt, 0, 0)*(CleanJet_pt[0]>30), Alt(CleanJet_pt, 1, 0)*(CleanJet_pt[1]>30), \
            Alt(CleanJet_eta, 0, -99)*(Alt(CleanJet_pt, 0, 0)>30)-99*(Alt(CleanJet_pt,0,0)<30), \
            Alt(CleanJet_eta, 1, -99)*(Alt(CleanJet_pt, 1, 0)>30)-99*(Alt(CleanJet_pt,1,0)<30), \
            Lepton_pt[0], Lepton_pt[1], Lepton_eta[0], Lepton_eta[1], Lepton_phi[0], Lepton_phi[1], \
            Sum(CleanJet_pt>30)',
    'afterNuis' : True
  #'samples': mc
}
"""
