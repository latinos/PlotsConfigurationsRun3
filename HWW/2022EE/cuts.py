cuts = {}

preselections = 'Lepton_pt[0]>25 && Lepton_pt[1]>13\
            && abs(Lepton_eta[0])<2.5 && fabs(Lepton_eta[1])<2.5 \
            && Alt(Lepton_pt, 2, 0)<10.0 \
            && mll > 12 \
            && ptll > 30 \
            && PuppiMET_pt > 20' 


# CUTS

################################
### Nonprompt control region ###
################################

"""
cuts['ss_cr']  = {
    'expr' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == 11*13) && bVeto',
    'categories' : {
        'em' : '(Lepton_pdgId[0] * Lepton_pdgId[1] == 11*13)',
    }
}
"""

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
      '1j_th40': 'oneJet && Alt(CleanJet_pt, 1, 0) < 30 && ((CleanJet_pt[0] > 30)*(abs(CleanJet_eta[0]) < 2.5) || (CleanJet_pt[0] > 40)*(abs(CleanJet_eta[0]) > 2.5))',
      '2j_th40': 'multiJet && (((CleanJet_pt[1] > 30)*(abs(CleanJet_eta[1]) < 2.5) || (CleanJet_pt[1] > 40)*(abs(CleanJet_eta[1]) > 2.5)) && ((CleanJet_pt[0] > 30)*(abs(CleanJet_eta[0]) < 2.5) || (CleanJet_pt[0] > 40)*(abs(CleanJet_eta[0]) > 2.5)))',
      '1j_th50': 'oneJet && Alt(CleanJet_pt, 1, 0) < 30 && ((CleanJet_pt[0] > 30)*(abs(CleanJet_eta[0]) < 2.5) || (CleanJet_pt[0] > 50)*(abs(CleanJet_eta[0]) > 2.5))',
      '2j_th50': 'multiJet && (((CleanJet_pt[1] > 30)*(abs(CleanJet_eta[1]) < 2.5) || (CleanJet_pt[1] > 50)*(abs(CleanJet_eta[1]) > 2.5)) && ((CleanJet_pt[0] > 30)*(abs(CleanJet_eta[0]) < 2.5) || (CleanJet_pt[0] > 50)*(abs(CleanJet_eta[0]) > 2.5)))',
      '1j_tracker': 'oneJet && Alt(CleanJet_pt, 1, 0) < 30 && abs(CleanJet_eta[0]) < 2.5',
      '2j_tracker': 'multiJet && abs(CleanJet_eta[1]) < 2.5 && abs(CleanJet_eta[0]) < 2.5 ',
      'inc': '1',
      'anypt_eta_cut' : 'Sum(abs(CleanJet_eta)>=1.5) == 0',
      'jet_eta_cut' : 'Sum(CleanJet_pt[abs(CleanJet_eta)>=1.5]>30) == 0'
      #'inc_4j_in' : 'abs(CleanJet_eta[0]) < 1.5 && abs(CleanJet_eta[1]) < 1.5 && abs(CleanJet_eta[2]) < 1.5 && abs(CleanJet_eta[3]) < 1.5',
      #'inc_2j_in' : 'abs(CleanJet_eta[0]) < 1.5 && abs(CleanJet_eta[1]) < 1.5'
   }
}

