
mcProduction = 'Summer22_130x_nAODv12_Full2022v12'
mcSteps      = 'MCl2loose2022v12__MCCorr2022v12JetScaling__l2tight'
dataReco     = 'Run2022_Prompt_nAODv12_Full2022v12'
dataSteps    = 'DATAl2loose2022v12__l2tight'

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
# https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun3
nuisances['lumi_2022EE'] = {
    'name'    : 'lumi_2022EE',
    'type'    : 'lnN',
    'samples' : dict((skey, '1.014') for skey in mc)
}

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
