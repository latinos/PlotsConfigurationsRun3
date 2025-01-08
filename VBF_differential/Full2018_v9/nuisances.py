mcProduction = 'Summer20UL18_106x_nAODv9_Full2018v9'
dataReco = 'Run2018_UL2018_nAODv9_Full2018v9'
mcSteps = 'MCl1loose2018v9__MCCorr2018v9NoJERInHorn__l2tightOR2018v9'
fakeSteps = 'DATAl1loose2018v9__l2loose__fakeW'
dataSteps = 'DATAl1loose2018v9__l2loose__l2tightOR2018v9'

treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'
#limitFiles = -1

# from mkShapesRDF.processor.tools.HiggsXSection import HiggsXSection
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

##### Luminosity

# https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun2#LumiComb
# Uncorrelated 2016               1.0
# Uncorrelated       2017              2.0
# Uncorrelated             2018             1.5
# Correlated   2016, 2017, 2018   0.6, 0.9, 2.0
# Correlated         2017, 2018        0.6, 0.2

nuisances['lumi_Uncorrelated'] = {
    'name'    : 'lumi_13TeV_2018',
    'type'    : 'lnN',
    'samples' : dict((skey, '1.015') for skey in mc if skey not in ['top',  'dytt'])
}

nuisances['lumi_Correlated_Run2'] = {
    'name'    : 'lumi_13TeV_correlated',
    'type'    : 'lnN',
    'samples' : dict((skey, '1.020') for skey in mc if skey not in ['top',  'dytt'])
}

nuisances['lumi_Correlated_2017_2018'] = {
    'name'    : 'lumi_13TeV_1718',
    'type'    : 'lnN',
    'samples' : dict((skey, '1.002') for skey in mc if skey not in ['top',  'dytt'])
}


##### FAKES

nuisances['fake_syst_e'] = {
    'name': 'CMS_fake_syst_e',
    'type': 'lnN',
    'samples': {
        'Fake_e': '1.3'
    },
}

nuisances['fake_syst_m'] = {
    'name': 'CMS_fake_syst_m',
    'type': 'lnN',
    'samples': {
        'Fake_m': '1.3'
    },
}

nuisances['fake_ele'] = {
    'name': 'CMS_fake_e_2018',
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake': ['fakeWEleUp', 'fakeWEleDown'],
    }
}

nuisances['fake_ele_stat'] = {
    'name': 'CMS_fake_stat_e_2018',
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake': ['fakeWStatEleUp', 'fakeWStatEleDown']
    }
}

nuisances['fake_mu'] = {
    'name': 'CMS_fake_m_2018',
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake': ['fakeWMuUp', 'fakeWMuDown'],
    }
}

nuisances['fake_mu_stat'] = {
    'name': 'CMS_fake_stat_m_2018',
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake': ['fakeWStatMuUp', 'fakeWStatMuDown'],
    }
}

###### B-tagger

# Fixed BTV SF variations
for flavour in ['bc', 'light']:
    for corr in ['uncorrelated', 'correlated']:
        btag_syst = [f'btagSF{flavour}_up_{corr}/btagSF{flavour}', f'btagSF{flavour}_down_{corr}/btagSF{flavour}']
        if corr == 'correlated':
            name = f'CMS_btagSF{flavour}_{corr}'
        else:
            name = f'CMS_btagSF{flavour}_2018'
        nuisances[f'btagSF{flavour}{corr}'] = {
            'name': name,
            'skipCMS' : 1,
            'kind': 'weight',
            'type': 'shape',
            'samples': dict((skey, btag_syst) for skey in mc),
        }
'''
for shift in ['lf', 'hf', 'hfstats1', 'hfstats2', 'lfstats1', 'lfstats2', 'cferr1', 'cferr2']:
    btag_syst = ['(btagSF%sup)/(btagSF)' % shift, '(btagSF%sdo)/(btagSF)' % shift]

    name = 'CMS_btag_%s' % shift
    if 'stats' in shift:
        name += '_2018'

    nuisances['btag_shape_%s' % shift] = {
        'name': name,
        'kind': 'weight',
        'type': 'shape',
        'samples': dict((skey, btag_syst) for skey in mc),
    }
'''
##### Trigger Scale Factors

