

groupPlot = {}


groupPlot['top']  = {  
                  'nameHR' : 'tW and t#bar{t}',
                  'isSignal' : 0,
                  #'color': 400,   # kYellow
                  'color': ROOT.kYellow,   # kYellow
                  'samples'  : ['top']
              }



groupPlot['WW']  = {  
    'nameHR' : 'WW',
    'isSignal' : 0,
    'color': 851, # kAzure -9 
    'samples'  : ['WW', 'ggWW']
}




groupPlot['WWewk']  = {
    'nameHR' : 'WWewk',
    'isSignal' : 0,
    'color': 855, # kAzure -10 
    'samples'  : ['WWewk']

}


groupPlot['DY']  = {  
                  'nameHR' : "DYtt",
                  'isSignal' : 0,
                  'color': 418,    # kGreen+2
                  'samples'  : ['dytt']
}

groupPlot['Fake']  = {
                  'nameHR' : 'nonprompt',
                  'isSignal' : 0,
                  'color': 921,    # kGray + 1
                  'samples'  : ['Fake_m', 'Fake_e']
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
                  'samples'  : ['VZ']
              }

groupPlot['Vg']  = {  
                  'nameHR' : "V#gamma",
                  'isSignal' : 0,
                  'color'    : 810,   # kOrange + 10
                  'samples'  : ['Vg']
              }

groupPlot['VgS']  = {
                  'nameHR' : "V#gamma*",
                  'isSignal' : 0,
                  'color'    : 409,   # kGreen - 9
                  'samples'  : ['VgS_H','VgS_L']
              }



# groupPlot['Higgs']  = {  
#                   'nameHR' : 'Higgs',
#                   'isSignal' : 0,
#                   'color': 920, # kRed 
# 		  #'samples'  : ['H_htt', 'H_hww', 'ZH_hww', 'ggZH_hww', 'WH_hww', 'qqH_hww', 'ggH_hww','bbH_hww','ttH_hww','ZH_htt', 'ggZH_htt', 'WH_htt', 'qqH_htt', 'ggH_htt','bbH_htt','ttH_htt' ]
# 		  #'samples'  : ['H_htt', 'H_hww', 'ZH_hww', 'ggZH_hww', 'WH_hww', 'ggH_hww','bbH_hww','ttH_hww', 'qqH_htt', 'ggH_htt' ] with ggH
#                   'samples'  : ['ggZH_hww',' ZH_hww',' WH_hww',' ttH_hww',' qqH_htt',' ggH_htt' ]
#               }

# groupPlot['VBF']  = {
#                   'nameHR' : "Higgs VBF",
#                   'isSignal' : 1,
#                   'color'    : 632,   # kBlue                                                                                                                                                              
#                   'samples'  : ['qqH_hww_GenDeltaPhijj_0fid',' qqH_hww_GenDeltaPhijj_1fid',' qqH_hww_GenDeltaPhijj_2fid',' qqH_hww_GenDeltaPhijj_3fid',' qqH_hww_GenDeltaPhijj_0nonfid',' qqH_hww_GenDeltaPhijj_1nonfid',' qqH_hww_GenDeltaPhijj_2nonfid',' qqH_hww_GenDeltaPhijj_3nonfid ']
#               }


groupPlot['VBF_0']  = {
                  'nameHR' : "Higgs VBF bin 0 ",
                  'isSignal' : 2,
                  'color'    : 632,   # kBlue                                                                                                                                                              
                  'samples'  : ['qqH_hww_GenDeltaPhijj_0fid',' qqH_hww_GenDeltaPhijj_0nonfid']
              }

groupPlot['VBF_1']  = {
                  'nameHR' : "Higgs VBF bin 1 ",
                  'isSignal' : 2,
                  'color'    : 632+3,   # kBlue                                                                                                                                                              
                  'samples'  : ['qqH_hww_GenDeltaPhijj_1fid',' qqH_hww_GenDeltaPhijj_1nonfid']
              }
