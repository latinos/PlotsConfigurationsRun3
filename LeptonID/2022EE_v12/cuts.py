'''
Reference: Legacy analysis:
https://github.com/latinos/PlotsConfigurations/blob/master/Configurations/ggH/Full2018_v7/cuts.py
'''

cuts = {}

preselections = 'mll > 12 \
            && Lepton_pt[0]>25 \
            && Lepton_pt[1]>13 \
            && (nLepton>=2 && Alt(Lepton_pt,2,0)<10) \
            && abs(Lepton_eta[0])<2.5 && abs(Lepton_eta[1])<2.5 \
            && ptll>30 \
            && PuppiMET_pt > 20 \
            && (Lepton_pdgId[0]*Lepton_pdgId[1] < 0) \
            && mth>60 \
            && mtw2>30 \
            && bVeto \
'

#########################################################
# Preselections - only needed to calculate efficiencies #
#########################################################

cuts['macthed_selections'] = {
    'expr' : 'mll > 12 && Alt(Lepton_promptgenmatched,0,0) == 1 && Alt(Lepton_promptgenmatched,1,0) == 1',
    'categories' : {
        'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
        'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
        'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
        'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
        'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
        'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
    }
}

cuts['unmacthed_selections'] = {
    'expr' : 'mll > 12 && Alt(Lepton_promptgenmatched,0,0) == 1 && Alt(Lepton_promptgenmatched,1,0) == 0',
    'categories' : {
        'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
        'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
        'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
        'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
        'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
        'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
    }
}

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


# eleID : muonID
all_cuts_list = [
    # Dumb selections
    ['wp90iso', 'cut_TightID_POG'],
    ['wp90iso', 'cut_MediumID_POG'],
    ['wp90iso', 'mvaMuID_WP_medium'],
    ['wp90iso', 'mvaMuID_WP_tight'],
    # Basic selections with p.f. Iso
    ['mvaWinter22V2Iso_WP90', 'cut_Tight_HWW'],
    ['mvaWinter22V2Iso_WP90', 'cut_Medium_HWW'],
    ['mvaWinter22V2Iso_WP90', 'mvaMuID_WP_medium_HWW'],
    ['mvaWinter22V2Iso_WP90', 'mvaMuID_WP_tight_HWW'], 
    # Basic selections with mini Iso
    ['mvaWinter22V2Iso_WP90', 'cut_TightMiniIso_HWW'],
    ['mvaWinter22V2Iso_WP90', 'cut_MediumMiniIso_HWW'],
    ['mvaWinter22V2Iso_WP90', 'mvaMuID_WP_mediumMiniIso_HWW'],
    ['mvaWinter22V2Iso_WP90', 'mvaMuID_WP_tightMiniIso_HWW'],
    # Basic selections with mini Iso for muons
    ['mvaWinter22V2Iso_WP90', 'cut_TightMiniIso_HWW'],
    ['mvaWinter22V2Iso_WP90', 'cut_MediumMiniIso_HWW'],
    ['mvaWinter22V2Iso_WP90', 'mvaMuID_WP_mediumMiniIso_HWW'],
    ['mvaWinter22V2Iso_WP90', 'mvaMuID_WP_tightMiniIso_HWW'],
    # Basic selections with mini Iso for muons and noLostHits for electrons --> could we add this to the previous step?
    ['mvaWinter22V2Iso_WP90_noLostHits', 'cut_TightMiniIso_HWW'],
    ['mvaWinter22V2Iso_WP90_noLostHits', 'cut_MediumMiniIso_HWW'],
    ['mvaWinter22V2Iso_WP90_noLostHits', 'mvaMuID_WP_mediumMiniIso_HWW'],
    ['mvaWinter22V2Iso_WP90_noLostHits', 'mvaMuID_WP_tightMiniIso_HWW'],
    # TTHMVA selection on top of p.f. Iso
    ['mvaWinter22V2Iso_WP90_ttHMVA_90', 'cut_Tight_HWW_ttHMVA_67'],
    ['mvaWinter22V2Iso_WP90_ttHMVA_90', 'cut_Medium_HWW_ttHMVA_67'],
    ['mvaWinter22V2Iso_WP90_ttHMVA_90', 'mvaMuID_WP_medium_HWW_ttHMVA_67'],
    ['mvaWinter22V2Iso_WP90_ttHMVA_90', 'mvaMuID_WP_tight_HWW_ttHMVA_67'],
    # TTHMVA selection on top of mini Iso
    ['mvaWinter22V2Iso_WP90_ttHMVA_90', 'cut_TightMiniIso_HWW_ttHMVA_67'],
    ['mvaWinter22V2Iso_WP90_ttHMVA_90', 'cut_MediumMiniIso_HWW_ttHMVA_67'],
    ['mvaWinter22V2Iso_WP90_ttHMVA_90', 'mvaMuID_WP_mediumMiniIso_HWW_ttHMVA_67'],
    ['mvaWinter22V2Iso_WP90_ttHMVA_90', 'mvaMuID_WP_tightMiniIso_HWW_ttHMVA_67'],
    # TTHMVA selection on top of loose p.f. iso
    ['mvaWinter22V2Iso_WP90_looseIso_ttHMVA_90', 'cut_Tight_looseIso_ttHMVA_67'],
    ['mvaWinter22V2Iso_WP90_looseIso_ttHMVA_90', 'cut_Medium_looseIso_ttHMVA_67'],
    ['mvaWinter22V2Iso_WP90_looseIso_ttHMVA_90', 'mvaMuID_WP_medium_looseIso_ttHMVA_67'],
    ['mvaWinter22V2Iso_WP90_looseIso_ttHMVA_90', 'mvaMuID_WP_tight_looseIso_ttHMVA_67'],
    # TTHMVA selection on top of mini Iso for muons and noLostHits for electrons --> could we add this to the 'TTHMVA selection on top of mini Iso' step?
    ['mvaWinter22V2Iso_WP90_noLostHits_ttHMVA_90', 'cut_TightMiniIso_HWW_ttHMVA_67'],
    ['mvaWinter22V2Iso_WP90_noLostHits_ttHMVA_90', 'cut_MediumMiniIso_HWW_ttHMVA_67'],
    ['mvaWinter22V2Iso_WP90_noLostHits_ttHMVA_90', 'mvaMuID_WP_mediumMiniIso_HWW_ttHMVA_67'],
    ['mvaWinter22V2Iso_WP90_noLostHits_ttHMVA_90', 'mvaMuID_WP_tightMiniIso_HWW_ttHMVA_67'],
]


