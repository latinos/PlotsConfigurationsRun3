cuts = {}

# cuts
preselections = 'mll>12  \
             && Lepton_pt[0]>25 \
             && Lepton_pt[1]>10 \
             && (abs(Lepton_pdgId[1])==13 || Lepton_pt[1]>13) \
             && abs(Lepton_eta[0])<2.5 && abs(Lepton_eta[1])<2.5 \
             && bVeto \
             && noJetInHorn'

# m-m
cuts['ss_mm_SR'] = {
    'expr' : '(Lepton_pdgId[0]*Lepton_pdgId[1] == 13*13) && nLepton==2 && ptll>30  && PuppiMET_pt > 20 && mth > 60 && mtw2 > 30',
    'categories' : {
        '0j' : 'zeroJet',
        '1j' : 'oneJet && Alt(CleanJet_pt, 1, 0) < 30',
        '2j' : 'multiJet',
        'inc' : '1',
    }
}
# e-e
cuts['ss_ee_SR'] = {
    'expr' : '(Lepton_pdgId[0]*Lepton_pdgId[1] == 11*11) && nLepton==2 && abs(mll - 91) > 15 && ptll>30  && PuppiMET_pt > 20 && mth > 60 && mtw2 > 30',
    'categories' : {
        '0j' : 'zeroJet',
        '1j' : 'oneJet && Alt(CleanJet_pt, 1, 0) < 30',
        '2j' : 'multiJet',
        'inc' : '1',
    }
}
# e-m
cuts['ss_em_SR'] = {
    'expr' : '(Lepton_pdgId[0]*Lepton_pdgId[1] == 13*11) && nLepton==2 && ptll>30  && PuppiMET_pt > 20 && mth > 60 && mtw2 > 30',
    'categories' : {
        '0j' : 'zeroJet',
        '1j' : 'oneJet && Alt(CleanJet_pt, 1, 0) < 30',
        '2j' : 'multiJet',
        'inc' : '1',
    }
}

