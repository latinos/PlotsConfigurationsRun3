groupPlot = {}

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

"""
groupPlot['Fake']  = {
    'nameHR' : 'nonprompt',
    'isSignal' : 0,
    'color': '#94a4a2',    # 921 kGray + 1                                                                                                                          
    'samples'  : ['Fake']
}
"""

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

"""
groupPlot['VVV']  = {
    'nameHR' : 'VVV',
    'isSignal' : 0,
    'color': 857, # kAzure -3
    'samples'  : ['VVV']
}
"""

groupPlot['VZ']  = {
    'nameHR' : "VZ",
    'isSignal' : 0,
    'color'    : '#a96b59',   # 617 kViolet + 1 
    'samples'  : ['WZ', 'ZZ']
}


groupPlot['HWW']  = {
    'nameHR' : "Higgs",
    'isSignal' : 1,
    'color'    : '#bd1f01',   # 632 kRed
    'samples'  : ['ggH_hww', 'qqH_hww']
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

"""
plot['Fake']  = {
    'nameHR'   : 'nonprompt',
    'color'    : 921,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}
"""

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

"""
plot['VVV']  = {
    'nameHR'   : 'VVV',
    'color'    : 857,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}
"""

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
legend['lumi'] = 'L =  8.0 fb^{-1}'
legend['sqrt'] = '#sqrt{s} = 13.6 TeV'
