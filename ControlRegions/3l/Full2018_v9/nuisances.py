import sys
 
nuisances = {}

mcProduction = 'Summer20UL18_106x_nAODv9_Full2018v9'
dataReco     = 'Run2018_UL2018_nAODv9_Full2018v9'
mcSteps      = 'MCl1loose2018v9__MCCorr2018v9NoJERInHorn__l2tightOR2018v9'
fakeSteps    = 'DATAl1loose2018v9__l2loose__fakeW'
dataSteps    = 'DATAl1loose2018v9__l2loose__l2tightOR2018v9'

treeBaseDir  = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'
limitFiles   = -1

mc = [skey for skey in samples if skey not in ('Fake', 'DATA','ChargeFlip')]

redirector = ""

useXROOTD = False

def makeMCDirectory(var=''):
    if var== '':
        print(os.path.join(treeBaseDir, mcProduction, mcSteps))
        return os.path.join(treeBaseDir, mcProduction, mcSteps)
    else:
        print(os.path.join(treeBaseDir, mcProduction, mcSteps + '__' + var))
        return os.path.join(treeBaseDir, mcProduction, mcSteps + '__' + var)

mcDirectory = makeMCDirectory()
fakeDirectory = os.path.join(treeBaseDir, dataReco, fakeSteps)
dataDirectory = os.path.join(treeBaseDir, dataReco, dataSteps)

################################ EXPERIMENTAL UNCERTAINTIES  #################################

#### Luminosity

# https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun2#LumiComb
# Uncorrelated 2016               1.0
# Uncorrelated       2017              2.0
# Uncorrelated             2018             1.5
# Correlated   2016, 2017, 2018   0.6, 0.9, 2.0
# Correlated         2017, 2018        0.6, 0.2

nuisances['lumi_Uncorrelated'] = {
    'name'    : 'lumi_13TeV_2018',
    'type'    : 'lnN',
    'samples' : dict((skey, '1.015') for skey in mc if skey not in ['WZ'])
}

nuisances['lumi_Correlated_Run2'] = {
    'name'    : 'lumi_13TeV_correlated',
    'type'    : 'lnN',
    'samples' : dict((skey, '1.020') for skey in mc if skey not in ['WZ'])
}

nuisances['lumi_Correlated_2017_2018'] = {
    'name'    : 'lumi_13TeV_1718',
    'type'    : 'lnN',
    'samples' : dict((skey, '1.002') for skey in mc if skey not in ['WZ'])
}


### Fakes

# Per lepton
nuisances['fake_ele'] = {
    'name'    : 'CMS_WH_hww_fake_e_2018',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : {
        'Fake_ee' : ['fakeWEleUp', 'fakeWEleDown'],
        'Fake_em' : ['fakeWEleUp', 'fakeWEleDown'],
    }
}

nuisances['fake_ele_stat'] = {
    'name'    : 'CMS_WH_hww_fake_stat_e_2018',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : {
        'Fake_ee' : ['fakeWStatEleUp', 'fakeWStatEleDown'],
        'Fake_em' : ['fakeWStatEleUp', 'fakeWStatEleDown'],
    }
}


nuisances['fake_mu'] = {
    'name'    : 'CMS_WH_hww_fake_m_2018',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : {
        'Fake_mm' : ['fakeWMuUp', 'fakeWMuDown'],
        'Fake_em' : ['fakeWMuUp', 'fakeWMuDown'],
    }   
}       

nuisances['fake_mu_stat'] = {
    'name'    : 'CMS_WH_hww_fake_stat_m_2018',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : {
        'Fake_mm' : ['fakeWStatMuUp', 'fakeWStatMuDown'],
        'Fake_em' : ['fakeWStatMuUp', 'fakeWStatMuDown'],
    }
}


# # Normalization per final state
# jet_bins = ['0j','1j','2j']
# channels = ['ee', 'em', 'mm']
# charges  = ['plus', 'minus']

# eta_regimes = ['barrel', 'endcap']
# pt_regimes  = ['high', 'medium']

# fake_syst_dict = {
#     'endcap_medium_pt': ['1.0*(abs(Lepton_eta[1])<=1.479) + 1.0*(Lepton_pt[1]> 35) +     1.1*(abs(Lepton_eta[1])> 1.479 && Lepton_pt[1]<=35)',
#                          '1.0*(abs(Lepton_eta[1])<=1.479) + 1.0*(Lepton_pt[1]> 35) + 1.0/1.1*(abs(Lepton_eta[1])> 1.479 && Lepton_pt[1]<=35)'],
#     'barrel_medium_pt': ['1.0*(abs(Lepton_eta[1])> 1.479) + 1.0*(Lepton_pt[1]> 35) +     1.1*(abs(Lepton_eta[1])<=1.479 && Lepton_pt[1]<=35)',
#                          '1.0*(abs(Lepton_eta[1])> 1.479) + 1.0*(Lepton_pt[1]> 35) + 1.0/1.1*(abs(Lepton_eta[1])<=1.479 && Lepton_pt[1]<=35)'],
#     'endcap_high_pt'  : ['1.0*(abs(Lepton_eta[1])<=1.479) + 1.0*(Lepton_pt[1]<=35) +     1.1*(abs(Lepton_eta[1])> 1.479 && Lepton_pt[1]> 35)',
#                          '1.0*(abs(Lepton_eta[1])<=1.479) + 1.0*(Lepton_pt[1]<=35) + 1.0/1.1*(abs(Lepton_eta[1])> 1.479 && Lepton_pt[1]> 35)'],
#     'barrel_high_pt'  : ['1.0*(abs(Lepton_eta[1])> 1.479) + 1.0*(Lepton_pt[1]<=35) +     1.1*(abs(Lepton_eta[1])<=1.479 && Lepton_pt[1]> 35)',
#                          '1.0*(abs(Lepton_eta[1])> 1.479) + 1.0*(Lepton_pt[1]<=35) + 1.0/1.1*(abs(Lepton_eta[1])<=1.479 && Lepton_pt[1]> 35)'],   
# }

