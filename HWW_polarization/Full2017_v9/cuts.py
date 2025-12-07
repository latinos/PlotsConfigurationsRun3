
# cuts

cuts = {}

_tmp = [
    #'Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
    'Lepton_pt[0] > 25.',
    'Lepton_pt[1] > 10.',
    '(abs(Lepton_pdgId[1]) == 13 || Lepton_pt[1] > 13.)',
    '(nLepton >= 2 && Alt(Lepton_pt,2, 0) < 10.)',
    'ptll>15',
    'mll > 12',
    'CleanJet_VetoMap>0.5'
]

preselections = ' && '.join(_tmp)


cuts['hww2l2v_13TeV_ss'] = {
    'expr': 'bVeto && mll>35 && mpmet<30 && Lepton_pdgId[0]*Lepton_pdgId[1] == 11*13',
    'categories' : {
        'Inc': 'mll>12',
        '0j' : 'Alt(CleanJet_pt,0, 0.0)<30.0',
        '1j' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0',
        '2j' : 'Sum(CleanJet_pt>30.0)==2',
    }
}

#cuts['hww2l2v_13TeV_sr_RF_bkg'] = {
#    'expr': 'sr && mpmet>15 && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
#    'categories' : {
#        '0j' : 'Alt(CleanJet_pt,0, 0.0)<30.0 && (RF_score_0J_Bkg>RF_score_0J_LL && RF_score_0J_Bkg>RF_score_0J_TT)',
#        '1j' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0 && (RF_score_1J_Bkg>RF_score_1J_LL && RF_score_1J_Bkg>RF_score_1J_TT)',
#        '2j_tot': 'Sum(CleanJet_pt>30.0)==2 && D_VBF_QCD<0.5 && ((RF_score_2J_Bkg>RF_score_2J_LL && RF_score_2J_Bkg>RF_score_2J_TT) && (RF_score_VBF_Bkg>RF_score_VBF_LL && RF_score_VBF_Bkg>RF_score_VBF_TT))',
#        '2j' : 'Sum(CleanJet_pt>30.0)==2 && D_VBF_QCD<0.5 && (RF_score_2J_Bkg>RF_score_2J_LL && RF_score_2J_Bkg>RF_score_2J_TT)',
#        '2j_vbf' : 'Sum(CleanJet_pt>30.0)==2 && D_VBF_QCD>0.5 && (RF_score_VBF_Bkg>RF_score_VBF_LL && RF_score_VBF_Bkg>RF_score_VBF_TT)',
#    }
#}
#
#cuts['hww2l2v_13TeV_sr_RF_Signal'] = {
#    'expr': 'sr && mpmet>15 && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
#    'categories' : {
#        '0j_pt2gt20' : 'Alt(CleanJet_pt,0, 0.0)<30.0 && Lepton_pt[1]>=20 && (RF_score_0J_LL>RF_score_0J_Bkg || RF_score_0J_TT>RF_score_0J_Bkg)',
#        '0j_pt2lt20' : 'Alt(CleanJet_pt,0, 0.0)<30.0 && Lepton_pt[1]<20 && (RF_score_0J_LL>RF_score_0J_Bkg || RF_score_0J_TT>RF_score_0J_Bkg)',
#        '1j_pt2gt20' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0 && Lepton_pt[1]>=20 && (RF_score_1J_LL>RF_score_1J_Bkg || RF_score_1J_TT>RF_score_1J_Bkg)',
#        '1j_pt2lt20' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0 && Lepton_pt[1]<20 && (RF_score_1J_LL>RF_score_1J_Bkg || RF_score_1J_TT>RF_score_1J_Bkg)',
#        '2j_tot': 'Sum(CleanJet_pt>30.0)==2 && ((RF_score_2J_LL>RF_score_2J_Bkg || RF_score_2J_TT>RF_score_2J_Bkg) || (RF_score_VBF_LL>RF_score_VBF_Bkg || RF_score_VBF_TT>RF_score_VBF_Bkg))',
#        '2j' : 'Sum(CleanJet_pt>30.0)==2 && D_VBF_QCD<0.5 && (RF_score_2J_LL>RF_score_2J_Bkg || RF_score_2J_TT>RF_score_2J_Bkg)',
#        '2j_vbf' : 'Sum(CleanJet_pt>30.0)==2 && D_VBF_QCD>0.5 && (RF_score_VBF_LL>RF_score_VBF_Bkg || RF_score_VBF_TT>RF_score_VBF_Bkg)',
#    }
#}

if not doSignals:
    cuts['hww2l2v_13TeV_sr_RF02'] = {
        'expr': 'sr && mpmet>15 && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
        'categories' : {
            '0j_pt2gt20' : 'Alt(CleanJet_pt,0, 0.0)<30.0 && Lepton_pt[1]>=20 && RF_score_0J_Bkg<0.2',
            '0j_pt2lt20' : 'Alt(CleanJet_pt,0, 0.0)<30.0 && Lepton_pt[1]<20 && RF_score_0J_Bkg<0.2',
            '1j_pt2gt20' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0 && Lepton_pt[1]>=20 && RF_score_1J_Bkg<0.2',
            '1j_pt2lt20' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0 && Lepton_pt[1]<20 && RF_score_1J_Bkg<0.2',
            '2j_tot': 'Sum(CleanJet_pt>30.0)==2 && (RF_score_2J_Bkg<0.2 || RF_score_VBF_Bkg<0.2)',
            '2j' : 'Sum(CleanJet_pt>30.0)==2 && D_VBF_QCD<0.5 && RF_score_2J_Bkg<0.2',
            '2j_vbf' : 'Sum(CleanJet_pt>30.0)==2 && D_VBF_QCD>0.5 && RF_score_VBF_Bkg<0.2',
        }
    }

cuts['hww2l2v_13TeV_sr'] = {
    'expr': 'sr && mpmet>15 && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
    'categories' : {
        '0j_pt2gt20' : 'Alt(CleanJet_pt,0, 0.0)<30.0 && Lepton_pt[1]>=20',
        '0j_pt2lt20' : 'Alt(CleanJet_pt,0, 0.0)<30.0 && Lepton_pt[1]<20',
        '1j_pt2gt20' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0 && Lepton_pt[1]>=20',
        '1j_pt2lt20' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0 && Lepton_pt[1]<20',
        '2j' : 'Sum(CleanJet_pt>30.0)==2 && D_VBF_QCD<0.5',
        '2j_vbf' : 'Sum(CleanJet_pt>30.0)==2 && D_VBF_QCD>0.5',
    }
}

cuts['hww2l2v_13TeV_top']  = { 
   'expr' : 'topcr && mpmet>15 && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
   'categories' : {
       '0j' : 'Alt(CleanJet_pt,0, 0.0)<30.0',
       '1j' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0',
       '2j' : 'Sum(CleanJet_pt>30.0)==2',
   }
}

cuts['hww2l2v_13TeV_dytt']  = { 
   'expr' : 'dycr && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
   'categories' : { 
       '0j' : 'Alt(CleanJet_pt,0, 0.0)<30.0',
       '1j' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0',
       '2j' : 'Sum(CleanJet_pt>30.0)==2',
   }
}




    
