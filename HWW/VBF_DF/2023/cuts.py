cuts = {}

preselections = ' mll > 12 \
            && Lepton_pt[0]>25 \
            && Lepton_pt[1]>13 \
            && Alt(Lepton_pt, 2, 0)<10.0  \
            && abs(Lepton_eta[0])<2.5 && abs(Lepton_eta[1])<2.5 \
            && ptll>30 \
            && PuppiMET_pt > 20 \
            && (Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13) \
            && Sum(CleanJet_pt > 30) == 2 \
            && mjj > 120 \
            && noJetInHorn'


# CUTS

#####################
### Signal region ###
#####################

cuts['hww_sr']  = {
   'expr': 'sr',
    # Define the sub-categorization of sr
   'categories' : {
      '2j_vbflike' : 'multiJet && vbflike',
      '2j_gghlike' : 'multiJet && gghlike',
      '2j_toplike' : 'multiJet && toplike',
      '2j_wwlike' : 'multiJet && wwlike',
   }
}

cuts['dycr']  = {
   'expr': 'dycr',
    # Define the sub-categorization of sr
   'categories' : {
      '2j' : 'multiJet',
   }
}

cuts['topcr']  = {
   'expr': 'topcr',
    # Define the sub-categorization of sr
   'categories' : {
      '2j' : 'multiJet',
   }
}

