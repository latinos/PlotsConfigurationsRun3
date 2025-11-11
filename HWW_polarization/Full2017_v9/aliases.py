import os
import copy
import inspect

configurations = os.path.realpath(inspect.getfile(inspect.currentframe()))


aliases = {}
aliases = OrderedDict()

mc = [skey for skey in samples if skey not in ('Fake', 'DATA', 'Dyemb')]
mc_emb = [skey for skey in samples if skey not in ('Fake', 'DATA')]

eleWP = 'mvaFall17V2Iso_WP90'
muWP  = 'cut_Tight_HWWW'

aliases['LepWPCut'] = {
    'expr': 'LepCut2l__ele_mvaFall17V2Iso_WP90__mu_cut_Tight_HWWW*\
    ( ((abs(Lepton_pdgId[0])==13 && Muon_mvaTTH[Lepton_muonIdx[0]]>0.82) || (abs(Lepton_pdgId[0])==11 && Lepton_mvaTTH_UL[0]>0.90)) \
    && ((abs(Lepton_pdgId[1])==13 && Muon_mvaTTH[Lepton_muonIdx[1]]>0.82) || (abs(Lepton_pdgId[1])==11 && Lepton_mvaTTH_UL[1]>0.90)) )',
    'samples': mc + ['DATA','Fake','Dyemb']
}

aliases['LepWPSF'] = {
    'expr': 'LepSF2l__ele_'+eleWP+'__mu_'+muWP,
    'samples': mc_emb
}

# ttHMVA SFs and uncertainties 
# RVecD results = {SF, SF_up_out_el, SF_up_out_mu, SF_down_out_el, SF_down_out_mu};
aliases['LepWPttHMVASF_tot'] = {
    'linesToProcess':['ROOT.gSystem.Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/ttHMVASF_cc.so","", ROOT.kTRUE)',
                      'ROOT.gInterpreter.Declare("ttHMVASF tth_sf;")'],
    'expr' :   'tth_sf("2017", 2, "all", "nominal",Lepton_pt,Lepton_eta,Lepton_pdgId)',
    'samples'    : mc
}

aliases['LepWPttHMVASF'] = {
    'expr' : 'LepWPttHMVASF_tot[0]',
    'samples'    : mc
}
aliases['LepWPttHMVASFEleUp'] = {
    'expr' : 'LepWPttHMVASF_tot[1]',
    'samples'    : mc
}
aliases['LepWPttHMVASFEleDown'] = {
    'expr' : 'LepWPttHMVASF_tot[2]',
    'samples'    : mc
}
aliases['LepWPttHMVASFMuUp'] = {
    'expr' : 'LepWPttHMVASF_tot[3]',
    'samples'    : mc
}
aliases['LepWPttHMVASFMuDown'] = {
    'expr' : 'LepWPttHMVASF_tot[4]',
    'samples'    : mc
}

aliases['embednorm'] = {
    'linesToProcess':['ROOT.gSystem.Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/EmbededNormalization_cc.so","", ROOT.kTRUE)',
                      """ROOT.gInterpreter.Declare('EmbededNormalization emb_sf("2017UL");')"""],
    'expr' :   'emb_sf(GenPart_pt, GenPart_eta, GenPart_phi, GenPart_pdgId, GenPart_genPartIdxMother, Lepton_pt, Lepton_eta, Lepton_phi, Lepton_pdgId, Lepton_muonIdx, Lepton_electronIdx, Muon_genPartIdx, Electron_genPartIdx)',
    'samples'    : 'Dyemb'
}

aliases['embedtotal'] = {
    'expr': 'embednorm*genWeight*TriggerSFWeight_2l',
    'samples': 'Dyemb'
}

# gen-matching to prompt only (GenLepMatch2l matches to *any* gen lepton)
aliases['PromptGenLepMatch2l'] = {
    'expr': 'Alt(Lepton_promptgenmatched,0,0)*Alt(Lepton_promptgenmatched,1,0)',
    'samples': mc
}

