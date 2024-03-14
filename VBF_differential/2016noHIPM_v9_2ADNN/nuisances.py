mcProduction = 'Summer20UL16_106x_nAODv9_noHIPM_Full2016v9'
dataReco = 'Run2016_UL2016_nAODv9_noHIPM_Full2016v9'
mcSteps = 'MCl1loose2016v9__MCCorr2016v9NoJERInHorn__l2tightOR2016v9'
fakeSteps = 'DATAl1loose2016v9__l2loose__fakeW'
dataSteps = 'DATAl1loose2016v9__l2loose__l2tightOR2016v9'

treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'
#limitFiles = -1

import HiggsXSection
HiggsXS = HiggsXSection.HiggsXSection()

def makeMCDirectory(var=''):
    if var== '':
        return os.path.join(treeBaseDir, mcProduction, mcSteps)
    else:
        return os.path.join(treeBaseDir, mcProduction, mcSteps + '__' + var)


# merge cuts
_mergedCuts = []
for cut in list(cuts.keys()):
    __cutExpr = ''
    if type(cuts[cut]) == dict:
        __cutExpr = cuts[cut]['expr']
        for cat in list(cuts[cut]['categories'].keys()):
            _mergedCuts.append(cut + '_' + cat)
    elif type(cuts[cut]) == str:
        _mergedCuts.append(cut)

cuts2j = _mergedCuts
#cuts2j_em = list(filter(lambda k: k.endswith('ee'), cuts2j))
#cuts2j_mm = list(filter(lambda k: k.endswith('mm'), cuts2j))



cuts_DeltaPhi_0 = []
cuts_DeltaPhi_1 = []
cuts_DeltaPhi_2 = []
cuts_DeltaPhi_3 = []


for k in cuts:
  if 'inclusive' in k: continue
  for cat in cuts[k]['categories']:
    if '0' in cat: cuts_DeltaPhi_0.append(k+'_'+cat)
    elif '1' in cat: cuts_DeltaPhi_1.append(k+'_'+cat)
    elif '2' in cat: cuts_DeltaPhi_2.append(k+'_'+cat)
    elif '3' in cat: cuts_DeltaPhi_3.append(k+'_'+cat)
    else: print ('WARNING: name of category does not contain either DeltaPhi_0,1,2,3')


nuisances = {}

################################ EXPERIMENTAL UNCERTAINTIES  #################################

#### Luminosity


nuisances['lumi_Uncorrelated'] = {
    'name': 'lumi_13TeV_2016',
    'type': 'lnN',
    'samples': dict((skey, '1.010') for skey in mc if skey not in ['WW', 'top',  'dytt'])
}

nuisances['lumi_correlated'] = {
    'name': 'lumi_13TeV_correlated',
    'type': 'lnN',
    'samples': dict((skey, '1.006') for skey in mc if skey not in ['WW', 'top',  'dytt'])
}

#### FAKES

nuisances['fake_syst_e'] = {
    'name': 'CMS_fake_syst_e',
    'type': 'lnN',
    'samples': {
        'Fake_e': '1.3'
    },
    #'cutspost': lambda self, cuts: [cut for cut in cuts if 'mm' not in cut],
}

nuisances['fake_syst_m'] = {
    'name': 'CMS_fake_syst_m',
    'type': 'lnN',
    'samples': {
        'Fake_m': '1.3'
    },
    #'cutspost': lambda self, cuts: [cut for cut in cuts if 'ee' not in cut],
}

nuisances['fake_ele'] = {
    'name': 'CMS_fake_e_2016',
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake': ['fakeWEleUp', 'fakeWEleDown'],
    }
}

nuisances['fake_ele_stat'] = {
    'name': 'CMS_fake_stat_e_2016',
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake': ['fakeWStatEleUp', 'fakeWStatEleDown']
    }
}

nuisances['fake_mu'] = {
    'name': 'CMS_fake_m_2016',
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake': ['fakeWMuUp', 'fakeWMuDown'],
    }
}

nuisances['fake_mu_stat'] = {
    'name': 'CMS_fake_stat_m_2016',
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake': ['fakeWStatMuUp', 'fakeWStatMuDown'],
    }
}



