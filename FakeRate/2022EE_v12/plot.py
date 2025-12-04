# plot configuration

# Groups of samples to improve the plots.
# If not defined, normal plots is used

lepton_categories = ['_ele_low_pt', '_ele_high_pt', '_muon_low_pt', '_muon_high_pt']

groupPlot = {}

# groupPlot['TTToSemiLeptonic']  = {  
#     'nameHR'   : 'Top Semi-Leptonic',
#     'isSignal' : 0,
#     'color'    : 401, # kYellow+1
#     'samples'  : ['TTToSemiLeptonic' + lep_cat for lep_cat in lepton_categories]
# }

# groupPlot['TTTo2L2Nu']  = {  
#     'nameHR'   : 'Top Fully-Leptonic',
#     'isSignal' : 0,
#     'color'    : 400, # kYellow
#     'samples'  : ['TTTo2L2Nu' + lep_cat for lep_cat in lepton_categories]
# }

groupPlot['DY']  = {  
    'nameHR'   : "DY",
    'isSignal' : 0,
    'color'    : '#832db6', 
    'samples'  : ['DY' + lep_cat for lep_cat in lepton_categories]
}

groupPlot['WJets']  = {  
    'nameHR'   : "WJets",
    'isSignal' : 0,
    'color'    : '#717581', 
    'samples'  : ['WJets' + lep_cat for lep_cat in lepton_categories]
}

# keys here must match keys in samples.py    

plot = {}

for lep_cat in lepton_categories:

    plot['DY' + lep_cat]  = {  
        'nameHR'   : 'DY',
        'color'    : '#832db6', 
        'isSignal' : 0,
        'isData'   : 0, 
        'scale'    : 1.0,
    }

    # plot['TTToSemiLeptonic' + lep_cat] = {   
    #     'nameHR' : 'Top Semi-Leptonic',
    #     'color'    : 401, # kYellow+1
    #     'isSignal' : 0,
    #     'isData'   : 0, 
    #     'scale'    : 1.0,
    # }

    # plot['TTTo2L2Nu' + lep_cat] = {   
    #     'nameHR' : 'Top Fully-Leptonic',
    #     'color'    : 400, # kYellow
    #     'isSignal' : 0,
    #     'isData'   : 0, 
    #     'scale'    : 1.0,
    # }
    
    plot['WJets' + lep_cat] = {   
        'nameHR' : 'WJets',
        'color'    : '#717581', 
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

legend['lumi'] = '' # L = 59.8 fb^{-1}'
legend['sqrt'] = '13.6 TeV'