# for jet_bin in jet_bins:
#     for channel in channels:
#         for charge in charges:

#             nuisances[f'CMS_WH_hww_fake_syst_{jet_bin}_{channel}_{charge}']  = {
#                 'name'    : f'CMS_WH_hww_fake_syst_{jet_bin}_{channel}_{charge}_2018',
#                 'samples' : {
#                     f'Fake_{channel}' : '1.30',
#                 },
#                 'type'    : 'lnN',
#                 'cuts'    : [
#                     f'hww2l2v_13TeV_WH_SS_{channel}_{jet_bin}_SS_CR_{charge}_pt2ge20',
#                 ],
#             }

#             # for eta_regime in eta_regimes:
#             #     for pt_regime in pt_regimes:
#             #         nuisances[f'CMS_WH_hww_fake_syst_{eta_regime}_{pt_regime}_{channel}']  = {
#             #             'name'    : f'CMS_WH_hww_fake_syst_{eta_regime}_{pt_regime}_{channel}_2018',
#             #             'samples' : {
#             #                 f'Fake_{channel}' : f'{eta_regime}_{pt_regime}_pt',
#             #             },
#             #             'type'    : 'shape',
#             #             'cuts'    : [cut for cut in cuts if (f'_{channel}_' in cut)],
#             #         }
            

# flavors  = ['sssf', 'ossf']

# for flavor in flavors:
#     for charge in charges:
        
#         nuisances[f'CMS_WH_hww_fake_syst_{flavor}_{charge}']  = {
#             'name'    : f'CMS_WH_hww_fake_syst_{flavor}_{charge}_2018',
#             'samples' : {
#                 'Fake' : '1.30',
#             },
#             'type'    : 'lnN',
#             'cuts'    : [
#                 f'hww2l2v_13TeV_WH_3l_{flavor}_{charge}_pt2ge20',
#             ],
#         }
        
#         # for eta_regime in eta_regimes:
#         #     for pt_regime in pt_regimes:
#         #         nuisances[f'CMS_WH_hww_fake_syst_{eta_regime}_{pt_regime}_{flavor}']  = {
#         #             'name'    : f'CMS_WH_hww_fake_syst_{eta_regime}_{pt_regime}_{flavor}_2018',
#         #             'samples' : {
#         #                 f'Fake' : f'{eta_regime}_{pt_regime}_pt',
#         #             },
#         #             'type'    : 'shape',
#         #             'cuts'    : [cut for cut in cuts if (f'_{flavor}_' in cut)],
#         #         }


# ###### B-tagger

# for shift in ['lf', 'hf', 'hfstats1', 'hfstats2', 'lfstats1', 'lfstats2', 'cferr1', 'cferr2']:
#     btag_syst = ['(btagSF%sup)/(btagSF)' % shift, '(btagSF%sdown)/(btagSF)' % shift]

#     name = 'CMS_btag_%s' % shift
#     if 'stats' in shift:
#         name += '_2018'

#     nuisances['btag_shape_%s' % shift] = {
#         'name'    : name,
#         'kind'    : 'weight',
#         'type'    : 'shape',
#         'samples' : dict((skey, btag_syst) for skey in mc),
#     }

# ##### Trigger Scale Factors

# trig_syst = ['TriggerSFWeight_2l_u/TriggerSFWeight_2l', 'TriggerSFWeight_2l_d/TriggerSFWeight_2l']

# nuisances['trigg'] = {
#     'name'    : 'CMS_eff_hwwtrigger_2018',
#     'kind'    : 'weight',
#     'type'    : 'shape',
#     'samples' : dict((skey, trig_syst) for skey in mc)
# }

# ##### Electron Efficiency and energy scale

# nuisances['eff_e'] = {
#     'name'    : 'CMS_eff_e_2018',
#     'kind'    : 'weight',
#     'type'    : 'shape',
#     'samples' : dict((skey, ['SFweightEleUp', 'SFweightEleDown']) for skey in mc)
# }

# nuisances['eff_ttHMVA_e'] = {
#     'name'    : 'CMS_eff_ttHMVA_e_2018',
#     'kind'    : 'weight',
#     'type'    : 'shape',
#     'samples' : dict((skey, ['LepWPttHMVASFEleUp', 'LepWPttHMVASFEleDown']) for skey in mc)
# }

