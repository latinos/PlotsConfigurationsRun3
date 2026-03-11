cuts = {}

# Preselections - applied to all the cuts
preselections = ' nLepton == 2 \
&& Lepton_pt[0]>25 \
&& Lepton_pt[1]>20 \
&& abs(Lepton_eta[0])<2.5 \
&& abs(Lepton_eta[1])<2.5 \
&& bVeto \
&& noJetInHorn'

cuts['ss_2l_ee_dy'] = '(Lepton_pdgId[0]*Lepton_pdgId[1]==11*11) && abs(mll-91.2)<15'

cuts['os_2l_ee_dy'] = '(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*11) && abs(mll-91.2)<15'

cuts['ss_2l_ee_sr'] = '(Lepton_pdgId[0]*Lepton_pdgId[1]==11*11)'

# cuts['ss_2l_ee'] = {
#     'expr' : '(Lepton_pdgId[0]*Lepton_pdgId[1] == 11*11)',
#     'categories' : {
#         '0j' : 'zeroJet',
#         '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
#         '2j' : 'multiJet',
#     }
# }

# cuts['os_2l_ee'] = {
#     'expr' : '(Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11)',
#     'categories' : {
#         '0j' : 'zeroJet',
#         '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
#         '2j' : 'multiJet',
#     }
# }

# lep_pt_thresholds = [20, 30, 50, 100, 200]
# lep_eta_thresholds = [0, 1.4, 2.5]

# for lep_eta_threshold in lep_eta_thresholds:
#     cuts[f'ss_2l_eta_{lep_eta_threshold}'] = {
#         'expr' : f'(Lepton_pdgId[0]*Lepton_pdgId[1] == 11*11) && Lepton_pt[0] > {lep_pt_threshold} && Lepton_eta[0] > {lep_eta_threshold}'
#     }

# cuts['ss_2l_ee_dy_pt1_25_60'] = '(Lepton_pdgId[0]*Lepton_pdgId[1]==11*11) && abs(mll-91.2)<15 && Lepton_pt[0]>25 && Lepton_pt[0]<60'
# cuts['ss_2l_ee_dy_pt1_60_200'] = '(Lepton_pdgId[0]*Lepton_pdgId[1]==11*11) && abs(mll-91.2)<15 && Lepton_pt[0]>60 && Lepton_pt[0]<200'

# cuts['os_2l_ee_dy_pt1_25_60'] = '(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*11) && abs(mll-91.2)<15 && Lepton_pt[0]>25 && Lepton_pt[0]<60'
# cuts['os_2l_ee_dy_pt1_60_200'] = '(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*11) && abs(mll-91.2)<15 && Lepton_pt[0]>60 && Lepton_pt[0]<200'

# cuts['ss_2l_ee_dy_eta1_0_1p4'] = '(Lepton_pdgId[0]*Lepton_pdgId[1]==11*11) && abs(mll-91.2)<15 && abs(Lepton_eta[0])<1.4'
# cuts['ss_2l_ee_dy_eta1_1p4_2p5'] = '(Lepton_pdgId[0]*Lepton_pdgId[1]==11*11) && abs(mll-91.2)<15 && abs(Lepton_eta[0])>1.4' 

# cuts['ss_2l_ee_dy_eta2_0_1p4'] = '(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*11) && abs(mll-91.2)<15 && abs(Lepton_eta[0])<1.4'
# cuts['ss_2l_ee_dy_eta2_1p4_2p5'] = '(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*11) && abs(mll-91.2)<15 && abs(Lepton_eta[0])>1.4' 

# cuts['os_2l_ee'] = {
#     'expr' : 'nLepton == 2 && (Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11) && abs(mll-91.2) < 15',
#     'categories' : {
#         '0j' : 'zeroJet',
#         '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
#         '2j' : 'multiJet && mjj<100',
#     }
# }

# cuts['val_2l_ee'] = {
#     'expr' : 'nLepton == 2 && (Lepton_pdgId[0]*Lepton_pdgId[1] == 11*11) && Lepton_pt[0]>25 && Lepton_pt[1]>20',
#     'categories' : {
#         '0j' : 'zeroJet',
#         '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
#         '2j' : 'multiJet && mjj<100',
#     }
# }
