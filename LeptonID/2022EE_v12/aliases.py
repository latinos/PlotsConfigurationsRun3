import os
import copy
import inspect

# /afs/cern.ch/user/n/ntrevisa/work/latinos/Run3/PlotsConfigurationsRun3/LeptonID/2022EE_v12
configurations = os.path.realpath(inspect.getfile(inspect.currentframe())) # this file
configurations = os.path.dirname(configurations) # 2022EE_v12
configurations = os.path.dirname(configurations) # LeptonID

aliases = {}
aliases = OrderedDict()

mc     = [skey for skey in samples if skey not in ('Fake', 'DATA', 'Dyemb', 'DATA_EG', 'DATA_Mu', 'DATA_EMu', 'Fake_EG', 'Fake_Mu', 'Fake_EMu')]
mc_emb = [skey for skey in samples if skey not in ('Fake', 'DATA', 'DATA_Mu', 'DATA_EMu', 'Fake_EG', 'Fake_Mu', 'Fake_EMu')]

#############################
# Evaluate BDT discriminant #
#############################
aliases['Lepton_ttHMVA_Run3'] = {
    'linesToAdd'     : [f'#include "{configurations}/macros/ttH_MVA_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.Declare('ttH_MVA_reader ttHMVA = ttH_MVA_reader(\"BDTG\",\"{configurations}/data/Electron-mvaTTH.2022EE.weights_mvaISO.xml\",\"BDTG\",\"{configurations}/data/Muon-mvaTTH.2022EE.weights.xml\");')"],
    'expr'           : 'ttHMVA(nLepton,Lepton_pdgId,Lepton_electronIdx,Electron_jetIdx,Electron_pt,Electron_eta,Electron_pfRelIso03_all,Electron_miniPFRelIso_chg,Electron_miniPFRelIso_all,Electron_jetNDauCharged,Electron_jetPtRelv2,Electron_jetRelIso,Jet_btagDeepFlavB,Electron_sip3d,Electron_dxy,Electron_dz,Electron_mvaIso,Lepton_muonIdx,Muon_jetIdx,Muon_pt,Muon_eta,Muon_pfRelIso03_all,Muon_miniPFRelIso_chg,Muon_miniPFRelIso_all,Muon_jetNDauCharged,Muon_jetPtRelv2,Muon_jetRelIso,Muon_sip3d,Muon_dxy,Muon_dz,Muon_segmentComp)',
}

# aliases['Lepton_hwwMVA_Run3'] = {
#     'linesToAdd'     : [f'#include "{configurations}/macros/hww_MVA_reader_class.cc"'],
#     'linesToProcess' : [f"ROOT.gInterpreter.Declare('hww_MVA_reader hwwMVA = hww_MVA_reader(\"BDTG\",\"{configurations}/data/random_forest_xgboost_electron_MVA-HWW_simple.xml\",\"BDTG\",\"{configurations}/data/random_forest_xgboost_muon_MVA-HWW_simple.xml\");')"],
#     'expr'           : 'ttHMVA(nLepton,Lepton_pdgId,Lepton_electronIdx,Electron_jetIdx,Electron_pt,Electron_eta,Electron_pfRelIso03_all,Electron_miniPFRelIso_chg,Electron_miniPFRelIso_all,Electron_jetNDauCharged,Electron_jetPtRelv2,Electron_jetRelIso,Jet_btagDeepFlavB,Electron_sip3d,Electron_dxy,Electron_dz,Electron_mvaIso,Electron_lostHits,Electron_scEtOverPt,Electron_r9,Electron_sieie,Electron_hoe,Electron_eInvMinusPInv,Electron_dr03TkSumPt,Lepton_muonIdx,Muon_jetIdx,Muon_pt,Muon_eta,Muon_pfRelIso03_all,Muon_miniPFRelIso_chg,Muon_miniPFRelIso_all,Muon_jetNDauCharged,Muon_jetPtRelv2,Muon_jetRelIso,Muon_sip3d,Muon_dxy,Muon_dz,Muon_segmentComp,Muon_nStations,Muon_nTrackerLayers,Muon_highPurity,Muon_bsConstrainedChi2,Muon_tkRelIso)',
# }


###############################
# Define different lepton IDs #
###############################

### Dumb Selections:
#
# - ele_wp90iso
#
# - mu_cut_TightID_POG
# - mu_cut_MediumID_POG
# - mu_mvaMuID_WP_medium
# - mu_mvaMuID_WP_tight

# LepCut2l__ele_wp90iso__mu_cut_TightID_POG
eleWP = 'wp90iso'
muWP  = 'cut_TightID_POG'

aliases['LepWPCut__ele_' + eleWP + '__mu_' + muWP] = {
    'expr' : 'nLepton > 1 ? \
              ( ( (abs(Lepton_pdgId[0]) == 13 && abs(Lepton_eta[0]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[0]]) < 0.1 && ((Lepton_pt[0] <= 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.01) || (Lepton_pt[0] > 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.02)) && Muon_tightId[Lepton_muonIdx[0]] == 1) || (abs(Lepton_pdgId[0]) == 11 && Lepton_isTightElectron_' + eleWP + '[0]>0.5) ) && \
              ( ( (abs(Lepton_pdgId[1]) == 13 && abs(Lepton_eta[1]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[1]]) < 0.1 && ((Lepton_pt[1] <= 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.01) || (Lepton_pt[1] > 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.02)) && Muon_tightId[Lepton_muonIdx[1]] == 1) || (abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_' + eleWP + '[1]>0.5) ) ) ) : 0',
    'samples': mc,
}

# LepCut2l__ele_wp90iso__mu_cut_MediumID_POG
eleWP = 'wp90iso'
muWP  = 'cut_MediumID_POG'

aliases['LepWPCut__ele_' + eleWP + '__mu_' + muWP] = {
    'expr' : 'nLepton > 1 ? \
              ( ( (abs(Lepton_pdgId[0]) == 13 && abs(Lepton_eta[0]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[0]]) < 0.1 && ((Lepton_pt[0] <= 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.01) || (Lepton_pt[0] > 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.02)) && Muon_mediumId[Lepton_muonIdx[0]] == 1) || (abs(Lepton_pdgId[0]) == 11 && Lepton_isTightElectron_' + eleWP + '[0]>0.5) ) && \
              ( ( (abs(Lepton_pdgId[1]) == 13 && abs(Lepton_eta[1]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[1]]) < 0.1 && ((Lepton_pt[1] <= 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.01) || (Lepton_pt[1] > 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.02)) && Muon_mediumId[Lepton_muonIdx[1]] == 1) || (abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_' + eleWP + '[1]>0.5) ) ) ) : 0',
    'samples': mc,
}

# LepCut2l__ele_wp90iso__mu_mvaMuID_WP_medium
eleWP = 'wp90iso'
muWP  = 'mvaMuID_WP_medium'

aliases['LepWPCut__ele_' + eleWP + '__mu_' + muWP] = {
    'expr' : 'nLepton > 1 ? \
              ( ( (abs(Lepton_pdgId[0]) == 13 && abs(Lepton_eta[0]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[0]]) < 0.1 && ((Lepton_pt[0] <= 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.01) || (Lepton_pt[0] > 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[0]] >= 1) || (abs(Lepton_pdgId[0]) == 11 && Lepton_isTightElectron_' + eleWP + '[0]>0.5) ) && \
              ( ( (abs(Lepton_pdgId[1]) == 13 && abs(Lepton_eta[1]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[1]]) < 0.1 && ((Lepton_pt[1] <= 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.01) || (Lepton_pt[1] > 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[1]] >= 1) || (abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_' + eleWP + '[1]>0.5) ) ) ) : 0',
    'samples': mc,
}

# LepCut2l__ele_wp90iso__mu_mvaMuID_WP_tight
eleWP = 'wp90iso'
muWP  = 'mvaMuID_WP_tight'

aliases['LepWPCut__ele_' + eleWP + '__mu_' + muWP] = {
    'expr' : 'nLepton > 1 ? \
              ( ( (abs(Lepton_pdgId[0]) == 13 && abs(Lepton_eta[0]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[0]]) < 0.1 && ((Lepton_pt[0] <= 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.01) || (Lepton_pt[0] > 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[0]] >= 2) || (abs(Lepton_pdgId[0]) == 11 && Lepton_isTightElectron_' + eleWP + '[0]>0.5) ) && \
              ( ( (abs(Lepton_pdgId[1]) == 13 && abs(Lepton_eta[1]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[1]]) < 0.1 && ((Lepton_pt[1] <= 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.01) || (Lepton_pt[1] > 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[1]] >= 2) || (abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_' + eleWP + '[1]>0.5) ) ) ) : 0',
    'samples': mc,
}



### Basic selections
#
# - ele_mvaWinter22V2Iso_WP90
# - ele_mvaWinter22V2Iso_WP90 + Electron_lostHits == 0
# - ele_mvaWinter22V2Iso_WP90_MiniIso ??
#
# - mu_cut_Tight_HWW
# - mu_cut_MediumID_HWW
# - mu_mvaMuID_WP_medium_HWW
# - mu_mvaMuID_WP_tight_HWW
#
# - mu_cut_TightMiniIso_HWW
# - mu_cut_MediumMiniIso_HWW
# - mu_mvaMuID_WP_medium_MiniIso_HWW
# - mu_mvaMuID_WP_tight_MiniIso_HWW


# LepCut2l__ele_mvaWinter22V2Iso_WP90__mu_cut_Tight_HWW
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'cut_Tight_HWW'

aliases['LepWPCut__ele_' + eleWP + '__mu_' + muWP] = {
    'expr': 'LepCut2l__ele_' + eleWP + '__mu_' + muWP,
    'samples': mc,
}

# LepCut2l__ele_mvaWinter22V2Iso_WP90__mu_cut_Medium_HWW
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'cut_Medium_HWW'

aliases['LepWPCut__ele_' + eleWP + '__mu_' + muWP] = {
    'expr' : 'nLepton > 1 ? \
              ( ( (abs(Lepton_pdgId[0]) == 13 && abs(Lepton_eta[0]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[0]]) < 0.1 && ((Lepton_pt[0] <= 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.01) || (Lepton_pt[0] > 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.02)) && Muon_mediumId[Lepton_muonIdx[0]] == 1 && Muon_pfIsoId[Lepton_muonIdx[0]] >= 4) || (abs(Lepton_pdgId[0]) == 11 && Lepton_isTightElectron_' + eleWP + '[0]>0.5) ) && \
              ( ( (abs(Lepton_pdgId[1]) == 13 && abs(Lepton_eta[1]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[1]]) < 0.1 && ((Lepton_pt[1] <= 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.01) || (Lepton_pt[1] > 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.02)) && Muon_mediumId[Lepton_muonIdx[1]] == 1 && Muon_pfIsoId[Lepton_muonIdx[1]] >= 4) || (abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_' + eleWP + '[1]>0.5) ) ) ) : 0',
    'samples': mc,
}

# LepCut2l__ele_mvaWinter22V2Iso_WP90__mu_mvaMuID_WP_medium_HWW
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'mvaMuID_WP_medium_HWW'

aliases['LepWPCut__ele_' + eleWP + '__mu_' + muWP] = {
    'expr' : 'nLepton > 1 ? \
              ( ( (abs(Lepton_pdgId[0]) == 13 && abs(Lepton_eta[0]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[0]]) < 0.1 && ((Lepton_pt[0] <= 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.01) || (Lepton_pt[0] > 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[0]] >= 1 && Muon_pfIsoId[Lepton_muonIdx[0]] >= 4) || (abs(Lepton_pdgId[0]) == 11 && Lepton_isTightElectron_' + eleWP + '[0]>0.5) ) && \
              ( ( (abs(Lepton_pdgId[1]) == 13 && abs(Lepton_eta[1]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[1]]) < 0.1 && ((Lepton_pt[1] <= 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.01) || (Lepton_pt[1] > 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[1]] >= 1 && Muon_pfIsoId[Lepton_muonIdx[1]] >= 4) || (abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_' + eleWP + '[1]>0.5) ) ) ) : 0',
    'samples': mc,
}

# LepCut2l__ele_mvaWinter22V2Iso_WP90__mu_mvaMuID_WP_tight_HWW
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'mvaMuID_WP_tight_HWW'

aliases['LepWPCut__ele_' + eleWP + '__mu_' + muWP] = {
    'expr' : 'nLepton > 1 ? \
              ( ( (abs(Lepton_pdgId[0]) == 13 && abs(Lepton_eta[0]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[0]]) < 0.1 && ((Lepton_pt[0] <= 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.01) || (Lepton_pt[0] > 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[0]] >= 2 && Muon_pfIsoId[Lepton_muonIdx[0]] >= 4) || (abs(Lepton_pdgId[0]) == 11 && Lepton_isTightElectron_' + eleWP + '[0]>0.5) ) && \
              ( ( (abs(Lepton_pdgId[1]) == 13 && abs(Lepton_eta[1]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[1]]) < 0.1 && ((Lepton_pt[1] <= 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.01) || (Lepton_pt[1] > 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[1]] >= 2 && Muon_pfIsoId[Lepton_muonIdx[1]] >= 4) || (abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_' + eleWP + '[1]>0.5) ) ) ) : 0',
    'samples': mc,
}


# LepCut2l__ele_mvaWinter22V2Iso_WP90__mu_cut_TightMiniIso_HWW
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'cut_TightMiniIso_HWW'

aliases['LepWPCut__ele_' + eleWP + '__mu_' + muWP] = {
    'expr': 'LepCut2l__ele_' + eleWP + '__mu_' + muWP,
    'samples': mc,
}

# LepCut2l__ele_mvaWinter22V2Iso_WP90__mu_cut_MediumMiniIso_HWW
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'cut_MediumMiniIso_HWW'

aliases['LepWPCut__ele_' + eleWP + '__mu_' + muWP] = {
    'expr' : 'nLepton > 1 ? \
              ( ( (abs(Lepton_pdgId[0]) == 13 && abs(Lepton_eta[0]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[0]]) < 0.1 && ((Lepton_pt[0] <= 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.01) || (Lepton_pt[0] > 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.02)) && Muon_mediumId[Lepton_muonIdx[0]] == 1 && Muon_miniIsoId[Lepton_muonIdx[0]] >= 3) || (abs(Lepton_pdgId[0]) == 11 && Lepton_isTightElectron_' + eleWP + '[0]>0.5) ) && \
              ( ( (abs(Lepton_pdgId[1]) == 13 && abs(Lepton_eta[1]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[1]]) < 0.1 && ((Lepton_pt[1] <= 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.01) || (Lepton_pt[1] > 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.02)) && Muon_mediumId[Lepton_muonIdx[1]] == 1 && Muon_miniIsoId[Lepton_muonIdx[1]] >= 3) || (abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_' + eleWP + '[1]>0.5) ) ) ) : 0',
    'samples': mc,
}

# LepCut2l__ele_mvaWinter22V2Iso_WP90__mu_mvaMuID_WP_mediumMiniIso_HWW
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'mvaMuID_WP_mediumMiniIso_HWW'

aliases['LepWPCut__ele_' + eleWP + '__mu_' + muWP] = {
    'expr' : 'nLepton > 1 ? \
              ( ( (abs(Lepton_pdgId[0]) == 13 && abs(Lepton_eta[0]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[0]]) < 0.1 && ((Lepton_pt[0] <= 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.01) || (Lepton_pt[0] > 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[0]] >= 1 && Muon_miniIsoId[Lepton_muonIdx[0]] >= 3) || (abs(Lepton_pdgId[0]) == 11 && Lepton_isTightElectron_' + eleWP + '[0]>0.5) ) && \
              ( ( (abs(Lepton_pdgId[1]) == 13 && abs(Lepton_eta[1]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[1]]) < 0.1 && ((Lepton_pt[1] <= 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.01) || (Lepton_pt[1] > 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[1]] >= 1 && Muon_miniIsoId[Lepton_muonIdx[1]] >= 3) || (abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_' + eleWP + '[1]>0.5) ) ) ) : 0',
    'samples': mc,
}

# LepCut2l__ele_mvaWinter22V2Iso_WP90__mu_mvaMuID_WP_tightMiniIso_HWW
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'mvaMuID_WP_tightMiniIso_HWW'

aliases['LepWPCut__ele_' + eleWP + '__mu_' + muWP] = {
    'expr' : 'nLepton > 1 ? \
              ( ( (abs(Lepton_pdgId[0]) == 13 && abs(Lepton_eta[0]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[0]]) < 0.1 && ((Lepton_pt[0] <= 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.01) || (Lepton_pt[0] > 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[0]] >= 2 && Muon_miniIsoId[Lepton_muonIdx[0]] >= 3) || (abs(Lepton_pdgId[0]) == 11 && Lepton_isTightElectron_' + eleWP + '[0]>0.5) ) && \
              ( ( (abs(Lepton_pdgId[1]) == 13 && abs(Lepton_eta[1]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[1]]) < 0.1 && ((Lepton_pt[1] <= 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.01) || (Lepton_pt[1] > 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[1]] >= 2 && Muon_miniIsoId[Lepton_muonIdx[1]] >= 3) || (abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_' + eleWP + '[1]>0.5) ) ) ) : 0',
    'samples': mc,
}


# LepCut2l__ele_mvaWinter22V2Iso_WP90_noLostHits__mu_cut_Tight_HWW
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'cut_Tight_HWW'

aliases['LepWPCut__ele_' + eleWP + '_noLostHits__mu_' + muWP] = {
    'expr': 'LepCut2l__ele_' + eleWP + '__mu_' + muWP + ' \
             && ((abs(Lepton_pdgId[0]) == 11 && Electron_lostHits[Lepton_electronIdx[0]] == 0) || (abs(Lepton_pdgId[0]) == 13)) \
             && ((abs(Lepton_pdgId[1]) == 11 && Electron_lostHits[Lepton_electronIdx[1]] == 0) || (abs(Lepton_pdgId[1]) == 13))',
    'samples': mc,
}

# LepCut2l__ele_mvaWinter22V2Iso_WP90_noLostHits__mu_cut_Medium_HWW
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'cut_Medium_HWW'

aliases['LepWPCut__ele_' + eleWP + '_noLostHits__mu_' + muWP] = {
    'expr' : 'nLepton > 1 ? \
              ( ( (abs(Lepton_pdgId[0]) == 13 && abs(Lepton_eta[0]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[0]]) < 0.1 && ((Lepton_pt[0] <= 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.01) || (Lepton_pt[0] > 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.02)) && Muon_mediumId[Lepton_muonIdx[0]] == 1 && Muon_pfIsoId[Lepton_muonIdx[0]] >= 4) || (abs(Lepton_pdgId[0]) == 11 && (Lepton_isTightElectron_' + eleWP + '[0]>0.5 && Electron_lostHits[Lepton_electronIdx[0]] == 0) ) ) && \
              ( ( (abs(Lepton_pdgId[1]) == 13 && abs(Lepton_eta[1]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[1]]) < 0.1 && ((Lepton_pt[1] <= 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.01) || (Lepton_pt[1] > 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.02)) && Muon_mediumId[Lepton_muonIdx[1]] == 1 && Muon_pfIsoId[Lepton_muonIdx[1]] >= 4) || (abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_' + eleWP + '[1]>0.5 && Electron_lostHits[Lepton_electronIdx[1]] == 0) ) ) ) : 0',
    'samples': mc,
}

# LepCut2l__ele_mvaWinter22V2Iso_WP90_noLostHits__mu_mvaMuID_WP_medium_HWW
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'mvaMuID_WP_medium_HWW'

aliases['LepWPCut__ele_' + eleWP + '_noLostHits__mu_' + muWP] = {
    'expr' : 'nLepton > 1 ? \
              ( ( (abs(Lepton_pdgId[0]) == 13 && abs(Lepton_eta[0]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[0]]) < 0.1 && ((Lepton_pt[0] <= 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.01) || (Lepton_pt[0] > 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[0]] >= 1 && Muon_pfIsoId[Lepton_muonIdx[0]] >= 4) || (abs(Lepton_pdgId[0]) == 11 && Lepton_isTightElectron_' + eleWP + '[0]>0.5 && Electron_lostHits[Lepton_electronIdx[0]] == 0) ) && \
              ( ( (abs(Lepton_pdgId[1]) == 13 && abs(Lepton_eta[1]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[1]]) < 0.1 && ((Lepton_pt[1] <= 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.01) || (Lepton_pt[1] > 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[1]] >= 1 && Muon_pfIsoId[Lepton_muonIdx[1]] >= 4) || (abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_' + eleWP + '[1]>0.5 && Electron_lostHits[Lepton_electronIdx[1]] == 0) ) ) ) : 0',
    'samples': mc,
}

# LepCut2l__ele_mvaWinter22V2Iso_WP90_noLostHits__mu_mvaMuID_WP_tight_HWW
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'mvaMuID_WP_tight_HWW'

aliases['LepWPCut__ele_' + eleWP + '_noLostHits__mu_' + muWP] = {
    'expr' : 'nLepton > 1 ? \
              ( ( (abs(Lepton_pdgId[0]) == 13 && abs(Lepton_eta[0]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[0]]) < 0.1 && ((Lepton_pt[0] <= 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.01) || (Lepton_pt[0] > 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[0]] >= 2 && Muon_pfIsoId[Lepton_muonIdx[0]] >= 4) || (abs(Lepton_pdgId[0]) == 11 && Lepton_isTightElectron_' + eleWP + '[0]>0.5 && Electron_lostHits[Lepton_electronIdx[0]] == 0) ) && \
              ( ( (abs(Lepton_pdgId[1]) == 13 && abs(Lepton_eta[1]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[1]]) < 0.1 && ((Lepton_pt[1] <= 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.01) || (Lepton_pt[1] > 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[1]] >= 2 && Muon_pfIsoId[Lepton_muonIdx[1]] >= 4) || (abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_' + eleWP + '[1]>0.5 && Electron_lostHits[Lepton_electronIdx[1]] == 0) ) ) ) : 0',
    'samples': mc,
}


# LepCut2l__ele_mvaWinter22V2Iso_WP90_noLostHits__mu_cut_TightMiniIso_HWW
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'cut_TightMiniIso_HWW'

aliases['LepWPCut__ele_' + eleWP + '_noLostHits__mu_' + muWP] = {
    'expr': 'LepCut2l__ele_' + eleWP + '__mu_' + muWP + '\
             && ((abs(Lepton_pdgId[0]) == 11 && Electron_lostHits[Lepton_electronIdx[0]] == 0) || (abs(Lepton_pdgId[0]) == 13)) \
             && ((abs(Lepton_pdgId[1]) == 11 && Electron_lostHits[Lepton_electronIdx[1]] == 0) || (abs(Lepton_pdgId[1]) == 13))',
    'samples': mc,
}

# LepCut2l__ele_mvaWinter22V2Iso_WP90_noLostHits__mu_cut_MediumMiniIso_HWW
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'cut_MediumMiniIso_HWW'

aliases['LepWPCut__ele_' + eleWP + '_noLostHits__mu_' + muWP] = {
    'expr' : 'nLepton > 1 ? \
              ( ( (abs(Lepton_pdgId[0]) == 13 && abs(Lepton_eta[0]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[0]]) < 0.1 && ((Lepton_pt[0] <= 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.01) || (Lepton_pt[0] > 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.02)) && Muon_mediumId[Lepton_muonIdx[0]] == 1 && Muon_miniIsoId[Lepton_muonIdx[0]] >= 3) || (abs(Lepton_pdgId[0]) == 11 && Lepton_isTightElectron_' + eleWP + '[0]>0.5 && Electron_lostHits[Lepton_electronIdx[0]] == 0) ) && \
              ( ( (abs(Lepton_pdgId[1]) == 13 && abs(Lepton_eta[1]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[1]]) < 0.1 && ((Lepton_pt[1] <= 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.01) || (Lepton_pt[1] > 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.02)) && Muon_mediumId[Lepton_muonIdx[1]] == 1 && Muon_miniIsoId[Lepton_muonIdx[1]] >= 3) || (abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_' + eleWP + '[1]>0.5 && Electron_lostHits[Lepton_electronIdx[1]] == 0) ) ) ) : 0',
    'samples': mc,
}

# LepCut2l__ele_mvaWinter22V2Iso_WP90_noLostHits__mu_mvaMuID_WP_mediumMiniIso_HWW
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'mvaMuID_WP_mediumMiniIso_HWW'

aliases['LepWPCut__ele_' + eleWP + '_noLostHits__mu_' + muWP] = {
    'expr' : 'nLepton > 1 ? \
              ( ( (abs(Lepton_pdgId[0]) == 13 && abs(Lepton_eta[0]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[0]]) < 0.1 && ((Lepton_pt[0] <= 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.01) || (Lepton_pt[0] > 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[0]] >= 1 && Muon_miniIsoId[Lepton_muonIdx[0]] >= 3) || (abs(Lepton_pdgId[0]) == 11 && Lepton_isTightElectron_' + eleWP + '[0]>0.5 && Electron_lostHits[Lepton_electronIdx[0]] == 0) ) && \
              ( ( (abs(Lepton_pdgId[1]) == 13 && abs(Lepton_eta[1]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[1]]) < 0.1 && ((Lepton_pt[1] <= 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.01) || (Lepton_pt[1] > 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[1]] >= 1 && Muon_miniIsoId[Lepton_muonIdx[1]] >= 3) || (abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_' + eleWP + '[1]>0.5 && Electron_lostHits[Lepton_electronIdx[1]] == 0) ) ) ) : 0',
    'samples': mc,
}

# LepCut2l__ele_mvaWinter22V2Iso_WP90_noLostHits__mu_mvaMuID_WP_tightMiniIso_HWW
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'mvaMuID_WP_tightMiniIso_HWW'

aliases['LepWPCut__ele_' + eleWP + '_noLostHits__mu_' + muWP] = {
    'expr' : 'nLepton > 1 ? \
              ( ( (abs(Lepton_pdgId[0]) == 13 && abs(Lepton_eta[0]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[0]]) < 0.1 && ((Lepton_pt[0] <= 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.01) || (Lepton_pt[0] > 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[0]] >= 2 && Muon_miniIsoId[Lepton_muonIdx[0]] >= 3) || (abs(Lepton_pdgId[0]) == 11 && Lepton_isTightElectron_' + eleWP + '[0]>0.5 && Electron_lostHits[Lepton_electronIdx[0]] == 0) ) && \
              ( ( (abs(Lepton_pdgId[1]) == 13 && abs(Lepton_eta[1]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[1]]) < 0.1 && ((Lepton_pt[1] <= 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.01) || (Lepton_pt[1] > 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[1]] >= 2 && Muon_miniIsoId[Lepton_muonIdx[1]] >= 3) || (abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_' + eleWP + '[1]>0.5 && Electron_lostHits[Lepton_electronIdx[1]] == 0) ) ) ) : 0',
    'samples': mc,
}


### Selections Incuding ttHMVA Run3 discriminant. It could also be tuned on top of the previous steps, looking at expected significance or comparing the fake rate in UL
#
# - ele_mvaWinter22V2Iso_WP90_ttHMVA_90
# - ele_mvaWinter22V2Iso_WP90_looseIso_ttHMVA_90
# - ele_mvaWinter22V2Iso_WP90_noLostHits_ttHMVA_90
#
# - ele_mvaWinter22V2Iso_WP90_MiniIso_ttHMVA_90 ??
#
#
# - mu_cut_Tight_HWW_ttHMVA_67
# - mu_cut_Medium_HWW_ttHMVA_67
# - mu_mvaMuID_WP_medium_HWW_ttHMVA_67
# - mu_mvaMuID_WP_tight_HWW_ttHMVA_67
#
# - mu_cut_TightMiniIso_HWW_ttHMVA_67
# - mu_cut_MediumMiniIso_HWW_ttHMVA_67
# - mu_mvaMuID_WP_medium_MiniIso_HWW_ttHMVA_67
# - mu_mvaMuID_WP_tight_MiniIso_HWW_ttHMVA_67
#
# - mu_cut_Tight_looseIso_ttHMVA_67
# - mu_cut_Medium_looseIso_ttHMVA_67
# - mu_mvaMuID_WP_medium_looseIso_ttHMVA_67


# LepCut2l__ele_mvaWinter22V2Iso_WP90_looseIso_ttHMVA_90__mu_cut_Tight_looseIso_ttHMVA_67
eleWP = 'mvaWinter22V2Iso_WP90_looseIso'
muWP  = 'cut_Tight_looseIso'

aliases['LepWPCut__ele_' + eleWP + '_ttHMVA_90__mu_' + muWP + '_ttHMVA_67'] = {
    'expr' : '( ( (abs(Lepton_pdgId[0]) == 13 && Lepton_ttHMVA_Run3[Lepton_muonIdx[0]]>0.67 && Muon_tightId[Lepton_muonIdx[0]] == 1) || (abs(Lepton_pdgId[0]) == 11 && Electron_mvaIso_WP90[Lepton_electronIdx[0]] == 1 && Electron_convVeto[Lepton_electronIdx[0]] == 1 && Electron_pfRelIso03_all[Lepton_electronIdx[0]] < 0.4 && ((abs(Lepton_eta[0]) <= 1.479 && abs(Electron_dxy[Lepton_electronIdx[0]]) < 0.05 && abs(Electron_dz[Lepton_electronIdx[0]]) < 0.1) || (abs(Lepton_eta[0]) > 1.479 && abs(Electron_dxy[Lepton_electronIdx[0]]) < 0.1 && abs(Electron_dz[Lepton_electronIdx[0]]) < 0.2)) && Lepton_ttHMVA_Run3[Lepton_electronIdx[0]]>0.90) ) && \
                ( (abs(Lepton_pdgId[1]) == 13 && Lepton_ttHMVA_Run3[Lepton_muonIdx[1]]>0.67 && Muon_tightId[Lepton_muonIdx[1]] == 1) || (abs(Lepton_pdgId[1]) == 11 && Electron_mvaIso_WP90[Lepton_electronIdx[1]] == 1 && Electron_convVeto[Lepton_electronIdx[1]] == 1 && Electron_pfRelIso03_all[Lepton_electronIdx[1]] < 0.4 && ((abs(Lepton_eta[1]) <= 1.479 && abs(Electron_dxy[Lepton_electronIdx[1]]) < 0.05 && abs(Electron_dz[Lepton_electronIdx[1]]) < 0.1) || (abs(Lepton_eta[1]) > 1.479 && abs(Electron_dxy[Lepton_electronIdx[1]]) < 0.1 && abs(Electron_dz[Lepton_electronIdx[1]]) < 0.2)) && Lepton_ttHMVA_Run3[Lepton_electronIdx[1]]>0.90) ) )',
    'samples' : mc,
}

# LepCut2l__ele_mvaWinter22V2Iso_WP90_looseIso_ttHMVA_90__mu_cut_Medium_looseIso_ttHMVA_67
eleWP = 'mvaWinter22V2Iso_WP90_looseIso'
muWP  = 'cut_Medium_looseIso'

aliases['LepWPCut__ele_' + eleWP + '_ttHMVA_90__mu_' + muWP + '_ttHMVA_67'] = {
    'expr' : '( ( (abs(Lepton_pdgId[0]) == 13 && Lepton_ttHMVA_Run3[Lepton_muonIdx[0]]>0.67 && Muon_mediumId[Lepton_muonIdx[0]] == 1) || (abs(Lepton_pdgId[0]) == 11 && Electron_mvaIso_WP90[Lepton_electronIdx[0]] == 1 && Electron_convVeto[Lepton_electronIdx[0]] == 1 && Electron_pfRelIso03_all[Lepton_electronIdx[0]] < 0.4 && ((abs(Lepton_eta[0]) <= 1.479 && abs(Electron_dxy[Lepton_electronIdx[0]]) < 0.05 && abs(Electron_dz[Lepton_electronIdx[0]]) < 0.1) || (abs(Lepton_eta[0]) > 1.479 && abs(Electron_dxy[Lepton_electronIdx[0]]) < 0.1 && abs(Electron_dz[Lepton_electronIdx[0]]) < 0.2)) && Lepton_ttHMVA_Run3[Lepton_electronIdx[0]]>0.90) ) && \
                ( (abs(Lepton_pdgId[1]) == 13 && Lepton_ttHMVA_Run3[Lepton_muonIdx[1]]>0.67 && Muon_mediumId[Lepton_muonIdx[1]] == 1) || (abs(Lepton_pdgId[1]) == 11 && Electron_mvaIso_WP90[Lepton_electronIdx[1]] == 1 && Electron_convVeto[Lepton_electronIdx[1]] == 1 && Electron_pfRelIso03_all[Lepton_electronIdx[1]] < 0.4 && ((abs(Lepton_eta[1]) <= 1.479 && abs(Electron_dxy[Lepton_electronIdx[1]]) < 0.05 && abs(Electron_dz[Lepton_electronIdx[1]]) < 0.1) || (abs(Lepton_eta[1]) > 1.479 && abs(Electron_dxy[Lepton_electronIdx[1]]) < 0.1 && abs(Electron_dz[Lepton_electronIdx[1]]) < 0.2)) && Lepton_ttHMVA_Run3[Lepton_electronIdx[1]]>0.90) ) )',
    'samples' : mc,
}

# LepCut2l__ele_mvaWinter22V2Iso_WP90_looseIso_ttHMVA_90__mu_mvaMuID_WP_medium_looseIso_ttHMVA_67
eleWP = 'mvaWinter22V2Iso_WP90_looseIso'
muWP  = 'mvaMuID_WP_medium_looseIso'

aliases['LepWPCut__ele_' + eleWP + '_ttHMVA_90__mu_' + muWP + '_ttHMVA_67'] = {
    'expr' : '( ( (abs(Lepton_pdgId[0]) == 13 && Lepton_ttHMVA_Run3[Lepton_muonIdx[0]]>0.67 && Muon_mvaMuID_WP[Lepton_muonIdx[0]] >= 1) || (abs(Lepton_pdgId[0]) == 11 && Electron_mvaIso_WP90[Lepton_electronIdx[0]] == 1 && Electron_convVeto[Lepton_electronIdx[0]] == 1 && Electron_pfRelIso03_all[Lepton_electronIdx[0]] < 0.4 && ((abs(Lepton_eta[0]) <= 1.479 && abs(Electron_dxy[Lepton_electronIdx[0]]) < 0.05 && abs(Electron_dz[Lepton_electronIdx[0]]) < 0.1) || (abs(Lepton_eta[0]) > 1.479 && abs(Electron_dxy[Lepton_electronIdx[0]]) < 0.1 && abs(Electron_dz[Lepton_electronIdx[0]]) < 0.2)) && Lepton_ttHMVA_Run3[Lepton_electronIdx[0]]>0.90) ) && \
                ( (abs(Lepton_pdgId[1]) == 13 && Lepton_ttHMVA_Run3[Lepton_muonIdx[1]]>0.67 && Muon_mvaMuID_WP[Lepton_muonIdx[1]] >= 1) || (abs(Lepton_pdgId[1]) == 11 && Electron_mvaIso_WP90[Lepton_electronIdx[1]] == 1 && Electron_convVeto[Lepton_electronIdx[1]] == 1 && Electron_pfRelIso03_all[Lepton_electronIdx[1]] < 0.4 && ((abs(Lepton_eta[1]) <= 1.479 && abs(Electron_dxy[Lepton_electronIdx[1]]) < 0.05 && abs(Electron_dz[Lepton_electronIdx[1]]) < 0.1) || (abs(Lepton_eta[1]) > 1.479 && abs(Electron_dxy[Lepton_electronIdx[1]]) < 0.1 && abs(Electron_dz[Lepton_electronIdx[1]]) < 0.2)) && Lepton_ttHMVA_Run3[Lepton_electronIdx[1]]>0.90) ) )',
    'samples' : mc,
}

# LepCut2l__ele_mvaWinter22V2Iso_WP90_looseIso_ttHMVA_90__mu_mvaMuID_WP_tight_looseIso_ttHMVA_67
eleWP = 'mvaWinter22V2Iso_WP90_looseIso'
muWP  = 'mvaMuID_WP_tight_looseIso'

aliases['LepWPCut__ele_' + eleWP + '_ttHMVA_90__mu_' + muWP + '_ttHMVA_67'] = {
    'expr' : '( ( (abs(Lepton_pdgId[0]) == 13 && Lepton_ttHMVA_Run3[Lepton_muonIdx[0]]>0.67 && Muon_mvaMuID_WP[Lepton_muonIdx[0]] >= 2) || (abs(Lepton_pdgId[0]) == 11 && Electron_mvaIso_WP90[Lepton_electronIdx[0]] == 1 && Electron_convVeto[Lepton_electronIdx[0]] == 1 && Electron_pfRelIso03_all[Lepton_electronIdx[0]] < 0.4 && ((abs(Lepton_eta[0]) <= 1.479 && abs(Electron_dxy[Lepton_electronIdx[0]]) < 0.05 && abs(Electron_dz[Lepton_electronIdx[0]]) < 0.1) || (abs(Lepton_eta[0]) > 1.479 && abs(Electron_dxy[Lepton_electronIdx[0]]) < 0.1 && abs(Electron_dz[Lepton_electronIdx[0]]) < 0.2)) && Lepton_ttHMVA_Run3[Lepton_electronIdx[0]]>0.90) ) && \
                ( (abs(Lepton_pdgId[1]) == 13 && Lepton_ttHMVA_Run3[Lepton_muonIdx[1]]>0.67 && Muon_mvaMuID_WP[Lepton_muonIdx[1]] >= 2) || (abs(Lepton_pdgId[1]) == 11 && Electron_mvaIso_WP90[Lepton_electronIdx[1]] == 1 && Electron_convVeto[Lepton_electronIdx[1]] == 1 && Electron_pfRelIso03_all[Lepton_electronIdx[1]] < 0.4 && ((abs(Lepton_eta[1]) <= 1.479 && abs(Electron_dxy[Lepton_electronIdx[1]]) < 0.05 && abs(Electron_dz[Lepton_electronIdx[1]]) < 0.1) || (abs(Lepton_eta[1]) > 1.479 && abs(Electron_dxy[Lepton_electronIdx[1]]) < 0.1 && abs(Electron_dz[Lepton_electronIdx[1]]) < 0.2)) && Lepton_ttHMVA_Run3[Lepton_electronIdx[1]]>0.90) ) )',
    'samples' : mc,
}


# LepCut2l__ele_mvaWinter22V2Iso_WP90_ttHMVA_90__mu_cut_Tight_HWW_ttHMVA_67
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'cut_Tight_HWW'

aliases['LepWPCut__ele_' + eleWP + '_ttHMVA_90__mu_' + muWP + '_ttHMVA_67'] = {
    'expr': 'LepCut2l__ele_' + eleWP + '__mu_' + muWP + ' && \
            ( ((abs(Lepton_pdgId[0])==13 && Lepton_ttHMVA_Run3[Lepton_muonIdx[0]]>0.67) || (abs(Lepton_pdgId[0])==11 && Lepton_ttHMVA_Run3[Lepton_electronIdx[0]]>0.90)) \
            && ((abs(Lepton_pdgId[1])==13 && Lepton_ttHMVA_Run3[Lepton_muonIdx[1]]>0.67) || (abs(Lepton_pdgId[1])==11 && Lepton_ttHMVA_Run3[Lepton_electronIdx[1]]>0.90)) )',
    'samples': mc,
}

# LepCut2l__ele_mvaWinter22V2Iso_WP90_ttHMVA_90__mu_cut_MediumID_HWW_ttHMVA_67
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'cut_Medium_HWW'

aliases['LepWPCut__ele_' + eleWP + '_ttHMVA_90__mu_' + muWP + '_ttHMVA_67'] = {
    'expr' : 'nLepton > 1 ? \
              ( ( (abs(Lepton_pdgId[0]) == 13 && abs(Lepton_eta[0]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[0]]) < 0.1 && ((Lepton_pt[0] <= 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.01) || (Lepton_pt[0] > 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.02)) && Muon_mediumId[Lepton_muonIdx[0]] == 1 && Muon_pfIsoId[Lepton_muonIdx[0]] >= 4 && Lepton_ttHMVA_Run3[Lepton_muonIdx[0]]>0.67) || (abs(Lepton_pdgId[0]) == 11 && Lepton_isTightElectron_' + eleWP + '[0]>0.5 && Lepton_ttHMVA_Run3[Lepton_electronIdx[0]]>0.90) ) && \
              ( ( (abs(Lepton_pdgId[1]) == 13 && abs(Lepton_eta[1]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[1]]) < 0.1 && ((Lepton_pt[1] <= 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.01) || (Lepton_pt[1] > 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.02)) && Muon_mediumId[Lepton_muonIdx[1]] == 1 && Muon_pfIsoId[Lepton_muonIdx[1]] >= 4 && Lepton_ttHMVA_Run3[Lepton_muonIdx[1]]>0.67) || (abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_' + eleWP + '[1]>0.5 && Lepton_ttHMVA_Run3[Lepton_electronIdx[1]]>0.90) ) ) ) : 0',
    'samples': mc,
}

# LepCut2l__ele_mvaWinter22V2Iso_WP90_ttHMVA_90__mu_mvaMuID_WP_medium_HWW_ttHMVA_67
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'mvaMuID_WP_medium_HWW'

aliases['LepWPCut__ele_' + eleWP + '_ttHMVA_90__mu_' + muWP + '_ttHMVA_67'] = {
    'expr' : 'nLepton > 1 ? \
              ( ( (abs(Lepton_pdgId[0]) == 13 && abs(Lepton_eta[0]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[0]]) < 0.1 && ((Lepton_pt[0] <= 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.01) || (Lepton_pt[0] > 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[0]] >= 1 && Muon_pfIsoId[Lepton_muonIdx[0]] >= 4 && Lepton_ttHMVA_Run3[Lepton_muonIdx[0]]>0.67) || (abs(Lepton_pdgId[0]) == 11 && Lepton_isTightElectron_' + eleWP + '[0]>0.5 && Lepton_ttHMVA_Run3[Lepton_electronIdx[0]]>0.90) ) && \
              ( ( (abs(Lepton_pdgId[1]) == 13 && abs(Lepton_eta[1]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[1]]) < 0.1 && ((Lepton_pt[1] <= 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.01) || (Lepton_pt[1] > 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[1]] >= 1 && Muon_pfIsoId[Lepton_muonIdx[1]] >= 4 && Lepton_ttHMVA_Run3[Lepton_muonIdx[1]]>0.67) || (abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_' + eleWP + '[1]>0.5 && Lepton_ttHMVA_Run3[Lepton_electronIdx[1]]>0.90) ) ) ) : 0',
    'samples': mc,
}

# LepCut2l__ele_mvaWinter22V2Iso_WP90_ttHMVA_90__mu_mvaMuID_WP_tight_HWW_ttHMVA_67
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'mvaMuID_WP_tight_HWW'

aliases['LepWPCut__ele_' + eleWP + '_ttHMVA_90__mu_' + muWP + '_ttHMVA_67'] = {
    'expr' : 'nLepton > 1 ? \
              ( ( (abs(Lepton_pdgId[0]) == 13 && abs(Lepton_eta[0]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[0]]) < 0.1 && ((Lepton_pt[0] <= 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.01) || (Lepton_pt[0] > 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[0]] >= 2 && Muon_pfIsoId[Lepton_muonIdx[0]] >= 4 && Lepton_ttHMVA_Run3[Lepton_muonIdx[0]]>0.67) || (abs(Lepton_pdgId[0]) == 11 && Lepton_isTightElectron_' + eleWP + '[0]>0.5 && Lepton_ttHMVA_Run3[Lepton_electronIdx[0]]>0.90) ) && \
              ( ( (abs(Lepton_pdgId[1]) == 13 && abs(Lepton_eta[1]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[1]]) < 0.1 && ((Lepton_pt[1] <= 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.01) || (Lepton_pt[1] > 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[1]] >= 2 && Muon_pfIsoId[Lepton_muonIdx[1]] >= 4 && Lepton_ttHMVA_Run3[Lepton_muonIdx[1]]>0.67) || (abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_' + eleWP + '[1]>0.5 && Lepton_ttHMVA_Run3[Lepton_electronIdx[1]]>0.90) ) ) ) : 0',
    'samples': mc,
}


# LepCut2l__ele_mvaWinter22V2Iso_WP90_ttHMVA_90__mu_cut_TightMiniIso_HWW_ttHMVA_67
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'cut_TightMiniIso_HWW'

aliases['LepWPCut__ele_' + eleWP + '_ttHMVA_90__mu_' + muWP + '_ttHMVA_67'] = {
    'expr': 'LepCut2l__ele_' + eleWP + '__mu_' + muWP + ' && \
             ( ( (abs(Lepton_pdgId[0]) == 13 && Lepton_ttHMVA_Run3[Lepton_muonIdx[0]]>0.67) || (abs(Lepton_pdgId[0]) == 11 && Lepton_ttHMVA_Run3[Lepton_electronIdx[0]]>0.90) ) && \
               ( (abs(Lepton_pdgId[1]) == 13 && Lepton_ttHMVA_Run3[Lepton_muonIdx[1]]>0.67) || (abs(Lepton_pdgId[1]) == 11 && Lepton_ttHMVA_Run3[Lepton_electronIdx[1]]>0.90) ) ) \
    ',
    'samples': mc,
}

# LepCut2l__ele_mvaWinter22V2Iso_WP90_ttHMVA_90__mu_cut_MediumMiniIso_HWW_ttHMVA_67
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'cut_MediumMiniIso_HWW'

aliases['LepWPCut__ele_' + eleWP + '_ttHMVA_90__mu_' + muWP + '_ttHMVA_67'] = {
    'expr' : 'nLepton > 1 ? \
              ( ( (abs(Lepton_pdgId[0]) == 13 && abs(Lepton_eta[0]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[0]]) < 0.1 && ((Lepton_pt[0] <= 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.01) || (Lepton_pt[0] > 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.02)) && Muon_mediumId[Lepton_muonIdx[0]] == 1 && Muon_miniIsoId[Lepton_muonIdx[0]] >= 3 && Lepton_ttHMVA_Run3[Lepton_muonIdx[0]]>0.67) || (abs(Lepton_pdgId[0]) == 11 && Lepton_isTightElectron_' + eleWP + '[0]>0.5 && Lepton_ttHMVA_Run3[Lepton_electronIdx[0]]>0.90) ) && \
              ( ( (abs(Lepton_pdgId[1]) == 13 && abs(Lepton_eta[1]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[1]]) < 0.1 && ((Lepton_pt[1] <= 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.01) || (Lepton_pt[1] > 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.02)) && Muon_mediumId[Lepton_muonIdx[1]] == 1 && Muon_miniIsoId[Lepton_muonIdx[1]] >= 3 && Lepton_ttHMVA_Run3[Lepton_muonIdx[1]]>0.67) || (abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_' + eleWP + '[1]>0.5 && Lepton_ttHMVA_Run3[Lepton_electronIdx[1]]>0.90) ) ) ) : 0',
    'samples': mc,
}

# LepCut2l__ele_mvaWinter22V2Iso_WP90_ttHMVA_90__mu_mvaMuID_WP_mediumMiniIso_HWW_ttHMVA_67
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'mvaMuID_WP_mediumMiniIso_HWW'

aliases['LepWPCut__ele_' + eleWP + '_ttHMVA_90__mu_' + muWP + '_ttHMVA_67'] = {
    'expr' : 'nLepton > 1 ? \
              ( ( (abs(Lepton_pdgId[0]) == 13 && abs(Lepton_eta[0]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[0]]) < 0.1 && ((Lepton_pt[0] <= 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.01) || (Lepton_pt[0] > 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[0]] >= 1 && Muon_miniIsoId[Lepton_muonIdx[0]] >= 3 && Lepton_ttHMVA_Run3[Lepton_muonIdx[0]]>0.67) || (abs(Lepton_pdgId[0]) == 11 && Lepton_isTightElectron_' + eleWP + '[0]>0.5 && Lepton_ttHMVA_Run3[Lepton_electronIdx[0]]>0.90) ) && \
              ( ( (abs(Lepton_pdgId[1]) == 13 && abs(Lepton_eta[1]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[1]]) < 0.1 && ((Lepton_pt[1] <= 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.01) || (Lepton_pt[1] > 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[1]] >= 1 && Muon_miniIsoId[Lepton_muonIdx[1]] >= 3 && Lepton_ttHMVA_Run3[Lepton_muonIdx[1]]>0.67) || (abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_' + eleWP + '[1]>0.5 && Lepton_ttHMVA_Run3[Lepton_electronIdx[1]]>0.90) ) ) ) : 0',
    'samples': mc,
}

# LepCut2l__ele_mvaWinter22V2Iso_WP90_ttHMVA_90__mu_mvaMuID_WP_tightMiniIso_HWW_ttHMVA_67
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'mvaMuID_WP_tightMiniIso_HWW'

aliases['LepWPCut__ele_' + eleWP + '_ttHMVA_90__mu_' + muWP + '_ttHMVA_67'] = {
    'expr' : 'nLepton > 1 ? \
              ( ( (abs(Lepton_pdgId[0]) == 13 && abs(Lepton_eta[0]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[0]]) < 0.1 && ((Lepton_pt[0] <= 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.01) || (Lepton_pt[0] > 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[0]] >= 2 && Muon_miniIsoId[Lepton_muonIdx[0]] >= 3 && Lepton_ttHMVA_Run3[Lepton_muonIdx[0]]>0.67) || (abs(Lepton_pdgId[0]) == 11 && Lepton_isTightElectron_' + eleWP + '[0]>0.5 && Lepton_ttHMVA_Run3[Lepton_electronIdx[0]]>0.90) ) && \
              ( ( (abs(Lepton_pdgId[1]) == 13 && abs(Lepton_eta[1]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[1]]) < 0.1 && ((Lepton_pt[1] <= 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.01) || (Lepton_pt[1] > 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[1]] >= 2 && Muon_miniIsoId[Lepton_muonIdx[1]] >= 3 && Lepton_ttHMVA_Run3[Lepton_muonIdx[1]]>0.67) || (abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_' + eleWP + '[1]>0.5 && Lepton_ttHMVA_Run3[Lepton_electronIdx[1]]>0.90) ) ) ) : 0',
    'samples': mc,
}

# LepCut2l__ele_mvaWinter22V2Iso_WP90_noLostHits_ttHMVA_90__mu_cut_TightMiniIso_HWW_ttHMVA_67
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'cut_TightMiniIso_HWW'

aliases['LepWPCut__ele_' + eleWP + '_noLostHits_ttHMVA_90__mu_' + muWP + '_ttHMVA_67'] = {
    'expr': 'LepCut2l__ele_' + eleWP + '__mu_' + muWP + ' && \
             ( ( (abs(Lepton_pdgId[0]) == 13 && Electron_lostHits[Lepton_electronIdx[0]] == 0 && Lepton_ttHMVA_Run3[Lepton_muonIdx[0]]>0.67) || (abs(Lepton_pdgId[0]) == 11 && Lepton_ttHMVA_Run3[Lepton_electronIdx[0]]>0.90) ) && \
               ( (abs(Lepton_pdgId[1]) == 13 && Electron_lostHits[Lepton_electronIdx[1]] == 0 && Lepton_ttHMVA_Run3[Lepton_muonIdx[1]]>0.67) || (abs(Lepton_pdgId[1]) == 11 && Lepton_ttHMVA_Run3[Lepton_electronIdx[1]]>0.90) ) ) \
    ',
    'samples': mc,
}

# LepCut2l__ele_mvaWinter22V2Iso_WP90_noLostHits_ttHMVA_90__mu_cut_MediumMiniIso_HWW_ttHMVA_67
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'cut_MediumMiniIso_HWW'

aliases['LepWPCut__ele_' + eleWP + '_noLostHits_ttHMVA_90__mu_' + muWP + '_ttHMVA_67'] = {
    'expr' : 'nLepton > 1 ? \
              ( ( (abs(Lepton_pdgId[0]) == 13 && abs(Lepton_eta[0]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[0]]) < 0.1 && ((Lepton_pt[0] <= 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.01) || (Lepton_pt[0] > 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.02)) && Muon_mediumId[Lepton_muonIdx[0]] == 1 && Muon_miniIsoId[Lepton_muonIdx[0]] >= 3 && Lepton_ttHMVA_Run3[Lepton_muonIdx[0]]>0.67) || (abs(Lepton_pdgId[0]) == 11 && Lepton_isTightElectron_' + eleWP + '[0]>0.5 && Electron_lostHits[Lepton_electronIdx[0]] == 0 && Lepton_ttHMVA_Run3[Lepton_electronIdx[0]]>0.90) ) && \
              ( ( (abs(Lepton_pdgId[1]) == 13 && abs(Lepton_eta[1]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[1]]) < 0.1 && ((Lepton_pt[1] <= 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.01) || (Lepton_pt[1] > 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.02)) && Muon_mediumId[Lepton_muonIdx[1]] == 1 && Muon_miniIsoId[Lepton_muonIdx[1]] >= 3 && Lepton_ttHMVA_Run3[Lepton_muonIdx[1]]>0.67) || (abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_' + eleWP + '[1]>0.5 && Electron_lostHits[Lepton_electronIdx[1]] == 0 && Lepton_ttHMVA_Run3[Lepton_electronIdx[1]]>0.90) ) ) ) : 0',
    'samples': mc,
}

# LepCut2l__ele_mvaWinter22V2Iso_WP90_noLostHits_ttHMVA_90__mu_mvaMuID_WP_mediumMiniIso_HWW_ttHMVA_67
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'mvaMuID_WP_mediumMiniIso_HWW'

aliases['LepWPCut__ele_' + eleWP + '_noLostHits_ttHMVA_90__mu_' + muWP + '_ttHMVA_67'] = {
    'expr' : 'nLepton > 1 ? \
              ( ( (abs(Lepton_pdgId[0]) == 13 && abs(Lepton_eta[0]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[0]]) < 0.1 && ((Lepton_pt[0] <= 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.01) || (Lepton_pt[0] > 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[0]] >= 1 && Muon_miniIsoId[Lepton_muonIdx[0]] >= 3 && Lepton_ttHMVA_Run3[Lepton_muonIdx[0]]>0.67) || (abs(Lepton_pdgId[0]) == 11 && Lepton_isTightElectron_' + eleWP + '[0]>0.5 && Electron_lostHits[Lepton_electronIdx[0]] == 0 && Lepton_ttHMVA_Run3[Lepton_electronIdx[0]]>0.90) ) && \
              ( ( (abs(Lepton_pdgId[1]) == 13 && abs(Lepton_eta[1]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[1]]) < 0.1 && ((Lepton_pt[1] <= 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.01) || (Lepton_pt[1] > 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[1]] >= 1 && Muon_miniIsoId[Lepton_muonIdx[1]] >= 3 && Lepton_ttHMVA_Run3[Lepton_muonIdx[1]]>0.67) || (abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_' + eleWP + '[1]>0.5 && Electron_lostHits[Lepton_electronIdx[1]] == 0 && Lepton_ttHMVA_Run3[Lepton_electronIdx[1]]>0.90) ) ) ) : 0',
    'samples': mc,
}

# LepCut2l__ele_mvaWinter22V2Iso_WP90_noLostHits_ttHMVA_90__mu_mvaMuID_WP_tightMiniIso_HWW_ttHMVA_67
eleWP = 'mvaWinter22V2Iso_WP90'
muWP  = 'mvaMuID_WP_tightMiniIso_HWW'

aliases['LepWPCut__ele_' + eleWP + '_noLostHits_ttHMVA_90__mu_' + muWP + '_ttHMVA_67'] = {
    'expr' : 'nLepton > 1 ? \
              ( ( (abs(Lepton_pdgId[0]) == 13 && abs(Lepton_eta[0]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[0]]) < 0.1 && ((Lepton_pt[0] <= 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.01) || (Lepton_pt[0] > 20 && abs(Muon_dxy[Lepton_muonIdx[0]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[0]] >= 2 && Muon_miniIsoId[Lepton_muonIdx[0]] >= 3 && Lepton_ttHMVA_Run3[Lepton_muonIdx[0]]>0.67) || (abs(Lepton_pdgId[0]) == 11 && Lepton_isTightElectron_' + eleWP + '[0]>0.5 && Electron_lostHits[Lepton_electronIdx[0]] == 0 && Lepton_ttHMVA_Run3[Lepton_electronIdx[0]]>0.90) ) && \
              ( ( (abs(Lepton_pdgId[1]) == 13 && abs(Lepton_eta[1]) < 2.4 && abs(Muon_dz[Lepton_muonIdx[1]]) < 0.1 && ((Lepton_pt[1] <= 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.01) || (Lepton_pt[1] > 20 && abs(Muon_dxy[Lepton_muonIdx[1]]) < 0.02)) && Muon_mvaMuID_WP[Lepton_muonIdx[1]] >= 2 && Muon_miniIsoId[Lepton_muonIdx[1]] >= 3 && Lepton_ttHMVA_Run3[Lepton_muonIdx[1]]>0.67) || (abs(Lepton_pdgId[1]) == 11 && Lepton_isTightElectron_' + eleWP + '[1]>0.5 && Electron_lostHits[Lepton_electronIdx[1]] == 0 && Lepton_ttHMVA_Run3[Lepton_electronIdx[1]]>0.90) ) ) ) : 0',
    'samples': mc,
}


##########################################################################
# B-Tagging WP: https://btv-wiki.docs.cern.ch/ScaleFactors/Run3Summer22EE/
##########################################################################

# Algo / WP / WP cut
btagging_WPs = {
    "DeepFlavB" : {
        "loose"    : "0.0614",
        "medium"   : "0.3196",
        "tight"    : "0.7300",
        "xtight"   : "0.8184",
        "xxtight"  : "0.9542",
    },
    "RobustParTAK4B" : {
        "loose"    : "0.0897",
        "medium"   : "0.4510",
        "tight"    : "0.8604",
        "xtight"   : "0.9234",
        "xxtight"  : "0.9893",
    },
    "PNetB" : {
        "loose"    : "0.0499",
        "medium"   : "0.2605",
        "tight"    : "0.6915",    
        "xtight"   : "0.8033",
        "xxtight"  : "0.9664",
    }
}

# Algo / SF name
btagging_SFs = {
    "DeepFlavB"      : "deepjet",
    "RobustParTAK4B" : "partTransformer",
    "PNetB"          : "deepjet",
}

# Algorithm and WP selection
bAlgo = 'DeepFlavB' # ['DeepFlavB','RobustParTAK4B','PNetB'] 
WP    = 'loose'     # ['loose','medium','tight','xtight','xxtight']

# Access information from dictionaries
bWP   = btagging_WPs[bAlgo][WP]
bSF   = btagging_SFs[bAlgo]

# B tagging selections and scale factors
aliases['bVeto'] = {
    'expr': f'Sum(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{bAlgo}, CleanJet_jetIdx) > {bWP}) == 0'
}

aliases['bVetoSF'] = {
    'expr': 'TMath::Exp(Sum(LogVec((CleanJet_pt>20 && abs(CleanJet_eta)<2.5)*Take(Jet_btagSF_{}_shape, CleanJet_jetIdx)+1*(CleanJet_pt<20 || abs(CleanJet_eta)>2.5))))'.format(bSF),
    'samples': mc
}

aliases['bReq'] = { 
    'expr': f'Sum(CleanJet_pt > 30. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{bAlgo}, CleanJet_jetIdx) > {bWP}) >= 1'
}

aliases['bReqSF'] = {
    'expr': 'TMath::Exp(Sum(LogVec((CleanJet_pt>30 && abs(CleanJet_eta)<2.5)*Take(Jet_btagSF_{}_shape, CleanJet_jetIdx)+1*(CleanJet_pt<30 || abs(CleanJet_eta)>2.5))))'.format(bSF),
    'samples': mc
}

# No jet with pt > 30 GeV
aliases['zeroJet'] = {
    'expr': 'Alt(CleanJet_pt, 0, 0) < 30.'
}

aliases['oneJet'] = {
    'expr': 'Alt(CleanJet_pt, 0, 0) > 30.'
}

aliases['multiJet'] = {
    'expr': 'Alt(CleanJet_pt, 1, 0) > 30.'
}
    
# Top control region
aliases['topcr'] = {
    'expr': 'mtw2>30 && mll>50 && ((zeroJet && !bVeto) || bReq)'
}

# WW control region
aliases['wwcr'] = {
    'expr': 'mth>60 && mtw2>30 && mll>100 && bVeto'
}

# Overall b tag SF
aliases['btagSF'] = {
    'expr': '(bVeto || (topcr && zeroJet))*bVetoSF + (topcr && !zeroJet)*bReqSF',
    'samples': mc
}

# Systematic uncertainty variations
for shift in ['jes','lf','hf','lfstats1','lfstats2','hfstats1','hfstats2','cferr1','cferr2']:

    for targ in ['bVeto', 'bReq']:
        alias = aliases['%sSF%sup' % (targ, shift)] = copy.deepcopy(aliases['%sSF' % targ])
        alias['expr'] = alias['expr'].replace('btagSF_deepjet_shape', 'btagSF_deepjet_shape_up_%s' % shift)

        alias = aliases['%sSF%sdown' % (targ, shift)] = copy.deepcopy(aliases['%sSF' % targ])
        alias['expr'] = alias['expr'].replace('btagSF_deepjet_shape', 'btagSF_deepjet_shape_down_%s' % shift)

    aliases['btagSF%sup' % shift] = {
        'expr': aliases['btagSF']['expr'].replace('SF', 'SF' + shift + 'up'),
        'samples': mc
    }

    aliases['btagSF%sdown' % shift] = {
        'expr': aliases['btagSF']['expr'].replace('SF', 'SF' + shift + 'down'),
        'samples': mc
    }

##########################################################################
# End of b tagging
##########################################################################

# Lepton IDs
############

### Muons:

# - cut_TightID_POG
#   + abs(Muon_eta) < 2.4
#   + abs(Muon_dz) < 0.1
#   + Muon_pt <= 20.0 : abs(Muon_dxy) < 0.01
#   + Muon_pt >  20.0 : abs(Muon_dxy) < 0.02
#   + Muon_tightId

# - cut_Tight_HWW
#   + abs(Muon_eta) < 2.4
#   + abs(Muon_dz) < 0.1
#   + Muon_pt <= 20.0 : abs(Muon_dxy) < 0.01
#   + Muon_pt >  20.0 : abs(Muon_dxy) < 0.02
#   + Muon_tightId
#   + Muon_pfIsoId >= 4

# - cut_TightMiniIso_HWW
#   + abs(Muon_eta) < 2.4
#   + abs(Muon_dz) < 0.1
#   + Muon_pt <= 20.0 : abs(Muon_dxy) < 0.01
#   + Muon_pt >  20.0 : abs(Muon_dxy) < 0.02
#   + Muon_tightId
#   + Muon_miniIsoId >= 3


# - cut_MediumID_POG
#   + abs(Muon_eta) < 2.4
#   + abs(Muon_dz) < 0.1
#   + Muon_pt <= 20.0 : abs(Muon_dxy) < 0.01
#   + Muon_pt >  20.0 : abs(Muon_dxy) < 0.02
#   + Muon_mediumId

# - cut_Medium_HWW
#   + abs(Muon_eta) < 2.4
#   + abs(Muon_dz) < 0.1
#   + Muon_pt <= 20.0 : abs(Muon_dxy) < 0.01
#   + Muon_pt >  20.0 : abs(Muon_dxy) < 0.02
#   + Muon_mediumId
#   + Muon_pfIsoId >= 4

# - cut_MediumMiniIso_HWW
#   + abs(Muon_eta) < 2.4
#   + abs(Muon_dz) < 0.1
#   + Muon_pt <= 20.0 : abs(Muon_dxy) < 0.01
#   + Muon_pt >  20.0 : abs(Muon_dxy) < 0.02
#   + Muon_mediumId
#   + Muon_miniIsoId >= 3


# - mvaMuID_WP_medium
#   + abs(Muon_eta) < 2.4
#   + abs(Muon_dz) < 0.1
#   + Muon_pt <= 20.0 : abs(Muon_dxy) < 0.01
#   + Muon_pt >  20.0 : abs(Muon_dxy) < 0.02
#   + Muon_mvaMuID_WP >= 1

# - mvaMuID_WP_medium_HWW
#   + abs(Muon_eta) < 2.4
#   + abs(Muon_dz) < 0.1
#   + Muon_pt <= 20.0 : abs(Muon_dxy) < 0.01
#   + Muon_pt >  20.0 : abs(Muon_dxy) < 0.02
#   + Muon_mvaMuID_WP >= 1
#   + Muon_pfRelIso04_all < 0.15

# - mvaMuID_WP_medium_miniIso_HWW
#   + abs(Muon_eta) < 2.4
#   + abs(Muon_dz) < 0.1
#   + Muon_pt <= 20.0 : abs(Muon_dxy) < 0.01
#   + Muon_pt >  20.0 : abs(Muon_dxy) < 0.02
#   + Muon_mvaMuID_WP >= 1
#   + Muon_miniIsoId >= 3


# - mvaMuID_WP_tight
#   + abs(Muon_eta) < 2.4
#   + abs(Muon_dz) < 0.1
#   + Muon_pt <= 20.0 : abs(Muon_dxy) < 0.01
#   + Muon_pt >  20.0 : abs(Muon_dxy) < 0.02
#   + Muon_mvaMuID_WP >= 2

# - mvaMuID_WP_tight_HWW
#   + abs(Muon_eta) < 2.4
#   + abs(Muon_dz) < 0.1
#   + Muon_pt <= 20.0 : abs(Muon_dxy) < 0.01
#   + Muon_pt >  20.0 : abs(Muon_dxy) < 0.02
#   + Muon_mvaMuID_WP >= 2
#   + Muon_pfRelIso04_all < 0.15

# - mvaMuID_WP_tight_miniIso_HWW
#   + abs(Muon_eta) < 2.4
#   + abs(Muon_dz) < 0.1
#   + Muon_pt <= 20.0 : abs(Muon_dxy) < 0.01
#   + Muon_pt >  20.0 : abs(Muon_dxy) < 0.02
#   + Muon_mvaMuID_WP >= 2
#   + Muon_miniIsoId >= 3


### Electrons:

# - wp90iso
#   + abs(Electron_eta) < 2.5
#   + Electron_mvaIso_WP90
#   + Electron_convVeto

# - mvaWinter22V2Iso_WP90
#   + abs(Electron_eta) < 2.5
#   + Electron_mvaIso_WP90
#   + Electron_convVeto
#   + Electron_pfRelIso03_all < 0.06
#   + abs(Electron_eta) <= 1.479 : abs(Electron_dxy) < 0.05 and abs(Electron_dz)  < 0.1
#   + abs(Electron_eta) >  1.479 : abs(Electron_dxy) < 0.1  and abs(Electron_dz)  < 0.2
