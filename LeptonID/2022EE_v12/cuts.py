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

# Muon ID: mvaMuID WP tight HWW
# Ele  ID: wp90iso
cuts['sr_ele_wp90iso__mu_mvaMuID_WP_tight'] = {
    'expr' : 'LepCut2l__ele_wp90iso__mu_mvaMuID_WP_tight > 0.5',
    'categories' : {
        'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
        'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
        'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
        'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
        'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
        'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
    }
}

# Muon ID: mvaMuID WP medium HWW
# Ele  ID: wp90iso
cuts['sr_ele_wp90iso__mu_mvaMuID_WP_medium'] = {
    'expr' : 'LepCut2l__ele_wp90iso__mu_mvaMuID_WP_medium > 0.5',
    'categories' : {
        'ee_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] >= 20',
        'ee_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11 && Lepton_pt[1] <  20',
        'em_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] >= 20',
        'em_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Lepton_pt[1] <  20',
        'mm_high_pt' : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] >= 20',
        'mm_low_pt'  : 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13 && Lepton_pt[1] <  20',
    }
}


