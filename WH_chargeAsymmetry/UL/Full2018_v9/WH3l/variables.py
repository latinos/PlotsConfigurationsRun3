# variables

# 0 = not fold (default), 1 = fold underflowbin, 2 = fold overflow bin, 3 = fold underflow and overflow
    
variables = {}

variables['events'] = {
    'name'  : '1',      
    'range' : (1,0,2),  
    'xaxis' : 'events', 
    'fold'  : 3
}

###################
# Control variables
###################

variables['jetpt1'] = {
    'name': 'CleanJet_pt[0]*(CleanJet_pt[0]>30)',
    'range' : (10,0.,200),
    'xaxis' : 'p_{T} 1st jet [GeV]',
    'fold' : 0
}

variables['pt1'] = {
    'name': 'Alt(Lepton_pt, 0, 0)',
    'range' : (10,0.,200),
    'xaxis' : 'p_{T} 1st lep [GeV]',
    'fold' : 0
}

variables['pt2'] = {
    'name': 'Alt(Lepton_pt, 1, 0)',
    'range' : (10,0.,200),
    'xaxis' : 'p_{T} 2nd lep [GeV]',
    'fold' : 0
}

variables['pt3'] = {
    'name': 'Alt(Lepton_pt, 2, 0)',
    'range' : (7,0.,100),
    'xaxis' : 'p_{T} 3rd lep [GeV]',
    'fold' : 0
}

variables['puppimet'] = {
    'name'  : 'PuppiMET_pt',    
    'range' : (20,0,200),
    'xaxis' : 'PUPPI met [GeV]',
    'fold'  : 3
}

variables['WH3l_ptlll'] = {
    'name'  : 'WH3l_ptlll',
    'range' : (10,0,400),
    'xaxis' : 'WH3l ptlll [GeV]',
    'fold'  : 0
}

# DeltaPhi(l,met)
variables['WH3l_dphilmet0'] = {
    'name': 'Alt(WH3l_dphilmet, 0, 0)',
    'range' : (10,0,5),
    'xaxis' : '#Delta #Phi_{l1,met}',
    'fold' : 0
}

variables['WH3l_dphilmet1'] = {
    'name': 'Alt(WH3l_dphilmet, 1, 0)',
    'range' : (10,0,5),
    'xaxis' : '#Delta #Phi_{l2,met}',
    'fold' : 0
}

variables['WH3l_dphilmet2'] = {
    'name': 'Alt(WH3l_dphilmet, 2, 0)',
    'range' : (10,0,5),
    'xaxis' : '#Delta #Phi_{l3,met}',
    'fold' : 0
}

# variables['min_WH3l_dphilmet'] = {
#     'name': 'MinIf$( WH3l_dphilmet[], WH3l_dphilmet[Iteration$] > 0)',
#     'range' : (10,0,5),
#     'xaxis' : 'min #Delta #Phi_{l,met}',
#     'fold' : 0
# }

# DeltaPhi(OS leptons)
variables['WH3l_drOSll0'] = {
    'name': 'Alt(WH3l_drOSll, 0, 0)',
    'range' : (10,0,5),
    'xaxis' : '#Delta R_{l1,l2}',
    'fold' : 0
}

variables['WH3l_drOSll1'] = {
    'name': 'Alt(WH3l_drOSll, 1, 0)',
    'range' : (10,0,5),
    'xaxis' : '#Delta R_{l2,l3}',
    'fold' : 0
}

variables['WH3l_drOSll2'] = {
    'name': 'Alt(WH3l_drOSll, 2, 0)',
    'range' : (10,0,5),
    'xaxis' : '#Delta R_{l2,l3}',
    'fold' : 0
}

# variables['min_WH3l_drOSll'] = {
#     'name': 'MinIf$( WH3l_drOSll[], WH3l_drOSll[Iteration$] > 0)',
#     'range' : (10,0,5),
#     'xaxis' : 'min #Delta R(OS lepton pairs)',
#     'fold' : 0
# }

# m(OS lepton pairs)
variables['WH3l_mOSll0'] = {
    'name': 'Alt(WH3l_mOSll, 0, 0)',
    'range' : (10,0,400),
    'xaxis' : 'm_{l1,l2}',
    'fold' : 0
}

variables['WH3l_mOSll1'] = {
    'name': 'Alt(WH3l_mOSll, 1, 0)',
    'range' : (10,0,400),
    'xaxis' : 'm_{l2,l3}',
    'fold' : 0
}

variables['WH3l_mOSll2'] = {
    'name': 'Alt(WH3l_mOSll, 2, 0)',
    'range' : (10,0,400),
    'xaxis' : 'm_{l2,l3}',
    'fold' : 0
}

