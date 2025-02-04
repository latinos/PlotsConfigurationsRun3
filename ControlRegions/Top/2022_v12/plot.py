# Group plot
groupPlot = {}

groupPlot['DY']  = {  
    'nameHR'   : 'DY',
    'isSignal' : 0,
    'color'    : 420, # kGreen+4
    'samples'  : ['DY']
}

groupPlot['Top']  = {  
    'nameHR'   : 'Top',
    'isSignal' : 0,
    'color'    : 400, # kYellow
    'samples'  : ['Top']
}

groupPlot['WW']  = {  
    'nameHR'   : 'WW',
    'isSignal' : 0,
    'color'    : 851, # kAzure-9
    'samples'  : ['WW']
}


# Plot
plot = {}

plot['DY']  = {  
    'color'    : 420, # kGreen+4
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.0,
}

plot['Top']  = {  
    'color'    : 400, # kYellow
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.0,
}

plot['WW']  = {  
    'color'    : 851, # kAzure-9
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
legend['lumi'] = 'L =  8.2 fb^{-1}'
legend['sqrt'] = '#sqrt{s} = 13.6 TeV'
