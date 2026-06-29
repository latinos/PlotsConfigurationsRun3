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


variables['tree'] = {
    'tree' : {
        # 'baseSF' : 'XSWeight*METFilter_Common*PromptGenLepMatch2l*SFweight',
######## dphill
        'dphill' : 'dphill',
######## drll
        'drll' : 'drll',
######## mth
        'mth' : 'mth',
######## mll
        'mll' : 'mll',
######## puppimet
        'puppimet' : 'PuppiMET_pt',
######## eta1
        'eta1' : 'Lepton_eta[0]',
######## eta2
        'eta2' : 'Lepton_eta[1]',
######## pt1
        'pt1' : 'Lepton_pt[0]',   
######## pt2
        'pt2' : 'Lepton_pt[1]',  
######## jeteta1
        'jeteta1' : 'Alt(CleanJet_eta, 0, -99) - 9999.9*(CleanJet_pt[0]<30)',
######## jeteta2
        'jeteta2' : 'Alt(CleanJet_eta, 1, -99) - 9999.9*(CleanJet_pt[1]<30)',
######## jetpt1
        'jetpt1' : 'Alt(CleanJet_pt, 0, -99) - 9999.9*(CleanJet_pt[0]<30)',
######## jetpt2
        'jetpt2' : 'Alt(CleanJet_pt, 1, -99) - 9999.9*(CleanJet_pt[1]<30)',
######## dphillmet
        'dphillmet' : 'dphillmet',
######## ptll
        'ptll' : 'ptll',
    },
    'cuts' : ['hww_sr'],
    'blind' : dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}