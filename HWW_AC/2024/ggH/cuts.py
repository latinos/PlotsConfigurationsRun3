cuts = {}

preselections = 'mll>12  \
            && Lepton_pt[0]>25 \
            && Lepton_pt[1]>10 \
            && (abs(Lepton_pdgId[1])==13 || Lepton_pt[1]>13) \
            && abs(Lepton_eta[0])<2.5 && abs(Lepton_eta[1])<2.5 \
            && ptll>30 \
            && PuppiMET_pt > 20 \
            && (Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13) \
            && noJetInHorn'

# CUTS

#####################
### Signal region ###
#####################

cuts['hww_sr']  = {
   'expr': 'sr',
    # Define the sub-categorization of sr
   'categories' : {
      '01j' : '(zeroJet)||(oneJet && Alt(CleanJet_pt,1,0)<30)',
   }
}


cuts['wwcr']  = {
   'expr': 'wwcr',
    # Define the sub-categorization of sr
   'categories' : {
      '01j' : '(zeroJet)||(oneJet && Alt(CleanJet_pt,1,0)<30)', 
   }
}

cuts['topcr']  = {
   'expr': 'topcr',
    # Define the sub-categorization of sr
   'categories' : {
      '01j' : '(zeroJet)||(oneJet && Alt(CleanJet_pt,1,0)<30)',
   }
}

cuts['dyttcr']  = {
   'expr': 'dycr',
    # Define the sub-categorization of sr
   'categories' : {
      '01j' : '(zeroJet)||(oneJet && Alt(CleanJet_pt,1,0)<30)', 
   }
}