trig_syst = ['TriggerSFWeight_2l_u/TriggerSFWeight_2l', 'TriggerSFWeight_2l_d/TriggerSFWeight_2l']

nuisances['trigg'] = {
    'name': 'CMS_eff_hwwtrigger_2018',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, trig_syst) for skey in mc)
}

##### Electron Efficiency and energy scale

nuisances['eff_e'] = {
    'name': 'CMS_eff_e_2018',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, ['SFweightEleUp', 'SFweightEleDown']) for skey in mc)
}

nuisances['electronpt'] = {
    'name': 'CMS_scale_e_2018',
    'kind': 'suffix',
    'type': 'shape',
    'mapUp': 'ElepTup',
    'mapDown': 'ElepTdo',
    'samples': dict((skey, ['1', '1']) for skey in mc if skey not in ac_sig),
    'folderUp': makeMCDirectory('ElepTup_suffix'),
    'folderDown': makeMCDirectory('ElepTdo_suffix'),
#    'AsLnN': '1'
}

##### Muon Efficiency and energy scale

nuisances['eff_m'] = {
    'name': 'CMS_eff_m_2018',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, ['SFweightMuUp', 'SFweightMuDown']) for skey in mc)
}

nuisances['muonpt'] = {
    'name': 'CMS_scale_m_2018',
    'kind': 'suffix',
    'type': 'shape',
    'mapUp': 'MupTup',
    'mapDown': 'MupTdo',
    'samples': dict((skey, ['1', '1']) for skey in mc if skey not in ac_sig),
    'folderUp': makeMCDirectory('MupTup_suffix'),
    'folderDown': makeMCDirectory('MupTdo_suffix'),
#    'AsLnN': '1'
}

##### PU ID SF uncertainty

puid_syst = ['Jet_PUIDSF_up/Jet_PUIDSF', 'Jet_PUIDSF_down/Jet_PUIDSF']

nuisances['jetPUID'] = {
    'name': 'CMS_PUID_2018',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, puid_syst) for skey in mc)
}


##### Jet energy scale
jes_systs    = ['JESAbsolute','JESAbsolute_2018','JESBBEC1','JESBBEC1_2018','JESEC2','JESEC2_2018','JESFlavorQCD','JESHF','JESHF_2018','JESRelativeBal','JESRelativeSample_2018']

for js in jes_systs:

  nuisances[js] = {
      'name'      : 'CMS_scale_' + js,
      'kind'      : 'suffix',
      'type'      : 'shape',
      'mapUp'     : js + 'up',
      'mapDown'   : js + 'do',
      'samples'   : dict((skey, ['1', '1']) for skey in mc if skey not in ac_sig),
      'folderUp'  : makeMCDirectory('RDF__JESup_suffix'),
      'folderDown': makeMCDirectory('RDF__JESdo_suffix'),
      'AsLnN'     : '1'
  }


##### Jet energy resolution
nuisances['JER'] = {
    'name'      : 'CMS_res_j_2018',
    'kind'      : 'suffix',
    'type'      : 'shape',
    'mapUp'     : 'JERup',
    'mapDown'   : 'JERdo',
    'samples'   : dict((skey, ['1', '1']) for skey in mc if skey not in ac_sig),
    'folderUp'  : makeMCDirectory('JERup_suffix'),
    'folderDown': makeMCDirectory('JERdo_suffix'),
    'AsLnN'     : '0'
}

##### MET energy scale
# metUp.PuppiMET_pt_METup
nuisances['met'] = {
    'name'      : 'CMS_scale_met_2018',
    'kind'      : 'suffix',
    'type'      : 'shape',
    'mapUp'     : 'METup',
    'mapDown'   : 'METdo',
    'samples'   : dict((skey, ['1', '1']) for skey in mc if skey not in ac_sig),
    'folderUp'  : makeMCDirectory('METup_suffix'),
    'folderDown': makeMCDirectory('METdo_suffix'),
    'AsLnN'   : '1',
}

