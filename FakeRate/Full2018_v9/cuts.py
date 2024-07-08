cuts = {}

# cuts
preselections = 'nLepton > 0'

##########################
# Loose leptons selections
##########################

# QCD region
cuts['QCD'] = {
    'expr'    : 'nLepton == 1 && mtw1 < 20 && PuppiMET_pt < 20 && nCleanJet > 0 && bVeto && abs(CleanJet_eta[0]) < 2.4 && dRl1j1 > 1',
    'categories' : {
        'ele_high_pt_0j'  : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] > 25  && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && zeroJet',
        'ele_high_pt_1j'  : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] > 25  && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && oneJet',
        'ele_high_pt_2j'  : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] > 25  && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && multiJet',
        'ele_low_pt_0j'   : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] <= 25 && HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && zeroJet',
        'ele_low_pt_1j'   : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] <= 25 && HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && oneJet',
        'ele_low_pt_2j'   : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] <= 25 && HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && multiJet',
        'muon_high_pt_0j' : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] > 20  && HLT_Mu17_TrkIsoVVL > 0.5 && zeroJet',
        'muon_high_pt_1j' : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] > 20  && HLT_Mu17_TrkIsoVVL > 0.5 && oneJet',
        'muon_high_pt_2j' : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] > 20  && HLT_Mu17_TrkIsoVVL > 0.5 && multiJet',
        'muon_low_pt_0j'  : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] <= 20 && HLT_Mu8_TrkIsoVVL  > 0.5 && zeroJet', 
        'muon_low_pt_1j'  : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] <= 20 && HLT_Mu8_TrkIsoVVL  > 0.5 && oneJet',  
        'muon_low_pt_2j'  : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] <= 20 && HLT_Mu8_TrkIsoVVL  > 0.5 && multiJet',
    }
}

# Z-peak
cuts['Zpeak'] = {
    'expr'    : 'nLepton > 1 && PuppiMET_pt < 20 && mll > 20 && bVeto',
    'categories' : {
        'ele_high_pt_0j'  : 'abs(Lepton_pdgId[0]) == 11 && abs(Lepton_pdgId[1]) == 11 && Lepton_pt[0] > 25  && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && zeroJet', 
        'ele_high_pt_1j'  : 'abs(Lepton_pdgId[0]) == 11 && abs(Lepton_pdgId[1]) == 11 && Lepton_pt[0] > 25  && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && oneJet',  
        'ele_high_pt_2j'  : 'abs(Lepton_pdgId[0]) == 11 && abs(Lepton_pdgId[1]) == 11 && Lepton_pt[0] > 25  && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && multiJet',
        'ele_low_pt_0j'   : 'abs(Lepton_pdgId[0]) == 11 && abs(Lepton_pdgId[1]) == 11 && Lepton_pt[0] <= 25 && HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && zeroJet', 
        'ele_low_pt_1j'   : 'abs(Lepton_pdgId[0]) == 11 && abs(Lepton_pdgId[1]) == 11 && Lepton_pt[0] <= 25 && HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && oneJet',  
        'ele_low_pt_2j'   : 'abs(Lepton_pdgId[0]) == 11 && abs(Lepton_pdgId[1]) == 11 && Lepton_pt[0] <= 25 && HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && multiJet',
        'muon_high_pt_0j' : 'abs(Lepton_pdgId[0]) == 13 && abs(Lepton_pdgId[1]) == 13 && Lepton_pt[0] > 20  && HLT_Mu17_TrkIsoVVL > 0.5 && zeroJet', 
        'muon_high_pt_1j' : 'abs(Lepton_pdgId[0]) == 13 && abs(Lepton_pdgId[1]) == 13 && Lepton_pt[0] > 20  && HLT_Mu17_TrkIsoVVL > 0.5 && oneJet',  
        'muon_high_pt_2j' : 'abs(Lepton_pdgId[0]) == 13 && abs(Lepton_pdgId[1]) == 13 && Lepton_pt[0] > 20  && HLT_Mu17_TrkIsoVVL > 0.5 && multiJet',
        'muon_low_pt_0j'  : 'abs(Lepton_pdgId[0]) == 13 && abs(Lepton_pdgId[1]) == 13 && Lepton_pt[0] <= 20 && HLT_Mu8_TrkIsoVVL  > 0.5 && zeroJet', 
        'muon_low_pt_1j'  : 'abs(Lepton_pdgId[0]) == 13 && abs(Lepton_pdgId[1]) == 13 && Lepton_pt[0] <= 20 && HLT_Mu8_TrkIsoVVL  > 0.5 && oneJet',  
        'muon_low_pt_2j'  : 'abs(Lepton_pdgId[0]) == 13 && abs(Lepton_pdgId[1]) == 13 && Lepton_pt[0] <= 20 && HLT_Mu8_TrkIsoVVL  > 0.5 && multiJet',
    }
}

