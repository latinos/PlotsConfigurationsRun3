
mcProduction = 'Summer22_130x_nAODv12_Full2022v12'
mcSteps = 'MCl2loose2022v12__MCCorr2022v12JetScaling__l2tight' 
dataReco = 'Run2022_ReReco_nAODv12_Full2022v12'
fakeSteps = 'DATAl2loose2022v12__l2loose'
dataSteps = 'DATAl2loose2022v12__l2loose'

treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'
limitFiles = -1

mc = [skey for skey in samples if skey not in ('Fake', 'DATA')]

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



mcDirectory = makeMCDirectory()
fakeDirectory = os.path.join(treeBaseDir, dataReco, fakeSteps)
dataDirectory = os.path.join(treeBaseDir, dataReco, dataSteps)
print(treeBaseDir)

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

nuisances = {}

################################ EXPERIMENTAL UNCERTAINTIES  #################################

nuisances['JER'] = {
    'name': 'CMS_res_j_2022',
    'skipCMS' : 1,
    'kind': 'suffix',
    'type': 'shape',
    'mapUp': 'jerup',
    'mapDown': 'jerdo',
    #'separator': '__',
    'samples': dict((skey, ['1', '1']) for skey in mc),
    'folderUp': makeMCDirectory('jerup_suffix'),
    'folderDown': makeMCDirectory('jerdo_suffix'),
    'AsLnN': '0'
}

jes_systs    = ["Absolute", "Absolute_2022", "FlavorQCD", "BBEC1", "EC2", "HF", "BBEC1_2022", "EC2_2022", "RelativeBal", "RelativeSample_2022", "HF_2022"] # Reduced set of 11 uncertainties
#jes_systs = ['jesTotal']

for js in jes_systs:
    
    nuisances[js] = {
        'name'      : 'CMS_scale_j_' + js,
        'skipCMS' : 1,
        'kind'      : 'suffix',
        'type'      : 'shape',
        'mapUp'     : 'jesRegroed_' + js + 'up',
        'mapDown'   : 'jesRegroed_' + js + 'do',
        'samples'   : dict((skey, ['1', '1']) for skey in mc),
        'folderUp'  : makeMCDirectory('jesRegroed_' + js + 'up_suffix'),
        'folderDown': makeMCDirectory('jesRegroed_' + js + 'do_suffix'),
        'AsLnN'     : '0'
    }

nuisances['MET'] = {
    'name': 'CMS_scale_met_2022',
    'skipCMS' : 1,
    'kind': 'suffix',
    'type': 'shape',
    'mapUp': 'unclustEnup',
    'mapDown': 'unclustEndo',
    #'separator': '__',
    'samples': dict((skey, ['1', '1']) for skey in mc),
    'folderUp': makeMCDirectory('unclustEnup_suffix'),
    'folderDown': makeMCDirectory('unclustEndo_suffix'),
    'AsLnN': '0'
}

##### Lepton scale
nuisances['lepscale'] = {
    'name': 'CMS_lepscale_2022',
    'skipCMS' : 1,
    'kind': 'suffix',
    'type': 'shape',
    'mapUp': 'leptonScaleup',
    'mapDown': 'leptonScaledo',
    #'separator': '__',
    'samples': dict((skey, ['1', '1']) for skey in mc),
    'folderUp': makeMCDirectory('leptonScaleup_suffix'),
    'folderDown': makeMCDirectory('leptonScaledo_suffix'),
    'AsLnN': '0'
}
##### Lepton resolution
nuisances['lepres'] = {
    'name': 'CMS_lepres_2022',
    'skipCMS' : 1,
    'kind': 'suffix',
    'type': 'shape',
    'mapUp': 'leptonResolutionup',
    'mapDown': 'leptonResolutiondo',
    #'separator': '__',
    'samples': dict((skey, ['1', '1']) for skey in mc),
    'folderUp': makeMCDirectory('leptonResolutionup_suffix'),
    'folderDown': makeMCDirectory('leptonResolutiondo_suffix'),
    'AsLnN': '0'
}