# variables['min_WH3l_mOSll'] = {
#     'name': 'MinIf$( WH3l_mOSll[], WH3l_mOSll[Iteration$] > 0)',
#     'range' : (10,0,400),
#     'xaxis' : 'min m(OS lepton pairs)',
#     'fold' : 0
# }

# pT(OS lepton pairs)
variables['WH3l_ptOSll0'] = {
    'name': 'Alt(WH3l_ptOSll, 0, 0)',
    'range' : (10,0,400),
    'xaxis' : 'p_T^{l1,l2}',
    'fold' : 0
}

variables['WH3l_ptOSll1'] = {
    'name': 'Alt(WH3l_ptOSll, 1, 0)',
    'range' : (10,0,400),
    'xaxis' : 'p_T^{l2,l3}',
    'fold' : 0
}

variables['WH3l_ptOSll2'] = {
    'name': 'Alt(WH3l_ptOSll, 2, 0)',
    'range' : (10,0,400),
    'xaxis' : 'p_T^{l2,l3}',
    'fold' : 0
}

# variables['min_WH3l_ptOSll'] = {
#     'name': 'MinIf$( WH3l_ptOSll[], WH3l_ptOSll[Iteration$] > 0)',
#     'range' : (10,0,400),
#     'xaxis' : 'min p_T(OS lepton pairs)',
#     'fold' : 0
# }

# mT(l, met)
variables['WH3l_mtlmet0'] = {
    'name': 'Alt(WH3l_mtlmet, 0, 0)',
    'range' : (10,0,400),
    'xaxis' : 'm_T^{l1,met}',
    'fold' : 0
}

variables['WH3l_mtlmet1'] = {
    'name': 'Alt(WH3l_mtlmet, 1, 0)',
    'range' : (10,0,400),
    'xaxis' : 'm_T^{l2,met}',
    'fold' : 0
}

variables['WH3l_mtlmet2'] = {
    'name': 'Alt(WH3l_mtlmet, 2, 0)',
    'range' : (10,0,400),
    'xaxis' : 'm_T^{l3,met}',
    'fold' : 0
}

# variables['min_WH3l_mtlmet'] = {
#     'name': 'MinIf$( WH3l_mtlmet[], WH3l_mtlmet[Iteration$] > 0)',
#     'range' : (10,0,400),
#     'xaxis' : 'min m_T(l,met)',
#     'fold' : 0
# }

# # mT(WWW)
# variables['WH3l_mtWWW'] = {
#     'name': 'Alt(WH3l_mtWWW, 0)',
#     'range' : (10,0,400),
#     'xaxis' : 'm_T^{WWW}',
#     'fold' : 0
# }

# # pT(WWW)
# variables['WH3l_ptWWW'] = {
#     'name': 'Alt(WH3l_ptWWW, 0)',
#     'range' : (10,0,400),
#     'xaxis' : 'p_T^{WWW}',
#     'fold' : 0
# }

# # pT(W) -- considers the W least likely to come from the Higgs
# variables['WH3l_ptW'] = {
#     'name': 'Alt(WH3l_ptW, 0)',
#     'range' : (10,0,400),
#     'xaxis' : 'p_T^{W}',
#     'fold' : 0
# }

# # DeltaPhi between the tri-lepton system and the met
# variables['WH3l_dphilllmet'] = {
#     'name': 'Alt(WH3l_dphilllmet, 0)',
#     'range' : (10,0,5),
#     'xaxis' : '#Delta #Phi(lll,met)',
#     'fold' : 0
# }

# # m(lll)
# variables['WH3l_mlll'] = {
#     'name': 'Alt(WH3l_mlll, 0)',
#     'range' : (10,0,400),
#     'xaxis' : 'm_{lll}',
#     'fold' : 0
# }

# Variable specifically used for WZ CR
variables['dphillmet'] = {
    'name'  : 'dphillmet',
    'range' : (20,0,3.2),
    'xaxis' : 'dphillmet',
    'fold'  : 3
}

variables['mlljj20_whss_bin2'] = {
    'name'  : 'mlljj20_whss',
    'range' : ([60.,100.,110.,120.,130.,140.,150.,160.,170.,180.,190.,200.,250.,300.],),
    'xaxis' : 'mlljj20_whss [GeV]',
    'fold'  : 3
}

variables['dphilep1jet1'] = {
    'name'  : 'dphilep1jet1',
    'range' : (20,0,3.2),
    'xaxis' : 'dphilep1jet1',
    'fold'  : 3
}

# variables['BDTG6_TT'] = {
#     'name'     : 'BDT_WHSS_TopSemileptonic_v9',     
#     'range'    : (40,-1,1),   
#     # 'doWeight' : 1,
#     # 'binX'     : 1,
#     # 'binY'     : 40,
#     'xaxis'    : 'BDT discriminant',
#     'fold'     : 3
# }

variables['mll'] = {
    'name'  : 'mll',
    'range' : (20, 40,120),
    'xaxis' : 'm_{ll} [GeV]',
    'fold'  : 0
}

