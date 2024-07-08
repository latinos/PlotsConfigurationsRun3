import sys
 
nuisances = {}

# mcProduction = 'Summer20UL18_106x_nAODv9_Full2018v9'
# dataReco     = 'Run2018_UL2018_nAODv9_Full2018v9'
# mcSteps      = 'MCl1loose2018v9__MCCorr2018v9NoJERInHorn__l2tightOR2018v9'
# fakeSteps    = 'DATAl1loose2018v9__l2loose__fakeW'
# dataSteps    = 'DATAl1loose2018v9__l2loose__l2tightOR2018v9'

# treeBaseDir  = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'
# limitFiles   = -1

mc = [skey for skey in samples if skey not in ('Fake', 'DATA','ChargeFlip')]

redirector = ""

useXROOTD = False

# def makeMCDirectory(var=''):
#     if var== '':
#         print(os.path.join(treeBaseDir, mcProduction, mcSteps))
#         return os.path.join(treeBaseDir, mcProduction, mcSteps)
#     else:
#         print(os.path.join(treeBaseDir, mcProduction, mcSteps + '__' + var))
#         return os.path.join(treeBaseDir, mcProduction, mcSteps + '__' + var)

# mcDirectory = makeMCDirectory()
# fakeDirectory = os.path.join(treeBaseDir, dataReco, fakeSteps)
# dataDirectory = os.path.join(treeBaseDir, dataReco, dataSteps)

################################ EXPERIMENTAL UNCERTAINTIES  #################################

#### Luminosity

# https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun2#LumiComb
# Uncorrelated 2016               1.0
# Uncorrelated       2017              2.0
# Uncorrelated             2018             1.5
# Correlated   2016, 2017, 2018   0.6, 0.9, 2.0
# Correlated         2017, 2018        0.6, 0.2

nuisances['lumi_Uncorrelated'] = {
    'name'    : 'lumi_13TeV_2018',
    'type'    : 'lnN',
    'samples' : dict((skey, '1.015') for skey in mc if skey not in ['WZ'])
}