# Top region
cuts['Top'] = {
    'expr'    : 'nLepton == 1 && mtw1 < 20 && PuppiMET_pt < 20 && nCleanJet > 0 && bReq && abs(CleanJet_eta[0]) < 2.4',
    'categories' : {
        'ele_high_pt_0j'  : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] > 25  && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && zeroJet', 
        'ele_high_pt_1j'  : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] > 25  && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && oneJet',  
        'ele_high_pt_2j'  : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] > 25  && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && multiJet',
        'ele_low_pt_0j'   : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] <= 25 && HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && zeroJet', 
        'ele_low_pt_1j'   : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] <= 25 && HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && oneJet',  
        'ele_low_pt_2j'   : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] <= 25 && HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && multiJet',
        'muon_high_pt_0j' : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] > 20  && HLT_Mu17_TrkIsoVVL > 0.5 && zeroJet', 
        'muon_high_pt_1j' : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] > 20  && HLT_Mu17_TrkIsoVVL > 0.5 && oneJet',  
        'muon_high_pt_2j' : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] > 20  && HLT_Mu17_TrkIsoVVL > 0.5 && multiJet',
        'muon_low_pt_0j'  : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] <= 20 && HLT_Mu8_TrkIsoVVL  > 0.5 && zeroJet', 
        'muon_low_pt_1j'  : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] <= 20 && HLT_Mu8_TrkIsoVVL  > 0.5 && oneJet',  
        'muon_low_pt_2j'  : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] <= 20 && HLT_Mu8_TrkIsoVVL  > 0.5 && multiJet',
    }
}

# WJets region
cuts['WJets'] = {
    'expr'    : 'nLepton == 1 && mtw1 > 20 && PuppiMET_pt < 20 && nCleanJet > 0 && bVeto && abs(CleanJet_eta[0]) < 2.4 && dRl1j1 > 1',
    'categories' : {
        'ele_high_pt_0j'  : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] > 25  && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && zeroJet', 
        'ele_high_pt_1j'  : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] > 25  && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && oneJet',  
        'ele_high_pt_2j'  : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] > 25  && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && multiJet',
        'ele_low_pt_0j'   : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] <= 25 && HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && zeroJet', 
        'ele_low_pt_1j'   : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] <= 25 && HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && oneJet',  
        'ele_low_pt_2j'   : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] <= 25 && HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && multiJet',
        'muon_high_pt_0j' : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] > 20  && HLT_Mu17_TrkIsoVVL > 0.5 && zeroJet', 
        'muon_high_pt_1j' : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] > 20  && HLT_Mu17_TrkIsoVVL > 0.5 && oneJet',  
        'muon_high_pt_2j' : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] > 20  && HLT_Mu17_TrkIsoVVL > 0.5 && multiJet',
        'muon_low_pt_0j'  : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] <= 20 && HLT_Mu8_TrkIsoVVL  > 0.5 && zeroJet', 
        'muon_low_pt_1j'  : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] <= 20 && HLT_Mu8_TrkIsoVVL  > 0.5 && oneJet',  
        'muon_low_pt_2j'  : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] <= 20 && HLT_Mu8_TrkIsoVVL  > 0.5 && multiJet',
    }
}

