cuts = {}

preselections = ' mll > 12 \
            && Lepton_pt[0]>25 \
            && Lepton_pt[1]>13 \
            && Alt(Lepton_pt, 2, 0)<10.0  \
            && abs(Lepton_eta[0])<2.5 && abs(Lepton_eta[1])<2.5 \
            && ptll>30 \
            && PuppiMET_pt > 20 \
            && abs(91.1876 - mll) > 15 \
            && noJetInHorn'


# CUTS

#####################
### Signal region ###
#####################

cuts['hww_sr']  = {
   'expr': 'sr',
    # Define the sub-categorization of sr
   'categories' : {
      '0j_ee' : ' zeroJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11) && mll < 60 && mth > 90 && abs(dphill) < 2.3',
      '0j_mm' : ' zeroJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13) && mll < 60 && mth > 90 && abs(dphill) < 2.3',
      '1j_ee' : ' oneJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11) && mll < 60 && mth > 80 && abs(dphill) < 2.3',
      '1j_mm' : ' oneJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13) && mll < 60 && mth > 80 && abs(dphill) < 2.3',
      '2j_ee' : ' multiJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11) && mll < 60 && mth > 66 && mth < 150',
      '2j_mm' : ' multiJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13) && mll < 60 && mth > 66 && mth < 150',
   }
}

cuts['wwcr']  = {
   'expr': 'wwcr',
    # Define the sub-categorization of sr
   'categories' : {
      '0j_ee' : ' zeroJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11) && abs(dphill) < 2.3',
      '0j_mm' : ' zeroJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13) && abs(dphill) < 2.3',
      '1j_ee' : ' oneJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11) && abs(dphill) < 2.3',
      '1j_mm' : ' oneJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13) && abs(dphill) < 2.3',
      '2j_ee' : ' multiJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11)',
      '2j_mm' : ' multiJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13)',
   }
}

cuts['topcr']  = {
   'expr': 'topcr',  
    # Define the sub-categorization of sr
   'categories' : {
      '0j_ee' : ' zeroJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11)',
      '0j_mm' : ' zeroJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13)',
      '1j_ee' : ' oneJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11)',
      '1j_mm' : ' oneJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13)',
      '2j_ee' : ' multiJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11)',
      '2j_mm' : ' multiJet && (Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13)',
   }
}

#cuts['dyttcr']  = {
#   'expr': 'dycr',
#    # Define the sub-categorization of sr
#   'categories' : {
#      '0j' : 'zeroJet',
#      '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
#      '2j' : '(mjj<65 || mjj>105) && mjj<120 && multiJet',
#   }
#}
