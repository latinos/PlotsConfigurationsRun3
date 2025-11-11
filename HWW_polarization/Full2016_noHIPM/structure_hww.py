# structure configuration for datacard

#structure = {}

# keys here must match keys in samples.py    
#                    

structure = {}

structure['DY']  = {  
                  'isSignal' : 0,
                  'isData'   : 0,
              }

structure['Dyemb']  = {
                  'isSignal' : 0,
                  'isData'   : 0,
              }

structure['top'] = {   
                  'isSignal' : 0,
                  'isData'   : 0 
                  }


structure['WW_minnlo']  = {
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

structure['ZZ']  = {
                  'isSignal' : 0,
                  'isData'   : 0
                  }

structure['Vg']  = { 
                  'isSignal' : 0,
                  'isData'   : 0 
                  }

structure['VgS'] = { 
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

############

structure['hww'] = {
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scaleSampleForDatacard' : {cut : 1.03621 for cut in cuts.keys()}, # XSECxBR correction for mH = 125.38 
                  }

structure['htt'] = {
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scaleSampleForDatacard' : {cut : 1.03621 for cut in cuts.keys()}, # XSECxBR correction for mH = 125.38                                                                                  
                  }

structure['Fake']  = {
                  'isSignal' : 0,
                  'isData'   : 0
              }

structure['DATA']  = { 
                  'isSignal' : 0,
                  'isData'   : 1 
              }


for nuis in nuisances.values():
    if 'cutspost' in nuis:
        print(nuis)
        nuis['cuts'] = nuis['cutspost']
        print(nuis)

        
        
