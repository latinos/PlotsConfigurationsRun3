mcProduction = 'Summer20UL17_106x_nAODv9_Full2017v9'
dataReco = 'Run2017_UL2017_nAODv9_Full2017v9'
mcSteps = 'MCl1loose2017v9__MCCorr2017v9NoJERInHorn__l2tightOR2017v9'
fakeSteps = 'DATAl1loose2017v9__l2loose__fakeW'
dataSteps = 'DATAl1loose2017v9__l2loose__l2tightOR2017v9'

treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'
#limitFiles = -1

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

nuisances = {}

nuisances['lumi_Uncorrelated'] = {
    'name': 'lumi_13TeV_2017',
    'type': 'lnN',
    'samples': dict((skey, '1.02') for skey in mc if skey not in ['WW', 'top', 'dytt'])
}

nuisances['lumi_correlated'] = {
    'name': 'lumi_13TeV_correlated',
    'type': 'lnN',
    'samples': dict((skey, '1.009') for skey in mc if skey not in ['WW', 'top', 'dytt'])
}

nuisances['lumi_correlated_1718'] = {
    'name': 'lumi_13TeV_correlated_1718',
    'type': 'lnN',
    'samples': dict((skey, '1.006') for skey in mc if skey not in ['WW', 'top', 'dytt'])
}

#### FAKES

nuisances['fake_syst_e'] = {
    'name': 'fake_syst_e',
    'type': 'lnN',
    'samples': {
        'Fake_e': '1.3'
    },
}

nuisances['fake_syst_m'] = {
    'name': 'fake_syst_m',
    'type': 'lnN',
    'samples': {
        'Fake_m': '1.3'
    },
}

nuisances['fake_ele'] = {
    'name': 'fake_e_2017',
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake': ['fakeWEleUp', 'fakeWEleDown'],
    }
}

nuisances['fake_ele_stat'] = {
    'name': 'fake_stat_e_2017',
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake': ['fakeWStatEleUp', 'fakeWStatEleDown']
    }
}

nuisances['fake_mu'] = {
    'name': 'fake_m_2017',
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake': ['fakeWMuUp', 'fakeWMuDown'],
    }
}

nuisances['fake_mu_stat'] = {
    'name': 'fake_stat_m_2017',
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake': ['fakeWStatMuUp', 'fakeWStatMuDown'],
    }
}

### B-tagger
for shift in ['jes', 'lf', 'hf', 'hfstats1', 'hfstats2', 'lfstats1', 'lfstats2', 'cferr1', 'cferr2']:
    btag_syst = ['(btagSF%sup)/(btagSF)' % shift, '(btagSF%sdown)/(btagSF)' % shift]

    name = 'btag_%s' % shift
    if 'stats' in shift:
        name += '_2017'

    nuisances['btag_shape_%s' % shift] = {
        'name': name,
        'kind': 'weight',
        'type': 'shape',
        'samples': dict((skey, btag_syst) for skey in mc),
    }

##### Trigger Efficiency
trig_syst = ['TriggerSFWeight_2l_u/TriggerSFWeight_2l', 'TriggerSFWeight_2l_d/TriggerSFWeight_2l']

nuisances['trigg'] = {
    'name': 'eff_hwwtrigger_2017',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, trig_syst) for skey in mc)
}

##### Electron Efficiency and energy scale

nuisances['eff_e'] = {
    'name': 'eff_e_2017',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, ['SFweightEleUp', 'SFweightEleDown']) for skey in mc)
}

nuisances['electronpt'] = {
    'name': 'scale_e_2017',
    'kind': 'suffix',
    'type': 'shape',
    'mapUp': 'ElepTup',
    'mapDown': 'ElepTdo',
    'samples': dict((skey, ['1', '1']) for skey in mc),
    'folderUp': makeMCDirectory('ElepTup_suffix'),
    'folderDown': makeMCDirectory('ElepTdo_suffix'),
    'AsLnN': '0'
}

##### Muon Efficiency and energy scale

nuisances['eff_m'] = {
    'name': 'eff_m_2017',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, ['SFweightMuUp', 'SFweightMuDown']) for skey in mc)
}

nuisances['muonpt'] = {
    'name': 'scale_m_2017',
    'kind': 'suffix',
    'type': 'shape',
    'mapUp': 'MupTup',
    'mapDown': 'MupTdo',
    'samples': dict((skey, ['1', '1']) for skey in mc),
    'folderUp': makeMCDirectory('MupTup_suffix'),
    'folderDown': makeMCDirectory('MupTdo_suffix'),
    'AsLnN': '0'
}

