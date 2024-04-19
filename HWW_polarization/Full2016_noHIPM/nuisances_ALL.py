# nuisances

#nuisances = {}

# name of samples here must match keys in samples.py 

# imported from samples.py:
# samples, treeBaseDir, mcProduction, mcSteps
# imported from cuts.py
# cuts

nuisances = {}

#from mkShapesRDF.lib.HiggsXSection import HiggsXSection
#from HiggsXSection import HiggsXSection
#HiggsXS = HiggsXSection()

mcProduction = 'Summer20UL16_106x_nAODv9_noHIPM_Full2016v9'
dataReco     = 'Run2016_UL2016_nAODv9_noHIPM_Full2016v9'
mcSteps      = 'MCl1loose2016v9__MCCorr2016v9NoJERInHorn__l2tightOR2016v9'
fakeSteps    = 'DATAl1loose2016v9__l2loose__fakeW'
dataSteps    = 'DATAl1loose2016v9__l2loose__l2tightOR2016v9'

treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'
limitFiles = -1

useXROOTD = False

mc = [skey for skey in samples if skey not in ('Fake', 'DATA')]

redirector = ""

def makeMCDirectory(var=''):
    _treeBaseDir = treeBaseDir + ''
    if useXROOTD:
        _treeBaseDir = redirector + treeBaseDir
    if var== '':
        return '/'.join([_treeBaseDir, mcProduction, mcSteps])
    else:
        return '/'.join([_treeBaseDir, mcProduction, mcSteps + '__' + var])


mcDirectory = makeMCDirectory()
fakeDirectory = os.path.join(treeBaseDir, dataReco, fakeSteps)
dataDirectory = os.path.join(treeBaseDir, dataReco, dataSteps)


cuts0j = []
cuts1j = []
cuts2j = []
cuts_vbf = []
cuts_2j = []
total_cuts = []
for k in cuts:
    for cat in cuts[k]['categories']:
        total_cuts.append(k+'_'+cat)
        if '0j' in cat:
            cuts0j.append(k+'_'+cat)
        elif '1j' in cat:
            cuts1j.append(k+'_'+cat)
        elif '2j' in cat and '2j_vbf' not in cat:
            cuts2j.append(k+'_'+cat)
            cuts_2j.append(k+'_'+cat)
        elif '2j_vbf' in cat:
            cuts_vbf.append(k+'_'+cat)
            cuts_2j.append(k+'_'+cat)
        else:
            print('WARNING: name of category does not contain either 0j,1j,2j')
            
################################ EXPERIMENTAL UNCERTAINTIES  #################################

#### Luminosity

nuisances['lumi_Uncorrelated'] = {
    'name': 'lumi_13TeV_2016',
    'type': 'lnN',
    'samples': dict((skey, '1.010') for skey in mc if skey not in ['WZ'])
}
nuisances['lumi_Correlated_Run2'] = {
    'name': 'lumi_13TeV_correlated',
    'type': 'lnN',
    'samples': dict((skey, '1.006') for skey in mc if skey not in ['WZ'])
}


#### FAKES

nuisances['fake_syst'] = {
    'name': 'CMS_fake_syst',
    'type': 'lnN',
    'samples': {
        'Fake': '1.3'
    },
}
nuisances['fake_ele'] = {
    'name': 'CMS_fake_e_2016',
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake': ['fakeWEleUp', 'fakeWEleDown'],
    },
}
nuisances['fake_ele_stat'] = {
    'name': 'CMS_fake_stat_e_2016',
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake': ['fakeWStatEleUp', 'fakeWStatEleDown']
    },
}
nuisances['fake_mu'] = {
    'name': 'CMS_fake_m_2016',
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake': ['fakeWMuUp', 'fakeWMuDown'],
    },
}
nuisances['fake_mu_stat'] = {
    'name': 'CMS_fake_stat_m_2016',
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake': ['fakeWStatMuUp', 'fakeWStatMuDown'],
    },
}

##### B-tagger

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


##### Trigger Scale Factors                                                                                                                                                                                

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
    'samples': dict((skey, ['SFweightEleUp', 'SFweightEleDown']) for skey in mc),
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
    'name': 'CMS_eff_m_2016',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, ['SFweightMuUp', 'SFweightMuDown']) for skey in mc),
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
jes_systs = ['JESAbsolute','JESAbsolute_2016','JESBBEC1','JESBBEC1_2016','JESEC2','JESEC2_2016','JESFlavorQCD','JESHF','JESHF_2016','JESRelativeBal','JESRelativeSample_2016']

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
      'AsLnN'     : '0'
  }

