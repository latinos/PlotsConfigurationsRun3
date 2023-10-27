import numpy as np

preselections = '   mll>12 \
            && Lepton_pt[0]>25 \
            && Lepton_pt[1]>13 \
            && (nLepton>=2 && Alt(Lepton_pt, 2, 0)<10) \
            && abs(Lepton_eta[0])<2.5 && abs(Lepton_eta[1])<2.5 \
            && ptll>30 \
            && PuppiMET_pt > 20 \
            && (Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13) \
           '

cuts = {}
## Top control regions
cuts['hww2l2v_13TeV_top']  = {
   'expr' : 'topcr',
   'categories' : {
      '0j' : 'zeroJet',
      '1j' : 'oneJet && Alt(CleanJet_pt, 1, 0)<30',
      '2j' : 'multiJet',
   }
}

## WW control regions
cuts['hww2l2v_13TeV_ww']  = {
   'expr' : 'mtw2>30 && mll>50 && bVeto',
   'categories' : {
      '0j' : 'zeroJet',
      '1j' : 'oneJet && Alt(CleanJet_pt, 1, 0)<30',
      '2j' : 'multiJet',
   }
}