# Fake leptons transfer factor
aliases['fakeW'] = {
    'linesToAdd' : ['#include "/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/fake_rate_reader_class.cc"'],
    'linesToProcess':["ROOT.gInterpreter.Declare('fake_rate_reader fr_reader = fake_rate_reader(\"2017\", \"90\", \"82\", 0.90, 0.82, \"nominal\", 2, \"std\");')"],
    'expr': 'fr_reader(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_cut_Tight_HWWW, Lepton_isTightElectron_mvaFall17V2Iso_WP90, Lepton_mvaTTH_UL, Muon_mvaTTH, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'    : ['Fake']
}

# And variations - already divided by central values in formulas !
aliases['fakeWEleUp'] = {
    'linesToAdd' : ['#include "/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/fake_rate_reader_class.cc"'],
    'linesToProcess':["ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_EleUp = fake_rate_reader(\"2017\", \"90\", \"82\", 0.90, 0.82, \"EleUp\", 2, \"std\");')"],
    'expr': 'fr_reader_EleUp(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_cut_Tight_HWWW, Lepton_isTightElectron_mvaFall17V2Iso_WP90, Lepton_mvaTTH_UL, Muon_mvaTTH, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
        'samples': ['Fake']
}
aliases['fakeWEleDown'] = {
    'linesToAdd' : ['#include "/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/fake_rate_reader_class.cc"'],
    'linesToProcess':["ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_EleDown = fake_rate_reader(\"2017\", \"90\", \"82\", 0.90, 0.82, \"EleDown\", 2, \"std\");')"],
    'expr': 'fr_reader_EleDown(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_cut_Tight_HWWW, Lepton_isTightElectron_mvaFall17V2Iso_WP90, Lepton_mvaTTH_UL, Muon_mvaTTH, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
        'samples': ['Fake']
}

aliases['fakeWMuUp'] = {
    'linesToAdd' : ['#include "/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/fake_rate_reader_class.cc"'],
    'linesToProcess':["ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_MuUp = fake_rate_reader(\"2017\", \"90\", \"82\", 0.90, 0.82, \"MuUp\", 2, \"std\");')"],
    'expr': 'fr_reader_MuUp(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_cut_Tight_HWWW, Lepton_isTightElectron_mvaFall17V2Iso_WP90, Lepton_mvaTTH_UL, Muon_mvaTTH, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
        'samples': ['Fake']
}

aliases['fakeWMuDown'] = {
    'linesToAdd' : ['#include "/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/fake_rate_reader_class.cc"'],
    'linesToProcess':["ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_MuDown = fake_rate_reader(\"2017\", \"90\", \"82\", 0.90, 0.82, \"MuDown\", 2, \"std\");')"],
    'expr': 'fr_reader_MuDown(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_cut_Tight_HWWW, Lepton_isTightElectron_mvaFall17V2Iso_WP90, Lepton_mvaTTH_UL, Muon_mvaTTH, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
        'samples': ['Fake']
}

aliases['fakeWStatEleUp'] = {
    'linesToAdd' : ['#include "/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/fake_rate_reader_class.cc"'],
    'linesToProcess':["ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_StatEleUp = fake_rate_reader(\"2017\", \"90\", \"82\", 0.90, 0.82, \"StatEleUp\", 2, \"std\");')"],
    'expr': 'fr_reader_StatEleUp(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_cut_Tight_HWWW, Lepton_isTightElectron_mvaFall17V2Iso_WP90, Lepton_mvaTTH_UL, Muon_mvaTTH, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
        'samples': ['Fake']
}
aliases['fakeWStatEleDown'] = {
    'linesToAdd' : ['#include "/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/fake_rate_reader_class.cc"'],
    'linesToProcess':["ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_StatEleDown = fake_rate_reader(\"2017\", \"90\", \"82\", 0.90, 0.82, \"StatEleDown\", 2, \"std\");')"],
    'expr': 'fr_reader_StatEleDown(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_cut_Tight_HWWW, Lepton_isTightElectron_mvaFall17V2Iso_WP90, Lepton_mvaTTH_UL, Muon_mvaTTH, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
        'samples': ['Fake']
}