## B-tagger
#Fixed BTV SF variations
for flavour in ['bc', 'light']:
    for corr in ['uncorrelated', 'correlated']:
        btag_syst = [f'btagSF{flavour}_up_{corr}/btagSF{flavour}', f'btagSF{flavour}_down_{corr}/btagSF{flavour}']
        if corr == 'correlated':
            name = f'CMS_btagSF{flavour}_{corr}'
        else:
            name = f'CMS_btagSF{flavour}_2022'
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
    'name': 'CMS_eff_hwwtrigger_2022',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, trig_syst) for skey in mc)
}

##### Electron Efficiency and energy scale

nuisances['eff_e'] = {
    'name': 'CMS_eff_e_2022',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, ['SFweightEleUp', 'SFweightEleDown']) for skey in mc),
}

##### Muon Efficiency and energy scale

nuisances['eff_m'] = {
    'name': 'CMS_eff_m_2022',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, ['SFweightMuUp', 'SFweightMuDown']) for skey in mc),
}


nuisances['PU'] = {
    'name': 'CMS_pileup_2022',
    'skipCMS'    : 1,
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, ['puWeightUp/puWeight', 'puWeightDown/puWeight']) for skey in mc),
    'AsLnN'   : '0'
}      

##### PS

nuisances['PS_ISR']  = {
    'name'    : 'ps_isr',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['PSWeight[2]', 'PSWeight[0]']) for skey in mc),
    'AsLnN'   : '0',
}
nuisances['PS_FSR']  = {
    'name'    : 'ps_fsr',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['PSWeight[3]', 'PSWeight[1]']) for skey in mc),
    'AsLnN'   : '0',
}

nuisances['UE_CP5']  = {
    'name'    : 'UEPS',
    'type'    : 'lnN',
    'samples' : dict((skey, '1.015') for skey in mc),
}

##### pdf uncertainties
pdf_variations = ["LHEPdfWeight[%d]" %i for i in range(1,101)] # Float_t LHE pdf variation weights (w_var / w_nominal) for LHA IDs  320901 - 321000
nuisances['pdf_WW']  = {
    'name'  : 'CMS_pdf_WW',
    'skipCMS' : 1,
    'kind'  : 'weight_rms',
    'type'  : 'shape',
    'AsLnN': '0',
    'samples'  : {
        'WW'   : pdf_variations,
    },
}

nuisances['pdf_top']  = {
    'name'  : 'CMS_pdf_top',
    'skipCMS' : 1,
    'kind'  : 'weight_rms',
    'type'  : 'shape',
    'AsLnN': '0',
    'samples'  : {
        'Top'   : pdf_variations,
    },
}

nuisances['pdf_ggH']  = {
    'name'  : 'CMS_pdf_ggH',
    'skipCMS' : 1,
    'kind'  : 'weight_rms',
    'type'  : 'shape',
    'AsLnN': '0',
    'samples'  : {
        'ggH_hww'   : pdf_variations,
    },
}

nuisances['pdf_qqH']  = {
    'name'  : 'CMS_pdf_qqH',
    'skipCMS' : 1,
    'kind'  : 'weight_rms',
    'type'  : 'shape',
    'AsLnN': '0',
    'samples'  : {
        'qqH_hww'   : pdf_variations,
    },
}

nuisances['pdf_qqbar'] = {
    'name': 'pdf_qqbar',
    'type': 'lnN',
    'samples': {
        'VZ': '1.04',
        'Vg': '1.04',
        'VgS': '1.04', # PDF: 0.0064 / 0.1427 = 0.0448493
    },
}


## This should work for samples with either 8 or 9 LHE scale weights (Length$(LHEScaleWeight) == 8 or 9)
variations = ['Alt(LHEScaleWeight,0,1)',
              'Alt(LHEScaleWeight,1,1)',
              'Alt(LHEScaleWeight,3,1)',
              'Alt(LHEScaleWeight,nLHEScaleWeight-4,1)',
              'Alt(LHEScaleWeight,nLHEScaleWeight-2,1)',
              'Alt(LHEScaleWeight,nLHEScaleWeight-1,1)']