# nuisances['electronpt'] = {
#     'name'       : 'CMS_scale_e_2018',
#     'kind'       : 'suffix',
#     'type'       : 'shape',
#     'mapUp'      : 'ElepTup',
#     'mapDown'    : 'ElepTdo',
#     'samples'    : dict((skey, ['1', '1']) for skey in mc),
#     'folderUp'   : makeMCDirectory('ElepTup_suffix'),
#     'folderDown' : makeMCDirectory('ElepTdo_suffix'),
#     'AsLnN'      : '0'
# }

# ##### Muon Efficiency and energy scale

# nuisances['eff_m'] = {
#     'name'    : 'CMS_eff_m_2018',
#     'kind'    : 'weight',
#     'type'    : 'shape',
#     'samples' : dict((skey, ['SFweightMuUp', 'SFweightMuDown']) for skey in mc)
# }

# nuisances['eff_ttHMVA_m'] = {
#     'name'    : 'CMS_eff_ttHMVA_m_2018',
#     'kind'    : 'weight',
#     'type'    : 'shape',
#     'samples' : dict((skey, ['LepWPttHMVASFMuUp', 'LepWPttHMVASFMuDown']) for skey in mc)
# }

# nuisances['muonpt'] = {
#     'name'       : 'CMS_scale_m_2018',
#     'kind'       : 'suffix',
#     'type'       : 'shape',
#     'mapUp'      : 'MupTup',
#     'mapDown'    : 'MupTdo',
#     'samples'    : dict((skey, ['1', '1']) for skey in mc),
#     'folderUp'   : makeMCDirectory('MupTup_suffix'),
#     'folderDown' : makeMCDirectory('MupTdo_suffix'),
#     'AsLnN'      : '0'
# }

# ##### Jet energy scale
# jes_systs    = ['JESAbsolute','JESAbsolute_2018','JESBBEC1','JESBBEC1_2018','JESEC2','JESEC2_2018','JESFlavorQCD','JESHF','JESHF_2018','JESRelativeBal','JESRelativeSample_2018']

# for js in jes_systs:

#   nuisances[js] = {
#       'name'      : 'CMS_scale_' + js.replace("JES","j_"),
#       'kind'      : 'suffix',
#       'type'      : 'shape',
#       'mapUp'     : js + 'up',
#       'mapDown'   : js + 'do',
#       'samples'   : dict((skey, ['1', '1']) for skey in mc),
#       'folderUp'  : makeMCDirectory('RDF__JESup_suffix'),
#       'folderDown': makeMCDirectory('RDF__JESdo_suffix'),
#       'reweight'  : ['btagSF'+js.replace('JES','jes')+'up/btagSF','btagSF'+js.replace('JES','jes')+'down/btagSF'],
#       'AsLnN'     : '0'
#   }

# ##### Jet energy resolution
# nuisances['JER'] = {
#     'name'      : 'CMS_res_j_2018',
#     'kind'      : 'suffix',
#     'type'      : 'shape',
#     'mapUp'     : 'JERup',
#     'mapDown'   : 'JERdo',
#     'samples'   : dict((skey, ['1', '1']) for skey in mc),
#     'folderUp'  : makeMCDirectory('JERup_suffix'),
#     'folderDown': makeMCDirectory('JERdo_suffix'),
#     'AsLnN'     : '0'
# }

# ##### MET unclustered energy

# # metUp.PuppiMET_pt_METup
# nuisances['met'] = {
#     'name'      : 'CMS_scale_met_2018',
#     'kind'      : 'suffix',
#     'type'      : 'shape',
#     'mapUp'     : 'METup',
#     'mapDown'   : 'METdo',
#     'samples'   : dict((skey, ['1', '1']) for skey in mc),
#     'folderUp'  : makeMCDirectory('METup_suffix'),
#     'folderDown': makeMCDirectory('METdo_suffix'),
#     'AsLnN'     : '0'
# }


# ##### Pileup

# # puWeight_UL2018
# nuisances['PU'] = {
#     'name'    : 'CMS_pileup_2018',
#     'kind'    : 'weight',
#     'type'    : 'shape',
#     'samples' : {
#         'DY'      : ['0.998687*(puWeightUp/puWeight)', '1.001976*(puWeightDown/puWeight)'],
#         'top'     : ['1.002595*(puWeightUp/puWeight)', '0.997470*(puWeightDown/puWeight)'],
#         'WW'      : ['1.004449*(puWeightUp/puWeight)', '0.995660*(puWeightDown/puWeight)'],
#         'WWewk'   : ['1.002122*(puWeightUp/puWeight)', '0.998087*(puWeightDown/puWeight)'],
#         'ggWW'    : ['1.004870*(puWeightUp/puWeight)', '0.995315*(puWeightDown/puWeight)'],
#         'WZ'      : ['0.999330*(puWeightUp/puWeight)', '1.000992*(puWeightDown/puWeight)'],
#         'ZZ'      : ['0.999469*(puWeightUp/puWeight)', '1.000751*(puWeightDown/puWeight)'],
#         'VVV'     : ['1.003485*(puWeightUp/puWeight)', '0.997561*(puWeightDown/puWeight)'],
#         'ggH_hww' : ['1.003677*(puWeightUp/puWeight)', '0.995996*(puWeightDown/puWeight)'],
#         'qqH_hww' : ['1.003747*(puWeightUp/puWeight)', '0.995878*(puWeightDown/puWeight)'],
#     },
#     'AsLnN'   : '0',
# }