### B-tagger
for shift in ['jes', 'lf', 'hf', 'hfstats1', 'hfstats2', 'lfstats1', 'lfstats2', 'cferr1', 'cferr2']:
    btag_syst = ['(btagSF%sup)/(btagSF)' % shift, '(btagSF%sdown)/(btagSF)' % shift]

    name = 'CMS_btag_%s' % shift
    if 'stats' in shift:
        name += '_2016'

    nuisances['btag_shape_%s' % shift] = {
        'name': name,
        'kind': 'weight',
        'type': 'shape',
        'samples': dict((skey, btag_syst) for skey in mc),
    }

##### Trigger Efficiency

trig_syst = ['TriggerSFWeight_2l_u/TriggerSFWeight_2l', 'TriggerSFWeight_2l_d/TriggerSFWeight_2l']

nuisances['trigg'] = {
    'name': 'CMS_eff_hwwtrigger_2016',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, trig_syst) for skey in mc)
}


##### Electron Efficiency and energy scale

nuisances['eff_e'] = {
    'name': 'CMS_eff_e_2016',
    'kind': 'weight',
    'type': 'shape',
    #'samples': dict((skey, ['SFweightEleUp', 'SFweightEleDown']) for skey in mc_emb)
    'samples': dict((skey, ['SFweightEleUp', 'SFweightEleDown']) for skey in mc)
}

nuisances['electronpt'] = {
    'name': 'CMS_scale_e_2016',
    'kind': 'suffix',
    'type': 'shape',
    'mapUp': 'ElepTup',
    'mapDown': 'ElepTdo',
    'samples': dict((skey, ['1', '1']) for skey in mc),
    'folderUp': makeMCDirectory('ElepTup_suffix'),
    'folderDown': makeMCDirectory('ElepTdo_suffix'),
    'AsLnN': '1'
}

##### Muon Efficiency and energy scale

nuisances['eff_m'] = {
    'name': 'CMS_eff_m_2016',
    'kind': 'weight',
    'type': 'shape',
    # 'samples': dict((skey, ['ttHMVA_2l_mu_SF_Up', 'ttHMVA_2l_mu_SF_Down']) for skey in mc_emb)
    #'samples': dict((skey, ['SFweightMuUp', 'SFweightMuDown']) for skey in mc_emb)
    'samples': dict((skey, ['SFweightMuUp', 'SFweightMuDown']) for skey in mc)
}

nuisances['muonpt'] = {
    'name': 'CMS_scale_m_2016',
    'kind': 'suffix',
    'type': 'shape',
    'mapUp': 'MupTup',
    'mapDown': 'MupTdo',
    'samples': dict((skey, ['1', '1']) for skey in mc),
    'folderUp': makeMCDirectory('MupTup_suffix'),
    'folderDown': makeMCDirectory('MupTdo_suffix'),
    'AsLnN': '1'
}


# ### Pile-up uncertainty
# nuisances['pileup']  = {
#     'name'  : 'pileup', 
#     'kind'  : 'weight',
#     'type'  : 'shape',
#     'samples'  : {
#         'DY' : ['puWeightUp/puWeight', 'puWeightDown/puWeight']
#     }
# }


### PU ID SF uncertainty
puid_syst = ['Jet_PUIDSF_up/Jet_PUIDSF', 'Jet_PUIDSF_down/Jet_PUIDSF']

nuisances['jetPUID'] = {
    'name': 'CMS_PUID_2016',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, puid_syst) for skey in mc)
}



# ##### Jet energy scale

# jes_systs = ['JESAbsolute','JESAbsolute_2016','JESBBEC1','JESBBEC1_2016','JESEC2','JESEC2_2016','JESFlavorQCD','JESHF','JESHF_2016','JESRelativeBal','JESRelativeSample_2016']
# folderup = ""
# folderdo = ""

# for js in jes_systs:
#   if 'Absolute' in js:
#     folderup = makeMCDirectory('JESAbsoluteup_suffix')
#     folderdo = makeMCDirectory('JESAbsolutedo_suffix')
#   elif 'BBEC1' in js:
#     folderup = makeMCDirectory('JESBBEC1up_suffix')
#     folderdo = makeMCDirectory('JESBBEC1do_suffix')
#   elif 'EC2' in js:
#     folderup = makeMCDirectory('JESEC2up_suffix')
#     folderdo = makeMCDirectory('JESEC2do_suffix')
#   elif 'HF' in js:
#     folderup = makeMCDirectory('JESHFup_suffix')
#     folderdo = makeMCDirectory('JESHFdo_suffix')
#   elif 'Relative' in js:
#     folderup = makeMCDirectory('JESRelativeup_suffix')
#     folderdo = makeMCDirectory('JESRelativedo_suffix')
#   elif 'FlavorQCD' in js:
#     folderup = makeMCDirectory('JESFlavorQCDup_suffix')
#     folderdo = makeMCDirectory('JESFlavorQCDdo_suffix')

