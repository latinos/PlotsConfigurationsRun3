

groupPlot = {}
plot = {}

# groupPlot = {}
# 
# Groups of samples to improve the plots.
# If not defined, normal plots is used
#


groupPlot['top']  = {  
                  'nameHR' : 'tW and $t\overline{t}$',
                  'isSignal' : 0,
                  'color': 400,   # kYellow
                  'colorPlt': "#ffff00",
                  'samples'  : ['top']
              }

groupPlot['WW']  = {  
                  'nameHR' : 'WW',
                  'isSignal' : 0,
                  'color': 851, # kAzure -9
                  'colorPlt': "#87cefa",
                  'samples'  : ['WW_minnlo', 'ggWW', 'WWewk']
              }

groupPlot['Fake']  = {
                  'nameHR' : 'nonprompt',
                  'isSignal' : 0,
                  'color': 921,    # kGray + 1
                  'colorPlt': "#778899",
                  # 'samples'  : ['Fake_me', 'Fake_em']
                  'samples'  : ['Fake']
}


groupPlot['DY']  = {  
                  'nameHR' : "DY",
                  'isSignal' : 0,
                  'color': 418,    # kGreen+2
                  'colorPlt': "#6b8e23",
                  'samples'  : ['DY']
              }



groupPlot['VVV']  = {  
                  'nameHR' : 'VVV',
                  'isSignal' : 0,
                  'color': 857, # kAzure -3
                  'colorPlt': "#4b0082",
                  'samples'  : ['VVV']
              }


groupPlot['VZ']  = {  
                  'nameHR' : "VZ",
                  'isSignal' : 0,
                  'color'    : 617,   # kViolet + 1
                  'colorPlt': "#800080",
                  'samples'  : ['WZ', 'ZZ']
              }

groupPlot['Vg']  = {  
                  'nameHR' : "$V\gamma$",
                  'isSignal' : 0,
                  'color'    : 810,   # kOrange + 10
                  'colorPlt': "#e76300",
                  'samples'  : ['Vg', 'VgS']
              }

#groupPlot['VgS']  = {
#                  'nameHR' : "V#gamma*",
#                  'isSignal' : 0,
#                  'color'    : 409,   # kGreen - 9
#                  'colorPlt': "#e76300",
#                  'samples'  : ['VgS']
#              }


'''
groupPlot['ggF']  = {
                  'nameHR' : "ggF",
                  'isSignal' : 1,
                  'color'    : 623,
                  'colorPlt': "",
                  'samples'  : ['ggH_hww']
              }

groupPlot['VBF']  = {
                  'nameHR' : "VBF",
                  'isSignal' : 1,
                  'color'    : 600,
                  'colorPlt': "",
                  'samples'  : ['qqH_hww']
              }

'''


groupPlot['HWLWL']  = {
                  'nameHR' : "$H->W_{L}^{+}W_{L}^{-}$",
                  'isSignal' : 1,
                  'color'    : 600,
                  'colorPlt': "#7a21dd",
                  'samples'  : ['ggH_HWLWL', 'qqH_HWLWL']
              }

groupPlot['HWTWT']  = {
                  'nameHR' : "$H->W_{T}^{+}W_{T}^{-}$",
                  'isSignal' : 1,
                  'color'    : 632,
                  'colorPlt': "#e42536",
                  'samples'  : ['ggH_HWTWT', 'qqH_HWTWT']
              }


#groupPlot['qqH_HWLWL']  = {
#                  'nameHR' : "VBF: LL",
#                  'isSignal' : 1,
#                  'color'    : 418+1,
#                  'colorPlt': "",
#                  'samples'  : ['qqH_HWLWL']
#              }


#groupPlot['qqH_HWTWT']  = {
#                  'nameHR' : "VBF: TT",
#                  'isSignal' : 1,
#                  'color'    : 632+1,
#                  'colorPlt': "",
#                  'samples'  : ['qqH_HWTWT']
#              }


groupPlot['Higgs']  = {  
                  'nameHR' : 'Other Higgs',
                  'isSignal' : 0,
                  'color': 632+3, # kRed
                  'colorPlt': "#800000",
                  'samples'  : ['hww', 'htt']
              }




#plot = {}

# keys here must match keys in samples.py    
#  


plot['DY']  = {
                  'color': 418,    # kGreen+2
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scale'    : 1.0,
                  'cuts'  : {
                       'hww2l2v_13TeV_top_0j'  : 0.76 ,
                       'hww2l2v_13TeV_dytt_0j' : 0.76 ,
                       'hww2l2v_13TeV_top_1j'  : 0.79 ,
                       'hww2l2v_13TeV_dytt_1j' : 0.79 ,
                       'hww2l2v_13TeV_WW_1j'     : 0.79 ,
                       'hww2l2v_13TeV_WW_noVeto_1j'     : 0.79 ,
                       'hww2l2v_13TeV_WP65_sr_1j' : 0.76,
                       'hww2l2v_13TeV_top_2j'  : 0.76 ,
                       'hww2l2v_13TeV_dytt_2j' : 0.76 ,
                       'hww2l2v_13TeV_WW_2j'     : 0.76 ,
                       'hww2l2v_13TeV_WW_noVeto_2j'     : 0.76 ,
                       'hww2l2v_13TeV_WP75_sr_2j' : 0.76,
                       'hww2l2v_13TeV_top_Inclusive'  : 0.77 ,
                       'hww2l2v_13TeV_dytt_Inclusive' : 0.77 ,
                       'hww2l2v_13TeV_WW_Inclusive'     : 0.77 ,
                        },
}

