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

# Jet bins regions
cuts['Top_cr_em']  = {
    'expr' : 'topcr && (Lepton_pdgId[0] * Lepton_pdgId[1] == -13*11)',
    'categories' : {
        '0j' : 'zeroJet',
        '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
        '2j' : 'multiJet',
        'incl' : '1',
    }
}

cuts['Top_cr_ee']  = {
    'expr' : 'topcr && (Lepton_pdgId[0] * Lepton_pdgId[1] == -11*11)',
    'categories' : {
        '0j' : 'zeroJet',
        '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
        '2j' : 'multiJet',
        'incl' : '1',
    }
}

cuts['Top_cr_mm']  = {
    'expr' : 'topcr && (Lepton_pdgId[0] * Lepton_pdgId[1] == -13*13)',
    'categories' : {
        '0j' : 'zeroJet',
        '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
        '2j' : 'multiJet',
        'incl' : '1',
    }
}
