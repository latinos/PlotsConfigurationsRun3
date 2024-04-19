

groupPlot = {}
plot = {}

# groupPlot = {}
# 
# Groups of samples to improve the plots.
# If not defined, normal plots is used
#


groupPlot['top']  = {  
                  'nameHR' : 'tW and t#bar{t}',
                  'isSignal' : 0,
                  'color': 400,   # kYellow
                  'samples'  : ['top']
              }

groupPlot['WW']  = {  
                  'nameHR' : 'WW',
                  'isSignal' : 0,
                  'color': 851, # kAzure -9 
                  'samples'  : ['WW', 'ggWW', 'WWewk']
              }

groupPlot['Fake']  = {
                  'nameHR' : 'nonprompt',
                  'isSignal' : 0,
                  'color': 921,    # kGray + 1
                  # 'samples'  : ['Fake_me', 'Fake_em']
                  'samples'  : ['Fake']
}


groupPlot['DY']  = {  
                  'nameHR' : "DY",
                  'isSignal' : 0,
                  'color': 418,    # kGreen+2
                  'samples'  : ['DY']
              }



groupPlot['VVV']  = {  
                  'nameHR' : 'VVV',
                  'isSignal' : 0,
                  'color': 857, # kAzure -3  
                  'samples'  : ['VVV']
              }


groupPlot['VZ']  = {  
                  'nameHR' : "VZ",
                  'isSignal' : 0,
                  'color'    : 617,   # kViolet + 1  
                  'samples'  : ['WZ', 'ZZ']
              }

groupPlot['Vg']  = {  
                  'nameHR' : "V#gamma",
                  'isSignal' : 0,
                  'color'    : 810,   # kOrange + 10
                  'samples'  : ['Vg']
              }

'''
groupPlot['ggF']  = {
                  'nameHR' : "ggF",
                  'isSignal' : 0,
                  'color'    : 623,
                  'samples'  : ['ggH_hww']
              }
'''

groupPlot['VBF']  = {
                  'nameHR' : "VBF",
                  'isSignal' : 0,
                  'color'    : 600,
                  'samples'  : ['qqH_hww']
              }


groupPlot['ggH_HWLWL']  = {
                  'nameHR' : "ggF: LL",
                  'isSignal' : 1,
                  'color'    : 600,
                  'samples'  : ['ggH_HWLWL']
              }

groupPlot['ggH_HWTWT']  = {
                  'nameHR' : "ggF: TT",
                  'isSignal' : 2,
                  'color'    : 632,
                  'samples'  : ['ggH_HWTWT']
              }

'''
groupPlot['ggH_HWW_Int']  = {
                  'nameHR' : "ggF: Int.",
                  'isSignal' : 1,
                  'color'    : 921,
                  'samples'  : ['ggH_HWW_Int']
              }

'''


'''
groupPlot['qqH_HWLWL']  = {
                  'nameHR' : "VBF: LL",
                  'isSignal' : 0,
                  'color'    : 600+1,
                  'samples'  : ['qqH_HWLWL']
              }


groupPlot['qqH_HWTWT']  = {
                  'nameHR' : "VBF H #to W_{T}W_{T}",
                  'isSignal' : 1,
                  'color'    : 632+1,
                  'samples'  : ['qqH_HWTWT']
              }


groupPlot['qqH_HWW_Int']  = {
                  'nameHR' : "ggF: Int",
                  'isSignal' : 0,
                  'color'    : 921+1,
                  'samples'  : ['qqH_HWW_Int']
              }


groupPlot['qqH_HWW_TTInt']  = {
                  'nameHR' : "VBF: TT+Int",
                  'isSignal' : 0,
                  'color'    : 632+1,
                  'samples'  : ['qqH_HWW_TTInt']
              }

'''


