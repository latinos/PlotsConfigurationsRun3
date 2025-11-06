# plot configuration

# Groups of samples to improve the plots.
# If not defined, normal plots is used

groupPlot = {}

groupPlot['Fake']  = {  
    'nameHR'   : 'Non-prompt',
    'isSignal' : 0,
    'color'    : 921,    # kGray + 1
    'samples'  : ['Fake_mm','Fake_em','Fake_ee']
}

groupPlot['DY']  = {  
    'nameHR'   : "DY",
    'isSignal' : 0,
    'color'    : 418,    # kGreen+2
    'samples'  : ['DY']
}

groupPlot['VVV']  = {  
    'nameHR'   : 'VVV',
    'isSignal' : 0,
    'color'    : 857, # kAzure -3  
    'samples'  : ['VVV']
}

groupPlot['ZZ']  = {  
    'nameHR'   : "ZZ",
    'isSignal' : 0,
    'color'    : 617,   # kViolet + 1  
    'samples'  : ['ZZ']
}

groupPlot['WZ']  = {    
    'nameHR'   : "WZ",
    'isSignal' : 0,
    'color'    : 619,   # kViolet + 1  
    'samples'  : ['WZ']
}

groupPlot['Vg']  = {
    'nameHR' : "V#gamma",
    'isSignal' : 0,
    'color'    : 810,   # kOrange + 10
    'samples'  : ['Vg']
}

groupPlot['VgS']  = {
    'nameHR'   : "V#gamma*",
    'isSignal' : 0,
    'color'    : 412,   # kGreen - 9
    'samples'  : ['VgS']
}

groupPlot['Higgs']  = {  
    'nameHR'   : 'Higgs',
    'isSignal' : 0,
    'color'    : 632, # kRed 
    'samples'  : ['ggH_hww','qqH_hww','ZH_hww','ggZH_hww','ttH_hww','ggH_htt','qqH_htt','ZH_htt']
}

groupPlot['WH_minus']  = {  
    'nameHR'   : 'W^{-} H (x 10)',
    'isSignal' : 2,
    'color'    : 600, # kBlue 
    'samples'  : ['WH_hww_minus','WH_htt_minus']
}

groupPlot['WH_plus']  = {  
    'nameHR'   : 'W^{+} H (x 10)',
    'isSignal' : 2,
    'color'    : 632, # kRed 
    'samples'  : ['WH_hww_plus', 'WH_htt_plus']
}


# keys here must match keys in samples.py    

plot = {}

plot['DY']  = {  
    'nameHR'   : 'DY',
    'color'    : 418,    # kGreen+2
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.0,
}

plot['Vg']  = {
    'nameHR'   : 'Vg',
    'color'    : 859, # kAzure -1  
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0
}

plot['VgS'] = { 
    'nameHR'   : 'VgS',
    'color'    : 617, # kViolet + 1  
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0
}

plot['WZ']  = {
    'nameHR'   : 'WZ',
    'color'    : 858, # kAzure -2  
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.138 # NLO -> NNLO k-factor!
}

plot['ZZ']  = { 
    'nameHR'   : 'ZZ',
    'color'    : 858, # kAzure -2  
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0
}

plot['VVV']  = { 
    'nameHR'   : 'VVV',
    'color'    : 857, # kAzure -3  
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0
}

###########
# Signals #
###########

# HWW 

plot['ggH_hww'] = {
    'nameHR'   : 'ggH_hww',
    'color'    : 632, # kRed 
    'isSignal' : 0,
    'isData'   : 0,    
    'scale'    : 1
}

plot['qqH_hww'] = {
    'nameHR'   : 'qqH_hww',
    'color'    : 632+1, # kRed+1 
    'isSignal' : 0,
    'isData'   : 0,    
    'scale'    : 1
}

plot['ZH_hww'] = {
    'nameHR'   : 'ZH_hww',
    'color'    : 632+3, # kRed+3 
    'isSignal' : 0,
    'isData'   : 0,    
    'scale'    : 1
}

plot['ggZH_hww'] = {
    'nameHR'   : 'ggZH_hww',
    'color'    : 632+4, # kRed+4
    'isSignal' : 0,
    'isData'   : 0,    
    'scale'    : 1
}

plot['WH_hww_plus'] = {
    'nameHR'   : 'WH_hww_plus',
    'color'    : 632+2, # kRed+2 
    'isSignal' : 2,
    'isData'   : 0,    
    'scale'    : 10
}

plot['WH_hww_minus'] = {
    'nameHR'   : 'WH_hww_minus',
    'color'    : 600, # kBlue 
    'isSignal' : 2,
    'isData'   : 0,    
    'scale'    : 10
}

plot['ttH_hww'] = {
    'nameHR'   : 'ttH_hww',
    'color'    : 632+3, # kRed+3 
    'isSignal' : 0,
    'isData'   : 0,    
    'scale'    : 1
}


# Htautau

plot['ggH_htt'] = {
    'nameHR'   : 'ggH_htt',
    'color'    : 632, # kRed 
    'isSignal' : 0,
    'isData'   : 0,    
    'scale'    : 1
}

plot['qqH_htt'] = {
    'nameHR'   : 'qqH_htt',
    'color'    : 632+1, # kRed+1 
    'isSignal' : 0,
    'isData'   : 0,    
    'scale'    : 1
}

plot['ZH_htt'] = {
    'nameHR'   : 'ZH_htt',
    'color'    : 632+3, # kRed+3 
    'isSignal' : 0,
    'isData'   : 0,    
    'scale'    : 1
}

plot['WH_htt_plus'] = {
    'nameHR'   : 'WH_htt_plus',
    'color'    : 632+2, # kRed+2 
    'isSignal' : 2,
    'isData'   : 0,    
    'scale'    : 10
}

plot['WH_htt_minus'] = {
    'nameHR'   : 'WH_htt_minus',
    'color'    : 632+2, # kRed+2 
    'isSignal' : 2,
    'isData'   : 0,    
    'scale'    : 10
}


########
# Fake #
########

plot['Fake_em']  = {  
    'nameHR'   : 'Fake_em',
    'color'    : 921,    # kGray + 1
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0                  
}

plot['Fake_ee']  = {  
    'nameHR'   : 'Fake_ee',
    'color'    : 921,    # kGray + 1
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0                  
}

plot['Fake_mm']  = { 
    'nameHR'   : 'Fake_mm',
    'color'    : 921,    # kGray + 1
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0                  
}

# plot['Fake']  = { 
#     'color'    : 921,    # kGray + 1
#     'isSignal' : 0,
#     'isData'   : 0,
#     'scale'    : 1.0                  
# }

########
# Data #
########

plot['DATA']  = { 
    'nameHR'   : 'Data',
    'color'    : 1 ,  
    'isSignal' : 0,
    'isData'   : 1,
    'isBlind'  : 0
}


# Define legend

legend = {}

legend['lumi'] = 'L = 41.5 fb^{-1}'
legend['sqrt'] = '#sqrt{s} = 13 TeV'
