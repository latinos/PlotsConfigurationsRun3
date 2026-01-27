# structure configuration for datacard

# keys here must match keys in samples.py    
                    
signal_normalization = 1.0

# BTag normalization factors
# Cut = hww2l2v_13TeV_samesign_1j
scale_histo_ttH_hww      = 0.278463585073/0.198399064164     # 1.40355291617
scale_histo_WW           = 11.9240135473/11.8936383035       # 1.0025539068
scale_histo_DY           = 23.7998453643/24.13561201         # 0.986088330988
scale_histo_WZ           = 217.377574697/214.112860961       # 1.01524763025
scale_histo_Wg           = 192.104240751/188.453876959       # 1.01937006472
scale_histo_Zg           = 18.2835418169/18.0335635947       # 1.01386183163
scale_histo_Vg           = (192.104240751+18.2835418169)/(188.453876959+18.0335635947)
scale_histo_WgS          = 102.259372051/100.766688696       # 1.01481326194
scale_histo_ZgS          = 7.73643537408/7.69800467123       # 1.00499229404
scale_histo_VgS          = (102.259372051+7.73643537408)/(100.766688696+7.69800467123)
scale_histo_ZH_htt       = 0.382145552294/0.366986989934     # 1.0413054489
scale_histo_WH_hww_minus = 3.97872061159/3.86678267178       # 1.0289485987
scale_histo_ggZH_hww     = 0.024401131945/0.0244469872582    # 0.99812429594
scale_histo_qqH_hww      = 0.0332415686758/0.0307787139725   # 1.08001811594
scale_histo_ZZ           = 19.0898027537/18.6698592152       # 1.02249312829
scale_histo_ggH_hww      = 0.390363058603/0.370950665958     # 1.0523314673
scale_histo_WH_htt_minus = 1.48038721595/1.44664552462       # 1.02332409064
scale_histo_VVV          = 7.16275029065/6.9746646703        # 1.0269669768
scale_histo_WH_hww_plus  = 6.57352403872/6.397406968         # 1.02752944616
scale_histo_ggH_htt      = 0.0964261129201/0.0961659672328   # 1.00270517414
scale_histo_qqH_htt      = 0.00592310688963/0.00504034422224 # 1.17513936122
scale_histo_ggWW         = 0.834000198004/0.824596610464     # 1.01140386393
scale_histo_top          = 88.7100329809/66.5443631655       # 1.33309612957
scale_histo_WWewk        = 0.0861724390405/0.0866167563057   # 0.994870308193
scale_histo_ZH_hww       = 0.966494221804/0.921496482209     # 1.04883115721
scale_histo_WH_htt_plus  = 2.21316388717/2.18382148893       # 1.01343626225

structure = {}

structure['Vg']  = { 
    'isSignal' : 0,
    'isData'   : 0,
    'scaleSampleForDatacard' : scale_histo_Vg,
}

structure['VgS']  = {
    'isSignal' : 0,
    'isData'   : 0,
    'scaleSampleForDatacard' : scale_histo_VgS,
}

structure['WZ'] = {
    'isSignal' : 0,
    'isData'   : 0,
    'scaleSampleForDatacard' : scale_histo_WZ * 1.138 # NLO -> NNLO k-factor
}

structure['ZZ']  = { 
    'isSignal' : 0,
    'isData'   : 0,
    'scaleSampleForDatacard' : scale_histo_ZZ,
}

structure['VVV']  = { 
    'isSignal' : 0,
    'isData'   : 0,
    'scaleSampleForDatacard' : scale_histo_VVV,
}


# Higgs
structure['ggH_hww'] = {
    'isSignal' : 0,
    'isData'   : 0,
    'scaleSampleForDatacard' : scale_histo_ggH_hww,
}

structure['qqH_hww'] = {
    'isSignal' : 0,
    'isData'   : 0,
    'scaleSampleForDatacard' : scale_histo_qqH_hww,
}

structure['ZH_hww'] = {
    'isSignal' : 0,
    'isData'   : 0,
    'scaleSampleForDatacard' : scale_histo_ZH_hww,
}

structure['ggZH_hww'] = {
    'isSignal' : 0,
    'isData'   : 0,
    'scaleSampleForDatacard' : scale_histo_ggZH_hww,
}

structure['WH_hww_plus'] = {
    'isSignal' : 1,
    'isData'   : 0,
    'scaleSampleForDatacard' : scale_histo_WH_hww_plus*signal_normalization,
}

structure['WH_hww_minus'] = {
    'isSignal' : 1,
    'isData'   : 0,
    'scaleSampleForDatacard' : scale_histo_WH_hww_minus*signal_normalization,
}

structure['ttH_hww'] = {
    'isSignal' : 0,
    'isData'   : 0,
    'scaleSampleForDatacard' : scale_histo_ttH_hww,
}

structure['ggH_htt'] = {
    'isSignal' : 0,
    'isData'   : 0,
    'scaleSampleForDatacard' : scale_histo_ggH_htt,
}

structure['qqH_htt'] = {
    'isSignal' : 0,
    'isData'   : 0,
    'scaleSampleForDatacard' : scale_histo_qqH_htt,
}

structure['ZH_htt'] = {
    'isSignal' : 0,
    'isData'   : 0,
    'scaleSampleForDatacard' : scale_histo_ZH_htt,
}

structure['WH_htt_plus'] = {
    'isSignal' : 1,
    'isData'   : 0,
    'scaleSampleForDatacard' : scale_histo_WH_htt_plus*signal_normalization,
}

structure['WH_htt_minus'] = {
    'isSignal' : 1,
    'isData'   : 0,
    'scaleSampleForDatacard' : scale_histo_WH_htt_minus*signal_normalization,
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


# Data-driven charge flip estimation
structure['ChargeFlip']  = {  
    'isSignal' : 0,
    'isData'   : 0,
    'scaleSampleForDatacard' : 0.5,
}

# Data
structure['DATA']  = { 
    'isSignal' : 0,
    'isData'   : 1 
}
