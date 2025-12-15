# variables

# 0 = not fold (default), 1 = fold underflowbin, 2 = fold overflow bin, 3 = fold underflow and overflow
    
variables = {}

variables['events'] = {
    'name'  : '1',      
    'range' : (1,0,2),  
    'xaxis' : 'events', 
    'fold'  : 3
}

# 1 jet binning
variables['mlljj20_whss_1j_bin'] = {
    'name'  : 'mlljj20_whss',
    'range' : ([60.,70.,80.,90.,100.,110.,120.,130.,140.,150.,160.,170.,180.,190.,200.,250.,300.],),
    'xaxis' : 'mlljj20_whss [GeV]',
    'fold'  : 3
}

# 2 jets binning
variables['mlljj20_whss_2j_bin'] = {
    'name'  : 'mlljj20_whss',
    'range' : ([60.,120.,130.,140.,150.,160.,170.,180.,190.,200.,250.,300.],),
    'xaxis' : 'mlljj20_whss [GeV]',
    'fold'  : 3
}

########################################################
# Default BDT training but with TopSemileptonic as fakes
########################################################

variables['BDTG6_TT'] = {
    'name'     : 'BDT_WHSS_TopSemileptonic_v9',     
    'range'    : (40,-1,1),   
    'doWeight' : 1,
    'binX'     : 1,
    'binY'     : 40,
    'xaxis'    : 'BDT discriminant',
    'yaxis'    : 'Events',
    'fold'     : 3
}

variables['BDTG6_TT_0_75'] = {
    'name'  : 'BDT_WHSS_TopSemileptonic_v9',     
    'range' : ([-1.0, -0.5, -0.25, 0.0, 0.25, 0.5, 0.75, 1.0],),
    'xaxis' : 'BDT discriminant',
    'fold'  : 3
}

# em 1j ge, mm 1j ge
variables['BDTG6_TT_0_6'] = {
    'name'  : 'BDT_WHSS_TopSemileptonic_v9',     
    'range' : ([-1.0, -0.2, 0.2, 0.6, 1.0],),
    'xaxis' : 'BDT discriminant',
    'fold'  : 3
}

# em 2j ge, em 1j lt, mm 1j lt, ee 1j ge, mm 2j ge
variables['BDTG6_TT_0_5'] = {
    'name'  : 'BDT_WHSS_TopSemileptonic_v9',     
    'range' : ([-1.0, 0.0, 0.5, 1.0],),
    'xaxis' : 'BDT discriminant',
    'fold'  : 3
}

# ee 2j ge, em 2j lt, mm 2j lt, ee 1j lt, ee 2j lt
variables['BDTG6_TT_0_0'] = {
    'name'  : 'BDT_WHSS_TopSemileptonic_v9',     
    'range' : ([-1.0, 0.0, 1.0],),
    'xaxis' : 'BDT discriminant',
    'fold'  : 3
}

###################
# Control variables
###################

variables['mll'] = {
    'name'  : 'mll',
    'range' : (20, 40,120),
    'xaxis' : 'm_{ll} [GeV]',
    'fold'  : 0
}

variables['mjj'] = {
    'name'  : 'mjj*(CleanJet_pt[1]>30)',
    'range' : (50,0,400),
    'xaxis' : 'm_{jj} [GeV]',
    'fold'  : 3
}

variables['mtw1'] = {
    'name'  : 'mtw1',
    'range' : (40,0,200),
    'xaxis' : 'm_{T}^{W_{1}} [GeV]',
    'fold'  : 3
}

variables['mtw2'] = {
    'name'  : 'mtw2',
    'range' : (40,0,200),
    'xaxis' : 'm_{T}^{W_{2}} [GeV]',
    'fold'  : 3
}

variables['ptll'] = {
    'name'  : 'ptll',     
    'range' : (40, 0,200),   
    'xaxis' : 'p_{T}^{ll} [GeV]',
    'fold'  : 0
}

variables['mlljj20_whss'] = {
    'name'  : 'mlljj20_whss',
    'range' : (50, 0, 1000),
    'xaxis' : 'mlljj20_whss [GeV]',
    'fold'  : 3
}

variables['puppimet'] = {
    'name'  : 'PuppiMET_pt',    
    'range' : (20,0,200),
    'xaxis' : 'PUPPI met [GeV]',
    'fold'  : 3
}

variables['dphill']  = {  
    'name'  : 'abs(dphill)',     
    'range' : (20,0,3.14),   
    'xaxis' : '#Delta#phi_{ll}',
    'fold'  : 3
}

variables['dphijj'] = {
    'name'  : 'dphijj',
    'range' : (20,0,3.2),
    'xaxis' : 'dphijj',
    'fold'  : 3
}

variables['dphillmet'] = {
    'name'  : 'dphillmet',
    'range' : (20,0,3.2),
    'xaxis' : 'dphillmet',
    'fold'  : 3
}

variables['dphilmet2'] = {
    'name'  : 'dphilmet2',
    'range' : (20,0,3.2),
    'xaxis' : 'dphilmet2',
    'fold'  : 3
}

variables['dphijet1met'] = {
    'name'  : 'dphijet1met',
    'range' : (20,0,3.2),
    'xaxis' : 'dphijet1met',
    'fold'  : 3
}

variables['DeepCSV_jet1'] = {
    'name'  : 'Alt(Jet_btagDeepB,CleanJet_jetIdx[0],-2)',
    'range' : (50,0.0,1.0),
    'xaxis' : 'Leading jet DeepCSV',
    'fold'  : 3
}

variables['DeepCSV_jet2'] = {
    'name'  : 'Alt(Jet_btagDeepB,CleanJet_jetIdx[1],-2)',
    'range' : (50,0.0,1.0),
    'xaxis' : 'Sub-leading jet DeepCSV',
    'fold'  : 3
}