##### Pileup

# puWeight_UL2018
nuisances['PU'] = {
    'name'    : 'CMS_pileup_2018',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : {
        'dytt'      : ['0.998687*(puWeightUp/puWeight)', '1.001976*(puWeightDown/puWeight)'],
        'top'     : ['1.002595*(puWeightUp/puWeight)', '0.997470*(puWeightDown/puWeight)'],
        'WW'      : ['1.004449*(puWeightUp/puWeight)', '0.995660*(puWeightDown/puWeight)'],
        'WWewk'   : ['1.002122*(puWeightUp/puWeight)', '0.998087*(puWeightDown/puWeight)'],
        'ggWW'    : ['1.004870*(puWeightUp/puWeight)', '0.995315*(puWeightDown/puWeight)'],
        'WZ'      : ['0.999330*(puWeightUp/puWeight)', '1.000992*(puWeightDown/puWeight)'],
        'ZZ'      : ['0.999469*(puWeightUp/puWeight)', '1.000751*(puWeightDown/puWeight)'],
        'VVV'     : ['1.003485*(puWeightUp/puWeight)', '0.997561*(puWeightDown/puWeight)'],
        'ggH_hww' : ['1.003677*(puWeightUp/puWeight)', '0.995996*(puWeightDown/puWeight)'],
        'qqH_hww' : ['1.003747*(puWeightUp/puWeight)', '0.995878*(puWeightDown/puWeight)'],
    },
    'AsLnN'   : '0',
}

nuisances['PU']['samples'].update(dict((skey, ['1.003677*(puWeightUp/puWeight)', '0.995996*(puWeightDown/puWeight)']) for skey in mc if 'ggH_hww' in skey))
nuisances['PU']['samples'].update(dict((skey, ['1.003747*(puWeightUp/puWeight)', '0.995878*(puWeightDown/puWeight)']) for skey in mc if 'qqH_hww' in skey))

##### PS and UE

nuisances['PS_ISR']  = {
    'name'    : 'PS_ISR',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['PSWeight[2]', 'PSWeight[0]']) for skey in mc if skey not in ['ggH_hww','qqH_hww']),
    'AsLnN'   : '0',
}


nuisances['PS_ISR_higgs']  = {
    'name'    : 'PS_ISR',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict(list((skey, ['PSWeight[2]*norm_ggh_PS_ISR_up', 'PSWeight[0]*norm_ggh_PS_ISR_down']) for skey in ggH_sig) +
                     list((skey, ['PSWeight[2]*norm_qqh_PS_ISR_up', 'PSWeight[0]*norm_qqh_PS_ISR_down']) for skey in qqH_sig)),
    # 'samples' : {
    #     'ggH_hww' : ['PSWeight[2]*norm_ggh_PS_ISR_up', 'PSWeight[0]*norm_ggh_PS_ISR_down'],
    #     'qqH_hww' : ['PSWeight[2]*norm_qqh_PS_ISR_up', 'PSWeight[0]*norm_qqh_PS_ISR_down'],
    #     },
    'AsLnN'   : '0',
}


mc_bkg = [skey for skey in mc if skey not in ['ggH_hww','qqH_hww']]
for skey in mc_bkg:
    if skey not in ['VgS']:
        nuisances['PS_FSR_'+ skey]  = {
            'name'    : 'PS_FSR_'+ skey,
            'kind'    : 'weight',
            'type'    : 'shape',
            'samples' : {
                skey : ['PSWeight[3]', 'PSWeight[1]'],
                },
            'AsLnN'   : '0',
        }
    else:
         nuisances['PS_FSR_'+ skey]  = {
            'name'    : 'PS_FSR_'+ skey,
            'kind'    : 'weight',
            'type'    : 'shape',
            'samples' : {
                skey : ['PSWeight[3]', 'PSWeight[1]'],
                },
            'AsLnN'   : '1',
        }