# ### PU ID SF uncertainty

# # puid_syst = ['Jet_PUIDSF_loose_up/Jet_PUIDSF_loose', 'Jet_PUIDSF_loose_down/Jet_PUIDSF_loose']
# puid_syst = ['Jet_PUIDSF_up/Jet_PUIDSF', 'Jet_PUIDSF_down/Jet_PUIDSF']

# nuisances['jetPUID'] = {
#     'name'    : 'CMS_eff_j_PUJET_id_2018',
#     'kind'    : 'weight',
#     'type'    : 'shape',
#     'samples' : dict((skey, puid_syst) for skey in mc)
# }

# ### PS and UE

# nuisances['PS_ISR']  = {
#     'name'    : 'PS_WH_hww_ISR',
#     'kind'    : 'weight',
#     'type'    : 'shape',
#     'samples' : dict((skey, ['PSWeight[2]', 'PSWeight[0]']) for skey in mc),
#     'AsLnN'   : '0',
# }

# nuisances['PS_FSR']  = {
#     'name'    : 'PS_WH_hww_FSR',
#     'kind'    : 'weight',
#     'type'    : 'shape',
#     'samples' : dict((skey, ['PSWeight[3]', 'PSWeight[1]']) for skey in mc),
#     'AsLnN'   : '0',
# }

# nuisances['UE_CP5']  = {
#     'name'    : 'CMS_WH_hww_UE',
#     'skipCMS' : 1,
#     'type'    : 'lnN',
#     'samples' : dict((skey, '1.015') for skey in mc),
# }

# # Charge flip efficiency
# nuisances['chargeFlipEff'] = {
#     'name'    : 'CMS_whss_chargeFlipEff_2018',
#     'kind'    : 'weight',
#     'type'    : 'shape',
#     'samples' : dict((skey, ['1-ttHMVA_eff_err_flip_2l', '1+ttHMVA_eff_err_flip_2l']) for skey in ['DY','ChargeFlip']),
#     'cuts'    : [cut for cut in cuts if ('_ee_' in cut or '_em_' in cut)],
# }

# # Charge flip: uncertainty on opposite sign processes not affected by charge-flip
# nuisances['chargeFlip_syst'] = {
#     'name'    : 'CMS_ChargeFlip_syst',
#     'type'    : 'lnN',
#     'samples' : {
#         'ChargeFlip' : '1.10',
#     },
#     'cuts'    : [cut for cut in cuts if ('_ee_' in cut or '_em_' in cut)],
# }

# ## Top pT reweighting uncertainty

# nuisances['TopPtRew'] = {
#     'name'       : 'CMS_top_pT_reweighting',   # Theory uncertainty
#     'kind'       : 'weight',
#     'type'       : 'shape',
#     'samples'    : {
#         'top': ["1.", "1./Top_pTrw"]
#     },
#     'symmetrize' : True
# }

# nuisances['VgStar'] = {
#     'name'    : 'CMS_hww_VgStarScale',
#     'type'    : 'lnN',
#     'samples' : {
#         'VgS' : '1.25'
#     }
# }

# nuisances['Vg'] = {
#     'name'    : 'CMS_hww_VgScale',
#     'type'    : 'lnN',
#     'samples' : {
#         'Vg' : '1.25'
#     }
# }

# ###### pdf uncertainties

# valuesggh  = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ggH', '125.09','pdf','sm')
# valuesggzh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ggZH','125.09','pdf','sm')
# valuesbbh  = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','bbH', '125.09','pdf','sm')

# nuisances['pdf_Higgs_gg'] = {
#     'name'    : 'pdf_Higgs_gg',
#     'samples' : {
#         'ggH_hww'  : valuesggh,
#         'ggH_htt'  : valuesggh,
#         'ggZH_hww' : valuesggzh,
#         'bbH_hww'  : valuesbbh,
#     },
#     'type'    : 'lnN',
# }

# # For ttH, we need to use 1./values
# values = str(1./float(HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ttH','125.09','pdf','sm')))

# nuisances['pdf_Higgs_ttH'] = {
#     'name'    : 'pdf_Higgs_ttH',
#     'samples' : {
#         'ttH_hww': values,
#     },
#     'type'    : 'lnN',
# }

# valuesqqh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','vbfH','125.09','pdf','sm')
# valueswh  = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','WH',  '125.09','pdf','sm')
# valueszh  = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ZH',  '125.09','pdf','sm')

