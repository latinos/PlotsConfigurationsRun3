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

structure['WWewk']  = { # WWewk_si
                  'isSignal' : 0,
                  'isData'   : 0
                  }

structure['ggWW']  = { # ggWW_si
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


###### POLARIZED SIGNALS

#structure['ggH_fL_1p0_fPerp_0p0'] = {
#    'isSignal' : 2,
#    'isData'   : 0,
#    'scaleSampleForDatacard' : {cut : 1.03621 for cut in cuts.keys()}, # XSECxBR correction for mH = 125.38
#}
#
#structure['qqH_fL_1p0_fPerp_0p0'] = {
#    'isSignal' : 2,
#    'isData'   : 0,
#    'scaleSampleForDatacard' : {cut : 1.03621 for cut in cuts.keys()},
#}

index = 2
for i in np.linspace(-1, 1, 201):
    jlim = round(1.0 - abs(i), 2)
    if abs(round(i,2)) == 1.0:
        jlist = [jlim]
    else:
        jlist = [-jlim, 0.0, jlim]

    for j in jlist:
        i = round(i, 2)
        j = round(j, 2)

        if i<0.0:
            itxt = str(i).replace("-", "m")
        else:
            itxt = str(i)
        itxt = itxt.replace(".", "p")

        if j<0.0:
            jtxt = str(j).replace("-", "m")
        else:
            jtxt = str(j)
        jtxt = jtxt.replace(".", "p")

        txt = f"_fL_{itxt}_fPerp_{jtxt}"

        structure[f'ggH{txt}'] = {
            'isSignal' : index,
            'isData'   : 0,
            'scaleSampleForDatacard' : {cut : 1.03621 for cut in cuts.keys()}, 
        }
        structure[f'qqH{txt}'] = {
            'isSignal' : index,
            'isData'   : 0,
            'scaleSampleForDatacard' : {cut : 1.03621 for cut in cuts.keys()},
        }
        
    index = index + 1


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

        
        