groupPlot['Higgs']  = {  
                  'nameHR' : 'Higgs',
                  'isSignal' : 0,
                  'color': 632+3, # kRed 
                  #'samples'  : ['H_htt', 'H_hww', 'ZH_hww', 'ggZH_hww', 'WH_hww','bbH_hww','ttH_hww','ZH_htt', 'ggZH_htt', 'WH_htt', 'qqH_htt', 'ggH_htt','bbH_htt','ttH_htt' ]
                  'samples'  : ['ZH_hww', 'ggZH_hww', 'WH_hww','bbH_hww','ttH_hww', 'qqH_htt', 'ggH_htt', 'ZH_htt', 'WH_htt']
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
                      'hww2l2v_13TeV_WW_0j' : 0.76,
                      'hww2l2v_13TeV_loose_sr_0j' : 0.76,
                      'hww2l2v_13TeV_medium_sr_0j' : 0.76,
                      'hww2l2v_13TeV_tight_sr_0j' : 0.76,
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


plot['WW']  = {
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

plot['ZH_htt'] = {
                  'nameHR' : 'ZHtt',
                  'color': 632+3, # kRed+3 
                  'isSignal' : 1,
                  'isData'   : 0,    
                  'scale'    : 1    #
                  }

#plot['bbH_htt'] = {
#                  'nameHR' : 'bbHtt',
#                  'color': 632-1, # kRed-1 
#                  'isSignal' : 1,
#                  'isData'   : 0,
#                  'scale'    : 1    #
#                  }
#
#plot['ttH_htt'] = {
#                  'nameHR' : 'bbHtt',
#                  'color': 632-2, # kRed-1 
#                  'isSignal' : 1,
#                  'isData'   : 0,
#                  'scale'    : 1    #
#                  }
#
#
#plot['ggZH_htt'] = {
#                  'nameHR' : 'ggZHtt',
#                  'color': 632+4, # kRed+4
#                  'isSignal' : 1,
#                  'isData'   : 0,    
#                  'scale'    : 1    #
#                  }

plot['WH_htt'] = {
                  'nameHR' : 'WHtt',
                  'color': 632+2, # kRed+2 
                  'isSignal' : 0,
                  'isData'   : 0,    
                  'scale'    : 1    #
                  }


plot['qqH_htt'] = {
                  'nameHR' : 'qqHtt',
                  'color': 632+1, # kRed+1 
                  'isSignal' : 0,
                  'isData'   : 0,    
                  'scale'    : 1    #
                  }


plot['ggH_htt'] = {
                  'nameHR' : 'ggHtt',
                  'color': 632, # kRed 
                  'isSignal' : 0,
                  'isData'   : 0,    
                  'scale'    : 1    #
                  }

# HWW 

#plot['H_hww'] = {
#                  'nameHR' : 'Hww',
#                  'color': 632, # kRed 
#                  'isSignal' : 1,
#                  'isData'   : 0,    
#                  'scale'    : 1    #
#                  }

plot['ZH_hww'] = {
                  'nameHR' : 'ZH',
                  'color': 632+3, # kRed+3 
                  'isSignal' : 0,
                  'isData'   : 0,    
                  'scale'    : 1    #
                  }

plot['ggZH_hww'] = {
                  'nameHR' : 'ggZH',
                  'color': 632+4, # kRed+4
                  'isSignal' : 0,
                  'isData'   : 0,    
                  'scale'    : 1    #
                  }

plot['WH_hww'] = {
                  'nameHR' : 'WH',
                  'color': 632+2, # kRed+2 
                  'isSignal' : 0,
                  'isData'   : 0,    
                  'scale'    : 1    #
                  }



plot['qqH_hww'] = {
                  'nameHR' : 'qqH',
                  'color': 632+1, # kRed+1 
                  'isSignal' : 0,
                  'isData'   : 0,    
                  'scale'    : 1    #
                  }

'''
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


'''
plot['ggH_HWW_Int'] = {
                  'nameHR' : 'ggH Int',
                  'color': 632,
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scale'    : 1
}



plot['qqH_HWLWL'] = {
                  'nameHR' : 'qqH',
                  'color': 600+1, # kRed+1 
                  'isSignal' : 0,
                  'isData'   : 0,    
                  'scale'    : 1    #
                  }


plot['qqH_HWTWT'] = {
                  'nameHR' : 'qqH',
                  'color': 632+1, 
                  'isSignal' : 1,
                  'isData'   : 0,    
                  'scale'    : 1   
                  }


plot['qqH_HWW_TTInt'] = {
                  'nameHR' : 'VBF HWW TT+Int',
                  'color': 632,
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scale'    : 1
                  }


plot['qqH_HWW_Int'] = {
                  'nameHR' : 'VBF HWW Int',
                  'color': 632,
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scale'    : 1
                  }

'''


#plot['bbH_hww'] = {
#                  'nameHR' : 'bbH',
#                  'color': 632+5, # kRed+5 
#                  'isSignal' : 1,
#                  'isData'   : 0,
#                  'scale'    : 1    #
#                  }

plot['ttH_hww'] = {
                  'nameHR' : 'ttH',
                  'color': 632+6, # kRed+6
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scale'    : 1    #
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

legend['lumi'] = 'L = 16.8/fb'

legend['sqrt'] = '#sqrt{s} = 13 TeV'
