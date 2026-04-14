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


variables['classvbf'] = { 
    'name': 'vbf_clf[0]',
    'range' : (750,0.25,1.),
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
    #'range' : ([0.,0.485, 0.555, 0.615, 0.665, 0.715, 0.7750, 0.865, 1.],),
    'range' : (750,0.25,1.),
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
#
#variables['mjj']  = {
#    'name': 'mjj',
#    'range' : (20, 100,1100),
#    'xaxis' : 'm_{jj}',
#    'fold' : 0,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#variables['detajj']  = {
#    'name': 'detajj',
#    'range' : (20, 0,10),
#    'xaxis' : '#Delta #eta_{jj}',
#    'fold' : 0,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#variables['ht']  = {
#    'name': 'ht',
#    'range' : (20, 200, 600),
#    'xaxis' : 'H_{T}',
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
#variables['mll'] = {
#    'name': 'mll',    
#    'range' : (20, 12, 200),
#    'xaxis' : 'm_{ll} [GeV]',
#    'fold' : 0,
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
#
#variables['dphillmet']  = {
#    'name': 'dphillmet',
#    'range' : (30, 0,3),
#    'xaxis' : '#Delta #phi_{ll,MET}',
#    'fold' : 0,
#    'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#variables['ptll']  = {  
#    'name': 'ptll',     
#    'range' : (20, 30,200),   
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
#variables['dphill']  = {
#    'name': 'dphill',
#    'range' : (50, 0,5),
#    'xaxis' : '#Delta #phi_{ll}',
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
#variables['Ctot'] = {
#     'name': 'log((abs(2*Lepton_eta[0]-CleanJet_eta[0]-CleanJet_eta[1])+abs(2*Lepton_eta[1]-CleanJet_eta[0]-CleanJet_eta[1]))/detajj)',
#     'range' : (20,-4.,6.),
#     'xaxis' : 'Ctot',
#     'fold'  : 3,
#     'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#variables['mlj11'] = {
#     'name': 'm_lj[0]',
#     'range' : (28,0.,1400.),
#     'xaxis' : 'mlj11',
#     'fold'  : 3,
#     'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#
#variables['mlj12'] = {
#     'name': 'm_lj[1]',
#     'range' : (28,0.,1400.),
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
#     'xaxis' : 'mlj21',
#     'fold'  : 3,
#     'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#
#variables['mlj22'] = {
#     'name': 'm_lj[3]',
#     'range' : (28,0.,1400.),
#     'xaxis' : 'mlj22',
#     'fold'  : 3,
#     'blind'   :  dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
#}
#
#