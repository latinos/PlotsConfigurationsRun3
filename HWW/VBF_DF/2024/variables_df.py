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
        'baseSF' : 'XSWeight*METFilter_Common*PromptGenLepMatch2l*SFweight',
######## detajj
        'detajj' : 'detajj',
        'detajj_relsample_up' : 'detajj_jesRegroed_RelativeSample_2024up',
        'detajj_relsample_down' : 'detajj_jesRegroed_RelativeSample_2024do',
        'detajj_jer_up' : 'detajj_jerup',
        'detajj_jer_down' : 'detajj_jerdo',
        'detajj_absolute_up' : 'detajj_jesRegroed_Absoluteup',
        'detajj_absolute_down' : 'detajj_jesRegroed_Absolutedo',
        'detajj_flavor_up' : 'detajj_jesRegroed_FlavorQCDup',
        'detajj_flavor_down' : 'detajj_jesRegroed_FlavorQCDdo',
######## dphill
        'dphill' : 'dphill',
        'dphill_relsample_up' : 'dphill_jesRegroed_RelativeSample_2024up',
        'dphill_relsample_down' : 'dphill_jesRegroed_RelativeSample_2024do',
        'dphill_jer_up' : 'dphill_jerup',
        'dphill_jer_down' : 'dphill_jerdo',
        'dphill_absolute_up' : 'dphill_jesRegroed_Absoluteup',
        'dphill_absolute_down' : 'dphill_jesRegroed_Absolutedo',
        'dphill_flavor_up' : 'dphill_jesRegroed_FlavorQCDup',
        'dphill_flavor_down' : 'dphill_jesRegroed_FlavorQCDdo',
        'dphill_lepres_up' : 'dphill_leptonResolutionup',
        'dphill_lepres_down' : 'dphill_leptonResolutiondo',
######## drll
        'drll' : 'drll',
        'drll_relsample_up' : 'drll_jesRegroed_RelativeSample_2024up',
        'drll_relsample_down' : 'drll_jesRegroed_RelativeSample_2024do',
        'drll_jer_up' : 'drll_jerup',
        'drll_jer_down' : 'drll_jerdo',
        'drll_absolute_up' : 'drll_jesRegroed_Absoluteup',
        'drll_absolute_down' : 'drll_jesRegroed_Absolutedo',
        'drll_flavor_up' : 'drll_jesRegroed_FlavorQCDup',
        'drll_flavor_down' : 'drll_jesRegroed_FlavorQCDdo',
        'drll_lepres_up' : 'drll_leptonResolutionup',
        'drll_lepres_down' : 'drll_leptonResolutiondo',
######## mjj
        'mjj' : 'mjj',
        'mjj_relsample_up' : 'mjj_jesRegroed_RelativeSample_2024up',
        'mjj_relsample_down' : 'mjj_jesRegroed_RelativeSample_2024do',
        'mjj_jer_up' : 'mjj_jerup',
        'mjj_jer_down' : 'mjj_jerdo',
        'mjj_absolute_up' : 'mjj_jesRegroed_Absoluteup',
        'mjj_absolute_down' : 'mjj_jesRegroed_Absolutedo',
        'mjj_flavor_up' : 'mjj_jesRegroed_FlavorQCDup',
        'mjj_flavor_down' : 'mjj_jesRegroed_FlavorQCDdo',
######## ht
        'ht' : 'ht',
        'ht_relsample_up' : 'ht_jesRegroed_RelativeSample_2024up',
        'ht_relsample_down' : 'ht_jesRegroed_RelativeSample_2024do',
        'ht_jer_up' : 'ht_jerup',
        'ht_jer_down' : 'ht_jerdo',
        'ht_absolute_up' : 'ht_jesRegroed_Absoluteup',
        'ht_absolute_down' : 'ht_jesRegroed_Absolutedo',
        'ht_flavor_up' : 'ht_jesRegroed_FlavorQCDup',
        'ht_flavor_down' : 'ht_jesRegroed_FlavorQCDdo',
        'ht_lepres_up' : 'ht_leptonResolutionup',
        'ht_lepres_down' : 'ht_leptonResolutiondo',
