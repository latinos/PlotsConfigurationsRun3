# Group plot
# Groups of samples to improve the plots.
# If not defined, normal plots is used

groupPlot = {}

groupPlot['DY']  = {  
    'nameHR'   : 'DY',
    'isSignal' : 0,
    'color'    : 420, # kGreen+4
    'samples'  : ['DY']
}

groupPlot['background']  = {  
    'nameHR'   : 'background',
    'isSignal' : 0,
    'color'    : 851, # kAzure -9 
    'samples'  : ['top', 'diboson', 'SMhiggs']
}


# Plot
# keys here must match keys in samples.py    

plot = {}

plot['DY']  = {  
    'color'    : 420, # kGreen+4
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.0,
}

plot['top']  = {  
    'color'    : 400,   # kYellow
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.0,
}

plot['diboson']  = {  
    'color'    : 851, # kAzure -9 
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.0,
}

plot['SMhiggs']  = {  
    'color'    : 632+3, # kRed+3 
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