##### Jet energy resolution
nuisances['JER'] = {
    'name'       : 'CMS_res_j_2016',
    'kind'       : 'suffix',
    'type'       : 'shape',
    'mapUp'      : 'JERup',
    'mapDown'    : 'JERdo',
    'samples'    : dict((skey, ['1', '1']) for skey in mc),
    'folderUp'   : makeMCDirectory('JERup_suffix'),
    'folderDown' : makeMCDirectory('JERdo_suffix'),
    'AsLnN'      : '0'
}

##### MET energy scale
# metUp.PuppiMET_pt_METup
nuisances['met'] = {
    'name'       : 'CMS_scale_met_2016',
    'kind'       : 'suffix',
    'type'       : 'shape',
    'mapUp'      : 'METup',
    'mapDown'    : 'METdo',
    'samples'    : dict((skey, ['1', '1']) for skey in mc),
    'folderUp'   : makeMCDirectory('METup_suffix'),
    'folderDown' : makeMCDirectory('METdo_suffix'),
    'AsLnN'      : '0'
}

##### Pileup

nuisances['PU'] = {
    'name'    : 'CMS_pileup_2016',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : {
        'DY'      : ['1.000489*(puWeightUp/puWeight)', '0.998828*(puWeightDown/puWeight)'],
        'WW'      : ['1.007152*(puWeightUp/puWeight)', '0.993194*(puWeightDown/puWeight)'],
        'ggWW'    : ['1.006460*(puWeightUp/puWeight)', '0.993661*(puWeightDown/puWeight)'],
        'Vg'      : ['1.004694*(puWeightUp/puWeight)', '0.998294*(puWeightDown/puWeight)'],
        'WZ'      : ['1.003158*(puWeightUp/puWeight)', '0.997747*(puWeightDown/puWeight)'],
        'ZZ'      : ['1.000801*(puWeightUp/puWeight)', '0.999199*(puWeightDown/puWeight)'],
        'VVV'     : ['0.996144*(puWeightUp/puWeight)', '1.005616*(puWeightDown/puWeight)'],
        'top'     : ['1.004374*(puWeightUp/puWeight)', '0.995684*(puWeightDown/puWeight)'],
        'ggH_hww'   : ['1.006460*(puWeightUp/puWeight)', '0.993559*(puWeightDown/puWeight)'],
        'qqH_hww'   : ['1.006460*(puWeightUp/puWeight)', '0.993559*(puWeightDown/puWeight)'],
        'ggH_HWLWL'   : ['1.006460*(puWeightUp/puWeight)', '0.993559*(puWeightDown/puWeight)'],
        'ggH_HWTWT'   : ['1.006460*(puWeightUp/puWeight)', '0.993559*(puWeightDown/puWeight)'],
        'qqH_HWLWL'   : ['1.006460*(puWeightUp/puWeight)', '0.993559*(puWeightDown/puWeight)'],
        'qqH_HWTWT'   : ['1.006460*(puWeightUp/puWeight)', '0.993559*(puWeightDown/puWeight)'],
        'ggToWW'    : ['1.006460*(puWeightUp/puWeight)', '0.993661*(puWeightDown/puWeight)'],
        'qqToWW'    : ['1.006460*(puWeightUp/puWeight)', '0.993661*(puWeightDown/puWeight)'],
    },
    'AsLnN'   : '0',
}

### PU ID SF uncertainty
puid_syst = ['Jet_PUIDSF_up/Jet_PUIDSF', 'Jet_PUIDSF_down/Jet_PUIDSF']

nuisances['jetPUID'] = {
    'name': 'CMS_PUID_2016',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, puid_syst) for skey in mc)
}

##### PS

nuisances['PS_ISR']  = {
    'name'    : 'PS_hww_ISR',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['PSWeight[2]', 'PSWeight[0]']) for skey in mc),
    'AsLnN'   : '0',
}
nuisances['PS_FSR']  = {
    'name'    : 'PS_hww_FSR',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['PSWeight[3]', 'PSWeight[1]']) for skey in mc),
    'AsLnN'   : '0',
}
nuisances['UE_CP5']  = {
    'name'    : 'CMS_hww_UE',
    'skipCMS' : 1,
    'type'    : 'lnN',
    'samples' : dict((skey, '1.015') for skey in mc),
}