### PU ID SF uncertainty
puid_syst = ['Jet_PUIDSF_up/Jet_PUIDSF', 'Jet_PUIDSF_down/Jet_PUIDSF']

nuisances['jetPUID'] = {
    'name': 'PUID_2017',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, puid_syst) for skey in mc)
}

##### Jet energy scale
jes_systs = ['JESAbsolute','JESAbsolute_2017','JESBBEC1','JESBBEC1_2017','JESEC2','JESEC2_2017','JESFlavorQCD','JESHF','JESHF_2017','JESRelativeBal','JESRelativeSample_2017']

for js in jes_systs:
    # Split source, applied to jets and MET
    nuisances[js] = {
        'name': 'scale_'+js,
        'kind': 'suffix',
        'type': 'shape',
        'mapUp': js+'up',
        'mapDown': js+'do',
        'samples': dict((skey, ['1', '1']) for skey in mc),
        'folderUp': makeMCDirectory('RDF__JESup_suffix'),
        'folderDown': makeMCDirectory('RDF__JESdo_suffix'),
        'AsLnN': '0'
    }

##### MET energy scale
nuisances['met'] = {
    'name': 'CMS_scale_met_2017',
    'skipCMS' : 1,
    'kind': 'suffix',
    'type': 'shape',
    'mapUp': 'METup',
    'mapDown': 'METdo',
    'samples': dict((skey, ['1', '1']) for skey in mc),
    'folderUp': makeMCDirectory('METup_suffix'),
    'folderDown': makeMCDirectory('METdo_suffix'),
    'AsLnN': '0'
}

##### Jet energy resolution
nuisances['JER'] = {
    'name': 'CMS_res_j_2017',
    'skipCMS' : 1,
    'kind': 'suffix',
    'type': 'shape',
    'mapUp': 'JERup',
    'mapDown': 'JERdo',
    'samples': dict((skey, ['1', '1']) for skey in mc),
    'folderUp': makeMCDirectory('JERup_suffix'),
    'folderDown': makeMCDirectory('JERdo_suffix'),
    'AsLnN': '0'
}

# Uncertainty on SR/CR ratio
nuisances['CRSR_accept_DY'] = {
    'name': 'hww_CRSR_accept_DY',
    'type': 'lnN',
    'samples': {'DY': '1.02'},
    'cuts': [cut for cut in cuts2j if 'DY' in cut],
}

# Uncertainty on SR/CR ratio
nuisances['CRSR_accept_top'] = {
    'name': 'hww_CRSR_accept_top',
    'type': 'lnN',
    'samples': {'top': '1.01'},
    'cuts': [cut for cut in cuts2j if 'top' in cut],
}

##### Pileup

nuisances['PU'] = {
    'name': 'CMS_PU_2017',
    'skipCMS' : 1,
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'top'               : ['puWeightUp/puWeight',   'puWeightDown/puWeight'],
        'dytt'              : ['puWeightUp/puWeight',   'puWeightDown/puWeight'],
        'WWjj_QCD'          : ['puWeightUp/puWeight',   'puWeightDown/puWeight'],
        'ggWW'              : ['puWeightUp/puWeight',   'puWeightDown/puWeight'],
        'WWewk_CMWWW_LL'    : ['puWeightUp/puWeight',   'puWeightDown/puWeight'],
        'WWewk_CMWWW_LT'    : ['puWeightUp/puWeight',   'puWeightDown/puWeight'],
        'WWewk_CMWWW_TL'    : ['puWeightUp/puWeight',   'puWeightDown/puWeight'],
        'WWewk_CMWWW_TT'    : ['puWeightUp/puWeight',   'puWeightDown/puWeight'],
        'WWewk_LL'          : ['puWeightUp/puWeight',   'puWeightDown/puWeight'],
        'WWewk_LT'          : ['puWeightUp/puWeight',   'puWeightDown/puWeight'],
        'WWewk_TL'          : ['puWeightUp/puWeight',   'puWeightDown/puWeight'],
        'WWewk_TT'          : ['puWeightUp/puWeight',   'puWeightDown/puWeight'],
    },
    'AsLnN': '0',
}

##### PS

nuisances['PS_ISR']  = {
    'name'    : 'PS_ISR',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['PSWeight[2]', 'PSWeight[0]']) for skey in mc if 'WWewk' not in skey),
    'AsLnN'   : '0',
}

