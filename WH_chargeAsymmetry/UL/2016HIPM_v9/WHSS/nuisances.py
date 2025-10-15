import sys
 
# Enable reading YR for Higgs XS and uncertainties
sys.path.append('{}/macros/'.format(configurations_nuisance))
import HiggsXSection
HiggsXS = HiggsXSection.HiggsXSection()

nuisances = {}

mcProduction = 'Summer20UL16_106x_nAODv9_HIPM_Full2016v9'
dataReco     = 'Run2016_UL2016_nAODv9_HIPM_Full2016v9'
mcSteps      = 'MCl1loose2016v9__MCCorr2016v9NoJERInHorn__l2tightOR2016v9'
fakeSteps    = 'DATAl1loose2016v9__l2loose__fakeW'
dataSteps    = 'DATAl1loose2016v9__l2loose__l2tightOR2016v9'

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
    'name'    : 'lumi_13TeV_2016',
    'type'    : 'lnN',
    'samples' : dict((skey, '1.010') for skey in mc if skey not in ['WZ'])
}

nuisances['lumi_Correlated_Run2'] = {
    'name'    : 'lumi_13TeV_correlated',
    'type'    : 'lnN',
    'samples' : dict((skey, '1.006') for skey in mc if skey not in ['WZ'])
}


#### FAKES

# Systematic uncertainty split into barrel and endcap, and per final state: 10% per bin
fake_syst_endcap = ['1.0*(abs(Lepton_eta[1])<=1.479) +     1.1*(abs(Lepton_eta[1])>1.479)',
                    '1.0*(abs(Lepton_eta[1])<=1.479) + 1.0/1.1*(abs(Lepton_eta[1])>1.479)']

fake_syst_barrel = ['    1.1*(abs(Lepton_eta[1])<=1.479) + 1.0*(abs(Lepton_eta[1])>1.479)',
                    '1.0/1.1*(abs(Lepton_eta[1])<=1.479) + 1.0*(abs(Lepton_eta[1])>1.479)']

# nuisances['fake_syst_mm_barrel'] = {
#     'name'    : 'CMS_WH_hww_fake_syst_mm_barrel',
#     'kind'    : 'weight',
#     'type'    : 'shape',
#     'samples' : {
#         'Fake_mm' : fake_syst_barrel,
#     },
#     'cuts'    : [cut for cut in cuts if ('_mm_' in cut)]
# }
# nuisances['fake_syst_mm_endcap'] = {
#     'name'    : 'CMS_WH_hww_fake_syst_mm_endcap',
#     'kind'    : 'weight',
#     'type'    : 'shape',
#     'samples' : {
#         'Fake_mm' : fake_syst_endcap,
#     },
#     'cuts'    : [cut for cut in cuts if ('_mm_' in cut)]
# }

# nuisances['fake_syst_em_barrel'] = {
#     'name'    : 'CMS_WH_hww_fake_syst_em_barrel',
#     'kind'    : 'weight',
#     'type'    : 'shape',
#     'samples' : {
#         'Fake_em' : fake_syst_barrel,
#     },
#     'cuts'    : [cut for cut in cuts if ('_em_' in cut)]
# }
# nuisances['fake_syst_em_endcap'] = {
#     'name'    : 'CMS_WH_hww_fake_syst_em_endcap',
#     'kind'    : 'weight',
#     'type'    : 'shape',
#     'samples' : {
#         'Fake_em' : fake_syst_endcap,
#     },
#     'cuts'    : [cut for cut in cuts if ('_em_' in cut)]
# }

# nuisances['fake_syst_ee_barrel'] = {
#     'name'    : 'CMS_WH_hww_fake_syst_ee_barrel',
#     'kind'    : 'weight',
#     'type'    : 'shape',
#     'samples' : {
#         'Fake_ee' : fake_syst_barrel,
#     },
#     'cuts'    : [cut for cut in cuts if ('_ee' in cut)]
# }
# nuisances['fake_syst_ee_endcap'] = {
#     'name'    : 'CMS_WH_hww_fake_syst_ee_endcap',
#     'kind'    : 'weight',
#     'type'    : 'shape',
#     'samples' : {
#         'Fake_ee' : fake_syst_endcap,
#     },
#     'cuts'    : [cut for cut in cuts if ('_ee' in cut)]
# }

