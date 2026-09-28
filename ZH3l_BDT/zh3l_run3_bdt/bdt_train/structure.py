# structure configuration for datacard
# keys here must match keys in samples.py    
structure = {}

# Backgrounds    


structure['WZ']  = { 
                  'isSignal' : 0,
                  'isData'   : 0 
                  }

structure['ZZ']  = { 
                  'isSignal' : 0,
                  'isData'   : 0 
                  }


# Signal
# structure['ZH_hww'] = {
#                   'isSignal' : 1,
#                   'isData'   : 0    
#                   }

structure['ggZH_hww'] = {
                  'isSignal' : 1,
                  'isData'   : 0    
                  }

# Data
structure['DATA']  = { 
                 'isSignal' : 0,
                 'isData'   : 1 
             }