###########################
### DYtt control region ###
###########################
'''
cuts['dytt_cr']  = {
	'expr' : 'dycr && (Lepton_pdgId[0] * Lepton_pdgId[1] == -11*13)',
# Define the sub-categorization of dycr
   'categories' : { 
      # '0j' : 'zeroJet',
      # '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
      # '2j' : 'multiJet',
      # "1j_th40": "oneJet && Alt(CleanJet_pt, 1, 0) < 30 && ((CleanJet_pt[0] > 30)*(abs(CleanJet_eta[0]) < 2.5) || (CleanJet_pt[0] > 40)*(abs(CleanJet_eta[0]) > 2.5))",
      # "2j_th40": "multiJet && (((CleanJet_pt[1] > 30)*(abs(CleanJet_eta[1]) < 2.5) || (CleanJet_pt[1] > 40)*(abs(CleanJet_eta[1]) > 2.5)) && ((CleanJet_pt[0] > 30)*(abs(CleanJet_eta[0]) < 2.5) || (CleanJet_pt[0] > 40)*(abs(CleanJet_eta[0]) > 2.5)))",
      # "1j_th50": "oneJet && Alt(CleanJet_pt, 1, 0) < 30 && ((CleanJet_pt[0] > 30)*(abs(CleanJet_eta[0]) < 2.5) || (CleanJet_pt[0] > 50)*(abs(CleanJet_eta[0]) > 2.5))",
      # "2j_th50": "multiJet && (((CleanJet_pt[1] > 30)*(abs(CleanJet_eta[1]) < 2.5) || (CleanJet_pt[1] > 50)*(abs(CleanJet_eta[1]) > 2.5)) && ((CleanJet_pt[0] > 30)*(abs(CleanJet_eta[0]) < 2.5) || (CleanJet_pt[0] > 50)*(abs(CleanJet_eta[0]) > 2.5)))",
      # "1j_tracker": "oneJet && Alt(CleanJet_pt, 1, 0) < 30 && abs(CleanJet_eta[0]) < 2.5",
      # "2j_tracker": "multiJet && abs(CleanJet_eta[1]) < 2.5 && abs(CleanJet_eta[0]) < 2.5 ",
      'inc_4j_in' : '1 && abs(CleanJet_eta[0]) < 1.5 && abs(CleanJet_eta[1]) < 1.5 && abs(CleanJet_eta[2]) < 1.5 && abs(CleanJet_eta[3]) < 1.5',
      'inc_2j_in' : '1 && abs(CleanJet_eta[0]) < 1.5 && abs(CleanJet_eta[1]) < 1.5'
   }
}
'''
#########################
### WW control region ###
#########################
'''
cuts['ww_cr']  = {
  'expr' : 'wwcr && (Lepton_pdgId[0] * Lepton_pdgId[1] == -11*13)',
	  'categories' : {
      # '0j' : 'zeroJet',
      # '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
      # '2j' : 'multiJet',
      # "1j_th40": "oneJet && Alt(CleanJet_pt, 1, 0) < 30 && ((CleanJet_pt[0] > 30)*(abs(CleanJet_eta[0]) < 2.5) || (CleanJet_pt[0] > 40)*(abs(CleanJet_eta[0]) > 2.5))",
      # "2j_th40": "multiJet && (((CleanJet_pt[1] > 30)*(abs(CleanJet_eta[1]) < 2.5) || (CleanJet_pt[1] > 40)*(abs(CleanJet_eta[1]) > 2.5)) && ((CleanJet_pt[0] > 30)*(abs(CleanJet_eta[0]) < 2.5) || (CleanJet_pt[0] > 40)*(abs(CleanJet_eta[0]) > 2.5)))",
      # "1j_th50": "oneJet && Alt(CleanJet_pt, 1, 0) < 30 && ((CleanJet_pt[0] > 30)*(abs(CleanJet_eta[0]) < 2.5) || (CleanJet_pt[0] > 50)*(abs(CleanJet_eta[0]) > 2.5))",
      # "2j_th50": "multiJet && (((CleanJet_pt[1] > 30)*(abs(CleanJet_eta[1]) < 2.5) || (CleanJet_pt[1] > 50)*(abs(CleanJet_eta[1]) > 2.5)) && ((CleanJet_pt[0] > 30)*(abs(CleanJet_eta[0]) < 2.5) || (CleanJet_pt[0] > 50)*(abs(CleanJet_eta[0]) > 2.5)))",
      # "1j_tracker": "oneJet && Alt(CleanJet_pt, 1, 0) < 30 && abs(CleanJet_eta[0]) < 2.5",
      # "2j_tracker": "multiJet && abs(CleanJet_eta[1]) < 2.5 && abs(CleanJet_eta[0]) < 2.5 ",
      'inc_4j_in' : '1 && abs(CleanJet_eta[0]) < 1.5 && abs(CleanJet_eta[1]) < 1.5 && abs(CleanJet_eta[2]) < 1.5 && abs(CleanJet_eta[3]) < 1.5',
      'inc_2j_in' : '1 && abs(CleanJet_eta[0]) < 1.5 && abs(CleanJet_eta[1]) < 1.5'
	  }
	}
'''
#####################
### Signal region ###
#####################
'''
cuts['hww_sr']  = {
   'expr': 'sr && (Lepton_pdgId[0] * Lepton_pdgId[1] == -11*13)',
    # Define the sub-categorization of sr
   'categories' : {
      # '0j' : 'zeroJet',
      # '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
      # '2j' : 'multiJet',
      # "1j_th40": "oneJet && Alt(CleanJet_pt, 1, 0) < 30 && ((CleanJet_pt[0] > 30)*(abs(CleanJet_eta[0]) < 2.5) || (CleanJet_pt[0] > 40)*(abs(CleanJet_eta[0]) > 2.5))",
      # "2j_th40": "multiJet && (((CleanJet_pt[1] > 30)*(abs(CleanJet_eta[1]) < 2.5) || (CleanJet_pt[1] > 40)*(abs(CleanJet_eta[1]) > 2.5)) && ((CleanJet_pt[0] > 30)*(abs(CleanJet_eta[0]) < 2.5) || (CleanJet_pt[0] > 40)*(abs(CleanJet_eta[0]) > 2.5)))",
      # "1j_th50": "oneJet && Alt(CleanJet_pt, 1, 0) < 30 && ((CleanJet_pt[0] > 30)*(abs(CleanJet_eta[0]) < 2.5) || (CleanJet_pt[0] > 50)*(abs(CleanJet_eta[0]) > 2.5))",
      # "2j_th50": "multiJet && (((CleanJet_pt[1] > 30)*(abs(CleanJet_eta[1]) < 2.5) || (CleanJet_pt[1] > 50)*(abs(CleanJet_eta[1]) > 2.5)) && ((CleanJet_pt[0] > 30)*(abs(CleanJet_eta[0]) < 2.5) || (CleanJet_pt[0] > 50)*(abs(CleanJet_eta[0]) > 2.5)))",
      # "1j_tracker": "oneJet && Alt(CleanJet_pt, 1, 0) < 30 && abs(CleanJet_eta[0]) < 2.5",
      # "2j_tracker": "multiJet && abs(CleanJet_eta[1]) < 2.5 && abs(CleanJet_eta[0]) < 2.5 ",
      'inc_4j_in' : '1 && abs(CleanJet_eta[0]) < 1.5 && abs(CleanJet_eta[1]) < 1.5 && abs(CleanJet_eta[2]) < 1.5 && abs(CleanJet_eta[3]) < 1.5',
      'inc_2j_in' : '1 && abs(CleanJet_eta[0]) < 1.5 && abs(CleanJet_eta[1]) < 1.5'
   }
}
'''
# Additional categories for JER studies
"""
"1j_th40": "oneJet && Alt(CleanJet_pt, 1, 0) < 30 && ((CleanJet_pt[0] > 30)*(abs(CleanJet_eta[0]) < 2.5) || (CleanJet_pt[0] > 40)*(abs(CleanJet_eta[0]) > 2.5))",
"2j_th40": "multiJet && (((CleanJet_pt[1] > 30)*(abs(CleanJet_eta[1]) < 2.5) || (CleanJet_pt[1] > 40)*(abs(CleanJet_eta[1]) > 2.5)) && ((CleanJet_pt[0] > 30)*(abs(CleanJet_eta[0]) < 2.5) || (CleanJet_pt[0] > 40)*(abs(CleanJet_eta[0]) > 2.5)))",
"1j_th50": "oneJet && Alt(CleanJet_pt, 1, 0) < 30 && ((CleanJet_pt[0] > 30)*(abs(CleanJet_eta[0]) < 2.5) || (CleanJet_pt[0] > 50)*(abs(CleanJet_eta[0]) > 2.5))",
"2j_th50": "multiJet && (((CleanJet_pt[1] > 30)*(abs(CleanJet_eta[1]) < 2.5) || (CleanJet_pt[1] > 50)*(abs(CleanJet_eta[1]) > 2.5)) && ((CleanJet_pt[0] > 30)*(abs(CleanJet_eta[0]) < 2.5) || (CleanJet_pt[0] > 50)*(abs(CleanJet_eta[0]) > 2.5)))",
"1j_out": "oneJet && Alt(CleanJet_pt, 1, 0) < 30 && abs(CleanJet_eta[0]) > 2.5",
"2j_out": "multiJet && abs(CleanJet_eta[1]) > 2.5 && abs(CleanJet_eta[0]) > 2.5 ",
"1j_out_th40": "oneJet && Alt(CleanJet_pt, 1, 0) < 30 && abs(CleanJet_eta[0]) > 2.5 && CleanJet_pt[0] > 40",
"2j_out_th40": "multiJet && abs(CleanJet_eta[1]) > 2.5 && abs(CleanJet_eta[0]) > 2.5 && CleanJet_pt[0] > 40 && CleanJet_pt[1] > 40",
"1j_out_th50": "oneJet && Alt(CleanJet_pt, 1, 0) < 30 && abs(CleanJet_eta[0]) > 2.5 && CleanJet_pt[0] > 50",
"2j_out_th50": "multiJet && abs(CleanJet_eta[1]) > 2.5 && abs(CleanJet_eta[0]) > 2.5 && CleanJet_pt[0] > 50 && CleanJet_pt[1] > 50",
"1j_tracker": "oneJet && Alt(CleanJet_pt, 1, 0) < 30 && abs(CleanJet_eta[0]) < 2.5",
"2j_tracker": "multiJet && abs(CleanJet_eta[1]) < 2.5 && abs(CleanJet_eta[0]) < 2.5 "
"""