# nuisances['pdf_Higgs_qqbar'] = {
#     'name'   : 'pdf_Higgs_qqbar',
#     'type'   : 'lnN',
#     'samples': {
#         'qqH_hww'     : valuesqqh,
#         'qqH_htt'     : valuesqqh,
#         'WH_hww_plus' : valueswh,
#         'WH_hww_minus': valueswh,
#         'WH_htt_plus' : valueswh,
#         'WH_htt_minus': valueswh,
#         'ZH_hww'      : valueszh,
#         'ZH_htt'      : valueszh
#     },
# }

# nuisances['pdf_qqbar'] = {
#     'name'    : 'pdf_qqbar',
#     'type'    : 'lnN',
#     'samples' : {
#         'Vg'  : '1.04',
#         'ZZ'  : '1.04', # PDF: 0.0064 / 0.1427 = 0.0448493
#         # 'WZ'  : '1.04', # PDF: 0.0064 / 0.1427 = 0.0448493
#         'VgS' : '1.04', # PDF: 0.0064 / 0.1427 = 0.0448493
#     },
# }

# nuisances['pdf_gg'] = {
#     'name': 'pdf_WH_hww_gg',
#     'type': 'lnN',
#     'samples': {
#         'ggWW' : '1.05',
#     },
# }

# nuisances['pdf_Higgs_gg_ACCEPT'] = {
#     'name'    : 'pdf_WH_hww_Higgs_gg_ACCEPT',
#     'samples' : {
#         'ggH_hww'  : '1.006',
#         'ggH_htt'  : '1.006',
#         'ggZH_hww' : '1.006',
#         'bbH_hww'  : '1.006'
#     },
#     'type'    : 'lnN',
# }
# nuisances['pdf_gg_ACCEPT'] = {
#     'name'    : 'pdf_WH_hww_gg_ACCEPT',
#     'samples' : {
#         'ggWW' : '1.006',
#     },
#     'type'    : 'lnN',
# }

# nuisances['pdf_Higgs_qqbar_ACCEPT'] = {
#     'name'    : 'pdf_WH_hww_Higgs_qqbar_ACCEPT',
#     'type'    : 'lnN',
#     'samples' : {
#         'qqH_hww'     : '1.002',
#         'qqH_htt'     : '1.002',
#         'WH_hww_plus' : '1.003',
#         'WH_hww_minus': '1.003',
#         'WH_htt_plus' : '1.003',
#         'WH_htt_minus': '1.003',
#         'ZH_hww'      : '1.002',
#         'ZH_htt'      : '1.002',
#     },
# }

# nuisances['pdf_qqbar_ACCEPT'] = {
#     'name'    : 'pdf_WH_hww_qqbar_ACCEPT',
#     'type'    : 'lnN',
#     'samples' : {
#         'ZZ' : '1.001',
#         # 'WZ' : '1.001',
#     },
# }

# ##### Renormalization & factorization scales

# ## Shape nuisance due to QCD scale variations for DY
# ## LHE scale variation weights (w_var / w_nominal)

# ## This should work for samples with either 8 or 9 LHE scale weights (Length$(LHEScaleWeight) == 8 or 9)
# variations = ['Alt(LHEScaleWeight,0,1)', 'Alt(LHEScaleWeight,1,1)', 'Alt(LHEScaleWeight,3,1)', 'Alt(LHEScaleWeight,nLHEScaleWeight-4,1)', 'Alt(LHEScaleWeight,nLHEScaleWeight-2,1)', 'Alt(LHEScaleWeight,nLHEScaleWeight-1,1)']

# # nuisances['QCDscale_V'] = {
# #     'name'    : 'QCDscale_V',
# #     'skipCMS' : 1,
# #     'kind'    : 'weight_envelope',
# #     'type'    : 'shape',
# #     'samples' : {
# #         'DY' : variations
# #     },
# #     'AsLnN'   : '0'
# # }

# nuisances['QCDscale_VV'] = {
#     'name' : 'QCDscale_VV',
#     'kind' : 'weight_envelope',
#     'type' : 'shape',
#     'samples' : {
#         'WW'  : variations,
#         'Vg'  : variations,
#         'ZZ'  : variations,
#         'WZ'  : variations,
#         'VgS' : variations,
#     }
# }

# nuisances['QCDscale_ggVV'] = {
#     'name'    : 'QCDscale_ggVV',
#     'type'    : 'lnN',
#     'samples' : {
#         'ggWW' : '1.15',
#     },
# }

# #### QCD scale uncertainties for Higgs signals other than ggH

# values = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','vbfH','125.09','scale','sm')

# nuisances['QCDscale_qqH'] = {
#     'name'    : 'QCDscale_qqH',
#     'samples' : {
#         'qqH_hww' : values,
#         'qqH_htt' : values,
#     },
#     'type'    : 'lnN'
# }

# valueswh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','WH','125.09','scale','sm')
# valueszh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ZH','125.09','scale','sm')

# nuisances['QCDscale_VH'] = {
#     'name'    : 'QCDscale_VH',
#     'samples' : {
#         'WH_hww_plus'  : valueswh,
#         'WH_hww_minus' : valueswh,
#         'WH_htt_plus'  : valueswh,
#         'WH_htt_minus' : valueswh,
#         'ZH_hww'       : valueszh,
#         'ZH_htt'       : valueszh,
#     },
#     'type'    : 'lnN',
# }

