cuts = {}

preselections = 'Lepton_pt[0] > 25 && Lepton_pt[1] > 10 \
            && abs(Lepton_eta[0]) < 2.5 && abs(Lepton_eta[1]) < 2.5 \
            && Alt(Lepton_pt, 2, 0) < 10.0 \
            && mll > 12 \
            && bVeto \
            && (Lepton_pdgId[0]*Lepton_pdgId[1] < 0) \
            && mth > 40 \
            && mtw2 > 30 \
            && ptll > 15 \
            && PuppiMET_pt > 20 \
'

# && mpmet > 15 \

# Preselections - only needed to calculate efficiencies
cuts['basic_selections'] = {
    'expr' : 'mll > 12', # transparent selection, already present in preselections
    'categories' : {
        'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
        'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
        'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
        'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
        'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
        'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
    }
}

# Muon ID: Tight ID POG
# Ele  ID: wp90iso
cuts['sr_ele_wp90iso_mu_cut_TightID_POG'] = {
    'expr' : 'LepWPCut__ele_wp90iso__mu_cut_TightID_POG > 0.5',
    'categories' : {
        'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
        'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
        'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
        'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
        'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
        'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
    }
}

# Muon ID: Tight HWW
# Ele  ID: mvaWinter22V2Iso_WP90
cuts['sr_ele_mvaWinter22V2Iso_WP90_mu_cut_Tight_HWW'] = {
    'expr' : 'LepWPCut__ele_mvaWinter22V2Iso_WP90__mu_cut_Tight_HWW > 0.5',
    'categories' : {
        'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
        'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
        'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
        'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
        'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
        'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
    }
}

# Muon ID: Tight ID MiniIso HWW
# Ele  ID: mvaWinter22V2Iso_WP90
cuts['sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightMiniIso_HWW'] = {
    'expr' : 'LepWPCut__ele_mvaWinter22V2Iso_WP90__mu_cut_TightMiniIso_HWW > 0.5',
    'categories' : {
        'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
        'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
        'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
        'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
        'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
        'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
    }
}



# cuts['ss']  = {
#     'expr' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == 11*13) && mll>12 && bVeto',
#     'categories' : {
#         'em' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == 11*13)',
#     }
# }


# cuts['ww2l2nu_top']  = {
#     'expr' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == -11*13) && topcr && ptll_>15 && PuppiMET_pt > 20',
#     'categories' : {
#         'inc' :'Lepton_pt[0]>20'
#     }
# }

# cuts['ww2l2nu_dytt']  = {
#     'expr' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == -11*13) && bVeto && mth_<40 && ptll_>15 && PuppiMET_pt > 20',
#     'categories' : {
#         'inc' : 'Lepton_pt[0]>20'
#     }
# }

# cuts['ww2l2nu_top_smp']  = {
#     'expr' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == -11*13) && topcr && ptll_>15 && PuppiMET_pt > 20',
#     'categories' : {
#         'inc' :'Lepton_pt[0]>20'
#     }
# }

# cuts['ww2l2nu_dytt_smp']  = {
#     'expr' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == -11*13) && bVeto && mll_<85 && ptll_<30',
#     'categories' : {
#         'inc' : 'Lepton_pt[0]>20'
#     }
# }

# cuts['ww2l2nu_sr_smp']  = {
#     'expr' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == -11*13) && mll_>85 && bVeto',
#     'categories' : {
#         'inc' : 'Lepton_pt[0]>20'
#     }
# }
