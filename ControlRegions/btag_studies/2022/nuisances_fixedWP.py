
mcProduction = 'Summer22_130x_nAODv12_Full2022v12__OLD' # OLD
mcSteps = 'MCl2loose2022v12__MCCorr2022v12JetScaling__l2tight' 
dataReco = 'Run2022_ReReco_nAODv12_Full2022v12'
# fakeSteps = 'DATAl1loose2022EFGv12__fakeW'
dataSteps = 'DATAl2loose2022v12__l2tight'

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
'''
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

nuisances['JES'] = {
    'name': 'CMS_jes_2022',
    'skipCMS' : 1,
    'kind': 'suffix',
    'type': 'shape',
    'mapUp': 'jesTotalup',
    'mapDown': 'jesTotaldo',
    #'separator': '__',
    'samples': dict((skey, ['1', '1']) for skey in mc),
    'folderUp': makeMCDirectory('jesTotalup_suffix'),
    'folderDown': makeMCDirectory('jesTotaldo_suffix'),
    'AsLnN': '0'
}


nuisances['MET'] = {
    'name': 'CMS_MET_2022',
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
'''
### B-tagger
# Fixed WP btag SFs

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
'''
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
    'samples': dict((skey, ['SFweightEleUp', '1/SFweightEleDown']) for skey in mc), # IN THIS SAMPLES THERE'S AN ERROR AND SFUP AND SFDO ARE THE SAME, NEEDS TO BE FIXED
}

##### Muon Efficiency and energy scale

nuisances['eff_m'] = {
    'name': 'CMS_eff_m_2022',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, ['SFweightMuUp', 'SFweightMuDown']) for skey in mc),
}


nuisances['PU'] = {
    'name'    : 'CMS_pileup_2022',
    'type'    : 'lnN',
    'samples' : dict((skey, '1.05') for skey in mc),
}
'''
##### PS
'''
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
'''

## This should work for samples with either 8 or 9 LHE scale weights (Length$(LHEScaleWeight) == 8 or 9)
'''
nuisances['QCDscale_top']  = {
    'name'  : 'QCDscale_top',
    'kind'  : 'weight',
    'type'  : 'shape',
    'samples'  : {'top' : ['Alt(LHEScaleWeight,0, 1.)', 'Alt(LHEScaleWeight,nLHEScaleWeight-1,1)']}
}

nuisances['QCDscale_DY'] = {
    'name': 'QCDscale_DY',
    'skipCMS': 1,
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
'''

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
