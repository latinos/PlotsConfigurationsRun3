import os
import copy
import inspect
import ROOT

ROOT.gSystem.Load("libGpad.so")
ROOT.gSystem.Load("libGraf.so")

configurations = os.path.realpath(inspect.getfile(inspect.currentframe()))
macros = os.path.dirname(configurations) + '/macros/'
fakerates = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(configurations)))) + '/utils/data/FakeRate'
btagmaps = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(configurations)))) + '/utils/data/btag'
print(macros)
print(fakerates)
print(btagmaps)


aliases = {}
aliases = OrderedDict()

mc     = [skey for skey in samples if skey not in ('Fake', 'DATA')]
mc_emb = [skey for skey in samples if skey not in ('Fake', 'DATA')]


# LepSF2l__ele_cutBased_LooseID_tthMVA_Run3__mu_cut_TightID_pfIsoTight_HWW_tthmva_67
eleWP = 'cutBased_MediumID_tthMVA_Run3'
muWP  = 'cut_TightID_pfIsoTight_HWW_tthmva_67'

aliases['LepWPCut'] = {
    'expr': 'LepCut2l__ele_'+eleWP+'__mu_'+muWP,
    'samples': mc + ['DATA'],
}

aliases['LepWPSF'] = {
    'expr': 'LepSF2l__ele_'+eleWP+'__mu_'+muWP,
    'samples': mc
}

# gen-matching to prompt only (GenLepMatch2l matches to *any* gen lepton)
aliases['PromptGenLepMatch2l'] = {
    'expr': 'Alt(Lepton_promptgenmatched, 0, 0) * Alt(Lepton_promptgenmatched, 1, 0)',
    'samples': mc
}

aliases['PromptGenLepMatch1l'] = {
    'expr': '(Alt(Lepton_promptgenmatched, 0, 0) + Alt(Lepton_promptgenmatched, 1, 0)) >= 1',
    'samples': mc
}

# Conept
"""
aliases['Lepton_conept'] = {
    'expr': 'LeptonConePt(Lepton_pt, Lepton_pdgId, Lepton_electronIdx, Lepton_muonIdx, Electron_jetRelIso, Muon_jetRelIso)',
    'linesToAdd': [f'#include "{macros}LeptonConePt_class.cc"'],
    'samples': mc + ['Fake', 'DATA', 'DATA_unprescaled']
}
"""

