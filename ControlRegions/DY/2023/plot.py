groupPlot = {}

groupPlot['DY']  = {  
    'nameHR'   : 'DY',
    'isSignal' : 0,
    'color'    : '#832db6', #kGreen+4
    'samples'  : ['DY']
}

# groupPlot['DY_nHardJets_0']  = {  
#     'nameHR'   : 'DY_nHardJets_0',
#     'isSignal' : 0,
#     'color'    : '#832db6', #kGreen+4
#     'samples'  : ['DY_nHardJets_0']
# }
# 
# groupPlot['DY_nHardJets_1']  = {  
#     'nameHR'   : 'DY_nHardJets_1',
#     'isSignal' : 0,
#     'color'    : '#b27cd1', 
#     'samples'  : ['DY_nHardJets_1']
# }
# 
# groupPlot['DY_nHardJets_2']  = {  
#     'nameHR'   : 'DY_nHardJets_2',
#     'isSignal' : 0,
#     'color'    : '#e0cbed', #kGreen
#     'samples'  : ['DY_nHardJets_2']
# }


plot = {}

# plot['DY_nHardJets_0']  = {  
#     'color'    : 418,    # kGreen+2
#     'isSignal' : 0,
#     'isData'   : 0, 
#     'scale'    : 1.0,
# }
# 
# plot['DY_nHardJets_1']  = {  
#     'color'    : 418,    # kGreen+2
#     'isSignal' : 0,
#     'isData'   : 0, 
#     'scale'    : 1.0,
# }
# 
# plot['DY_nHardJets_2']  = {  
#     'color'    : 418,    # kGreen+2
#     'isSignal' : 0,
#     'isData'   : 0, 
#     'scale'    : 1.0,
# }

plot['DY']  = {  
    'color'    : 418,    # kGreen+2
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.0,
}

# data

plot['DATA']  = { 
    'nameHR'   : 'Data',
    'color'    : 1 ,  
    'isSignal' : 0,
    'isData'   : 1 ,
    'isBlind'  : 0
}


# Legend definition
legend = {}
legend['lumi'] = 'L =  17.8 fb^{-1}'
legend['sqrt'] = '#sqrt{s} = 13.6 TeV'
