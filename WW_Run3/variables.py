# variables

variables = {}
#variables['nvtx']  = {   'name': 'PV_npvsGood',      
#                        'range' : (20,0,100),  
#                        'xaxis' : 'nvtx', 
#                         'fold' : 3
#                      }



variables['RandomForest']  = {
    'name': 'RandomForest_evaluator',
    'range' : (40, 0,1),
    'xaxis' : 'Random Forest score (LL)',
    'fold' : 3
}

variables['RandomForest_WP50']  = {
    'name': 'RandomForest_evaluator',
    'range' : (40,0.5,1),
    'xaxis' : 'Random Forest score (LL)',
    'fold' : 3
}


variables['mll'] = {
    'name': 'mll_',            #   variable name
    'range' : (40,85,200),    #   variable range
    'xaxis' : 'm_{ll} [GeV]',  #   x axis name
    'fold' : 0
}

variables['ptll']  = {  
    'name': 'ptll_',     
    'range' : (20, 0,200),   
    'xaxis' : 'p_{T}^{ll} [GeV]',
    'fold' : 0
}

variables['mpmet']  = {
    'name': 'mpmet',
    'range' : (50, 0,100),
    'xaxis' : 'p_{T}^{ll} [GeV]',
    'fold' : 0
}

variables['drll']  = {
    'name': 'drll_',
    'range' : (50, 0,5),
    'xaxis' : '#Delta R_{ll}',
    'fold' : 0
}

variables['dphill']  = {
    'name': 'dphill_',
    'range' : (50, 0,5),
    'xaxis' : '#Delta #phi_{ll}',
    'fold' : 0
}

variables['ptll_more']  = {
    'name': 'ptll_',
    'range' : (50, 0,100),
    'xaxis' : 'p_{T}^{ll} [GeV]',
    'fold' : 0
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

variables['jetdeepb']  = {
    'name': 'Alt(Take(Jet_btagDeepFlavB, MyCleanJet_jetIdx), 0, -99)',
    'range' : (30,-1,1),
    'xaxis' : 'B tagger 1st jet (DeepB)',
    'fold' : 2
}


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

variables['re_njet']  = {
    'name': 'Sum(MyCleanJet_pt>30)',
    'range' : (5,0,5),
    'xaxis' : 'Number of jets',
    'fold' : 2
}

variables['re_jetpt1']  = {
    'name': 'Alt(MyCleanJet_pt, 0, -99) - 9999.9*(MyCleanJet_pt[0]<30)',
    'range' : (40,0,200),
    'xaxis' : 'p_{T} 1st jet',
    'fold' : 0
}

variables['re_jetpt2']  = {
    'name': 'Alt(MyCleanJet_pt, 1, -99)  - 9999.9*(MyCleanJet_pt[1]<30)',
    'range' : (40,0,200),
    'xaxis' : 'p_{T} 2nd jet',
    'fold' : 0
}

variables['re_jeteta1']  = {
    'name': 'Alt(MyCleanJet_eta, 0, -99) - 9999.9*(MyCleanJet_pt[0]<30)',
    'range' : (30,-4.7,4.7),
    'xaxis' : '#eta 1st jet',
    'fold' : 0
}

variables['re_jeteta2']  = {
    'name': 'Alt(MyCleanJet_eta, 1, -99) - 9999.9*(MyCleanJet_pt[1]<30)',
    'range' : (30,-4.7,4.7),
    'xaxis' : '#eta 2nd jet',
    'fold' : 0
}


variables['re_njet_noHorn']  = {
    'name': 'Sum(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5]>30)',
    'range' : (5,0,5),
    'xaxis' : 'Number of jets',
    'fold' : 2
}

variables['re_jetpt1_noHorn']  = {
    'name': 'Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 0, -99) - 9999.9*(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5][0]<30)',
    'range' : (40,0,200),
    'xaxis' : 'p_{T} 1st jet',
    'fold' : 0
}

variables['re_jetpt2_noHorn']  = {
    'name': 'Alt(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5], 1, -99) - 9999.9*(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5][1]<30)',
    'range' : (40,0,200),
    'xaxis' : 'p_{T} 2nd jet',
    'fold' : 0
}

variables['re_jeteta1_noHorn']  = {
    'name': 'Alt(MyCleanJet_eta[abs(MyCleanJet_eta)<=2.5], 0, -99) - 9999.9*(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5][0]<30)',
    'range' : (30,-2.5,2.5),
    'xaxis' : '#eta 1st jet',
    'fold' : 0
}

variables['re_jeteta2_noHorn']  = {
    'name': 'Alt(MyCleanJet_eta[abs(MyCleanJet_eta)<=2.5], 1, -99) - 9999.9*(MyCleanJet_pt[abs(MyCleanJet_eta)<=2.5][1]<30)',
    'range' : (30,-2.5,2.5),
    'xaxis' : '#eta 2nd jet',
    'fold' : 0
}



