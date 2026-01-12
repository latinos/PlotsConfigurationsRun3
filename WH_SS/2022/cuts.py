cuts = {}

# Preselections - applied to all the cuts
preselections = 'Lepton_pt[0]>15 \
&& Lepton_pt[1]>15 \
&& (nLepton >= 2 && Alt(Lepton_pt,2,0) < 10) \
&& abs(Lepton_eta[0])<2.5 \
&& abs(Lepton_eta[1])<2.5 \
&& bVeto \
&& noJetInHorn \
&& abs(mll-91.2)<15'

cuts['ss_2l_ee_incl'] = '(Lepton_pdgId[0]*Lepton_pdgId[1]==11*11)'

cuts['os_2l_ee_incl'] = '(Lepton_pdgId[0]*Lepton_pdgId[1]==-11*11)'

cuts['ss_2l_ee'] = {
    'expr' : '(Lepton_pdgId[0]*Lepton_pdgId[1] == 11*11)',
    'categories' : {
        '0j' : 'zeroJet',
        '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
        '2j' : 'multiJet',
    }
}

cuts['os_2l_ee'] = {
    'expr' : '(Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11)',
    'categories' : {
        '0j' : 'zeroJet',
        '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
        '2j' : 'multiJet',
    }
}

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
