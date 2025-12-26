cuts = {}

# cuts
preselections = 'mll>12  \
             && Lepton_pt[0]>25 \
             && Lepton_pt[1]>10 \
             && (abs(Lepton_pdgId[1])==13 || Lepton_pt[1]>13) \
             && abs(Lepton_eta[0])<2.5 && abs(Lepton_eta[1])<2.5 \
             && bVeto \
             && PuppiMET_pt > 30 \
             '

# Splitting in sub-leading lepton pT 
####################################

## SR 2jets

# mu-e
cuts['hww2l2v_13TeV_WH_SS_em_2j'] = {
    'expr' : '(Lepton_pdgId[0]*Lepton_pdgId[1] == 11*13) && nLepton==2 && Alt(CleanJet_pt,0,0)>30 && Alt(CleanJet_pt,1,0)>30 && mjj < 400',
    'categories' : {
        # Sub-leading lepton pT >= 20 GeV
        'plus_pt2ge20'  : '((Lepton_pdgId[0] == -13 && Lepton_pdgId[1] == -11) || (Lepton_pdgId[0] == -11 && Lepton_pdgId[1] == -13)) && Lepton_pt[1]>=20 && abs(Lepton_eta[0] - Lepton_eta[1])<2.0',
        'minus_pt2ge20' : '((Lepton_pdgId[0] == +13 && Lepton_pdgId[1] == +11) || (Lepton_pdgId[0] == +11 && Lepton_pdgId[1] == +13)) && Lepton_pt[1]>=20 && abs(Lepton_eta[0] - Lepton_eta[1])<2.0',
    }
}

# e-e
cuts['hww2l2v_13TeV_WH_SS_ee_2j'] = {
    'expr' : '(Lepton_pdgId[0]*Lepton_pdgId[1] == 11*11) && nLepton==2 && Alt(CleanJet_pt,0,0)>30 && Alt(CleanJet_pt,1,0)>30 && mjj < 400 && abs(mll-91.2)>15',
    'categories' : {
        # Sub-leading lepton pT >= 20 GeV
        'plus_pt2ge20'  : 'Lepton_pdgId[0] == -11 && Lepton_pdgId[1] == -11 && Lepton_pt[1]>=20 && abs(Lepton_eta[0] - Lepton_eta[1])<2.0',
        'minus_pt2ge20' : 'Lepton_pdgId[0] == +11 && Lepton_pdgId[1] == +11 && Lepton_pt[1]>=20 && abs(Lepton_eta[0] - Lepton_eta[1])<2.0',
    }
}

# DY CR 2jet
cuts['hww2l2v_13TeV_WH_SS_DYee_2j'] = {
    'expr' : '(Lepton_pdgId[0]*Lepton_pdgId[1] == 11*11) && nLepton==2 && Alt(CleanJet_pt,0,0)>30 && Alt(CleanJet_pt,1,0)<30 && abs(Lepton_eta[0] - Lepton_eta[1])<2.0 && abs(mll-91.2)<15',
    'categories' : {
        # Sub-leading lepton pT >= 20 GeV
        'plus_pt2ge20'  : 'Lepton_pdgId[0] == -11 && Lepton_pdgId[1] == -11 && Lepton_pt[1]>=20',
        'minus_pt2ge20' : 'Lepton_pdgId[0] == +11 && Lepton_pdgId[1] == +11 && Lepton_pt[1]>=20',
    }
}

# mlljj20_whss:
# inv_mass of: (jet1, jet2, 2*closest_lep_to_jets)
# jets are considered with pT > 20 GeV 

# Definitions of WH3l variables:
# https://github.com/latinos/LatinoAnalysis/blob/76e7c4b93aa5f056c92440d4e8d24e7de749c8fe/NanoGardener/python/modules/l3KinProducer.py