# nuisances['PS_FSR']  = {
#     'name'    : 'PS_FSR',
#     'kind'    : 'weight',
#     'type'    : 'shape',
#     'samples' : dict((skey, ['PSWeight[3]', 'PSWeight[1]']) for skey in mc if skey not in ['ggH_hww','qqH_hww']),
#     'AsLnN'   : '0',
# }

nuisances['PS_FSR_qqH_hww']  = {
    'name'    : 'PS_FSR_qqH_hww',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['PSWeight[3]*norm_qqh_PS_FSR_up', 'PSWeight[1]*norm_qqh_PS_FSR_down']) for skey in qqH_sig), 
    # 'samples' : {
    #     'qqH_hww' : ['PSWeight[3]*norm_qqh_PS_FSR_up', 'PSWeight[1]*norm_qqh_PS_FSR_down'],
    #     },
    'AsLnN'   : '0',
}

nuisances['PS_FSR_ggH_hww']  = {
    'name'    : 'PS_FSR_ggH_hww',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['PSWeight[3]*norm_ggh_PS_FSR_up', 'PSWeight[1]*norm_ggh_PS_FSR_down']) for skey in ggH_sig),
    # 'samples' : {
    #     'ggH_hww' : ['PSWeight[3]*norm_ggh_PS_FSR_up', 'PSWeight[1]*norm_ggh_PS_FSR_down'],
    #     },
    'AsLnN'   : '0',
}



nuisances['UE_CP5']  = {
    'name'    : 'CMS_UE',
    'skipCMS' : 1,
    'type'    : 'lnN',
    'samples' : dict((skey, '1.015') for skey in mc),
}

###### pdf uncertainties

valuesggh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ggH','125.09','pdf','sm')
valuesggzh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ggZH','125.09','pdf','sm')
valuesbbh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','bbH','125.09','pdf','sm')

nuisances['pdf_Higgs_gg'] = {
    'name': 'pdf_Higgs_gg',
    'samples': {
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
    'cuts' : ['hww2l2v_13TeV_of2j_dphijj_4bins_0', 'hww2l2v_13TeV_of2j_dphijj_4bins_1', 'hww2l2v_13TeV_of2j_dphijj_4bins_2', 'hww2l2v_13TeV_of2j_dphijj_4bins_3'],
}

nuisances['pdf_gg_ACCEPT'] = {
    'name': 'pdf_gg_ACCEPT',
    'samples': {
        'ggWW': '1.006',
    },
    'type': 'lnN',
    'cuts' : ['hww2l2v_13TeV_of2j_dphijj_4bins_0', 'hww2l2v_13TeV_of2j_dphijj_4bins_1', 'hww2l2v_13TeV_of2j_dphijj_4bins_2', 'hww2l2v_13TeV_of2j_dphijj_4bins_3'],
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
    'cuts' : ['hww2l2v_13TeV_of2j_dphijj_4bins_0', 'hww2l2v_13TeV_of2j_dphijj_4bins_1', 'hww2l2v_13TeV_of2j_dphijj_4bins_2', 'hww2l2v_13TeV_of2j_dphijj_4bins_3'],
}

nuisances['pdf_qqbar_ACCEPT'] = {
    'name': 'pdf_qqbar_ACCEPT',
    'type': 'lnN',
    'samples': {
        'VZ': '1.001',
    },
    'cuts' : ['hww2l2v_13TeV_of2j_dphijj_4bins_0', 'hww2l2v_13TeV_of2j_dphijj_4bins_1', 'hww2l2v_13TeV_of2j_dphijj_4bins_2', 'hww2l2v_13TeV_of2j_dphijj_4bins_3'],
}


###### pdf uncertainties
pdf_variations = ["Alt(LHEPdfWeight,%d,1)" %i for i in range(100)]

##### PDF uncertainties on WW
nuisances['pdf_WW']  = {
 'name'  : 'CMS_hww_pdf_WW',
 'skipCMS' : 1,
 'kind'  : 'weight_rms',
 'type'  : 'shape',
 'samples'  : {
    'WW'   : pdf_variations,
  },
}

##### PDF uncertainties on top
nuisances['pdf_top']  = {
 'name'  : 'CMS_hww_pdf_top',
 'skipCMS' : 1,
 'kind'  : 'weight_rms',
 'type'  : 'shape',
 'samples'  : {
    'top'   : pdf_variations,
  },
}

##### Generic "cross section uncertainties"

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

##### Top pT reweighting uncertainty

# nuisances['TopPtRew'] = {
#     'name'       : 'CMS_top_pT_reweighting',   # Theory uncertainty
#     'kind'       : 'weight',
#     'type'       : 'shape',
#     'samples'    : {
#         'top': ["1.", "1./Top_pTrw"]
#     },
#     'symmetrize' : True
# }

#####  VgStar and Vg

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
}

