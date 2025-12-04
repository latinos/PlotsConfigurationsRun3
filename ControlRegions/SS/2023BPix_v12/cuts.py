cuts = {}

# cuts
preselections = 'mll>12  \
             && Lepton_pt[0]>25 \
             && Lepton_pt[1]>10 \
             && (abs(Lepton_pdgId[1])==13 || Lepton_pt[1]>13) \
             && abs(Lepton_eta[0])<2.5 && abs(Lepton_eta[1])<2.5 \
             && bVeto \
             && noJetInHorn'


###########################################################################
# B-veto: pre-selection compared to the WH charge-asymmetry signal region #
###########################################################################

# mu-mu
cuts['ss_mm'] = {
    'expr' : '(Lepton_pdgId[0]*Lepton_pdgId[1] == 13*13) && nLepton==2',
    'categories' : {
        '0j_plus_ptge20' : 'zeroJet && Lepton_pdgId[0] == +13 && Lepton_pdgId[1] == +13 && Lepton_pt[1]>=20',
        '0j_minus_ptge20' : 'zeroJet && Lepton_pdgId[0] == -13 && Lepton_pdgId[1] == -13 && Lepton_pt[1]>=20',
        '0j_plus_ptlt20' : 'zeroJet && Lepton_pdgId[0] == +13 && Lepton_pdgId[1] == +13 && Lepton_pt[1]<20',
        '0j_minus_ptlt20' : 'zeroJet && Lepton_pdgId[0] == -13 && Lepton_pdgId[1] == -13 && Lepton_pt[1]<20',
        '1j_plus_ptge20' : 'oneJet && Alt(CleanJet_pt, 1, 0) < 30 && Lepton_pdgId[0] == +13 && Lepton_pdgId[1] == +13 && Lepton_pt[1]>=20',
        '1j_minus_ptge20' : 'oneJet && Alt(CleanJet_pt, 1, 0) < 30 && Lepton_pdgId[0] == -13 && Lepton_pdgId[1] == -13 && Lepton_pt[1]>=20',
        '1j_plus_ptlt20' : 'oneJet && Alt(CleanJet_pt, 1, 0) < 30 && Lepton_pdgId[0] == +13 && Lepton_pdgId[1] == +13 && Lepton_pt[1]<20',
        '1j_minus_ptlt20' : 'oneJet && Alt(CleanJet_pt, 1, 0) < 30 && Lepton_pdgId[0] == -13 && Lepton_pdgId[1] == -13 && Lepton_pt[1]<20',
        '2j_plus_ptge20' : 'multiJet && Lepton_pdgId[0] == +13 && Lepton_pdgId[1] == +13 && Lepton_pt[1]>=20',
        '2j_minus_ptge20' : 'multiJet && Lepton_pdgId[0] == -13 && Lepton_pdgId[1] == -13 && Lepton_pt[1]>=20',
        '2j_plus_ptlt20' : 'multiJet && Lepton_pdgId[0] == +13 && Lepton_pdgId[1] == +13 && Lepton_pt[1]<20',
        '2j_minus_ptlt20' : 'multiJet && Lepton_pdgId[0] == -13 && Lepton_pdgId[1] == -13 && Lepton_pt[1]<20',
    }
}
# e-e
cuts['ss_ee'] = {
    'expr' : '(Lepton_pdgId[0]*Lepton_pdgId[1] == 11*11) && nLepton==2',
    'categories' : {
        '0j_plus_ptge20' : 'zeroJet && Lepton_pdgId[0] == +11 && Lepton_pdgId[1] == +11 && Lepton_pt[1]>=20',
        '0j_minus_ptge20' : 'zeroJet && Lepton_pdgId[0] == -11 && Lepton_pdgId[1] == -11 && Lepton_pt[1]>=20',
        '0j_plus_ptlt20' : 'zeroJet && Lepton_pdgId[0] == +11 && Lepton_pdgId[1] == +11 && Lepton_pt[1]<20',
        '0j_minus_ptlt20' : 'zeroJet && Lepton_pdgId[0] == -11 && Lepton_pdgId[1] == -11 && Lepton_pt[1]<20',
        '1j_plus_ptge20' : 'oneJet && Alt(CleanJet_pt, 1, 0) < 30 && Lepton_pdgId[0] == +11 && Lepton_pdgId[1] == +11 && Lepton_pt[1]>=20',
        '1j_minus_ptge20' : 'oneJet && Alt(CleanJet_pt, 1, 0) < 30 && Lepton_pdgId[0] == -11 && Lepton_pdgId[1] == -11 && Lepton_pt[1]>=20',
        '1j_plus_ptlt20' : 'oneJet && Alt(CleanJet_pt, 1, 0) < 30 && Lepton_pdgId[0] == +11 && Lepton_pdgId[1] == +11 && Lepton_pt[1]<20',
        '1j_minus_ptlt20' : 'oneJet && Alt(CleanJet_pt, 1, 0) < 30 && Lepton_pdgId[0] == -11 && Lepton_pdgId[1] == -11 && Lepton_pt[1]<20',
        '2j_plus_ptge20' : 'multiJet && Lepton_pdgId[0] == +11 && Lepton_pdgId[1] == +11 && Lepton_pt[1]>=20',
        '2j_minus_ptge20' : 'multiJet && Lepton_pdgId[0] == -11 && Lepton_pdgId[1] == -11 && Lepton_pt[1]>=20',
        '2j_plus_ptlt20' : 'multiJet && Lepton_pdgId[0] == +11 && Lepton_pdgId[1] == +11 && Lepton_pt[1]<20',
        '2j_minus_ptlt20' : 'multiJet && Lepton_pdgId[0] == -11 && Lepton_pdgId[1] == -11 && Lepton_pt[1]<20',
    }
}
# e-m
cuts['ss_em'] = {
    'expr' : '(Lepton_pdgId[0]*Lepton_pdgId[1] == 13*11) && nLepton==2',
    'categories' : {
        '0j_plus_ptge20' : 'zeroJet && ((Lepton_pdgId[0] == +13 && Lepton_pdgId[1] == +11) || (Lepton_pdgId[0] == +11 && Lepton_pdgId[1] == +13)) && Lepton_pt[1]>=20',
        '0j_minus_ptge20' : 'zeroJet && ((Lepton_pdgId[0] == -13 && Lepton_pdgId[1] == -11) || (Lepton_pdgId[0] == -11 && Lepton_pdgId[1] == -13)) && Lepton_pt[1]>=20',
        '0j_plus_ptlt20' : 'zeroJet && ((Lepton_pdgId[0] == +13 && Lepton_pdgId[1] == +11) || (Lepton_pdgId[0] == +11 && Lepton_pdgId[1] == +13)) && Lepton_pt[1]<20',
        '0j_minus_ptlt20' : 'zeroJet && ((Lepton_pdgId[0] == -13 && Lepton_pdgId[1] == -11) || (Lepton_pdgId[0] == -11 && Lepton_pdgId[1] == -13)) && Lepton_pt[1]<20',
        '1j_plus_ptge20' : 'oneJet && Alt(CleanJet_pt, 1, 0) < 30 && ((Lepton_pdgId[0] == +13 && Lepton_pdgId[1] == +11) || (Lepton_pdgId[0] == +11 && Lepton_pdgId[1] == +13)) && Lepton_pt[1]>=20',
        '1j_minus_ptge20' : 'oneJet && Alt(CleanJet_pt, 1, 0) < 30 && ((Lepton_pdgId[0] == -13 && Lepton_pdgId[1] == -11) || (Lepton_pdgId[0] == -11 && Lepton_pdgId[1] == -13)) && Lepton_pt[1]>=20',
        '1j_plus_ptlt20' : 'oneJet && Alt(CleanJet_pt, 1, 0) < 30 && ((Lepton_pdgId[0] == +13 && Lepton_pdgId[1] == +11) || (Lepton_pdgId[0] == +11 && Lepton_pdgId[1] == +13)) && Lepton_pt[1]<20',
        '1j_minus_ptlt20' : 'oneJet && Alt(CleanJet_pt, 1, 0) < 30 && ((Lepton_pdgId[0] == -13 && Lepton_pdgId[1] == -11) || (Lepton_pdgId[0] == -11 && Lepton_pdgId[1] == -13)) && Lepton_pt[1]<20',
        '2j_plus_ptge20' : 'multiJet && ((Lepton_pdgId[0] == +13 && Lepton_pdgId[1] == +11) || (Lepton_pdgId[0] == +11 && Lepton_pdgId[1] == +13)) && Lepton_pt[1]>=20',
        '2j_minus_ptge20' : 'multiJet && ((Lepton_pdgId[0] == -13 && Lepton_pdgId[1] == -11) || (Lepton_pdgId[0] == -11 && Lepton_pdgId[1] == -13)) && Lepton_pt[1]>=20',
        '2j_plus_ptlt20' : 'multiJet && ((Lepton_pdgId[0] == +13 && Lepton_pdgId[1] == +11) || (Lepton_pdgId[0] == +11 && Lepton_pdgId[1] == +13)) && Lepton_pt[1]<20',
        '2j_minus_ptlt20' : 'multiJet && ((Lepton_pdgId[0] == -13 && Lepton_pdgId[1] == -11) || (Lepton_pdgId[0] == -11 && Lepton_pdgId[1] == -13)) && Lepton_pt[1]<20',
    }
}