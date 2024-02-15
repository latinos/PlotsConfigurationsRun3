# structure configuration for datacard

structure = {}

# keys here must match keys in samples.py    
#                    


chi_mass_step = 50
mpoints = []

for sb_mass in sb_masses:
  start_chi_mass = 200 if sb_mass==300 else 400
  for chi_mass in [200 + i*50 for i in range(int((sb_mass-start_chi_mass)/chi_mass_step))]:
    for slep_mass in [chi_mass - 10 - i*20 for i in range(4)]:

        structure['RPV_sb'+str(sb_mass)+'_chi'+str(chi_mass)+'_sl'+str(slep_mass)] = {
                  'isSignal' : 1,
                  'isData'   : 0,
                  'scaleSampleForDatacard' : 0.001, 
                }

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

structure['ttH_hww']  = {
                  'isSignal' : 0,
                  'isData'   : 0
                  }

structure['sig']  = {
                  'isSignal' : 1,
                  'isData'   : 0,
                  'parametric' : 1,
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