groupPlot['VBF_2']  = {
                  'nameHR' : "Higgs VBF bin 2 ",
                  'isSignal' : 2,
                  'color'    : 632-6,   # kBlue                                                                                                                                                              
                  'samples'  : ['qqH_hww_GenDeltaPhijj_2fid',' qqH_hww_GenDeltaPhijj_2nonfid']
              }

groupPlot['VBF_3']  = {
                  'nameHR' : "Higgs VBF bin 3 ",
                  'isSignal' : 2,
                  'color'    : 632-10,   # kBlue                                                                                                                                                              
                  'samples'  : ['qqH_hww_GenDeltaPhijj_3fid',' qqH_hww_GenDeltaPhijj_3nonfid']
              }

# groupPlot['ggF']  = {
#                   'nameHR' : "Higgs ggF",
#                   'isSignal' : 2,
#                   'color'    : 600,   #kBlue                                                                                                                                                              
#                   'samples'  : ['ggH_hww_GenDeltaPhijj_0fid',' ggH_hww_GenDeltaPhijj_1fid',' ggH_hww_GenDeltaPhijj_2fid',' ggH_hww_GenDeltaPhijj_3fid',' ggH_hww_GenDeltaPhijj_0nonfid',' ggH_hww_GenDeltaPhijj_1nonfid',' ggH_hww_GenDeltaPhijj_2nonfid',' ggH_hww_GenDeltaPhijj_3nonfid']
#               }

groupPlot['ggH']  = {
                  'nameHR' : "Higgs ggH",
                  'isSignal' : 2,
                  'color'    : 600,   # kBlue                                                                                                                                                              
                  'samples'  : ['ggH_hww_GenDeltaPhijj_0fid',' ggH_hww_GenDeltaPhijj_0nonfid','ggH_hww_GenDeltaPhijj_1fid',' ggH_hww_GenDeltaPhijj_1nonfid','ggH_hww_GenDeltaPhijj_2fid',' ggH_hww_GenDeltaPhijj_2nonfid','ggH_hww_GenDeltaPhijj_3fid',' ggH_hww_GenDeltaPhijj_3nonfid']
              }



# groupPlot['ggH_0']  = {
#                   'nameHR' : "Higgs ggH bin 0 ",
#                   'isSignal' : 2,
#                   'color'    : 632,   # kBlue                                                                                                                                                              
#                   'samples'  : ['ggH_hww_GenDeltaPhijj_0fid',' ggH_hww_GenDeltaPhijj_0nonfid']
#               }

# groupPlot['ggH_1']  = {
#                   'nameHR' : "Higgs ggH bin 1 ",
#                   'isSignal' : 2,
#                   'color'    : 632+3,   # kBlue                                                                                                                                                              
#                   'samples'  : ['ggH_hww_GenDeltaPhijj_1fid',' ggH_hww_GenDeltaPhijj_1nonfid']
#               }
# groupPlot['ggH_2']  = {
#                   'nameHR' : "Higgs ggH bin 2 ",
#                   'isSignal' : 2,
#                   'color'    : 632-6,   # kBlue                                                                                                                                                              
#                   'samples'  : ['ggH_hww_GenDeltaPhijj_2fid',' ggH_hww_GenDeltaPhijj_2nonfid']
#               }

# groupPlot['ggH_3']  = {
#                   'nameHR' : "Higgs ggH bin 3 ",
#                   'isSignal' : 2,
#                   'color'    : 632-10,   # kBlue                                                                                                                                                              
#                   'samples'  : ['ggH_hww_GenDeltaPhijj_3fid',' ggH_hww_GenDeltaPhijj_3nonfid']
#               }









# groupPlot['DATA']  = { 
#                   'nameHR' : 'Data',
#                   'color': 1 ,  
#                   'isSignal' : 0,
#                   'isData'   : 1 ,
#                   'isBlind'  : {
#                       'SR_2j': 'full',
#                       }
# }

plot = {}


#vbf fid e non fid

