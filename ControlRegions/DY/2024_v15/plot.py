groupPlot = {}

groupPlot['top']  = {
    'nameHR' : 'top',
    'isSignal' : 0,
    'color': '#ffa90e',   # 400 kYellow                                                                                                                                                                                                                                  
    'samples'  : ['top']
}


groupPlot['WW']  = {
    'nameHR' : 'WW',
    'isSignal' : 0,
    'color': '#3f90da', # 851 kAzure -9                                                                                                                                                                                                                                  
    'samples'  : ['WW', 'ggWW']
}

groupPlot['DY']  = {
    'nameHR' : "DY",
    'isSignal' : 0,
    'color'    : '#832db6',    # 418 kGreen+2
    'samples'  : ['DY']
}


plot = {}
# keys here must match keys in samples.py    
                    
plot['DY']  = {  
    'nameHR'   : 'DY',
    'color'    : 418,
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.,
}


plot['top']  = {
    'nameHR'   : 'top',
    'color'    : 400,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.,
}


plot['WW']  = {
    'nameHR'   : 'WW',
    'color'    : 851,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['ggWW']  = {
    'nameHR'   : 'ggWW',
    'color'    : 921,
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
legend['lumi'] = 'L =  109.08 fb^{-1}'
legend['sqrt'] = '13.6 TeV'
