# variables
variables = {}

variables['events'] = {
    'name'  : '1',      
    'range' : (1,0,2),  
    'xaxis' : 'events', 
    'fold'  : 3
}

variables['nvtx'] = {     
    'name'  : 'PV_npvsGood',      
    'range' : (100, 0, 100),  
    'xaxis' : 'number of vertices', 
    'fold'  : 3
}

variables['mll'] = {
    'name': 'mll',    
    'range' : (100,0,200), 
    'xaxis' : 'm_{ll} [GeV]',
    'fold' : 0
}

variables['ptll']  = {  
    'name': 'ptll',     
    'range' : (40,0,200),   
    'xaxis' : 'p_{T}^{ll} [GeV]',
    'fold' : 0
}

variables['drll']  = {
    'name': 'drll',
    'range' : (50, 0,5),
    'xaxis' : '#Delta R_{ll}',
    'fold' : 0
}

variables['dphill']  = {
    'name': 'dphill',
    'range' : (50,0,5),
    'xaxis' : '#Delta #phi_{ll}',
    'fold' : 0
}

variables['pt1']  = { 
    'name': 'Lepton_pt[0]',     
    'range' : (40,0,200),
    'xaxis' : 'p_{T} 1st lep',
    'fold'  : 3                         
}

variables['pt2']  = {
    'name': 'Lepton_pt[1]',     
    'range' : (40,0,160),   
    'xaxis' : 'p_{T} 2nd lep',
    'fold'  : 3                         
}

variables['cone_pt1']  = { 
    'name': 'Lepton_conept[0]',     
    'range' : (40,0,200),
    'xaxis' : 'p_{T} 1st lepton cone',
    'fold'  : 3                         
}

variables['cone_pt2']  = {
    'name': 'Lepton_conept[1]',     
    'range' : (40,0,160),   
    'xaxis' : 'p_{T} 2nd lepton cone',
    'fold'  : 3                         
}

variables['eta1']  = {
    'name': 'Lepton_eta[0]',     
    'range' : (50,-2.5,2.5),   
    'xaxis' : '#eta 1st lep',
    'fold'  : 3                         
}

variables['eta2']  = {
    'name': 'Lepton_eta[1]',     
    'range' : (50,-2.5,2.5),   
    'xaxis' : '#eta 2nd lep',
    'fold'  : 3                         
}


# MET
variables['trkMet']  = { 
    'name': 'TkMET_pt',
    'range' : (20,0,200),
    'xaxis' : 'trk met [GeV]',
    'fold' : 3
}

variables['puppimet']  = {
    'name': 'PuppiMET_pt',
    'range' : (20,0,200),
    'xaxis' : 'Puppi MET p_{T} [GeV]',
    'fold' : 3
}

############# New Jet processing
variables['njet']  = {
    'name': 'Sum(CleanJet_pt>30)',
    'range' : (5,0,5),
    'xaxis' : 'Number of jets',
    'fold' : 2
}

variables['jetpt1']  = {
    'name': 'Alt(CleanJet_pt, 0, -99) - 9999.9*(CleanJet_pt[0]<30)',
    'range' : (40,0,200),
    'xaxis' : 'p_{T} 1st jet',
    'fold' : 0
}

variables['jetpt2']  = {
    'name': 'Alt(CleanJet_pt, 1, -99)  - 9999.9*(CleanJet_pt[1]<30)',
    'range' : (40,0,200),
    'xaxis' : 'p_{T} 2nd jet',
    'fold' : 0
}

variables['jeteta1']  = {
    'name': 'Alt(CleanJet_eta, 0, -99) - 9999.9*(CleanJet_pt[0]<30)',
    'range' : (30,-4.7,4.7),
    'xaxis' : '#eta 1st jet',
    'fold' : 0
}

variables['jeteta1_fine_binning']  = {
    'name': 'Alt(CleanJet_eta, 0, -99) - 9999.9*(CleanJet_pt[0]<30)',
    'range' : (94,-4.7,4.7),
    'xaxis' : '#eta 1st jet',
    'fold' : 0
}

variables['jeteta2']  = {
    'name': 'Alt(CleanJet_eta, 1, -99) - 9999.9*(CleanJet_pt[1]<30)',
    'range' : (30,-4.7,4.7),
    'xaxis' : '#eta 2nd jet',
    'fold' : 0
}

