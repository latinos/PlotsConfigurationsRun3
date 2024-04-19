
# cuts

cuts = {}

_tmp = [
    'Lepton_pt[0] > 25.',
    'Lepton_pt[1] > 10.',
    '(abs(Lepton_pdgId[1]) == 13 || Lepton_pt[1] > 13.)',
    '(nLepton >= 2 && Alt(Lepton_pt,2, 0) < 10.)',
    'ptll>15',
    'mll > 12',
    'CleanJet_VetoMap>0.5'
]

preselections = ' && '.join(_tmp)


'''
cuts['hww2l2v_13TeV_sr_BDT80'] = {
    'expr': 'sr && mpmet>15 && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
    'categories' : {
        '0j' : 'Alt(CleanJet_pt,0, 0.0)<30.0 && BDTG4D3_0J>0.3',
        '1j' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0 && BDTG4D3_1J>0.4',
        '2j' : 'Sum(CleanJet_pt>30.0)==2 && D_VBF_QCD<0.25 && BDTG4D3_2J>0.3',
        '2j_vbf' : 'Sum(CleanJet_pt>30.0)==2 && D_VBF_QCD>0.25 && BDTG4D3_VBF>0.6',
    }
}

cuts['hww2l2v_13TeV_sr_BDT10'] = {
    'expr': 'sr && mpmet>15 && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
    'categories' : {
        '0j' : 'Alt(CleanJet_pt,0, 0.0)<30.0 && BDTG4D3_0J>0.6',
        '1j' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0 && BDTG4D3_1J>0.5',
        '2j' : 'Sum(CleanJet_pt>30.0)==2 && D_VBF_QCD<0.25 && BDTG4D3_2J>0.5',
        '2j_vbf' : 'Sum(CleanJet_pt>30.0)==2 && D_VBF_QCD>0.25 && BDTG4D3_VBF>0.8',
    }
}
'''

cuts['hww2l2v_13TeV_sr_RF_bkg'] = {
    'expr': 'sr && mpmet>15 && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
    'categories' : {
        '0j' : 'Alt(CleanJet_pt,0, 0.0)<30.0 && (RF_score_0J_Bkg>RF_score_0J_LL && RF_score_0J_Bkg>RF_score_0J_TT)',
        '1j' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0 && (RF_score_1J_Bkg>RF_score_1J_LL && RF_score_1J_Bkg>RF_score_1J_TT)',
        '2j' : 'Sum(CleanJet_pt>30.0)==2 && D_VBF_QCD<0.5 && (RF_score_2J_Bkg>RF_score_2J_LL && RF_score_2J_Bkg>RF_score_2J_TT)',
        '2j_vbf' : 'Sum(CleanJet_pt>30.0)==2 && D_VBF_QCD>0.5 && (RF_score_VBF_Bkg>RF_score_VBF_LL && RF_score_VBF_Bkg>RF_score_VBF_TT)',
    }
}

cuts['hww2l2v_13TeV_sr_RF_Signal'] = {
    'expr': 'sr && mpmet>15 && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
    'categories' : {
        '0j' : 'Alt(CleanJet_pt,0, 0.0)<30.0 && (RF_score_0J_LL>RF_score_0J_Bkg || RF_score_0J_TT>RF_score_0J_Bkg)',
        '1j' : 'Alt(CleanJet_pt,0, 0.0)>30.0 && Alt(CleanJet_pt,1, 0.0)<30.0 && (RF_score_1J_LL>RF_score_1J_Bkg || RF_score_1J_TT>RF_score_1J_Bkg)',
        '2j' : 'Sum(CleanJet_pt>30.0)==2 && D_VBF_QCD<0.5 && (RF_score_2J_LL>RF_score_2J_Bkg || RF_score_2J_TT>RF_score_2J_Bkg)',
        '2j_vbf' : 'Sum(CleanJet_pt>30.0)==2 && D_VBF_QCD>0.5 && (RF_score_VBF_LL>RF_score_VBF_Bkg || RF_score_VBF_TT>RF_score_VBF_Bkg)',
    }
}

cuts['hww2l2v_13TeV_top']  = { 
   'expr' : 'topcr && mpmet>15 && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
   'categories' : {
       '0j' : 'zeroJet',
       '1j' : 'oneJet',
       '2j' : 'Sum(CleanJet_pt>30.0)==2',
   }
}

cuts['hww2l2v_13TeV_dytt']  = { 
   'expr' : 'dycr && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
   'categories' : { 
       '0j' : 'zeroJet',
       '1j' : 'oneJet',
       '2j' : 'Sum(CleanJet_pt>30.0)==2',
   }
}

#cuts['hww2l2v_13TeV_WW'] = {
#    'expr' : 'sr && mpmet>15 && Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13',
#    'categories' : {
#        '0j' : 'zeroJet && BDTG4D3_0J<-0.3',
#        '1j' : 'oneJet && BDTG4D3_1J<-0.1',
#        '2j' : 'Sum(CleanJet_pt>30.0)==2 && BDTG4D3_VBF<-0.4 && BDTG4D3_2J<-0.5',
#    }
#}


