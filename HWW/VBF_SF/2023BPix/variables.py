_mergedCuts = []
for cut in list(cuts.keys()):
    __cutExpr = ''
    if type(cuts[cut]) == dict:
        __cutExpr = cuts[cut]['expr']
        for cat in list(cuts[cut]['categories'].keys()):
            _mergedCuts.append(cut + '_' + cat)
    elif type(cuts[cut]) == str:
        _mergedCuts.append(cut)

cuts2j = _mergedCuts

variables = {}


variables['events'] = {
    'name'  : '1',      
    'range' : (1,0,2),  
    'xaxis' : 'events', 
    'fold'  : 3,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}

variables['dymva_score'] = {
    'name' : 'dymva[0]',
    'range' : (20, 0, 1),
    'xaxis' : 'DYMVA score',
    'fold' : 3,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}
"""
variables['nvtx'] = {     
    'name'  : 'PV_npvsGood',      
    'range' : (100, 0, 100),  
    'xaxis' : 'number of vertices', 
    'fold'  : 3,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}


variables['mll'] = {
    'name': 'mll',    
    'range' : (20, 12, 200),
    'xaxis' : 'm_{ll} [GeV]',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}

variables['mth']  = {  
    'name': 'mth',     
    'range' : (20, 60, 200),   
    'xaxis' : 'm_{T}^{H} [GeV]',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}


variables['ptll']  = {  
    'name': 'ptll',     
    'range' : (20, 30,200),   
    'xaxis' : 'p_{T}^{ll} [GeV]',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}

# variables['mpmet']  = {
#     'name': 'mpmet',
#     'range' : (50, 0,100),
#     'xaxis' : 'p_{T}^{ll} [GeV]',
#     'fold' : 0
# }

variables['drll']  = {
    'name': 'drll',
    'range' : (50, 0,5),
    'xaxis' : '#Delta R_{ll}',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}

variables['dphill']  = {
    'name': 'dphill',
    'range' : (50, 0,5),
    'xaxis' : '#Delta #phi_{ll}',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}

variables['ptll_more']  = {
    'name': 'ptll',
    'range' : (50, 0,100),
    'xaxis' : 'p_{T}^{ll} [GeV]',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}

variables['pt1']  = { 
    'name': 'Lepton_pt[0]',     
    'range' : (20,20,100),
    'xaxis' : 'p_{T} 1st lep',
    'fold'  : 3,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])                         
}

variables['pt2']  = {
    'name': 'Lepton_pt[1]',     
    'range' : (20,10,100),   
    'xaxis' : 'p_{T} 2nd lep',
    'fold'  : 3,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])                         
}

variables['eta1']  = {
    'name': 'Lepton_eta[0]',     
    'range' : (20,-3,3),   
    'xaxis' : '#eta 1st lep',
    'fold'  : 3,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])                         
}

variables['eta2']  = {
    'name': 'Lepton_eta[1]',     
    'range' : (20,-3,3),   
    'xaxis' : '#eta 2nd lep',
    'fold'  : 3,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])                         
}

                        
variables['phi1']  = {
    'name': 'Lepton_phi[0]',
    'range' : (20,-3.2,3.2),
    'xaxis' : '#phi 1st lep',
    'fold'  : 3,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}

variables['phi2']  = {
    'name': 'Lepton_phi[1]',
    'range' : (20,-3.2,3.2),
    'xaxis' : '#phi 2nd lep',
    'fold'  : 3,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}

variables['jetdeepb']  = {
    'name': 'Alt(Take(Jet_btagDeepFlavB, CleanJet_jetIdx), 0, -99)',
    'range' : (30,-1,1),
    'xaxis' : 'B tagger 1st jet (DeepFlavB)',
    'fold' : 2,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}

variables['jetdeepb2']  = {
    'name': 'Alt(Take(Jet_btagDeepFlavB, CleanJet_jetIdx), 1, -99) -999.99*(CleanJet_pt[1]<20)',
    'range' : ([0., 0.0583, 1.],),
    'xaxis' : 'B tagger 2nd jet (DeepFlavB)',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}

variables['trkMet']  = { 
    'name': 'TkMET_pt',
    'range' : (20,0,200),
    'xaxis' : 'trk met [GeV]',
    'fold' : 3,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}

variables['puppimet']  = {
    'name': 'PuppiMET_pt',
    'range' : (20,0,200),
    'xaxis' : 'Puppi MET p_{T} [GeV]',
    'fold' : 3,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}

############# New Jet processing

variables['njet']  = {
    'name': 'Sum(CleanJet_pt>30)',
    'range' : (5,0,5),
    'xaxis' : 'Number of jets',
    'fold' : 2,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}

variables['jetpt1']  = {
    'name': 'Alt(CleanJet_pt, 0, -99) - 9999.9*(CleanJet_pt[0]<30)', 
    'range' : (20,0,200),
    'xaxis' : 'p_{T} 1st jet [GeV]',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}

variables['jetpt2']  = {
    'name': 'Alt(CleanJet_pt, 1, -99) - 9999.9*(CleanJet_pt[1]<30)',
    'range' : (20,0,200),
    'xaxis' : 'p_{T} 2nd jet',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}

variables['jeteta1']  = {
    'name': 'Alt(CleanJet_eta, 0, -99) - 9999.9*(CleanJet_pt[0]<30)',
    'range' : (30,-4.7,4.7),
    'xaxis' : '#eta 1st jet',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}

variables['jeteta2']  = {
    'name': 'Alt(CleanJet_eta, 1, -99) - 9999.9*(CleanJet_pt[1]<30)',
    'range' : (30,-4.7,4.7),
    'xaxis' : '#eta 2nd jet',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}
"""

