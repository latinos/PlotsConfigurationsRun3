import os
import copy
import inspect

configurations = os.path.realpath(inspect.getfile(inspect.currentframe())) # this file

aliases = {}
aliases = OrderedDict()

mc     = [skey for skey in samples if skey not in ('Fake', 'DATA', 'Dyemb', 'DATA_EG', 'DATA_Mu', 'DATA_EMu', 'Fake_EG', 'Fake_Mu', 'Fake_EMu')]
mc_emb = [skey for skey in samples if skey not in ('Fake', 'DATA', 'DATA_Mu', 'DATA_EMu', 'Fake_EG', 'Fake_Mu', 'Fake_EMu')]

# LepCut2l__ele_mvaFall17V2Iso_WP90__mu_cut_Tight_HWWW_tthmva_80
eleWP = 'wp90iso'
muWP  = 'cut_TightID_POG'

#eleWP = 'mvaWinter22V2Iso_WP90'
#muWP  = 'cut_Tight_HWW'


aliases['LepWPCut'] = {
    #'expr': 'LepCut2l__ele_'+eleWP+'__mu_'+muWP,
    'expr': "_2lepOk ? (Lepton_isTightElectron_" + eleWP + "[0]>0.5 && Lepton_isTightMuon_" + muWP + "[0]>0.5) && (Lepton_isTightElectron_" + eleWP + "[1]>0.5 && Lepton_isTightMuon_" + muWP + "[1]>0.5) : false",
    'samples': mc + ['DATA', 'DATA_EG', 'DATA_Mu', 'DATA_EMu', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
}

aliases['LepWPSF'] = {
    'expr': 'LepSF2l__ele_'+eleWP+'__mu_'+muWP,
    'samples': mc
}

#aliases['Lepton_mvaIso_0'] = {
#    'expr': "abs(Lepton_pdgId[0])==11 ? Electron_mvaIso[Lepton_electronIdx[0]] : -2.0"
#}

#aliases['Lepton_mvaIso_1'] = {
#    'expr': "abs(Lepton_pdgId[1])==11 ? Electron_mvaIso[Lepton_electronIdx[1]] : -2.0"
#}

Tag = 'ele_'+eleWP+'_mu_'+muWP

aliases["fakeW"] = {
    "expr": f"fakeW_{Tag}_2l0j*(Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 0, 0)<30.0) + fakeW_{Tag}_2l1j*(Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 0, 0)>30.0 && Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 1, 0)<30.0) + fakeW_{Tag}_2l2j*(Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 1, 0)>30.0)",
    'samples': ['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
}
aliases["fakeWEleUp"] = {
    "expr": f"fakeW_{Tag}_2l0jElUp*(Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 0, 0)<30.0) + fakeW_{Tag}_2l1jElUp*(Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 0, 0)>30.0 && Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 1, 0)<30.0) + fakeW_{Tag}_2l2jElUp*(Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 1, 0)>30.0)",
    'samples': ['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
}
aliases["fakeWEleDown"] = {
    "expr": f"fakeW_{Tag}_2l0jElDown*(Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 0, 0)<30.0) + fakeW_{Tag}_2l1jElDown*(Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 0, 0)>30.0 && Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 1, 0)<30.0) + fakeW_{Tag}_2l2jElDown*(Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 1, 0)>30.0)",
    'samples': ['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
}
aliases["fakeWMuUp"] = {
    "expr": f"fakeW_{Tag}_2l0jMuUp*(Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 0, 0)<30.0) + fakeW_{Tag}_2l1jMuUp*(Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 0, 0)>30.0 && Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 1, 0)<30.0) + fakeW_{Tag}_2l2jMuUp*(Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 1, 0)>30.0)",
    'samples': ['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
}
aliases["fakeWMuDown"] = {
    "expr": f"fakeW_{Tag}_2l0jMuDown*(Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 0, 0)<30.0) + fakeW_{Tag}_2l1jMuDown*(Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 0, 0)>30.0 && Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 1, 0)<30.0) + fakeW_{Tag}_2l2jMuDown*(Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 1, 0)>30.0)",
    'samples': ['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
}
aliases["fakeWStatEleUp"] = {
    "expr": f"fakeW_{Tag}_2l0jstatElUp*(Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 0, 0)<30.0) + fakeW_{Tag}_2l1jstatElUp*(Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 0, 0)>30.0 && Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 1, 0)<30.0) + fakeW_{Tag}_2l2jstatElUp*(Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 1, 0)>30.0)",
    'samples': ['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
}
aliases["fakeWStatEleDown"] = {
    "expr": f"fakeW_{Tag}_2l0jstatElDown*(Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 0, 0)<30.0) + fakeW_{Tag}_2l1jstatElDown*(Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 0, 0)>30.0 && Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 1, 0)<30.0) + fakeW_{Tag}_2l2jstatElDown*(Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 1, 0)>30.0)",
    'samples': ['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
}
aliases["fakeWStatMuUp"] = {
    "expr": f"fakeW_{Tag}_2l0jstatMuUp*(Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 0, 0)<30.0) + fakeW_{Tag}_2l1jstatMuUp*(Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 0, 0)>30.0 && Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 1, 0)<30.0) + fakeW_{Tag}_2l2jstatMuUp*(Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 1, 0)>30.0)",
    'samples': ['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
}
aliases["fakeWStatMuDown"] = {
    "expr": f"fakeW_{Tag}_2l0jstatMuDown*(Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 0, 0)<30.0) + fakeW_{Tag}_2l1jstatMuDown*(Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 0, 0)>30.0 && Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 1, 0)<30.0) + fakeW_{Tag}_2l2jstatMuDown*(Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 1, 0)>30.0)",
    'samples': ['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
}

"""
# # Fake leptons transfer factor
aliases['fakeW'] = {
    'expr': 'fakeW2l_ele_'+eleWP+'_mu_'+muWP,
    'samples': ['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
}
# And variations - already divided by central values in formulas !
aliases['fakeWEleUp'] = {
    'expr': 'fakeW2l_ele_'+eleWP+'_mu_'+muWP+'_EleUp',
    'samples': ['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
}
aliases['fakeWEleDown'] = {
    'expr': 'fakeW2l_ele_'+eleWP+'_mu_'+muWP+'_EleDown',
    'samples': ['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
}
aliases['fakeWMuUp'] = {
    'expr': 'fakeW2l_ele_'+eleWP+'_mu_'+muWP+'_MuUp',
    'samples': ['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
}
aliases['fakeWMuDown'] = {
    'expr': 'fakeW2l_ele_'+eleWP+'_mu_'+muWP+'_MuDown',
    'samples': ['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
}
aliases['fakeWStatEleUp'] = {
    'expr': 'fakeW2l_ele_'+eleWP+'_mu_'+muWP+'_statEleUp',
    'samples': ['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
}
aliases['fakeWStatEleDown'] = {
    'expr': 'fakeW2l_ele_'+eleWP+'_mu_'+muWP+'_statEleDown',
    'samples': ['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
}
aliases['fakeWStatMuUp'] = {
    'expr': 'fakeW2l_ele_'+eleWP+'_mu_'+muWP+'_statMuUp',
    'samples': ['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
}
aliases['fakeWStatMuDown'] = {
    'expr': 'fakeW2l_ele_'+eleWP+'_mu_'+muWP+'_statMuDown',
    'samples': ['Fake', 'Fake_EG', 'Fake_Mu', 'Fake_EMu']
}
"""

# gen-matching to prompt only (GenLepMatch2l matches to *any* gen lepton)
aliases['PromptGenLepMatch2l'] = {
    'expr': 'Alt(Lepton_promptgenmatched, 0, 0) * Alt(Lepton_promptgenmatched, 1, 0)',
    'samples': mc
}

aliases['Top_pTrw'] = {
    'expr': '(topGenPt * antitopGenPt > 0.) * (TMath::Sqrt((0.103*TMath::Exp(-0.0118*topGenPt) - 0.000134*topGenPt + 0.973) * (0.103*TMath::Exp(-0.0118*antitopGenPt) - 0.000134*antitopGenPt + 0.973))) + (topGenPt * antitopGenPt <= 0.)',
    'samples': ['top','top_EE']
}

# Jet bins
# using Alt$(CleanJet_pt[n], 0) instead of Sum$(CleanJet_pt >= 30) because jet pt ordering is not strictly followed in JES-varied samples

# No jet with pt > 30 GeV
aliases['zeroJet'] = {
    'expr': 'Alt(MyCleanJet_pt, 0, 0) < 30.'
}

aliases['oneJet'] = {
    'expr': 'Alt(MyCleanJet_pt, 0, 0) > 30.'
}

aliases['multiJet'] = {
    'expr': 'Alt(MyCleanJet_pt, 1, 0) > 30.'
}

# DeepFlavB = DeepJet  
bWP_loose_deepFlavB  = '0.0583'
bWP_medium_deepFlavB = '0.3086'
bWP_tight_deepFlavB  = '0.7183'

# Actual algo and WP definition. BE CONSISTENT!!
bAlgo = 'DeepFlavB'          # ['DeepB','DeepFlavB'] 
bWP   = bWP_loose_deepFlavB # [bWP_loose_deepB, bWP_loose_deepFlavB]
bSF   = 'deepjet'        # ['deepcsv','deepjet']

aliases['bVeto'] = {
    'expr': f'Sum(MyCleanJet_pt > 20. && abs(MyCleanJet_eta) < 2.5 && Take(Jet_btag{bAlgo}, MyCleanJet_jetIdx) > {bWP}) == 0'
}

aliases['bReq'] = { 
    'expr': f'Sum(MyCleanJet_pt > 30. && abs(MyCleanJet_eta) < 2.5 && Take(Jet_btag{bAlgo}, MyCleanJet_jetIdx) > {bWP}) >= 1'
}

# CR definition

aliases['topcr'] = {
    'expr': '(Lepton_pdgId[0] * Lepton_pdgId[1] == -11*13) && mll > 12 && ((zeroJet && !bVeto) || bReq)'
}


# SF
aliases['bVetoSF'] = {
    'expr': 'TMath::Exp(Sum(LogVec((MyCleanJet_pt>20 && abs(MyCleanJet_eta)<2.5)*Take(Jet_btagSF_deepjet_shape, MyCleanJet_jetIdx)+1*(MyCleanJet_pt<20 || abs(MyCleanJet_eta)>2.5))))',
    'samples': mc
}

aliases['bReqSF'] = {
    'expr': 'TMath::Exp(Sum(LogVec((MyCleanJet_pt>30 && abs(MyCleanJet_eta)<2.5)*Take(Jet_btagSF_deepjet_shape, MyCleanJet_jetIdx)+1*(MyCleanJet_pt<30 || abs(MyCleanJet_eta)>2.5))))',
    'samples': mc
}

aliases['btagSF'] = {
    'expr': '(bVeto || (topcr && zeroJet))*bVetoSF + (topcr && !zeroJet)*bReqSF',
    'samples': mc
}


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


# data/MC scale factors
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

aliases["nMyCleanJet"] = {
    'expr': 'MyCleanJet_pt.size()'
}

aliases['WWvariables_B'] = {
    'linesToAdd': [".L /afs/cern.ch/work/s/sblancof/private/Run3Analysis/mkShapesRDF/examples/extended/BoostVar.C+"],
    'class': "getVariables",
    'args': 'Lepton_pt,Lepton_eta,Lepton_phi,Lepton_pdgId,PuppiMET_pt,PuppiMET_phi',
    'afterNuis': True
}

aliases["cosTheta_CS"] = {
    'expr': 'WWvariables_B[0]',
    'afterNuis': True
}
aliases["cosTheta_star"] = {
    'expr': 'WWvariables_B[1]',
    'afterNuis': True
}
aliases["dphi_star3"] = {
    'expr': 'WWvariables_B[2]',
    'afterNuis': True
}
aliases["costheta_CS2"] = {
    'expr': 'WWvariables_B[3]',
    'afterNuis': True
}
aliases["ME_WW_cos"] = {
    'expr': 'WWvariables_B[4]',
    'afterNuis': True
}
aliases["ME_WW_cos1"] = {
    'expr': 'WWvariables_B[5]',
    'afterNuis': True
}
aliases["ME_WW_Eta"] = {
    'expr': 'WWvariables_B[6]',
    'afterNuis': True
}

aliases['WWvariables'] = {
    'linesToAdd': [".L /afs/cern.ch/work/s/sblancof/private/Run3Analysis/mkShapesRDF/examples/polarization/DelaPhiMET.C+"],
    'class': "getVariables",
    'args': 'Lepton_pt,Lepton_phi,Lepton_eta,PuppiMET_pt,PuppiMET_phi,TkMET_pt,TkMET_phi',
    'afterNuis': True
}

aliases['mll_'] = {
    'expr': 'WWvariables[9]',
    'afterNuis': True
}
aliases['mth_'] = {
    'expr': 'WWvariables[10]',
    'afterNuis': True
}
aliases['mtw1_'] = {
    'expr': 'WWvariables[11]',
    'afterNuis': True
}
aliases['mtw2_'] = {
    'expr': 'WWvariables[12]',
    'afterNuis': True
}
aliases['ptll_'] = {
    'expr': 'WWvariables[7]',
    'afterNuis': True
}
aliases['drll_'] = {
    'expr': 'WWvariables[8]',
    'afterNuis': True
}
aliases['dphill_'] = {
    'expr': 'WWvariables[6]',
    'afterNuis': True
}
aliases['detall_'] = {
    'expr': 'WWvariables[5]',
    'afterNuis': True
}
aliases['mpmet'] = {
    'expr': 'WWvariables[4]',
    'afterNuis': True
}
aliases['dphilmet_'] = {
    'expr': 'WWvariables[0]',
    'afterNuis': True
}

aliases['RandomForest_evaluator'] = {
    'linesToAdd' : ['.L /afs/cern.ch/work/s/sblancof/private/Run3Analysis/mkShapesRDF/examples/extended/evaluate_RF_polarization.cc+'],
    'class' : 'evaluate_dnn',
    'args': 'Lepton_pt[0],Lepton_pt[1],mll_,mth_,mtw1_,mtw2_,ptll_,drll_,dphill_,PuppiMET_pt,PuppiMET_phi,detall_,mpmet,dphilmet_,cosTheta_CS,dphi_star3,costheta_CS2,ME_WW_cos,ME_WW_cos1,ME_WW_Eta',
    'afterNuis': True
}


