
cuts = {}


preselections = 'Lepton_pt[0]>25 && Lepton_pt[1]>20\
            && abs(Lepton_eta[0])<2.5 && fabs(Lepton_eta[1])<2.5 \
            && Alt(Lepton_pt, 2, 0)<10.0 \
            && mll > 12'


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
