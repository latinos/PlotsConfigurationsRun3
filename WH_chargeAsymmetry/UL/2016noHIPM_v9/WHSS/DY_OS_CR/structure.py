# structure configuration for datacard

# keys here must match keys in samples.py    
                    
structure = {}

structure['DY']  = {  
    'isSignal' : 0,
    'isData'   : 0,
}

structure['top'] = {   
    'isSignal' : 0,
    'isData'   : 0,
}

structure['WW']  = {
    'isSignal' : 0,
    'isData'   : 0,
}

structure['WWewk']  = {
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

structure['VgS']  = {
    'isSignal' : 0,
    'isData'   : 0,
}

structure['WZ'] = {
    'isSignal' : 0,
    'isData'   : 0,
    'scaleSampleForDatacard' : 1.138 # NLO -> NNLO k-factor
}

structure['ZZ']  = { 
    'isSignal' : 0,
    'isData'   : 0,
}

structure['VVV']  = { 
    'isSignal' : 0,
    'isData'   : 0,
}


# Higgs
structure['ggH_hww'] = {
    'isSignal' : 0,
    'isData'   : 0,
}

structure['qqH_hww'] = {
    'isSignal' : 0,
    'isData'   : 0,
}

structure['ZH_hww'] = {
    'isSignal' : 0,
    'isData'   : 0,
}

structure['ggZH_hww'] = {
    'isSignal' : 0,
    'isData'   : 0,
}

structure['WH_hww_plus'] = {
    'isSignal' : 1,
    'isData'   : 0,
    'scaleSampleForDatacard' : 10 # scaling signal to have sensitivity
}

structure['WH_hww_minus'] = {
    'isSignal' : 1,
    'isData'   : 0,
    'scaleSampleForDatacard' : 10 # scaling signal to have sensitivity
}

structure['ttH_hww'] = {
    'isSignal' : 0,
    'isData'   : 0,
}

structure['ggH_htt'] = {
    'isSignal' : 0,
    'isData'   : 0,
}

structure['qqH_htt'] = {
    'isSignal' : 0,
    'isData'   : 0,
}

structure['ZH_htt'] = {
    'isSignal' : 0,
    'isData'   : 0,
}

structure['WH_htt_plus'] = {
    'isSignal' : 1,
    'isData'   : 0,
    'scaleSampleForDatacard' : 10 # scaling signal to have sensitivity
}

structure['WH_htt_minus'] = {
    'isSignal' : 1,
    'isData'   : 0,
    'scaleSampleForDatacard' : 10 # scaling signal to have sensitivity
}


# Fakes
structure['Fake_ee']  = {
    'isSignal' : 0,
    'isData'   : 0,
}

structure['Fake_mm']  = {
    'isSignal' : 0,
    'isData'   : 0,
}

structure['Fake_em']  = {
    'isSignal' : 0,
    'isData'   : 0,
}


# Data
structure['DATA']  = { 
    'isSignal' : 0,
    'isData'   : 1 
}