plot['qqH_hww_GenDeltaPhijj_0fid'] = {
    'nameHR' : 'qqH -#pi <#Delta#phi_{jj,GEN} < -#pi/2',
    'color': 632, # kRed
    'isSignal' : 1,
    'isData'   : 0,    
    'scale'    : 1,
    #'cuts': dict((skey, '0') for skey in ['hww2l2v_13TeV_of2j_dphijj_4bins_vbflike_1','hww2l2v_13TeV_of2j_dphijj_4bins_vbflike_2','hww2l2v_13TeV_of2j_dphijj_4bins_vbflike_3'] )
}

plot['qqH_hww_GenDeltaPhijj_1fid'] = {
    'nameHR' : 'qqH -#pi/2 < #Delta#phi_{jj,GEN} < 0',
    'color': 632+3, # kRed+3 
    'isSignal' : 1,
    'isData'   : 0,    
    'scale'    : 1,
    #'cuts': dict((skey, '0') for skey in ['hww2l2v_13TeV_of2j_dphijj_4bins_vbflike_0','hww2l2v_13TeV_of2j_dphijj_4bins_vbflike_2','hww2l2v_13TeV_of2j_dphijj_4bins_vbflike_3'] )
}

plot['qqH_hww_GenDeltaPhijj_2fid'] = {
    'nameHR' : 'qqH 0 < #Delta#phi_{jj,GEN} < #pi/2',
    'color': 632-6, # kRed-6 
    'isSignal' : 1,
    'isData'   : 0,    
    'scale'    : 1,
    #'cuts': dict((skey, '0') for skey in ['hww2l2v_13TeV_of2j_dphijj_4bins_vbflike_1','hww2l2v_13TeV_of2j_dphijj_4bins_vbflike_0','hww2l2v_13TeV_of2j_dphijj_4bins_vbflike_3'] )
}

plot['qqH_hww_GenDeltaPhijj_3fid'] = {
    'nameHR' : 'qqH #pi/2 <#Delta#phi_{jj,GEN}< #pi',
    'color': 632-10, # kRed-10 
    'isSignal' : 1,
    'isData'   : 0,    
    'scale'    : 1,
    #'cuts': dict((skey, '0') for skey in ['hww2l2v_13TeV_of2j_dphijj_4bins_vbflike_1','hww2l2v_13TeV_of2j_dphijj_4bins_vbflike_2','hww2l2v_13TeV_of2j_dphijj_4bins_vbflike_0'] )
}
plot['qqH_hww_GenDeltaPhijj_0nonfid'] = {
    'nameHR' : 'qqH nonfid -#pi <#Delta#phi_{jj,GEN} < -#pi/2',
    'color': 409, # kRed
    'isSignal' : 1,
    'isData'   : 0,    
    'scale'    : 1,
    #'cuts': dict((skey, '0') for skey in ['hww2l2v_13TeV_of2j_dphijj_4bins_vbflike_1','hww2l2v_13TeV_of2j_dphijj_4bins_vbflike_2','hww2l2v_13TeV_of2j_dphijj_4bins_vbflike_3'] )
}

plot['qqH_hww_GenDeltaPhijj_1nonfid'] = {
    'nameHR' : 'qqH nonfid -#pi/2 < #Delta#phi_{jj,GEN} < 0',
    'color': 416+4, # kRed+3 
    'isSignal' : 1,
    'isData'   : 0,    
    'scale'    : 1,
    #'cuts': dict((skey, '0') for skey in ['hww2l2v_13TeV_of2j_dphijj_4bins_vbflike_0','hww2l2v_13TeV_of2j_dphijj_4bins_vbflike_2','hww2l2v_13TeV_of2j_dphijj_4bins_vbflike_3'] )
}

plot['qqH_hww_GenDeltaPhijj_2nonfid'] = {
    'nameHR' : 'qqH nonfid 0 < #Delta#phi_{jj,GEN} < #pi/2',
    'color': 416-5, # kRed-6 
    'isSignal' : 1,
    'isData'   : 0,    
    'scale'    : 1,
    #'cuts': dict((skey, '0') for skey in ['hww2l2v_13TeV_of2j_dphijj_4bins_vbflike_1','hww2l2v_13TeV_of2j_dphijj_4bins_vbflike_0','hww2l2v_13TeV_of2j_dphijj_4bins_vbflike_3'] )
}

