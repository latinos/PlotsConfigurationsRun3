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

# ptbins[8]  = {10, 15, 20, 25, 30, 35, 40, 45, 50};
# etabins[2] = {0, 1.479, 2.5};

# variables['pt1_eta1'] = {
#     'name'  : 'Lepton_pt[0]:abs(Lepton_eta[0])',
#     'range' : ([10, 15, 20, 25, 30, 35, 40, 45, 50],[0.0, 0.5, 1.0, 1.5, 2.0, 2.5],),
#     'xaxis' : 'p_{T}^{#ell 1}:#eta^{#ell 1}',
#     'fold'  : 3,
# }

# Cone_pt1 vs eta1
variables['pt1_eta1'] = {
    'name'  : 'Lepton_conept[0]:abs(Lepton_eta[0])',
    'range' : ([10, 15, 20, 25, 30, 35, 40, 45, 50],[0.0, 1.479, 2.5]),
    'xaxis' : 'p_{T}^{cone}(#ell 1):|#eta(#ell 1})|',
    'fold'  : 3,
}

# variables['pt2_eta2'] = {
#     'name'  : 'Alt(Lepton_pt,1,0):abs(Alt(Lepton_eta,1,999))',
#     'range' : ([10, 15, 20, 25, 30, 35, 40, 45, 50],[0.0, 0.5, 1.0, 1.5, 2.0, 2.5],),
#     'xaxis' : 'p_{T}^{#ell 2}:#eta^{#ell 2}',
#     'fold'  : 3,
# }

# Cone_pt2 vs eta2
variables['pt2_eta2'] = {
    'name'  : 'Lepton_conept[1]:abs(Lepton_eta[1])',
    'range' : ([10, 15, 20, 25, 30, 35, 40, 45, 50],[0.0, 1.479, 2.5]),
    'xaxis' : 'p_{T}^{cone}(#ell 2):|#eta^{#ell 2}|',
    'fold'  : 3,
}

variables['mll'] = {
    'name'  : 'mll',
    'range' : (20, 60,120),
    'xaxis' : 'm_{ll} [GeV]',
    'fold'  : 0
}

variables['pt1'] = {
    'name'  : 'Lepton_pt[0]',     
    'range' : (20,0,100),   
    'xaxis' : 'p_{T} 1st lep',
    'fold'  : 0                         
}

variables['conept1'] = {
    'name'  : 'Lepton_conept[0]',
    'range' : (20,0,100),
    'xaxis' : 'p_{T}^{cone} 1st lep',
    'fold'  : 0
}

variables['eta1']  = {
    'name'  : 'Lepton_eta[0]',     
    'range' : (40,-3,3),   
    'xaxis' : '#eta 1st lep',
    'fold'  : 3                         
}

variables['pt2'] = {
    'name'  : 'Alt(Lepton_pt,1,0)',
    'range' : (20,0,100),   
    'xaxis' : 'p_{T} 2nd lep',
    'fold'  : 0                         
}

variables['conept2'] = {
    'name'  : 'Lepton_conept[1]',
    'range' : (20,0,100),
    'xaxis' : 'p_{T}^{cone} 2nd lep',
    'fold'  : 0
}

variables['eta2']  = {
    'name'  : 'Alt(Lepton_eta,1,999)',
    'range' : (40,-3,3),
    'xaxis' : '#eta 2nd lep',
    'fold'  : 3                         
}

variables['mtw1'] = {
    'name'  : 'mtw1',
    'range' : (20,0,100),
    'xaxis' : 'm_{T}^{W_{1}} [GeV]',
    'fold'  : 3
}

variables['LepWPCut1l'] = {
    'name'  : 'LepWPCut1l',
    'range' : (2,0,2),
    'xaxis' : 'Tight lepton flag',
    'fold'  : 3
}

variables['dRl1j1'] = {
    'name'  : 'dRl1j1',
    'range' : (20,0,10),
    'xaxis' : '#Delta R (#ell1,jet1)',
    'fold'  : 3
}

variables['dphilep1jet1'] = {
    'name'  : 'dphilep1jet1',
    'range' : (10,0,5),
    'xaxis' : '#Delta #phi (#ell1,jet1)',
    'fold'  : 3
}

variables['puppimet'] = {
    'name'  : 'PuppiMET_pt',    
    'range' : (20,0,200),
    'xaxis' : 'PUPPI met [GeV]',
    'fold'  : 3
}

# variables['jetpt1']  = {
#     'name'  : 'CleanJet_pt[0]*(CleanJet_pt[0]>30)',     
#     'range' : (40,0,200),   
#     'xaxis' : 'p_{T} 1st jet',
#     'fold'  : 2   
# }
