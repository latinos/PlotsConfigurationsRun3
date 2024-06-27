# variables

variables = {}

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