# Loop over all ID definitions
# for eleWP, muWP in all_cuts_dict.items():
for wps in all_cuts_list:
    eleWP = wps[0]
    muWP  = wps[1]
    print(f"Current cut = {eleWP},{muWP}")
    cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
        'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
        'categories' : {
            'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
            'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
            'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
            'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
            'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
            'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
        }
    }



# ###################
# # Dumb Selections #
# ###################

# # Muon ID: Tight ID POG
# # Ele  ID: wp90iso
# eleWP = 'wp90iso'
# muWP  = 'cut_TightID_POG'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }

# # Muon ID: Medium ID POG
# # Ele  ID: wp90iso
# eleWP = 'wp90iso'
# muWP  = 'cut_MediumID_POG'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }

# # Muon ID: mvaMuID WP medium
# # Ele  ID: wp90iso
# eleWP = 'wp90iso'
# muWP  = 'mvaMuID_WP_medium'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }

# # Muon ID: mvaMuID WP tight
# # Ele  ID: wp90iso
# eleWP = 'wp90iso'
# muWP  = 'mvaMuID_WP_tight'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }


# ###############################
# # Basic Selections - P.F. Iso #
# ###############################

# # Muon ID: Tight ID POG HWW
# # Ele  ID: mvaWinter22V2Iso_WP90
# eleWP = 'mvaWinter22V2Iso_WP90'
# muWP  = 'cut_Tight_HWW'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }

# # LepWPCut__ele_mvaWinter22V2Iso_WP90__mu_cut_Medium_HWW
# # Muon ID: Medium ID POG HWW
# # Ele  ID: mvaWinter22V2Iso_WP90
# eleWP = 'mvaWinter22V2Iso_WP90'
# muWP  = 'cut_Medium_HWW'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }

# # Muon ID: mvaMuID WP medium HWW
# # Ele  ID: mvaWinter22V2Iso_WP90
# eleWP = 'mvaWinter22V2Iso_WP90'
# muWP  = 'mvaMuID_WP_medium_HWW'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }

# # Muon ID: mvaMuID WP tight HWW
# # Ele  ID: mvaWinter22V2Iso_WP90
# eleWP = 'mvaWinter22V2Iso_WP90'
# muWP  = 'mvaMuID_WP_tight_HWW'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }


# ###############################
# # Basic Selections - Mini Iso #
# ###############################

