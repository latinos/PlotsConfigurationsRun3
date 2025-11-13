# structure configuration for datacard

structure = {}

# scaleSampleForDatacard
# keys here must match keys in samples.py    
#                    

structure['DY']  = {  
                  'isSignal' : 0,
                  'isData'   : 0,
              }

structure['Fake']  = {  
                  'isSignal' : 0,
                  'isData'   : 0,                 
              }

structure['top'] = {   
                  'isSignal' : 0,
                  'isData'   : 0,
                  }


structure['ggWW']  = {
                  'isSignal' : 0,
                  'isData'   : 0,
                  }


structure['Vg']  = { 
                  'isSignal' : 0,
                  'isData'   : 0,
                  }


structure['VZ']  = { 
                  'isSignal' : 0,
                  'isData'   : 0, 
                  }

structure['WW']  = { 
                  'isSignal' : 0,
                  'isData'   : 0, 
                  }


structure['ggH_hww'] = {
                  'isSignal' : 1,
                  'isData'   : 0,    
                  }

structure['qqH_hww'] = {
                  'isSignal' : 1,
                  'isData'   : 0,  
                  }

# data


structure['DATA']  = { 
                  'isSignal' : 0,
                  'isData'   : 1,
              }