aliases['fakeWStatMuUp'] = {
    'linesToAdd' : ['#include "/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/fake_rate_reader_class.cc"'],
    'linesToProcess':["ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_StatMuUp = fake_rate_reader(\"2017\", \"90\", \"82\", 0.90, 0.82, \"StatMuUp\", 2, \"std\");')"],
    'expr': 'fr_reader_StatMuUp(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_cut_Tight_HWWW, Lepton_isTightElectron_mvaFall17V2Iso_WP90, Lepton_mvaTTH_UL, Muon_mvaTTH, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
        'samples': ['Fake']
}

aliases['fakeWStatMuDown'] = {
    'linesToAdd' : ['#include "/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/fake_rate_reader_class.cc"'],
    'linesToProcess':["ROOT.gInterpreter.Declare('fake_rate_reader fr_reader_StatMuDown = fake_rate_reader(\"2017\", \"90\", \"82\", 0.90, 0.82, \"StatMuDown\", 2, \"std\");')"],
    'expr': 'fr_reader_StatMuDown(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_cut_Tight_HWWW, Lepton_isTightElectron_mvaFall17V2Iso_WP90, Lepton_mvaTTH_UL, Muon_mvaTTH, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
        'samples': ['Fake']
}

aliases['Top_pTrw'] = {
    'expr': '(topGenPt * antitopGenPt > 0.) * (TMath::Sqrt((0.103*TMath::Exp(-0.0118*topGenPt) - 0.000134*topGenPt + 0.973) * (0.103*TMath::Exp(-0.0118*antitopGenPt) - 0.000134*antitopGenPt + 0.973))) + (topGenPt * antitopGenPt <= 0.)',
    'samples': ['top']
}

aliases['CleanJet_VetoMap'] = {
    'linesToAdd': [".L /eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/Full2017_v9/jet_veto_2017.cc+"],
    'class' : 'Jet_Veto',
    'args': 'CleanJet_pt,CleanJet_eta,CleanJet_phi,Jet_neEmEF,Jet_chEmEF,CleanJet_jetIdx',
}

aliases['gstarLow'] = {
    'expr': 'Gen_ZGstar_mass > 0 && Gen_ZGstar_mass < 4',
    'samples': 'VgS'
}

aliases['gstarHigh'] = {
    'expr': 'Gen_ZGstar_mass < 0 || Gen_ZGstar_mass > 4',
    'samples': 'WZ'
}

#######

aliases['nCleanGenJet'] = {
    #'linesToAdd': ['/afs/cern.ch/work/s/sblancof/private/Run2Analysis/mkShapesRDF/examples/Full2017_v9/ngenjet.cc'],
    'linesToAdd': ['.L /eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/ngenjet.cc+'],
    'class': 'CountGenJet',
    'args': 'nLeptonGen, LeptonGen_isPrompt,\
        LeptonGen_pdgId, LeptonGen_pt, LeptonGen_eta, LeptonGen_phi, \
        LeptonGen_mass, nPhotonGen, PhotonGen_pt, PhotonGen_eta,PhotonGen_phi, \
        PhotonGen_mass, nGenJet, GenJet_pt, GenJet_eta, GenJet_phi',
    'samples': mc
}

##### DY Z pT reweighting
aliases['getGenZpt_OTF'] = {
    #'linesToAdd': ['/afs/cern.ch/work/s/sblancof/private/Run2Analysis/mkShapesRDF/examples/Full2017_v9/getGenZpt.cc'],
    'linesToAdd': ['.L /eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/getGenZpt.cc+'],
    'class': 'getGenZpt',
    'args': 'nGenPart, GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, GenPart_statusFlags, gen_ptll',
    'samples': ['DY']
}


#DYrew = {}
exec(open('DYrew30.py', "r").read())
#handle = open('./DYrew30.py','r')
#eval(handle)
#handle.close()

aliases['DY_NLO_pTllrw'] = {
    'expr': '('+DYrew['2017']['NLO'].replace('x', 'getGenZpt_OTF')+')*(nCleanGenJet == 0)+1.0*(nCleanGenJet > 0)',
    'samples': ['DY']
}
aliases['DY_LO_pTllrw'] = {
    'expr': '('+DYrew['2017']['LO'].replace('x', 'getGenZpt_OTF')+')*(nCleanGenJet == 0)+1.0*(nCleanGenJet > 0)',
    'samples': ['DY']
}

