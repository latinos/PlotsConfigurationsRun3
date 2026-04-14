cuts = {}

preselections = ' mll > 12 \
            && Lepton_pt[0]>25 \
            && Lepton_pt[1]>13 \
            && Alt(Lepton_pt, 2, 0)<10.0  \
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
      'pm_0j_pt2ge20' : ' Lepton_pdgId[0] < 0 && Lepton_pt[1]>=20 && zeroJet',
      'mp_0j_pt2ge20' : ' Lepton_pdgId[0] > 0 && Lepton_pt[1]>=20 && zeroJet',
      #
      'pm_0j_pt2lt20' : ' Lepton_pdgId[0] < 0 && Lepton_pt[1]<20 && zeroJet',
      'mp_0j_pt2lt20' : ' Lepton_pdgId[0] > 0 && Lepton_pt[1]<20 && zeroJet',
      #
      'pm_1j_pt2ge20' : ' Lepton_pdgId[0] < 0 && Lepton_pt[1]>=20 && oneJet && Alt(CleanJet_pt,1,0)<30',
      'mp_1j_pt2ge20' : ' Lepton_pdgId[0] > 0 && Lepton_pt[1]>=20 && oneJet && Alt(CleanJet_pt,1,0)<30',
      #
      'pm_1j_pt2lt20' : ' Lepton_pdgId[0] < 0 && Lepton_pt[1]<20 && oneJet && Alt(CleanJet_pt,1,0)<30',
      'mp_1j_pt2lt20' : ' Lepton_pdgId[0] > 0 && Lepton_pt[1]<20 && oneJet && Alt(CleanJet_pt,1,0)<30',
      # 
      '2j' : ' (mjj<65 || mjj>105) && mjj<120 && multiJet',
   }
}

cuts['wwcr']  = {
   'expr': 'wwcr',
    # Define the sub-categorization of sr
   'categories' : {
      '0j' : 'zeroJet',
      '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
      '2j' : '(mjj<65 || mjj>105) && mjj<120 && multiJet',
   }
}

cuts['topcr']  = {
   'expr': 'topcr',
    # Define the sub-categorization of sr
   'categories' : {
      '0j' : 'zeroJet',
      '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
      '2j' : '(mjj<65 || mjj>105) && mjj<120 && multiJet',
   }
}

cuts['dyttcr']  = {
   'expr': 'dycr',
    # Define the sub-categorization of sr
   'categories' : {
      '0j' : 'zeroJet',
      '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
      '2j' : '(mjj<65 || mjj>105) && mjj<120 && multiJet',
   }
}