# Plot configuration

# Groups of samples to improve the plots.
# If not defined, normal plots is used

lepton_categories = ['_ele_low_pt', '_ele_high_pt', '_muon_low_pt', '_muon_high_pt']

groupPlot = {}

groupPlot['DY']  = {  
    'nameHR'   : "DY",
    'isSignal' : 0,
    'color'    : 418, # kGreen+2
    'samples'  : ['DY' + lep_cat for lep_cat in lepton_categories]
}

groupPlot['WJets']  = {  
    'nameHR'   : "WJets",
    'isSignal' : 0,
    'color'    : 11, # kGrey
    'samples'  : ['WJets' + lep_cat for lep_cat in lepton_categories]
}

# keys here must match keys in samples.py    

plot = {}

for lep_cat in lepton_categories:

    plot['DY' + lep_cat]  = {  
        'nameHR'   : 'DY',
        'color'    : 418, # kGreen+2
        'isSignal' : 0,
        'isData'   : 0, 
        'scale'    : 1.0,
    }

    plot['WJets' + lep_cat] = {   
        'nameHR' : 'WJets',
        'color'    : 11, # kGrey
        'isSignal' : 0,
        'isData'   : 0, 
        'scale'    : 1.0,
    }

########
# Data #
########

plot['DATA']  = { 
    'nameHR'   : 'Data',
    'color'    : 1 ,  
    'isSignal' : 0,
    'isData'   : 1,
    'isBlind'  : 0
}


# Define legend

legend = {}

legend['lumi'] = '' # L = 41.5 fb^{-1}'
legend['sqrt'] = '#sqrt{s} = 13 TeV'
