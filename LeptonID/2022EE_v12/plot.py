# Group plots

groupPlot = {}

groupPlot['WJets']  = {
    'nameHR'   : 'WJets',
    'isSignal' : 0,
    'color'    : 921, # kGray+1
    'samples'  : ['WJets'],
}

groupPlot['TTToSemiLeptonic']  = {
    'nameHR'   : 'Top',
    'isSignal' : 0,
    'color'    : 400, # kYellow
    'samples'  : ['TTToSemiLeptonic'],
}

groupPlot['WW']  = {
    'nameHR'   : 'WW',
    'isSignal' : 0,
    'color'    : 851, # kAzure -9
    'samples'  : ['WW'],
}

groupPlot['ggH_hww']  = {
    'nameHR'   : 'ggF',
    'isSignal' : 0,
    'color'    : 632, # kRed
    'samples'  : ['ggH_hww'],
}

# Plots

plot = {}

plot['WJets']  = {
    'nameHR'   : 'WJets',
    'color'    : 921,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

plot['TTToSemiLeptonic']  = {
    'nameHR'   : 'Top',
    'color'    : 400,
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

plot['ggH_hww']  = {
    'nameHR'   : 'ggF',
    'color'    : 632,
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0,
}

# Legend definition
legend = {}
legend['lumi'] = ''
legend['sqrt'] = '#sqrt{s} = 13.6 TeV'
