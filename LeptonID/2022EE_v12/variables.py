# variables

variables = {}

# variables['Lepton_hwwMVA_1']  = { 
#     'name'  : 'Lepton_hwwMVA_Run3[0]',     
#     'range' : (40,-1,1),
#     'xaxis' : 'Leading muon hww MVA discriminant',
#     'fold'  : 3                         
# }

# variables['Lepton_hwwMVA_2']  = { 
#     'name'  : 'Lepton_hwwMVA_Run3[1]',     
#     'range' : (40,-1,1),
#     'xaxis' : 'Sub-leading muon hww MVA discriminant',
#     'fold'  : 3                         
# }

variables['Muon_mvaTTH_1']  = { 
    'name': 'Muon_mvaTTH[Lepton_muonIdx[0]]',     
    'range' : (40,-1,1),
    'xaxis' : 'Leading muon ttH MVA discriminant',
    'fold'  : 3                         
}

variables['Muon_mvaTTH_2']  = { 
    'name': 'Muon_mvaTTH[Lepton_muonIdx[1]]',     
    'range' : (40,-1,1),
    'xaxis' : 'Sub-leading muon ttH MVA discriminant',
    'fold'  : 3                         
}

variables['Electron_mvaTTH_1']  = { 
    'name': 'Electron_mvaTTH[Lepton_electronIdx[0]]',     
    'range' : (40,-1,1),
    'xaxis' : 'Leading electron ttH MVA discriminant',
    'fold'  : 3                         
}

variables['Electron_mvaTTH_2']  = { 
    'name': 'Electron_mvaTTH[Lepton_electronIdx[1]]',     
    'range' : (40,-1,1),
    'xaxis' : 'Sub-leading electron ttH MVA discriminant',
    'fold'  : 3                         
}

variables['Lepton_mva1']  = { 
    'name': 'Lepton_ttHMVA_Run3[0]',     
    'range' : (40,-1,1),
    'xaxis' : 'Leading lepton ttH MVA discriminant',
    'fold'  : 3                         
}

variables['Lepton_mva2']  = { 
    'name': 'Lepton_ttHMVA_Run3[1]',     
    'range' : (40,-1,1),
    'xaxis' : 'Sub-leading lepton ttH MVA discriminant',
    'fold'  : 3                         
}

variables['pt1']  = { 
    'name': 'Lepton_pt[0]',     
    'range' : (20,0,100),
    'xaxis' : 'p_{T} 1st lep',
    'fold'  : 3                         
}

variables['pt2']  = {
    'name': 'Lepton_pt[1]',     
    'range' : (20,0,100),   
    'xaxis' : 'p_{T} 2nd lep',
    'fold'  : 3                         
}

variables['eta1']  = {
    'name': 'Lepton_eta[0]',     
    'range' : (40,-3,3),   
    'xaxis' : '#eta 1st lep',
    'fold'  : 3                         
}

variables['eta2']  = {
    'name': 'Lepton_eta[1]',     
    'range' : (40,-3,3),   
    'xaxis' : '#eta 2nd lep',
    'fold'  : 3                         
}

                        
variables['phi1']  = {
    'name': 'Lepton_phi[0]',
    'range' : (20,-3.2,3.2),
    'xaxis' : '#phi 1st lep',
    'fold'  : 3
}

variables['phi2']  = {
    'name': 'Lepton_phi[1]',
    'range' : (20,-3.2,3.2),
    'xaxis' : '#phi 2nd lep',
    'fold'  : 3
}

variables['nvtx'] = {     
    'name'  : 'PV_npvsGood',      
    'range' : (100, 0, 100),  
    'xaxis' : 'number of vertices', 
    'fold'  : 3
}

variables['puppimet']  = {
    'name': 'PuppiMET_pt',
    'range' : (20,0,200),
    'xaxis' : 'Puppi MET p_{T} [GeV]',
    'fold' : 3
}
