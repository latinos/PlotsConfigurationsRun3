cuts = {}

# cuts
preselections = 'mll>12  \
             && Lepton_pt[0]>25 \
             && Lepton_pt[1]>10 \
             && (abs(Lepton_pdgId[1])==13 || Lepton_pt[1]>13) \
             && abs(Lepton_eta[0])<2.5 && abs(Lepton_eta[1])<2.5 \
             && bVeto \
             && !hole_veto \
             '


###########################################################################
# B-veto: pre-selection compared to the WH charge-asymmetry signal region #
###########################################################################

# mu-mu
cuts['hww2l2v_13TeV_WH_SS_mm_2j'] = {
    'expr' : '(Lepton_pdgId[0]*Lepton_pdgId[1] == 13*13) && nLepton==2 && Alt(CleanJet_pt,0,0)>30 && Alt(CleanJet_pt,1,0)>30',
    'categories' : {
        'SS_CR_plus_pt2ge20'  : 'Lepton_pdgId[0] == -13 && Lepton_pdgId[1] == -13 && Lepton_pt[1]>=20',
        'SS_CR_minus_pt2ge20' : 'Lepton_pdgId[0] == +13 && Lepton_pdgId[1] == +13 && Lepton_pt[1]>=20',
        # 'SS_CR_plus_pt2lt20'  : 'Lepton_pdgId[0] == -13 && Lepton_pdgId[1] == -13 && Lepton_pt[1]<20',
        # 'SS_CR_minus_pt2lt20' : 'Lepton_pdgId[0] == +13 && Lepton_pdgId[1] == +13 && Lepton_pt[1]<20',
    }
}

# mu-e
cuts['hww2l2v_13TeV_WH_SS_em_2j'] = {
    'expr' : '(Lepton_pdgId[0]*Lepton_pdgId[1] == 11*13) && nLepton==2 && Alt(CleanJet_pt,0,0)>30 && Alt(CleanJet_pt,1,0)>30',
    'categories' : {
        'SS_CR_plus_pt2ge20'  : '((Lepton_pdgId[0] == -13 && Lepton_pdgId[1] == -11) || (Lepton_pdgId[0] == -11 && Lepton_pdgId[1] == -13)) && Lepton_pt[1]>=20',
        'SS_CR_minus_pt2ge20' : '((Lepton_pdgId[0] == +13 && Lepton_pdgId[1] == +11) || (Lepton_pdgId[0] == +11 && Lepton_pdgId[1] == +13)) && Lepton_pt[1]>=20',
        # 'SS_CR_plus_pt2lt20'  : '((Lepton_pdgId[0] == -13 && Lepton_pdgId[1] == -11) || (Lepton_pdgId[0] == -11 && Lepton_pdgId[1] == -13)) && Lepton_pt[1]<20',
        # 'SS_CR_minus_pt2lt20' : '((Lepton_pdgId[0] == +13 && Lepton_pdgId[1] == +11) || (Lepton_pdgId[0] == +11 && Lepton_pdgId[1] == +13)) && Lepton_pt[1]<20',
    }
}

# e-e
cuts['hww2l2v_13TeV_WH_SS_ee_2j'] = {
    'expr' : '(Lepton_pdgId[0]*Lepton_pdgId[1] == 11*11) && nLepton==2 && Alt(CleanJet_pt,0,0)>30 && Alt(CleanJet_pt,1,0)>30 && abs(mll-91.2)>15',
    'categories' : {
        'SS_CR_plus_pt2ge20'  : 'Lepton_pdgId[0] == -11 && Lepton_pdgId[1] == -11 && Lepton_pt[1]>=20',
        'SS_CR_minus_pt2ge20' : 'Lepton_pdgId[0] == +11 && Lepton_pdgId[1] == +11 && Lepton_pt[1]>=20',
        # 'SS_CR_plus_pt2lt20'  : 'Lepton_pdgId[0] == -11 && Lepton_pdgId[1] == -11 && Lepton_pt[1]<20',
        # 'SS_CR_minus_pt2lt20' : 'Lepton_pdgId[0] == +11 && Lepton_pdgId[1] == +11 && Lepton_pt[1]<20',
    }
}


## SR 1jet

