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

mcProduction = 'Summer20UL16_106x_nAODv9_HIPM_Full2016v9'
dataReco = 'Run2016_UL2016_nAODv9_HIPM_Full2016v9'
fakeReco = dataReco
mcSteps = 'MCl1loose2016v9__MCCorr2016v9NoJERInHorn__l2tightOR2016v9'
fakeSteps = 'DATAl1loose2016v9__l2loose__fakeW'
dataSteps = 'DATAl1loose2016v9__l2loose__l2tightOR2016v9'
embedReco    = 'Embedding2016_UL2016_nAODv9_HIPM_Full2016v9'
embedSteps   = 'DATAl1loose2016v9__l2loose__l2tightOR2016v9__Embedding'

treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'
limitFiles = -1

mc_emb = [skey for skey in samples if skey != 'DATA' and skey != 'Dyveto' and not skey.startswith('Fake')]
mc = [skey for skey in mc_emb if skey != 'Dyemb']

useEmbeddedDY = True
runDYveto = True

redirector = ""
useXROOTD = False

def makeMCDirectory(var=''):
    _treeBaseDir = treeBaseDir + ''
    if useXROOTD:
        _treeBaseDir = redirector + treeBaseDir
    if var== '':
        return '/'.join([_treeBaseDir, mcProduction, mcSteps])
    else:
        return '/'.join([_treeBaseDir, mcProduction, mcSteps + '__' + var])

def makeEMBDDirectory(var=''):
    _treeBaseDir = treeBaseDir + ''
    if var== '':
        return '/'.join([_treeBaseDir, embedReco, embedSteps])
    else:
        return '/'.join([_treeBaseDir, embedReco, embedSteps + '__' + var])

    
