

groupPlot = {}



groupPlot['qqH_hww']  = {
                  'nameHR' : "Higgs VBF",
                  'isSignal' : 2,
                  'color'    : 632,   # kBlue                                                                                                                                                              
                  'samples'  : ['qqH_hww']
              }

plot = {}


#vbf fid e non fid

plot['qqH_hww'] = {
    'nameHR' : 'qqH',
    'color': 632, # kRed
    'isSignal' : 1,
    'isData'   : 0,    
    'scale'    : 1,
}


#plot['DATA']  = { 
#                  'nameHR' : 'Data',
#                  'color': 1 ,  
#                  'isSignal' : 0,
#                  'isData'   : 1 ,
#                  'isBlind'  : 0
#                  }

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


# additional options
legend = {}

legend['lumi'] = 'L =  59.8 fb^{-1}'

legend['sqrt'] = '#sqrt{s} = 13 TeV'
