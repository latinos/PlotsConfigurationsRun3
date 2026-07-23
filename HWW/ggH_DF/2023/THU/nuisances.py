mcProduction = 'Summer23_130x_nAODv12_Full2023v12'
mcSteps      = 'MCl2loose2023v12__MCCorr2023v12JetScaling__l2tight'
dataReco     = 'Run2023_Prompt_nAODv12_Full2023v12'
dataSteps    = 'DATAl2loose2023v12__l2loose'
fakeSteps    = 'DATAl2loose2023v12__l2loose'

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

nuisances = {}

##### PS

nuisances['PS_ISR_higgs']  = {
    'name'    : 'ps_isr',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : {
        'ggH_hww' : ['PSWeight[2]', 'PSWeight[0]'],
        'qqH_hww' : ['PSWeight[2]', 'PSWeight[0]'],
        },
    'AsLnN'   : '0',
}

nuisances['PS_FSR_higgs']  = {
    'name'    : 'ps_fsr',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : {
        'ggH_hww' : ['PSWeight[3]', 'PSWeight[1]'],
        'qqH_hww' : ['PSWeight[3]', 'PSWeight[1]'],
        },
    'AsLnN'   : '0',
}


## This should work for samples with either 8 or 9 LHE scale weights (Length$(LHEScaleWeight) == 8 or 9)
variations_ggH = ['Alt(LHEScaleWeight,0,1)',
              'Alt(LHEScaleWeight,1,1)',
              'Alt(LHEScaleWeight,3,1)',
              'Alt(LHEScaleWeight,nLHEScaleWeight-4,1)',
              'Alt(LHEScaleWeight,nLHEScaleWeight-2,1)',
              'Alt(LHEScaleWeight,nLHEScaleWeight-1,1)']

nuisances['QCDscale_ggH'] = {
    'name' : 'QCDscale_ggH',
    'kind' : 'weight_envelope',
    'type' : 'shape',
    'samples' : {'ggH_hww'  : variations_ggH}
}

variations_qqH = ['Alt(LHEScaleWeight,0,1)',
              'Alt(LHEScaleWeight,1,1)',
              'Alt(LHEScaleWeight,3,1)',
              'Alt(LHEScaleWeight,nLHEScaleWeight-4,1)',
              'Alt(LHEScaleWeight,nLHEScaleWeight-2,1)',
              'Alt(LHEScaleWeight,nLHEScaleWeight-1,1)']

nuisances['QCDscale_qqH'] = {
    'name' : 'QCDscale_qqH',
    'kind' : 'weight_envelope',
    'type' : 'shape',
    'samples' : {'qqH_hww'  : variations_qqH}
}

