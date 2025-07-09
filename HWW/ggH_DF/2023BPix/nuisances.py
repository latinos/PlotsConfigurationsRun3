mcProduction = 'Summer22EE_130x_nAODv12_Full2022v12'
mcSteps      = 'MCl2loose2022EEv12__MCCorr2022EEv12JetScaling__l2tight'
dataReco     = 'Run2022EE_Prompt_nAODv12_Full2022v12'
dataSteps    = 'DATAl2loose2022EEv12__l2tight'

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

#### Luminosity
##
#nuisances['lumi_2022EE'] = {
#    'name'    : 'lumi_2022EE',
#    'type'    : 'lnN',
#    'samples' : dict((skey, '1.013') for skey in mc)
#}
#
#
#nuisances['JER'] = {
#    'name': 'CMS_res_j_2022EE',
#    'skipCMS' : 1,
#    'kind': 'suffix',
#    'type': 'shape',
#    'mapUp': 'jerup',
#    'mapDown': 'jerdo',
#    #'separator': '__',
#    'samples': dict((skey, ['1', '1']) for skey in mc),
#    'folderUp': makeMCDirectory('jerup_suffix'),
#    'folderDown': makeMCDirectory('jerdo_suffix'),
#    'AsLnN': '0'
#}
#
#nuisances['JES'] = {
#    'name': 'CMS_jes_2022EE',
#    'skipCMS' : 1,
#    'kind': 'suffix',
#    'type': 'shape',
#    'mapUp': 'jesTotalup',
#    'mapDown': 'jesTotaldo',
#    #'separator': '__',
#    'samples': dict((skey, ['1', '1']) for skey in mc),
#    'folderUp': makeMCDirectory('jesTotalup_suffix'),
#    'folderDown': makeMCDirectory('jesTotaldo_suffix'),
#    'AsLnN': '0'
#}
#
#
#nuisances['MET'] = {
#    'name': 'CMS_MET_2022EE',
#    'skipCMS' : 1,
#    'kind': 'suffix',
#    'type': 'shape',
#    'mapUp': 'unclustEnup',
#    'mapDown': 'unclustEndo',
#    #'separator': '__',
#    'samples': dict((skey, ['1', '1']) for skey in mc),
#    'folderUp': makeMCDirectory('unclustEnup_suffix'),
#    'folderDown': makeMCDirectory('unclustEndo_suffix'),
#    'AsLnN': '0'
#}
#
#
###### Electron Efficiency and energy scale
#
#nuisances['eff_e'] = {
#    'name': 'CMS_eff_e_2022EE',
#    'kind': 'weight',
#    'type': 'shape',
#    'samples': dict((skey, ['SFweightEleUp', 'SFweightEleDown']) for skey in mc),
#}
#
###### Muon Efficiency and energy scale
#
#nuisances['eff_m'] = {
#    'name': 'CMS_eff_m_2022EE',
#    'kind': 'weight',
#    'type': 'shape',
#    'samples': dict((skey, ['SFweightMuUp', 'SFweightMuDown']) for skey in mc),
#}
#
###### Trigger Efficiency
#
#trig_syst = ['TriggerSFWeight_2l_u/TriggerSFWeight_2l', 'TriggerSFWeight_2l_d/TriggerSFWeight_2l']
#
#nuisances['trigg'] = {
#    'name': 'CMS_eff_hwwtrigger_2022EE',
#    'kind': 'weight',
#    'type': 'shape',
#    'samples': dict((skey, trig_syst) for skey in mc)
#}
#
###### Lepton scale
#nuisances['lepscale'] = {
#    'name': 'CMS_lepscale_2022EE',
#    'skipCMS' : 1,
#    'kind': 'suffix',
#    'type': 'shape',
#    'mapUp': 'leptonScaleup',
#    'mapDown': 'leptonScaledo',
#    #'separator': '__',
#    'samples': dict((skey, ['1', '1']) for skey in mc),
#    'folderUp': makeMCDirectory('leptonScaleup_suffix'),
#    'folderDown': makeMCDirectory('leptonScaledo_suffix'),
#    'AsLnN': '0'
#}
#
###### Lepton resolution
#nuisances['lepres'] = {
#    'name': 'CMS_lepres_202EE',
#    'skipCMS' : 1,
#    'kind': 'suffix',
#    'type': 'shape',
#    'mapUp': 'leptonResolutionup',
#    'mapDown': 'leptonResolutiondo',
#    #'separator': '__',
#    'samples': dict((skey, ['1', '1']) for skey in mc),
#    'folderUp': makeMCDirectory('leptonResolutionup_suffix'),
#    'folderDown': makeMCDirectory('leptonResolutiondo_suffix'),
#    'AsLnN': '0'
#}

### MC statistical uncertainty
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