######## mth
        'mth' : 'mth',
        'mth_relsample_up' : 'mth_jesRegroed_RelativeSample_2024up',
        'mth_relsample_down' : 'mth_jesRegroed_RelativeSample_2024do',
        'mth_jer_up' : 'mth_jerup',
        'mth_jer_down' : 'mth_jerdo',
        'mth_absolute_up' : 'mth_jesRegroed_Absoluteup',
        'mth_absolute_down' : 'mth_jesRegroed_Absolutedo',
        'mth_flavor_up' : 'mth_jesRegroed_FlavorQCDup',
        'mth_flavor_down' : 'mth_jesRegroed_FlavorQCDdo',
        'mth_lepres_up' : 'mth_leptonResolutionup',
        'mth_lepres_down' : 'mth_leptonResolutiondo',
######## mll
        'mll' : 'mll',
        'mll_relsample_up' : 'mll_jesRegroed_RelativeSample_2024up',
        'mll_relsample_down' : 'mll_jesRegroed_RelativeSample_2024do',
        'mll_jer_up' : 'mll_jerup',
        'mll_jer_down' : 'mll_jerdo',
        'mll_absolute_up' : 'mll_jesRegroed_Absoluteup',
        'mll_absolute_down' : 'mll_jesRegroed_Absolutedo',
        'mll_flavor_up' : 'mll_jesRegroed_FlavorQCDup',
        'mll_flavor_down' : 'mll_jesRegroed_FlavorQCDdo',
        'mll_lepres_up' : 'mll_leptonResolutionup',
        'mll_lepres_down' : 'mll_leptonResolutiondo',
######## puppimet
        'puppimet' : 'PuppiMET_pt',
        'puppimet_relsample_up' : 'PuppiMET_pt_jesRegroed_RelativeSample_2024up',
        'puppimet_relsample_down' : 'PuppiMET_pt_jesRegroed_RelativeSample_2024do',
        'puppimet_jer_up' : 'PuppiMET_pt_jerup',
        'puppimet_jer_down' : 'PuppiMET_pt_jerdo',
        'puppimet_absolute_up' : 'PuppiMET_pt_jesRegroed_Absoluteup',
        'puppimet_absolute_down' : 'PuppiMET_pt_jesRegroed_Absolutedo',
        'puppimet_flavor_up' : 'PuppiMET_pt_jesRegroed_FlavorQCDup',
        'puppimet_flavor_down' : 'PuppiMET_pt_jesRegroed_FlavorQCDdo',
        'puppimet_lepres_up' : 'PuppiMET_pt_leptonResolutionup',
        'puppimet_lepres_down' : 'PuppiMET_pt_leptonResolutiondo',
######## eta1
        'eta1' : 'Lepton_eta[0]',
######## eta2
        'eta2' : 'Lepton_eta[1]',
######## pt1
        'pt1' : 'Lepton_pt[0]',
        'pt1_lepres_up' : 'Lepton_pt_leptonResolutionup[0]',
        'pt1_lepres_down' : 'Lepton_pt_leptonResolutiondo[0]',    
######## pt2
        'pt2' : 'Lepton_pt[1]',
        'pt2_lepres_up' : 'Lepton_pt_leptonResolutionup[1]',
        'pt2_lepres_down' : 'Lepton_pt_leptonResolutiondo[1]',    
######## jeteta1
        'jeteta1' : 'Alt(CleanJet_eta, 0, -99) - 9999.9*(CleanJet_pt[0]<30)',
        'jeteta1_relsample_up' : 'Alt(CleanJet_eta_jesRegroed_RelativeSample_2024up, 0, -99) - 9999.9*(CleanJet_pt_jesRegroed_RelativeSample_2024up[0]<30)',
        'jeteta1_relsample_down' : 'Alt(CleanJet_eta_jesRegroed_RelativeSample_2024do, 0, -99) - 9999.9*(CleanJet_pt_jesRegroed_RelativeSample_2024do[0]<30)',
        'jeteta1_jer_up' : 'Alt(CleanJet_eta_jerup, 0, -99) - 9999.9*(CleanJet_pt_jerup[0]<30)',
        'jeteta1_jer_down' : 'Alt(CleanJet_eta_jerdo, 0, -99) - 9999.9*(CleanJet_pt_jerdo[0]<30)',
        'jeteta1_absolute_up' : 'Alt(CleanJet_eta_jesRegroed_Absoluteup, 0, -99) - 9999.9*(CleanJet_pt_jesRegroed_Absoluteup[0]<30)',
        'jeteta1_absolute_down' : 'Alt(CleanJet_eta_jesRegroed_Absolutedo, 0, -99) - 9999.9*(CleanJet_pt_jesRegroed_Absolutedo[0]<30)',
        'jeteta1_flavor_up' : 'Alt(CleanJet_eta_jesRegroed_FlavorQCDup, 0, -99) - 9999.9*(CleanJet_pt_jesRegroed_FlavorQCDup[0]<30)',
        'jeteta1_flavor_down' : 'Alt(CleanJet_eta_jesRegroed_FlavorQCDdo, 0, -99) - 9999.9*(CleanJet_pt_jesRegroed_FlavorQCDdo[0]<30)',
