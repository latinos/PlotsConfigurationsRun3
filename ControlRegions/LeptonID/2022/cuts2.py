
cuts = {}


preselections = 'Lepton_pt[0]>25 && Lepton_pt[1]>13\
            && (nLepton>=2 && Alt$(Lepton_pt[2],0)<10) \
            && abs(Lepton_eta[0])<2.5 && abs(Lepton_eta[1])<2.5 \
            && ptll>30 \
            && PuppiMET_pt > 20 \
            && (Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13) \
            && mll > 12'
            
cuts['hww2l2v_'] = {
   'expr': 'sr',
    # Define the sub-categorization of sr
   'categories' : {
      'pm_0j_pt2ge20' : ' Lepton_pdgId[0] < 0 && Lepton_pt[1]>=20 && zeroJet',
      'mp_0j_pt2ge20' : ' Lepton_pdgId[0] > 0 && Lepton_pt[1]>=20 && zeroJet',
      #
      'pm_0j_pt2lt20' : ' Lepton_pdgId[0] < 0 && Lepton_pt[1]<20 && zeroJet',
      'mp_0j_pt2lt20' : ' Lepton_pdgId[0] > 0 && Lepton_pt[1]<20 && zeroJet',
      #
      'pm_1j_pt2ge20' : ' Lepton_pdgId[0] < 0 && Lepton_pt[1]>=20 && oneJet && Alt$(CleanJet_pt[1],0)<30',
      'mp_1j_pt2ge20' : ' Lepton_pdgId[0] > 0 && Lepton_pt[1]>=20 && oneJet && Alt$(CleanJet_pt[1],0)<30',
      #
      'pm_1j_pt2lt20' : ' Lepton_pdgId[0] < 0 && Lepton_pt[1]<20 && oneJet && Alt$(CleanJet_pt[1],0)<30',
      'mp_1j_pt2lt20' : ' Lepton_pdgId[0] > 0 && Lepton_pt[1]<20 && oneJet && Alt$(CleanJet_pt[1],0)<30',
      # FIXME fix the mjj or additional cuts to make this orthogonal to VH2j and VBF
      '2j'               : ' (mjj<65 || mjj>105) && mjj<120 && multiJet', 
   }
}
     
## Top control regions
cuts['hww2l2v_13TeV_top']  = { 
   'expr' : 'topcr',
    # Define the sub-categorization of topcr
   'categories' : {
      '0j' : 'zeroJet',
      '1j' : 'oneJet && Alt$(CleanJet_pt[1],0)<30',
      '2j' : '(mjj<65 || mjj>105) && mjj<120 && multiJet',
   }
}

cuts['hww2l2v_13TeV_top_ee']  = {
   'expr' : 'topcr',
    # Define the sub-categorization of topcr
   'categories' : {
      '0j' : 'zeroJet && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11',
      '1j' : 'oneJet && Alt$(CleanJet_pt[1],0)<30 && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11',
      '2j' : '(mjj<65 || mjj>105) && mjj<120 && multiJet && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11',
   }
}

cuts['hww2l2v_13TeV_top_mm']  = {
   'expr' : 'topcr',
    # Define the sub-categorization of topcr
   'categories' : {
      '0j' : 'zeroJet && Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13',
      '1j' : 'oneJet && Alt$(CleanJet_pt[1],0)<30 && Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13',
      '2j' : '(mjj<65 || mjj>105) && mjj<120 && multiJet && Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13',
   }
}

'''
cuts['ss']  = {
    'expr' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == 11*13) && mll>12 && bVeto',
    'categories' : {
        'em' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == 11*13)',
    }
}


cuts['ww2l2nu_top']  = {
    'expr' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == -11*13) && topcr && ptll_>15 && PuppiMET_pt > 20',
    'categories' : {
        'inc' :'Lepton_pt[0]>20'
    }
}

cuts['ww2l2nu_dytt']  = {
    'expr' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == -11*13) && bVeto && mth_<40 && ptll_>15 && PuppiMET_pt > 20',
    'categories' : {
        'inc' : 'Lepton_pt[0]>20'
    }
}

cuts['ww2l2nu_sr']  = {
    'expr' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == -11*13) && mll_>85 && bVeto && mth_>40 && mpmet>15 && ptll_>15 && PuppiMET_pt > 20',
    'categories' : {
        'inc' : 'Lepton_pt[0]>20'
    }
}

cuts['ww2l2nu_top_smp']  = {
    'expr' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == -11*13) && topcr && ptll_>15 && PuppiMET_pt > 20',
    'categories' : {
        'inc' :'Lepton_pt[0]>20'
    }
}

cuts['ww2l2nu_dytt_smp']  = {
    'expr' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == -11*13) && bVeto && mll_<85 && ptll_<30',
    'categories' : {
        'inc' : 'Lepton_pt[0]>20'
    }
}

cuts['ww2l2nu_sr_smp']  = {
    'expr' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == -11*13) && mll_>85 && bVeto',
    'categories' : {
        'inc' : 'Lepton_pt[0]>20'
    }
}
'''
