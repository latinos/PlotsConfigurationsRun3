# structure configuration for datacard

structure = {}

# keys here must match keys in samples.py    
#                    

structure['dytt']  = {  
                  'isSignal' : 0,
                  'isData'   : 0
              }



structure['Fake_e']  = {  
                  'isSignal' : 0,
                  'isData'   : 0,
#                  'removeFromCuts' : [ k for k in cuts if 'me' in k],
              }

structure['Fake_m']  = {  
                  'isSignal' : 0,
                  'isData'   : 0,
#                  'removeFromCuts' : [ k for k in cuts if 'em' in k],
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

# structure['Wg']  = { 
#                   'isSignal' : 0,
#                   'isData'   : 0 
#                   }

structure['Vg']  = { 
                  'isSignal' : 0,
                  'isData'   : 0 
                  }

# structure['VgS'] = { 
#                   'isSignal' : 0,
#                   'isData'   : 0 
#                   }

structure['VgS_L'] = {
                  'isSignal' : 0,
                  'isData'   : 0
                  }

structure['VgS_H'] = {
                  'isSignal' : 0,
                  'isData'   : 0
                  }

# structure['Zg']  = { 
#                   'isSignal' : 0,
#                   'isData'   : 0 
#                   }

structure['VZ']  = { 
                  'isSignal' : 0,
                  'isData'   : 0 
                  }

# structure['WZ']  = { 
#                   'isSignal' : 0,
#                   'isData'   : 0 
#                   }


structure['VVV']  = { 
                  'isSignal' : 0,
                  'isData'   : 0 
                  }

# structure['ZZ']  = {
#                   'isSignal' : 0,
#                   'isData'   : 0    
#                   }

### qqH ###
structure['qqH_hww_GenDeltaPhijj_0fid'] = {
                  'isSignal' : 1,
                  'isData'   : 0    
                  }

structure['qqH_hww_GenDeltaPhijj_1fid'] = {
                  'isSignal' : 1,
                  'isData'   : 0    
                  }

structure['qqH_hww_GenDeltaPhijj_2fid'] = {
                  'isSignal' : 1,
                  'isData'   : 0    
                  }

structure['qqH_hww_GenDeltaPhijj_3fid'] = {
                  'isSignal' : 1,
                  'isData'   : 0    
                  }
structure['qqH_hww_GenDeltaPhijj_0nonfid'] = {
                  'isSignal' : 1,
                  'isData'   : 0    
                  }

structure['qqH_hww_GenDeltaPhijj_1nonfid'] = {
                  'isSignal' : 1,
                  'isData'   : 0    
                  }

structure['qqH_hww_GenDeltaPhijj_2nonfid'] = {
                  'isSignal' : 1,
                  'isData'   : 0    
                  }

structure['qqH_hww_GenDeltaPhijj_3nonfid'] = {
                  'isSignal' : 1,
                  'isData'   : 0    
                  }
                  
structure['qqH_hww_noGenDeltaPhijj'] = {
                  'isSignal' : 1,
                  'isData'   : 0    
                  }





### BSM ###

structure['GGHjj_H0M_GenDeltaPhijj_0fid'] = {
    'isSignal' : 1,
    'isData'   : 0    
}

structure['GGHjj_H0M_GenDeltaPhijj_1fid'] = {
    'isSignal' : 1,
    'isData'   : 0    
}

structure['GGHjj_H0M_GenDeltaPhijj_2fid'] = {
    'isSignal' : 1,
    'isData'   : 0    
}

structure['GGHjj_H0M_GenDeltaPhijj_3fid'] = {
    'isSignal' : 1,
    'isData'   : 0    
}
structure['GGHjj_H0M_GenDeltaPhijj_0nonfid'] = {
    'isSignal' : 1,
    'isData'   : 0    
}

structure['GGHjj_H0M_GenDeltaPhijj_1nonfid'] = {
    'isSignal' : 1,
    'isData'   : 0    
}

structure['GGHjj_H0M_GenDeltaPhijj_2nonfid'] = {
    'isSignal' : 1,
    'isData'   : 0    
}

structure['GGHjj_H0M_GenDeltaPhijj_3nonfid'] = {
    'isSignal' : 1,
    'isData'   : 0    
}

structure['GGHjj_H0M_noGenDeltaPhijj'] = {
    'isSignal' : 0,
    'isData'   : 0    
}


structure['ZH_hww'] = {
                  'isSignal' : 0,
                  'isData'   : 0    
                  }

structure['ggZH_hww'] = {
                  'isSignal' : 0,
                  'isData'   : 0    
                  }

structure['WH_hww'] = {
                  'isSignal' : 0,
                  'isData'   : 0    
                  }

structure['ttH_hww'] = {
                  'isSignal' : 0,
                  'isData'   : 0
                  }

structure['ggH_htt'] = {
                  'isSignal' : 0,
                  'isData'   : 0
                  }

structure['qqH_htt'] = {
                  'isSignal' : 0,
                  'isData'   : 0
                  }

# data


structure['DATA']  = { 
                  'isSignal' : 0,
                  'isData'   : 1 
              }


'''
print "INSTRUCTURE"
print cuts
#print nuisances['WWresum0j']
print "OK"

for nuis in nuisances.itervalues():
  if 'cutspost' in nuis:
    nuis['cuts'] = nuis['cutspost'](nuis, cuts)

    print nuis
'''
