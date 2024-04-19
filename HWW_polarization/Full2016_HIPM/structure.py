# structure configuration for datacard

#structure = {}

# keys here must match keys in samples.py    
#                    

structure = {}

structure['DY']  = {  
                  'isSignal' : 0,
                  'isData'   : 0,
              }


structure['Fake']  = {  
                  'isSignal' : 0,
                  'isData'   : 0 
              }

structure['top'] = {   
                  'isSignal' : 0,
                  'isData'   : 0 
                  }


structure['WW']  = {
                  'isSignal' : 0,
                  'isData'   : 0    
                  }

structure['WWewk']  = {
                  'isSignal' : 0,
                  'isData'   : 0
                  }

structure['ggWW']  = {
                  'isSignal' : 0,
                  'isData'   : 0    
                  }


structure['Vg']  = { 
                  'isSignal' : 0,
                  'isData'   : 0 
                  }

structure['VZ']  = { 
                  'isSignal' : 0,
                  'isData'   : 0 
                  }

structure['WZ']  = { 
                  'isSignal' : 0,
                  'isData'   : 0 
                  }


structure['VVV']  = { 
                  'isSignal' : 0,
                  'isData'   : 0 
                  }

structure['ZZ']  = {
                  'isSignal' : 0,
                  'isData'   : 0    
                  }

structure['ggH_hww'] = {
                  'isSignal' : 1,
                  'isData'   : 0,
                  'scaleSampleForDatacard' : {cut : 1.03364 for cut in cuts.keys()}, # XSECxBR correction for mH = 125.38
                  }

structure['qqH_hww'] = {
                  'isSignal' : 1,
                  'isData'   : 0,
                  'scaleSampleForDatacard' : {cut : 1.03621 for cut in cuts.keys()}, # XSECxBR correction for mH = 125.38
                  }


###### POLARIZED SIGNALS

structure['ggH_HWLWL'] = {
                  'isSignal' : 1,
                  'isData'   : 0,
                  'scaleSampleForDatacard' : {cut : 1.03364 for cut in cuts.keys()}, # XSECxBR correction for mH = 125.38
                  }

structure['ggH_HWTWT'] = {
                  'isSignal' : 1,
                  'isData'   : 0,
                  'scaleSampleForDatacard' : {cut : 1.03364 for cut in cuts.keys()}, # XSECxBR correction for mH = 125.38
                  }

'''
structure['ggH_HWW_Int'] = {
                  'isSignal' : 1,
                  'isData'   : 0,
                  'scaleSampleForDatacard' : {cut : 1.03364 for cut in cuts.keys()}, # XSECxBR correction for mH = 125.38                                                                                  
                  }

'''

structure['qqH_HWLWL'] = {
                  'isSignal' : 1,
                  'isData'   : 0,
                  'scaleSampleForDatacard' : {cut : 1.03621 for cut in cuts.keys()}, # XSECxBR correction for mH = 125.38
                  }

structure['qqH_HWTWT'] = {
                  'isSignal' : 1,
                  'isData'   : 0,
                  'scaleSampleForDatacard' : {cut : 1.03621 for cut in cuts.keys()}, # XSECxBR correction for mH = 125.38
                  }


#structure['ggH_gWW_Int'] = {
#    'isSignal' : 1,
#    'isData'   : 0,
#}

#structure['qqH_qqWW_Int'] = {
#    'isSignal' : 1,
#    'isData'   : 0,
#}

structure['ggToWW'] = {
    'isSignal' : 1,
    'isData'   : 0,
}

structure['qqToWW'] = {
    'isSignal' : 1,
    'isData'   : 0,
}

############

structure['WH_hww_plus'] = {
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scaleSampleForDatacard' : {cut : 1.01724 for cut in cuts.keys()}, # XSECxBR correction for mH = 125.38 
                  }

structure['WH_hww_minus'] = {
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scaleSampleForDatacard' : {cut : 1.01724 for cut in cuts.keys()}, # XSECxBR correction for mH = 125.38                                                                                  
                  }

structure['ZH_hww'] = {
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scaleSampleForDatacard' : {cut : 1.01994 for cut in cuts.keys()}, # XSECxBR correction for mH = 125.38
                  }

structure['ggZH_hww'] = {
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scaleSampleForDatacard' : {cut : 1.02494 for cut in cuts.keys()}, # XSECxBR correction for mH = 125.38
                  }

structure['H_hww'] = {
                  'isSignal' : 0,
                  'isData'   : 0    
                  }

structure['bbH_hww'] = {
                  'isSignal' : 0,
                  'isData'   : 0
                  }

structure['ttH_hww'] = {
                  'isSignal' : 0,
                  'isData'   : 0
                  }

structure['ggH_htt'] = {
                  'isSignal' : 0,
                  'isData'   : 0,
                  }

structure['qqH_htt'] = {
                  'isSignal' : 0,
                  'isData'   : 0,
                  }

structure['WH_htt_plus'] = {
                  'isSignal' : 0,
                  'isData'   : 0,
                  }

structure['WH_htt_minus'] = {
                  'isSignal' : 0,
                  'isData'   : 0,
                  }

structure['ZH_htt'] = {
                  'isSignal' : 0,
                  'isData'   : 0,
                  }



structure['DATA']  = { 
                  'isSignal' : 0,
                  'isData'   : 1 
              }

for nuis in nuisances.values():
    if 'cutspost' in nuis:
        nuis['cuts'] = nuis['cutspost']