variables['jeteta2_fine_binning']  = {
    'name': 'Alt(CleanJet_eta, 1, -99) - 9999.9*(CleanJet_pt[1]<30)',
    'range' : (94,-4.7,4.7),
    'xaxis' : '#eta 2nd jet',
    'fold' : 0
}

variables['jetdeepb']  = {
    'name': 'Alt(Take(Jet_btagPNetB, CleanJet_jetIdx), 0, -99)',
    'range' : (30,-1,1),
    'xaxis' : 'B tagger 1st jet (PNetB)',
    'fold' : 0
}

variables['jetdeepb2']  = {
    'name': 'Alt(Take(Jet_btagPNetB, CleanJet_jetIdx), 1, -99) -999.99*(CleanJet_pt[1]<20)',
    'range' : ([0., 0.0499, 1.],),
    'xaxis' : 'B tagger 2nd jet (PNetB)',
    'fold' : 0
}

variables['mtw1'] = {
    'name'  : 'mtw1',
    'range' : (50,0,250),
    'xaxis' : 'm_{T}^{W_{1}} [GeV]',
    'fold'  : 3
}

variables['mtw2'] = {
    'name'  : 'mtw2',
    'range' : (50,0,200),
    'xaxis' : 'm_{T}^{W_{2}} [GeV]',
    'fold'  : 3
}

variables['dphilljet'] = {
    'name'  : 'dphilljet',
    'range' : (20,0,3.2),
    'xaxis' : 'dphilljet',
    'fold'  : 3
}

variables['dphilljetjet'] = {
    'name'  : 'dphilljetjet*(CleanJet_pt[1]>30)',
    'range' : (20,0,3.2),
    'xaxis' : 'dphilljetjet',
    'fold'  : 3
}

variables['dphilmet'] = {
    'name'  : 'dphilmet',
    'range' : (20,0,3.2),
    'xaxis' : 'dphilmet',
    'fold'  : 3
}

variables['dphilmet2'] = {
    'name'  : 'dphilmet2',
    'range' : (20,0,3.2),
    'xaxis' : 'dphilmet2',
    'fold'  : 3
}

variables['dphillmet'] = {
    'name'  : 'dphillmet',
    'range' : (20,0,3.2),
    'xaxis' : 'dphillmet',
    'fold'  : 3
}

variables['dphilep1jet1'] = {
    'name'  : 'dphilep1jet1',
    'range' : (20,0,3.2),
    'xaxis' : 'dphilep1jet1',
    'fold'  : 3
}

variables['dphilep1jet2'] = {
    'name'  : 'dphilep1jet2*(CleanJet_pt[1]>30)',
    'range' : (20,0,3.2),
    'xaxis' : 'dphilep1jet2',
    'fold'  : 3
}

variables['dphilep2jet1'] = {
    'name'  : 'dphilep2jet1',
    'range' : (20,0,3.2),
    'xaxis' : 'dphilep2jet1',
    'fold'  : 3
}

variables['dphilep2jet2'] = {
    'name'  : 'dphilep2jet2*(CleanJet_pt[1]>30)',
    'range' : (20,0,3.2),
    'xaxis' : 'dphilep1jet2',
    'fold'  : 3
}

variables['dphijjmet'] = {
    'name'  : 'dphijjmet',
    'range' : (20,0,3.2),
    'xaxis' : 'dphijjmet',
    'fold'  : 3
}

variables['ht'] = {
    'name'  : 'ht',
    'range' : (30,0,1500),
    'xaxis' : 'ht [GeV]',
    'fold'  : 3
}

variables['dphijet1met'] = {
    'name'  : 'dphijet1met',
    'range' : (20,0,3.2),
    'xaxis' : 'dphijet1met',
    'fold'  : 3
}

variables['detajj']  = {  
    'name'  : 'abs(CleanJet_eta[0] - CleanJet_eta[1])*(CleanJet_pt[1]>30)',
    'range' : (20,0.,10.),
    'xaxis' : '#Delta#eta_{jj}',
    'fold'  : 3
}

variables['dphijj'] = {
    'name'  : 'dphijj',
    'range' : (20,0,3.2),
    'xaxis' : '#Delta#phi_{jj}',
    'fold'  : 3
}