aliases['KFactor_ggWW_NLO'] = {
    'linesToProcess':[
        'ROOT.gSystem.Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/ggzz_kfactor_cc.so","", ROOT.kTRUE)',
        "ROOT.gInterpreter.Declare('ggzz_K_producer k_reader_GGZZ = ggzz_K_producer();')"
    ],
    'expr': f'k_reader_GGZZ(nLHEPart,LHEPart_pt,LHEPart_eta,LHEPart_phi,LHEPart_mass,LHEPart_pdgId,LHEPart_status)',
    'samples': ['ggWW','ggH_gWW_Int']
}
aliases['KFactor_ggWW'] = {
    'expr': 'KFactor_ggWW_NLO[0]',
    'samples': ['ggWW','ggH_gWW_Int']
}
aliases['KFactor_ggWW_Up'] = {
    'expr': 'KFactor_ggWW_NLO[1]',
    'samples': ['ggWW','ggH_gWW_Int']
}
aliases['KFactor_ggWW_Down'] = {
    'expr': 'KFactor_ggWW_NLO[2]',
    'samples': ['ggWW','ggH_gWW_Int']
}

# Jet bins
# using Alt$(CleanJet_pt[n], 0) instead of Sum$(CleanJet_pt >= 30) because jet pt ordering is not strictly followed in JES-varied samples

# No jet with pt > 30 GeV
aliases['zeroJet'] = {
    'expr': 'Alt(CleanJet_pt,0, 0) < 30.'
}

aliases['oneJet'] = {
    'expr': 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0'
}

aliases['multiJet'] = {
    'expr': 'Alt(CleanJet_pt,1, 0) > 30.'
}

####################################################################################
# b tagging WPs: https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL18
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
bAlgo = 'DeepFlavB' # ['DeepB','DeepFlavB']
bWP   = bWP_loose_deepFlavB
bSF   = 'deepjet' # ['deepcsv','deepjet']  ## deepflav is new b-tag SF


# b veto
aliases['bVeto'] = {
    'expr': 'Sum(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{}, CleanJet_jetIdx) > {}) == 0'.format(bAlgo, bWP)
}

# At least one b-tagged jet  
aliases['bReq'] = { 
    'expr': 'Sum(CleanJet_pt > 30. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{}, CleanJet_jetIdx) > {}) >= 1'.format(bAlgo, bWP)
}

year = '2017_UL' # allowed options are = ["2016postVFP_UL, 2016preVFP_UL", "2017_UL", "2018_UL"] 
btv_path =  '/afs/cern.ch/work/s/sblancof/private/Run2Analysis/sendEOSJobs/jsonpog-integration/POG/BTV/' + year
shifts = ['central', 'up_uncorrelated', 'down_uncorrelated', 'up_correlated', 'down_correlated']
shift_str = '{"' + '","'.join(shifts) + '"}'

for flavour in ['bc', 'light']:
    btagsf_tmp = 'btagSF_TMP_' + flavour
    aliases[btagsf_tmp] = {
        'linesToProcess':[
            f'ROOT.gSystem.Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/evaluate_btagSF{flavour}_cc.so","", ROOT.kTRUE)',
            f"ROOT.gInterpreter.Declare('btagSF{flavour} btag_SF{flavour} = btagSF{flavour}(\"/afs/cern.ch/work/s/sblancof/private/Run2Analysis/sendEOSJobs/Full2017_v9/BtagEff/bTagEff_2017_ttbar_DeepFlavB_loose.root\",\"{year}\");')"
        ],
        'expr': f'btag_SF{flavour}(CleanJet_pt, CleanJet_eta, CleanJet_jetIdx, nCleanJet, Jet_hadronFlavour, Jet_btagDeepFlavB, "L", {shift_str})',
        'samples' : mc,
    }
    for i in range(len(shifts)):
        btagsf = 'btagSF' + flavour
        if shifts[i] != 'central':
            btagsf += '_' + shifts[i]
        aliases[btagsf] = {
            'expr': f"{btagsf_tmp}[{i}]",
            'samples' : mc,
        }

