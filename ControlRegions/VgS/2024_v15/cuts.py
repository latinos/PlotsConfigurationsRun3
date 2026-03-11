cuts = {}

# Preselections - applied to all the cuts
preselections = 'Alt(Lepton_pt,0,0)>25 \
              && Alt(Lepton_pt,1,0)>10 \
              && Alt(Lepton_pt,2,0)>10 \
              && (nLepton>=3 && Alt(Lepton_pt,3,0)<10) \
              && abs(WH3l_chlll) == 1 \
              && PuppiMET_pt > 45 \
              && bVeto \
              && noJetInHorn \
'

### WgS CR

# m-ee
cuts['WgS_WtoMu_gStoEE'] = {
    'expr': '(abs(Lepton_pdgId[0]) == 13 && abs(Lepton_pdgId[1]) == 11 && abs(Lepton_pdgId[2]) == 11) && (Lepton_pdgId[1] * Lepton_pdgId[2] < 0)',
    'categories': {
        '0j'  : 'zeroJet',
        '1j'  : 'oneJet && Alt(CleanJet_pt,1,0)<30',
        '2j'  : 'multiJet',
        'inc' : '1',
    }
}

# e-mm
cuts['WgS_WtoE_gStoMuMu'] = {
    'expr': '(abs(Lepton_pdgId[0]) == 11 && abs(Lepton_pdgId[1]) == 13 && abs(Lepton_pdgId[2]) == 13) && (Lepton_pdgId[1] * Lepton_pdgId[2] < 0) && (Alt(Lepton_pt,0,0)>32)',
    'categories': {
        '0j'  : 'zeroJet',
        '1j'  : 'oneJet && Alt(CleanJet_pt,1,0)<30',
        '2j'  : 'multiJet',
        'inc' : '1',
    }
}

# e-ee
cuts['WgS_WtoE_gStoEE'] = {
    'expr': '(abs(Lepton_pdgId[0]) == 11 && abs(Lepton_pdgId[1]) == 11 && abs(Lepton_pdgId[2]) == 11) && (Lepton_pdgId[1] * Lepton_pdgId[2] < 0) && (Alt(Lepton_pt,0,0)>32)',
    'categories': {
        '0j'  : 'zeroJet',
        '1j'  : 'oneJet && Alt(CleanJet_pt,1,0)<30',
        '2j'  : 'multiJet',
        'inc' : '1',
    }
}

# m-mm
cuts['WgS_WtoMu_gStoMuMu'] = {
    'expr': '(abs(Lepton_pdgId[0]) == 13 && abs(Lepton_pdgId[1]) == 13 && abs(Lepton_pdgId[2]) == 13) && (Lepton_pdgId[1] * Lepton_pdgId[2] < 0)',
    'categories': {
        '0j'  : 'zeroJet',
        '1j'  : 'oneJet && Alt(CleanJet_pt,1,0)<30',
        '2j'  : 'multiJet',
        'inc' : '1',
    }
}

### Invariant mass variables
# m(lep1,lep2) : mll
# m(lep2,lep3) : mllTwoThree
# m(lep1,lep3) : mllOneThree
# mllWgSt : ???