mcDirectory = makeMCDirectory()
fakeDirectory = os.path.join(treeBaseDir, dataReco, fakeSteps)
dataDirectory = os.path.join(treeBaseDir, dataReco, dataSteps)
embedDirectory = os.path.join(treeBaseDir, embedReco, embedSteps)

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
    'samples': dict((skey, '1.010') for skey in mc if skey not in ['top', 'DY', 'WW_minnlo'])
}
nuisances['lumi_Correlated_Run2'] = {
    'name': 'lumi_13TeV_correlated',
    'type': 'lnN',
    'samples': dict((skey, '1.006') for skey in mc if skey not in ['top', 'DY', 'WW_minnlo'])
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
# 'Fake': ['abs(fakeWStatEleUp)<10 ? fakeWStatEleUp : 1.0', 'abs(fakeWStatEleUp)<10 ? fakeWStatEleDown : 1.0']
nuisances['fake_ele_stat'] = {
    'name': 'CMS_fake_stat_e_2016',
    'kind': 'weight',
    'type': 'shape',
    'cutspost' : [cut for cut in total_cuts if '_sr_RF_Signal_0j' not in cut],
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
for flavour in ['bc', 'light']:
    for corr in ['uncorrelated', 'correlated']:
        btag_syst = [f'btagSF{flavour}_up_{corr}/btagSF{flavour}', f'btagSF{flavour}_down_{corr}/btagSF{flavour}']
        if corr == 'correlated':
            name = f'CMS_btagSF{flavour}_{corr}'
        else:
            name = f'CMS_btagSF{flavour}_2016'
        nuisances[f'btagSF{flavour}{corr}'] = {
            'name': name,
            'skipCMS' : 1,
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
    'samples': dict((skey, trig_syst) for skey in mc_emb)
}

##### Electron Efficiency and energy scale

nuisances['eff_e'] = {
    'name': 'CMS_eff_e',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, ['SFweightEleUp', 'SFweightEleDown']) for skey in mc_emb),
}
nuisances['eff_ttHMVA_e'] = {
    'name'    : 'CMS_eff_ttHMVA_e',
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
nuisances['electronptembd'] = {
    'name'       : 'CMS_scale_e_2016',
    'kind'       : 'suffix',
    'type'       : 'shape',
    'mapUp'      : 'ElepTup',
    'mapDown'    : 'ElepTdo',
    'samples'    : dict((skey, ['1', '1']) for skey in ['Dyemb']),
    'folderUp'   : makeEMBDDirectory('EmbElepTup_suffix'),
    'folderDown' : makeEMBDDirectory('EmbElepTdo_suffix'),
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
nuisances['muonptembd'] = {
    'name'       : 'CMS_scale_m_2016',
    'kind'       : 'suffix',
    'type'       : 'shape',
    'mapUp'      : 'MupTup',
    'mapDown'    : 'MupTdo',
    'samples'    : dict((skey, ['1', '1']) for skey in ['Dyemb']),
    'folderUp'   : makeEMBDDirectory('EmbMupTup_suffix'),
    'folderDown' : makeEMBDDirectory('EmbMupTdo_suffix'),
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

##### Di-Tau vetoing for embedding 
if useEmbeddedDY:
    if runDYveto:
        nuisances['embedveto']  = {
            'name'  : 'CMS_embed_veto_2016',
            'kind'  : 'weight',
            'type'  : 'shape',
            'samples'  : {
                'Dyemb'    : ['1', '1'],
                'Dyveto'   : ['0.1', '-0.1'],
            }
        }

##### Pileup

nuisances['PU'] = {
    'name': 'CMS_pileup_2016',
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'DY'      : ['1.008421*(puWeightUp/puWeight)', '0.992494*(puWeightDown/puWeight)'],
        'WW'      : ['1.010428*(puWeightUp/puWeight)', '0.990400*(puWeightDown/puWeight)'],
        'WW_minnlo': ['1.010428*(puWeightUp/puWeight)', '0.990400*(puWeightDown/puWeight)'],
        'ggWW'    : ['1.012367*(puWeightUp/puWeight)', '0.988402*(puWeightDown/puWeight)'],
        'ggWW_si'    : ['1.012367*(puWeightUp/puWeight)', '0.988402*(puWeightDown/puWeight)'],
        'Vg'      : ['0.995630*(puWeightUp/puWeight)', '1.007076*(puWeightDown/puWeight)'],
        'WZ'      : ['1.002037*(puWeightUp/puWeight)', '0.997721*(puWeightDown/puWeight)'],
        'ZZ'      : ['1.006574*(puWeightUp/puWeight)', '0.993175*(puWeightDown/puWeight)'],
        'VVV'     : ['1.012827*(puWeightUp/puWeight)', '0.989623*(puWeightDown/puWeight)'],
        'top'     : ['1.009336*(puWeightUp/puWeight)', '0.991324*(puWeightDown/puWeight)'],
        'ggH_hww'   : ['1.011609*(puWeightUp/puWeight)', '0.989039*(puWeightDown/puWeight)'],
        'qqH_hww'   : ['1.011609*(puWeightUp/puWeight)', '0.989039*(puWeightDown/puWeight)'],
        'ggH_HWLWL'   : ['1.011609*(puWeightUp/puWeight)', '0.989039*(puWeightDown/puWeight)'],
        'ggH_HWTWT'   : ['1.011609*(puWeightUp/puWeight)', '0.989039*(puWeightDown/puWeight)'],
        'qqH_HWLWL'   : ['1.011609*(puWeightUp/puWeight)', '0.989039*(puWeightDown/puWeight)'],
        'qqH_HWTWT'   : ['1.011609*(puWeightUp/puWeight)', '0.989039*(puWeightDown/puWeight)'],
        'ggToWW'   : ['1.011609*(puWeightUp/puWeight)', '0.989039*(puWeightDown/puWeight)'],
        'qqToWW'   : ['1.011609*(puWeightUp/puWeight)', '0.989039*(puWeightDown/puWeight)'],
    },
    'AsLnN': '0',
}

### PU ID SF uncertainty
puid_syst = ['Jet_PUIDSF_up/Jet_PUIDSF', 'Jet_PUIDSF_down/Jet_PUIDSF']

nuisances['jetPUID'] = {
    'name': 'CMS_eff_j_PUJET_id_2016',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, puid_syst) for skey in mc)
}

##### PS

#
# As suggested by Emmanuelle, split the nuisance parameters as a function of the number of jets; in a similar behavior as it's done with the top QCD scales.
#

for ibin in ['0j','1j','2j']:
    nuisances['PS_ISR_'+ibin]  = {
        'name'    : 'PS_hww_ISR_'+ibin,
        'kind'    : 'weight',
        'type'    : 'shape',
        'samples' : dict((skey, ['PSWeight[2]', 'PSWeight[0]']) for skey in mc),
        'cutspost' : [cut for cut in total_cuts if ibin in cut],
        'AsLnN'   : '0',
    }
    nuisances['PS_FSR_'+ibin]  = {
        'name'    : 'PS_hww_FSR_'+ibin,
        'kind'    : 'weight',
        'type'    : 'shape',
        'samples' : dict((skey, ['PSWeight[3]', 'PSWeight[1]']) for skey in mc),
        'cutspost' : [cut for cut in total_cuts if ibin in cut],
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
    'name'       : 'CMS_top_pT_reweighting',   # Theory uncertainty
    'kind'       : 'weight',
    'type'       : 'shape',
    'samples'    : {
        'top': ["1.", "1./Top_pTrw"]
    },
    'symmetrize' : True
}
nuisances['WgStar'] = {
    'name'    : 'CMS_hww_WgStarScale',
    'type'    : 'lnN',
    'samples' : {
        'WgS' : '1.25'
    }
}