nuisances['PS_FSR']  = {
    'name'    : 'PS_FSR',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['PSWeight[3]', 'PSWeight[1]']) for skey in mc if 'WWewk' not in skey),
    'AsLnN'   : '0',
}

nuisances['PS_ISR_WWewk']  = {
    'name'    : 'PS_ISR',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['PSWeight[2]*NormTHU_' + skey + '_PS_ISR_Up', 'PSWeight[0]*NormTHU_' + skey + '_PS_ISR_Do']) for skey in mc if skey in ['WWewk_CMWW_LL', 'WWewk_CMWW_LT', 'WWewk_CMWW_TL', 'WWewk_CMWW_TT', 'WWewk_LL', 'WWewk_LT', 'WWewk_TL', 'WWewk_TT']),
    'AsLnN'   : '0',
}

nuisances['PS_FSR_WWewk']  = {
    'name'    : 'PS_FSR',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['PSWeight[3]*NormTHU_' + skey + '_PS_FSR_Up', 'PSWeight[1]*NormTHU_' + skey + '_PS_FSR_Do']) for skey in mc if skey in ['WWewk_CMWW_LL', 'WWewk_CMWW_LT', 'WWewk_CMWW_TL', 'WWewk_CMWW_TT', 'WWewk_LL', 'WWewk_LT', 'WWewk_TL', 'WWewk_TT']),
    'AsLnN'   : '0',
}

##### Renormalization & factorization scales

## Shape nuisance due to QCD scale variations
# LHE scale variation weights (w_var / w_nominal)

## This should work for samples with either 8 or 9 LHE scale weights (nLHEScaleWeight == 8 or 9)
variations = ['LHEScaleWeight[0]',
              'LHEScaleWeight[1]',
              'LHEScaleWeight[3]',
              'LHEScaleWeight[nLHEScaleWeight - 4]',
              'LHEScaleWeight[nLHEScaleWeight - 2]',
              'LHEScaleWeight[nLHEScaleWeight - 1]']

VBSvariations = ['LHEScaleWeight[2]', 'LHEScaleWeight[0]'] # LO samples include only variations on muF scale [2]: mu_R = 2.0, [0]: mu_R = 0.5

## QCD scale nuisances for top are decorrelated for each RECO jet bin: the QCD scale is different for different jet multiplicities so it doesn't make sense to correlate them

nuisances['QCDscale_WWewk'] = {
    'name': 'QCDscale_WWewk',
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'WWewk_CMWW_LL': ['LHEScaleWeight[0]*NormTHU_WWewk_CMWW_LL_QCDscale_WWewk_Up', 'LHEScaleWeight[2]*NormTHU_WWewk_CMWW_LL_QCDscale_WWewk_Do'],
        'WWewk_CMWW_LT': ['LHEScaleWeight[0]*NormTHU_WWewk_CMWW_LT_QCDscale_WWewk_Up', 'LHEScaleWeight[2]*NormTHU_WWewk_CMWW_LT_QCDscale_WWewk_Do'],
        'WWewk_CMWW_TL': ['LHEScaleWeight[0]*NormTHU_WWewk_CMWW_TL_QCDscale_WWewk_Up', 'LHEScaleWeight[2]*NormTHU_WWewk_CMWW_TL_QCDscale_WWewk_Do'],
        'WWewk_CMWW_TT': ['LHEScaleWeight[0]*NormTHU_WWewk_CMWW_TT_QCDscale_WWewk_Up', 'LHEScaleWeight[2]*NormTHU_WWewk_CMWW_TT_QCDscale_WWewk_Do'],
        'WWewk_LL': ['LHEScaleWeight[0]*NormTHU_WWewk_LL_QCDscale_WWewk_Up', 'LHEScaleWeight[2]*NormTHU_WWewk_LL_QCDscale_WWewk_Do'],
        'WWewk_LT': ['LHEScaleWeight[0]*NormTHU_WWewk_LT_QCDscale_WWewk_Up', 'LHEScaleWeight[2]*NormTHU_WWewk_LT_QCDscale_WWewk_Do'],
        'WWewk_TL': ['LHEScaleWeight[0]*NormTHU_WWewk_TL_QCDscale_WWewk_Up', 'LHEScaleWeight[2]*NormTHU_WWewk_TL_QCDscale_WWewk_Do'],
        'WWewk_TT': ['LHEScaleWeight[0]*NormTHU_WWewk_TT_QCDscale_WWewk_Up', 'LHEScaleWeight[2]*NormTHU_WWewk_TT_QCDscale_WWewk_Do'],
    }
}