# mu-mu
cuts['hww2l2v_13TeV_WH_SS_mm_1j'] = {
    'expr' : '(Lepton_pdgId[0]*Lepton_pdgId[1] == 13*13) && nLepton==2 && Alt(CleanJet_pt,0,0)>30 && Alt(CleanJet_pt,1,0)<30',
    'categories' : {
        'SS_CR_plus_pt2ge20'  : 'Lepton_pdgId[0] == -13 && Lepton_pdgId[1] == -13 && Lepton_pt[1]>=20',
        'SS_CR_minus_pt2ge20' : 'Lepton_pdgId[0] == +13 && Lepton_pdgId[1] == +13 && Lepton_pt[1]>=20',
        # 'SS_CR_plus_pt2lt20'  : 'Lepton_pdgId[0] == -13 && Lepton_pdgId[1] == -13 && Lepton_pt[1]<20',
        # 'SS_CR_minus_pt2lt20' : 'Lepton_pdgId[0] == +13 && Lepton_pdgId[1] == +13 && Lepton_pt[1]<20',
    }
}

# mu-e
cuts['hww2l2v_13TeV_WH_SS_em_1j'] = {
    'expr' : '(Lepton_pdgId[0]*Lepton_pdgId[1] == 11*13) && nLepton==2 && Alt(CleanJet_pt,0,0)>30 && Alt(CleanJet_pt,1,0)<30',
    'categories' : {
        'SS_CR_plus_pt2ge20'  : '((Lepton_pdgId[0] == -13 && Lepton_pdgId[1] == -11) || (Lepton_pdgId[0] == -11 && Lepton_pdgId[1] == -13)) && Lepton_pt[1]>=20',
        'SS_CR_minus_pt2ge20' : '((Lepton_pdgId[0] == +13 && Lepton_pdgId[1] == +11) || (Lepton_pdgId[0] == +11 && Lepton_pdgId[1] == +13)) && Lepton_pt[1]>=20',
        # 'SS_CR_plus_pt2lt20'  : '((Lepton_pdgId[0] == -13 && Lepton_pdgId[1] == -11) || (Lepton_pdgId[0] == -11 && Lepton_pdgId[1] == -13)) && Lepton_pt[1]<20',
        # 'SS_CR_minus_pt2lt20' : '((Lepton_pdgId[0] == +13 && Lepton_pdgId[1] == +11) || (Lepton_pdgId[0] == +11 && Lepton_pdgId[1] == +13)) && Lepton_pt[1]<20',
    }
}

# e-e
cuts['hww2l2v_13TeV_WH_SS_ee_1j'] = {
    'expr' : '(Lepton_pdgId[0]*Lepton_pdgId[1] == 11*11) && nLepton==2 && Alt(CleanJet_pt,0,0)>30 && Alt(CleanJet_pt,1,0)<30 && abs(mll-91.2)>15',
    'categories' : {
        'SS_CR_plus_pt2ge20'  : 'Lepton_pdgId[0] == -11 && Lepton_pdgId[1] == -11 && Lepton_pt[1]>=20',
        'SS_CR_minus_pt2ge20' : 'Lepton_pdgId[0] == +11 && Lepton_pdgId[1] == +11 && Lepton_pt[1]>=20',
        # 'SS_CR_plus_pt2lt20'  : 'Lepton_pdgId[0] == -11 && Lepton_pdgId[1] == -11 && Lepton_pt[1]<20',
        # 'SS_CR_minus_pt2lt20' : 'Lepton_pdgId[0] == +11 && Lepton_pdgId[1] == +11 && Lepton_pt[1]<20',
    }
}


## SR 0jet

# mu-mu
cuts['hww2l2v_13TeV_WH_SS_mm_0j'] = {
    'expr' : '(Lepton_pdgId[0]*Lepton_pdgId[1] == 13*13) && nLepton==2 && Alt(CleanJet_pt,0,0)<30',
    'categories' : {
        'SS_CR_plus_pt2ge20'  : 'Lepton_pdgId[0] == -13 && Lepton_pdgId[1] == -13 && Lepton_pt[1]>=20',
        'SS_CR_minus_pt2ge20' : 'Lepton_pdgId[0] == +13 && Lepton_pdgId[1] == +13 && Lepton_pt[1]>=20',
        # 'SS_CR_plus_pt2lt20'  : 'Lepton_pdgId[0] == -13 && Lepton_pdgId[1] == -13 && Lepton_pt[1]<20',
        # 'SS_CR_minus_pt2lt20' : 'Lepton_pdgId[0] == +13 && Lepton_pdgId[1] == +13 && Lepton_pt[1]<20',
    }
}

