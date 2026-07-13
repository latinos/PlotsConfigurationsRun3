nuisances = {}

mc     = [skey for skey in samples if skey not in ('Fake', 'DATA')]
mc_emb = [skey for skey in samples if skey not in ('Fake', 'DATA')]

################################ EXPERIMENTAL UNCERTAINTIES  #################################

for year in ['2022', '2022EE', '2023', '2023BPix', '2024']:

    ### jes ###
    jes_systs    = ["Absolute", f"Absolute_{year}", "FlavorQCD", "BBEC1", "EC2", "HF", f"BBEC1_{year}", "EC2_2024", "RelativeBal", f"RelativeSample_{year}", f"HF_{year}"] # Reduced set of 11 uncertainties
    for js in jes_systs:
        
        nuisances[js] = {
            'name'      : 'CMS_scale_j_' + js,
            'skipCMS' : 1,
            'kind'      : 'suffix',
            'type'      : 'shape',
            'mapUp'     : 'jesRegroed_' + js + 'up',
            'mapDown'   : 'jesRegroed_' + js + 'do',
            'samples'   : dict((skey, ['1', '1']) for skey in mc),
            'AsLnN'     : '0'
        }

    ### jer ###
    nuisances[f'JER_{year}'] = {
        'name': f'CMS_res_j_{year}',
        'skipCMS' : 1,
        'kind': 'suffix',
        'type': 'shape',
        'mapUp': 'jerup',
        'mapDown': 'jerdo',
        'samples': dict((skey, ['1', '1']) for skey in mc),
        'AsLnN': '0'
    }

    ### met ###
    nuisances[f'MET_{year}'] = {
        'name': f'CMS_scale_met_{year}',
        'skipCMS' : 1,
        'kind': 'suffix',
        'type': 'shape',
        'mapUp': 'unclustEnup',
        'mapDown': 'unclustEndo',
        'samples': dict((skey, ['1', '1']) for skey in mc),
        'AsLnN': '0'
    }

    ### lep scale ###
    nuisances[f'lepscale_{year}'] = {
        'name': f'CMS_lepscale_{year}',
        'skipCMS' : 1,
        'kind': 'suffix',
        'type': 'shape',
        'mapUp': 'leptonScaleup',
        'mapDown': 'leptonScaledo',
        'samples': dict((skey, ['1', '1']) for skey in mc),
        'AsLnN': '0'
    }

    ### lep res ###
    nuisances[f'lepres_{year}'] = {
        'name': f'CMS_lepres_{year}',
        'skipCMS' : 1,
        'kind': 'suffix',
        'type': 'shape',
        'mapUp': 'leptonResolutionup',
        'mapDown': 'leptonResolutiondo',
        'samples': dict((skey, ['1', '1']) for skey in mc),
        'AsLnN': '0'
    }

    ### btag ###
    for flavour in ['bc', 'light']:
        for corr in ['uncorrelated', 'correlated']:
            btag_syst = [f'btagSF{flavour}_up_{corr}/btagSF{flavour}', f'btagSF{flavour}_down_{corr}/btagSF{flavour}']
            if corr == 'correlated':
                name = f'CMS_btagSF{flavour}_{corr}'
            else:
                name = f'CMS_btagSF{flavour}_{year}'
            nuisances[f'btagSF{flavour}{corr}'] = {
                'name': name,
                'skipCMS' : 1,
                'kind': 'weight',
                'type': 'shape',
                'samples': dict((skey, btag_syst) for skey in mc),
            }
    
    ### trig ###
    trig_syst = ['TriggerSFWeight_2l_u/TriggerSFWeight_2l', 'TriggerSFWeight_2l_d/TriggerSFWeight_2l']
    nuisances[f'trigg_{year}'] = {
        'name': f'CMS_eff_hwwtrigger_{year}',
        'kind': 'weight',
        'type': 'shape',
        'samples': dict((skey, trig_syst) for skey in mc)
    }

    ### effe ###
    nuisances[f'eff_e_{year}'] = {
        'name': f'CMS_eff_e_{year}',
        'kind': 'weight',
        'type': 'shape',
        'samples': dict((skey, ['SFweightEleUp', 'SFweightEleDown']) for skey in mc),
    }

    ### effm ###
    nuisances[f'eff_m_{year}'] = {
        'name': f'CMS_eff_m_{year}',
        'kind': 'weight',
        'type': 'shape',
        'samples': dict((skey, ['SFweightMuUp', 'SFweightMuDown']) for skey in mc),
    }

    ### pu ###
    nuisances[f'PU_{year}'] = {
        'name': f'CMS_pileup_{year}',
        'skipCMS'    : 1,
        'kind': 'weight',
        'type': 'shape',
        'samples': dict((skey, ['puWeightUp/puWeight', 'puWeightDown/puWeight']) for skey in mc),
        'AsLnN'   : '0'
    }

    ### fakes ###
    nuisances[f'fake_ele_{year}'] = {
    'name': f'CMS_fake_e_{year}',
    'skipCMS': 1,
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake_e': ['fakeWEleUp', 'fakeWEleDown'],
        }
    }
    nuisances[f'fake_ele_stat_{year}'] = {
        'name': f'CMS_fake_stat_e_{year}',
        'skipCMS': 1,
        'kind': 'weight',
        'type': 'shape',
        'samples': {
            'Fake_e': ['fakeWStatEleUp', 'fakeWStatEleDown']
        }
    }
    nuisances[f'fake_mu_{year}'] = {
        'name': f'CMS_fake_m_{year}',
        'skipCMS': 1,
        'kind': 'weight',
        'type': 'shape',
        'samples': {
            'Fake_m': ['fakeWMuUp', 'fakeWMuDown'],
        }
    }
    nuisances[f'fake_mu_stat_{year}'] = {
        'name': f'CMS_fake_stat_m_{year}',
        'skipCMS': 1,
        'kind': 'weight',
        'type': 'shape',
        'samples': {
            'Fake_m': ['fakeWStatMuUp', 'fakeWStatMuDown'],
        }
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

###### pdf uncertainties
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

### lumi ###
nuisances['lumi_uncorrelated_2022'] = {
    'name'    : 'lumi_2022',
    'type'    : 'shape',
    'samples' : dict((skey, '1.014') for skey in mc)
}
nuisances['lumi_uncorrelated_2022EE'] = {
    'name'    : 'lumi_2022EE',
    'type'    : 'shape',
    'samples' : dict((skey, '1.014') for skey in mc)
}
nuisances['lumi_uncorrelated_2023'] = {
    'name'    : 'lumi_2023',
    'type'    : 'shape',
    'samples' : dict((skey, '1.013') for skey in mc)
}
nuisances['lumi_uncorrelated_2023BPix'] = {
    'name'    : 'lumi_2023BPix',
    'type'    : 'shape',
    'samples' : dict((skey, '1.016') for skey in mc)
}
nuisances['lumi_uncorrelated_2024'] = {
    'name'    : 'lumi_2024',
    'type'    : 'shape',
    'samples' : dict((skey, '1.016') for skey in mc)
}

### rate parameters ###

nuisances['DYnorm']  = {
    'name'  : 'CMS_hww_DYnorm2j',
    'skipCMS': 1,
    'type'  : 'rateParam',
    'samples'  : {'DY' : '1.00' },
}

nuisances['WWnorm'] = {
    'name'   : 'CMS_hww_WWnorm2j',
    'skipCMS': 1,
    'type'   : 'rateParam',
    'samples': {
        'WW'   : '1.00',
    },
}

nuisances['ggWWnorm'] = {
    'name'   : 'CMS_hww_WWnorm2j',
    'skipCMS': 1,
    'type'   : 'rateParam',
    'samples': {
        'ggWW'   : '1.00',
    },
}

nuisances['topnorm']  = {
    'name'  : 'CMS_hww_topnorm2j',
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