# Overall 30% normalization
nuisances['fake_syst_ee'] = {
    'name'    : 'CMS_WH_hww_fake_syst_ee_2016',
    'kind'    : 'weight',
    'type'    : 'lnN',
    'samples' : {
        'Fake_ee' : '1.3',
    },
}

nuisances['fake_syst_em'] = {
    'name'    : 'CMS_WH_hww_fake_syst_em_2016',
    'kind'    : 'weight',
    'type'    : 'lnN',
    'samples' : {
        'Fake_em' : '1.3',
    },
}

nuisances['fake_syst_mm'] = {
    'name'    : 'CMS_WH_hww_fake_syst_mm_2016',
    'kind'    : 'weight',
    'type'    : 'lnN',
    'samples' : {
        'Fake_mm' : '1.3',
    },
}

# Statistical and systematic uncertainty on the fake rates
nuisances['fake_ele'] = {
    'name'    : 'CMS_WH_hww_fake_e_2016',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : {
        'Fake_ee' : ['fakeWEleUp', 'fakeWEleDown'],
        'Fake_em' : ['fakeWEleUp', 'fakeWEleDown'],
    }
}
nuisances['fake_ele_stat'] = {
    'name'    : 'CMS_WH_hww_fake_stat_e_2016',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : {
        'Fake_ee' : ['fakeWStatEleUp', 'fakeWStatEleDown'],
        'Fake_em' : ['fakeWStatEleUp', 'fakeWStatEleDown'],
    }
}

nuisances['fake_mu'] = {
    'name'    : 'CMS_WH_hww_fake_m_2016',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : {
        'Fake_mm' : ['fakeWMuUp', 'fakeWMuDown'],
        'Fake_em' : ['fakeWMuUp', 'fakeWMuDown'],
    }   
}       
nuisances['fake_mu_stat'] = {
    'name'    : 'CMS_WH_hww_fake_stat_m_2016',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : {
        'Fake_mm' : ['fakeWStatMuUp', 'fakeWStatMuDown'],
        'Fake_em' : ['fakeWStatMuUp', 'fakeWStatMuDown'],
    }
}

###### B-tagger

for shift in ['lf', 'hf', 'hfstats1', 'hfstats2', 'lfstats1', 'lfstats2', 'cferr1', 'cferr2']:
    btag_syst = ['(btagSF%sup)/(btagSF)' % shift, '(btagSF%sdown)/(btagSF)' % shift]

    name = 'CMS_btag_%s' % shift
    if 'stats' in shift:
        name += '_2016'

    nuisances['btag_shape_%s' % shift] = {
        'name'    : name,
        'kind'    : 'weight',
        'type'    : 'shape',
        'samples' : dict((skey, btag_syst) for skey in mc),
    }

##### Trigger Scale Factors

trig_syst = ['TriggerSFWeight_2l_u/TriggerSFWeight_2l', 'TriggerSFWeight_2l_d/TriggerSFWeight_2l']

nuisances['trigg'] = {
    'name'    : 'CMS_eff_hwwtrigger_2016',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, trig_syst) for skey in mc)
}

##### Electron Efficiency and energy scale

nuisances['eff_e'] = {
    'name'    : 'CMS_eff_e_2016',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['SFweightEleUp', 'SFweightEleDown']) for skey in mc)
}

nuisances['eff_ttHMVA_e'] = {
    'name'    : 'CMS_eff_ttHMVA_e_2016',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['LepWPttHMVASFEleUp', 'LepWPttHMVASFEleDown']) for skey in mc)
}

nuisances['electronpt'] = {
    'name'       : 'CMS_scale_e_2016',
    'kind'       : 'suffix',
    'type'       : 'shape',
    'mapUp'      : 'ElepTup',
    'mapDown'    : 'ElepTdo',
    'samples'    : dict((skey, ['1', '1']) for skey in mc),
    'folderUp'   : makeMCDirectory('ElepTup_suffix'),
    'folderDown' : makeMCDirectory('ElepTdo_suffix'),
    'AsLnN'      : '0'
}