# mu-e
cuts['hww2l2v_13TeV_WH_SS_em_0j'] = {
    'expr' : '(Lepton_pdgId[0]*Lepton_pdgId[1] == 11*13) && nLepton==2 && Alt(CleanJet_pt,0,0)<30',
    'categories' : {
        'SS_CR_plus_pt2ge20'  : '((Lepton_pdgId[0] == -13 && Lepton_pdgId[1] == -11) || (Lepton_pdgId[0] == -11 && Lepton_pdgId[1] == -13)) && Lepton_pt[1]>=20',
        'SS_CR_minus_pt2ge20' : '((Lepton_pdgId[0] == +13 && Lepton_pdgId[1] == +11) || (Lepton_pdgId[0] == +11 && Lepton_pdgId[1] == +13)) && Lepton_pt[1]>=20',
        # 'SS_CR_plus_pt2lt20'  : '((Lepton_pdgId[0] == -13 && Lepton_pdgId[1] == -11) || (Lepton_pdgId[0] == -11 && Lepton_pdgId[1] == -13)) && Lepton_pt[1]<20',
        # 'SS_CR_minus_pt2lt20' : '((Lepton_pdgId[0] == +13 && Lepton_pdgId[1] == +11) || (Lepton_pdgId[0] == +11 && Lepton_pdgId[1] == +13)) && Lepton_pt[1]<20',
    }
}

# e-e
cuts['hww2l2v_13TeV_WH_SS_ee_0j'] = {
    'expr' : '(Lepton_pdgId[0]*Lepton_pdgId[1] == 11*11) && nLepton==2 && Alt(CleanJet_pt,0,0)<30 && abs(mll-91.2)>15',
    'categories' : {
        'SS_CR_plus_pt2ge20'  : 'Lepton_pdgId[0] == -11 && Lepton_pdgId[1] == -11 && Lepton_pt[1]>=20',
        'SS_CR_minus_pt2ge20' : 'Lepton_pdgId[0] == +11 && Lepton_pdgId[1] == +11 && Lepton_pt[1]>=20',
        # 'SS_CR_plus_pt2lt20'  : 'Lepton_pdgId[0] == -11 && Lepton_pdgId[1] == -11 && Lepton_pt[1]<20',
        # 'SS_CR_minus_pt2lt20' : 'Lepton_pdgId[0] == +11 && Lepton_pdgId[1] == +11 && Lepton_pt[1]<20',
    }
}


# ## SR 3 leptons: only 0 jet bin
# cuts['hww2l2v_13TeV_WH_3l'] = {
#     'expr' : 'nLepton>=3 && Alt(Lepton_pt,3,0)<10 && Alt(CleanJet_pt,0,0)<30 && (WH3l_mOSll[0]<0 || WH3l_mOSll[0]>12) && (WH3l_mOSll[1]<0 || WH3l_mOSll[1]>12) && (WH3l_mOSll[2]<0 || WH3l_mOSll[2]>12)',
#     'categories' : {
#         'sssf_plus_pt2ge20'  : 'WH3l_flagOSSF == 0 && abs(WH3l_chlll) == 1 && Lepton_pdgId[0]*Lepton_pdgId[1]*Lepton_pdgId[2]>0 && Lepton_pt[1]>=20 && Lepton_pt[2]>=15',
#         'sssf_minus_pt2ge20' : 'WH3l_flagOSSF == 0 && abs(WH3l_chlll) == 1 && Lepton_pdgId[0]*Lepton_pdgId[1]*Lepton_pdgId[2]<0 && Lepton_pt[1]>=20 && Lepton_pt[2]>=15',
#         'ossf_plus_pt2ge20'  : 'WH3l_flagOSSF == 1 && abs(WH3l_chlll) == 1 && Lepton_pdgId[0]*Lepton_pdgId[1]*Lepton_pdgId[2]>0 && Lepton_pt[1]>=20 && Lepton_pt[2]>=15 && WH3l_ZVeto > 20 && PuppiMET_pt > 40',
#         'ossf_minus_pt2ge20' : 'WH3l_flagOSSF == 1 && abs(WH3l_chlll) == 1 && Lepton_pdgId[0]*Lepton_pdgId[1]*Lepton_pdgId[2]<0 && Lepton_pt[1]>=20 && Lepton_pt[2]>=15 && WH3l_ZVeto > 20 && PuppiMET_pt > 40',
#     }
# }

# mlljj20_whss:
# inv_mass of: (jet1, jet2, 2*closest_lep_to_jets)
# jets are considered with pT > 20 GeV 

# Definitions of WH3l variables:
# https://github.com/latinos/LatinoAnalysis/blob/76e7c4b93aa5f056c92440d4e8d24e7de749c8fe/NanoGardener/python/modules/l3KinProducer.py