'''
aliases['bVetoSF'] = {
    'expr': 'TMath::Exp(Sum(LogVec((CleanJet_pt>20 && abs(CleanJet_eta)<2.5)*Take(Jet_btagSF_{}_shape, CleanJet_jetIdx)+1*(CleanJet_pt<20 || abs(CleanJet_eta)>2.5))))'.format(bSF),
    'samples': mc_emb
}

aliases['bReqSF'] = {
    'expr': 'TMath::Exp(Sum(LogVec((CleanJet_pt>30 && abs(CleanJet_eta)<2.5)*Take(Jet_btagSF_{}_shape, CleanJet_jetIdx)+1*(CleanJet_pt<30 || abs(CleanJet_eta)>2.5))))'.format(bSF),
    'samples': mc_emb
}
'''

# Top control region                                                                                                                                                                                       
aliases['topcr'] = {
    'expr': 'mth>40 && PuppiMET_pt>20 && mll > 12 && ((zeroJet && !bVeto) || bReq) && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13'
}

aliases['dycr'] = {
    'expr': 'mth<40 && PuppiMET_pt>20 && mll>12 && bVeto && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13'
}

aliases['wwcr'] = {
    'expr': 'mth>40 && PuppiMET_pt>20 && bVeto && mll>12 && mpmet>20 && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13'
}

aliases['sr'] = {
    'expr': 'mth>40 && PuppiMET_pt>20 && bVeto && mll > 12 && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13'
}

'''
# Overall b tag SF
aliases['btagSF'] = {
    'expr': '(bVeto || (topcr && zeroJet))*bVetoSF + (topcr && !zeroJet)*bReqSF',
    #'expr': 'bVeto*bVetoSF + topcr*bReqSF',
    #    'expr': 'bVeto*bVetoSF',
    'samples': mc
}


for shift in ['jes','lf','hf','lfstats1','lfstats2','hfstats1','hfstats2','cferr1','cferr2']:

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
'''


####################################################################################
# End of b tagging pippone
####################################################################################


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

aliases['SFweight'] = {
    #'expr': ' * '.join(['SFweight2l', 'LepWPCut', 'LepWPSF','Jet_PUIDSF', 'btagSF', 'L1PreFiringWeight_Nom', 'LepWPttHMVASF']),
    'expr': ' * '.join(['SFweight2l', 'LepWPCut', 'LepWPSF','Jet_PUIDSF', 'btagSFbc', 'btagSFlight', 'L1PreFiringWeight_Nom', 'LepWPttHMVASF']),
    'samples': mc
}

# variations
aliases['SFweightEleUp'] = {
    'expr': 'LepSF2l__ele_'+eleWP+'__Up',
    'samples': mc_emb
}
aliases['SFweightEleDown'] = {
    'expr': 'LepSF2l__ele_'+eleWP+'__Do',
    'samples': mc_emb
}
aliases['SFweightMuUp'] = {
    'expr': 'LepSF2l__mu_'+muWP+'__Up',
    'samples': mc_emb
}
aliases['SFweightMuDown'] = {
    'expr': 'LepSF2l__mu_'+muWP+'__Do',
    'samples': mc_emb
}


samplesToAdd = ['ggH_hww', 'ggH_HWLWL', 'ggH_HWTWT', 'ggH_HWW_Int', 'ggH_HWW_TTInt','ggH_gWW_Int', 'ggH_gWW_Tot', 'ggH_perp']
for i in np.linspace(-1, 1, 21):
    jlim = round(1.0 - abs(i), 2)
    jn = 2 * 10*abs(jlim) + 2
    for j in np.linspace(-1*jlim, jlim, int(jn)-1):
        i = round(i, 1)
        j = round(j, 1)

        if i<0.0:
            itxt = str(i).replace("-", "m")
        else:
            itxt = str(i)
        itxt = itxt.replace(".", "p")

        if j<0.0:
            jtxt = str(j).replace("-", "m")
        else:
            jtxt = str(j)
        jtxt = jtxt.replace(".", "p")

        weighttxt = f"p_GEN_fL_{itxt}_fPerp_{jtxt}"
        txt = f"_fL_{itxt}_fPerp_{jtxt}"

        samplesToAdd.append('ggH'+txt)

