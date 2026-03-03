import sys

# Enable reading YR for Higgs XS and uncertainties
sys.path.append('../macros/')
#import HiggsXSection
#HiggsXS = HiggsXSection.HiggsXSection()

# nuisances = {}

limitFiles   = -1

#
# AM: for the time being exclude the signal from the list of nuisances ... missing adequate post-processing
#
mc = [skey for skey in samples if skey not in ('Fake', 'DATA', 'Hgluglu')]
mcln = [skey for skey in samples if skey not in ('Fake', 'DATA')]

################################ EXPERIMENTAL UNCERTAINTIES  #################################

#### Luminosity

# https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun2#LumiComb
# Uncorrelated 2016               1.0
# Uncorrelated       2017              2.0
# Uncorrelated             2018             1.5
# Correlated   2016, 2017, 2018   0.6, 0.9, 2.0
# Correlated         2017, 2018        0.6, 0.2

nuisances['lumi_Uncorrelated_2017'] = {
    'name'    : 'lumi_13TeV_2017',
    'type'    : 'shape',
    'samples' : dict((skey, '1.020') for skey in mc if skey not in ['WZ']),
    'perYearType' : 'lnN'
}

nuisances['lumi_Uncorrelated_2018'] = {
    'name'    : 'lumi_13TeV_2018',
    'type'    : 'shape',
    'samples' : dict((skey, '1.015') for skey in mcln if skey not in ['blabla']),
    'perYearType' : 'lnN'
}

nuisances['lumi_Correlated_2017_2018'] = {
    'name'    : 'lumi_13TeV_1718',
    'type'    : 'shape',
    'samples' : dict((skey, '1.002') for skey in mcln if skey not in ['blabla']),
    'perYearType' : 'lnN'
}

nuisances['lumi_Correlated_Run2'] = {
    'name'    : 'lumi_13TeV_correlated',
    'type'    : 'shape',
    'samples' : dict((skey, '1.020') for skey in mcln if skey not in ['blabla']),
    'perYearType' : 'lnN'
}




nuisances['test_lnn'] = {
    'name'    : 'mynuisance',
    'type'    : 'lnN',
    'samples' : dict((skey, '1.006') for skey in mc if skey not in ['WZ']),
    'perYearType' : 'lnN'
}



#
# AM: if different for the different years then to be tranformed into a shape uncertainty
#








## Use the following if you want to apply the automatic combine MC stat nuisances.
nuisances['stat']  = {
    'type'          : 'auto',
    'maxPoiss'      : '10',
    'includeSignal' : '0',
    'samples'       : {}
}
#  nuisance ['maxPoiss'] =  Number of threshold events for Poisson modelling
#  nuisance ['includeSignal'] =  Include MC stat nuisances on signal processes (1=True, 0=False)

for n in nuisances.values():
    n['skipCMS'] = 1
