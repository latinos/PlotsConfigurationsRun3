import sys
 
nuisances = {}

mcProduction = 'Summer20UL16_106x_nAODv9_noHIPM_Full2016v9'
dataReco     = 'Run2016_UL2016_nAODv9_noHIPM_Full2016v9'
mcSteps      = 'MCl1loose2016v9__MCCorr2016v9NoJERInHorn__l2tightOR2016v9'
fakeSteps    = 'DATAl1loose2016v9__l2loose__fakeW'
dataSteps    = 'DATAl1loose2016v9__l2loose__l2tightOR2016v9'

treeBaseDir  = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'
limitFiles   = -1

mc = [skey for skey in samples if skey not in ('Fake', 'DATA')]

redirector = ""

useXROOTD = False

def makeMCDirectory(var=''):
    if var== '':
        print(os.path.join(treeBaseDir, mcProduction, mcSteps))
        return os.path.join(treeBaseDir, mcProduction, mcSteps)
    else:
        print(os.path.join(treeBaseDir, mcProduction, mcSteps + '__' + var))
        return os.path.join(treeBaseDir, mcProduction, mcSteps + '__' + var)

mcDirectory   = makeMCDirectory()
fakeDirectory = os.path.join(treeBaseDir, dataReco, fakeSteps)
dataDirectory = os.path.join(treeBaseDir, dataReco, dataSteps)

################################ EXPERIMENTAL UNCERTAINTIES  #################################

#### Luminosity

# https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun2#LumiComb
# Uncorrelated 2016               1.0
# Uncorrelated       2017              2.0
# Uncorrelated             2018             1.5
# Correlated   2016, 2017, 2018   0.6, 0.9, 2.0
# Correlated         2017, 2018        0.6, 0.2

nuisances['lumi_Uncorrelated'] = {
    'name'    : 'lumi_13TeV_2016',
    'type'    : 'lnN',
    'samples' : dict((skey, '1.010') for skey in mc if skey not in ['WZ'])
}

nuisances['lumi_Correlated_Run2'] = {
    'name'    : 'lumi_13TeV_correlated',
    'type'    : 'lnN',
    'samples' : dict((skey, '1.006') for skey in mc if skey not in ['WZ'])
}


### Fakes

# Per lepton
nuisances['fake_ele'] = {
    'name'    : 'CMS_WH_hww_fake_e_2016',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : {
        'Fake_ee' : ['fakeWEleUp', 'fakeWEleDown'],
        'Fake_em' : ['fakeWEleUp', 'fakeWEleDown'],
    }
}

nuisances['fake_ele_stat'] = {
    'name'    : 'CMS_WH_hww_fake_stat_e_2016',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : {
        'Fake_ee' : ['fakeWStatEleUp', 'fakeWStatEleDown'],
        'Fake_em' : ['fakeWStatEleUp', 'fakeWStatEleDown'],
    }
}


nuisances['fake_mu'] = {
    'name'    : 'CMS_WH_hww_fake_m_2016',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : {
        'Fake_mm' : ['fakeWMuUp', 'fakeWMuDown'],
        'Fake_em' : ['fakeWMuUp', 'fakeWMuDown'],
    }   
}       

nuisances['fake_mu_stat'] = {
    'name'    : 'CMS_WH_hww_fake_stat_m_2016',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : {
        'Fake_mm' : ['fakeWStatMuUp', 'fakeWStatMuDown'],
        'Fake_em' : ['fakeWStatMuUp', 'fakeWStatMuDown'],
    }
}


# Use the following if you want to apply the automatic combine MC stat nuisances.
nuisances['stat']  = {
    'type'          : 'auto',
    'maxPoiss'      : '10',
    'includeSignal' : '0',
    'samples'       : {}
}
# nuisance ['maxPoiss']      = Number of threshold events for Poisson modelling
# nuisance ['includeSignal'] = Include MC stat nuisances on signal processes (1=True, 0=False)

for n in nuisances.values():
    n['skipCMS'] = 1