#   nuisances[js] = {
#       'name': 'CMS_scale_'+js,
#       'kind': 'suffix',
#       'type': 'shape',
#       'mapUp': js+'up',
#       'mapDown': js+'do',
#       'samples': dict((skey, ['1', '1']) for skey in mc),
#       'folderUp': folderup,
#       'folderDown': folderdo,
#       'AsLnN': '1'
#   }

# ##### Jet energy resolution
# nuisances['JER'] = {
#     'name'      : 'CMS_res_j_2018',
#     'kind'      : 'suffix',
#     'type'      : 'shape',
#     'mapUp'     : 'JERup',
#     'mapDown'   : 'JERdo',
#     'samples'   : dict((skey, ['1', '1']) for skey in mc if skey not in ['ggH_hww']),
#     'folderUp'  : makeMCDirectory('JERup_suffix'),
#     'folderDown': makeMCDirectory('JERdo_suffix'),
#     'AsLnN': '1'
# }


##### MET energy scale

nuisances['met'] = {
    'name': 'CMS_scale_met_2016',
    'kind': 'suffix',
    'type': 'shape',
    'mapUp': 'METup',
    'mapDown': 'METdo',
    'samples': dict((skey, ['1', '1']) for skey in mc),
    'folderUp': makeMCDirectory('METup_suffix'),
    'folderDown': makeMCDirectory('METdo_suffix'),
    'AsLnN': '1'
}

##### Pileup

##### PS

## An overall 1.5% UE uncertainty will cover all the UEup/UEdo variations
## And we don't observe any dependency of UE variations on njet
#nuisances['UE']  = {
#                'name'  : 'UE_CUET',
#                'skipCMS' : 1,
#                'type': 'lnN',
#                'samples': dict((skey, '1.015') for skey in mc if not skey in ['WW','top']),
#}



###### pdf uncertainties

valuesggh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ggH','125.09','pdf','sm')
valuesggzh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ggZH','125.09','pdf','sm')
valuesbbh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','bbH','125.09','pdf','sm')

nuisances['pdf_Higgs_gg'] = {
    'name': 'pdf_Higgs_gg',
    'samples': {
        'ggH_hww': valuesggh,
        'ggH_htt': valuesggh,
        'ggZH_hww': valuesggzh,
        'bbH_hww': valuesbbh
    },
    'type': 'lnN',
}

values = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ttH','125.09','pdf','sm')

nuisances['pdf_Higgs_ttH'] = {
    'name': 'pdf_Higgs_ttH',
    'samples': {
        'ttH_hww': values
    },
    'type': 'lnN',
}

valuesqqh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','vbfH','125.09','pdf','sm')
valueswh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','WH','125.09','pdf','sm')
valueszh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ZH','125.09','pdf','sm')

nuisances['pdf_Higgs_qqbar'] = {
    'name': 'pdf_Higgs_qqbar',
    'type': 'lnN',
    'samples': {
        'qqH_hww': valuesqqh,
        'qqH_htt': valuesqqh,
        'WH_hww': valueswh,
        'WH_htt': valueswh,
        'ZH_hww': valueszh,
        'ZH_htt': valueszh,
    },
}

#FIXME: check this 4%
nuisances['pdf_qqbar'] = {
    'name': 'pdf_qqbar',
    'type': 'lnN',
    'samples': {
        'Vg': '1.04',
        'VZ': '1.04',  # PDF: 0.0064 / 0.1427 = 0.0448493
        'VgS': '1.04', # PDF: 0.0064 / 0.1427 = 0.0448493
    },
}

nuisances['pdf_Higgs_gg_ACCEPT'] = {
    'name': 'pdf_Higgs_gg_ACCEPT',
    'samples': {
        'ggH_hww': '1.006',
        'ggH_htt': '1.006',
        'ggZH_hww': '1.006',
        'bbH_hww': '1.006'
    },
    'type': 'lnN',
}

nuisances['pdf_gg_ACCEPT'] = {
    'name': 'pdf_gg_ACCEPT',
    'samples': {
        'ggWW': '1.006',
    },
    'type': 'lnN',
}

