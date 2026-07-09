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

## events cross check

variables['events'] = {
    'name'  : '1',      
    'range' : (1,0,2),  
    'xaxis' : 'events', 
    'fold'  : 3,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

## input DNN
variables['jet1eta']  = {
    'name': 'Alt(CleanJet_eta, 0, -99) - 9999.9*(CleanJet_pt[0]<30)',
    'range' : (25,-5.,5.),
    'xaxis' : '#eta^{j1}',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['jet2eta']  = {
    'name': 'Alt(CleanJet_eta, 1, -99) - 9999.9*(CleanJet_pt[1]<30)',
    'range' : (25,-5.,5.),
    'xaxis' : '#eta^{j2}',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['jet1phi']  = {
    'name': 'Alt(CleanJet_phi, 0, -99) - 9999.9*(CleanJet_pt[0]<30)',
    'range' : (20,-3.14,3.14),
    'xaxis' : '#phi^{j1}',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['jet2phi']  = {
    'name': 'Alt(CleanJet_phi, 1, -99) - 9999.9*(CleanJet_pt[1]<30)',
    'range' : (20,-3.14,3.14),
    'xaxis' : '#phi^{j2}',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['jet1pt']  = {
    'name': 'Alt(CleanJet_pt, 0, -99) - 9999.9*(CleanJet_pt[0]<30)',
    'range' : (30,0,300),
    'xaxis' : 'p_{T}^{j1} [GeV]',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['jet2pt']  = {
    'name': 'Alt(CleanJet_pt, 1, -99) - 9999.9*(CleanJet_pt[1]<30)',
    'range' : (30,0,300),
    'xaxis' : 'p_{T}^{j2} [GeV]',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['lep1eta']  = {
    'name': 'Lepton_eta[0]',
    'range' : (25,-2.5,2.5),
    'xaxis' : '#eta^{l1}',
    'fold'  : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['lep2eta']  = {
    'name': 'Lepton_eta[1]',
    'range' : (25,-2.5,2.5),
    'xaxis' : '#eta^{l2}',
    'fold'  : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['lep1phi']  = {
    'name': 'Lepton_phi[0]',
    'range' : (20,-3.14,3.14),
    'xaxis' : '#phi^{l1}',
    'fold'  : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['lep2phi']  = {
    'name': 'Lepton_phi[1]',
    'range' : (20,-3.14,3.14),
    'xaxis' : '#phi^{l2}',
    'fold'  : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['lep1pt']  = {
    'name': 'Lepton_pt[0]',
    'range' : (30,0,300),
    'xaxis' : 'p_{T}^{l1} [GeV]',
    'fold'  : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['lep2pt']  = {
    'name': 'Lepton_pt[1]',
    'range' : (30,0,300),
    'xaxis' : 'p_{T}^{l2} [GeV]',
    'fold'  : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['Rpt']  = {
    'name': 'Rpt',
    'range' : (20,0,20),
    'xaxis' : 'R_{p_{T}}',
    'fold'  : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['Zepp_l1']  = {
    'name': 'Zepp_l1',
    'range' : (20,-5,5),
    'xaxis' : 'Zepp_{l1}',
    'fold'  : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['Zepp_l2']  = {
    'name': 'Zepp_l2',
    'range' : (20,-5,5),
    'xaxis' : 'Zepp_{l2}',
    'fold'  : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['Zepp_ll']  = {
    'name': 'Zepp_ll',
    'range' : (20,0,5),
    'xaxis' : 'Zepp_{ll}',
    'fold'  : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['detajj']  = {
    'name': 'detajj',
    'range' : (20,0,10),
    'xaxis' : '#Delta #eta_{jj}',
    'fold'  : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['detall']  = {
    'name': 'detall',
    'range' : (20,0,10),
    'xaxis' : '#Delta #eta_{ll}',
    'fold'  : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['dphijj']  = {
    'name': 'dphijj',
    'range' : (20,0,3.14),
    'xaxis' : '#Delta #phi_{jj}',
    'fold'  : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['dphilep1jet1']  = {
    'name': 'dphilep1jet1',
    'range' : (20,0,3.14),
    'xaxis' : '#Delta #phi_{l1j1}',
    'fold'  : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['dphilep1jet2']  = {
    'name': 'dphilep1jet2',
    'range' : (20,0,3.14),
    'xaxis' : '#Delta #phi_{l1j2}',
    'fold'  : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['dphilep1jj']  = {
    'name': 'dphilep1jj',
    'range' : (20,0,3.14),
    'xaxis' : '#Delta #phi_{l1jj}',
    'fold'  : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['dphilep2jet1']  = {
    'name': 'dphilep2jet1',
    'range' : (20,0,3.14),
    'xaxis' : '#Delta #phi_{l2j1}',
    'fold'  : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['dphilep2jet2']  = {
    'name': 'dphilep2jet2',
    'range' : (20,0,3.14),
    'xaxis' : '#Delta #phi_{l2j2}',
    'fold'  : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['dphilep2jj']  = {
    'name': 'dphilep2jj',
    'range' : (20,0,3.14),
    'xaxis' : '#Delta #phi_{l2jj}',
    'fold'  : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['dphill']  = {
    'name': 'dphill',
    'range' : (20, 0, 3.14),
    'xaxis' : '#Delta #phi_{ll}',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['dphilljet']  = {
    'name': 'dphilljet',
    'range' : (20, 0, 3.14),
    'xaxis' : '#Delta #phi_{llj}',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['dphilljetjet']  = {
    'name': 'dphilljetjet',
    'range' : (20, 0, 3.14),
    'xaxis' : '#Delta #phi_{lljj}',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['dphillmet']  = {
    'name': 'dphillmet',
    'range' : (20, 0, 3.14),
    'xaxis' : '#Delta #phi_{llMET}',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['dphilmet1']  = {
    'name': 'dphilmet1',
    'range' : (20, 0, 3.14),
    'xaxis' : '#Delta #phi_{l1MET}',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['dphilmet2']  = {
    'name': 'dphilmet2',
    'range' : (20, 0, 3.14),
    'xaxis' : '#Delta #phi_{l2MET}',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['drl1j1']  = {
    'name': 'dr_lj[0]',
    'range' : (20, 0, 8),
    'xaxis' : '#Delta R_{l1j1}',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['drl1j2']  = {
    'name': 'dr_lj[1]',
    'range' : (20, 0, 8),
    'xaxis' : '#Delta R_{l1j2}',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['drl2j1']  = {
    'name': 'dr_lj[2]',
    'range' : (20, 0, 8),
    'xaxis' : '#Delta R_{l2j1}',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['drl2j2']  = {
    'name': 'dr_lj[3]',
    'range' : (20, 0, 8),
    'xaxis' : '#Delta R_{l2j2}',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['drll']  = {
    'name': 'drll',
    'range' : (20, 0, 8),
    'xaxis' : '#Delta R_{ll}',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['ht']  = {
    'name': 'ht',
    'range' : (20, 0, 1000),
    'xaxis' : 'HT [GeV]',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['m2ljj30']  = {
    'name': 'm2ljj30',
    'range' : (30, 0, 3000),
    'xaxis' : 'm_{lljj}',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['mT2']  = {
    'name': 'mT2',
    'range' : (20, 0, 1000),
    'xaxis' : 'm_{T2} [GeV]',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['mTi']  = {
    'name': 'mTi',
    'range' : (20, 0, 1000),
    'xaxis' : 'm_{Ti} [GeV]',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['mlj_00']  = {
    'name': 'm_lj[0]',
    'range' : (20, 0, 2000),
    'xaxis' : 'm_{l1j1} [GeV]',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['mlj_01']  = {
    'name': 'm_lj[1]',
    'range' : (20, 0, 2000),
    'xaxis' : 'm_{l1j2} [GeV]',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['mlj_10']  = {
    'name': 'm_lj[2]',
    'range' : (20, 0, 2000),
    'xaxis' : 'm_{l2j1} [GeV]',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['mlj_11']  = {
    'name': 'm_lj[3]',
    'range' : (20, 0, 2000),
    'xaxis' : 'm_{l2j2} [GeV]',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['mcoll']  = {
    'name': 'mcoll',
    'range' : (20, 0, 1000),
    'xaxis' : 'm_{coll} [GeV]',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['mcollWW']  = {
    'name': 'mcollWW',
    'range' : (20, 0, 1000),
    'xaxis' : 'm_{collWW} [GeV]',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['mjj']  = {
    'name': 'mjj',
    'range' : (30, 0, 3000),
    'xaxis' : 'm_{jj} [GeV]',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['mll'] = {
    'name': 'mll',
    'range' : (20, 0, 1000),
    'xaxis' : 'm_{ll} [GeV]',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['mtw1'] = {
    'name': 'mtw1',
    'range' : (20, 0, 1000),
    'xaxis' : 'm_{T}^{W1} [GeV]',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['mtw2'] = {
    'name': 'mtw2',
    'range' : (20, 0, 1000),
    'xaxis' : 'm_{T}^{W2} [GeV]',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['PuppiMET_phi']  = {
    'name': 'PuppiMET_phi',
    'range' : (20,-3.14,3.14),
    'xaxis' : '#phi^{miss}',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['proxyW1'] = {
    'name': 'proxyW[0]',
    'range' : (20, 0, 500),
    'xaxis' : 'proxy_{W1} [GeV]',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['proxyW2'] = {
    'name': 'proxyW[1]',
    'range' : (20, 0, 500),
    'xaxis' : 'proxy_{W2} [GeV]',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['PuppiMET_pt']  = {
    'name': 'PuppiMET_pt',
    'range' : (30,0,300),
    'xaxis' : 'p_{T}^{miss} [GeV]',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['ptll']  = {
    'name': 'ptll',
    'range' : (20, 0, 500),
    'xaxis' : 'p_{T}^{ll} [GeV]',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['recoil']  = {
    'name': 'recoil',
    'range' : (20, 0, 1000),
    'xaxis' : 'recoil [GeV]',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['yll']  = {
    'name': 'yll',
    'range' : (20, -2.5, 2.5),
    'xaxis' : 'y_{ll}',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

## other

variables['nvtx'] = {     
    'name'  : 'PV_npvsGood',      
    'range' : (100, 0, 100),  
    'xaxis' : 'number of vertices', 
    'fold'  : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['mth']  = {  
    'name': 'mth',     
    'range' : (25, 0, 200),   
    'xaxis' : 'm_{T}^{H} [GeV]',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}

variables['njet']  = {
    'name': 'Sum(CleanJet_pt>30)',
    'range' : (5,0,5),
    'xaxis' : 'Number of jets',
    'fold' : 0,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'isVBS' in cut])
}
