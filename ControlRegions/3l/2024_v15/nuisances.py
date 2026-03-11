mcProduction = 'Summer24_150x_nAODv15_Full2024v15'
mcSteps      = 'MCl2loose2024v15__MCCorr2024v15__JERFrom23BPix__l2tight'
dataRecoMuon     = 'Run2024_ReRecoCDE_PromptFGHI_nAODv15_Full2024v15_Muon'
dataRecoEGamma     = 'Run2024_ReRecoCDE_PromptFGHI_nAODv15_Full2024v15_EGamma'
dataRecoMuonEG     = 'Run2024_ReRecoCDE_PromptFGHI_nAODv15_Full2024v15_MuonEG'
dataSteps    = 'DATAl2loose2024v15__l2loose'

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
#fakeDirectory = os.path.join(treeBaseDir, dataReco, fakeSteps)
#dataDirectory = os.path.join(treeBaseDir, dataReco, dataSteps)
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
    'name': 'CMS_res_j_2024',
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

jes_systs    = ["Absolute", "Absolute_2024", "FlavorQCD", "BBEC1", "EC2", "HF", "BBEC1_2024", "EC2_2024", "RelativeBal", "RelativeSample_2024", "HF_2024"] # Reduced set of 11 uncertainties
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

#nuisances['MET'] = {
#    'name': 'CMS_scale_met_2024',
#    'skipCMS' : 1,
#    'kind': 'suffix',
#    'type': 'shape',
#    'mapUp': 'unclustEnup',
#    'mapDown': 'unclustEndo',
    #'separator': '__',
#    'samples': dict((skey, ['1', '1']) for skey in mc),
#    'folderUp': makeMCDirectory('unclustEnup_suffix'),
#    'folderDown': makeMCDirectory('unclustEndo_suffix'),
#    'AsLnN': '0'
#}

##### Lepton scale
nuisances['lepscale'] = {
    'name': 'CMS_lepscale_2024',
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
    'name': 'CMS_lepres_2024',
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

nuisance_sources = {
    'bc': [ 'fsrdef', 'hdamp', 'isrdef', 'jer', 'jes', 'mass', 'statistic', 'tune'],
    'light': [ 'correlated', 'uncorrelated'],
}

for source in nuisance_sources['bc']:
    btag_syst = [f'btagSFbc_up_{source}/btagSFbc', f'btagSFbc_down_{source}/btagSFbc']
    if source == 'statistic':
        name = f'CMS_btagSFbc_correlated'
    else :
        name = f'CMS_btagSFbc_{source}_2024'
    nuisances[f'btagSFbc_{source}'] = {
        'name': name,
        'skipCMS': 1,
        'kind': 'weight',
        'type': 'shape',
        'samples': dict((skey, btag_syst) for skey in mc),
    }

for corr in nuisance_sources['light']:
    btag_syst = [ f'btagSFlight_up_{corr}/btagSFlight', f'btagSFlight_down_{corr}/btagSFlight']
    name = (f'CMS_btagSFlight_{corr}' if corr == 'correlated' else f'CMS_btagSFlight_2024')
    nuisances[f'btagSFlight_{corr}'] = {
        'name': name,
        'skipCMS': 1,
        'kind': 'weight',
        'type': 'shape',
        'samples': dict((skey, btag_syst) for skey in mc),
    }


##### Trigger Scale Factors                                                                                                                                                                                

trig_syst = ['TriggerSFWeight_2l_u/TriggerSFWeight_2l', 'TriggerSFWeight_2l_d/TriggerSFWeight_2l']

nuisances['trigg'] = {
    'name': 'CMS_eff_hwwtrigger_2024',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, trig_syst) for skey in mc)
}

##### Electron Efficiency and energy scale

nuisances['eff_e'] = {
    'name': 'CMS_eff_e_2024',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, ['SFweightEleUp', 'SFweightEleDown']) for skey in mc), # IN THIS SAMPLES THERE'S AN ERROR AND SFUP AND SFDO ARE THE SAME, NEEDS TO BE FIXED
}

##### Muon Efficiency and energy scale

nuisances['eff_m'] = {
    'name': 'CMS_eff_m_2024',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, ['SFweightMuUp', 'SFweightMuDown']) for skey in mc),
}


nuisances['PU'] = {
    'name'    : 'CMS_pileup_2024',
    'type'    : 'lnN',
    'samples' : dict((skey, '1.05') for skey in mc),
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


## This should work for samples with either 8 or 9 LHE scale weights (Length$(LHEScaleWeight) == 8 or 9)

nuisances['QCDscale_top']  = {
    'name'  : 'QCDscale_ttbar',
    'kind'  : 'weight',
    'type'  : 'shape',
    'samples'  : {'top' : ['Alt(LHEScaleWeight,0, 1.)', 'Alt(LHEScaleWeight,nLHEScaleWeight-1,1)']}
}

nuisances['QCDscale_DY'] = {
    'name': 'QCDscale_DY',
    'kind'  : 'weight',
    'type': 'shape',
    'samples': {'DY': ['Alt(LHEScaleWeight,0, 1.)', 'Alt(LHEScaleWeight,nLHEScaleWeight-1,1)']}
}
nuisances['QCDscale_VV'] = {
    'name' : 'QCDscale_VV',
    'kind' : 'weight',
    'type' : 'shape',
    'samples' : {'WW'  : ['Alt(LHEScaleWeight,0, 1.)', 'Alt(LHEScaleWeight,nLHEScaleWeight-1,1)']}
}

nuisances['QCDscale_ggVV'] = {
    'name': 'QCDscale_ggVV',
    'type': 'lnN',
    'samples': {'ggWW': '1.15'},
}


nuisances['QCDscale_ggH'] = {
    'name' : 'QCDscale_ggH',
    'kind' : 'weight',
    'type' : 'shape',
    'samples' : {'ggH_hww'  : ['Alt(LHEScaleWeight,0, 1.)', 'Alt(LHEScaleWeight,nLHEScaleWeight-1,1)']}
}

nuisances['QCDscale_qqH'] = {
    'name' : 'QCDscale_qqH',
    'kind' : 'weight',
    'type' : 'shape',
    'samples' : {'qqH_hww'  : ['Alt(LHEScaleWeight,0, 1.)', 'Alt(LHEScaleWeight,nLHEScaleWeight-1,1)']}
}

nuisances['fake_syst'] = {
    'name': 'CMS_fake_syst',
    'type': 'lnN',
    'samples': {
        'Fake': '1.3'
    },
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
