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
            && Lepton_pdgId[0]==-Lepton_pdgId[1] \
            && multiJet \
            && abs(dphill) < 1.6 \
            && mjj > 350'


# CUTS

#####################
### Signal region ###
#####################

cuts['hww_sr']  = {
   'expr': 'sr && dymva[0] > 0.9',
    # Define the sub-categorization of sr
   'categories' : {
      '2j_ee' : '(Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11)',
      '2j_mm' : '(Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13)',
   }
}

cuts['wwcr']  = {
   #'expr': 'wwcr && dymva[0] > 0.05',
   'expr' : 'wwcr',
    # Define the sub-categorization of sr
   'categories' : {
      '2j_ee' : '(Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11)',
      '2j_mm' : '(Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13)',
   }
}

cuts['topcr']  = {
   #'expr': 'topcr && dymva[0] > 0.05',  
   'expr': 'topcr',
    # Define the sub-categorization of sr
   'categories' : {
      '2j_ee' : '(Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11)',
      '2j_mm' : '(Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13)',
   }
}