plot['qqH_hww_GenDeltaPhijj_3nonfid'] = {
    'nameHR' : 'qqH #pi/2 <#Delta#phi_{jj,GEN}< #pi',
    'color': 416-10, # kRed-10 
    'isSignal' : 1,
    'isData'   : 0,    
    'scale'    : 1,
    #'cuts': dict((skey, '0') for skey in ['hww2l2v_13TeV_of2j_dphijj_4bins_vbflike_1','hww2l2v_13TeV_of2j_dphijj_4bins_vbflike_2','hww2l2v_13TeV_of2j_dphijj_4bins_vbflike_0'] )
}




#ggh
plot['ggH_hww_GenDeltaPhijj_0fid'] = {
    'nameHR' : 'ggH -#pi <#Delta#phi_{jj,GEN} < -#pi/2',
    'color': 409, # kGreen-7 (416-7)
    'isSignal' : 1,
    'isData'   : 0,    
    'scale'    : 1
}

plot['ggH_hww_GenDeltaPhijj_1fid'] = {
    'nameHR' : 'ggH -#pi/2 < #Delta#phi_{jj,GEN} < 0',
    'color': 416+4, # kGreen+4 
    'isSignal' : 1,
    'isData'   : 0,    
    'scale'    : 1
}

plot['ggH_hww_GenDeltaPhijj_2fid'] = {
    'nameHR' : 'ggH 0 < #Delta#phi_{jj,GEN} < #pi/2',
    'color': 416-5, # kGreen-5 
    'isSignal' : 1,
    'isData'   : 0,    
    'scale'    : 1
}

plot['ggH_hww_GenDeltaPhijj_3fid'] = {
    'nameHR' : 'ggH #pi/2 <#Delta#phi_{jj,GEN}< #pi',
    'color': 416-10, # kGreen-10 
    'isSignal' : 1,
    'isData'   : 0,    
    'scale'    : 1
}

plot['ggH_hww_GenDeltaPhijj_0nonfid'] = {
    'nameHR' : 'ggH -#pi <#Delta#phi_{jj,GEN} < -#pi/2',
    'color': 409, # kGreen-7 (416-7)
    'isSignal' : 1,
    'isData'   : 0,    
    'scale'    : 1
}

plot['ggH_hww_GenDeltaPhijj_1nonfid'] = {
    'nameHR' : 'ggH -#pi/2 < #Delta#phi_{jj,GEN} < 0',
    'color': 420, # kGreen+4 
    'isSignal' : 1,
    'isData'   : 0,    
    'scale'    : 1
}

plot['ggH_hww_GenDeltaPhijj_2nonfid'] = {
    'nameHR' : 'ggH 0 < #Delta#phi_{jj,GEN} < #pi/2',
    'color': 411, # kGreen-5 
    'isSignal' : 1,
    'isData'   : 0,    
    'scale'    : 1
}

plot['ggH_hww_GenDeltaPhijj_3nonfid'] = {
    'nameHR' : 'ggH #pi/2 <#Delta#phi_{jj,GEN}< #pi',
    'color': 416-10, # kGreen-10 
    'isSignal' : 1,
    'isData'   : 0,    
    'scale'    : 1
}

                    
plot['dytt']  = {  
                  'color': 418,    # kGreen+2
                  'isSignal' : 0,
                  'isData'   : 0, 
                  'scale'    : 1.0,
              }


plot['Fake_m']  = {  
                  'color': 921,    # kGray + 1
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scale'    : 1.0                  
              }


plot['Fake_e']  = {  
                  'color': 921,    # kGray + 1
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scale'    : 1.0                  
              }

              
plot['top'] = {   
                  'color': 400,   # kYellow
                  'isSignal' : 0,
                  'isData'   : 0, 
                  'scale'    : 1.0,
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
                  'color': 859, # kAzure -1  
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scale'    : 1.0
                  }