aliases['Weight2MINLO'] = {
    'linesToAdd': ['.L /eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/weight2MINLO.cc+'],
    'class': 'Weight2MINLO',
    'args': '"NNLOPS_reweight.root", HTXS_njets30, HTXS_Higgs_pt',
    #'samples': ['ggH_hww', 'ggH_HWLWL', 'ggH_HWTWT', 'ggH_HWW_Int', 'ggH_HWW_TTInt','ggH_gWW_Int', 'ggH_gWW_Tot', 'ggH_perp']
    'samples': samplesToAdd
}


## GGHUncertaintyProducer wasn't run for GluGluHToWWTo2L2Nu_Powheg_M125 
thus = [
    'ggH_mu',
    'ggH_res',
    'ggH_mig01',
    'ggH_mig12',
    'ggH_VBF2j',
    'ggH_VBF3j',
    'ggH_pT60',
    'ggH_pT120',
    'ggH_qmtop'
]

for thu in thus:
    aliases[thu+'_2'] = {
        'linesToAdd': ['.L /eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/gghuncertainty.cc+'],
        'class': 'GGHUncertainty',
        'args': '"{}", HTXS_njets30, HTXS_Higgs_pt, HTXS_stage_1_pTjet30'.format(thu),
        'samples': ['ggH_hww', 'ggH_HWLWL', 'ggH_HWTWT', 'ggH_HWW_Int', 'ggH_HWW_TTInt', 'ggH_perp']
    }
    

"""
aliases['Higgs_WW_Rew'] = {
    'linesToAdd' : ['.L /eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/doHiggsPolarization.cc+'],
    'class' : 'DoHiggsPolarizationWeight',
    'args': 'GenPart_pt, GenPart_eta, GenPart_phi, GenPart_mass, GenPart_pdgId, GenPart_status, GenPart_genPartIdxMother',
    'samples' : ['ggH_HWLWL', 'ggH_HWTWT', 'ggH_HWW_Int', 'ggH_HWW_TTInt', 'qqH_HWLWL', 'qqH_HWTWT'],
}

aliases['Higgs_WW_LL'] = {
    'expr': 'Higgs_WW_Rew[0]',
    'samples': ['ggH_HWLWL', 'ggH_HWTWT', 'ggH_HWW_Int', 'ggH_HWW_TTInt', 'qqH_HWLWL', 'qqH_HWTWT'],
}

aliases['Higgs_WW_TT'] = {
    'expr': 'Higgs_WW_Rew[1]',
    'samples': ['ggH_HWLWL', 'ggH_HWTWT', 'ggH_HWW_Int', 'ggH_HWW_TTInt', 'qqH_HWLWL', 'qqH_HWTWT'],
}

aliases['Higgs_WW_Int'] = {
    'expr': 'Higgs_WW_Rew[2]',
    'samples': ['ggH_HWLWL', 'ggH_HWTWT', 'ggH_HWW_Int', 'ggH_HWW_TTInt', 'qqH_HWLWL', 'qqH_HWTWT'],
}

aliases['Higgs_WW_TTInt'] = {
    'expr': 'Higgs_WW_Rew[3]',
    'samples': ['ggH_HWLWL', 'ggH_HWTWT', 'ggH_HWW_Int', 'ggH_HWW_TTInt', 'qqH_HWLWL', 'qqH_HWTWT'],
}
"""

####
#### Interference qq/ggWW - qq/ggH
####