# Fake leptons transfer factor
aliases['fakeW'] = {
    'linesToAdd'     : [f'#include "{macros}fake_rate_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.ProcessLine('fake_rate_reader fr_reader = fake_rate_reader(\"cutBased_LooseID_tthMVA_Run3\", \"{muWP}\", \"nominal\", 2, \"std\", \"{fakerates}\", \"2024_v15_pt\");')"],
    'expr'           : f'fr_reader(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_{muWP}, Lepton_isTightElectron_{eleWP}, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}

aliases['gstarLow'] = {
    'expr': 'Gen_ZGstar_mass > 0 && Gen_ZGstar_mass < 4',
    'samples': ['WZ', 'VgS', 'Vg']
}
aliases['gstarHigh'] = {
    'expr': 'Gen_ZGstar_mass < 0 || Gen_ZGstar_mass > 4',
    'samples': ['WZ', 'VgS', 'Vg'],
}

aliases['Top_pTrw'] = {
    'expr': '(topGenPt * antitopGenPt > 0.) * (TMath::Sqrt((0.103*TMath::Exp(-0.0118*topGenPt) - 0.000134*topGenPt + 0.973) * (0.103*TMath::Exp(-0.0118*antitopGenPt) - 0.000134*antitopGenPt + 0.973))) + (topGenPt * antitopGenPt <= 0.)',
    'samples': ['top']
}

# Jet bins
# using Alt(CleanJet_pt, n, 0) instead of Sum(CleanJet_pt >= 30) because jet pt ordering is not strictly followed in JES-varied samples

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

aliases['noJetInHorn'] = {
    'expr' : 'Sum(CleanJet_pt > 30 && CleanJet_pt < 50 && abs(CleanJet_eta) > 2.5 && abs(CleanJet_eta) < 3.0) == 0',
}

########################################################################
# B-Tagging WP: https://btv-wiki.docs.cern.ch/ScaleFactors/Run3Summer23/
########################################################################

# Algo / WP / WP cut
btagging_WPs = {
    "UParTAK4B" : {"loose" : "0.0246", "medium" : "0.1272", "tight" : "0.4648", "xtight" : "0.6298", "xxtight" : "0.9739"},
}

# Algo / SF name
btagging_SFs = {
    "UParTAK4B"      : "upart",
}

# Algorithm and WP selection
bAlgo = 'UParTAK4B'
WP    = 'loose'     # ['loose','medium','tight','xtight','xxtight']

WP_eval = 'L' # ['L', 'M', 'T', 'XT', 'XXT']
tagger = 'UParTAK4'

# Access information from dictionaries
bWP   = btagging_WPs[bAlgo][WP]

# B tagging selections and scale factors
aliases['bVeto'] = {
    'expr': f'Sum(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{bAlgo}, CleanJet_jetIdx) > {bWP}) == 0'
}

aliases['bReq'] = { 
    'expr': f'Sum(CleanJet_pt > 30. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{bAlgo}, CleanJet_jetIdx) > {bWP}) >= 1'
}

##########################################################################
# End of b tagging
##########################################################################

eff_map_year = '2024' # ['2022', '2022EE', '2023', '2023BPix']
year = 'Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15' # ['Run3-22CDSep23-Summer22-NanoAODv12', 'Run3-22EFGSep23-Summer22EE-NanoAODv12, 'Run3-23CSep23-Summer23-NanoAODv12', 'Run3-23DSep23-Summer23BPix-NanoAODv12', 'Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15']

for flavour in ['bc', 'light']:
    for shift in ['central', 'down_correlated', 'down_uncorrelated', 'up_correlated', 'up_uncorrelated']:
        btagsf = 'btagSF' + flavour
        if shift != 'central':
            btagsf += '_' + shift
        aliases[btagsf] = {
            'linesToAdd': [f'#include "{macros}evaluate_btagSF{flavour}.cc"'],
            'linesToProcess': [f"ROOT.gInterpreter.ProcessLine('btagSF{flavour} btagSF{flavour}_{shift} = btagSF{flavour}(\"{btagmaps}/{eff_map_year}/bTagEff_{eff_map_year}_ttbar_{bAlgo}_loose.root\", \"{year}\");')"],
            'expr': f'btagSF{flavour}_{shift}(CleanJet_pt, CleanJet_eta, CleanJet_jetIdx, nCleanJet, Jet_hadronFlavour, Jet_btag{bAlgo}, "{WP_eval}", "{shift}", "{tagger}","{eff_map_year}")',
            'samples' : mc,
        }

# Number of hard (= gen-matched) jets                                                                                                                                                                      
aliases['nHardJets'] = {
    'expr'    :  'Sum(Take(Jet_genJetIdx,CleanJet_jetIdx) >= 0 && Take(GenJet_pt,Take(Jet_genJetIdx,CleanJet_jetIdx)) > 25)',
    'samples' : mc
}

# CR definition
aliases['topcr'] = {
    'expr': 'mtw2 > 30 && mll > 50 && ((zeroJet && !bVeto) || bReq)'
}
aliases['dycr'] = {
    'expr': 'mth < 60 && mll > 40 && mll < 80 && bVeto && mtw2 > 30'
}
aliases['wwcr'] = {
    'expr': 'mth > 60 && mtw2 > 30 && mll > 100 && bVeto'
}


# SR definition
aliases['sr'] = {
    'expr': 'mth > 60 && mth < 125 && mtw2 > 30 && bVeto && mll < 55' #DM Tune mll cut!
}

# Data/MC scale factors and systematic uncertainties
aliases['SFweight'] = {
    'expr': ' * '.join(['SFweight2l', 'LepWPCut', 'LepWPSF', 'btagSFbc', ' btagSFlight']),
    'samples': mc
}

aliases['SFweightEleUp'] = {
    'expr': 'LepSF2l__ele_'+eleWP+'__Up',
    'samples': mc
}
aliases['SFweightEleDown'] = {
    'expr': 'LepSF2l__ele_'+eleWP+'__Down',
    'samples': mc
}
aliases['SFweightMuUp'] = {
    'expr': 'LepSF2l__mu_'+muWP+'__Up',
    'samples': mc
}
aliases['SFweightMuDown'] = {
    'expr': 'LepSF2l__mu_'+muWP+'__Down',
    'samples': mc
}

###########################################
##      AC/EFT Analysis specific         ##
###########################################

## VH AC sample normalisation from rewighting of SM

aliases['xsec_zh']        = { 'expr': '0.05'}
aliases['ZH_H0PM_N']      = { 'expr': ' xsec_zh'}
aliases['ZH_H0PH_N']      = { 'expr': ' xsec_zh*62.02'} 
aliases['ZH_H0M_N']       = { 'expr': ' xsec_zh*15.81'} 
aliases['ZH_H0L1_N']      = { 'expr': ' xsec_zh*1.96e-14'} 
aliases['ZH_H0PHf05_N']   = { 'expr': ' xsec_zh*0.57'} 
aliases['ZH_H0Mf05_N']    = { 'expr': ' xsec_zh*2.05'} 
aliases['ZH_H0L1f05_N']   = { 'expr': ' xsec_zh*0.69'}
aliases['ZH_H0LZgf05_N']  = { 'expr': ' xsec_zh*2.36'} 
aliases['ZH_H0PHZgf05_N'] = { 'expr': ' xsec_zh*2.78'} 
aliases['ZH_H0MZgf05_N']  = { 'expr': ' xsec_zh*2.34'} 
aliases['ZH_H0PHggf05_N'] = { 'expr': ' xsec_zh*4.82'} 
aliases['ZH_H0Mggf05_N']  = { 'expr': ' xsec_zh*5.04'}

aliases['xsec_wh']        = { 'expr': '0.04'}
aliases['WH_H0PM_N']      = { 'expr': ' xsec_wh'}
aliases['WH_H0PH_N']      = { 'expr': ' xsec_wh*79.91'} 
aliases['WH_H0M_N']       = { 'expr': ' xsec_wh*21.7'} 
aliases['WH_H0L1_N']      = { 'expr': ' xsec_wh*1.91e-14'} 
aliases['WH_H0PHf05_N']   = { 'expr': ' xsec_wh*0.62'} 
aliases['WH_H0Mf05_N']    = { 'expr': ' xsec_wh*2.03'} 
aliases['WH_H0L1f05_N']   = { 'expr': ' xsec_wh*0.77'}

## gen ME weight for each signal reweighting

configurations = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(configurations))))) 

