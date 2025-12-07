cuts = {}

preselections = ' mll > 12 \
            && Lepton_pt[0]>25 \
            && Lepton_pt[1]>13 \
            && Alt(Lepton_pt, 2, 0)<10.0  \
            && abs(Lepton_eta[0])<2.5 && abs(Lepton_eta[1])<2.5 \
            && ptll>30 \
            && PuppiMET_pt > 20 \
            && abs(91.1876 - mll) > 15 \
            && noJetInHorn \
            && Lepton_pdgId[0]==-Lepton_pdgId[1] '


# CUTS

#####################
### Signal region ###
#####################

cuts['hww_sr']  = {
   'expr': 'sr && dymva[0] > 0.005',
    # Define the sub-categorization of sr
   'categories' : {
      '0j_ee' : ' zeroJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11) && mth > 90 && abs(dphill) < 2.3',
      '0j_mm' : ' zeroJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13) && mth > 90 && abs(dphill) < 2.3',
      '1j_ee' : ' oneJet && Alt(CleanJet_pt,1,0)<30 && (Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11) && mth > 80 && abs(dphill) < 2.3',
      '1j_mm' : ' oneJet && Alt(CleanJet_pt,1,0)<30 && (Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13) && mth > 80 && abs(dphill) < 2.3',
      '2j_ee' : ' multiJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11) && mth > 65 && mth < 150',
      '2j_mm' : ' multiJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13) && mth > 65 && mth < 150',
   }
}

cuts['wwcr']  = {
   'expr': 'wwcr && dymva[0] > 0.005',
    # Define the sub-categorization of sr
   'categories' : {
      '0j_ee' : ' zeroJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11)',
      '0j_mm' : ' zeroJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13)',
      '1j_ee' : ' oneJet && Alt(CleanJet_pt,1,0)<30 && (Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11)',
      '1j_mm' : ' oneJet && Alt(CleanJet_pt,1,0)<30 && (Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13)',
      '2j_ee' : ' multiJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11)',
      '2j_mm' : ' multiJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13)',
   }
}

cuts['topcr']  = {
   'expr': 'topcr && dymva[0] > 0.005',  
    # Define the sub-categorization of sr
   'categories' : {
      '0j_ee' : ' zeroJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11)',
      '0j_mm' : ' zeroJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13)',
      '1j_ee' : ' oneJet && Alt(CleanJet_pt,1,0)<30 && (Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11)',
      '1j_mm' : ' oneJet && Alt(CleanJet_pt,1,0)<30 && (Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13)',
      '2j_ee' : ' multiJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11)',
      '2j_mm' : ' multiJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13)',
   }
}