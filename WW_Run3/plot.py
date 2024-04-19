

groupPlot = {}

groupPlot['top']  = {
    'nameHR' : 'tW and t#bar{t}',
    'isSignal' : 0,
    'color': 400,   # kYellow                                                                                                                                                                                                                                  
    'samples'  : ['top','top_EE']
}

groupPlot['Fake']  = {
    'nameHR' : 'nonprompt',
    'isSignal' : 0,
    'color': 921,    # kGray + 1                                                                                                                          
    'samples'  : ['Fake']
}

groupPlot['WW']  = {
    'nameHR' : 'WW',
    'isSignal' : 0,
    'color': 851, # kAzure -9                                                                                                                                                                                                                                  
    'samples'  : ['WW','WW_EE']
}

groupPlot['DY']  = {
    'nameHR' : "DY",
    'isSignal' : 0,
    'color'    : 418,    # kGreen+2
    'samples'  : ['DY','DY_EE']
}

groupPlot['VVV']  = {
    'nameHR' : 'VVV',
    'isSignal' : 0,
    'color': 857, # kAzure -3
    'samples'  : ['VVV','VVV_EE']
}

groupPlot['VZ']  = {
    'nameHR' : "VZ",
    'isSignal' : 0,
    'color'    : 617,   # kViolet + 1 
    'samples'  : ['WZ', 'ZZ', 'WZ_EE', 'ZZ_EE']
}



plot = {}
# keys here must match keys in samples.py    
                    
plot['DY']  = {  
    'nameHR'   : 'DY',
    'color'    : 418,
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.03125,
}

plot['DY_EE']  = {
    'nameHR'   : 'DY',
    'color'    : 418,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.046052631578947366,
}

plot['top']  = {
    'nameHR'   : 'Top',
    'color'    : 400,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.023255813953488372,
}

plot['top_EE']  = {
    'nameHR'   : 'Top',
    'color'    : 400,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.03398058252427184,
}

plot['Fake']  = {
    'nameHR'   : 'nonprompt',
    'color'    : 921,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['WW']  = {
    'nameHR'   : 'WW',
    'color'    : 851,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['WW_EE']  = {
    'nameHR'   : 'WW',
    'color'    : 851,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['VVV']  = {
    'nameHR'   : 'VVV',
    'color'    : 857,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['VVV_EE']  = {
    'nameHR'   : 'VVV',
    'color'    : 857,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['WZ']  = {
    'nameHR'   : 'WZ',
    'color'    : 617,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['WZ_EE']  = {
    'nameHR'   : 'WZ',
    'color'    : 617,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['ZZ']  = {
    'nameHR'   : 'ZZ',
    'color'    : 617,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['ZZ_EE']  = {
    'nameHR'   : 'ZZ',
    'color'    : 617,
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


# additional options
legend = {}

legend['lumi'] = 'L =  35.0 fb^{-1}'

legend['sqrt'] = '#sqrt{s} = 13.6 TeV'