aliases['HWW_interference'] = {
    'linesToProcess':['ROOT.gSystem.Load("/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/JHUGenMELA/MELA/data/slc7_amd64_gcc920/libmcfm_705.so","", ROOT.kTRUE)',
                      'ROOT.gSystem.Load("/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/JHUGenMELA/MELA/data/slc7_amd64_gcc920/libJHUGenMELAMELA.so","", ROOT.kTRUE)',
                      'ROOT.gSystem.Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/IvyFramework/IvyDataTools/lib/libIvyFrameworkIvyDataTools.so","", ROOT.kTRUE)',
                      'ROOT.gSystem.Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/IvyFramework/IvyAutoMELA/lib/libIvyFrameworkIvyAutoMELA.so","", ROOT.kTRUE)',
                      'ROOT.gSystem.Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/MelaAnalytics/GenericMEComputer/lib/libMelaAnalyticsGenericMEComputer.so","", ROOT.kTRUE)',
                      'ROOT.gSystem.Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/MelaAnalytics/EventContainer/lib/libMelaAnalyticsEventContainer.so","", ROOT.kTRUE)',
                      'ROOT.gSystem.Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/MelaAnalytics/CandidateLOCaster/lib/libMelaAnalyticsCandidateLOCaster.so","", ROOT.kTRUE)',
                      'ROOT.gSystem.Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/doGenInterference_cc.so","", ROOT.kTRUE)',
                      'ROOT.gInterpreter.Declare("GEN_INTERFERENCE b;")'],
    'expr' :   'b(nLHEPart,LHEPart_pt,LHEPart_eta,LHEPart_phi,LHEPart_mass,LHEPart_incomingpz,LHEPart_pdgId,LHEPart_status,LHEPart_spin,GenPart_genPartIdxMother,GenPart_pdgId,GenPart_status,GenPart_pt,GenPart_eta,GenPart_phi,GenPart_mass,Generator_x1,Generator_x2,Generator_id1,Generator_id2)',
    'samples': ['ggH_gWW_Int', 'ggH_gWW_Tot','qqH_qqWW_Int', 'qqH_qqWW_Tot'],
}

aliases['ggHWW_Interference'] = {
    'expr': '(HWW_interference[1]-HWW_interference[0]-HWW_interference[2]) / (HWW_interference[0]+HWW_interference[2])',
    'samples': ['ggH_gWW_Int', 'ggH_gWW_Tot', 'ggH_Int', 'ggH_Tot', 'ggWW_Int', 'ggWW_Tot'],
}

aliases['ggHWW_Total'] = {
    'expr': 'HWW_interference[1] / (HWW_interference[0]+HWW_interference[2])',
    'samples': ['ggH_gWW_Int', 'ggH_gWW_Tot', 'ggH_Int', 'ggH_Tot', 'ggWW_Int', 'ggWW_Tot'],
}

aliases['qqHWW_Interference'] = {
    'expr': '(HWW_interference[3]+HWW_interference[5])!=0.0 ? (HWW_interference[4]-HWW_interference[3]-HWW_interference[5]) / (HWW_interference[3]+HWW_interference[5]) : 0.0',
    'samples': ['qqH_qqWW_Int', 'qqH_qqWW_Tot'],
}

aliases['qqHWW_Total'] = {
    'expr': '(HWW_interference[3]+HWW_interference[5])!=0.0 ? HWW_interference[4] / (HWW_interference[3]+HWW_interference[5]) : 1.0',
    'samples': ['qqH_qqWW_Int', 'qqH_qqWW_Tot'],
}


aliases['D_ME'] = {
    'linesToProcess':['ROOT.gSystem.Load("/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/JHUGenMELA/MELA/data/slc7_amd64_gcc920/libmcfm_705.so","", ROOT.kTRUE)',
                      'ROOT.gSystem.Load("/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/JHUGenMELA/MELA/data/slc7_amd64_gcc920/libJHUGenMELAMELA.so","", ROOT.kTRUE)',
                      'ROOT.gSystem.Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/RecoMELA_VBF_cc.so","", ROOT.kTRUE)',
                      'ROOT.gInterpreter.Declare("RECOMELA_VBF a;")'],
    'expr' :   'a(nCleanJet, nLepton, PuppiMET_pt, PuppiMET_phi, Lepton_pt, Lepton_phi, Lepton_eta, CleanJet_pt, CleanJet_phi, CleanJet_eta, Lepton_pdgId)',
    'afterNuis': True
}

aliases['D_VBF_QCD'] = {
    'expr': 'D_ME[0]',
    'afterNuis': True
}

aliases['D_VBF_VH'] = {
    'expr': 'D_ME[1]',
    'afterNuis': True
}

aliases['D_QCD_VH'] = {
    'expr': 'D_ME[2]',
    'afterNuis': True
}