##########################
# Tight leptons selections
##########################

# QCD region
cuts['QCD'] = {
    'expr'    : 'nLepton == 1 && mtw1 < 20 && PuppiMET_pt < 20 && nCleanJet > 0 && bVeto && abs(CleanJet_eta[0]) < 2.4 && dRl1j1 > 1 && LepWPCut',
    'categories' : {
        'ele_high_pt_0j'  : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] > 25  && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && zeroJet',
        'ele_high_pt_1j'  : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] > 25  && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && oneJet',
        'ele_high_pt_2j'  : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] > 25  && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && multiJet',
        'ele_low_pt_0j'   : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] <= 25 && HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && zeroJet',
        'ele_low_pt_1j'   : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] <= 25 && HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && oneJet',
        'ele_low_pt_2j'   : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] <= 25 && HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && multiJet',
        'muon_high_pt_0j' : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] > 20  && HLT_Mu17_TrkIsoVVL > 0.5 && zeroJet',
        'muon_high_pt_1j' : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] > 20  && HLT_Mu17_TrkIsoVVL > 0.5 && oneJet',
        'muon_high_pt_2j' : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] > 20  && HLT_Mu17_TrkIsoVVL > 0.5 && multiJet',
        'muon_low_pt_0j'  : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] <= 20 && HLT_Mu8_TrkIsoVVL  > 0.5 && zeroJet', 
        'muon_low_pt_1j'  : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] <= 20 && HLT_Mu8_TrkIsoVVL  > 0.5 && oneJet',  
        'muon_low_pt_2j'  : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] <= 20 && HLT_Mu8_TrkIsoVVL  > 0.5 && multiJet',
    }
}

# Z-peak
cuts['Zpeak'] = {
    'expr'    : 'nLepton > 1 && PuppiMET_pt < 20 && mll > 20 && bVeto && LepWPCut',
    'categories' : {
        'ele_high_pt_0j'  : 'abs(Lepton_pdgId[0]) == 11 && abs(Lepton_pdgId[1]) == 11 && Lepton_pt[0] > 25  && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && zeroJet', 
        'ele_high_pt_1j'  : 'abs(Lepton_pdgId[0]) == 11 && abs(Lepton_pdgId[1]) == 11 && Lepton_pt[0] > 25  && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && oneJet',  
        'ele_high_pt_2j'  : 'abs(Lepton_pdgId[0]) == 11 && abs(Lepton_pdgId[1]) == 11 && Lepton_pt[0] > 25  && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && multiJet',
        'ele_low_pt_0j'   : 'abs(Lepton_pdgId[0]) == 11 && abs(Lepton_pdgId[1]) == 11 && Lepton_pt[0] <= 25 && HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && zeroJet', 
        'ele_low_pt_1j'   : 'abs(Lepton_pdgId[0]) == 11 && abs(Lepton_pdgId[1]) == 11 && Lepton_pt[0] <= 25 && HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && oneJet',  
        'ele_low_pt_2j'   : 'abs(Lepton_pdgId[0]) == 11 && abs(Lepton_pdgId[1]) == 11 && Lepton_pt[0] <= 25 && HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && multiJet',
        'muon_high_pt_0j' : 'abs(Lepton_pdgId[0]) == 13 && abs(Lepton_pdgId[1]) == 13 && Lepton_pt[0] > 20  && HLT_Mu17_TrkIsoVVL > 0.5 && zeroJet', 
        'muon_high_pt_1j' : 'abs(Lepton_pdgId[0]) == 13 && abs(Lepton_pdgId[1]) == 13 && Lepton_pt[0] > 20  && HLT_Mu17_TrkIsoVVL > 0.5 && oneJet',  
        'muon_high_pt_2j' : 'abs(Lepton_pdgId[0]) == 13 && abs(Lepton_pdgId[1]) == 13 && Lepton_pt[0] > 20  && HLT_Mu17_TrkIsoVVL > 0.5 && multiJet',
        'muon_low_pt_0j'  : 'abs(Lepton_pdgId[0]) == 13 && abs(Lepton_pdgId[1]) == 13 && Lepton_pt[0] <= 20 && HLT_Mu8_TrkIsoVVL  > 0.5 && zeroJet', 
        'muon_low_pt_1j'  : 'abs(Lepton_pdgId[0]) == 13 && abs(Lepton_pdgId[1]) == 13 && Lepton_pt[0] <= 20 && HLT_Mu8_TrkIsoVVL  > 0.5 && oneJet',  
        'muon_low_pt_2j'  : 'abs(Lepton_pdgId[0]) == 13 && abs(Lepton_pdgId[1]) == 13 && Lepton_pt[0] <= 20 && HLT_Mu8_TrkIsoVVL  > 0.5 && multiJet',
    }
}

