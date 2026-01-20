cuts = {}

#
# 2 leptons: pt> 25 GeV and 13 GeV
# 2 jets with pT>30 GeV
#

preselections = '          Lepton_pt[0]>25 \
                        && Lepton_pt[1]>13 \
                        && Alt(Lepton_pt, 2, 0) < 10 \
                        && abs(Lepton_eta[0])<2.5 && abs(Lepton_eta[1])<2.5 \
                        && ((Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11) || (Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13)) \
                        && Alt(CleanJet_pt, 1, 0)>30 \
                        && abs(CleanJet_eta[0])<4.7 && abs(CleanJet_eta[1])<4.7 \
                        && mll > 50 \
                        '

cuts['topcr'] = {
    'expr': 'abs(mll-91)>15 && bReq',
    'categories':{
        'ee': '(Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11)',
        'mm': '(Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13)',
    }
}

#    cuts['vvcr'] = {
#        'expr': 'abs(mll-91)>15 && bVeto', 
#        'categories':{
#            'ee': '(Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11)',
#            'mm': '(Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13)',
#        }
#    }


cuts['dycr'] = {
    'expr': 'abs(mll-91)<15 && bVeto',
    'categories':{
        'ee': '(Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11)',
        'mm': '(Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13)',
    }
} 

cuts['sr'] = {
    'expr': 'abs(mll-91)<15 && bVeto && Jet_qgl[0]<0.5 && Jet_qgl[1]<0.5',
    'categories':{
        'ee': '(Lepton_pdgId[0]*Lepton_pdgId[1] == -11*11)',
        'mm': '(Lepton_pdgId[0]*Lepton_pdgId[1] == -13*13)',
    }
}
