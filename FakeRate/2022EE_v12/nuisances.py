import sys
 
nuisances = {}

mc = [skey for skey in samples if skey not in ('Fake', 'DATA','ChargeFlip')]

redirector = ""

useXROOTD = False

################################ EXPERIMENTAL UNCERTAINTIES  #################################

#### Luminosity

# https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun3

nuisances['lumi_Uncorrelated'] = {
    'name'    : 'lumi_13TeV_2022EE',
    'type'    : 'lnN',
    'samples' : dict((skey, '1.014') for skey in mc if skey not in ['WZ'])
}

