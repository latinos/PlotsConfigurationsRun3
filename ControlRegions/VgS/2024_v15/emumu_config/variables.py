# variables
variables = {}

variables['events'] = {
    'name'  : '1',
    'range' : (1,0,2),
    'xaxis' : 'events',
    'fold'  : 3
}

variables['mll'] = {
    'name': 'mll',
    'range' : (60,0,120),
    'xaxis' : 'm(\ell_1,\ell_2) [GeV]',
    'fold' : 3
}

variables['ptll']  = {  
    'name': 'ptll',     
    'range' : (20, 0,200),   
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
    'range' : (50, 0,5),
    'xaxis' : '#Delta #phi_{ll}',
    'fold' : 0
}

variables['pt1']  = { 
    'name': 'Lepton_pt[0]',     
    'range' : (20,0,200),
    'xaxis' : 'p_{T} 1st lep',
    'fold'  : 3                         
}

variables['pt2']  = {
    'name': 'Lepton_pt[1]',     
    'range' : (20,0,140),   
    'xaxis' : 'p_{T} 2nd lep',
    'fold'  : 3                         
}

variables['pt3']  = {
    'name': 'Lepton_pt[2]',     
    'range' : (20,0,100),   
    'xaxis' : 'p_{T} 3rd lep',
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

variables['eta3']  = {
    'name': 'Lepton_eta[2]',     
    'range' : (40,-3,3),   
    'xaxis' : '#eta 3rd lep',
    'fold'  : 3                         
}

variables['mllOneThree'] = {
    'name': 'mllOneThree',
    'range' : (60,0,120),
    'xaxis' : 'm(\ell_1,\ell_3) [GeV]',
    'fold' : 3
}

variables['mllTwoThree'] = {
    'name': 'mllTwoThree',
    'range' : (60,0,120),
    'xaxis' : 'm(\ell_2,\ell_3) [GeV]',
    'fold' : 3
}

variables['mllTwoThree_zoomed'] = {
    'name': 'mllTwoThree',
    'range' : (25,0,10.0),
    'xaxis' : 'm(\ell_2,\ell_3) [GeV]',
    'fold' : 3
}

variables['nvtx'] = {     
    'name'  : 'PV_npvsGood',      
    'range' : (100, 0, 100),  
    'xaxis' : 'number of vertices', 
    'fold'  : 3
}

variables['puppimet'] = {
    'name': 'PuppiMET_pt',
    'range' : (25,0,100),
    'xaxis' : 'PUPPI pT miss [GeV]',
    'fold' : 3
}

# variables['evType'] = {
#     'name': 'evType',
#     'range' : (5,0,5),
#     'xaxis' : 'evType',
#     'fold' : 3
# }

