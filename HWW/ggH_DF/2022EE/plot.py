# Group of plots

groupPlot = {}

groupPlot['DY']  = {  
    'nameHR'   : 'DY',
    'isSignal' : 0,
    'color'    : '#832db6', #kGreen+4
    'samples'  : ['DY']
}

groupPlot['WW']  = {
    'nameHR' : 'WW',
    'isSignal' : 0,
    'color': '#3f90da', # 851 kAzure -9                                                                                                                                                                                                                                  
    'samples'  : ['WW']
}

groupPlot['ttbar']  = {
    'nameHR' : 't#bar{t}',
    'isSignal' : 0,
    'color': '#ffa90e',   # 400 kYellow                                                                                                                                                                                                                                  
    'samples'  : ['ttbar']
}

groupPlot['tW']  = {
    'nameHR' : 'tW',
    'isSignal' : 0,
    'color': '#92dadd',   # 400 kYellow                                                                                                                                                                                                                                  
    'samples'  : ['tW']
}

groupPlot['WZ']  = {  
    'nameHR'   : 'WZ',
    'isSignal' : 0,
    'color'    : '#e76300', # kViolet + 1
    'samples'  : ['WZ']
}

groupPlot['ggF']  = {
    'nameHR' : "ggF",
    'isSignal' : 1,
    'color'    : '#bd1f01',   # 632 kRed
    'samples'  : ['ggH_hww', 'qqH_hww']
}

groupPlot['VBF']  = {
    'nameHR' : "VBF",
    'isSignal' : 1,
    'color'    : '#a96b59',   # 632 kRed
    'samples'  : ['qqH_hww']
}

# Plots

plot = {}

plot['DY']  = {  
    'color'    : 418, # kGreen + 2
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.0,
}

plot['ttbar']  = {
    'nameHR'   : 'ttbar',
    'color'    : 400,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.,
}

plot['tW']  = {
    'nameHR'   : 'tW',
    'color'    : 400,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.,
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

# Higgs

plot['ggH_hww'] = {
    'nameHR'   : 'HWW',
    'color'    : 632,
    'isSignal' : 1,
    'isData'   : 0,
    'scale'    : 1.0,
}


plot['qqH_hww'] = {
    'nameHR'   : 'HWW',
    'color'    : 632,
    'isSignal' : 1,
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
legend['lumi'] = 'L =  26.7 fb^{-1}'
legend['sqrt'] = '13.6 TeV'