plot['Fake']  = {
                  'color': 921,    # kGray + 1
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scale'    : 1.0
              }



'''
plot['Fake_me']  = {  
                  'color': 921,    # kGray + 1
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scale'    : 1.0                  
              }
plot['Fake_em']  = {  
                  'color': 921,    # kGray + 1
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scale'    : 1.0                  
              }
'''


plot['top'] = {   
                  'nameHR' : 't#bar{t}',
                  'color': 400,   # kYellow
                  'isSignal' : 0,
                  'isData'   : 0, 
                  'scale'    : 1.0,
                  #'cuts'  : {
                       #'hww2l2v_13TeV_of0j'      : 0.94 ,
                       #'hww2l2v_13TeV_top_of0j'  : 0.94 , 
                       #'hww2l2v_13TeV_dytt_of0j' : 0.94 ,
                       #'hww2l2v_13TeV_em_0j'     : 0.94 , 
                       #'hww2l2v_13TeV_me_0j'     : 0.94 , 
                       ##
                       #'hww2l2v_13TeV_of1j'      : 0.86 ,
                       #'hww2l2v_13TeV_top_of1j'  : 0.86 , 
                       #'hww2l2v_13TeV_dytt_of1j' : 0.86 ,
                       #'hww2l2v_13TeV_em_1j'     : 0.86 , 
                       #'hww2l2v_13TeV_me_1j'     : 0.86 , 
                        #},
                  }


plot['WW_minnlo']  = {
                  'color': 851, # kAzure -9 
                  'isSignal' : 0,
                  'isData'   : 0,    
                  'scale'    : 1.0   # ele/mu trigger efficiency   datadriven
                  }

plot['ggWW']  = {
                  'color': 850, # kAzure -10
                  'isSignal' : 0,
                  'isData'   : 0,    
                  'scale'    : 1.0
                  }

plot['WWewk']  = {
                  'color': 851, # kAzure -9 
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scale'    : 1.0   # ele/mu trigger efficiency   datadriven
                  }


plot['Vg']  = { 
                  'color': 859,
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scale'    : 1.0
                  }

plot['VgS']  = { 
    'color'    : 859, # kAzure -1  
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0
}

plot['ZZ']  = { 
                  'color': 858,
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scale'    : 1.0
                  }

plot['WZ']  = {
                  'color': 858,
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scale'    : 1.0
                  }

plot['VVV']  = { 
                  'color': 857, # kAzure -3  
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scale'    : 1.0
                  }

# Htautau

plot['htt'] = {
                  'nameHR' : 'htt',
                  'color': 632+3, # kRed+3 
                  'isSignal' : 1,
                  'isData'   : 0,    
                  'scale'    : 1    #
                  }


# HWW 

plot['hww'] = {
                  'nameHR' : 'hww',
                  'color': 632+3, # kRed+3 
                  'isSignal' : 0,
                  'isData'   : 0,    
                  'scale'    : 1    #
                  }

'''
plot['qqH_hww'] = {
                  'nameHR' : 'qqH',
                  'color': 632+1, # kRed+1 
                  'isSignal' : 0,
                  'isData'   : 0,    
                  'scale'    : 1    #
                  }

plot['ggH_hww'] = {
                  'nameHR' : 'ggH',
                  'color': 632, # kRed 
                  'isSignal' : 0,
                  'isData'   : 0,    
                  'scale'    : 1    #
                  }

'''
###
### POLARIZATION
###


plot['ggH_HWLWL'] = {
                  'nameHR' : 'ggH HWLWL',
                  'color': 600,
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scale'    : 1
                  }

plot['ggH_HWTWT'] = {
                  'nameHR' : 'ggH HWTWT',
                  'color': 632,
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scale'    : 1
                  }


plot['qqH_HWLWL'] = {
                  'nameHR' : 'qqH',
                  'color': 418+1, # kRed+1 
                  'isSignal' : 0,
                  'isData'   : 0,    
                  'scale'    : 1    #
                  }


plot['qqH_HWTWT'] = {
                  'nameHR' : 'qqH',
                  'color': 632+1, 
                  'isSignal' : 0,
                  'isData'   : 0,    
                  'scale'    : 1   
                  }


# data

plot['DATA']  = { 
                  'nameHR' : 'Data',
                  'color': 1 ,  
                  'isSignal' : 0,
                  'isData'   : 1 ,
                  'isBlind'  : 1
              }

# additional options

legend = {}

legend['lumi'] = 'L = 41.5/fb'

legend['sqrt'] = '#sqrt{s} = 13 TeV'
