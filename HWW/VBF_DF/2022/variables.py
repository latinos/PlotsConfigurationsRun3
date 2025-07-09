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

"""
variables['tree'] = {
    'tree' : {
        'nvtx' : 'PV_npvsGood',
        'nvtx_jer_do' : '-99',
        'nvtx_jer_up' : '-99',
        'nvtx_jes_do' : '-99',
        'nvtx_jes_up' : '-99',
        'nvtx_MET_do' : '-99',
        'nvtx_MET_up' : '-99',
        'mll' : 'mll',
        'mll_jer_do' : 'mll__jer_do',
        'mll_jer_up' : 'mll__jer_up',
        'mll_jes_do' : 'mll__jesTotal_do',
        'mll_jes_up' : 'mll__jesTotal_up',
        'mll_MET_up' : 'mll__unclustEn_up',
        'mll_MET_do' : 'mll__unclustEn_do',
        'mth' : 'mth',
        'mth_jer_do' : 'mth__jer_do',
        'mth_jer_up' : 'mth__jer_up',
        'mth_jes_do' : 'mth__jesTotal_do',
        'mth_jes_up' : 'mth__jesTotal_up',
        'mth_MET_up' : 'mth__unclustEn_up',
        'mth_MET_do' : 'mth__unclustEn_do',
        'ptll' : 'ptll',
        'ptll_jer_do' : 'ptll__jer_do',
        'ptll_jer_up' : 'ptll__jer_up',
        'ptll_jes_do' : 'ptll__jesTotal_do',
        'ptll_jes_up' : 'ptll__jesTotal_up',
        'ptll_MET_up' : 'ptll__unclustEn_up',
        'ptll_MET_do' : 'ptll__unclustEn_do',
        'drll' : 'drll',
        'drll_jer_do' : 'drll__jer_do',
        'drll_jer_up' : 'drll__jer_up',
        'drll_jes_do' : 'drll__jesTotal_do',
        'drll_jes_up' : 'drll__jesTotal_up',
        'drll_MET_up' : 'drll__unclustEn_up',
        'drll_MET_do' : 'drll__unclustEn_do',
        'dphill' : 'dphill',
        'dphill_jer_do' : 'dphill__jer_do',
        'dphill_jer_up' : 'dphill__jer_up',
        'dphill_jes_do' : 'dphill__jesTotal_do',
        'dphill_jes_up' : 'dphill__jesTotal_up',
        'dphill_MET_up' : 'dphill__unclustEn_up',
        'dphill_MET_do' : 'dphill__unclustEn_do',
        'pt1' : 'Lepton_pt[0]',
        'pt1_jer_do' : '-99',
        'pt1_jer_up' : '-99',
        'pt1_jes_do' : '-99',
        'pt1_jes_up' : '-99',
        'pt1_MET_do' : '-99',
        'pt1_MET_up' : '-99',
        'pt2' : 'Lepton_pt[1]',
        'pt2_jer_do' : '-99',
        'pt2_jer_up' : '-99',
        'pt2_jes_do' : '-99',
        'pt2_jes_up' : '-99',
        'pt2_MET_do' : '-99',
        'pt2_MET_up' : '-99',
        'eta1' : 'Lepton_eta[0]',
        'eta1_jer_do' : '-99',
        'eta1_jer_up' : '-99',
        'eta1_jes_do' : '-99',
        'eta1_jes_up' : '-99',
        'eta1_MET_do' : '-99',
        'eta1_MET_up' : '-99',
        'eta2' : 'Lepton_eta[1]',
        'eta2_jer_do' : '-99',
        'eta2_jer_up' : '-99',
        'eta2_jes_do' : '-99',
        'eta2_jes_up' : '-99',
        'eta2_MET_do' : '-99',
        'eta2_MET_up' : '-99',
        'phi1' : 'Lepton_phi[0]',
        'phi1_jer_do' : '-99',
        'phi1_jer_up' : '-99',
        'phi1_jes_do' : '-99',
        'phi1_jes_up' : '-99',
        'phi1_MET_do' : '-99',
        'phi1_MET_up' : '-99',
        'phi2' : 'Lepton_phi[1]',
        'phi2_jer_do' : '-99',
        'phi2_jer_up' : '-99',
        'phi2_jes_do' : '-99',
        'phi2_jes_up' : '-99',
        'phi2_MET_do' : '-99',
        'phi2_MET_up' : '-99',
        'jetdeepb' : 'Alt(Take(Jet_btagDeepFlavB, CleanJet_jetIdx), 0, -99)',
        'jetdeepb_jer_do' : '-99',
        'jetdeepb_jer_up' : '-99',
        'jetdeepb_jes_do' : '-99',
        'jetdeepb_jes_up' : '-99',
        'jetdeepb_MET_do' : '-99',
        'jetdeepb_MET_up' : '-99',
        'trkMet' : 'TkMET_pt',
        'trkMet_jer_do' : '-99',
        'trkMet_jer_up' : '-99',
        'trkMet_jes_do' : '-99',
        'trkMet_jes_up' : '-99',
        'trkMet_MET_do' : '-99',
        'trkMet_MET_up' : '-99',
        'puppimet' : 'PuppiMET_pt',
        'puppimet_jer_do' : 'PuppiMET_pt__jer_do',
        'puppimet_jer_up' : 'PuppiMET_pt__jer_up',
        'puppimet_jes_do' : 'PuppiMET_pt__jesTotal_do',
        'puppimet_jes_up' : 'PuppiMET_pt__jesTotal_up',
        'puppimet_MET_do' : 'PuppiMET_pt__unclustEn_do',
        'puppimet_MET_up' : 'PuppiMET_pt__unclustEn_up',
        'njet' : 'Sum(CleanJet_pt>30)',
        'njet_jer_do' : 'Sum(CleanJet_pt__jer_do>30)',
        'njet_jer_up' : 'Sum(CleanJet_pt__jer_up>30)',
        'njet_jes_do' : 'Sum(CleanJet_pt__jesTotal_do>30)',
        'njet_jes_up' : 'Sum(CleanJet_pt__jesTotal_up>30)',
        'njet_MET_do' : '-99',
        'njet_MET_up' : '-99',
        'jetpt1' : 'Alt(CleanJet_pt, 0, 0)*(CleanJet_pt[0]>30)',
        'jetpt1_jer_do' : 'Alt(CleanJet_pt__jer_do, 0, 0)*(CleanJet_pt__jer_do[0]>30)',
        'jetpt1_jer_up' : 'Alt(CleanJet_pt__jer_up, 0, 0)*(CleanJet_pt__jer_up[0]>30)',
        'jetpt1_jes_do' : 'Alt(CleanJet_pt__jesTotal_do, 0, 0)*(CleanJet_pt__jesTotal_do[0]>30)',
        'jetpt1_jes_up' : 'Alt(CleanJet_pt__jesTotal_up, 0, 0)*(CleanJet_pt__jesTotal_up[0]>30)',
        'jetpt1_MET_do' : '-99',
        'jetpt1_MET_up' : '-99',
        'jetpt2' : 'Alt(CleanJet_pt, 1, 0)*(CleanJet_pt[1]>30)',
        'jetpt2_jer_do' : 'Alt(CleanJet_pt__jer_do, 1, 0)*(CleanJet_pt__jer_do[1]>30)',
        'jetpt2_jer_up' : 'Alt(CleanJet_pt__jer_up, 1, 0)*(CleanJet_pt__jer_up[1]>30)',
        'jetpt2_jes_do' : 'Alt(CleanJet_pt__jesTotal_do, 1, 0)*(CleanJet_pt__jesTotal_do[1]>30)',
        'jetpt2_jes_up' : 'Alt(CleanJet_pt__jesTotal_up, 1, 0)*(CleanJet_pt__jesTotal_up[1]>30)',
        'jetpt2_MET_do' : '-99',
        'jetpt2_MET_up' : '-99',
        'jeteta1' : 'Alt(CleanJet_eta, 0, -99)*(Alt(CleanJet_pt, 0, 0)>30)-99*(Alt(CleanJet_pt,0,0)<30)',
        'jeteta1_jer_do' : 'Alt(CleanJet_eta__jer_do, 0, -99)*(Alt(CleanJet_pt__jer_do, 0, 0)>30)-99*(Alt(CleanJet_pt__jer_do,0,0)<30)',
        'jeteta1_jer_up' : 'Alt(CleanJet_eta__jer_up, 0, -99)*(Alt(CleanJet_pt__jer_up, 0, 0)>30)-99*(Alt(CleanJet_pt__jer_up,0,0)<30)',
        'jeteta1_jes_do' : 'Alt(CleanJet_eta__jesTotal_do, 0, -99)*(Alt(CleanJet_pt__jesTotal_do, 0, 0)>30)-99*(Alt(CleanJet_pt__jesTotal_do,0,0)<30)',
        'jeteta1_jes_up' : 'Alt(CleanJet_eta__jesTotal_up, 0, -99)*(Alt(CleanJet_pt__jesTotal_up, 0, 0)>30)-99*(Alt(CleanJet_pt__jesTotal_up,0,0)<30)',
        'jeteta1_MET_do' : '-99',
        'jeteta1_MET_up' : '-99',
        'jeteta2' : 'Alt(CleanJet_eta, 1, -99)*(Alt(CleanJet_pt, 1, 0)>30)-99*(Alt(CleanJet_pt,1,0)<30)',
        'jeteta2_jer_do' : 'Alt(CleanJet_eta__jer_do, 1, -99)*(Alt(CleanJet_pt__jer_do, 1, 0)>30)-99*(Alt(CleanJet_pt__jer_do,1,0)<30)',
        'jeteta2_jer_up' : 'Alt(CleanJet_eta__jer_up, 1, -99)*(Alt(CleanJet_pt__jer_up, 1, 0)>30)-99*(Alt(CleanJet_pt__jer_up,1,0)<30)',
        'jeteta2_jes_do' : 'Alt(CleanJet_eta__jesTotal_do, 1, -99)*(Alt(CleanJet_pt__jesTotal_do, 1, 0)>30)-99*(Alt(CleanJet_pt__jesTotal_do,1,0)<30)',
        'jeteta2_jes_up' : 'Alt(CleanJet_eta__jesTotal_up, 1, -99)*(Alt(CleanJet_pt__jesTotal_up, 1, 0)>30)-99*(Alt(CleanJet_pt__jesTotal_up,1,0)<30)',
        'jeteta2_MET_do' : '-99',
        'jeteta2_MET_up' : '-99',
        'trig_syst_u' : 'TriggerSFWeight_2l_u/TriggerSFWeight_2l',
        'trig_syst_d' : 'TriggerSFWeight_2l_d/TriggerSFWeight_2l',
        'eff_e_u' : 'SFweightEleUp',
        'eff_e_d' : 'SFweightEleDown',
        'eff_m_u' : 'SFweightMuUp',
        'eff_m_d' : 'SFweightMuDown', 
        'PU' : '1.05',
        'PS_ISR_d' : 'PSWeight[2]',
        'PS_ISR_u' : 'PSWeight[0]',
        'PS_FSR_d' : 'PSWeight[3]',
        'PS_FSR_u' : 'PSWeight[1]',
        'UE_CP5' : '1.015',
        'QCDscale_1' : 'Alt(LHEScaleWeight,0,1)',
        'QCDscale_2' : 'Alt(LHEScaleWeight,1,1)',
        'QCDscale_3' : 'Alt(LHEScaleWeight,3,1)',
        'QCDscale_4' : 'Alt(LHEScaleWeight,nLHEScaleWeight-4,1)',
        'QCDscale_5' : 'Alt(LHEScaleWeight,nLHEScaleWeight-2,1)',
        'QCDscale_6' : 'Alt(LHEScaleWeight,nLHEScaleWeight-1,1)'
    },
    'cuts' : ['hww_sr'],
    'blind' : dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}


variables['adnn_isSig']  = {   
                            'name': 'adnn_SigVSBkg[0]',      
                            'range' : (20,0,1),
                            'xaxis' : 'ADNN(isSig)', 
                            'fold' : 0,
                            'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
                            }

variables['dbnn_isSig_0j']  = {   
                            'name': 'dbnn_SigVSBkg_0j[0]',      
                            'range' : (20,0,1),
                            'xaxis' : 'DBNN(isSig)', 
                            'fold' : 0,
                            'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
                            }

variables['dbnn_isSig_1j']  = {   
                            'name': 'dbnn_SigVSBkg_1j[0]',      
                            'range' : (20,0,1),
                            'xaxis' : 'DBNN(isSig)', 
                            'fold' : 0,
                            'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
                            }

variables['dbnn_isSig_2j']  = {   
                            'name': 'dbnn_SigVSBkg_2j[0]',      
                            'range' : (20,0,1),
                            'xaxis' : 'DBNN(isSig)', 
                            'fold' : 0,
                            'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
                            }


variables['snn_isSig_0j']  = {   
                            'name': 'snn_SigVSBkg_0j[0]',      
                            'range' : (20,0,1),
                            'xaxis' : 'SNN(isSig)', 
                            'fold' : 0,
                            'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
                            }

variables['snn_isSig_1j']  = {   
                            'name': 'snn_SigVSBkg_1j[0]',      
                            'range' : (20,0,1),
                            'xaxis' : 'SNN(isSig)', 
                            'fold' : 0,
                            'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
                            }

variables['snn_isSig_2j']  = {   
                            'name': 'snn_SigVSBkg_2j[0]',      
                            'range' : (20,0,1),
                            'xaxis' : 'SNN(isSig)', 
                            'fold' : 0,
                            'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
                            }

"""

#variables['events_lowpt'] = {
#    'name'  : '1*(CleanJet_pt[0] > 40 && CleanJet_pt[0] < 50)',      
#    'range' : (2,1,2),  
#    'xaxis' : 'events_lowpt', 
#    'fold'  : 0,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#variables['events_highpt'] = {
#    'name'  : '1*(CleanJet_pt[0] > 140 && CleanJet_pt[0] < 150)',      
#    'range' : (2,1,2),  
#    'xaxis' : 'events_highpt', 
#    'fold'  : 0,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}


variables['events'] = {
    'name'  : '1',      
    'range' : (1,0,2),  
    'xaxis' : 'events', 
    'fold'  : 3,
    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}

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


bin_mll = ['12.', '17.', '25.', '30.', '35.', '40.', '45.', '65.', '200.']
bin_mth = ['60.', '95.', '110.', '135.', '200.']
variables['mllVSmth_optim'] = {
        'name': 'mllVSmth_optim',
        'range': ((len(bin_mth)-1)*(len(bin_mll)-1), 1, (len(bin_mth)-1)*(len(bin_mll)-1)+1),
        'xaxis': 'm_{ll} : m_{T}^{H}',
        'fold' :3,
        'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}
"""
