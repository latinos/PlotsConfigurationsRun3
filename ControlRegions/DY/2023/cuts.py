cuts = {}

# Preselections - applied to all the cuts
preselections = 'Lepton_pt[0] > 25 \
              && Lepton_pt[1] > 13 \
              && (nLepton >= 2 && Alt(Lepton_pt,2,0) < 10) \
              && abs(Lepton_eta[0]) < 2.5 \
              && abs(Lepton_eta[1]) < 2.5 \
              && mll > 60 \
              && mll < 120'

# Individual cuts and categories

cuts['Zee']  = {
   'expr' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == -11*11)',
   'categories' : {
      '0j' : 'zeroJet',
      '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
      '2j' : 'multiJet',
      'incl' : '1',
      'incl_th50' : '((CleanJet_pt[1] > 30 && abs(CleanJet_eta[1]) > 2.5 && abs(CleanJet_eta[1]) < 3.0) ? (CleanJet_pt[1] > 50) : 1) && ((CleanJet_pt[0] > 30 && abs(CleanJet_eta[0]) > 2.5 && abs(CleanJet_eta[0]) < 3.0) ? (CleanJet_pt[0] > 50) : 1)',
      '1j_th50' : 'oneJet && Alt(CleanJet_pt,1,0)<30 && ((abs(CleanJet_eta[0]) > 2.5 && abs(CleanJet_eta[0]) < 3.0) ? (CleanJet_pt[0] > 50) : 1)'
   }
}

cuts['Zmm']  = {
   'expr' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == -13*13)',
   'categories' : {
      '0j' : 'zeroJet',
      '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
      '2j' : 'multiJet',
      'incl' : '1',
      'incl_th50' : '((CleanJet_pt[1] > 30 && abs(CleanJet_eta[1]) > 2.5 && abs(CleanJet_eta[1]) < 3.0) ? (CleanJet_pt[1] > 50) : 1) && ((CleanJet_pt[0] > 30 && abs(CleanJet_eta[0]) > 2.5 && abs(CleanJet_eta[0]) < 3.0) ? (CleanJet_pt[0] > 50) : 1)',
      '1j_th50' : 'oneJet && Alt(CleanJet_pt,1,0)<30 && ((abs(CleanJet_eta[0]) > 2.5 && abs(CleanJet_eta[0]) < 3.0) ? (CleanJet_pt[0] > 50) : 1)'
   }
}

