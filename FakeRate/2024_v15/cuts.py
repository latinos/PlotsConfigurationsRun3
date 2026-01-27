# jet_pt_thresholds = [10, 15, 20, 25, 30, 35, 40, 45]
jet_pt_thresholds = [20, 30, 40]

# cuts
cuts = {}

preselections = 'nLepton > 0 \
              && ((abs(Lepton_pdgId[0]) == 11 && Lepton_pt[0] > 13 && abs(Lepton_eta[0]) < 2.5)  \
              ||  (abs(Lepton_pdgId[0]) == 13 && Lepton_pt[0] > 10 && abs(Lepton_eta[0]) < 2.4)) \
'

# Prompt rate selections
cuts['Zpeak_PR_loose'] = {
    'expr'       : 'nLepton > 1 && Lepton_pt[0] > 32 && LepWPCut1l && Lepton_pt[1] > 10 && mll > 76 && mll < 106 && PuppiMET_pt < 20',
    'categories' : {
        'ele'  : 'Lepton_pdgId[0]*Lepton_pdgId[1] == -121',
        'muon' : 'Lepton_pdgId[0]*Lepton_pdgId[1] == -169',
    }
}

# Prompt rate selections
cuts['Zpeak_PR_tight'] = {
    'expr'       : 'nLepton > 1 && Lepton_pt[0] > 32 && Lepton_pt[1] > 10 && LepWPCut2l && mll > 76 && mll < 106 && PuppiMET_pt < 20',
    'categories' : {
        'ele'  : 'Lepton_pdgId[0]*Lepton_pdgId[1] == -121',
        'muon' : 'Lepton_pdgId[0]*Lepton_pdgId[1] == -169',
    }
}


for jet_pt_threshold in jet_pt_thresholds:

    ##########################
    # Loose leptons selections
    ##########################
    
    # QCD region
    cuts[f'QCD_loose_jet_pt_{jet_pt_threshold}'] = {
        'expr'    : f'nLepton == 1 && mtw1 < 20 && PuppiMET_pt < 20 && drlj_{jet_pt_threshold} > 1',
        'categories' : {
            'ele'  : 'abs(Lepton_pdgId[0]) == 11',
            'muon' : 'abs(Lepton_pdgId[0]) == 13',
        }
    }

    # Z-peak
    cuts[f'Zpeak_loose_jet_pt_{jet_pt_threshold}'] = {
        'expr'       : f'nLepton > 1 && Lepton_pt[0] > 25 && Lepton_pt[1] > 10 && PuppiMET_pt < 20 && mll > 60 && mll < 120',
        'categories' : {
            'ele'  : 'Lepton_pdgId[0]*Lepton_pdgId[1] == -121 && Lepton_pt[1] > 13',
            'muon' : 'Lepton_pdgId[0]*Lepton_pdgId[1] == -169',
        }
    }

    # WJets region
    cuts[f'WJets_loose_jet_pt_{jet_pt_threshold}'] = {
        'expr'       : f'nLepton == 1 && mtw1 > 20 && PuppiMET_pt < 20 && drlj_{jet_pt_threshold} > 1',
        'categories' : {
            'ele'  : 'abs(Lepton_pdgId[0]) == 11',
            'muon' : 'abs(Lepton_pdgId[0]) == 13',
        }
    }

    ##########################
    # Tight leptons selections
    ##########################

    # QCD region
    cuts[f'QCD_tight_jet_pt_{jet_pt_threshold}'] = {
        'expr'    : f'nLepton == 1 && mtw1 < 20 && PuppiMET_pt < 20 && drlj_{jet_pt_threshold} > 1 && LepWPCut1l',
        'categories' : {
            'ele'  : 'abs(Lepton_pdgId[0]) == 11',
            'muon' : 'abs(Lepton_pdgId[0]) == 13',
        }
    }

    # Z-peak
    cuts[f'Zpeak_tight_jet_pt_{jet_pt_threshold}'] = {
        'expr'    : f'nLepton > 1 && PuppiMET_pt < 20 && mll > 60 && mll < 120 && LepWPCut1l',
        'categories' : {
            'ele'  : 'Lepton_pdgId[0]*Lepton_pdgId[1] == -121 && Lepton_pt[1] > 13',
            'muon' : 'Lepton_pdgId[0]*Lepton_pdgId[1] == -169',
        }
    }

    # WJets region
    cuts[f'WJets_tight_jet_pt_{jet_pt_threshold}'] = {
        'expr'    : f'nLepton == 1 && mtw1 > 20 && PuppiMET_pt < 20 && drlj_{jet_pt_threshold} > 1 && LepWPCut1l',
        'categories' : {
            'ele'  : 'abs(Lepton_pdgId[0]) == 11',
            'muon' : 'abs(Lepton_pdgId[0]) == 13',
        }
    }
