cuts = {}

# Preselections - applied to all the cuts
preselections = ' mll > 12 \
              && Lepton_pt[0] > 25 \
              && Lepton_pt[1] > 13 \
              && (nLepton >= 2 && Alt(Lepton_pt,2,0) < 10) \
              && abs(Lepton_eta[0]) < 2.5 \
              && abs(Lepton_eta[1]) < 2.5 \
              && abs(Lepton_eta[0])<2.5 && abs(Lepton_eta[1])<2.5 \
              && ptll>30 \
              && PuppiMET_pt > 20 \
              && noJetInHorn \
'

cuts['WW_cr']  = {
    'expr' : 'wwcr && (Lepton_pdgId[0] * Lepton_pdgId[1] == -13*11)',
    'categories' : {
        '0j' : 'zeroJet',
        '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
        '2j' : 'multiJet',
        'incl' : '1',
    }
}