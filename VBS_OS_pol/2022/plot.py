groupPlot = {}

groupPlot['Higgs']  = {
    'nameHR' : "Higgs",
    'isSignal' : 0,
    'color'    : 632,   # 632 kRed
    'samples'  : ['ggH_hww','qqH_hww']
}

groupPlot['Fake']  = {
    'nameHR' : 'nonprompt',
    'isSignal' : 0,
    'color': 921,    # 921 kGray + 1                                                                                                                          
    'samples'  : ['Fake']
}

groupPlot['Multiboson']  = {
    'nameHR' : 'Multiboson',
    'isSignal' : 0,
    'color': 617,
    'samples'  : ['WZ','ZZ','Wg','Zg','WgS','ZgS','WZS','VVV']
}

groupPlot['DY']  = {
    'nameHR' : "DY",
    'isSignal' : 0,
    'color'    : 418,    # 418 kGreen+2
    'samples'  : ['DY']
}

groupPlot['ggWW']  = {
    'nameHR' : 'ggWW',
    'isSignal' : 0,
    'color': 851, # 851 kAzure -9                                                                                                                                                                                                                                  
    'samples'  : ['ggWW']
}

groupPlot['WW']  = {
    'nameHR' : 'WW',
    'isSignal' : 0,
    'color': '#1f5ea8',
    'samples'  : ['WW']
}

groupPlot['top']  = {
    'nameHR' : 'tW and t#bar{t}',
    'isSignal' : 0,
    'color': 400,   # 400 kYellow                                                                                                                                                                                                                                  
    'samples'  : ['top']
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


plot['Wg']  = {
    'nameHR'   : 'Wg',
    'color'    : 857,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['Zg']  = {
    'nameHR'   : 'Zg',
    'color'    : 857,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['WgS']  = {
    'nameHR'   : 'WgS',
    'color'    : 857,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['ZgS']  = {
    'nameHR'   : 'ZgS',
    'color'    : 857,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['WZS']  = {
    'nameHR'   : 'WZS',
    'color'    : 857,
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

plot['ZZ']  = {
    'nameHR'   : 'ZZ',
    'color'    : 617,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['VVV']  = {
    'nameHR'   : 'VVV',
    'color'    : 617,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

# Higgs

plot['ggH_hww'] = {
    'nameHR'   : 'ggF',
    'color'    : 632,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}


plot['qqH_hww'] = {
    'nameHR'   : 'VBF',
    'color'    : 632,
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
legend['lumi'] = 'L =  8.0 fb^{-1}'
legend['sqrt'] = '13.6 TeV'
