
plot = {}

groupPlot = {}
bkgs_to_plot = ['top', 'WWjj_QCD', 'ggWW', 'dytt', 'Vg', 'VgS_H', 'VgS_L', 'VZ', 'VVV', 'Fake_e', 'Fake_m', 
                'qqH_hww', 'ggH_hww', 'ZH_hww', 'WH_hww', 'ggZH_hww', 'ttH_hww']

groupPlot['Backgrounds']  = {
                  #'nameHR' : 'Other backgrounds',
                  'nameHR' : 'Backgrounds',
                  'isSignal' : 0,
                  'color': 920,    # kGray
                  'samples'  : bkgs_to_plot,
}

groupPlot['WWewk_CMWW_LL']  = {  
    'nameHR' : 'VBS LL (CMWW)',
    'isSignal' : 1,
    'color'    : 632,   # kRed
    'samples'  : ['WWewk_CMWW_LL'],
    'drawNormalized': 1
}

groupPlot['WWewk_CMWW_TX']  = {
    'nameHR' : 'VBS TX (CMWW)',
    'isSignal' : 1,
    'color'    : 600, # kBlue
    'samples'  : ['WWewk_CMWW_TT', 'WWewk_CMWW_LT', 'WWewk_CMWW_TL'],
    #'drawNormalized': 1
}

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

samples_to_plot = [ 'WWewk_CMWW_LL', 'WWewk_CMWW_LT', 'WWewk_CMWW_TL', 'WWewk_CMWW_TT', 'top', 'WWjj_QCD', 'ggWW', 
                    'dytt', 'Vg', 'VgS_H', 'VgS_L', 'VZ', 'VVV', 'Fake_e', 'Fake_m', 
                    'qqH_hww', 'ggH_hww', 'ZH_hww', 'WH_hww', 'ggZH_hww', 'ttH_hww']

for sample in samples_to_plot:
  plot[sample] = {
                  'nameHR' : 'name',
                  'color': 418 ,  
                  'isSignal' : 0,
                  'isData'   : 0, 
      }

plot['DATA']  = { 
                  'nameHR' : 'Data',
                  'color': 1 ,  
                  'isSignal' : 0,
                  'isData'   : 1 ,
                  'isBlind'  : 0,
                  'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
              }
legend = {}
legend['lumi'] = 'L = 59.83 fb^{-1}'

legend['sqrt'] = '#sqrt{s} = 13 TeV'