plot['VgS_H'] = { 
                  'color'    : 617,   # kViolet + 1  
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scale'    : 1.0
                  }

plot['VgS_L'] = {
                  'color'    : 617,   # kViolet + 1  
                  'isSignal' : 0,
                  'isData'   : 0,
                  'scale'    : 1.0
                  }


plot['VZ']  = { 
                  'color': 858, # kAzure -2  
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


# plot['ZH_hww'] = {
#                   'color': 923, # kRed+3 
#                   'isSignal' : 0,
#                   'isData'   : 0,    
#                   'scale'    : 1.0    #
#                   }

# plot['ggZH_hww'] = {
#                   'color': 924, # kRed+4
#                   'isSignal' : 0,
#                   'isData'   : 0,    
#                   'scale'    : 1.0    #
#                   }

# plot['WH_hww'] = {
#                   'color': 922, # kRed+2 
#                   'isSignal' : 0,
#                   'isData'   : 0,    
#                   'scale'    : 1.0    #
#                   }


# plot['ttH_hww'] = {
#                  'color': 632+6, # kRed+6
#                  'isSignal' : 1,
#                  'isData'   : 0,
#                  'scale'    : 1    #
#                  }


# # Htautau

# #plot['ZH_htt'] = {
# #                  'nameHR' : 'ZHtt',
# #                  'color': 632+3, # kRed+3 
# #                  'isSignal' : 1,
# #                  'isData'   : 0,    
# #                  'scale'    : 1    #
# #                  }
# #
# #plot['bbH_htt'] = {
# #                  'nameHR' : 'bbHtt',
# #                  'color': 632-1, # kRed-1 
# #                  'isSignal' : 1,
# #                  'isData'   : 0,
# #                  'scale'    : 1    #
# #                  }
# #
# #plot['ttH_htt'] = {
# #                  'nameHR' : 'bbHtt',
# #                  'color': 632-2, # kRed-1 
# #                  'isSignal' : 1,
# #                  'isData'   : 0,
# #                  'scale'    : 1    #
# #                  }
# #
# #
# #plot['ggZH_htt'] = {
# #                  'nameHR' : 'ggZHtt',
# #                  'color': 632+4, # kRed+4
# #                  'isSignal' : 1,
# #                  'isData'   : 0,    
# #                  'scale'    : 1    #
# #                  }
# #
# #plot['WH_htt'] = {
# #                  'nameHR' : 'WHtt',
# #                  'color': 632+2, # kRed+2 
# #                  'isSignal' : 1,
# #                  'isData'   : 0,    
# #                  'scale'    : 1    #
# #                  }
# #

# plot['qqH_htt'] = {
#                  'nameHR' : 'qqHtt',
#                  'color': 632+1, # kRed+1 
#                  'isSignal' : 1,
#                  'isData'   : 0,    
#                  'scale'    : 1    #
#                  }


# plot['ggH_htt'] = {
#                  'nameHR' : 'ggHtt',
#                  'color': 632, # kRed 
#                  'isSignal' : 1,
#                  'isData'   : 0,    
#                  'scale'    : 1    #
#                  }


plot['DATA']  = { 
                  'nameHR' : 'Data',
                  'color': 1 ,  
                  'isSignal' : 0,
                  'isData'   : 1 ,
                  'isBlind'  : 0
                  }

# merge cuts
_mergedCuts = []
for cut in list(cuts.keys()):
    __cutExpr = ''
    if type(cuts[cut]) == dict:
        __cutExpr = cuts[cut]['expr']
        for cat in list(cuts[cut]['categories'].keys()):
            _mergedCuts.append(cut + '_' + cat)
    elif type(cuts[cut]) == str:
        _mergedCuts.append(cut)

cuts2j = _mergedCuts


# additional options
legend = {}

legend['lumi'] = 'L =  59.8 fb^{-1}'

legend['sqrt'] = '#sqrt{s} = 13 TeV'