####### Generic "cross section uncertainties"

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

nuisances['TopPtRew'] = {
    'name': 'CMS_top_pT_reweighting',   # Theory uncertainty
    'kind': 'weight',
    'type': 'shape',
    'samples': {'top': ["1.", "1./Top_pTrw"]},
    'symmetrize': True
}
nuisances['WgStar'] = {
    'name': 'CMS_hww_WgStarScale',
    'type': 'lnN',
    'samples': {
        'WgS': '1.25'
    }
}

###### pdf uncertainties

for i in range(1,101):
    # LHE pdf variation weights (w_var / w_nominal) for LHA IDs 306000 - 306102 

    pdf_variations = ["abs(LHEPdfWeight[0])>0.01 ? LHEPdfWeight[%d]/LHEPdfWeight[0] : 1.0" %i, "abs(LHEPdfWeight[0])>0.01 ? 2. - LHEPdfWeight[%d]/LHEPdfWeight[0] : 1.0" %i ]

    nuisances['pdf_WW_eigen'+str(i)]  = {
        'name'  : 'CMS_hww_pdf_WW_eigen'+str(i),
        'skipCMS' : 1,
        'kind'  : 'weight',
        'type'  : 'shape',
        'samples'  : {
            'WW'   : pdf_variations,
        },
    }
    nuisances['pdf_top_eigen'+str(i)]  = {
        'name'  : 'CMS_hww_pdf_top_eigen'+str(i),
        'skipCMS' : 1,
        'kind'  : 'weight',
        'type'  : 'shape',
        'samples'  : {
            'top'   : pdf_variations,
	},
    }
    
#valuesggh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ggH','125.09','pdf','sm')
#valuesggzh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ggZH','125.09','pdf','sm')
#valuesbbh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','bbH','125.09','pdf','sm')
nuisances['pdf_Higgs_gg'] = {
    'name': 'pdf_Higgs_gg',
    'samples': {
        'ggH_hww': '1.032',
        'ggH_htt': '1.032',
        'ggZH_hww': '1.024',
        'bbH_hww': '1.0',
        'ggH_HWLWL': '1.032',
        'ggH_HWTWT': '1.032',
        'ggH_HWW_Int': '1.032',
        'ggH_HWW_TTInt': '1.032',
        'ggToWW': '1.032'
    },
    'type': 'lnN',
}
#values = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ttH','125.09','pdf','sm')
nuisances['pdf_Higgs_ttH'] = {
    'name': 'pdf_Higgs_ttH',
    'samples': {
        'ttH_hww': '1.036'
    },
    'type': 'lnN',
}
#valuesqqh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','vbfH','125.09','pdf','sm')
#valueswh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','WH','125.09','pdf','sm')
#valueszh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ZH','125.09','pdf','sm')
nuisances['pdf_Higgs_qqbar'] = {
    'name': 'pdf_Higgs_qqbar',
    'type': 'lnN',
    'samples': {
        'qqH_hww': '1.021',
        'qqH_htt': '1.021',
        'WH_hww': '1.019',
        'WH_htt': '1.019',
        'ZH_hww': '1.019',
        'ZH_htt': '1.019',
        'qqH_HWLWL': '1.021',
        'qqH_HWTWT': '1.021',
        'qqH_HWW_Int': '1.021',
        'qqH_HWW_TTInt': '1.021',
        'qqToWW': '1.021'
    },
}
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
        'bbH_hww': '1.006',
        'ggH_HWLWL': '1.006',
        'ggH_HWTWT': '1.006',
        'ggH_HWW_Int': '1.006',
        'ggH_HWW_TTInt': '1.006',
        'ggToWW': '1.006' ## Do not double count with pdf_gg_ACCEPT
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
    'type': 'lnN',
    'samples': {
        'qqH_hww': '1.002',
        'qqH_htt': '1.002',
        'WH_hww': '1.003',
        'WH_htt': '1.003',
        'ZH_hww': '1.002',
        'ZH_htt': '1.002',
        'qqH_HWLWL': '1.002',
        'qqH_HWTWT': '1.002',
        'qqH_HWW_Int': '1.002',
        'qqH_HWW_TTInt': '1.002',
        'qqToWW': '1.002'
    },
}
nuisances['pdf_qqbar_ACCEPT'] = {
    'name': 'pdf_qqbar_ACCEPT',
    'type': 'lnN',
    'samples': {
        'VZ': '1.001',
    },
}