######## jeteta2
        'jeteta2' : 'Alt(CleanJet_eta, 1, -99) - 9999.9*(CleanJet_pt[1]<30)',
        'jeteta2_relsample_up' : 'Alt(CleanJet_eta_jesRegroed_RelativeSample_2024up, 1, -99) - 9999.9*(CleanJet_pt_jesRegroed_RelativeSample_2024up[1]<30)',
        'jeteta2_relsample_down' : 'Alt(CleanJet_eta_jesRegroed_RelativeSample_2024do, 1, -99) - 9999.9*(CleanJet_pt_jesRegroed_RelativeSample_2024do[1]<30)',
        'jeteta2_jer_up' : 'Alt(CleanJet_eta_jerup, 1, -99) - 9999.9*(CleanJet_pt_jerup[1]<30)',
        'jeteta2_jer_down' : 'Alt(CleanJet_eta_jerdo, 1, -99) - 9999.9*(CleanJet_pt_jerdo[1]<30)',
        'jeteta2_absolute_up' : 'Alt(CleanJet_eta_jesRegroed_Absoluteup, 1, -99) - 9999.9*(CleanJet_pt_jesRegroed_Absoluteup[1]<30)',
        'jeteta2_absolute_down' : 'Alt(CleanJet_eta_jesRegroed_Absolutedo, 1, -99) - 9999.9*(CleanJet_pt_jesRegroed_Absolutedo[1]<30)',
        'jeteta2_flavor_up' : 'Alt(CleanJet_eta_jesRegroed_FlavorQCDup, 1, -99) - 9999.9*(CleanJet_pt_jesRegroed_FlavorQCDup[1]<30)',
        'jeteta2_flavor_down' : 'Alt(CleanJet_eta_jesRegroed_FlavorQCDdo, 1, -99) - 9999.9*(CleanJet_pt_jesRegroed_FlavorQCDdo[1]<30)',
######## jetpt1
        'jetpt1' : 'Alt(CleanJet_pt, 0, -99) - 9999.9*(CleanJet_pt[0]<30)',
        'jetpt1_relsample_up' : 'Alt(CleanJet_pt_jesRegroed_RelativeSample_2024up, 0, -99) - 9999.9*(CleanJet_pt_jesRegroed_RelativeSample_2024up[0]<30)',
        'jetpt1_relsample_down' : 'Alt(CleanJet_pt_jesRegroed_RelativeSample_2024do, 0, -99) - 9999.9*(CleanJet_pt_jesRegroed_RelativeSample_2024do[0]<30)',
        'jetpt1_jer_up' : 'Alt(CleanJet_pt_jerup, 0, -99) - 9999.9*(CleanJet_pt_jerup[0]<30)',
        'jetpt1_jer_down' : 'Alt(CleanJet_pt_jerdo, 0, -99) - 9999.9*(CleanJet_pt_jerdo[0]<30)',
        'jetpt1_absolute_up' : 'Alt(CleanJet_pt_jesRegroed_Absoluteup, 0, -99) - 9999.9*(CleanJet_pt_jesRegroed_Absoluteup[0]<30)',
        'jetpt1_absolute_down' : 'Alt(CleanJet_pt_jesRegroed_Absolutedo, 0, -99) - 9999.9*(CleanJet_pt_jesRegroed_Absolutedo[0]<30)',
        'jetpt1_flavor_up' : 'Alt(CleanJet_pt_jesRegroed_FlavorQCDup, 0, -99) - 9999.9*(CleanJet_pt_jesRegroed_FlavorQCDup[0]<30)',
        'jetpt1_flavor_down' : 'Alt(CleanJet_pt_jesRegroed_FlavorQCDdo, 0, -99) - 9999.9*(CleanJet_pt_jesRegroed_FlavorQCDdo[0]<30)',