# # Muon ID: Tight ID MiniIso HWW
# # Ele  ID: mvaWinter22V2Iso_WP90
# eleWP = 'mvaWinter22V2Iso_WP90'
# muWP  = 'cut_TightMiniIso_HWW'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }

# # Muon ID: Medium ID MiniIso HWW
# # Ele  ID: mvaWinter22V2Iso_WP90
# eleWP = 'mvaWinter22V2Iso_WP90'
# muWP  = 'cut_MediumMiniIso_HWW'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }

# # Muon ID: mvaMuID WP medium MiniIso HWW
# # Ele  ID: mvaWinter22V2Iso_WP90
# eleWP = 'mvaWinter22V2Iso_WP90'
# muWP  = 'mvaMuID_WP_mediumMiniIso_HWW'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }

# # Muon ID: mvaMuID WP tight MiniIso HWW
# # Ele  ID: mvaWinter22V2Iso_WP90
# eleWP = 'mvaWinter22V2Iso_WP90'
# muWP  = 'mvaMuID_WP_tightMiniIso_HWW'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }

# ############################################
# # Add no lost hits selection for electrons #
# ############################################

# # Muon ID: Tight ID MiniIso HWW
# # Ele  ID: mvaWinter22V2Iso_WP90 + Electron_lostHits == 0
# eleWP = 'mvaWinter22V2Iso_WP90_noLostHits'
# muWP  = 'cut_TightMiniIso_HWW'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }

# # Muon ID: Medium ID MiniIso HWW
# # Ele  ID: mvaWinter22V2Iso_WP90 + Electron_lostHits == 0
# eleWP = 'mvaWinter22V2Iso_WP90_noLostHits'
# muWP  = 'cut_MediumMiniIso_HWW'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }

# # Muon ID: mvaMuID WP medium MiniIso HWW
# # Ele  ID: mvaWinter22V2Iso_WP90 + Electron_lostHits == 0
# eleWP = 'mvaWinter22V2Iso_WP90_noLostHits'
# muWP  = 'mvaMuID_WP_mediumMiniIso_HWW'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }

# # Muon ID: mvaMuID WP tight MiniIso HWW
# # Ele  ID: mvaWinter22V2Iso_WP90 + Electron_lostHits == 0
# eleWP = 'mvaWinter22V2Iso_WP90_noLostHits'
# muWP  = 'mvaMuID_WP_tightMiniIso_HWW'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }


# ######################################################
# # Applying TTHMVA selection on top of P.F. Isolation #
# ######################################################

# # Muon ID: Tight ID HWW + ttHMVA_67
# # Ele  ID: mvaWinter22V2Iso_WP90 + ttHMVA_90
# eleWP = 'mvaWinter22V2Iso_WP90_ttHMVA_90'
# muWP  = 'cut_Tight_HWW_ttHMVA_67'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }

# # Muon ID: Medium ID HWW + ttHMVA_67
# # Ele  ID: mvaWinter22V2Iso_WP90 + ttHMVA_90
# eleWP = 'mvaWinter22V2Iso_WP90_ttHMVA_90'
# muWP  = 'cut_Medium_HWW_ttHMVA_67'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }

# # Muon ID: mvaMuID WP medium + ttHMVA_67
# # Ele  ID: mvaWinter22V2Iso_WP90 + ttHMVA_90
# eleWP = 'mvaWinter22V2Iso_WP90_ttHMVA_90'
# muWP  = 'mvaMuID_WP_medium_HWW_ttHMVA_67'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }

# # Muon ID: mvaMuID WP tight + ttHMVA_67
# # Ele  ID: mvaWinter22V2Iso_WP90 + ttHMVA_90
# eleWP = 'mvaWinter22V2Iso_WP90_ttHMVA_90'
# muWP  = 'mvaMuID_WP_tight_HWW_ttHMVA_67'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }


# ######################################################
# # Applying TTHMVA selection on top of Mini Isolation #
# ######################################################

# # Muon ID: Tight ID Mini Isolation HWW + ttHMVA_67
# # Ele  ID: mvaWinter22V2Iso_WP90 + ttHMVA_90
# eleWP = 'mvaWinter22V2Iso_WP90_ttHMVA_90'
# muWP  = 'cut_TightMiniIso_HWW_ttHMVA_67'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }

# # Muon ID: Medium ID Mini Isolation HWW + ttHMVA_67
# # Ele  ID: mvaWinter22V2Iso_WP90 + ttHMVA_90
# eleWP = 'mvaWinter22V2Iso_WP90_ttHMVA_90'
# muWP  = 'cut_MediumMiniIso_HWW_ttHMVA_67'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }

