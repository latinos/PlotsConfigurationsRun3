cuts = {}

# Preselections - applied to all the cuts
preselections = 'Alt(Lepton_pt,0,0)>25 \
              && Alt(Lepton_pt,1,0)>10 \
              && (abs(Lepton_pdgId[1])==13 || Lepton_pt[1]>13) \
              && Alt(Lepton_pt,2,0)>10 \
              && (nLepton>=3 && Alt(Lepton_pt,3,0)<10) \
              && (WH3l_mOSll[0] < 0 || WH3l_mOSll[0] > 12) \
              && (WH3l_mOSll[1] < 0 || WH3l_mOSll[1] > 12) \
              && (WH3l_mOSll[2] < 0 || WH3l_mOSll[2] > 12) \
              && abs(WH3l_chlll) == 1 \
              && bVeto \
              && noJetInHorn \
'

# Jet bins
cuts['3l_ossf'] = {
    'expr' : 'WH3l_flagOSSF == 1 && PuppiMET_pt > 45 && WH3l_ZVeto < 20 && WH3l_mlll > 100',
    'categories' : {
        '0j' : 'zeroJet',
        '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
        '2j' : 'multiJet',
        'inc' : '1',
    }
}