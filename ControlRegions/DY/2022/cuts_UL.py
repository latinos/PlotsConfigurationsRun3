cuts = {}

# here change the cuts with the ones used in UL studies (link in gDOC)

#UL cuts
preselections = 'Lepton_pt[0]>25 && Lepton_pt[1]>13 && (nLepton>=2 && Alt(Lepton_pt,2,0)<10) && abs(Lepton_eta[0])<2.5 && abs(Lepton_eta[1])<2.5 && mll > 60 && mll < 120'
#called supercut

cuts['Zee_incl']  = '(Lepton_pdgId[0] * Lepton_pdgId[1] == -11*11)'

cuts['Zmm_incl']  = '(Lepton_pdgId[0] * Lepton_pdgId[1] == -13*13)'

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



## here belowe are cuts from the file for Run 3 config
#commenta tutto 
