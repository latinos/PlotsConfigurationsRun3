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


#variables['tree'] = {
#    'tree' : {
#        'detajj' : 'detajj',
#        'dphill' : 'dphill',
#        'drll' : 'drll',
#        'mjj' : 'mjj',
#        'ht' : 'ht',
#        'mth' : 'mth',
#        'mll' : 'mll',
#        'puppimet' : 'PuppiMET_pt',
#        'eta1' : 'Lepton_eta[0]',
#        'eta2' : 'Lepton_eta[1]',        
#        'pt1' : 'Lepton_pt[0]',
#        'pt2' : 'Lepton_pt[1]',
#        'jeteta1' : 'Alt(CleanJet_eta, 0, -99) - 9999.9*(CleanJet_pt[0]<30)',
#        'jeteta2' : 'Alt(CleanJet_eta, 1, -99) - 9999.9*(CleanJet_pt[1]<30)',
#        'jetpt1' : 'Alt(CleanJet_pt, 0, -99) - 9999.9*(CleanJet_pt[0]<30)',
#        'jetpt2' : 'Alt(CleanJet_pt, 1, -99) - 9999.9*(CleanJet_pt[1]<30)',
#        'dphillmet' : 'dphillmet',
#        'ptll' : 'ptll',
#        'Ctot' : 'log((abs(2*Lepton_eta[0]-CleanJet_eta[0]-CleanJet_eta[1])+abs(2*Lepton_eta[1]-CleanJet_eta[0]-CleanJet_eta[1]))/detajj)',
#        'mlj11' : 'm_lj[0]',
#        'mlj12' : 'm_lj[1]',
#        'mlj21' : 'm_lj[2]',
#        'mlj22' : 'm_lj[3]',
#        #'nvtx' : 'PV_npvsGood',
#        #'mll' : 'mll',
#        #'mth' : 'mth',
#        #'ptll' : 'ptll',
#        #'drll' : 'drll',
#        #'dphill' : 'dphill',
#        #'pt1' : 'Lepton_pt[0]',
#        #'pt2' : 'Lepton_pt[1]',
#        #'eta1' : 'Lepton_eta[0]',
#        #'eta2' : 'Lepton_eta[1]',
#        #'phi1' : 'Lepton_phi[0]',
#        #'phi2' : 'Lepton_phi[1]',
#        #'puppimet' : 'PuppiMET_pt',
#        #'njet' : 'Sum(CleanJet_pt>30)',
#        #'jetpt1' : 'Alt(CleanJet_pt, 0, -99) - 9999.9*(CleanJet_pt[0]<30)',
#        #'jetpt2' : 'Alt(CleanJet_pt, 1, -99) - 9999.9*(CleanJet_pt[1]<30)',
#        #'jeteta1' : 'Alt(CleanJet_eta, 0, -99) - 9999.9*(CleanJet_pt[0]<30)',
#        #'jeteta2' : 'Alt(CleanJet_eta, 1, -99) - 9999.9*(CleanJet_pt[1]<30)',
#        ##'trig_syst_u' : 'TriggerSFWeight_2l_u/TriggerSFWeight_2l',
#        ##'trig_syst_d' : 'TriggerSFWeight_2l_d/TriggerSFWeight_2l',
#        ##'eff_e_u' : 'SFweightEleUp',
#        ##'eff_e_d' : 'SFweightEleDown',
#        ##'eff_m_u' : 'SFweightMuUp',
#        ##'eff_m_d' : 'SFweightMuDown', 
#        ##'PU' : '1.05',
#        ##'PS_ISR_d' : 'PSWeight[2]',
#        ##'PS_ISR_u' : 'PSWeight[0]',
#        ##'PS_FSR_d' : 'PSWeight[3]',
#        ##'PS_FSR_u' : 'PSWeight[1]',
#        ##'UE_CP5' : '1.015',
#        ##'QCDscale_1' : 'Alt(LHEScaleWeight,0,1)',
#        ##'QCDscale_6' : 'Alt(LHEScaleWeight,nLHEScaleWeight-1,1)'
#    },
#    'cuts' : ['hww_sr'],
#    'blind' : dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}

