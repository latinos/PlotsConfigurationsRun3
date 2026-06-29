# Group of plots

groupPlot = {}

groupPlot['DY'] = {
    'nameHR'   : 'DY',
    'isSignal' : 0,
    'color'    : 418, # kGreen + 2
    'samples'  : ['DY']
}

groupPlot['Top']  = {  
    'nameHR'   : 't#bar{t}',
    'isSignal' : 0,
    'color'    : 400, # kYellow
    'samples'  : ['Top']
}

groupPlot['WW']  = {  
    'nameHR'   : 'WW',
    'isSignal' : 0,
    'color'    : 851, # kAzure -9 
    'samples'  : ['WW']
}

groupPlot['WZ']  = {  
    'nameHR'   : 'WZ',
    'isSignal' : 0,
    'color'    : 619, # kViolet + 1
    'samples'  : ['WZ']
}

# Plots

plot = {}

plot['DY']  = {  
    'color'    : 418, # kGreen + 2
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.0,
}

plot['Top']  = {  
    'color'    : 400, # kKYellow
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.0,
}

plot['WW']  = {  
    'color'    : 851, # kKYellow
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.0,
}

plot['WZ']  = {  
    'color'    : 619, # kKYellow
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
legend['lumi'] = 'L = 17.8 fb^{-1}'
legend['sqrt'] = '#sqrt{s} = 13.6 TeV'
