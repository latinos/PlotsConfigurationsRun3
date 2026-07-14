nuisances = {}

mc     = [skey for skey in samples if skey not in ('Fake', 'DATA')]
mc_emb = [skey for skey in samples if skey not in ('Fake', 'DATA')]

# merge cuts
cuts0j = []
cuts1j = []
cuts2j = []
#cuts=[]
for k in cuts:
  for cat in cuts[k]['categories']:
    if '0j' in cat: cuts0j.append(k+'_'+cat)
    elif '1j' in cat: cuts1j.append(k+'_'+cat)
    elif '2j' in cat: cuts2j.append(k+'_'+cat)
    else: print('WARNING: name of category does not contain either 0j,1j,2j')

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
        'Fake': ['fakeWEleUp', 'fakeWEleDown'],
        }
    }
    nuisances[f'fake_ele_stat_{year}'] = {
        'name': f'CMS_fake_stat_e_{year}',
        'skipCMS': 1,
        'kind': 'weight',
        'type': 'shape',
        'samples': {
            'Fake': ['fakeWStatEleUp', 'fakeWStatEleDown']
        }
    }
    nuisances[f'fake_mu_{year}'] = {
        'name': f'CMS_fake_m_{year}',
        'skipCMS': 1,
        'kind': 'weight',
        'type': 'shape',
        'samples': {
            'Fake': ['fakeWMuUp', 'fakeWMuDown'],
        }
    }
    nuisances[f'fake_mu_stat_{year}'] = {
        'name': f'CMS_fake_stat_m_{year}',
        'skipCMS': 1,
        'kind': 'weight',
        'type': 'shape',
        'samples': {
            'Fake': ['fakeWStatMuUp', 'fakeWStatMuDown'],
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

nuisances['DYnorm0j']  = {
               'name'  : 'CMS_hww_DYnorm0j',
               'samples'  : {
                   'DY' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts0j
              }

nuisances['DYnorm1j']  = {
               'name'  : 'CMS_hww_DYnorm1j',
               'samples'  : {
                   'DY' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts1j
              }

nuisances['DYnorm2j']  = {
                 'name'  : 'CMS_hww_DYnorm2j',
                 'samples'  : {
                   'DY' : '1.00',
                     },
                 'type'  : 'rateParam',
                 'cuts'  : cuts2j
                }


nuisances['WWnorm0j']  = {
               'name'  : 'CMS_hww_WWnorm0j',
               'samples'  : {
                   'WW' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts0j
              }

nuisances['ggWWnorm0j']  = {
               'name'  : 'CMS_hww_WWnorm0j',
               'samples'  : {
                   'ggWW' : '1.00',
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

nuisances['ggWWnorm1j']  = {
               'name'  : 'CMS_hww_WWnorm1j',
               'samples'  : {
                   'ggWW' : '1.00',
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
               'cuts'  : cuts2j
              }

nuisances['ggWWnorm2j']  = {
               'name'  : 'CMS_hww_WWnorm2j',
               'samples'  : {
                   'ggWW' : '1.00',
                   },
               'type'  : 'rateParam',
               'cuts'  : cuts2j
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
               'cuts'  : cuts2j
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