##### Renormalization & factorization scales

## Shape nuisance due to QCD scale variations for DY
# LHE scale variation weights (w_var / w_nominal)

## This should work for samples with either 8 or 9 LHE scale weights (Length$(LHEScaleWeight) == 8 or 9)
variations = ['Alt(LHEScaleWeight,0,1)', 'Alt(LHEScaleWeight,1,1)', 'Alt(LHEScaleWeight,3,1)', 'Alt(LHEScaleWeight,nLHEScaleWeight-4,1)', 'Alt(LHEScaleWeight,nLHEScaleWeight-2,1)', 'Alt(LHEScaleWeight,nLHEScaleWeight-1,1)']

for ibin in ['0j','1j','2j']:
    nuisances['QCDscale_top_'+ibin]  = {
        'name'  : 'QCDscale_top_'+ibin,
        'kind'  : 'weight',
        'type'  : 'shape',
        'AsLnN': '0',
        'cutspost' : [cut for cut in total_cuts if ibin in cut],
        'samples'  : {
            'top' : variations,
        }
    }

nuisances['QCDscale_V'] = {
    'name': 'QCDscale_V',
    'skipCMS': 1,
    'kind'  : 'weight',
    'type': 'shape',
    'samples': {'DY': variations},
    'AsLnN': '1'
}
nuisances['QCDscale_VV'] = {
    'name' : 'QCDscale_VV',
    'kind' : 'weight',
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
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggWW': '1.15',
    },
}

############
############ QCD Scales for ggToWW  |  Take into account the amount of ggWW and ggH that contributes to ggToWW and then transmit to the nuisance
############


# Signals region ----- 
# 0-jet category 2016 noHIPM: 17.1% ggWW;  82.9% ggH 
# 1-jet category 2016 noHIPM: 17.2% ggWW;  82.8% ggH
# 2-jet category 2016 noHIPM: 13.3% ggWW;  86.7% ggH
# vbf   category 2016 noHIPM: 24.3% ggWW;  75.7% ggH
#
# WW Control region ----
# 0-jet category 2016 noHIPM: 88.4% ggWW;  11.6% ggH
# 1-jet category 2016 noHIPM: 85.5% ggWW;  14.5% ggH
# 2-jet category 2016 noHIPM: 82.0% ggWW;  18.0% ggH
# vbf   category 2016 noHIPM: 90.8% ggWW;   9.2% ggH 
#
# 0-jet category 2016 noHIPM: 41.6% ggWW;  58.4% ggH
# 1-jet category 2016 noHIPM: 38.0% ggWW;  42.0% ggH
# 2-jet category 2016 noHIPM: 39.0% ggWW;  61.0% ggH
#
# DY Control region ----
# 0-jet category 2016 noHIPM: 43.2% ggWW;  56.8% ggH
# 1-jet category 2016 noHIPM: 30.9% ggWW;  69.1% ggH 
# 2-jet category 2016 noHIPM: 29.1% ggWW;  70.9% ggH