nuisances['QCDscale_top']  = {
    'name'  : 'QCDscale_ttbar',
    'kind'  : 'weight_envelope',
    'type'  : 'shape',
    'samples'  : {'top' : variations}
}

nuisances['QCDscale_DY'] = {
    'name': 'QCDscale_DY',
    'kind'  : 'weight_envelope',
    'type': 'shape',
    'samples': {'DY': variations}
}

nuisances['QCDscale_VV'] = {
    'name' : 'QCDscale_VV',
    'kind' : 'weight_envelope',
    'type' : 'shape',
    'samples' : {'WW'  : variations}
}

nuisances['QCDscale_ggWW'] = {
    'name': 'QCDscale_ggWW',
    'type': 'lnN',
    'samples': {'ggWW': '1.15'},
}

nuisances['QCDscale_ggH'] = {
    'name' : 'QCDscale_ggH',
    'kind' : 'weight_envelope',
    'type' : 'shape',
    'samples' : {'ggH_hww'  : variations}
}

nuisances['QCDscale_qqH'] = {
    'name' : 'QCDscale_qqH',
    'kind' : 'weight_envelope',
    'type' : 'shape',
    'samples' : {'qqH_hww'  : variations}
}

##### FAKES

nuisances['fake_syst_e'] = {
    'name': 'CMS_fake_syst_e',
    'skipCMS': 1,
    'type': 'lnN',
    'samples': {
        'Fake_e': '1.3'
    },
}

nuisances['fake_syst_m'] = {
    'name': 'CMS_fake_syst_m',
    'skipCMS': 1,
    'type': 'lnN',
    'samples': {
        'Fake_m': '1.3'
    },
}

nuisances['fake_ele'] = {
    'name': 'CMS_fake_e_2022',
    'skipCMS': 1,
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake_e': ['fakeWEleUp', 'fakeWEleDown'],
    }
}

nuisances['fake_ele_stat'] = {
    'name': 'CMS_fake_stat_e_2022',
    'skipCMS': 1,
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake_e': ['fakeWStatEleUp', 'fakeWStatEleDown']
    }
}

nuisances['fake_mu'] = {
    'name': 'CMS_fake_m_2022',
    'skipCMS': 1,
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake_m': ['fakeWMuUp', 'fakeWMuDown'],
    }
}

nuisances['fake_mu_stat'] = {
    'name': 'CMS_fake_stat_m_2022',
    'skipCMS': 1,
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake_m': ['fakeWStatMuUp', 'fakeWStatMuDown'],
    }
}

nuisances['lumi_2022'] = {
    'name'    : 'lumi_2022',
    'type'    : 'lnN',
    'samples' : dict((skey, '1.014') for skey in mc)
}

##rate parameters

nuisances['DYnorm']  = {
    'name'  : 'CMS_hww_DYnorm2j_VBF_DF_2022',
    'skipCMS': 1,
    'type'  : 'rateParam',
    'samples'  : {'DY' : '1.00' },
}

nuisances['WWnorm'] = {
    'name'   : 'CMS_hww_WWnorm2j_VBF_DF_2022',
    'skipCMS': 1,
    'type'   : 'rateParam',
    'samples': {
        'WW'   : '1.00',
    },
}

nuisances['ggWWnorm'] = {
    'name'   : 'CMS_hww_WWnorm2j_VBF_DF_2022',
    'skipCMS': 1,
    'type'   : 'rateParam',
    'samples': {
        'ggWW'   : '1.00',
    },
}

nuisances['topnorm']  = {
    'name'  : 'CMS_hww_topnorm2j_VBF_DF_2022',
    'skipCMS': 1,
    'type'  : 'rateParam',
    'samples'  : {'top' : '1.00' },
}

autoStats = True
if autoStats:
    ## Use the following if you want to apply the automatic combine MC stat nuisances.
    nuisances['stat'] = {
        'type': 'auto',
        'maxPoiss': '10',
        'includeSignal': '0',
        #  nuisance ['maxPoiss'] =  Number of threshold events for Poisson modelling
        #  nuisance ['includeSignal'] =  Include MC stat nuisances on signal processes (1=True, 0=False)
        'samples': {}
    }
