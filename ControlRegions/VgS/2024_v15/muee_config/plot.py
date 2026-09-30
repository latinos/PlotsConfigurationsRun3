groupPlot = {}

groupPlot['DY']  = {
    'nameHR'   : "DY",
    'isSignal' : 0,
    'color'    : 418, # 418 kGreen+2
    'samples'  : ['DY']
}

groupPlot['Zg']  = {
    'nameHR'   : 'Z#gamma',
    'isSignal' : 0,
    'color'    : 434,
    'samples'  : ['Zg']
}

groupPlot['top']  = {
    'nameHR'   : 'top',
    'isSignal' : 0,
    'color'    : 400, # 400 kYellow                           
    'samples'  : ['top']
}

groupPlot['WW']  = {
    'nameHR'   : 'WW',
    'isSignal' : 0,
    'color'    : 851, # 851 kAzure -9
    'samples'  : ['WW', 'ggWW']
}

groupPlot['ZZ']  = {
    'nameHR'   : "ZZ",
    'isSignal' : 0,
    'color'    : 801, # kOrange + 1
    'samples'  : ['ZZ']
}

groupPlot['Wg']  = {
    'nameHR'   : 'W#gamma',
    'isSignal' : 0,
    'color'    : 617, # kViolet + 1
    'samples'  : ['Wg']
}

groupPlot['ZgS']  = {
    'nameHR'   : 'Z#gamma*',
    'isSignal' : 0,
    'color'    : 433, # kCyan + 1
    'samples'  : ['ZgS']
}

groupPlot['VVV']  = {
    'nameHR'   : "VVV",
    'isSignal' : 0,
    'color'    : 619, # kViolet + 3
    'samples'  : ['VVV']
}

groupPlot['WgS']  = {
    'nameHR'   : 'W#gamma*',
    'isSignal' : 0,
    'color'    : 633, # kRed + 1
    'samples'  : ['WgS']
}

groupPlot['WZ']  = {
    'nameHR'   : "WZ",
    'isSignal' : 0,
    'color'    : "#8d0000", 
    'samples'  : ['WZ']
}

# groupPlot['Fake']  = {
#     'nameHR'   : 'nonprompt',
#     'isSignal' : 0,
#     'color'    : 921,
#     'samples'  : ['Fake']
# }


# keys here must match keys in samples.py    
                    
plot = {}

plot['DY']  = {  
    'nameHR'   : 'DY',
    'color'    : 418,
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.,
}

plot['Zg']  = {
    'nameHR'   : 'Zg',
    'color'    : 436,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
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

plot['ZZ']  = {
    'nameHR'   : 'ZZ',
    'color'    : 801, # kOrange + 1
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['Wg']  = {
    'nameHR'   : 'Wg',
    'color'    : 617, # kViolet + 1
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['ZgS']  = {
    'nameHR'   : 'ZgS',
    'color'    : 858,
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

plot['WZ']  = {
    'nameHR'   : 'WZ',
    'color'    : "#8d0000",
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['WgS']  = {
    'nameHR'   : 'WgS',
    'color'    : 858,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

# plot['Fake']  = {
#     'nameHR'   : 'nonprompt',
#     'color'    : 921,
#     'isSignal' : 0,
#     'isData'   : 0,
#     'scale'    : 1.0,
# }



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
