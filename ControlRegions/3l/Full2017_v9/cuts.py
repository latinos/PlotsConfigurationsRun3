# cuts

cuts = {}

# MinIf$( WH3l_mOSll[], WH3l_mOSll[Iteration$] > 0) > 12
# Alt(WH3l_mOSll,0,9999) > 12 && Alt(WH3l_mOSll,1,9999) > 12 && Alt(WH3l_mOSll,2,9999) > 12 \

preselections = '(nLepton>=3 && Alt(Lepton_pt,3,0)<10) \
             && Alt(Lepton_pt,0,0)>25 \
             && Alt(Lepton_pt,1,0)>10 \
             && (abs(Lepton_pdgId[1])==13 || Lepton_pt[1]>13) \
             && Alt(Lepton_pt,2,0)>10 \
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
        'plus_pt2ge20'  : 'Lepton_pdgId[0]*Lepton_pdgId[1]*Lepton_pdgId[2]>0 && Lepton_pt[1]>=20 && Lepton_pt[2]>=15',
        'minus_pt2ge20' : 'Lepton_pdgId[0]*Lepton_pdgId[1]*Lepton_pdgId[2]<0 && Lepton_pt[1]>=20 && Lepton_pt[2]>=15',
        # 'plus_pt2lt20'  : 'Lepton_pdgId[0]*Lepton_pdgId[1]*Lepton_pdgId[2]>0 && Lepton_pt[1]<20',
        # 'minus_pt2lt20' : 'Lepton_pdgId[0]*Lepton_pdgId[1]*Lepton_pdgId[2]<0 && Lepton_pt[1]<20',
    }
}

# OSSF
cuts['wh3l_13TeV_ossf'] = {
    'expr' : 'WH3l_flagOSSF == 1 && WH3l_ZVeto > 20 && PuppiMET_pt > 40 && Alt(CleanJet_pt, 0, 0) < 30',
    'categories' : {
        'plus_pt2ge20'  : 'Lepton_pdgId[0]*Lepton_pdgId[1]*Lepton_pdgId[2]>0 && Lepton_pt[1]>=20 && Lepton_pt[2]>=15',
        'minus_pt2ge20' : 'Lepton_pdgId[0]*Lepton_pdgId[1]*Lepton_pdgId[2]<0 && Lepton_pt[1]>=20 && Lepton_pt[2]>=15',
        # 'plus_pt2lt20'  : 'Lepton_pdgId[0]*Lepton_pdgId[1]*Lepton_pdgId[2]>0 && Lepton_pt[1]<20',
        # 'minus_pt2lt20' : 'Lepton_pdgId[0]*Lepton_pdgId[1]*Lepton_pdgId[2]<0 && Lepton_pt[1]<20',
    }
}

# 11 = e
# 13 = mu
# 15 = tau
