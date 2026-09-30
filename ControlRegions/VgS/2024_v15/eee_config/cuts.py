cuts = {}

# Preselections - applied to all the cuts
preselections = 'Alt(Lepton_pt,0,0)>32 \
              && Alt(Lepton_pt,1,0)>10 \
              && Alt(Lepton_pt,2,0)>10 \
              && (nLepton>=3 && Alt(Lepton_pt,3,0)<10) \
              && PuppiMET_pt > 20 \
              && ((mll >= 10 && mll <= 80) || mll > 100) \
              && JpsiVeto \
              && bVeto \
              && noJetInHorn \
'

### WgS CR

# e-ee
cuts['WgS_WtoE_gStoEE'] = {
    'expr': '(abs(Lepton_pdgId[0]) == 11 && abs(Lepton_pdgId[1]) == 11 && abs(Lepton_pdgId[2]) == 11) && (Lepton_pdgId[1] * Lepton_pdgId[2] < 0)',
    'categories': {
        'mth_high': 'mth >= 60',
        'inc' : '1',
    }
}

cuts['WgS_WtoE_gStoSSEE'] = {
    'expr': '(abs(Lepton_pdgId[0]) == 11 && abs(Lepton_pdgId[1]) == 11 && abs(Lepton_pdgId[2]) == 11) && (Lepton_pdgId[1] * Lepton_pdgId[2] > 0)',
    'categories': {
        'mth_high': 'mth >= 60',
        'inc' : '1',
    }
}