nuisances['QCDscale_top_2j']  = {
    'name'  : 'QCDscale_top_2j',
    'kind'  : 'weight_envelope',
    'type'  : 'shape',
    'samples'  : {
       'top' : variations,
    }
}

nuisances['QCDscale_WW_2j']  = {
    'name'  : 'QCDscale_WW_2j',
    'kind'  : 'weight_envelope',
    'type'  : 'shape',
    'samples'  : {
       'WWjj_QCD' : variations,
    }
}

nuisances['QCDscale_V'] = {
    'name': 'QCDscale_V',
    'skipCMS': 1,
    'kind': 'weight_envelope',
    'type': 'shape',
    'samples': {
       'dytt' : variations,
    },
}

# nuisances['QCDscale_VV'] = {
#     'name': 'QCDscale_VV',
#     'kind': 'weight_envelope',
#     'type': 'shape',
#     'samples': {
#         'Vg': variations,
#         'VZ': variations,
#         'VgS': variations
#     }
# }

nuisances['QCDscale_ggVV'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {
        'ggWW': '1.15',
    },
}

###### pdf uncertainties
pdf_variations_WWewk_CMWW_LL = ['LHEPdfWeight[' + str(pdf) + ']*NormTHU_WWewk_CMWW_LL_pdf_WWewk_' + str(pdf) for pdf in range(1,100)]
pdf_variations_WWewk_CMWW_LT = ['LHEPdfWeight[' + str(pdf) + ']*NormTHU_WWewk_CMWW_LT_pdf_WWewk_' + str(pdf) for pdf in range(1,100)]
pdf_variations_WWewk_CMWW_TL = ['LHEPdfWeight[' + str(pdf) + ']*NormTHU_WWewk_CMWW_TL_pdf_WWewk_' + str(pdf) for pdf in range(1,100)]
pdf_variations_WWewk_CMWW_TT = ['LHEPdfWeight[' + str(pdf) + ']*NormTHU_WWewk_CMWW_TT_pdf_WWewk_' + str(pdf) for pdf in range(1,100)]
pdf_variations_WWewk_LL = ['LHEPdfWeight[' + str(pdf) + ']*NormTHU_WWewk_LL_pdf_WWewk_' + str(pdf) for pdf in range(1,100)]
pdf_variations_WWewk_LT = ['LHEPdfWeight[' + str(pdf) + ']*NormTHU_WWewk_LT_pdf_WWewk_' + str(pdf) for pdf in range(1,100)]
pdf_variations_WWewk_TL = ['LHEPdfWeight[' + str(pdf) + ']*NormTHU_WWewk_TL_pdf_WWewk_' + str(pdf) for pdf in range(1,100)]
pdf_variations_WWewk_TT = ['LHEPdfWeight[' + str(pdf) + ']*NormTHU_WWewk_TT_pdf_WWewk_' + str(pdf) for pdf in range(1,100)]
nuisances['pdf_WWewk'] = {
    'name': 'pdf_WWewk',
    'kind': 'weight_rms',
    'type': 'shape',
    'samples': {
        'WWewk_CMWW_LL': pdf_variations_WWewk_CMWW_LL,
        'WWewk_CMWW_LT': pdf_variations_WWewk_CMWW_LT,
        'WWewk_CMWW_TL': pdf_variations_WWewk_CMWW_TL,
        'WWewk_CMWW_TT': pdf_variations_WWewk_CMWW_TT,
        'WWewk_LL': pdf_variations_WWewk_LL,
        'WWewk_LT': pdf_variations_WWewk_LT,
        'WWewk_TL': pdf_variations_WWewk_TL,
        'WWewk_TT': pdf_variations_WWewk_TT
    },
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

nuisances['DYttnorm2j']  = {
               'name'  : 'CMS_hww_DYttnorm2j',
               'skipCMS' : 1,
               'samples'  : {
                   'dytt' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts2j
              }

nuisances['WWnorm2j']  = {
               'name'  : 'CMS_hww_WWnorm2j',
               'skipCMS' : 1,
               'samples'  : {
                   'WWjj_QCD' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts2j
              }

nuisances['ggWWnorm2j']  = {
               'name'  : 'CMS_hww_WWnorm2j',
               'skipCMS' : 1,
               'samples'  : {
                   'ggWW' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts2j
              }

nuisances['Topnorm2j']  = {
               'name'  : 'CMS_hww_Topnorm2j',
               'skipCMS' : 1,
               'samples'  : {
                   'top' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts2j
              }