nuisances['pdf_Higgs_qqbar_ACCEPT'] = {
    'name': 'pdf_Higgs_qqbar_ACCEPT',
    'samples': {
        'qqH_hww': '1.002',
        'qqH_htt': '1.002',
        'WH_hww': '1.003',
        'WH_htt': '1.003',
        'ZH_hww': '1.002',
        'ZH_htt': '1.002',
    },
    'type': 'lnN',
}

nuisances['pdf_qqbar_ACCEPT'] = {
    'name': 'pdf_qqbar_ACCEPT',
    'type': 'lnN',
    'samples': {
        'VZ': '1.001',
    },
}


###### Generic "cross section uncertainties"

apply_on = {
    'top': [
        '(topGenPt * antitopGenPt <= 0.) * 1.0816 + (topGenPt * antitopGenPt > 0.)',
        '(topGenPt * antitopGenPt <= 0.) * 0.9184 + (topGenPt * antitopGenPt > 0.)'
    ]
}

nuisances['singleTopToTTbar'] = {
    'name': 'singleTopToTTbar',
    'skipCMS': 1,
    'kind': 'weight',
    'type': 'shape',
    'samples': apply_on
}

## Top pT reweighting uncertainty

# nuisances['TopPtRew'] = {
#     'name': 'CMS_topPtRew',   # Theory uncertainty
#     'kind': 'weight',
#     'type': 'shape',
#     'samples': {'top': ["Top_pTrw*Top_pTrw", "1."]},
#     'symmetrize': True
# }

nuisances['VgStar'] = {
    'name': 'CMS_hww_VgStarScale',
    'type': 'lnN',
    'samples': {
        'VgS_L': '1.25'
    }
}

nuisances['VZ'] = {
    'name': 'CMS_hww_VZScale',
    'type': 'lnN',
    'samples': {
        'VgS_H': '1.16'
    }
}


# Uncertainty on SR/CR ratio
nuisances['CRSR_accept_DY'] = {
    'name': 'CMS_hww_CRSR_accept_DY',
    'type': 'lnN',
    'samples': {'dytt': '1.02'},
    'cuts': [cut for cut in cuts2j if 'dytt' in cut],
    #'cutspost': (lambda self, cuts: [cut for cut in cuts if 'DY' in cut]),
}

# Uncertainty on SR/CR ratio
nuisances['CRSR_accept_top'] = {
    'name': 'CMS_hww_CRSR_accept_top',
    'type': 'lnN',
    'samples': {'top': '1.01'},
    'cuts': [cut for cut in cuts2j if 'top' in cut],
    #'cutspost': (lambda self, cuts: [cut for cut in cuts if 'top' in cut]),
}

#### QCD scale uncertainties for Higgs signals other than ggH

values = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','vbfH','125.09','scale','sm')

nuisances['QCDscale_qqH'] = {
    'name': 'QCDscale_qqH', 
    'samples': {
        'qqH_hww': values,
        'qqH_htt': values,
    },
    'type': 'lnN',
}

valueswh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','WH','125.09','scale','sm')
valueszh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ZH','125.09','scale','sm')

nuisances['QCDscale_VH'] = {
    'name': 'QCDscale_VH', 
    'samples': {
        'WH_hww': valueswh,
        'WH_htt': valueswh,
        'ZH_hww': valueszh,
        'ZH_htt': valueszh
    },
    'type': 'lnN',
}

values = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ggZH','125.09','scale','sm')

nuisances['QCDscale_ggZH'] = {
    'name': 'QCDscale_ggZH', 
    'samples': {
        'ggZH_hww': values
    },
    'type': 'lnN',
}

values = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ttH','125.09','scale','sm')

nuisances['QCDscale_ttH'] = {
    'name': 'QCDscale_ttH',
    'samples': {
        'ttH_hww': values
    },
    'type': 'lnN',
}

# nuisances['QCDscale_WWewk'] = {
#     'name': 'QCDscale_WWewk',
#     'kind': 'weight_envelope',
#     'type': 'shape',
#     'samples': {
#         'WWewk': ['LHEScaleWeight[0]', 'LHEScaleWeight[2]']
#     }
# }

nuisances['QCDscale_qqbar_ACCEPT'] = {
    'name': 'QCDscale_qqbar_ACCEPT',
    'type': 'lnN',
    'samples': {
        'qqH_hww': '1.003',
        'qqH_htt': '1.003',
        'WH_hww': '1.010',
        'WH_htt': '1.010',
        'ZH_hww': '1.015',
        'ZH_htt': '1.015',
        #'VZ': '1.004',
    }
}

