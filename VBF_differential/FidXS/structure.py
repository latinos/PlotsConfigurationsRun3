# structure configuration for datacard

structure = {}

# keys here must match keys in samples.py    
#                    

structure['qqH_hww'] = {
                  'isSignal' : 1,
                  'isData'   : 0    
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