"""
# Jets neEmEF and neHF

variables['jet_neEmEF1'] = {
    'name' : 'Alt(Take(Jet_neEmEF, CleanJet_jetIdx), 0, -99) - 9999.9*(CleanJet_pt[0]<30)',
    'range' : (20, 0, 1),
    'xaxis' : 'neutral Electromagnetic Energy Fraction 1st jet',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}

variables['jet_neEmEF2'] = {
    'name' : 'Alt(Take(Jet_neEmEF, CleanJet_jetIdx), 1, -99) - 9999.9*(CleanJet_pt[1]<30)',
    'range' : (20, 0, 1),
    'xaxis' : 'neutral Electromagnetic Energy Fraction 2nd jet',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}


variables['jet_neHEF1'] = {
    'name' : 'Alt(Take(Jet_neHEF,CleanJet_jetIdx), 0, -99) - 9999.9*(CleanJet_pt[0]<30)',
    'range' : (20, 0, 1),
    'xaxis' : 'neutral Hadron Energy Fraction 1st jet',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}

variables['jet_neHEF2'] = {
    'name' : 'Alt(Take(Jet_neHEF,CleanJet_jetIdx), 1, -99) - 9999.9*(CleanJet_pt[1]<30)',
    'range' : (20, 0, 1),
    'xaxis' : 'neutral Hadron Energy Fraction 2nd jet',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}


# Jets chEmEF and chHEF
variables['jet_chEmEF1'] = {
    'name' : 'Alt(Take(Jet_chEmEF, CleanJet_jetIdx), 0, -99) - 9999.9*(CleanJet_pt[0]<30)',
    'range' : (20, 0, 1),
    'xaxis' : 'charged Electromagnetic Energy Fraction 1st jet',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}

variables['jet_chEmEF2'] = {
    'name' : 'Alt(Take(Jet_chEmEF, CleanJet_jetIdx), 1, -99) - 9999.9*(CleanJet_pt[1]<30)',
    'range' : (20, 0, 1),
    'xaxis' : 'charged Electromagnetic Energy Fraction 2nd jet',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}


variables['jet_chHEF1'] = {
    'name' : 'Alt(Take(Jet_chHEF, CleanJet_jetIdx), 0, -99) - 9999.9*(CleanJet_pt[0]<30)',
    'range' : (20, 0, 1),
    'xaxis' : 'charged Hadron Energy Fraction 1st jet',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}

variables['jet_chHEF2'] = {
    'name' : 'Alt(Take(Jet_chHEF, CleanJet_jetIdx), 1, -99) - 9999.9*(CleanJet_pt[1]<30)',
    'range' : (20, 0, 1),
    'xaxis' : 'charged Hadron Energy Fraction 2nd jet',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}

variables['njet_noHorn']  = {
    'name': 'Sum(CleanJet_pt[abs(CleanJet_eta)<=2.5]>30)',
    'range' : (5,0,5),
    'xaxis' : 'Number of jets',
    'fold' : 2,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}

"""
