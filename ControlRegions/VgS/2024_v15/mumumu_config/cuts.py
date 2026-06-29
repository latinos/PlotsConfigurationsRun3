cuts = {}

# Preselections - applied to all the cuts
preselections = 'Alt(Lepton_pt,0,0)>25 \
              && Alt(Lepton_pt,1,0)>8 \
              && Alt(Lepton_pt,2,0)>8 \
              && (nLepton>=3 && Alt(Lepton_pt,3,0)<10) \
              && PuppiMET_pt > 20 \
              && mll >= 100 \
              && JpsiVeto \
              && bVeto \
              && noJetInHorn \
'

### WgS CR

# m-mm
cuts['WgS_WtoMu_gStoMuMu'] = {
    'expr': '(abs(Lepton_pdgId[0]) == 13 && abs(Lepton_pdgId[1]) == 13 && abs(Lepton_pdgId[2]) == 13) && (Lepton_pdgId[1] * Lepton_pdgId[2] < 0)',
    'categories': {
        'ml2l3_low': 'mllTwoThree <= 10',
        'inc' : '1',
    }
}