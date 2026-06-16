# cuts

cuts = {}

preselections = 'mll>12  \
              && Lepton_pt[0]>25 \
              && Lepton_pt[1]>10 \
              && (abs(Lepton_pdgId[1])==13 || Lepton_pt[1]>13) \
              && abs(Lepton_eta[0])<2.5 && abs(Lepton_eta[1])<2.5 \
              && bVeto \
              '

              #&& bVeto \
              #&& PuppiMET_pt > 30 \
              #&& !hole_veto \


## Same-sign control region in the 0 jet bin: used in the WH3l category. Considering different flavor to avoid DY
#cuts['wh3l_13TeV_OS_CR'] = {
    #'expr' : 'Alt(Lepton_pt,2,0) < 15 && abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13 && Alt(CleanJet_pt,0,0) < 30',
    #'categories' : {
        #'pt2ge20'  : 'Lepton_pdgId[0]*Lepton_pdgId[1]<0',
    #}
#}



cuts['DY'] = {
    'expr' : 'Alt(Lepton_pt,2,0) < 15 && (abs(Lepton_pdgId[0])==abs(Lepton_pdgId[1]))',
    'categories' : {
        '0j'  : 'Alt(CleanJet_pt,0,0) < 30',
        '1j'  : 'Alt(CleanJet_pt,1,0) < 30 && Alt(CleanJet_pt,0,0) > 30',
        '2j'  : 'Alt(CleanJet_pt,2,0) < 30 && Alt(CleanJet_pt,1,0) > 30',
    }
}
    


cuts['Sig'] = {
    'expr' : 'Alt(Lepton_pt,2,0) < 15 && (abs(Lepton_pdgId[0])==abs(Lepton_pdgId[1])) && Alt(CleanJet_pt,2,0) < 30 && Alt(CleanJet_pt,1,0) > 30',
    'categories' : {
        'mllZ'               : 'mll>60 && mll< 120',
        'mllZpt1'            : 'mll>80 && mll< 100 && Lepton_pt[0]>40',
        'mllZpt1qgl'         : 'mll>80 && mll< 100 && Lepton_pt[0]>40 && Alt(Jet_qgl,CleanJet_jetIdx[0],2)<0.5 && Alt(Jet_qgl,CleanJet_jetIdx[1],2)<0.5',
        'mllZpt1qglmet'      : 'mll>80 && mll< 100 && Lepton_pt[0]>40 && Alt(Jet_qgl,CleanJet_jetIdx[0],2)<0.5 && Alt(Jet_qgl,CleanJet_jetIdx[1],2)<0.5 && PuppiMET_pt<60',
        'mllZpt1qglmetbVeto' : 'mll>80 && mll< 100 && Lepton_pt[0]>40 && Alt(Jet_qgl,CleanJet_jetIdx[0],2)<0.5 && Alt(Jet_qgl,CleanJet_jetIdx[1],2)<0.5 && PuppiMET_pt<60 && bVeto',
        'opt1'               : 'mll>80 && mll< 100 && Lepton_pt[0]>40 && Alt(Jet_qgl,CleanJet_jetIdx[0],2)<0.5 && Alt(Jet_qgl,CleanJet_jetIdx[1],2)<0.5 && PuppiMET_pt<60 && bVeto && detajj<3',
        'opt2'               : 'mll>80 && mll< 100 && Lepton_pt[0]>40 && Alt(Jet_qgl,CleanJet_jetIdx[0],2)<0.5 && Alt(Jet_qgl,CleanJet_jetIdx[1],2)<0.5 && PuppiMET_pt<60 && bVeto && detajj<3 && mjj<160 && mjj>60 && dphilljetjet>1',
        'opt3'               : 'mll>80 && mll< 100 && Lepton_pt[0]>40 && Alt(Jet_qgl,CleanJet_jetIdx[0],2)<0.5 && Alt(Jet_qgl,CleanJet_jetIdx[1],2)<0.5 && PuppiMET_pt<60 && bVeto && detajj<3 && mjj<160 && mjj>60 && dphilljetjet>1 && Alt(Jet_btagDeepB,CleanJet_jetIdx[0],2)<0.2 && Alt(Jet_btagDeepB,CleanJet_jetIdx[1],2) < 0.2 && Alt(Jet_btagCSVV2,CleanJet_jetIdx[0],2)<0.7 && Alt(Jet_btagCSVV2,CleanJet_jetIdx[1],2)<0.7',
        'opt4'               : 'mll>80 && mll< 100 && Lepton_pt[0]>40 && Alt(Jet_qgl,CleanJet_jetIdx[0],2)<0.5 && Alt(Jet_qgl,CleanJet_jetIdx[1],2)<0.5 && PuppiMET_pt<60 && bVeto && detajj<2 && mjj<150 && mjj>60 && dphilljetjet>1 && Alt(Jet_btagDeepB,CleanJet_jetIdx[0],2)<0.2 && Alt(Jet_btagDeepB,CleanJet_jetIdx[1],2) < 0.2 && Alt(Jet_btagCSVV2,CleanJet_jetIdx[0],2)<0.7 && Alt(Jet_btagCSVV2,CleanJet_jetIdx[1],2)<0.7 && ptll>20 && Alt(CleanJet_pt,0,0) > 50',
        'opt5future'         : 'mll>85 && mll< 95 && Lepton_pt[0]>40 && Alt(Jet_qgl,CleanJet_jetIdx[0],2)<0.1 && Alt(Jet_qgl,CleanJet_jetIdx[1],2)<0.1 && PuppiMET_pt<60 && bVeto && detajj<2 && mjj<150 && mjj>60 && dphilljetjet>1 && Alt(Jet_btagDeepB,CleanJet_jetIdx[0],2)<0.2 && Alt(Jet_btagDeepB,CleanJet_jetIdx[1],2) < 0.2 && Alt(Jet_btagCSVV2,CleanJet_jetIdx[0],2)<0.7 && Alt(Jet_btagCSVV2,CleanJet_jetIdx[1],2)<0.7 && ptll>20 && Alt(CleanJet_pt,0,0) > 50 && Alt(CleanJet_eta,1,0) < 2.5 && Alt(CleanJet_eta,1,0) > -2.5 && Alt(CleanJet_eta,0,0) < 2.5 && Alt(CleanJet_eta,0,0) > -2.5 && Alt(Lepton_pt,0,0)>50',
        'opt6future'         : 'mll>85 && mll< 95 && Lepton_pt[0]>40 && Alt(Jet_qgl,CleanJet_jetIdx[0],2)<0.04 && Alt(Jet_qgl,CleanJet_jetIdx[1],2)<0.04 && PuppiMET_pt<60 && bVeto && detajj<2 && mjj<150 && mjj>60 && dphilljetjet>1 && Alt(Jet_btagDeepB,CleanJet_jetIdx[0],2)<0.2 && Alt(Jet_btagDeepB,CleanJet_jetIdx[1],2) < 0.2 && Alt(Jet_btagCSVV2,CleanJet_jetIdx[0],2)<0.7 && Alt(Jet_btagCSVV2,CleanJet_jetIdx[1],2)<0.7 && ptll>20 && Alt(CleanJet_pt,0,0) > 75 && Alt(CleanJet_eta,1,0) < 2.0 && Alt(CleanJet_eta,1,0) > -2.0 && Alt(CleanJet_eta,0,0) < 2.0 && Alt(CleanJet_eta,0,0) > -2.0 && Alt(Lepton_pt,0,0)>50 && ptll>100 && Lepton_pt[1]>20',
        
    }
}
    