nuisances['QCDscale_ggVV_sr_0j'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.171*(1.15-1.0))
    },
    'cuts' : [cut for cut in cuts0j if 'Signal_0j' in cut],
}
nuisances['QCDscale_ggVV_sr_1j'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.172*(1.15-1.0))
    },
    'cuts' : [cut for cut in cuts1j if 'Signal_1j' in cut],
}
nuisances['QCDscale_ggVV_sr_2j'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.133*(1.15-1.0))
    },
    'cuts' : [cut for cut in cuts2j if 'Signal_2j' in cut],
}
nuisances['QCDscale_ggVV_sr_vbf'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.243*(1.15-1.0))
    },
    'cuts': [cut for cut in cuts_vbf if 'Signal_2j_vbf' in cut],
}
##
nuisances['QCDscale_ggVV_ww_0j'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.884*(1.15-1.0))
    },
    'cuts' : [cut for cut in cuts0j if 'bkg_0j' in cut],
}
nuisances['QCDscale_ggVV_ww_1j'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.855*(1.15-1.0))
    },
    'cuts' : [cut for cut in cuts1j if 'bkg_1j' in cut],
}
nuisances['QCDscale_ggVV_ww_2j'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.820*(1.15-1.0))
    },
    'cuts' : [cut for cut in cuts2j if 'bkg_2j' in cut],
}
nuisances['QCDscale_ggVV_ww_vbf'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.908*(1.15-1.0))
    },
    'cuts': [cut for cut in cuts_vbf if 'bkg_2j_vbf' in cut],
}
##
nuisances['QCDscale_ggVV_top_0j'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.416*(1.15-1.0))
    },
    'cuts' : [cut for cut in cuts0j if 'top_0j' in cut],
}
nuisances['QCDscale_ggVV_top_1j'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.38*(1.15-1.0))
    },
    'cuts' : [cut for cut in cuts1j if 'top_1j' in cut],
}
nuisances['QCDscale_ggVV_top_2j'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.39*(1.15-1.0))
    },
    'cuts' : [cut for cut in cuts2j if 'top_2j' in cut],
}
##
nuisances['QCDscale_ggVV_dytt_0j'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.432*(1.15-1.0))
    },
    'cuts' : [cut for cut in cuts0j if 'dytt_0j' in cut],
}
nuisances['QCDscale_ggVV_dytt_1j'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.309*(1.15-1.0))
    },
    'cuts' : [cut for cut in cuts1j if 'dytt_1j' in cut],
}
nuisances['QCDscale_ggVV_dytt_2j'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.291*(1.15-1.0))
    },
    'cuts' : [cut for cut in cuts2j if 'dytt_2j' in cut],
}
#### ----------------------------------------------

##### Renormalization & factorization scales
nuisances['WWresum0j']  = {
    'name'  : 'CMS_hww_WWresum_0j',
    'skipCMS' : 1,
    'kind'  : 'weight',
    'type'  : 'shape',
    'samples'  : {
        'WW'   : ['nllW_Rup/nllW', 'nllW_Rdown/nllW'],
    },
    'cutspost' : [cut for cut in total_cuts if '0j' in cut],
}

nuisances['WWqscale0j']  = {
    'name'  : 'CMS_hww_WWqscale_0j',
    'skipCMS' : 1,
    'kind'  : 'weight',
    'type'  : 'shape',
    'samples'  : {
        'WW'   : ['nllW_Qup/nllW', 'nllW_Qdown/nllW'],
    },
    'cutspost' : [cut for cut in total_cuts if '0j' in cut],
}


nuisances['WWresum1j']  = {
    'name'  : 'CMS_hww_WWresum_1j',
    'skipCMS' : 1,
    'kind'  : 'weight',
    'type'  : 'shape',
    'samples'  : {
        'WW'   : ['nllW_Rup/nllW', 'nllW_Rdown/nllW'],
    },
    'cutspost' : [cut for cut in total_cuts if '1j' in cut],
}

nuisances['WWqscale1j']  = {
    'name'  : 'CMS_hww_WWqscale_1j',
    'skipCMS' : 1,
    'kind'  : 'weight',
    'type'  : 'shape',
    'samples'  : {
        'WW'   : ['nllW_Qup/nllW', 'nllW_Qdown/nllW'],
    },
    'cutspost' : [cut for cut in total_cuts if '1j' in cut],
}

nuisances['WWresum2j']  = {
    'name'  : 'CMS_hww_WWresum_2j',
    'skipCMS' : 1,
    'kind'  : 'weight',
    'type'  : 'shape',
    'samples'  : {
        'WW'   : ['nllW_Rup/nllW', 'nllW_Rdown/nllW'],
    },
    'cutspost' : [cut for cut in total_cuts if '2j' in cut],
}

nuisances['WWqscale2j']  = {
    'name'  : 'CMS_hww_WWqscale_2j',
    'skipCMS' : 1,
    'kind'  : 'weight',
    'type'  : 'shape',
    'samples'  : {
        'WW'   : ['nllW_Qup/nllW', 'nllW_Qdown/nllW'],
    },
    'cutspost' : [cut for cut in total_cuts if '2j' in cut],
}


# Theory uncertainty for ggH
#
#
#   THU_ggH_Mu, THU_ggH_Res, THU_ggH_Mig01, THU_ggH_Mig12, THU_ggH_VBF2j, THU_ggH_VBF3j, THU_ggH_PT60, THU_ggH_PT120, THU_ggH_qmtop
#
#   see https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsWG/SignalModelingTools