# # Muon ID: mvaMuID WP medium Mini Isolation + ttHMVA_67
# # Ele  ID: mvaWinter22V2Iso_WP90 + ttHMVA_90
# eleWP = 'mvaWinter22V2Iso_WP90_ttHMVA_90'
# muWP  = 'mvaMuID_WP_mediumMiniIso_HWW_ttHMVA_67'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }

# # Muon ID: mvaMuID WP tight Mini Isolation + ttHMVA_67
# # Ele  ID: mvaWinter22V2Iso_WP90 + ttHMVA_90
# eleWP = 'mvaWinter22V2Iso_WP90_ttHMVA_90'
# muWP  = 'mvaMuID_WP_tightMiniIso_HWW_ttHMVA_67'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }

# ############################################################
# # Applying TTHMVA selection on top of Loose P.F. Isolation #
# ############################################################

# # Muon ID: Tight ID Loose Isolation + ttHMVA_67
# # Ele  ID: mvaWinter22V2Iso_WP90 + ttHMVA_90
# eleWP = 'mvaWinter22V2Iso_WP90_looseIso_ttHMVA_90'
# muWP  = 'cut_Tight_looseIso_ttHMVA_67'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }

# # Muon ID: Medium ID Loose Isolation + ttHMVA_67
# # Ele  ID: mvaWinter22V2Iso_WP90 + ttHMVA_90
# eleWP = 'mvaWinter22V2Iso_WP90_looseIso_ttHMVA_90'
# muWP  = 'cut_Medium_looseIso_ttHMVA_67'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }

# # Muon ID: mvaMuID WP medium Loose Isolation + ttHMVA_67
# # Ele  ID: mvaWinter22V2Iso_WP90 + ttHMVA_90
# eleWP = 'mvaWinter22V2Iso_WP90_looseIso_ttHMVA_90'
# muWP  = 'mvaMuID_WP_medium_looseIso_ttHMVA_67'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }

# # Muon ID: mvaMuID WP tight Loose Isolation + ttHMVA_67
# # Ele  ID: mvaWinter22V2Iso_WP90 + ttHMVA_90
# eleWP = 'mvaWinter22V2Iso_WP90_looseIso_ttHMVA_90'
# muWP  = 'mvaMuID_WP_tight_looseIso_ttHMVA_67'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }

# #####################################################################
# # Applying TTHMVA selection and noLostHits on top of Mini Isolation #
# #####################################################################

# # Muon ID: Tight ID Mini Isolation HWW + ttHMVA_67
# # Ele  ID: mvaWinter22V2Iso_WP90 + noLostHits + ttHMVA_90
# eleWP = 'mvaWinter22V2Iso_WP90_noLostHits_ttHMVA_90'
# muWP  = 'cut_TightMiniIso_HWW_ttHMVA_67'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }

# # Muon ID: Medium ID Mini Isolation HWW + ttHMVA_67
# # Ele  ID: mvaWinter22V2Iso_WP90 + noLostHits + ttHMVA_90
# eleWP = 'mvaWinter22V2Iso_WP90_noLostHits_ttHMVA_90'
# muWP  = 'cut_MediumMiniIso_HWW_ttHMVA_67'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }

# # Muon ID: mvaMuID WP medium Mini Isolation + ttHMVA_67
# # Ele  ID: mvaWinter22V2Iso_WP90 + noLostHits + ttHMVA_90
# eleWP = 'mvaWinter22V2Iso_WP90_noLostHits_ttHMVA_90'
# muWP  = 'mvaMuID_WP_mediumMiniIso_HWW_ttHMVA_67'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }

# # Muon ID: mvaMuID WP tight Mini Isolation + ttHMVA_67
# # Ele  ID: mvaWinter22V2Iso_WP90 + noLostHits + ttHMVA_90
# eleWP = 'mvaWinter22V2Iso_WP90_noLostHits_ttHMVA_90'
# muWP  = 'mvaMuID_WP_tightMiniIso_HWW_ttHMVA_67'

# cuts['sr_ele_' + eleWP + '__mu_' + muWP] = {
#     'expr' : 'LepWPCut__ele_' + eleWP + '__mu_' + muWP + ' > 0.5',
#     'categories' : {
#         'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
#         'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
#         'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
#         'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
#         'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
#         'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
#     }
# }