aliases['MELALib'] = {
  'linesToAdd':[f'#include "'+configurations+'/mkShapesRDF/JHUGenMELA/MELA/interface/Mela.h"'],
  'linesToProcess':[f'ROOT.gSystem.Load("'+configurations+'/mkShapesRDF/JHUGenMELA/MELA/data/el9_amd64_gcc12/libJHUGenMELAMELA.so","", ROOT.kTRUE)']
}

aliases['ToolsLib'] = {
  'linesToAdd':[f'#include "'+configurations+'/PlotsConfigurationsRun3/HWW_AC/macros/GenTools.cc"'],
}

for sig in reweight_ZH :
 hyp1 = ''.join(sig.split("ZH_")[1].split("to")[0])
 hyp2 = sig.split("to")[1]
 print("Reweight ZH ", hyp1," to ", hyp2," for ", cvtype_ZH," scenario")

 aliases['ZH_'+hyp1+'to'+hyp2+'_W'] = {
   'linesToAdd':[f'#include "'+configurations+'/PlotsConfigurationsRun3/HWW_AC/macros/GenWeight_HVV.cc"'],
   'linesToProcess':[f'ROOT.gInterpreter.Declare("GENWEIGHT_HVV mWgt_ZH;")'],
   'expr' :   f'mWgt_ZH("zh","'+hyp1+'","'+hyp2+'","'+cvtype_ZH+'", nLHEPart, nGenPart, LHEPart_pt, LHEPart_eta, LHEPart_phi, LHEPart_pdgId, LHEPart_status, GenPart_pt, GenPart_eta, GenPart_phi, GenPart_pdgId, GenPart_genPartIdxMother, Generator_x1, Generator_x2, Generator_id1, Generator_id2)',
   'samples': [''+sig+'']
 }