###### pdf uncertainties

# PDF eigenvariations for WW and top
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
            'WW_minnlo'   : pdf_variations,
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
        'ggToWW': '1.032',
        ##### Combined samples: take the largest uncertainty 
        'htt': '1.032',
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
        'qqToWW': '1.021',
        ##### Combined samples: take the largest uncertainty 
        'hww': '1.019',
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
        'ggToWW': '1.006', # Do not double count
        ##### Combined HTT samples
        'htt': '1.006',
    },
    'type': 'lnN',
}
nuisances['pdf_gg_ACCEPT'] = {
    'name': 'pdf_gg_ACCEPT',
    'samples': {
        'ggWW': '1.006',
        'ggWW_si': '1.006',
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
        'qqToWW': '1.002',
        ##### Combined HWW samples 
        'hww': '1.003',
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
        'cuts' : [cut for cut in total_cuts if ibin in cut],
        'samples'  : {
            'top' : variations,
        }
    }

nuisances['QCDscale_V'] = {
    'name': 'QCDscale_V',
    'skipCMS': 1,
    'kind'  : 'weight_envelope',
    'type': 'shape',
    'samples': {'DY': variations},
    'AsLnN': '1'
}
nuisances['QCDscale_VV'] = {
    'name' : 'QCDscale_VV',
    'kind' : 'weight_envelope',
    'type' : 'shape',
    'samples' : {
        'WW'  : variations,
        'WW_minnlo'  : variations,
        'Zg'  : variations,
        'Wg'  : variations,
        'Vg'  : variations,
        'VgS' : variations,
        'ZZ'  : variations,
        'WZ'  : variations,
        'WgS' : variations,
        'ZgS' : variations,
    }
}
nuisances['GGWWRew'] = {
    'name': 'CMS_ggWW_NLO_reweighting',
    'kind'       : 'weight',
    'type'       : 'shape',
    'samples'    : {
        'ggWW': ["KFactor_ggWW_Up/KFactor_ggWW", "KFactor_ggWW_Down/KFactor_ggWW"],
        'ggWW_si': ["KFactor_ggWW_Up/KFactor_ggWW", "KFactor_ggWW_Down/KFactor_ggWW"],
        'ggToWW': ["KFactor_ggWW_Up/KFactor_ggWW", "KFactor_ggWW_Down/KFactor_ggWW"],
    },
}
#nuisances['QCDscale_ggVV'] = {
#    'name': 'QCDscale_ggVV',
#    'type': 'lnN',
#    'samples': {
#        'ggWW': '1.15',
#    },
#}
"""
############ 
############ QCD Scales for ggToWW  |  Take into account the amount of ggWW and ggH that contributes to ggToWW and then transmit to the nuisance
############

nuisances['QCDscale_ggVV_hww2l2v_13TeV_ss_Inc'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.6530056905705897*(1.15-1.0))
    },
    'cuts' : [cut for cut in total_cuts if cut=='hww2l2v_13TeV_ss_Inc'],
}
nuisances['QCDscale_ggVV_hww2l2v_13TeV_ss_0j'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.6763336750988823*(1.15-1.0))
    },
    'cuts' : [cut for cut in total_cuts if cut=='hww2l2v_13TeV_ss_0j'],
}
nuisances['QCDscale_ggVV_hww2l2v_13TeV_ss_1j'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.6314762507095808*(1.15-1.0))
    },
    'cuts' : [cut for cut in total_cuts if cut=='hww2l2v_13TeV_ss_1j'],
}
nuisances['QCDscale_ggVV_hww2l2v_13TeV_ss_2j'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.6070641714023718*(1.15-1.0))
    },
    'cuts' : [cut for cut in total_cuts if cut=='hww2l2v_13TeV_ss_2j'],
}
nuisances['QCDscale_ggVV_hww2l2v_13TeV_sr_RF02_0j_pt2gt20'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.24021273659962533*(1.15-1.0))
    },
    'cuts' : [cut for cut in total_cuts if cut=='hww2l2v_13TeV_sr_RF02_0j_pt2gt20'],
}
nuisances['QCDscale_ggVV_hww2l2v_13TeV_sr_RF02_0j_pt2lt20'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.15559456331125232*(1.15-1.0))
    },
    'cuts' : [cut for cut in total_cuts if cut=='hww2l2v_13TeV_sr_RF02_0j_pt2lt20'],
}
nuisances['QCDscale_ggVV_hww2l2v_13TeV_sr_RF02_1j_pt2gt20'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.233747975556614*(1.15-1.0))
    },
    'cuts' : [cut for cut in total_cuts if cut=='hww2l2v_13TeV_sr_RF02_1j_pt2gt20'],
}
nuisances['QCDscale_ggVV_hww2l2v_13TeV_sr_RF02_1j_pt2lt20'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.17596811683183483*(1.15-1.0))
    },
    'cuts' : [cut for cut in total_cuts if cut=='hww2l2v_13TeV_sr_RF02_1j_pt2lt20'],
}
nuisances['QCDscale_ggVV_hww2l2v_13TeV_sr_RF02_2j_tot'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.24801709026141847*(1.15-1.0))
    },
    'cuts' : [cut for cut in total_cuts if cut=='hww2l2v_13TeV_sr_RF02_2j_tot'],
}
nuisances['QCDscale_ggVV_hww2l2v_13TeV_sr_RF02_2j'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.1907919892123816*(1.15-1.0))
    },
    'cuts' : [cut for cut in total_cuts if cut=='hww2l2v_13TeV_sr_RF02_2j'],
}
nuisances['QCDscale_ggVV_hww2l2v_13TeV_sr_RF02_2j_vbf'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.35257558715948445*(1.15-1.0))
    },
    'cuts' : [cut for cut in total_cuts if cut=='hww2l2v_13TeV_sr_RF02_2j_vbf'],
}
nuisances['QCDscale_ggVV_hww2l2v_13TeV_sr_0j_pt2gt20'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.6388733373312082*(1.15-1.0))
    },
    'cuts' : [cut for cut in total_cuts if cut=='hww2l2v_13TeV_sr_0j_pt2gt20'],
}
nuisances['QCDscale_ggVV_hww2l2v_13TeV_sr_0j_pt2lt20'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.2793533756590918*(1.15-1.0))
    },
    'cuts' : [cut for cut in total_cuts if cut=='hww2l2v_13TeV_sr_0j_pt2lt20'],
}
nuisances['QCDscale_ggVV_hww2l2v_13TeV_sr_1j_pt2gt20'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.6197084211452352*(1.15-1.0))
    },
    'cuts' : [cut for cut in total_cuts if cut=='hww2l2v_13TeV_sr_1j_pt2gt20'],
}
nuisances['QCDscale_ggVV_hww2l2v_13TeV_sr_1j_pt2lt20'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.3552745487841686*(1.15-1.0))
    },
    'cuts' : [cut for cut in total_cuts if cut=='hww2l2v_13TeV_sr_1j_pt2lt20'],
}
nuisances['QCDscale_ggVV_hww2l2v_13TeV_sr_2j'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.5638198657496979*(1.15-1.0))
    },
    'cuts' : [cut for cut in total_cuts if cut=='hww2l2v_13TeV_sr_2j'],
}
nuisances['QCDscale_ggVV_hww2l2v_13TeV_sr_2j_vbf'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.6055180553275765*(1.15-1.0))
    },
    'cuts' : [cut for cut in total_cuts if cut=='hww2l2v_13TeV_sr_2j_vbf'],
}
nuisances['QCDscale_ggVV_hww2l2v_13TeV_top_0j'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.5767139262568738*(1.15-1.0))
    },
    'cuts' : [cut for cut in total_cuts if cut=='hww2l2v_13TeV_top_0j'],
}
nuisances['QCDscale_ggVV_hww2l2v_13TeV_top_1j'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.5553727746541869*(1.15-1.0))
    },
    'cuts' : [cut for cut in total_cuts if cut=='hww2l2v_13TeV_top_1j'],
}
nuisances['QCDscale_ggVV_hww2l2v_13TeV_top_2j'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.5428522224224136*(1.15-1.0))
    },
    'cuts' : [cut for cut in total_cuts if cut=='hww2l2v_13TeV_top_2j'],
}
nuisances['QCDscale_ggVV_hww2l2v_13TeV_dytt_0j'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.5988817392308123*(1.15-1.0))
    },
    'cuts' : [cut for cut in total_cuts if cut=='hww2l2v_13TeV_dytt_0j'],
}
nuisances['QCDscale_ggVV_hww2l2v_13TeV_dytt_1j'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.47306386143698753*(1.15-1.0))
    },
    'cuts' : [cut for cut in total_cuts if cut=='hww2l2v_13TeV_dytt_1j'],
}
nuisances['QCDscale_ggVV_hww2l2v_13TeV_dytt_2j'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggToWW': str(1+0.4231617724925962*(1.15-1.0))
    },
    'cuts' : [cut for cut in total_cuts if cut=='hww2l2v_13TeV_dytt_2j'],
}
"""
## -----------------------------------------------

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
    'cuts' : [cut for cut in total_cuts if '0j' in cut],
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
    'cuts' : [cut for cut in total_cuts if '0j' in cut],
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
    'cuts' : [cut for cut in total_cuts if '1j' in cut],
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
    'cuts' : [cut for cut in total_cuts if '1j' in cut],
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
    'cuts' : [cut for cut in total_cuts if '2j' in cut],
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
    'cuts' : [cut for cut in total_cuts if '2j' in cut],
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
          'qqToWW': updown,
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
        #### Take the largest QCD Unc. for combined HTT samples  
        'htt': '0.997/1.004',
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
        'ZH_htt': '0.994/1.005',
        #### Take the largest QCD Unc. for combined HWW samples
        'hww': '0.993/1.005',
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
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'WWewk': ['LHEScaleWeight[0]', 'LHEScaleWeight[2]'],
        'WWewk_si': ['LHEScaleWeight[0]', 'LHEScaleWeight[2]'],
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
        #### Take the largest QCD Unc. for combined HWW samples
        'hww': '1.015',
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
        'ggWW_si': '1.012',
        #### Take the largest QCD Unc. for combined HTT samples  
        'htt': '1.012',
    },
    'type': 'lnN',
}