######## jetpt2
        'jetpt2' : 'Alt(CleanJet_pt, 1, -99) - 9999.9*(CleanJet_pt[1]<30)',
        'jetpt2_relsample_up' : 'Alt(CleanJet_pt_jesRegroed_RelativeSample_2024up, 1, -99) - 9999.9*(CleanJet_pt_jesRegroed_RelativeSample_2024up[1]<30)',
        'jetpt2_relsample_down' : 'Alt(CleanJet_pt_jesRegroed_RelativeSample_2024do, 1, -99) - 9999.9*(CleanJet_pt_jesRegroed_RelativeSample_2024do[1]<30)',
        'jetpt2_jer_up' : 'Alt(CleanJet_pt_jerup, 1, -99) - 9999.9*(CleanJet_pt_jerup[1]<30)',
        'jetpt2_jer_down' : 'Alt(CleanJet_pt_jerdo, 1, -99) - 9999.9*(CleanJet_pt_jerdo[1]<30)',
        'jetpt2_absolute_up' : 'Alt(CleanJet_pt_jesRegroed_Absoluteup, 1, -99) - 9999.9*(CleanJet_pt_jesRegroed_Absoluteup[1]<30)',
        'jetpt2_absolute_down' : 'Alt(CleanJet_pt_jesRegroed_Absolutedo, 1, -99) - 9999.9*(CleanJet_pt_jesRegroed_Absolutedo[1]<30)',
        'jetpt2_flavor_up' : 'Alt(CleanJet_pt_jesRegroed_FlavorQCDup, 1, -99) - 9999.9*(CleanJet_pt_jesRegroed_FlavorQCDup[1]<30)',
        'jetpt2_flavor_down' : 'Alt(CleanJet_pt_jesRegroed_FlavorQCDdo, 1, -99) - 9999.9*(CleanJet_pt_jesRegroed_FlavorQCDdo[1]<30)',
######## dphillmet
        'dphillmet' : 'dphillmet',
        'dphillmet_relsample_up' : 'dphillmet_jesRegroed_RelativeSample_2024up',
        'dphillmet_relsample_down' : 'dphillmet_jesRegroed_RelativeSample_2024do',
        'dphillmet_jer_up' : 'dphillmet_jerup',
        'dphillmet_jer_down' : 'dphillmet_jerdo',
        'dphillmet_absolute_up' : 'dphillmet_jesRegroed_Absoluteup',
        'dphillmet_absolute_down' : 'dphillmet_jesRegroed_Absolutedo',
        'dphillmet_flavor_up' : 'dphillmet_jesRegroed_FlavorQCDup',
        'dphillmet_flavor_down' : 'dphillmet_jesRegroed_FlavorQCDdo',
        'dphillmet_lepres_up' : 'dphillmet_leptonResolutionup',
        'dphillmet_lepres_down' : 'dphillmet_leptonResolutiondo',
######## ptll
        'ptll' : 'ptll',
        'ptll_relsample_up' : 'ptll_jesRegroed_RelativeSample_2024up',
        'ptll_relsample_down' : 'ptll_jesRegroed_RelativeSample_2024do',
        'ptll_jer_up' : 'ptll_jerup',
        'ptll_jer_down' : 'ptll_jerdo ',
        'ptll_absolute_up' : 'ptll_jesRegroed_Absoluteup',
        'ptll_absolute_down' : 'ptll_jesRegroed_Absolutedo',
        'ptll_flavor_up' : 'ptll_jesRegroed_FlavorQCDup',
        'ptll_flavor_down' : 'ptll_jesRegroed_FlavorQCDdo',
        'ptll_lepres_up' : 'ptll_leptonResolutionup',
        'ptll_lepres_down' : 'ptll_leptonResolutiondo',