# values = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ggZH','125.09','scale','sm')

# nuisances['QCDscale_ggZH'] = {
#     'name' : 'QCDscale_ggZH',
#     'samples' : {
#         'ggZH_hww' : values,
#     },
#     'type' : 'lnN',
# }

# values = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ttH','125.09','scale','sm')

# nuisances['QCDscale_ttH'] = {
#     'name' : 'QCDscale_ttH',
#     'samples' : {
#         'ttH_hww' : values,
#     },
#     'type' : 'lnN',
# }

# nuisances['QCDscale_WWewk'] = {
#     'name' : 'QCDscale_WWewk',
#     'samples' : {
#         'WWewk' : '1.11',
#     },
#     'type' : 'lnN'
# }

# nuisances['QCDscale_qqbar_ACCEPT'] = {
#     'name' : 'QCDscale_qqbar_ACCEPT',
#     'type' : 'lnN',
#     'samples' : {
#         'qqH_hww'      : '1.003',
#         'qqH_htt'      : '1.003',
#         'WH_hww_plus'  : '1.010',
#         'WH_hww_minus' : '1.010',
#         'WH_htt_plus'  : '1.010',
#         'WH_htt_minus' : '1.010',
#         'ZH_hww'       : '1.015',
#         'ZH_htt'       : '1.015',
#     }
# }

# # FIXME: these come from HIG-16-042, maybe should be recomputed?
# nuisances['QCDscale_gg_ACCEPT'] = {
#     'name' : 'QCDscale_gg_ACCEPT',
#     'samples' : {
#         'ggH_htt'  : '1.012',
#         'ggH_hww'  : '1.012',
#         'ggZH_hww' : '1.012',
#         'ggWW'     : '1.012',
#     },
#     'type' : 'lnN',
# }

# # WZ normalization from control region
# nuisances['WZ2jnorm']  = {
#     'name'    : 'CMS_hww_WZ3l2jnorm',
#     'samples' : {
#         'WZ' : '1.00',
#     },
#     'type' : 'rateParam',
#     'cuts' : [cut for cut in cuts if '2j' in cut],
# }

# nuisances['WZ1jnorm']  = {
#     'name'    : 'CMS_hww_WZ3l1jnorm',
#     'samples' : {
#         'WZ' : '1.00',
#     },
#     'type' : 'rateParam',
#     'cuts' : [cut for cut in cuts if '1j' in cut],
# }

# # WZ migration from W+Z to W-Z
# nuisances['WZ2j_charge_migration']  = {
#     'name'    : 'CMS_hww_WZ2jchargemigration',
#     'samples' : {
#         'WZ' : '1.02',
#     },
#     'type' : 'lnN',
#     'cuts' : [
#         'hww2l2v_13TeV_WH_SS_noZveto_mm_2j_plus_pt2ge20',
#         'hww2l2v_13TeV_WH_SS_noZveto_mm_2j_plus_pt2lt20',
#         'hww2l2v_13TeV_WH_SS_em_2j_plus_pt2ge20',
#         'hww2l2v_13TeV_WH_SS_em_2j_plus_pt2lt20',
#         'hww2l2v_13TeV_WH_SS_ee_2j_plus_pt2ge20',
#         'hww2l2v_13TeV_WH_SS_ee_2j_plus_pt2lt20',
#     ],
# }

# nuisances['WZ1j_charge_migration']  = {
#     'name'    : 'CMS_hww_WZ1jchargemigration',
#     'samples' : {
#         'WZ' : '1.02',
#     },
#     'type' : 'lnN',
#     'cuts' : [
#         'hww2l2v_13TeV_WH_SS_noZveto_mm_1j_plus_pt2ge20',
#         'hww2l2v_13TeV_WH_SS_noZveto_mm_1j_plus_pt2lt20',
#         'hww2l2v_13TeV_WH_SS_em_1j_plus_pt2ge20',
#         'hww2l2v_13TeV_WH_SS_em_1j_plus_pt2lt20',
#         'hww2l2v_13TeV_WH_SS_ee_1j_plus_pt2ge20',
#         'hww2l2v_13TeV_WH_SS_ee_1j_plus_pt2lt20',
#     ],
# }

# # Nonprompt leptons normalization per category
# nuisances['CMS_WH_hww_fake_syst_2jee_plus']  = {
#     'name'    : 'CMS_WH_hww_fake_syst_2jee_plus_2018',
#     'samples' : {
#         'Fake_ee' : '1.50',
#     },
#     'type' : 'lnN',
#     'cuts' : [
#         'hww2l2v_13TeV_WH_SS_ee_2j_plus_pt2ge20',
#     ],
# }
# nuisances['CMS_WH_hww_fake_syst_2jee_plus_lowpt']  = {
#     'name'    : 'CMS_WH_hww_fake_syst_2jee_plus_lowpt_2018',
#     'samples' : {
#         'Fake_ee' : '1.50',
#     },
#     'type' : 'lnN',
#     'cuts' : [
#         'hww2l2v_13TeV_WH_SS_ee_2j_plus_pt2lt20',
#     ],
# }