##### Muon Efficiency and energy scale

nuisances['eff_m'] = {
    'name'    : 'CMS_eff_m_2016',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['SFweightMuUp', 'SFweightMuDown']) for skey in mc)
}

nuisances['eff_ttHMVA_m'] = {
    'name'    : 'CMS_eff_ttHMVA_m_2016',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['LepWPttHMVASFMuUp', 'LepWPttHMVASFMuDown']) for skey in mc)
}

nuisances['muonpt'] = {
    'name'       : 'CMS_scale_m_2016',
    'kind'       : 'suffix',
    'type'       : 'shape',
    'mapUp'      : 'MupTup',
    'mapDown'    : 'MupTdo',
    'samples'    : dict((skey, ['1', '1']) for skey in mc),
    'folderUp'   : makeMCDirectory('MupTup_suffix'),
    'folderDown' : makeMCDirectory('MupTdo_suffix'),
    'AsLnN'      : '0'
}

##### Jet energy scale
jes_systs    = ['JESAbsolute','JESAbsolute_2016','JESBBEC1','JESBBEC1_2016','JESEC2','JESEC2_2016','JESFlavorQCD','JESHF','JESHF_2016','JESRelativeBal','JESRelativeSample_2016']

for js in jes_systs:

  nuisances[js] = {
      'name'      : 'CMS_scale_' + js.replace("JES","j_"),
      'kind'      : 'suffix',
      'type'      : 'shape',
      'mapUp'     : js + 'up',
      'mapDown'   : js + 'do',
      'samples'   : dict((skey, ['1', '1']) for skey in mc),
      'folderUp'  : makeMCDirectory('RDF__JESup_suffix'),
      'folderDown': makeMCDirectory('RDF__JESdo_suffix'),
      'reweight'  : ['btagSF'+js.replace('JES','jes')+'up/btagSF','btagSF'+js.replace('JES','jes')+'down/btagSF'],
      'AsLnN'     : '0'
  }

##### Jet energy resolution
nuisances['JER'] = {
    'name'      : 'CMS_res_j_2016',
    'kind'      : 'suffix',
    'type'      : 'shape',
    'mapUp'     : 'JERup',
    'mapDown'   : 'JERdo',
    'samples'   : dict((skey, ['1', '1']) for skey in mc),
    'folderUp'  : makeMCDirectory('JERup_suffix'),
    'folderDown': makeMCDirectory('JERdo_suffix'),
    'AsLnN'     : '0'
}

##### MET unclustered energy

# metUp.PuppiMET_pt_METup
nuisances['met'] = {
    'name'      : 'CMS_scale_met_2016',
    'kind'      : 'suffix',
    'type'      : 'shape',
    'mapUp'     : 'METup',
    'mapDown'   : 'METdo',
    'samples'   : dict((skey, ['1', '1']) for skey in mc),
    'folderUp'  : makeMCDirectory('METup_suffix'),
    'folderDown': makeMCDirectory('METdo_suffix'),
    'AsLnN'     : '0'
}


##### Pileup

# puWeight_UL2016
nuisances['PU'] = {
    'name'    : 'CMS_pileup_2016',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : {
        'DY'      : ['1.008421*(puWeightUp/puWeight)', '0.992494*(puWeightDown/puWeight)'],
        'WW'      : ['1.010428*(puWeightUp/puWeight)', '0.990400*(puWeightDown/puWeight)'],
        'ggWW'    : ['1.012367*(puWeightUp/puWeight)', '0.988402*(puWeightDown/puWeight)'],
        'Vg'      : ['0.995630*(puWeightUp/puWeight)', '1.007076*(puWeightDown/puWeight)'],
        'WZ'      : ['1.002037*(puWeightUp/puWeight)', '0.997721*(puWeightDown/puWeight)'],
        'ZZ'      : ['1.006574*(puWeightUp/puWeight)', '0.993175*(puWeightDown/puWeight)'],
        'VVV'     : ['1.012827*(puWeightUp/puWeight)', '0.989623*(puWeightDown/puWeight)'],
        'top'     : ['1.009336*(puWeightUp/puWeight)', '0.991324*(puWeightDown/puWeight)'],
        'Higgs'   : ['1.011609*(puWeightUp/puWeight)', '0.989039*(puWeightDown/puWeight)'],
    },
    'AsLnN'   : '0',
}

