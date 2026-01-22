groupPlot = {}

groupPlot['top']  = {
    'nameHR' : 'top',
    'isSignal' : 0,
    'color': '#ffa90e',   # 400 kYellow                                                                                                                                                                                                                                  
    'samples'  : ['top']
}


groupPlot['Fake']  = {
    'nameHR' : 'nonprompt',
    'isSignal' : 0,
    'color': '#94a4a2',    # 921 kGray + 1                                                                                                                          
    'samples'  : ['Fake']
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


groupPlot['Vg']  = {
    'nameHR' : 'V#gamma',
    'isSignal' : 0,
    'color': '#e76300', 
    'samples'  : ['Vg']
}

groupPlot['VgS']  = {
    'nameHR' : 'V#gamma*',
    'isSignal' : 0,
    'color': '#92dadd', 
    'samples'  : ['VgS']
}


groupPlot['VZ']  = {
    'nameHR' : "VZ",
    'isSignal' : 0,
    'color'    : '#a96b59',   # 617 kViolet + 1 
    'samples'  : ['WZ', 'ZZ']
}


groupPlot['ggF']  = {
    'nameHR' : "ggF",
    'isSignal' : 1,
    'color'    : '#bd1f01',   # 632 kRed
    'samples'  : ['ggH_hww']
}

groupPlot['VBF']  = {
    'nameHR' : "VBF",
    'isSignal' : 1,
    'color'    : '#b9ac70',   # 632 kRed
    'samples'  : ['qqH_hww']
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

plot['ggWW']  = {
    'nameHR'   : 'ggWW',
    'color'    : 921,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}


plot['Vg']  = {
    'nameHR'   : 'Vg',
    'color'    : 857,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['VgS']  = {
    'nameHR'   : 'VgS',
    'color'    : 858,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}


plot['WZ']  = {
    'nameHR'   : 'WZ',
    'color'    : '#a96b59',
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

"""
plot['ZZ']  = {
    'nameHR'   : 'ZZ',
    'color'    : 617,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}
"""

# Higgs

plot['ggH_hww'] = {
    'nameHR'   : 'ggF',
    'color'    : 632,
    'isSignal' : 1,
    'isData'   : 0,
    'scale'    : 1.0,
}


plot['qqH_hww'] = {
    'nameHR'   : 'VBF',
    'color'    : 632,
    'isSignal' : 1,
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
legend['sqrt'] = '13.6 TeV'
