# plot configuration

# BTag normalization factors
# Cut = wh3l_13TeV_ossf
scale_histo_ttH_hww      = 0.207326433653/0.170436879391   # 1.21644115049
scale_histo_WW           = 4.37024213423/4.34843379119     # 1.00501521791
scale_histo_DY           = 177.031320945/178.901628736     # 0.989545607806
scale_histo_WZ           = 256.955904208/251.837951959     # 1.0203224026
scale_histo_Wg           = 0.882308031899/0.882308031899   # 1.0
scale_histo_Zg           = 99.7614355404/97.4174861687     # 1.02406086899
scale_histo_Vg           = (99.7614355404+0.882308031899)/(97.4174861687+0.882308031899)
scale_histo_WgS          = 0.581382768902/0.562793014361   # 1.03303124607
scale_histo_ZgS          = 82.2681341524/80.4951733094     # 1.02202567893
scale_histo_VgS          = (82.2681341524+0.581382768902)/(80.4951733094+0.562793014361)
scale_histo_ZH_htt       = 0.321566818356/0.303203443179   # 1.06056453378
scale_histo_WH_htt_plus  = 1.63099405363/1.59659557382     # 1.02154489238
scale_histo_ggZH_hww     = 0.081267203464/0.0780232420435  # 1.04157686012
scale_histo_qqH_hww      = 0.0143895084463/0.0141931431929 # 1.01383521963
scale_histo_ZZ           = 19.0250543863/18.3740327613     # 1.03543161338
scale_histo_ggH_hww      = 0.198651131575/0.175196065144   # 1.13387895676
scale_histo_WH_htt_minus = 1.08936465173/1.05610226306     # 1.0314954241
scale_histo_VVV          = 8.85335748793/8.74920050633     # 1.01190474278
scale_histo_WH_hww_plus  = 7.25252938425/7.11678236006     # 1.01907421322
scale_histo_ggH_htt      = 0.0156947572713/0.0156947572713 # 1.0
scale_histo_ggWW         = 0.489402233956/0.473495546782   # 1.03359416426
scale_histo_top          = 317.29713522/289.863221576      # 1.0946443412
scale_histo_WWewk        = 0.077573268559/0.0757180968947  # 1.02450103397
scale_histo_ZH_hww       = 0.984859182497/0.95501818423    # 1.03124652364
scale_histo_WH_hww_minus = 4.6053082335/4.51958950426      # 1.01896604308
scale_histo_qqH_htt      = 0.0/1.0                         # 0.0

# Groups of samples to improve the plots.
# If not defined, normal plots is used

groupPlot = {}

groupPlot['top']  = {  
    'nameHR'   : 'tW+ and t#bar{t}',
    'isSignal' : 0,
    'color'    : 400,   # kYellow
    'samples'  : ['top']
}

groupPlot['Fake']  = {  
    'nameHR'   : 'Non-prompt',
    'isSignal' : 0,
    'color'    : 921,    # kGray + 1
    'samples'  : ['Fake']
}

groupPlot['WW']  = {  
    'nameHR'   : 'WW',
    'isSignal' : 0,
    'color'    : 851, # kAzure -9 
    'samples'  : ['WW'] # , 'ggWW', 'WWewk']
}

groupPlot['VVV']  = {  
    'nameHR'   : 'VVV',
    'isSignal' : 0,
    'color'    : 857, # kAzure -3  
    'samples'  : ['VVV']
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
    'color'    : 617,
    'samples'  : ['VgS']
}

groupPlot['ZZ']  = {  
    'nameHR'   : "ZZ",
    'isSignal' : 0,
    'color'    : 617,   # kViolet + 1  
    'samples'  : ['ZZ']
}

groupPlot['WZ']  = {    
    'nameHR'   : "WZ",
    'isSignal' : 0,
    'color'    : 619,   # kViolet + 1  
    'samples'  : ['WZ']
}

groupPlot['Higgs']  = {  
    'nameHR'   : 'Higgs',
    'isSignal' : 0,
    'color'    : 632, # kRed 
    'samples'  : ['ggH_hww','qqH_hww','ZH_hww','ggZH_hww','ttH_hww','ggH_hww','qqH_htt','ZH_htt']
}

groupPlot['WH_minus']  = {  
    'nameHR'   : 'W^{-} H (x 10)',
    'isSignal' : 2,
    'color'    : 600, # kBlue 
    'samples'  : ['WH_hww_minus','WH_htt_minus']
}

