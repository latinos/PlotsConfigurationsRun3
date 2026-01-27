cuts = {}

# Preselections - applied to all the cuts, noJetInHorn replaced by zeroJet
preselections = 'Lepton_pt[0] > 25 \
              && Lepton_pt[1] > 13 \
              && (nLepton >= 2 && Alt(Lepton_pt,2,0) < 10) \
              && abs(Lepton_eta[0]) < 2.5 \
              && abs(Lepton_eta[1]) < 2.5 \
              && mll > 60 \
              && mll < 120 \
              && zeroJet \
'

# Individual cuts and categories

# Commenting out the inclusive cuts (DS, 19Nov25)
# cuts['Zee_incl']  = '(Lepton_pdgId[0] * Lepton_pdgId[1] == -11*11)'
# cuts['Zmm_incl']  = '(Lepton_pdgId[0] * Lepton_pdgId[1] == -13*13)'

cuts['Zee']  = {
   'expr' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == -11*11)',
   'categories' : {
      '0j' : 'zeroJet',
      '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
      '2j' : 'multiJet',
   }
}

cuts['Zmm']  = {
   'expr' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == -13*13)',
   'categories' : {
      '0j' : 'zeroJet',
      '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
      '2j' : 'multiJet',
   }
}

# cuts['Zee_noJetInHorn_incl']  = '(Lepton_pdgId[0] * Lepton_pdgId[1] == -11*11) && Sum(CleanJet_pt > 30 && CleanJet_pt < 50 && abs(CleanJet_eta) > 2.6 && abs(CleanJet_eta) < 3.1) == 0'

# cuts['Zmm_noJetInHorn_incl']  = '(Lepton_pdgId[0] * Lepton_pdgId[1] == -13*13) && Sum(CleanJet_pt > 30 && CleanJet_pt < 50 && abs(CleanJet_eta) > 2.6 && abs(CleanJet_eta) < 3.1) == 0'

# cuts['Zee_noJetInHorn']  = {
#    'expr' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == -11*11) && Sum(CleanJet_pt > 30 && CleanJet_pt < 50 && abs(CleanJet_eta) > 2.6 && abs(CleanJet_eta) < 3.1) == 0',
#    'categories' : {
#       '0j' : 'zeroJet',
#       '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
#       '2j' : 'multiJet',
#    }
# }

# cuts['Zmm_noJetInHorn']  = {
#    'expr' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == -13*13) && Sum(CleanJet_pt > 30 && CleanJet_pt < 50 && abs(CleanJet_eta) > 2.6 && abs(CleanJet_eta) < 3.1) == 0',
#    'categories' : {
#       '0j' : 'zeroJet',
#       '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
#       '2j' : 'multiJet',
#    }
# }