# Uncertainty on SR/CR ratio
nuisances['CRSR_accept_top'] = {
    'name': 'CMS_hww_CRSR_accept_top',
    'type': 'lnN',
    'samples': {'top': '1.01'},
    'cuts': [cut for cut in cuts2j if 'top' in cut],
}


##### Renormalization & factorization scales

#### QCD scale for VBF and ggH


nuisances['QCDscale_ren_ggH_hww'] = {
        'name'    : 'CMS_QCDscale_ren_ggH_hww',
        'skipCMS' : 1,
        'kind'    : 'weight',
        'type'    : 'shape',
        'samples' : dict((skey, ['Alt(LHEScaleWeight,1,1)*norm_ggh_QCDscale_ren_ggH_hww_up','Alt(LHEScaleWeight,nLHEScaleWeight-2,1)*norm_ggh_QCDscale_ren_ggH_hww_down']) for skey in ggH_sig), 
        'AsLnN'   : '0'
    }


nuisances['QCDscale_fac_ggH_hww'] = {
        'name'    : 'CMS_QCDscale_fac_ggH_hww',
        'skipCMS' : 1,
        'kind'    : 'weight',
        'type'    : 'shape',
        'samples' : dict((skey, ['Alt(LHEScaleWeight,1,1)*norm_ggh_QCDscale_fac_ggH_hww_up','Alt(LHEScaleWeight,nLHEScaleWeight-2,1)*norm_ggh_QCDscale_fac_ggH_hww_down']) for skey in ggH_sig), 
        'AsLnN'   : '0'
    }

nuisances['QCDscale_ren_qqH_hww'] = {
        'name'    : 'CMS_QCDscale_ren_qqH_hww',
        'skipCMS' : 1,
        'kind'    : 'weight',
        'type'    : 'shape',
        'samples' : dict((skey, ['Alt(LHEScaleWeight,1,1)*norm_qqh_QCDscale_ren_qqH_hww_up','Alt(LHEScaleWeight,nLHEScaleWeight-2,1)*norm_qqh_QCDscale_ren_qqH_hww_down']) for skey in qqH_sig), 
        'AsLnN'   : '0'
    }


nuisances['QCDscale_fac_qqH_hww'] = {
        'name'    : 'CMS_QCDscale_fac_qqH_hww',
        'skipCMS' : 1,
        'kind'    : 'weight',
        'type'    : 'shape',
        'samples' : dict((skey, ['Alt(LHEScaleWeight,1,1)*norm_qqh_QCDscale_fac_qqH_hww_up','Alt(LHEScaleWeight,nLHEScaleWeight-2,1)*norm_qqh_QCDscale_fac_qqH_hww_down']) for skey in qqH_sig),
        'AsLnN'   : '0'
    }



#### QCD scale uncertainties for Higgs signals other than ggH

values = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','vbfH','125.09','scale','sm')

