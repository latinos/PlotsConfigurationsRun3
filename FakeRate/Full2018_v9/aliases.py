import os
import copy
import inspect

# /afs/cern.ch/user/n/ntrevisa/work/latinos/Run3/PlotsConfigurationsRun3/FakeRate/Full2018_v9

configurations = os.path.realpath(inspect.getfile(inspect.currentframe())) # this file
configurations = os.path.dirname(configurations) # Full2018_v9
configurations = os.path.dirname(configurations) # FakeRate

aliases = {}
aliases = OrderedDict()

mc = [skey for skey in samples if skey not in ('Fake', 'DATA')]


# Evaluate BDT discriminant
aliases['Lepton_mvaTTH_UL'] = {
    'linesToAdd'     : [f'#include "{configurations}/macros/ttH_MVA_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('ttH_MVA_reader ttHMVA = ttH_MVA_reader(\"BDTG\",\"{configurations}/data/UL20_el_TTH-like_2018_BDTG.weights.xml\",\"BDTG\",\"{configurations}/data/UL20_mu_TTH-like_2018_BDTG.weights.xml\");')"],
    'expr'           : 'ttHMVA(nLepton,Lepton_pdgId,Lepton_electronIdx,Electron_jetIdx,event,Electron_mvaTTH,Electron_mvaFall17V2noIso_WPL,Electron_lostHits,Electron_pt,Electron_eta,Electron_pfRelIso03_all,Electron_miniPFRelIso_chg,Electron_miniPFRelIso_all,Electron_jetNDauCharged,Electron_jetPtRelv2,Electron_jetRelIso,Jet_btagDeepFlavB,Electron_sip3d,Electron_dxy,Electron_dz,Electron_mvaFall17V2noIso,Lepton_muonIdx,Muon_jetIdx,Muon_mvaTTH,Muon_looseId,Muon_isGlobal,Muon_isTracker,Muon_isPFcand,Muon_mediumId,Muon_pt,Muon_eta,Muon_pfRelIso03_all,Muon_miniPFRelIso_chg,Muon_miniPFRelIso_all,Muon_jetNDauCharged,Muon_jetPtRelv2,Muon_jetRelIso,Muon_sip3d,Muon_dxy,Muon_dz,Muon_segmentComp)',
    'samples': ['DATA','DATA_unprescaled'],
}

# LepCut2l__ele_mvaFall17V2Iso_WP90__mu_cut_Tight_HWWW
eleWP = 'mvaFall17V2Iso_WP90'
muWP  = 'cut_Tight_HWWW'

aliases['LepWPCut2l'] = {
    # 'expr': 'LepCut2l__ele_' + eleWP + '__mu_' + muWP,
    'expr': 'LepCut2l__ele_mvaFall17V2Iso_WP90__mu_cut_Tight_HWWW*\
     ( ((abs(Lepton_pdgId[0])==13 && Muon_mvaTTH[Lepton_muonIdx[0]]>0.82) || (abs(Lepton_pdgId[0])==11 && Lepton_mvaTTH_UL[0]>0.90)) \
    && ((abs(Lepton_pdgId[1])==13 && Muon_mvaTTH[Lepton_muonIdx[1]]>0.82) || (abs(Lepton_pdgId[1])==11 && Lepton_mvaTTH_UL[1]>0.90)) )',
    'samples': mc + ['DATA','DATA_unprescaled']
}

aliases['LepWPCut1l'] = {
    'expr': '(abs(Lepton_pdgId[0])==11 && Lepton_isTightElectron_'+eleWP+'[0]>0.5 && Lepton_mvaTTH_UL[0]>0.90) \
          || (abs(Lepton_pdgId[0])==13 && Lepton_isTightMuon_'+muWP+'[0]>0.5 && Muon_mvaTTH[Lepton_muonIdx[0]]>0.82)',
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


# # Lepton SF (not considering the ttHMVA discriminant)
# aliases['LepWPSF'] = {
#     'expr': 'LepSF2l__ele_'+eleWP+'__mu_'+muWP,
#     'samples': mc
# }



# ####################################################################################
# # b tagging WPs: https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL18
# ####################################################################################

# # DeepB = DeepCSV
# bWP_loose_deepB  = '0.1208'
# bWP_medium_deepB = '0.4168' 
# bWP_tight_deepB  = '0.7665'

# # DeepFlavB = DeepJet
# bWP_loose_deepFlavB  = '0.0490'
# bWP_medium_deepFlavB = '0.2783'
# bWP_tight_deepFlavB  = '0.7100'

# # Actual algo and WP definition. BE CONSISTENT!!
# bAlgo = 'DeepB'          # ['DeepB',        'DeepFlavB'         ]
# bWP   = bWP_medium_deepB # [bWP_loose_deepB, bWP_loose_deepFlavB]
# bSF   = 'deepcsv'        # ['deepcsv',      'deepjet'           ]

# # b veto
# aliases['bVeto'] = {
#     'expr': 'Sum(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{}, CleanJet_jetIdx) > {}) == 0'.format(bAlgo, bWP)
# }

# aliases['bVetoSF'] = {
#     'expr': 'TMath::Exp(Sum(LogVec((CleanJet_pt>20 && abs(CleanJet_eta)<2.5)*Take(Jet_btagSF_{}_shape, CleanJet_jetIdx)+1*(CleanJet_pt<20 || abs(CleanJet_eta)>2.5))))'.format(bSF),
#     'samples': mc
# }

# # At least one b-tagged jet
# aliases['bReq'] = {
#     'expr': 'Sum(CleanJet_pt > 30. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{}, CleanJet_jetIdx) > {}) >= 1'.format(bAlgo, bWP)
# }

# aliases['bReqSF'] = {
#     'expr': 'TMath::Exp(Sum(LogVec((CleanJet_pt>30 && abs(CleanJet_eta)<2.5)*Take(Jet_btagSF_{}_shape, CleanJet_jetIdx)+1*(CleanJet_pt<30 || abs(CleanJet_eta)>2.5))))'.format(bSF),
#     'samples': mc
# }

# # Top control region
# aliases['topcr'] = {
#     'expr': 'mtw2>30 && mll>50 && ((zeroJet && !bVeto) || bReq)'
# }

# # WW control region
# aliases['wwcr'] = {
#     'expr': 'mth>60 && mtw2>30 && mll>100 && bVeto'
# }

# # Overall b tag SF
# aliases['btagSF'] = {
#     'expr': '(bVeto || (topcr && zeroJet))*bVetoSF + (topcr && !zeroJet)*bReqSF',
#     'samples': mc
# }

# for shift in ['jesAbsolute', 'jesAbsolute_2018', 'jesBBEC1', 'jesBBEC1_2018', 'jesEC2',
#         'jesEC2_2018', 'jesFlavorQCD', 'jesHF', 'jesHF_2018', 'jesRelativeBal',
#         'jesRelativeSample_2018']:
#     for var in ['up','down']:
#         aliases[f'Jet_btagSF_{bSF}_shape_{shift.replace("jes","JES")}{var[:2]}'] = {
#                 'expr' : f'Jet_btagSF_{bSF}_shape_{var}_{shift}',
#                 'samples' : mc
#         }

# for shift in ['jesAbsolute', 'jesAbsolute_2018', 'jesBBEC1', 'jesBBEC1_2018', 'jesEC2',
#               'jesEC2_2018', 'jesFlavorQCD', 'jesHF', 'jesHF_2018', 'jesRelativeBal',
#               'jesRelativeSample_2018', 'lf', 'hf', 'lfstats1', 'lfstats2',
#               'hfstats1', 'hfstats2', 'cferr1', 'cferr2']:
    
#     for targ in ['bVeto', 'bReq']:
#         alias = aliases['%sSF%sup' % (targ, shift)] = copy.deepcopy(aliases['%sSF' % targ])
#         alias['expr'] = alias['expr'].replace('btagSF_{}_shape'.format(bSF), 'btagSF_{}_shape_up_{}'.format(bSF, shift))

#         alias = aliases['%sSF%sdown' % (targ, shift)] = copy.deepcopy(aliases['%sSF' % targ])
#         alias['expr'] = alias['expr'].replace('btagSF_{}_shape'.format(bSF), 'btagSF_{}_shape_down_{}'.format(bSF, shift))

#     aliases['btagSF%sup' % shift] = {
#         'expr': aliases['btagSF']['expr'].replace('SF', 'SF' + shift + 'up'),
#         'samples': mc
#     }

#     aliases['btagSF%sdown' % shift] = {
#         'expr': aliases['btagSF']['expr'].replace('SF', 'SF' + shift + 'down'),
#         'samples': mc
#     }

# ####################################################################################
# # End of b tagging pippone
# ####################################################################################

# # Need to redefine PUID scale factors, so that they are double and not vectors
# aliases['Jet_PUIDSF'] = {
#   'expr' : 'TMath::Exp(Sum((Jet_jetId>=2)*LogVec(Jet_PUIDSF_loose)))',
#   'samples': mc
# }

# aliases['Jet_PUIDSF_up'] = {
#   'expr' : 'TMath::Exp(Sum((Jet_jetId>=2)*LogVec(Jet_PUIDSF_loose_up)))',
#   'samples': mc
# }

# aliases['Jet_PUIDSF_down'] = {
#   'expr' : 'TMath::Exp(Sum((Jet_jetId>=2)*LogVec(Jet_PUIDSF_loose_down)))',
#   'samples': mc
# }


# aliases['gstarLow'] = {
#     'expr': 'Gen_ZGstar_mass > 0 && Gen_ZGstar_mass < 4',
#     'samples': 'VgS'
# }

# aliases['gstarHigh'] = {
#     'expr': 'Gen_ZGstar_mass < 0 || Gen_ZGstar_mass > 4',
#     'samples': 'WZ'
# }

# # gen-matching to prompt only (GenLepMatch2l matches to *any* gen lepton)
# aliases['PromptGenLepMatch2l'] = {
#     'expr': 'Alt(Lepton_promptgenmatched, 0, 0) * Alt(Lepton_promptgenmatched, 1, 0)',
#     'samples': mc
# }

# # # PostProcessing did not create (anti)topGenPt for ST samples with _ext1
# # lastcopy = (1 << 13)

# aliases['Top_pTrw'] = {
#     'expr': '(topGenPt * antitopGenPt > 0.) * (TMath::Sqrt(TMath::Exp(0.0615 - 0.0005 * topGenPt) * TMath::Exp(0.0615 - 0.0005 * antitopGenPt))) + (topGenPt * antitopGenPt <= 0.)',
#     'samples': ['top']
# }

# # # data/MC scale factors
# # aliases['SFweight'] = {
# #     'expr': ' * '.join(['SFweight2l', 'LepWPCut', 'LepWPSF', 'btagSF']),
# #     'samples': mc,
# # }

# # variations
# aliases['SFweightEleUp'] = {
#     'expr': 'LepSF2l__ele_'+eleWP+'__Up',
#     'samples': mc
# }
# aliases['SFweightEleDown'] = {
#     'expr': 'LepSF2l__ele_'+eleWP+'__Do',
#     'samples': mc
# }

# aliases['SFweightMuUp'] = {
#     'expr': 'LepSF2l__mu_'+muWP+'__Up',
#     'samples': mc
# }
# aliases['SFweightMuDown'] = {
#     'expr': 'LepSF2l__mu_'+muWP+'__Do',
#     'samples': mc
# }

# # TriggerSFWeight_2l:TriggerSFWeight_2l_u:TriggerSFWeight_2l_d
# aliases['SFtriggUp'] = {
#     'expr': 'TriggerSFWeight_2l_u/TriggerSFWeight_2l',
#     'samples': mc
# }
# aliases['SFtriggDown'] = {
#     'expr': 'TriggerSFWeight_2l_d/TriggerSFWeight_2l',
#     'samples': mc
# }

# # Veto events in the problematic region: 
# # electrons or jets in:
# # (-1.57 < phi < -0.87) , (-2.5 < eta < -1.3)
# aliases['hole_veto'] = {
#     'expr': '( ( (Lepton_eta[0] < -1.3  && Lepton_eta[0] > -2.5 ) && (Lepton_phi[0] > -1.57 && Lepton_phi[0] < -0.87) && (abs(Lepton_pdgId[0])==11) ) \
#             || ( (Lepton_eta[1] < -1.3  && Lepton_eta[1] > -2.5 ) && (Lepton_phi[1] > -1.57 && Lepton_phi[1] < -0.87) && (abs(Lepton_pdgId[1])==11) ) \
#             || ( (Alt(CleanJet_eta, 0, 99) < -1.3 && (Alt(CleanJet_eta, 0, -99) > -2.5))  && (Alt(CleanJet_phi, 0, -99) > -1.57 && Alt(CleanJet_phi, 0, 99) < -0.87) ) \
#             || ( (Alt(CleanJet_eta, 1, 99) < -1.3 && (Alt(CleanJet_eta, 1, -99) > -2.5))  && (Alt(CleanJet_phi, 1, -99) > -1.57 && Alt(CleanJet_phi, 1, 99) < -0.87) ) \
#     ) ',
# }