# Top region
cuts['Top'] = {
    'expr'    : 'nLepton == 1 && mtw1 < 20 && PuppiMET_pt < 20 && nCleanJet > 0 && bReq && abs(CleanJet_eta[0]) < 2.4 && LepWPCut',
    'categories' : {
        'ele_high_pt_0j'  : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] > 25  && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && zeroJet', 
        'ele_high_pt_1j'  : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] > 25  && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && oneJet',  
        'ele_high_pt_2j'  : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] > 25  && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && multiJet',
        'ele_low_pt_0j'   : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] <= 25 && HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && zeroJet', 
        'ele_low_pt_1j'   : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] <= 25 && HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && oneJet',  
        'ele_low_pt_2j'   : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] <= 25 && HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && multiJet',
        'muon_high_pt_0j' : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] > 20  && HLT_Mu17_TrkIsoVVL > 0.5 && zeroJet', 
        'muon_high_pt_1j' : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] > 20  && HLT_Mu17_TrkIsoVVL > 0.5 && oneJet',  
        'muon_high_pt_2j' : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] > 20  && HLT_Mu17_TrkIsoVVL > 0.5 && multiJet',
        'muon_low_pt_0j'  : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] <= 20 && HLT_Mu8_TrkIsoVVL  > 0.5 && zeroJet', 
        'muon_low_pt_1j'  : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] <= 20 && HLT_Mu8_TrkIsoVVL  > 0.5 && oneJet',  
        'muon_low_pt_2j'  : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] <= 20 && HLT_Mu8_TrkIsoVVL  > 0.5 && multiJet',
    }
}

# WJets region
cuts['WJets'] = {
    'expr'    : 'nLepton == 1 && mtw1 > 20 && PuppiMET_pt < 20 && nCleanJet > 0 && bVeto && abs(CleanJet_eta[0]) < 2.4 && dRl1j1 > 1 && LepWPCut',
    'categories' : {
        'ele_high_pt_0j'  : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] > 25  && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && zeroJet', 
        'ele_high_pt_1j'  : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] > 25  && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && oneJet',  
        'ele_high_pt_2j'  : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] > 25  && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && multiJet',
        'ele_low_pt_0j'   : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] <= 25 && HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && zeroJet', 
        'ele_low_pt_1j'   : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] <= 25 && HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && oneJet',  
        'ele_low_pt_2j'   : 'abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] <= 25 && HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5 && multiJet',
        'muon_high_pt_0j' : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] > 20  && HLT_Mu17_TrkIsoVVL > 0.5 && zeroJet', 
        'muon_high_pt_1j' : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] > 20  && HLT_Mu17_TrkIsoVVL > 0.5 && oneJet',  
        'muon_high_pt_2j' : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] > 20  && HLT_Mu17_TrkIsoVVL > 0.5 && multiJet',
        'muon_low_pt_0j'  : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] <= 20 && HLT_Mu8_TrkIsoVVL  > 0.5 && zeroJet', 
        'muon_low_pt_1j'  : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] <= 20 && HLT_Mu8_TrkIsoVVL  > 0.5 && oneJet',  
        'muon_low_pt_2j'  : 'abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] <= 20 && HLT_Mu8_TrkIsoVVL  > 0.5 && multiJet',
    }
}