variables['classvbf'] = { 
    'name': 'vbf_clf[0]',
    'range' : ([0,0.545,0.635,0.695,0.745,0.785,1.],),
    'xaxis' : 'DNN discriminant vbf',
    'fold'  : 3,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}

variables['classtop'] = { 
    'name': 'vbf_clf[2]',
    'range' : (15,0.25,1.),
    'xaxis' : 'DNN discriminant top',
    'fold'  : 3,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])

}

variables['classww'] = { 
    'name': 'vbf_clf[3]',
    'range' : (15,0.25,1.),
    'xaxis' : 'DNN discriminant ww',
    'fold'  : 3,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}


variables['classggh'] = { 
    'name': 'vbf_clf[1]',
    'range' : ([0.,0.485, 0.555, 0.615, 0.665, 0.715, 0.775, 0.865, 1.],),
    'xaxis' : 'DNN discriminant ggh',
    'fold'  : 3,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}

variables['events'] = {
    'name'  : '1',      
    'range' : (1,0,2),  
    'xaxis' : 'events', 
    'fold'  : 3,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}


#variables['events'] = {
#    'name'  : '1',      
#    'range' : (1,0,2),  
#    'xaxis' : 'events', 
#    'fold'  : 3,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}

#variables['mllVSmth'] = {
#    'name'  : 'mll:mth',
#    'range' : ([12, 17, 25, 30, 35, 40, 45, 65, 200],[60, 95, 110, 135, 200],),
#    'xaxis' : 'm_{ll} : m_{T}^{H}',
#    'fold'  : 3,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#variables['snn_isSig']  = {   
#    'name': 'snn_SigVSBkg[0]',      
#    'range' : (20,0,1),
#    'xaxis' : 'SNN(isSig)', 
#    'fold' : 0,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#variables['dbnn_isSig']  = {   
#    'name': 'dbnn_SigVSBkg[0]',      
#    'range' : (20,0,1),
#    'xaxis' : 'DBNN(isSig)', 
#    'fold' : 0,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}