thus = [
    ('THU_ggH_Mu', 'ggH_mu_2'),
    ('THU_ggH_Res', 'ggH_res_2'),
    ('THU_ggH_Mig01', 'ggH_mig01_2'),
    ('THU_ggH_Mig12', 'ggH_mig12_2'),
    ('THU_ggH_VBF2j', 'ggH_VBF2j_2'),
    ('THU_ggH_VBF3j', 'ggH_VBF3j_2'),
    ('THU_ggH_PT60', 'ggH_pT60_2'),
    ('THU_ggH_PT120', 'ggH_pT120_2'),
    ('THU_ggH_qmtop', 'ggH_qmtop_2')
]

for name, vname in thus:
    updown = [vname, '2.-%s' % vname]
    
    nuisances[name] = {
        'name': name,
        'skipCMS': 1,
        'kind': 'weight',
        'type': 'shape',
        'samples': {
          'ggH_hww': updown,
          'ggH_HWLWL': updown,
          'ggH_HWTWT': updown,
          'ggH_HWW_Int': updown,
          'ggH_HWW_TTInt': updown,
          'ggToWW': updown,
        }
    }

# Theory uncertainty for qqH 
#
#
#   see https://gitlab.cern.ch/LHCHIGGSXS/LHCHXSWG2/STXS/VBF-Uncertainties/-/blob/master/qq2Hqq_uncert_scheme.cpp

thusQQH = [
  ("THU_qqH_YIELD","qqH_YIELD"),
  ("THU_qqH_PTH200","qqH_PTH200"),
  ("THU_qqH_Mjj60","qqH_Mjj60"),
  ("THU_qqH_Mjj120","qqH_Mjj120"),
  ("THU_qqH_Mjj350","qqH_Mjj350"),
  ("THU_qqH_Mjj700","qqH_Mjj700"),
  ("THU_qqH_Mjj1000","qqH_Mjj1000"),
  ("THU_qqH_Mjj1500","qqH_Mjj1500"),
  ("THU_qqH_PTH25","qqH_PTH25"),
  ("THU_qqH_JET01","qqH_JET01"),
  ("THU_qqH_EWK","qqH_EWK"),
]

for name, vname in thusQQH:
    updown = [vname, '2.-%s' % vname]
    
    nuisances[name] = {
        'name': name,
        'skipCMS': 1,
        'kind': 'weight',
        'type': 'shape',
        'samples': {
          'qqH_hww': updown,
          'qqH_HWLWL': updown,
          'qqH_HWTWT': updown,
          'qqH_HWW_Int': updown,
          'qqH_HWW_TTInt': updown,
          'qqToWW': updown
        }
    }

#### QCD scale uncertainties for Higgs signals other than ggH

#values = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','vbfH','125.09','scale','sm')
nuisances['QCDscale_qqH'] = {
    'name': 'QCDscale_qqH', 
    'samples': {
        'qqH_hww': '0.997/1.004',
        'qqH_HWLWL': '0.997/1.004',
        'qqH_HWTWT': '0.997/1.004',
        'qqH_HWW_Int': '0.997/1.004',
        'qqH_HWW_TTInt': '0.997/1.004',
        'qqH_htt': '0.997/1.004',
        'qqToWW': '0.997/1.004',
    },
    'type': 'lnN'
}
#valueswh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','WH','125.09','scale','sm')
#valueszh = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ZH','125.09','scale','sm')
nuisances['QCDscale_VH'] = {
    'name': 'QCDscale_VH', 
    'samples': {
        'WH_hww': '0.993/1.005',
        'WH_htt': '0.993/1.005',
        'ZH_hww': '0.994/1.005',
        'ZH_htt': '0.994/1.005'
    },
    'type': 'lnN',
}
#values = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ggZH','125.09','scale','sm')
nuisances['QCDscale_ggZH'] = {
    'name': 'QCDscale_ggZH', 
    'samples': {
        'ggZH_hww': '0.811/1.251'
    },
    'type': 'lnN',
}
#values = HiggsXS.GetHiggsProdXSNP('YR4','13TeV','ttH','125.09','scale','sm')
nuisances['QCDscale_ttH'] = {
    'name': 'QCDscale_ttH',
    'samples': {
        'ttH_hww': '0.908/1.058'
    },
    'type': 'lnN',
}
nuisances['QCDscale_WWewk'] = {
    'name': 'QCDscale_WWewk',
    #'kind': 'weight_envelope',
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'WWewk': ['LHEScaleWeight[0]', 'LHEScaleWeight[2]'],
        'qqToWW': ['LHEScaleWeight[0]', 'LHEScaleWeight[2]'],
    }
}
nuisances['QCDscale_qqbar_ACCEPT'] = {
    'name': 'QCDscale_qqbar_ACCEPT',
    'type': 'lnN',
    'samples': {
        'qqH_hww': '1.003',
        'qqH_HWLWL': '1.003',
        'qqH_HWTWT': '1.003',
        'qqH_HWW_Int': '1.003',
        'qqH_HWW_TTInt': '1.003',
        'qqH_htt': '1.003',
        'WH_hww': '1.010',
        'WH_htt': '1.010',
        'ZH_hww': '1.015',
        'ZH_htt': '1.015',
        'qqToWW': '1.003',
    }    
}
nuisances['QCDscale_gg_ACCEPT'] = {
    'name': 'QCDscale_gg_ACCEPT',
    'samples': {
        'ggH_htt': '1.012',
        'ggH_hww': '1.012',
        'ggH_HWLWL': '1.012',
        'ggH_HWTWT': '1.012',
        'ggH_HWW_TT': '1.012',
        'ggH_HWW_TTInt': '1.012',
        'ggZH_hww': '1.012',
        'ggWW': '1.012',
        'ggToWW': '1.012',
    },
    'type': 'lnN',
}