nuisances['QCDscale_qqH'] = {
    'name': 'QCDscale_qqH', 
    'samples': {
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

nuisances['QCDscale_WWewk'] = {
    'name': 'QCDscale_WWewk',
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'WWewk': ['LHEScaleWeight[0]', 'LHEScaleWeight[2]']
    }
}

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
    },
    'cuts' : ['hww2l2v_13TeV_of2j_dphijj_4bins_0', 'hww2l2v_13TeV_of2j_dphijj_4bins_1', 'hww2l2v_13TeV_of2j_dphijj_4bins_2', 'hww2l2v_13TeV_of2j_dphijj_4bins_3'],
}

nuisances['QCDscale_gg_ACCEPT'] = {
    'name': 'QCDscale_gg_ACCEPT',
    'samples': {
        'ggH_hww': '1.012',
        'ggH_htt': '1.012',
        'ggZH_hww': '1.012',
        'ggWW': '1.012',
    },
    'type': 'lnN',
    'cuts' : ['hww2l2v_13TeV_of2j_dphijj_4bins_0', 'hww2l2v_13TeV_of2j_dphijj_4bins_1', 'hww2l2v_13TeV_of2j_dphijj_4bins_2', 'hww2l2v_13TeV_of2j_dphijj_4bins_3'],
}


## Shape nuisance due to QCD scale variations for DY
## LHE scale variation weights (w_var / w_nominal)

## This should work for samples with either 8 or 9 LHE scale weights (Length$(LHEScaleWeight) == 8 or 9)
variations = ['Alt(LHEScaleWeight,0,1)', 'Alt(LHEScaleWeight,1,1)', 'Alt(LHEScaleWeight,3,1)', 'Alt(LHEScaleWeight,nLHEScaleWeight-4,1)', 'Alt(LHEScaleWeight,nLHEScaleWeight-2,1)', 'Alt(LHEScaleWeight,nLHEScaleWeight-1,1)']

nuisances['QCDscale_V'] = {
    'name'    : 'QCDscale_V',
    'skipCMS' : 1,
    'kind'    : 'weight_envelope',
    'type'    : 'shape',
    'samples' : {
        'dytt' : variations
    },
    'AsLnN'   : '0'
}

nuisances['QCDscale_VV'] = {
   'name' : 'QCDscale_VV',
   'kind' : 'weight_envelope',
   'type' : 'shape',
   'samples' : {
       'WW'  : variations,
       'Zg'  : variations,
       'Wg'  : variations,
       'ZZ'  : variations,
       'WZ'  : variations,
       'WgS' : variations,
       'ZgS' : variations
   }
}

nuisances['QCDscale_ggVV'] = {
    'name'    : 'QCDscale_ggVV',
    'type'    : 'lnN',
    'samples' : {
        'ggWW' : '1.15',
    },
}


nuisances['WWresum']  = {
    'name'  : 'CMS_hww_WWresum',
    'kind'  : 'weight',
    'type'  : 'shape',
    'AsLnN': '0',
    'samples'  : {
        'WW'   : ['nllW_Rup/nllW', 'nllW_Rdown/nllW'],
    },
}

nuisances['WWqscale']  = {
    'name'  : 'CMS_hww_WWqscale',
    'kind'  : 'weight',
    'type'  : 'shape',
    'AsLnN': '0',
    'samples'  : {
        'WW'   : ['nllW_Qup/nllW', 'nllW_Qdown/nllW'],
    },
}


topvars2j = ['Alt(LHEScaleWeight,0, 1.)', 'Alt(LHEScaleWeight,8, 1.)']

nuisances['QCDscale_top_2j']  = {
    'name'  : 'QCDscale_top_2j',
    'skipCMS' : 1,
    'kind'  : 'weight',
    'type'  : 'shape',
    'samples'  : {
       'top' : topvars2j,
    }
}


# Theory uncertainty for ggH
#
#
#   THU_ggH_Mu, THU_ggH_Res, THU_ggH_Mig01, THU_ggH_Mig12, THU_ggH_VBF2j, THU_ggH_VBF3j, THU_ggH_PT60, THU_ggH_PT120, THU_ggH_qmtop
#
#   see https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsWG/SignalModelingTools