#variables['nvtx'] = {     
#    'name'  : 'PV_npvsGood',      
#    'range' : (100, 0, 100),  
#    'xaxis' : 'number of vertices', 
#    'fold'  : 3,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#
#variables['mll'] = {
#    'name': 'mll',    
#    'range' : (20, 12, 200),
#    'xaxis' : 'm_{ll} [GeV]',
#    'fold' : 0,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#variables['mth']  = {  
#    'name': 'mth',     
#    'range' : (20, 60, 200),   
#    'xaxis' : 'm_{T}^{H} [GeV]',
#    'fold' : 0,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#
#variables['ptll']  = {  
#    'name': 'ptll',     
#    'range' : (20, 30,200),   
#    'xaxis' : 'p_{T}^{ll} [GeV]',
#    'fold' : 0,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#variables['drll']  = {
#    'name': 'drll',
#    'range' : (50, 0,5),
#    'xaxis' : '#Delta R_{ll}',
#    'fold' : 0,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#variables['dphill']  = {
#    'name': 'dphill',
#    'range' : (50, 0,5),
#    'xaxis' : '#Delta #phi_{ll}',
#    'fold' : 0,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#variables['ptll_more']  = {
#    'name': 'ptll',
#    'range' : (50, 0,100),
#    'xaxis' : 'p_{T}^{ll} [GeV]',
#    'fold' : 0,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#variables['pt1']  = { 
#    'name': 'Lepton_pt[0]',     
#    'range' : (20,20,100),
#    'xaxis' : 'p_{T} 1st lep',
#    'fold'  : 3,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])                         
#}
#
#variables['pt2']  = {
#    'name': 'Lepton_pt[1]',     
#    'range' : (20,10,100),   
#    'xaxis' : 'p_{T} 2nd lep',
#    'fold'  : 3,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])                         
#}
#
#variables['eta1']  = {
#    'name': 'Lepton_eta[0]',     
#    'range' : (20,-3,3),   
#    'xaxis' : '#eta 1st lep',
#    'fold'  : 3,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])                         
#}
#
#variables['eta2']  = {
#    'name': 'Lepton_eta[1]',     
#    'range' : (20,-3,3),   
#    'xaxis' : '#eta 2nd lep',
#    'fold'  : 3,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])                         
#}
#
#                        
#variables['phi1']  = {
#    'name': 'Lepton_phi[0]',
#    'range' : (20,-3.2,3.2),
#    'xaxis' : '#phi 1st lep',
#    'fold'  : 3,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#variables['phi2']  = {
#    'name': 'Lepton_phi[1]',
#    'range' : (20,-3.2,3.2),
#    'xaxis' : '#phi 2nd lep',
#    'fold'  : 3,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#variables['jetdeepb']  = {
#    'name': 'Alt(Take(Jet_btagDeepFlavB, CleanJet_jetIdx), 0, -99)',
#    'range' : (30,-1,1),
#    'xaxis' : 'B tagger 1st jet (DeepFlavB)',
#    'fold' : 2,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#variables['jetdeepb2']  = {
#    'name': 'Alt(Take(Jet_btagDeepFlavB, CleanJet_jetIdx), 1, -99) -999.99*(CleanJet_pt[1]<20)',
#    'range' : ([0., 0.0583, 1.],),
#    'xaxis' : 'B tagger 2nd jet (DeepFlavB)',
#    'fold' : 0,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#variables['trkMet']  = { 
#    'name': 'TkMET_pt',
#    'range' : (20,0,200),
#    'xaxis' : 'trk met [GeV]',
#    'fold' : 3,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#variables['puppimet']  = {
#    'name': 'PuppiMET_pt',
#    'range' : (20,0,200),
#    'xaxis' : 'Puppi MET p_{T} [GeV]',
#    'fold' : 3,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
############## New Jet processing
#
#variables['njet']  = {
#    'name': 'Sum(CleanJet_pt>30)',
#    'range' : (5,0,5),
#    'xaxis' : 'Number of jets',
#    'fold' : 2,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#variables['jetpt1']  = {
#    'name': 'Alt(CleanJet_pt, 0, -99) - 9999.9*(CleanJet_pt[0]<30)', 
#    'range' : (20,0,200),
#    'xaxis' : 'p_{T} 1st jet [GeV]',
#    'fold' : 0,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#variables['jetpt2']  = {
#    'name': 'Alt(CleanJet_pt, 1, -99) - 9999.9*(CleanJet_pt[1]<30)',
#    'range' : (20,0,200),
#    'xaxis' : 'p_{T} 2nd jet',
#    'fold' : 0,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#variables['jeteta1']  = {
#    'name': 'Alt(CleanJet_eta, 0, -99) - 9999.9*(CleanJet_pt[0]<30)',
#    'range' : (30,-4.7,4.7),
#    'xaxis' : '#eta 1st jet',
#    'fold' : 0,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#variables['jeteta2']  = {
#    'name': 'Alt(CleanJet_eta, 1, -99) - 9999.9*(CleanJet_pt[1]<30)',
#    'range' : (30,-4.7,4.7),
#    'xaxis' : '#eta 2nd jet',
#    'fold' : 0,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}

#variables['Ctot'] = {
#     'name': 'log((abs(2*Lepton_eta[0]-CleanJet_eta[0]-CleanJet_eta[1])+abs(2*Lepton_eta[1]-CleanJet_eta[0]-CleanJet_eta[1]))/detajj)',
#     'range' : (20,-4.,6.),
#     #'range' : (15,0.25,1.),
#     'xaxis' : 'Ctot',
#     'fold'  : 3,
#     'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#variables['mlj11'] = {
#     'name': 'm_lj[0]',
#     'range' : (28,0.,1400.),
#     #'range' : (15,0.25,1.),
#     'xaxis' : 'mlj11',
#     'fold'  : 3,
#     'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#
#variables['mlj12'] = {
#     'name': 'm_lj[1]',
#     'range' : (28,0.,1400.),
#     #'range' : (15,0.25,1.),
#     'xaxis' : 'mlj12',
#     'fold'  : 3,
#     'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#
#
#variables['mlj21'] = {
#     'name': 'm_lj[2]',
#     'range' : (28,0.,1400.),
#     #'range' : (15,0.25,1.),
#     'xaxis' : 'mlj21',
#     'fold'  : 3,
#     'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#
#variables['mlj22'] = {
#     'name': 'm_lj[3]',
#     'range' : (28,0.,1400.),
#     #'range' : (15,0.25,1.),
#     'xaxis' : 'mlj22',
#     'fold'  : 3,
#     'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}