nuisances['QCDscale_gg_ACCEPT'] = {
    'name': 'QCDscale_gg_ACCEPT',
    'samples': {
        #'ggH_hww': '1.012',
        'ggH_htt': '1.012',
        'ggZH_hww': '1.012',
        'ggWW': '1.012',
    },
    'type': 'lnN',
}



##rate parameters TOP

nuisances['top_DeltaPhi_0']  = {
                 'name'  : 'CMS_hww_top_DeltaPhi_0',
                 'samples'  : {
                   'top' : '1.00',
                     },
                 'type'  : 'rateParam',
                 'cuts' : cuts_DeltaPhi_0
                }


nuisances['top_DeltaPhi_1']  = {
                 'name'  : 'CMS_hww_top_DeltaPhi_1',
                 'samples'  : {
                   'top' : '1.00',
                     },
                 'type'  : 'rateParam',
                 'cuts' : cuts_DeltaPhi_1
                }

nuisances['top_DeltaPhi_2']  = {
                 'name'  : 'CMS_hww_top_DeltaPhi_2',
                 'samples'  : {
                   'top' : '1.00',
                     },
                 'type'  : 'rateParam',
                 'cuts' : cuts_DeltaPhi_2
                }

nuisances['top_DeltaPhi_3']  = {
                 'name'  : 'CMS_hww_top_DeltaPhi_3',
                 'samples'  : {
                   'top' : '1.00',
                     },
                 'type'  : 'rateParam',
                 'cuts' : cuts_DeltaPhi_3
                }

##rate parameters DYTT

nuisances['dytt_DeltaPhi_0']  = {
                 'name'  : 'CMS_hww_dytt_DeltaPhi_0',
                 'samples'  : {
                   'dytt' : '1.00',
                     },
                 'type'  : 'rateParam',
                 'cuts' : cuts_DeltaPhi_0
                }


nuisances['dytt_DeltaPhi_1']  = {
                 'name'  : 'CMS_hww_dytt_DeltaPhi_1',
                 'samples'  : {
                   'dytt' : '1.00',
                     },
                 'type'  : 'rateParam',
                 'cuts' : cuts_DeltaPhi_1
                }

nuisances['dytt_DeltaPhi_2']  = {
                 'name'  : 'CMS_hww_dytt_DeltaPhi_2',
                 'samples'  : {
                   'dytt' : '1.00',
                     },
                 'type'  : 'rateParam',
                 'cuts' : cuts_DeltaPhi_2
                }

nuisances['dytt_DeltaPhi_3']  = {
                 'name'  : 'CMS_hww_dytt_DeltaPhi_3',
                 'samples'  : {
                   'dytt' : '1.00',
                     },
                 'type'  : 'rateParam',
                 'cuts' : cuts_DeltaPhi_3
                }


#rate param WW
# nuisances['WW_DeltaPhi_0']  = {
#                  'name'  : 'CMS_hww_ww_DeltaPhi_0',
#                  'samples'  : {
#                    'WW' : '1.00',
#                      },
#                  'type'  : 'rateParam',
#                  'cuts' : cuts_DeltaPhi_0
#                 }


# nuisances['WW_DeltaPhi_1']  = {
#                  'name'  : 'CMS_hww_ww_DeltaPhi_1',
#                  'samples'  : {
#                    'WW' : '1.00',
#                      },
#                  'type'  : 'rateParam',
#                  'cuts' : cuts_DeltaPhi_1
#                 }

# nuisances['WW_DeltaPhi_2']  = {
#                  'name'  : 'CMS_hww_ww_DeltaPhi_2',
#                  'samples'  : {
#                    'WW' : '1.00',
#                      },
#                  'type'  : 'rateParam',
#                  'cuts' : cuts_DeltaPhi_2
#                 }

# nuisances['WW_DeltaPhi_3']  = {
#                  'name'  : 'CMS_hww_ww_DeltaPhi_3',
#                  'samples'  : {
#                    'WW' : '1.00',
#                      },
#                  'type'  : 'rateParam',
#                  'cuts' : cuts_DeltaPhi_3
#                 }




## Use the following if you want to apply the automatic combine MC stat nuisances.
nuisances['stat'] = {
    'type': 'auto',
    'maxPoiss': '10',
    'includeSignal': '0',
    #  nuisance ['maxPoiss'] =  Number of threshold events for Poisson modelling
    #  nuisance ['includeSignal'] =  Include MC stat nuisances on signal processes (1=True, 0=False)
    'samples': {}
}

