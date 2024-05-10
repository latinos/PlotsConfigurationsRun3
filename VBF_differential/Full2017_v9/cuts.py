import numpy as np
n_bins = 4

cuts = {}


preselections = 'mll>12 \
            && Lepton_pt[0]>25 && Lepton_pt[1]>13 \
            && Lepton_pdgId[0]*Lepton_pdgId[1]==-11*13 \
            && Alt(Lepton_pt,2,0)<10 \
            && Sum(CleanJet_pt>30)>=2\
            && mjj>120 \
            && ptll>30 \
            && PuppiMET_pt>20 \
            '



cuts['hww2l2v_13TeV_of2j_dphijj_4bins'] = {
   'expr': ' (abs(CleanJet_eta[0])<4.7) && (abs(CleanJet_eta[1])<4.7) && bVeto && mtw2>30 && mth>60',
   'categories' : {
        '0' : '( DeltaPhijj > {} && DeltaPhijj <= {})'.format(0*2*np.pi/n_bins - np.pi, 1*2*np.pi/n_bins - np.pi),
        '1' : '( DeltaPhijj > {} && DeltaPhijj <= {})'.format(1*2*np.pi/n_bins - np.pi, 2*2*np.pi/n_bins - np.pi),
        '2' : '( DeltaPhijj > {} && DeltaPhijj <= {})'.format(2*2*np.pi/n_bins - np.pi, 3*2*np.pi/n_bins - np.pi),
        '3' : '( DeltaPhijj > {} && DeltaPhijj <= {})'.format(3*2*np.pi/n_bins - np.pi, 4*2*np.pi/n_bins - np.pi),
   }
}

## Top control regions
cuts['hww2l2v_13TeV_top_of2j_dphijj_4bins']  = { 
   'expr' : 'topcr',
   'categories' : {
        '0' : '( DeltaPhijj > {} && DeltaPhijj <= {})'.format(0*2*np.pi/n_bins - np.pi, 1*2*np.pi/n_bins - np.pi),
        '1' : '( DeltaPhijj > {} && DeltaPhijj <= {})'.format(1*2*np.pi/n_bins - np.pi, 2*2*np.pi/n_bins - np.pi),
        '2' : '( DeltaPhijj > {} && DeltaPhijj <= {})'.format(2*2*np.pi/n_bins - np.pi, 3*2*np.pi/n_bins - np.pi),
        '3' : '( DeltaPhijj > {} && DeltaPhijj <= {})'.format(3*2*np.pi/n_bins - np.pi, 4*2*np.pi/n_bins - np.pi),
   }
}

## DY control regions
cuts['hww2l2v_13TeV_dytt_of2j_dphijj_4bins']  = { 
   'expr' : 'dycr',
   'categories' : {
        '0' : '( DeltaPhijj > {} && DeltaPhijj <= {})'.format(0*2*np.pi/n_bins - np.pi, 1*2*np.pi/n_bins - np.pi),
        '1' : '( DeltaPhijj > {} && DeltaPhijj <= {})'.format(1*2*np.pi/n_bins - np.pi, 2*2*np.pi/n_bins - np.pi),
        '2' : '( DeltaPhijj > {} && DeltaPhijj <= {})'.format(2*2*np.pi/n_bins - np.pi, 3*2*np.pi/n_bins - np.pi),
        '3' : '( DeltaPhijj > {} && DeltaPhijj <= {})'.format(3*2*np.pi/n_bins - np.pi, 4*2*np.pi/n_bins - np.pi),
   }
}