### PU ID SF uncertainty

puid_syst = ['Jet_PUIDSF_up/Jet_PUIDSF', 'Jet_PUIDSF_down/Jet_PUIDSF']

nuisances['jetPUID'] = {
    'name'    : 'CMS_eff_j_PUJET_id_2016',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, puid_syst) for skey in mc)
}

### PS and UE

nuisances['PS_ISR']  = {
    'name'    : 'PS_WH_hww_ISR',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['PSWeight[2]', 'PSWeight[0]']) for skey in mc),
    'AsLnN'   : '0',
}

nuisances['PS_FSR']  = {
    'name'    : 'PS_WH_hww_FSR',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['PSWeight[3]', 'PSWeight[1]']) for skey in mc if skey not in ['VgS']),
    'AsLnN'   : '0',
}

nuisances['UE_CP5']  = {
    'name'    : 'CMS_WH_hww_UE',
    'skipCMS' : 1,
    'type'    : 'lnN',
    'samples' : dict((skey, '1.015') for skey in mc),
}

# Charge flip efficiency
nuisances['chargeFlipEff'] = {
    'name'    : 'CMS_whss_chargeFlipEff_2016',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['1-ttHMVA_eff_err_flip_2l', '1+ttHMVA_eff_err_flip_2l']) for skey in ['DY','ChargeFlip']),
    'cuts'    : [cut for cut in cuts if ('_ee_' in cut or '_em_' in cut)],
}

# Charge flip: uncertainty on opposite sign processes not affected by charge-flip
nuisances['chargeFlip_syst'] = {
    'name'    : 'CMS_ChargeFlip_syst',
    'type'    : 'lnN',
    'samples' : {
        'ChargeFlip' : '1.10',
    },
    'cuts'    : [cut for cut in cuts if ('_ee_' in cut or '_em_' in cut)],
}

# Top pT reweighting uncertainty

nuisances['TopPtRew'] = {
    'name'       : 'CMS_top_pT_reweighting',   # Theory uncertainty
    'kind'       : 'weight',
    'type'       : 'shape',
    'samples'    : {
        'top': ["1.", "1./Top_pTrw"]
    },
    'symmetrize' : True
}

# Vg and VgS scale uncertainty
nuisances['VgStarScale2j'] = {
    'name'    : 'CMS_hww_VgStarScale2j_2016',
    'type'    : 'lnN',
    'samples' : {
        'VgS' : '1.25'
    },
    'cuts' : [cut for cut in cuts if '2j' in cut],
}

nuisances['VgScale2j'] = {
    'name'    : 'CMS_hww_VgScale2j_2016',
    'type'    : 'lnN',
    'samples' : {
        'Vg' : '1.25'
    },
    'cuts' : [cut for cut in cuts if '2j' in cut],
}

nuisances['VgStarScale1j'] = {
    'name'    : 'CMS_hww_VgStarScale1j_2016',
    'type'    : 'lnN',
    'samples' : {
        'VgS' : '1.25'
    },
    'cuts' : [cut for cut in cuts if '1j' in cut],
}

nuisances['VgScale1j'] = {
    'name'    : 'CMS_hww_VgScale1j_2016',
    'type'    : 'lnN',
    'samples' : {
        'Vg' : '1.25'
    },
    'cuts' : [cut for cut in cuts if '1j' in cut],
}

###### pdf uncertainties
valuesggh  = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ggH', '125.09','pdf','sm')
valuesggzh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ggZH','125.09','pdf','sm')
valuesbbh  = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','bbH', '125.09','pdf','sm')

nuisances['pdf_Higgs_gg'] = {
    'name'    : 'pdf_Higgs_gg',
    'samples' : {
        'ggH_hww'  : valuesggh,
        'ggH_htt'  : valuesggh,
        'ggZH_hww' : valuesggzh,
        'bbH_hww'  : valuesbbh,
    },
    'type'    : 'lnN',
}