######## Ctot
        'Ctot' : 'log((abs(2*Lepton_eta[0]-CleanJet_eta[0]-CleanJet_eta[1])+abs(2*Lepton_eta[1]-CleanJet_eta[0]-CleanJet_eta[1]))/detajj)',
        'Ctot_relsample_up' : 'log((abs(2*Lepton_eta[0]-CleanJet_eta_jesRegroed_RelativeSample_2024up[0]-CleanJet_eta_jesRegroed_RelativeSample_2024up[1])+abs(2*Lepton_eta[1]-CleanJet_eta_jesRegroed_RelativeSample_2024up[0]-CleanJet_eta_jesRegroed_RelativeSample_2024up[1]))/detajj_jesRegroed_RelativeSample_2024up)',
        'Ctot_relsample_down' : 'log((abs(2*Lepton_eta[0]-CleanJet_eta_jesRegroed_RelativeSample_2024do[0]-CleanJet_eta_jesRegroed_RelativeSample_2024do[1])+abs(2*Lepton_eta[1]-CleanJet_eta_jesRegroed_RelativeSample_2024do[0]-CleanJet_eta_jesRegroed_RelativeSample_2024do[1]))/detajj_jesRegroed_RelativeSample_2024do)',
        'Ctot_jer_up' : 'log((abs(2*Lepton_eta[0]-CleanJet_eta_jerup[0]-CleanJet_eta_jerup[1])+abs(2*Lepton_eta[1]-CleanJet_eta_jerup[0]-CleanJet_eta_jerup[1]))/detajj_jerup)',
        'Ctot_jer_down' : 'log((abs(2*Lepton_eta[0]-CleanJet_eta_jerdo[0]-CleanJet_eta_jerdo[1])+abs(2*Lepton_eta[1]-CleanJet_eta_jerdo[0]-CleanJet_eta_jerdo[1]))/detajj_jerdo)',
        'Ctot_absolute_up' : 'log((abs(2*Lepton_eta[0]-CleanJet_eta_jesRegroed_Absoluteup[0]-CleanJet_eta_jesRegroed_Absoluteup[1])+abs(2*Lepton_eta[1]-CleanJet_eta_jesRegroed_Absoluteup[0]-CleanJet_eta_jesRegroed_Absoluteup[1]))/detajj_jesRegroed_Absoluteup)',
        'Ctot_absolute_down' : 'log((abs(2*Lepton_eta[0]-CleanJet_eta_jesRegroed_Absolutedo[0]-CleanJet_eta_jesRegroed_Absolutedo[1])+abs(2*Lepton_eta[1]-CleanJet_eta_jesRegroed_Absolutedo[0]-CleanJet_eta_jesRegroed_Absolutedo[1]))/detajj_jesRegroed_Absolutedo)',
        'Ctot_flavor_up' : 'log((abs(2*Lepton_eta[0]-CleanJet_eta_jesRegroed_FlavorQCDup[0]-CleanJet_eta_jesRegroed_FlavorQCDup[1])+abs(2*Lepton_eta[1]-CleanJet_eta_jesRegroed_FlavorQCDup[0]-CleanJet_eta_jesRegroed_FlavorQCDup[1]))/detajj_jesRegroed_FlavorQCDup)',
        'Ctot_flavor_down' : 'log((abs(2*Lepton_eta[0]-CleanJet_eta_jesRegroed_FlavorQCDdo[0]-CleanJet_eta_jesRegroed_FlavorQCDdo[1])+abs(2*Lepton_eta[1]-CleanJet_eta_jesRegroed_FlavorQCDdo[0]-CleanJet_eta_jesRegroed_FlavorQCDdo[1]))/detajj_jesRegroed_FlavorQCDdo)',
######## mlj11
        'mlj11' : 'm_lj[0]',
######## mlj12
        'mlj12' : 'm_lj[1]',
######## mlj21
        'mlj21' : 'm_lj[2]',
######## mlj22
        'mlj22' : 'm_lj[3]',
######## weights
        'PS_ISR_d' : 'PSWeight[2]',
        'PS_ISR_u' : 'PSWeight[0]',
        'PS_FSR_d' : 'PSWeight[3]',
        'PS_FSR_u' : 'PSWeight[1]',
        'btagSF_bc_unc_up' : 'btagSFbc_up_correlated/btagSFbc',
        'btagSF_bc_unc_down' : 'btagSFbc_down_correlated/btagSFbc',
        'QCDscale_up' : 'Alt(LHEScaleWeight,0,1)',
        'QCDscale_down' : 'Alt(LHEScaleWeight,nLHEScaleWeight-1,1)'
    },
    'cuts' : ['hww_sr'],
    'blind' : dict([(cut, 'full') for cut in cuts2j if 'hww_sr' in cut])
}