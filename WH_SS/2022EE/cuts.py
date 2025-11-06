cuts = {}

# Preselections - applied to all the cuts
preselections = 'Lepton_pt[0]>25 \
&& Lepton_pt[1]>20 \
&& bVeto \
&& PuppiMET_pt>30 \
&& mll>12'

cuts['preselections'] = 'Lepton_pt[0]>25 && Lepton_pt[1]>20 && bVeto && PuppiMET_pt>30 && mll>12'

cuts['whss_2l_uu_incl'] = 'nLepton==2 && (Lepton_pdgId[0]*Lepton_pdgId[1] == 13*13) && abs(Lepton_eta[0] - Lepton_eta[1])<2.0'

cuts['whss_2l_uu'] = {
    'expr' : 'nLepton==2 && (Lepton_pdgId[0]*Lepton_pdgId[1] == 13*13) && abs(Lepton_eta[0] - Lepton_eta[1])<2.0',
    'categories' : {
        '0j' : 'zeroJet',
        '1j' : 'oneJet && Alt(CleanJet_pt,1,0)<30',
        '2j' : 'multiJet && mjj<100',
    }
}
