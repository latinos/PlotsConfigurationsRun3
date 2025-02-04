cuts = {}

# Preselections - applied to all the cuts
preselections = 'mll>12 \
              && Lepton_pt[0]>25 \
              && Lepton_pt[1]>10 \
              && (abs(Lepton_pdgId[1])==13 || Lepton_pt[1]>13) \
              && (nLepton>=2 && Alt(Lepton_pt,2,0)<10) \
              && abs(Lepton_eta[0])<2.5 && abs(Lepton_eta[1])<2.5 \
              && ptll>30 \
              && PuppiMET_pt > 20 \
              '

# Inclusive regions
cuts['Top_ee_incl'] = '(Lepton_pdgId[0] * Lepton_pdgId[1] == -11*11) && mll > 110 && ((zeroJet && !bVeto) || bReq)'
cuts['Top_mm_incl'] = '(Lepton_pdgId[0] * Lepton_pdgId[1] == -13*13) && mll > 110 && ((zeroJet && !bVeto) || bReq)'
cuts['Top_em_incl'] = '(Lepton_pdgId[0] * Lepton_pdgId[1] == -13*11) && mll > 50  && ((zeroJet && !bVeto) || bReq)'

# Jet bins regions
cuts['Top_cr']  = {
    'expr' : 'topcr',
    'categories' : {
        'ee_0j' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == -11*11) && zeroJet && mll > 110',
        'ee_1j' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == -11*11) && oneJet && Alt(CleanJet_pt,1,0)<30 && mll > 110',
        'ee_2j' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == -11*11) && (mjj<65 || mjj>105) && mjj<120 && multiJet && mll > 110',
        'em_0j' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == -11*13) && zeroJet',
        'em_1j' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == -11*13) && oneJet && Alt(CleanJet_pt,1,0)<30',
        'em_2j' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == -11*13) && (mjj<65 || mjj>105) && mjj<120 && multiJet', 
        'mm_0j' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == -13*13) && zeroJet && mll > 110',
        'mm_1j' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == -13*13) && oneJet && Alt(CleanJet_pt,1,0)<30 && mll > 110',
        'mm_2j' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == -13*13) && (mjj<65 || mjj>105) && mjj<120 && multiJet && mll > 110',
    }
}