variables['mtw1'] = {
    'name'  : 'mtw1',
    'range' : (40,0,200),
    'xaxis' : 'm_{T}^{W_{1}} [GeV]',
    'fold'  : 3
}

variables['dphill']  = {  
    'name'  : 'abs(dphill)',     
    'range' : (20,0,3.14),   
    'xaxis' : '#Delta#phi_{ll}',
    'fold'  : 3
}


# # 1 jet binning
# variables['mlljj20_whss_1j_bin'] = {
#     'name'  : 'mlljj20_whss',
#     'range' : ([60.,70.,80.,90.,100.,110.,120.,130.,140.,150.,160.,170.,180.,190.,200.,250.,300.],),
#     'xaxis' : 'mlljj20_whss [GeV]',
#     'fold'  : 3
# }

# # 2 jets binning
# variables['mlljj20_whss_2j_bin'] = {
#     'name'  : 'mlljj20_whss',
#     'range' : ([60.,120.,130.,140.,150.,160.,170.,180.,190.,200.,250.,300.],),
#     'xaxis' : 'mlljj20_whss [GeV]',
#     'fold'  : 3
# }

# # # ########################################################
# # # # Default BDT training but with TopSemileptonic as fakes
# # # ########################################################

# # # variables['BDTG6_TT'] = {
# # #     'name'     : 'BDT_WHSS_TopSemileptonic_v9',     
# # #     'range'    : (40,-1,1),   
# # #     'doWeight' : 1,
# # #     'binX'     : 1,
# # #     'binY'     : 40,
# # #     'xaxis'    : 'BDT discriminant',
# # #     'yaxis'    : 'Events',
# # #     'fold'     : 3
# # # }

# # # variables['BDTG6_TT_100_bins'] = {
# # #     'name'  : 'BDT_WHSS_TopSemileptonic_v9',     
# # #     'range' : (100,-1,1),   
# # #     'xaxis' : 'BDT discriminant',
# # #     'fold'  : 3
# # # }

# # ###################
# # # Control variables
# # ###################

# # variables['puppimet'] = {
# #     'name'  : 'PuppiMET_pt',    
# #     'range' : (20,0,200),
# #     'xaxis' : 'PUPPI met [GeV]',
# #     'fold'  : 3
# # }

# # variables['mll'] = {
# #     'name'  : 'mll',
# #     'range' : (20, 40,120),
# #     'xaxis' : 'm_{ll} [GeV]',
# #     'fold'  : 0
# # }

# # variables['ptll'] = {
# #     'name'  : 'ptll',     
# #     'range' : (40, 0,200),   
# #     'xaxis' : 'p_{T}^{ll} [GeV]',
# #     'fold'  : 0
# # }

# # variables['pt1'] = {
# #     'name'  : 'Lepton_pt[0]',     
# #     'range' : (30,0,150),   
# #     'xaxis' : 'p_{T} 1st lep',
# #     'fold'  : 0                         
# # }

# # variables['pt2'] = {
# #     'name'  : 'Lepton_pt[1]',     
# #     'range' : (20,0,100),   
# #     'xaxis' : 'p_{T} 2nd lep',
# #     'fold'  : 3                         
# # }

# # variables['mlljj20_whss_bin2'] = {
# #     'name'  : 'mlljj20_whss',
# #     'range' : ([60.,100.,110.,120.,130.,140.,150.,160.,170.,180.,190.,200.,250.,300.],),
# #     'xaxis' : 'mlljj20_whss [GeV]',
# #     'fold'  : 3
# # }

# # variables['detall']  = {  
# #     'name'  : 'abs(Lepton_eta[0] - Lepton_eta[1])',
# #     'range' : (20,0.,10.),
# #     'xaxis' : 'detall',
# #     'fold'  : 3
# # }

# # variables['mth']  = {  
# #     'name'  : 'mth',
# #     'range' : (40,0,200),
# #     'xaxis' : 'm_{T}^{H} [GeV]',
# #     'fold'  : 0
# # }

# # variables['dphill']  = {  
# #     'name'  : 'abs(dphill)',     
# #     'range' : (20,0,3.14),   
# #     'xaxis' : '#Delta#phi_{ll}',
# #     'fold'  : 3
# # }

# # variables['eta1']  = {
# #     'name'  : 'Lepton_eta[0]',     
# #     'range' : (40,-3,3),   
# #     'xaxis' : '#eta 1st lep',
# #     'fold'  : 3                         
# # }

# # variables['eta2']  = {
# #     'name'  : 'Lepton_eta[1]',     
# #     'range' : (40,-3,3),   
# #     'xaxis' : '#eta 2nd lep',
# #     'fold'  : 3                         
# # }

