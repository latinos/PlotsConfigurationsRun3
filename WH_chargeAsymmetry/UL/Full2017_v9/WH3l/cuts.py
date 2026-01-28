# cuts

cuts = {}

# MinIf$( WH3l_mOSll[], WH3l_mOSll[Iteration$] > 0) > 12
# Alt(WH3l_mOSll,0,9999) > 12 && Alt(WH3l_mOSll,1,9999) > 12 && Alt(WH3l_mOSll,2,9999) > 12 \

preselections = '(nLepton>=3 && Alt(Lepton_pt,3,0)<10) \
             && Alt(Lepton_pt,0,0)>25 \
             && Alt(Lepton_pt,1,0)>10 \
             && (abs(Lepton_pdgId[1])==13 || Lepton_pt[1]>13) \
             && (WH3l_mOSll[0] < 0 || WH3l_mOSll[0] > 12) \
             && (WH3l_mOSll[1] < 0 || WH3l_mOSll[1] > 12) \
             && (WH3l_mOSll[2] < 0 || WH3l_mOSll[2] > 12) \
             && abs(WH3l_chlll) == 1 \
             && bVeto \
'

## Signal region

# SSSF
cuts['wh3l_13TeV_sssf'] = {
    'expr' : 'WH3l_flagOSSF == 0 && Alt(CleanJet_pt, 0, 0) < 30',
    'categories' : {
        'plus_pt2ge20'  : 'Lepton_pdgId[0]*Lepton_pdgId[1]*Lepton_pdgId[2]>0 && Alt(Lepton_pt,1,0)>20 && Alt(Lepton_pt,2,0)>15',
        'minus_pt2ge20' : 'Lepton_pdgId[0]*Lepton_pdgId[1]*Lepton_pdgId[2]<0 && Alt(Lepton_pt,1,0)>20 && Alt(Lepton_pt,2,0)>15',
    }
}

# OSSF
cuts['wh3l_13TeV_ossf'] = {
    'expr' : 'WH3l_flagOSSF == 1 && WH3l_ZVeto > 20 && PuppiMET_pt > 40 && Alt(CleanJet_pt,0,0) < 30',
    'categories' : {
        'plus_pt2ge20'  : 'Lepton_pdgId[0]*Lepton_pdgId[1]*Lepton_pdgId[2]>0 && Alt(Lepton_pt,1,0)>20 && Alt(Lepton_pt,2,0)>15',
        'minus_pt2ge20' : 'Lepton_pdgId[0]*Lepton_pdgId[1]*Lepton_pdgId[2]<0 && Alt(Lepton_pt,1,0)>20 && Alt(Lepton_pt,2,0)>15',
    }
}

## WZ control region

# CR 0jet - WH3l
cuts['wh3l_wz_13TeV'] = 'WH3l_flagOSSF == 1 \
                         && PuppiMET_pt > 45 \
                         && WH3l_ZVeto < 20 \
                         && WH3l_mlll > 100 \
                         && Alt(CleanJet_pt,0,0) < 30 \
                         && Alt(Lepton_pt,1,0)>20 \
                         && Alt(Lepton_pt,2,0)>15 \
                         '

# CR 1jet - WHSS
cuts['hww2l2v_13TeV_WH_SS_WZ_1j'] = '((Lepton_pdgId[0]*Lepton_pdgId[1] == 13*13) || (Lepton_pdgId[0]*Lepton_pdgId[1] == 11*13) || (Lepton_pdgId[0]*Lepton_pdgId[1] == 11*11))\
                                    && Alt(Lepton_pt,1,0)>20 \
                                    && Alt(Lepton_pt,2,0)>15 \
                                    && Alt(CleanJet_pt, 0, 0)>30 \
                                    && Alt(CleanJet_pt, 1, 0)<30 \
                                    && WH3l_mlll > 100 \
                                    '

# CR 2jets - WHSS
cuts['hww2l2v_13TeV_WH_SS_WZ_2j'] = '((Lepton_pdgId[0]*Lepton_pdgId[1] == 13*13) || (Lepton_pdgId[0]*Lepton_pdgId[1] == 11*13) || (Lepton_pdgId[0]*Lepton_pdgId[1] == 11*11)) \
                                    && Alt(Lepton_pt,1,0)>20 \
                                    && Alt(Lepton_pt,2,0)>15 \
                                    && Alt(CleanJet_pt, 0, 0)>30 \
                                    && Alt(CleanJet_pt, 1, 0)>30 \
                                    && WH3l_mlll > 100 \
                                    '

# CR split into charge categories
cuts['hww2l2v_13TeV_WH_SS_WZ'] = {
    'expr' : '((Lepton_pdgId[0]*Lepton_pdgId[1] == 13*13) || (Lepton_pdgId[0]*Lepton_pdgId[1] == 11*13) || (Lepton_pdgId[0]*Lepton_pdgId[1] == 11*11)) && Alt(Lepton_pt,1,0)>20 && Alt(Lepton_pt,2,0)>15 && Alt(CleanJet_pt, 0, 0)>30 && WH3l_mlll > 100',
    'categories' : {
        '1j_plus'  : 'Alt(CleanJet_pt, 1, 0) <  30 && Lepton_pdgId[0] < 0 && Lepton_pdgId[1] < 0',
        '1j_minus' : 'Alt(CleanJet_pt, 1, 0) <  30 && Lepton_pdgId[0] > 0 && Lepton_pdgId[1] > 0',
        '2j_plus'  : 'Alt(CleanJet_pt, 1, 0) >= 30 && Lepton_pdgId[0] < 0 && Lepton_pdgId[1] < 0',
        '2j_minus' : 'Alt(CleanJet_pt, 1, 0) >= 30 && Lepton_pdgId[0] > 0 && Lepton_pdgId[1] > 0',
    }
}

# 11 = e
# 13 = mu
# 15 = tau