groupPlot['WH_plus']  = {  
    'nameHR'   : 'W^{+} H (x 10)',
    'isSignal' : 2,
    'color'    : 632, # kRed 
    'samples'  : ['WH_hww_plus', 'WH_htt_plus']
}


# keys here must match keys in samples.py    

plot = {}

plot['top'] = {   
    'nameHR' : 'tW and t#bar{t}',
    'color'    : 400,   # kYellow
    'isSignal' : 0,
    'isData'   : 0, 
    'scale'    : scale_histo_top,
}

plot['WW']  = {
    'color'    : 851, # kAzure -9 
    'isSignal' : 0,
    'isData'   : 0,    
    'scale'    : scale_histo_WW,
}

plot['Vg']  = { 
    'color'    : 859, # kAzure -1  
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : scale_histo_Vg,
}

plot['VgS']  = { 
    'color'    : 859, # kAzure -1  
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : scale_histo_VgS,
}

plot['ZZ']  = { 
    'color'    : 858, # kAzure -2  
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : scale_histo_ZZ,
}

plot['WZ']  = {
    'color'    : 858, # kAzure -2  
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : scale_histo_WZ * 1.138, # NLO->NNLO k-factor!
}

plot['VVV']  = { 
    'color'    : 857, # kAzure -3  
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : scale_histo_VVV,
}

###########
# Signals #
###########

# HWW 

plot['ggH_hww'] = {
    'color'    : 632, # kRed 
    'isSignal' : 0,
    'isData'   : 0,    
    'scale'    : scale_histo_ggH_hww,
}

plot['qqH_hww'] = {
    'color'    : 632+1, # kRed+1 
    'isSignal' : 0,
    'isData'   : 0,    
    'scale'    : scale_histo_qqH_hww,
}

plot['ZH_hww'] = {
    'color'    : 632+3, # kRed+3 
    'isSignal' : 0,
    'isData'   : 0,    
    'scale'    : scale_histo_ZH_hww,
}

plot['ggZH_hww'] = {
    'color'    : 632+4, # kRed+4
    'isSignal' : 0,
    'isData'   : 0,    
    'scale'    : scale_histo_ggZH_hww,
}

plot['WH_hww_minus'] = {
    'color'    : 600, # kBlue 
    'isSignal' : 2,
    'isData'   : 0,    
    'scale'    : 10.0 * scale_histo_WH_hww_minus,
}

plot['WH_hww_plus'] = {
    'color'    : 632+2, # kRed+2 
    'isSignal' : 2,
    'isData'   : 0,    
    'scale'    : 10.0 * scale_histo_WH_hww_plus,
}

plot['ttH_hww'] = {
    'color'    : 632+3, # kRed+3 
    'isSignal' : 0,
    'isData'   : 0,    
    'scale'    : scale_histo_ttH_hww,
}

# Htautau

plot['ggH_htt'] = {
    'color'    : 632, # kRed 
    'isSignal' : 0,
    'isData'   : 0,    
    'scale'    : scale_histo_ggH_htt,
}

plot['qqH_htt'] = {
    'color'    : 632+1, # kRed+1
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : scale_histo_qqH_htt,
}

plot['ZH_htt'] = {
    'color'    : 632+3, # kRed+3 
    'isSignal' : 0,
    'isData'   : 0,    
    'scale'    : scale_histo_ZH_htt,
}

plot['WH_htt_plus'] = {
    'color'    : 632+2, # kRed+2
    'isSignal' : 1,
    'isData'   : 0,
    'scale'    : 10.0 * scale_histo_WH_htt_plus,
}

plot['WH_htt_minus'] = {
    'color'    : 632+2, # kRed+2
    'isSignal' : 1,
    'isData'   : 0,
    'scale'    : 10.0 * scale_histo_WH_htt_minus,
}


########
# Fake #
########

plot['Fake']  = { 
    'color'    : 921,    # kGray + 1
    'isSignal' : 0,
    'isData'   : 0,
    'scale'    : 1.0                  
}


########
# Data #
########

plot['DATA']  = { 
    'nameHR'   : 'Data',
    'color'    : 1 ,  
    'isSignal' : 0,
    'isData'   : 1,
    'isBlind'  : 0,
}


# Define legend

legend = {}

legend['lumi'] = 'L = 59.8 fb^{-1}'
legend['sqrt'] = '#sqrt{s} = 13 TeV'