# # variables['jetpt1']  = {
# #     'name'  : 'CleanJet_pt[0]*(CleanJet_pt[0]>30)',     
# #     'range' : (40,0,200),   
# #     'xaxis' : 'p_{T} 1st jet',
# #     'fold'  : 2   
# # }

# # variables['jetpt2'] = {
# #     'name'  : 'CleanJet_pt[1]*(CleanJet_pt[1]>30)',     
# #     'range' : (40,0,200),   
# #     'xaxis' : 'p_{T} 2nd jet',
# #     'fold'  : 0
# # }

# # variables['mjj'] = {
# #     'name'  : 'mjj*(CleanJet_pt[1]>30)',
# #     'range' : (50,0,400),
# #     'xaxis' : 'm_{jj} [GeV]',
# #     'fold'  : 3
# # }

# # variables['mtw1'] = {
# #     'name'  : 'mtw1',
# #     'range' : (40,0,200),
# #     'xaxis' : 'm_{T}^{W_{1}} [GeV]',
# #     'fold'  : 3
# # }

# # variables['mtw2'] = {
# #     'name'  : 'mtw2',
# #     'range' : (40,0,200),
# #     'xaxis' : 'm_{T}^{W_{2}} [GeV]',
# #     'fold'  : 3
# # }

# # variables['dphilljet'] = {
# #     'name'  : 'dphilljet',
# #     'range' : (20,0,3.2),
# #     'xaxis' : 'dphilljet',
# #     'fold'  : 3
# # }

# # variables['dphilljetjet'] = {
# #     'name'  : 'dphilljetjet*(CleanJet_pt[1]>30)',
# #     'range' : (20,0,3.2),
# #     'xaxis' : 'dphilljetjet',
# #     'fold'  : 3
# # }

# # variables['dphilmet'] = {
# #     'name'  : 'dphilmet',
# #     'range' : (20,0,3.2),
# #     'xaxis' : 'dphilmet',
# #     'fold'  : 3
# # }

# # variables['dphilmet2'] = {
# #     'name'  : 'dphilmet2',
# #     'range' : (20,0,3.2),
# #     'xaxis' : 'dphilmet2',
# #     'fold'  : 3
# # }

# # variables['dphillmet'] = {
# #     'name'  : 'dphillmet',
# #     'range' : (20,0,3.2),
# #     'xaxis' : 'dphillmet',
# #     'fold'  : 3
# # }

# # variables['dphilep1jet1'] = {
# #     'name'  : 'dphilep1jet1',
# #     'range' : (20,0,3.2),
# #     'xaxis' : 'dphilep1jet1',
# #     'fold'  : 3
# # }

# # variables['dphilep1jet2'] = {
# #     'name'  : 'dphilep1jet2*(CleanJet_pt[1]>30)',
# #     'range' : (20,0,3.2),
# #     'xaxis' : 'dphilep1jet2',
# #     'fold'  : 3
# # }

# # variables['dphilep2jet1'] = {
# #     'name'  : 'dphilep2jet1',
# #     'range' : (20,0,3.2),
# #     'xaxis' : 'dphilep2jet1',
# #     'fold'  : 3
# # }

# # variables['dphilep2jet2'] = {
# #     'name'  : 'dphilep2jet2*(CleanJet_pt[1]>30)',
# #     'range' : (20,0,3.2),
# #     'xaxis' : 'dphilep1jet2',
# #     'fold'  : 3
# # }

# # variables['dphijjmet'] = {
# #     'name'  : 'dphijjmet',
# #     'range' : (20,0,3.2),
# #     'xaxis' : 'dphijjmet',
# #     'fold'  : 3
# # }

# # variables['ht'] = {
# #     'name'  : 'ht',
# #     'range' : (40,0,200),
# #     'xaxis' : 'ht [GeV]',
# #     'fold'  : 3
# # }

# # variables['dphijj'] = {
# #     'name'  : 'dphijj',
# #     'range' : (20,0,3.2),
# #     'xaxis' : 'dphijj',
# #     'fold'  : 3
# # }

# # variables['dphijet1met'] = {
# #     'name'  : 'dphijet1met',
# #     'range' : (20,0,3.2),
# #     'xaxis' : 'dphijet1met',
# #     'fold'  : 3
# # }

# # variables['DeepCSV_jet1'] = {
# #     'name'  : 'Alt(Jet_btagDeepB,CleanJet_jetIdx[0],-2)',
# #     'range' : (50,0.0,1.0),
# #     'xaxis' : 'Leading jet DeepCSV',
# #     'fold'  : 3
# # }

# # variables['DeepCSV_jet2'] = {
# #     'name'  : 'Alt(Jet_btagDeepB,CleanJet_jetIdx[1],-2)',
# #     'range' : (50,0.0,1.0),
# #     'xaxis' : 'Sub-leading jet DeepCSV',
# #     'fold'  : 3
# # }
