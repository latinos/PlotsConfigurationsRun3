# cuts

cuts = {}

preselections = 'Lepton_pt[0]>25 \
              && Alt(Lepton_pt,1,0)<10  \
              && abs(Lepton_eta[0])<2.5 \
              && bVeto \
              '


cuts['WjetsCR'] = {
    'expr' : '1',
    'categories' : {
        '0j'  : 'Alt(CleanJet_pt,0,0) < 30',
        '1j'  : 'Alt(CleanJet_pt,1,0) < 30 && Alt(CleanJet_pt,0,0) > 30',
        '2j'  : 'Alt(CleanJet_pt,2,0) < 30 && Alt(CleanJet_pt,1,0) > 30',
    }
}
    

cuts['Sig1l'] = {
    'expr' : '   Alt(Lepton_pt,1,0)<10 \
              && Alt(CleanJet_pt,2,0) < 30 && Alt(CleanJet_pt,1,0) > 30',
    'categories' : {
        'inclusive'               : '1',
        'opt1'                    : 'PuppiMET_pt>20 && detajj<3 && Alt(Jet_qgl,CleanJet_jetIdx[0],2)<0.5 && Alt(Jet_qgl,CleanJet_jetIdx[1],2)<0.5 && abs(Lepton_eta[0])<1.5',
        'opt2'                    : 'PuppiMET_pt>20 && detajj<3 && Alt(Jet_qgl,CleanJet_jetIdx[0],2)<0.5 && Alt(Jet_qgl,CleanJet_jetIdx[1],2)<0.5 && abs(Lepton_eta[0])<1.5 && Alt(Jet_btagCSVV2,CleanJet_jetIdx[0],2)<0.5 && Alt(Jet_btagCSVV2,CleanJet_jetIdx[1],2) < 0.5 && Alt(Jet_btagDeepB,CleanJet_jetIdx[0],2)<0.2 && Alt(Jet_btagDeepB,CleanJet_jetIdx[1],2)<0.2',
        'opt3'                    : 'PuppiMET_pt>20 && detajj<2 && Alt(Jet_qgl,CleanJet_jetIdx[0],2)<0.5 && Alt(Jet_qgl,CleanJet_jetIdx[1],2)<0.5 && abs(Lepton_eta[0])<1.5 && Alt(Jet_btagCSVV2,CleanJet_jetIdx[0],2)<0.5 && Alt(Jet_btagCSVV2,CleanJet_jetIdx[1],2) < 0.5 && Alt(Jet_btagDeepB,CleanJet_jetIdx[0],2)<0.2 && Alt(Jet_btagDeepB,CleanJet_jetIdx[1],2)<0.2 && mjj<180 && Alt(CleanJet_pt,0,0) > 50 && abs(Alt(CleanJet_eta,0,0))<2.0 && abs(Alt(CleanJet_eta,1,0))<2.0',

    }
}