# For ttH, we need to use 1./values
values = str(1./float(HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ttH','125.09','pdf','sm')))

nuisances['pdf_Higgs_ttH'] = {
    'name'    : 'pdf_Higgs_ttH',
    'samples' : {
        'ttH_hww': values,
    },
    'type'    : 'lnN',
}

valuesqqh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','vbfH','125.09','pdf','sm')
valueswh  = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','WH',  '125.09','pdf','sm')
valueszh  = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ZH',  '125.09','pdf','sm')

nuisances['pdf_Higgs_qqbar'] = {
    'name'   : 'pdf_Higgs_qqbar',
    'type'   : 'lnN',
    'samples': {
        'qqH_hww'     : valuesqqh,
        'qqH_htt'     : valuesqqh,
        'WH_hww_plus' : valueswh,
        'WH_hww_minus': valueswh,
        'WH_htt_plus' : valueswh,
        'WH_htt_minus': valueswh,
        'ZH_hww'      : valueszh,
        'ZH_htt'      : valueszh
    },
}

nuisances['pdf_qqbar'] = {
    'name'    : 'pdf_qqbar',
    'type'    : 'lnN',
    'samples' : {
        'ZZ'  : '1.04', # PDF: 0.0064 / 0.1427 = 0.0448493
        'WZ'  : '1.04', # PDF: 0.0064 / 0.1427 = 0.0448493
        'Vg'  : '1.04',
        'VgS' : '1.04', # PDF: 0.0064 / 0.1427 = 0.0448493
    },
}

nuisances['pdf_gg'] = {
    'name': 'pdf_gg',
    'type': 'lnN',
    'samples': {
        'ggWW' : '1.05',
    },
}

nuisances['pdf_Higgs_gg_ACCEPT'] = {
    'name'    : 'pdf_WH_hww_Higgs_gg_ACCEPT',
    'samples' : {
        'ggH_hww'  : '1.006',
        'ggH_htt'  : '1.006',
        'ggZH_hww' : '1.006',
        'bbH_hww'  : '1.006'
    },
    'type'    : 'lnN',
}
nuisances['pdf_gg_ACCEPT'] = {
    'name'    : 'pdf_WH_hww_gg_ACCEPT',
    'samples' : {
        'ggWW' : '1.006',
    },
    'type'    : 'lnN',
}

nuisances['pdf_Higgs_qqbar_ACCEPT'] = {
    'name'    : 'pdf_WH_hww_Higgs_qqbar_ACCEPT',
    'type'    : 'lnN',
    'samples' : {
        'qqH_hww'     : '1.002',
        'qqH_htt'     : '1.002',
        'WH_hww_plus' : '1.003',
        'WH_hww_minus': '1.003',
        'WH_htt_plus' : '1.003',
        'WH_htt_minus': '1.003',
        'ZH_hww'      : '1.002',
        'ZH_htt'      : '1.002',
    },
}

nuisances['pdf_qqbar_ACCEPT'] = {
    'name'    : 'pdf_WH_hww_qqbar_ACCEPT',
    'type'    : 'lnN',
    'samples' : {
        'ZZ' : '1.001',
        'WZ' : '1.001',
    },
}

##### Renormalization & factorization scales

## Shape nuisance due to QCD scale variations for DY
## LHE scale variation weights (w_var / w_nominal)

## This should work for samples with either 8 or 9 LHE scale weights (Length$(LHEScaleWeight) == 8 or 9)
variations = ['Alt(LHEScaleWeight,0,1)', 'Alt(LHEScaleWeight,1,1)', 'Alt(LHEScaleWeight,3,1)', 'Alt(LHEScaleWeight,nLHEScaleWeight-4,1)', 'Alt(LHEScaleWeight,nLHEScaleWeight-2,1)', 'Alt(LHEScaleWeight,nLHEScaleWeight-1,1)']

# nuisances['QCDscale_V'] = {
#     'name'    : 'QCDscale_V',
#     'skipCMS' : 1,
#     'kind'    : 'weight_envelope',
#     'type'    : 'shape',
#     'samples' : {
#         'DY' : variations
#     },
#     'AsLnN'   : '0'
# }

nuisances['QCDscale_VV'] = {
    'name' : 'QCDscale_VV',
    'kind' : 'weight_envelope',
    'type' : 'shape',
    'samples' : {
        'WW'  : variations,
        'ZZ'  : variations,
        'WZ'  : variations,
        # 'Vg'  : variations, TO BE INCLUDED IN THE NEXT ITERATION!
        # 'VgS' : variations, TO BE INCLUDED IN THE NEXT ITERATION!
    }
}

nuisances['QCDscale_ggVV'] = {
    'name'    : 'QCDscale_ggVV',
    'type'    : 'lnN',
    'samples' : {
        'ggWW' : '1.15',
    },
}

#### QCD scale uncertainties for Higgs signals other than ggH

values = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','vbfH','125.09','scale','sm')

nuisances['QCDscale_qqH'] = {
    'name'    : 'QCDscale_qqH',
    'samples' : {
        'qqH_hww' : values,
        'qqH_htt' : values,
    },
    'type'    : 'lnN'
}

valueswh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','WH','125.09','scale','sm')
valueszh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ZH','125.09','scale','sm')

nuisances['QCDscale_VH'] = {
    'name'    : 'QCDscale_VH',
    'samples' : {
        'WH_hww_plus'  : valueswh,
        'WH_hww_minus' : valueswh,
        'WH_htt_plus'  : valueswh,
        'WH_htt_minus' : valueswh,
        'ZH_hww'       : valueszh,
        'ZH_htt'       : valueszh,
    },
    'type'    : 'lnN',
}

values = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ggZH','125.09','scale','sm')

nuisances['QCDscale_ggZH'] = {
    'name' : 'QCDscale_ggZH',
    'samples' : {
        'ggZH_hww' : values,
    },
    'type' : 'lnN',
}

values = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ttH','125.09','scale','sm')

nuisances['QCDscale_ttH'] = {
    'name' : 'QCDscale_ttH',
    'samples' : {
        'ttH_hww' : values,
    },
    'type' : 'lnN',
}

nuisances['QCDscale_WWewk'] = {
    'name' : 'QCDscale_WWewk',
    'samples' : {
        'WWewk' : '1.11',
    },
    'type' : 'lnN'
}

nuisances['QCDscale_qqbar_ACCEPT'] = {
    'name' : 'QCDscale_qqbar_ACCEPT',
    'type' : 'lnN',
    'samples' : {
        'qqH_hww'      : '1.003',
        'qqH_htt'      : '1.003',
        'WH_hww_plus'  : '1.010',
        'WH_hww_minus' : '1.010',
        'WH_htt_plus'  : '1.010',
        'WH_htt_minus' : '1.010',
        'ZH_hww'       : '1.015',
        'ZH_htt'       : '1.015',
    }
}

# FIXME: these come from HIG-16-042, maybe should be recomputed?
nuisances['QCDscale_gg_ACCEPT'] = {
    'name' : 'QCDscale_gg_ACCEPT',
    'samples' : {
        'ggH_htt'  : '1.012',
        'ggH_hww'  : '1.012',
        'ggZH_hww' : '1.012',
        'ggWW'     : '1.012',
    },
    'type' : 'lnN',
}

# WZ normalization from control region
nuisances['WZ2jnorm']  = {
    'name'    : 'CMS_hww_WZ3l2jnorm_2016',
    'samples' : {
        'WZ' : '1.00',
    },
    'type' : 'rateParam',
    'cuts' : [cut for cut in cuts if '2j' in cut],
}

nuisances['WZ1jnorm']  = {
    'name'    : 'CMS_hww_WZ3l1jnorm_2016',
    'samples' : {
        'WZ' : '1.00',
    },
    'type' : 'rateParam',
    'cuts' : [cut for cut in cuts if '1j' in cut],
}

# Use the following if you want to apply the automatic combine MC stat nuisances.
nuisances['stat']  = {
    'type'          : 'auto',
    'maxPoiss'      : '10',
    'includeSignal' : '0',
    'samples'       : {}
}
# nuisance ['maxPoiss']      = Number of threshold events for Poisson modelling
# nuisance ['includeSignal'] = Include MC stat nuisances on signal processes (1=True, 0=False)

for n in nuisances.values():
    n['skipCMS'] = 1