thus = [
    # ('THU_ggH_Mu', 'ggH_mu'), # QCD uncertainty split into 4 independent sources: ggH_Mu: normalization, ggH_res: resummation, ggH_Mig01: 0-1 jet category migration, ggH_Mig12 1-2 jet category migration
    ('THU_ggH_Res', 'ggH_res'),
    # ('THU_ggH_Mig01', 'ggH_mig01'),
    # ('THU_ggH_Mig12', 'ggH_mig12'),
    # ('THU_ggH_VBF2j', 'ggH_VBF2j'), # VBF topology
    # ('THU_ggH_VBF3j', 'ggH_VBF3j'), # VBF topology
    # ('THU_ggH_PT60', 'ggH_pT60'), # Migration uncertainty around the 60 GeV boundary
    # ('THU_ggH_PT120', 'ggH_pT120'), # Migration uncertainty around the 120 GeV boundary
    ('THU_ggH_qmtop', 'ggH_qmtop') # Difference between finite top mass dependence @NLO vs @LO evaluated using Powheg NNLOPS taken as uncertainty on the treatment of top mass in ggF loop
]

for name, vname in thus:

    updown = [f'{vname}*norm_ggh_{name}_up', f'(2. - {vname})*norm_ggh_{name}_down']

    nuisances[name] = {
        'name': name,
        'skipCMS': 1,
        'kind': 'weight',
        'type': 'shape',
        'samples' : dict((skey, updown) for skey in ggH_sig),
        # 'samples' : {
        #     'ggH_hww' : updown,
        #     }
    }

# Theory uncertainty for qqH 
#
#
#   see https://gitlab.cern.ch/LHCHIGGSXS/LHCHXSWG2/STXS/VBF-Uncertainties/-/blob/master/qq2Hqq_uncert_scheme.cpp

#  uncertainty sources
#  10 QCD-nuisances:  1 x yields uncertainty on the inclusive xsec, 9 x migration uncertainties (1 x 3rd jet veto, 6 x Mjj cuts, 1 x PTH cut, 1 x 01->2 jetBin)

thusQQH = [
#   ("THU_qqH_YIELD","qqH_YIELD"),
#   ("THU_qqH_PTH200","qqH_PTH200"),
#   ("THU_qqH_Mjj60","qqH_Mjj60"),
#   ("THU_qqH_Mjj120","qqH_Mjj120"),
#   ("THU_qqH_Mjj350","qqH_Mjj350"),
#   ("THU_qqH_Mjj700","qqH_Mjj700"),
#   ("THU_qqH_Mjj1000","qqH_Mjj1000"),
#   ("THU_qqH_Mjj1500","qqH_Mjj1500"),
#   ("THU_qqH_PTH25","qqH_PTH25"),
#   ("THU_qqH_JET01","qqH_JET01"),
  ("THU_qqH_EWK","qqH_EWK"), # Electroweak corrections
]

for name, vname in thusQQH:

    updown = [f'{vname}*norm_qqh_{name}_up', f'(2. - {vname})*norm_qqh_{name}_down']

    nuisances[name] = {
        'name': name,
        'skipCMS': 1,
        'kind': 'weight',
        'type': 'shape',
        'samples' : dict((skey, updown) for skey in qqH_sig),
        # 'samples' : {
        #     'qqH_hww' : updown,
        #     }
        }


#####Rate parameters TOP

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

#####Rate parameters DYTT

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



## Use the following if you want to apply the automatic combine MC stat nuisances.
nuisances['stat'] = {
    'type': 'auto',
    'maxPoiss': '10',
    'includeSignal': '0',
    #  nuisance ['maxPoiss'] =  Number of threshold events for Poisson modelling
    #  nuisance ['includeSignal'] =  Include MC stat nuisances on signal processes (1=True, 0=False)
    'samples': {}
}