# nuisances['CMS_WH_hww_fake_syst_2jem_plus']  = {
#     'name'    : 'CMS_WH_hww_fake_syst_2jem_plus_2018',
#     'samples' : {
#         'Fake_em' : '1.50',
#     },
#     'type' : 'lnN',
#     'cuts' : [
#         'hww2l2v_13TeV_WH_SS_em_2j_plus_pt2ge20',
#     ],
# }
# nuisances['CMS_WH_hww_fake_syst_2jem_plus_lowpt']  = {
#     'name'    : 'CMS_WH_hww_fake_syst_2jem_plus_lowpt_2018',
#     'samples' : {
#         'Fake_em' : '1.50',
#     },
#     'type' : 'lnN',
#     'cuts' : [
#         'hww2l2v_13TeV_WH_SS_em_2j_plus_pt2lt20',
#     ],
# }

# nuisances['CMS_WH_hww_fake_syst_2jmm_plus']  = {
#     'name'    : 'CMS_WH_hww_fake_syst_2jmm_plus_2018',
#     'samples' : {
#         'Fake_mm' : '1.50',
#     },
#     'type' : 'lnN',
#     'cuts' : [
#         'hww2l2v_13TeV_WH_SS_noZeto_mm_2j_plus_pt2ge20',
#     ],
# }
# nuisances['CMS_WH_hww_fake_syst_2jmm_plus_lowpt']  = {
#     'name'    : 'CMS_WH_hww_fake_syst_2jmm_plus_lowpt_2018',
#     'samples' : {
#         'Fake_mm' : '1.50',
#     },
#     'type' : 'lnN',
#     'cuts' : [
#         'hww2l2v_13TeV_WH_SS_noZeto_mm_2j_plus_pt2lt20',
#     ],
# }

# nuisances['CMS_WH_hww_fake_syst_1jee_plus']  = {
#     'name'    : 'CMS_WH_hww_fake_syst_1jee_plus_2018',
#     'samples' : {
#         'Fake_ee' : '1.50',
#     },
#     'type' : 'lnN',
#     'cuts' : [
#         'hww2l2v_13TeV_WH_SS_ee_1j_plus_pt2ge20',
#     ],
# }
# nuisances['CMS_WH_hww_fake_syst_1jee_plus_lowpt']  = {
#     'name'    : 'CMS_WH_hww_fake_syst_1jee_plus_lowpt_2018',
#     'samples' : {
#         'Fake_ee' : '1.50',
#     },
#     'type' : 'lnN',
#     'cuts' : [
#         'hww2l2v_13TeV_WH_SS_ee_1j_plus_pt2lt20',
#     ],
# }

# nuisances['CMS_WH_hww_fake_syst_1jem_plus']  = {
#     'name'    : 'CMS_WH_hww_fake_syst_1jem_plus_2018',
#     'samples' : {
#         'Fake_em' : '1.50',
#     },
#     'type' : 'lnN',
#     'cuts' : [
#         'hww2l2v_13TeV_WH_SS_em_1j_plus_pt2ge20',
#     ],
# }
# nuisances['CMS_WH_hww_fake_syst_1jem_plus_lowpt']  = {
#     'name'    : 'CMS_WH_hww_fake_syst_1jem_plus_lowpt_2018',
#     'samples' : {
#         'Fake_em' : '1.50',
#     },
#     'type' : 'lnN',
#     'cuts' : [
#         'hww2l2v_13TeV_WH_SS_em_1j_plus_pt2lt20',
#     ],
# }

# nuisances['CMS_WH_hww_fake_syst_1jmm_plus']  = {
#     'name'    : 'CMS_WH_hww_fake_syst_1jmm_plus_2018',
#     'samples' : {
#         'Fake_mm' : '1.50',
#     },
#     'type' : 'lnN',
#     'cuts' : [
#         'hww2l2v_13TeV_WH_SS_noZeto_mm_1j_plus_pt2ge20',
#     ],
# }
# nuisances['CMS_WH_hww_fake_syst_1jmm_plus_lowpt']  = {
#     'name'    : 'CMS_WH_hww_fake_syst_1jmm_plus_lowpt_2018',
#     'samples' : {
#         'Fake_mm' : '1.50',
#     },
#     'type' : 'lnN',
#     'cuts' : [
#         'hww2l2v_13TeV_WH_SS_noZeto_mm_1j_plus_pt2lt20',
#     ],
# }


# nuisances['CMS_WH_hww_fake_syst_2jee_minus']  = {
#     'name'    : 'CMS_WH_hww_fake_syst_2jee_minus_2018',
#     'samples' : {
#         'Fake_ee' : '1.50',
#     },
#     'type' : 'lnN',
#     'cuts' : [
#         'hww2l2v_13TeV_WH_SS_ee_2j_minus_pt2ge20',
#     ],
# }
# nuisances['CMS_WH_hww_fake_syst_2jee_minus_lowpt']  = {
#     'name'    : 'CMS_WH_hww_fake_syst_2jee_minus_lowpt_2018',
#     'samples' : {
#         'Fake_ee' : '1.50',
#     },
#     'type' : 'lnN',
#     'cuts' : [
#         'hww2l2v_13TeV_WH_SS_ee_2j_minus_pt2lt20',
#     ],
# }

