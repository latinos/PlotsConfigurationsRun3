cuts = {}

preselections = 'Lepton_pt[0]>25 && Lepton_pt[1]>13\
            && abs(Lepton_eta[0])<2.5 && fabs(Lepton_eta[1])<2.5 \
            && Alt(Lepton_pt, 2, 0)<10.0 \
            && mll > 12 \
            && ptll > 30 \
            && PuppiMET_pt > 20' 


# CUTS

##########################
### Top control region ###
##########################

cuts['top_cr']  = { 
   'expr' : 'topcr && (Lepton_pdgId[0] * Lepton_pdgId[1] == -11*13)',
    # Define the sub-categorization of topcr
   'categories' : {
      '0j' : 'zeroJet',
      '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
      '2j' : 'multiJet',
      'inc': '1',
   }
}