# Uncertainty on SR/CR ratio
nuisances['CRSR_accept_DY'] = {
    'name': 'CMS_hww_CRSR_accept_DY',
    'type': 'lnN',
    'samples': {'DY': '1.02'},
    'cuts': [cut for cut in total_cuts if '_dytt_' in cut],
    'cutspost' : [cut for cut in total_cuts if '_dytt_' in cut],
}
# Uncertainty on SR/CR ratio
nuisances['CRSR_accept_top'] = {
    'name': 'CMS_hww_CRSR_accept_top',
    'type': 'lnN',
    'samples': {'top': '1.01'},
    'cuts': [cut for cut in total_cuts if '_top_' in cut],
    'cutspost' : [cut for cut in total_cuts if '_top_' in cut],
}
# Uncertainty on SR/CR ratio
nuisances['CRSR_accept_WW'] = {
    'name': 'CMS_hww_CRSR_accept_WW',
    'type': 'lnN',
    'samples': {'WW': '1.01'},
    'cuts': [cut for cut in total_cuts if '_sr_RF_bkg_' in cut],
    'cutspost' : [cut for cut in total_cuts if '_sr_RF_bkg_' in cut],
}

##rate parameters

nuisances['DYnorm0j']  = {
               'name'  : 'CMS_hww_DYttnorm0j',
               'samples'  : {
                   'DY' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts0j
              }
nuisances['DYnorm1j']  = {
               'name'  : 'CMS_hww_DYttnorm1j',
               'samples'  : {
                   'DY' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts1j
              }
nuisances['DYnorm2j']  = {
                 'name'  : 'CMS_hww_DYttnorm2j',
                 'samples'  : {
                   'DY' : '1.00',
                     },
                 'type'  : 'rateParam',
                 'cuts'  : cuts_2j
                }
nuisances['WWnorm0j']  = {
               'name'  : 'CMS_hww_WWnorm0j',
               'samples'  : {
                   'WW' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts0j
              }
nuisances['WWnorm1j']  = {
               'name'  : 'CMS_hww_WWnorm1j',
               'samples'  : {
                   'WW' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts1j
              }
nuisances['WWnorm2j']  = {
               'name'  : 'CMS_hww_WWnorm2j',
               'samples'  : {
                   'WW' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts': cuts2j,
              }
nuisances['WWnormVBF']  = {
               'name'  : 'CMS_hww_WWnormVBF',
               'samples'  : {
                   'WW' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts': cuts_vbf,
              }
nuisances['Topnorm0j']  = {
               'name'  : 'CMS_hww_Topnorm0j',
               'samples'  : {
                   'top' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts0j
              }
nuisances['Topnorm1j']  = {
               'name'  : 'CMS_hww_Topnorm1j',
               'samples'  : {
                   'top' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts1j
              }
nuisances['Topnorm2j']  = {
               'name'  : 'CMS_hww_Topnorm2j',
               'samples'  : {
                   'top' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts_2j
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

'''
for n in nuisances.values():
    n['skipCMS'] = 1

print(' '.join(nuis['name'] for nname, nuis in nuisances.items() if nname not in ('lumi', 'stat')))
'''