# nuisances['CMS_WH_hww_fake_syst_2jem_minus']  = {
#     'name'    : 'CMS_WH_hww_fake_syst_2jem_minus_2018',
#     'samples' : {
#         'Fake_em' : '1.50',
#     },
#     'type' : 'lnN',
#     'cuts' : [
#         'hww2l2v_13TeV_WH_SS_em_2j_minus_pt2ge20',
#     ],
# }
# nuisances['CMS_WH_hww_fake_syst_2jem_minus_lowpt']  = {
#     'name'    : 'CMS_WH_hww_fake_syst_2jem_minus_lowpt_2018',
#     'samples' : {
#         'Fake_em' : '1.50',
#     },
#     'type' : 'lnN',
#     'cuts' : [
#         'hww2l2v_13TeV_WH_SS_em_2j_minus_pt2lt20',
#     ],
# }

# nuisances['CMS_WH_hww_fake_syst_2jmm_minus']  = {
#     'name'    : 'CMS_WH_hww_fake_syst_2jmm_minus_2018',
#     'samples' : {
#         'Fake_mm' : '1.50',
#     },
#     'type' : 'lnN',
#     'cuts' : [
#         'hww2l2v_13TeV_WH_SS_noZeto_mm_2j_minus_pt2ge20',
#     ],
# }
# nuisances['CMS_WH_hww_fake_syst_2jmm_minus_lowpt']  = {
#     'name'    : 'CMS_WH_hww_fake_syst_2jmm_minus_lowpt_2018',
#     'samples' : {
#         'Fake_mm' : '1.50',
#     },
#     'type' : 'lnN',
#     'cuts' : [
#         'hww2l2v_13TeV_WH_SS_noZeto_mm_2j_minus_pt2lt20',
#     ],
# }

# nuisances['CMS_WH_hww_fake_syst_1jee_minus']  = {
#     'name'    : 'CMS_WH_hww_fake_syst_1jee_minus_2018',
#     'samples' : {
#         'Fake_ee' : '1.50',
#     },
#     'type' : 'lnN',
#     'cuts' : [
#         'hww2l2v_13TeV_WH_SS_ee_1j_minus_pt2ge20',
#     ],
# }
# nuisances['CMS_WH_hww_fake_syst_1jee_minus_lowpt']  = {
#     'name'    : 'CMS_WH_hww_fake_syst_1jee_minus_lowpt_2018',
#     'samples' : {
#         'Fake_ee' : '1.50',
#     },
#     'type' : 'lnN',
#     'cuts' : [
#         'hww2l2v_13TeV_WH_SS_ee_1j_minus_pt2lt20',
#     ],
# }

# nuisances['CMS_WH_hww_fake_syst_1jem_minus']  = {
#     'name'    : 'CMS_WH_hww_fake_syst_1jem_minus_2018',
#     'samples' : {
#         'Fake_em' : '1.50',
#     },
#     'type' : 'lnN',
#     'cuts' : [
#         'hww2l2v_13TeV_WH_SS_em_1j_minus_pt2ge20',
#     ],
# }
# nuisances['CMS_WH_hww_fake_syst_1jem_minus_lowpt']  = {
#     'name'    : 'CMS_WH_hww_fake_syst_1jem_minus_lowpt_2018',
#     'samples' : {
#         'Fake_em' : '1.50',
#     },
#     'type' : 'lnN',
#     'cuts' : [
#         'hww2l2v_13TeV_WH_SS_em_1j_minus_pt2lt20',
#     ],
# }

# nuisances['CMS_WH_hww_fake_syst_1jmm_minus']  = {
#     'name'    : 'CMS_WH_hww_fake_syst_1jmm_minus_2018',
#     'samples' : {
#         'Fake_mm' : '1.50',
#     },
#     'type' : 'lnN',
#     'cuts' : [
#         'hww2l2v_13TeV_WH_SS_noZeto_mm_1j_minus_pt2ge20',
#     ],
# }
# nuisances['CMS_WH_hww_fake_syst_1jmm_minus_lowpt']  = {
#     'name'    : 'CMS_WH_hww_fake_syst_1jmm_minus_lowpt_2018',
#     'samples' : {
#         'Fake_mm' : '1.50',
#     },
#     'type' : 'lnN',
#     'cuts' : [
#         'hww2l2v_13TeV_WH_SS_noZeto_mm_1j_minus_pt2lt20',
#     ],
# }

# End of Nonprompt leptons normalization per category

## Use the following if you want to apply the automatic combine MC stat nuisances.
nuisances['stat']  = {
    'type'          : 'auto',
    'maxPoiss'      : '10',
    'includeSignal' : '0',
    'samples'       : {}
}
#  nuisance ['maxPoiss'] =  Number of threshold events for Poisson modelling
#  nuisance ['includeSignal'] =  Include MC stat nuisances on signal processes (1=True, 0=False)

for n in nuisances.values():
    n['skipCMS'] = 1
