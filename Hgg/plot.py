groupPlot = {}

groupPlot['Fake']  = {
    'nameHR' : 'nonprompt',
    'isSignal' : 0,
    'color': 921,    # kGray + 1
    'samples'  : ['Fake_m', 'Fake_e']
}

groupPlot['top']  = {  
    'nameHR' : 'tW and t#bar{t}',
    'isSignal' : 0,
    #'color': 400,   # kYellow
    'color': ROOT.kYellow,   # kYellow
    'samples'  : ['top']
}


# # _i = 0
# # for dy in dys.keys():
# #     groupPlot[dy] = {
# #         'nameHR': dy,
# #         'isSignal': 0,
# #         'color': ROOT.kGreen - 7 + _i,
# #         'samples': ['DY_' + dy]
# #     }
# #     _i +=1

# groupPlot['DY_hardJets']  = {  
#     'nameHR'   : 'DY_hardJets',
#     'isSignal' : 0,
#     'color'    : ROOT.kGreen-7,
#     'samples'  : ['DY_hardJets']
# }

# groupPlot['DY_PUJets']  = {  
#     'nameHR'   : 'DY_PUJets',
#     'isSignal' : 0,
#     'color'    : ROOT.kGreen-6,
#     'samples'  : ['DY_PUJets']
# }

groupPlot['DY'] = {
    'nameHR'   : 'DY',
    'isSignal' : 0,
    'color'    : ROOT.kGreen-7,
    'samples'  : ['DY']
}



groupPlot['Multiboson']  = {  
    'nameHR' : 'Multiboson',
    'isSignal' : 0,
    'color': 617, # kViolet + 1  
    #'samples'  : ['WWewk','WW', 'ggWW', 'VVV', 'VZ', 'WZ', 'ZZ', 'Vg', 'Wg', 'VgS_H', 'VgS_L']
    'samples'  : ['WWewk','WW', 'ggWW', 'Vg', 'VgS_H', 'VgS_L', 'VZ', 'VVV']
    #'VVV', 'VZ', 'WZ', 'ZZ', 'Vg', 'Wg', 'VgS_H', 'VgS_L']
}

groupPlot['Zjj']  = {  
    'nameHR': 'Zjj',
    'isSignal' : 1,
    'color': 600,    # kBlue
    'samples'    : ['Zjj']
}

# groupPlot['DATA']  = { 
#     'nameHR'   : 'Data',
#     'color'    : 1 ,  
#     'isSignal' : 0,
#     'isData'   : 1 ,
#     'isBlind'  : {
#         'sr_ee': 'full',
#         'sr_mm': 'full',
#     },
#     'samples' : ['DATA']
# }

plot = {}

plot['Zjj'] = {   
    'color': 400,   # kYellow
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.0,
}

plot['top'] = {   
    'color': 400,   # kYellow
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.0,
}

# plot['DY_hardJets'] = {   
#     'color': 400,   # kYellow
#     'isSignal' : 0,
#     'isData'   : 0, 
#     'scale'    : 1.0,
# }

# plot['DY_PUJets'] = {   
#     'color': 400,   # kYellow
#     'isSignal' : 0,
#     'isData'   : 0, 
#     'scale'    : 1.0,
# }

plot['DY'] = {   
    'color': 400,   # kYellow
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.0,
}

plot['WW'] = {   
    'color': 400,   # kYellow
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.0,
}

plot['ggWW'] = {   
    'color': 400,   # kYellow
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.0,
}

plot['Vg'] = {   
    'color': 400,   # kYellow
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.0,
}

plot['VgS_H'] = {   
    'color': 400,   # kYellow
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.0,
}

plot['VgS_L'] = {   
    'color': 400,   # kYellow
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.0,
}

plot['VZ'] = {   
    'color': 400,   # kYellow
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.0,
}

plot['VVV'] = {   
    'color': 400,   # kYellow
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.0,
}

plot['WWewk'] = {   
    'color': 400,   # kYellow
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.0,
}

plot['Fake_e'] = {   
    'color': 400,   # kYellow
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.0,
}

plot['Fake_m'] = {   
    'color': 400,   # kYellow
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : 1.0,
}

# plot['DATA'] = {   
#     'color': 400,   # kYellow
#     'isSignal' : 0,
#     'isData'   : 0, 
#     'scale'    : 1.0,
# }


# merge cuts
_mergedCuts = []
for cut in list(cuts.keys()):
    __cutExpr = ''
    if type(cuts[cut]) == dict:
        __cutExpr = cuts[cut]['expr']
        for cat in list(cuts[cut]['categories'].keys()):
            _mergedCuts.append(cut + '_' + cat)
    elif type(cuts[cut]) == str:
        _mergedCuts.append(cut)

cuts2j = _mergedCuts
cuts2j_ee = list(filter(lambda k: k.endswith('ee'), cuts2j))
cuts2j_mm = list(filter(lambda k: k.endswith('mm'), cuts2j))
cuts2j_sr = list(filter(lambda k: k.startswith('sr'), cuts2j))
cuts2j_cr = list(set(cuts2j).difference(set(cuts2j_sr)))
#
plot['DATA']  = { 
    'nameHR'   : 'Data',
    'color'    : 1 ,  
    'isSignal' : 0,
    'isData'   : 1 ,
    'isBlind'  : 0,
    'blind'    :  dict([(cut, 'full') for cut in cuts2j_sr])
}

legend = {}
legend['lumi'] = 'L = 59.83 fb^{-1}'

legend['sqrt'] = '#sqrt{s} = 13 TeV'