aliases['D_VBF_DY'] = {
  'linesToProcess':['ROOT.gSystem.Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/lib/libmomemta.so","", ROOT.kTRUE);',
                    'ROOT.gSystem.Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/RecoMoMEMta_VBF_cc.so","", ROOT.kTRUE)',
                    'ROOT.gInterpreter.Declare("RecoMoMEMta_VBF EvMoMEMta;")'],
   'expr' :   'EvMoMEMta(nCleanJet, nLepton, PuppiMET_pt, PuppiMET_phi, Lepton_pt[0], Lepton_pt[1], Lepton_phi[0], Lepton_phi[1], Lepton_eta[0], Lepton_eta[1], CleanJet_pt[0], CleanJet_pt[1], CleanJet_phi[0], CleanJet_phi[1], CleanJet_eta[0], CleanJet_eta[1], Lepton_pdgId[0], Lepton_pdgId[1])',
    'afterNuis': True
}

aliases['Ctot'] = {
    'expr': 'detajj!=0 ? log((abs(2 * Lepton_eta[0] - CleanJet_eta[0] - CleanJet_eta[1]) + abs(2 * Lepton_eta[1] - CleanJet_eta[0] - CleanJet_eta[1])) / detajj) : -1.0',
    'afterNuis': True
}

aliases['btagDeepFlavB'] = {
    'expr': 'Alt(Jet_btagDeepFlavB, Alt(CleanJet_jetIdx, 0, -1), -2.0)',
    'afterNuis': True
}

aliases['btagDeepFlavB_1'] = {
    'expr': 'Alt(Jet_btagDeepFlavB, Alt(CleanJet_jetIdx, 1, -1), -2.0)',
    'afterNuis': True
}

aliases['RandomForest_evaluator'] = {
    'linesToProcess' : [
        'ROOT.gSystem.Load("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/evaluate_RF_polarization_cc.so","", ROOT.kTRUE)',
        """ROOT.gInterpreter.Declare('EvaluateRF rf_evaluator("2017");')"""
    ],
    'expr': 'rf_evaluator(mll,mth,mtw1,mtw2,mjj,mcollWW,ptll,Ctot,Lepton_pt,Lepton_eta,Lepton_phi,dphilmet1,dphilmet2,dphill,detall,dphijj,detajj,dphilep1jet1,dphilep2jet1,dphilep1jet2,dphilep2jet2,btagDeepFlavB,btagDeepFlavB_1,drll,mpmet,PuppiMET_pt,PuppiMET_phi,D_VBF_QCD,D_VBF_VH,D_QCD_VH,D_VBF_DY,mTi,zeroJet,oneJet,multiJet)',
    'afterNuis': True
}

#### 0 Jets
aliases['RF_score_0J_LL'] = {
    'expr': 'RandomForest_evaluator[0][0]',
    'afterNuis': True
}
aliases['RF_score_0J_TT'] = {
    'expr': 'RandomForest_evaluator[0][1]',
    'afterNuis': True
}
aliases['RF_score_0J_Bkg'] = {
    'expr': 'RandomForest_evaluator[0][2]',
    'afterNuis': True
}


#### 1 Jets
aliases['RF_score_1J_LL'] = {
    'expr': 'RandomForest_evaluator[1][0]',
    'afterNuis': True
}
aliases['RF_score_1J_TT'] = {
    'expr': 'RandomForest_evaluator[1][1]',
    'afterNuis': True
}
aliases['RF_score_1J_Bkg'] = {
    'expr': 'RandomForest_evaluator[1][2]',
    'afterNuis': True
}


#### 2 Jets
aliases['RF_score_2J_LL'] = {
    'expr': 'RandomForest_evaluator[2][0]',
    'afterNuis': True
}
aliases['RF_score_2J_TT'] = {
    'expr': 'RandomForest_evaluator[2][1]',
    'afterNuis': True
}
aliases['RF_score_2J_Bkg'] = {
    'expr': 'RandomForest_evaluator[2][2]',
    'afterNuis': True
}


#### VBF
aliases['RF_score_VBF_LL'] = {
    'expr': 'RandomForest_evaluator[3][0]',
    'afterNuis': True
}
aliases['RF_score_VBF_TT'] = {
    'expr': 'RandomForest_evaluator[3][1]',
    'afterNuis': True
}
aliases['RF_score_VBF_Bkg'] = {
    'expr': 'RandomForest_evaluator[3][2]',
    'afterNuis': True
}

