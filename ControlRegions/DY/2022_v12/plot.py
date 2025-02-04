# Group plot
groupPlot = {}

groupPlot['DY']  = {  
    'nameHR'   : 'DY',
    'isSignal' : 0,
    'color'    : 420, # kGreen+4
    'samples'  : ['DY']
}


# Plot
plot = {}

plot['DY']  = {  
    'color'    : 420, # kGreen+4
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.0,
}


# Data
plot['DATA']  = { 
    'nameHR'   : 'Data',
    'color'    : 1 ,  
    'isSignal' : 0,
    'isData'   : 1 ,
    'isBlind'  : 0
}

# Legend definition
legend = {}
legend['lumi'] = 'L =  8.2 fb^{-1}'
legend['sqrt'] = '#sqrt{s} = 13.6 TeV'