for sig in reweight_WH :
 hyp1 = ''.join(sig.split("WH_")[1].split("to")[0])
 hyp2 = sig.split("to")[1]
 print("Reweight WH ", hyp1," to ", hyp2," for ", cvtype_WH," scenario")

 aliases['WH_'+hyp1+'to'+hyp2+'_W'] = {
   'linesToAdd':[f'#include "'+configurations+'/PlotsConfigurationsRun3/HWW_AC/macros/GenWeight_HVV.cc"'],
   'linesToProcess':[f'ROOT.gInterpreter.Declare("GENWEIGHT_HVV mWgt_WH;")'],
   'expr' :   f'mWgt_WH("wh","'+hyp1+'","'+hyp2+'","'+cvtype_WH+'", nLHEPart, nGenPart, LHEPart_pt, LHEPart_eta, LHEPart_phi, LHEPart_pdgId, LHEPart_status, GenPart_pt, GenPart_eta, GenPart_phi, GenPart_pdgId, GenPart_genPartIdxMother, Generator_x1, Generator_x2, Generator_id1, Generator_id2)',
   'samples': [''+sig+'']
 }
 
## Reco ME for H+2 jet discriminant

aliases['me_zh'] = {
   'linesToAdd':[f'#include "'+configurations+'/PlotsConfigurationsRun3/HWW_AC/macros/RecoME_JJH.cc"'],
   'linesToProcess':[f'ROOT.gInterpreter.Declare("RECOME_JJH mZH;")'],
   'expr' :   f'mZH(TVar::Had_ZH, nCleanJet, nLepton, PuppiMET_pt, PuppiMET_phi, Lepton_pt, Lepton_phi, Lepton_eta, CleanJet_pt, CleanJet_phi, CleanJet_eta)',
   'afterNuis': True
}

aliases['me_wh'] = {
   'linesToAdd':[f'#include "'+configurations+'/PlotsConfigurationsRun3/HWW_AC/macros/RecoME_JJH.cc"'],
   'linesToProcess':[f'ROOT.gInterpreter.Declare("RECOME_JJH mWH;")'],
   'expr' :   f'mWH(TVar::Had_WH, nCleanJet, nLepton, PuppiMET_pt, PuppiMET_phi, Lepton_pt, Lepton_phi, Lepton_eta, CleanJet_pt, CleanJet_phi, CleanJet_eta)',
   'afterNuis': True
}

aliases['me_qcd'] = {
   'linesToAdd':[f'#include "'+configurations+'/PlotsConfigurationsRun3/HWW_AC/macros/RecoME_JJH.cc"'],
   'linesToProcess':[f'ROOT.gInterpreter.Declare("RECOME_JJH mQCD;")'],
   'expr' :   f'mQCD(TVar::JJQCD, nCleanJet, nLepton, PuppiMET_pt, PuppiMET_phi, Lepton_pt, Lepton_phi, Lepton_eta, CleanJet_pt, CleanJet_phi, CleanJet_eta)',
   'afterNuis': True
}

## VH KDs

aliases['kd'] = {
   'linesToAdd':[f'#include "'+configurations+'/PlotsConfigurationsRun3/HWW_AC/macros/RecoKD_VH.cc"'],
   'linesToProcess':[f'ROOT.gInterpreter.Declare("RECOKD_VH mKD;")'],
   'expr' :   f'mKD(me_wh, me_zh, me_qcd)',
   'afterNuis': True
}

aliases['h_mass']   = { 'expr': 'me_wh[0]', 'afterNuis': True }

aliases['kd_vh']    = { 'expr': 'kd[0]', 'afterNuis': True }
aliases['kd_hp']    = { 'expr': 'kd[1]', 'afterNuis': True }
aliases['kd_hm']    = { 'expr': 'kd[2]', 'afterNuis': True }
aliases['kd_hl']    = { 'expr': 'kd[3]', 'afterNuis': True }
aliases['kd_hpzg']  = { 'expr': 'kd[4]', 'afterNuis': True }
aliases['kd_hmzg']  = { 'expr': 'kd[5]', 'afterNuis': True }
aliases['kd_hpgg']  = { 'expr': 'kd[6]', 'afterNuis': True }
aliases['kd_hmgg']  = { 'expr': 'kd[7]', 'afterNuis': True }
aliases['kd_mixhp'] = { 'expr': 'kd[8]', 'afterNuis': True }
aliases['kd_mixhm'] = { 'expr': 'kd[9]', 'afterNuis': True }
aliases['kd_mixhl'] = { 'expr': 'kd[10]','afterNuis': True }



