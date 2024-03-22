cuts = {}


preselections = 'Lepton_pt[0]>25 && Lepton_pt[1]>13 && (nLepton>=2 && Alt(Lepton_pt, 2, 0)<10) \
            && abs(Lepton_eta[0])<2.5 && abs(Lepton_eta[1])<2.5 \
            && PuppiMET_pt > 20 && ptll > 30 && mll > 50 \
            && multiJet \
            && mjj > 300 && detajj > 2.5'



cuts['VBS'] = {
   'expr': 'sr',
   'categories' : {
      '2j_em_isVBS' : 'mth > 60 && dnn_SigVsBkg[0] > 0.5 && (Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13)',
      '2j_em_isBKG' : 'mth > 60 && dnn_SigVsBkg[0] < 0.5 && (Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13)',
    }
}

## Top control regions
cuts['top']  = { 
   'expr' : 'topcr',
   'categories' : {
      '2j_em' : '(Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13)',
   }
}

## DY control regions
cuts['DY']  = { 
   'expr' : 'dycr',
   'categories' : { 
      '2j_em'   : 'mth < 60 && (Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13) && abs(mll-65) < 15 ',
      }
}