# Uncertainty on SR/CR ratio
nuisances['CRSR_accept_DY'] = {
    'name': 'CMS_hww_CRSR_accept_DY',
    'type': 'lnN',
    'samples': {'Dyemb': '1.02'},
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
                   'Dyemb' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts0j
              }
nuisances['DYnorm1j']  = {
               'name'  : 'CMS_hww_DYttnorm1j',
               'samples'  : {
                   'Dyemb' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts1j
              }
nuisances['DYnorm2j']  = {
                 'name'  : 'CMS_hww_DYttnorm2j',
                 'samples'  : {
                   'Dyemb' : '1.00',
                     },
                 'type'  : 'rateParam',
                 'cuts'  : cuts_2j
                }
nuisances['WWnorm0j']  = {
               'name'  : 'CMS_hww_WWnorm0j',
               'samples'  : {
                   #'WW' : '1.00',
                   'WW_minnlo' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts0j
              }
nuisances['WWnorm1j']  = {
               'name'  : 'CMS_hww_WWnorm1j',
               'samples'  : {
                   #'WW' : '1.00',
                   'WW_minnlo' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts1j
              }
nuisances['WWnorm2j']  = {
               'name'  : 'CMS_hww_WWnorm2j',
               'samples'  : {
                   #'WW' : '1.00',
                   'WW_minnlo' : '1.00',
                   },
               'type'  : 'rateParam',
	       'cuts': cuts_2j,
              }
#nuisances['WWnormVBF']  = {
#               'name'  : 'CMS_hww_WWnormVBF',
#	       'samples'  : {
#                   #'WW' : '1.00',
#                   'WW_minnlo' : '1.00',
#                   },
#               'type'  : 'rateParam',
#               'cuts': cuts_vbf,
#              }
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

### Fakes --------------- 
nuisances['Fakenorm0j']  = {
               'name'  : 'CMS_hww_Fakenorm0j',
               'samples'  : {
                   'Fake' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts0j
              }
nuisances['Fakenorm1j']  = {
               'name'  : 'CMS_hww_Fakenorm1j',
               'samples'  : {
                   'Fake' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts1j
              }
nuisances['Fakenorm2j']  = {
	       'name'  : 'CMS_hww_Fakenorm2j',
	       'samples'  : {
                   'Fake' : '1.00',
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
