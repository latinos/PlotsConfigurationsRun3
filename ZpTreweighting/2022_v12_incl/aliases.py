import os
import copy
import inspect
import ROOT
import json

ROOT.gSystem.Load("libGpad.so")
ROOT.gSystem.Load("libGraf.so")

configurations = os.path.realpath(inspect.getfile(inspect.currentframe()))
print("Current frame = ", inspect.currentframe())
print("Configurations = ", configurations)
macros = os.path.dirname(configurations) + '/macros/'
fakerates = os.path.dirname(os.path.dirname(os.path.dirname(configurations))) + '/utils/data/FakeRate'
btagmaps = os.path.dirname(os.path.dirname(os.path.dirname(configurations))) + '/utils/data/btag'
# # bTagEff.c needs to be run (https://github.com/latinos/PlotsConfigurationsRun3/blob/2c97793c9009904e37f9fb04e357728ae18e0685/utils/btagEff/bTagEff.cc#L126). Make sure to change the output dir path.
print("Macros folder dir = ", macros)
print("Fakerates folder dir = ", fakerates)
print("B-tagging efficiency maps folder dir = ", btagmaps)


aliases = {}
aliases = OrderedDict()

mc     = [skey for skey in samples if skey not in ('Fake', 'DATA')]
mc_emb = [skey for skey in samples if skey not in ('Fake', 'DATA')]

# previous - LepCut2l__ele_cutBased_LooseID_tthMVA_Run3__mu_cut_TightID_pfIsoTight_HWW_tthmva_67
# moved from LooseID to MediumID for new post-processed samples (DS, 22Apr26)
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

aliases['gen_Zpt'] = {
    # 'linesToAdd': [".L /afs/cern.ch/user/d/dshekar/public/RDF/PlotsConfigurationsRun3/HWW_polarization/Extended/getGenZpt.cc+"],
    # 'linesToAdd': ['.L /eos/user/d/dshekar/public/RDF/PlotsConfigurationsRun3/HWW_polarization/Extended/getGenZpt.cc+'],
    'linesToAdd': [
        """
#ifndef getGenZpt
#define getGenZpt

#include <vector>

#include "TVector2.h"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"

#include <iostream>
#include "ROOT/RVec.hxx"

using namespace ROOT;
using namespace ROOT::VecOps;

double GetGenZpt(
		 int          nGenPart, 
		 RVecF  GenPart_pt,
		 RVecI  GenPart_pdgId,
		 RVecI  GenPart_genPartIdxMother,
		 RVecI  GenPart_statusFlags,
		 float  gen_ptll
		 ){



  // Find Gen pT of Z decaying into leptons 
  unsigned nGen = nGenPart;
  std::vector<int> LepCands{};
  std::vector<int> MotherIdx{};
  std::vector<int> MotherPdgId{};
  int pdgId, sFlag, MIdx;
  bool hasZ = false;
  //std::cout << "==========" << std::endl; 
  for (unsigned iGen{0}; iGen != nGen; ++iGen){
    pdgId = std::abs(GenPart_pdgId[iGen]);
    sFlag = GenPart_statusFlags[iGen];
    //std::cout << pdgId << " ; " << sFlag << " ; " << GenPart_pt->At(iGen) << " ; " << GenPart_genPartIdxMother->At(iGen) << std::endl;  
    if (((pdgId == 11) || (pdgId == 13) || (pdgId == 15)) && ((sFlag >> 0 & 1) || (sFlag >> 2 & 1) || (sFlag >> 3 & 1) || (sFlag >> 4 & 1))){
      LepCands.push_back(iGen);
      MIdx = GenPart_genPartIdxMother[iGen];
      MotherIdx.push_back(MIdx);
      if (MIdx > -1){
        MotherPdgId.push_back(GenPart_pdgId[MIdx]);
        if (GenPart_pdgId[MIdx]==23) hasZ = true;
      }else{
        MotherPdgId.push_back(0);
      }
    }
  }

  //std::cout << "Check:" << std::endl;
  for (unsigned iGen{0}; iGen != LepCands.size(); ++iGen){
    for (unsigned jGen{0}; jGen != LepCands.size(); ++jGen){
      if (jGen <= iGen) continue;
      //std::cout << iGen << " ; " << MotherIdx[iGen] << " ; " << jGen << " ; " << MotherIdx[jGen] << " ; " << MotherPdgId[iGen] << " ; " << hasZ << std::endl;
      // Some DY samples generate the Z; others have the two leptons produced directly -> motherId is 0 for those events
      if (hasZ){
        if (MotherIdx[iGen] == MotherIdx[jGen] && MotherPdgId[iGen] == 23) return GenPart_pt[MotherIdx[iGen]];
      }else{
        if (MotherIdx[iGen] == MotherIdx[jGen] && MotherIdx[iGen] == 0) return GenPart_pt[MotherIdx[iGen]];
      }
    }
  }
  //std::cout << "Falling back!" << std::endl; 
  return gen_ptll;

}

#endif
        """],
    'class': 'GetGenZpt',
    'args': 'nGenPart, GenPart_pt, GenPart_pdgId, GenPart_genPartIdxMother, GenPart_statusFlags, gen_ptll',
    # 'expr': 'gen_ptll',
    'samples': mc
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

_dyzptrw_json = os.path.join(os.path.dirname(configurations), 'dyZpTrw.json')
with open(_dyzptrw_json) as _fj:
    DYrew = json.load(_fj)
aliases['DY_NLO_ZpTrw'] = {
    'expr': '(' + DYrew['2022_v12']['LO_0j'].replace('x', 'gen_Zpt') + ')',
            # ' + (' + DYrew['2022_v12']['LO_1j'].replace('x', 'gen_Zpt') + ')*(oneJet&& Alt(CleanJet_pt,1,0)<30)' +
            # ' + (' + DYrew['2022_v12']['LO_2j'].replace('x', 'gen_Zpt') + ')*(multiJet)',
    'samples': ['DY']
}


# Lepton Cone pt
aliases['Lepton_conept'] = {
    'expr': 'LeptonConePt(Lepton_pt, Lepton_pdgId, Lepton_electronIdx, Lepton_muonIdx, Electron_jetRelIso, Muon_jetRelIso)',
    'linesToAdd': [f'#include "{macros}LeptonConePt_class.cc"'],
    'samples': mc + ['Fake', 'DATA', 'DATA_unprescaled']
}

# Fake leptons transfer factor
aliases['fakeW'] = {
    'linesToAdd'     : [f'#include "{macros}fake_rate_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.ProcessLine('fake_rate_reader fr_reader = fake_rate_reader(\"cutBased_LooseID_tthMVA_Run3\", \"{muWP}\", \"nominal\", 2, \"std\", \"{fakerates}\", \"2022_v12_pt\");')"],
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

# Top pT reweighting
aliases['Top_pTrw'] = {
    'expr': '(topGenPt * antitopGenPt > 0.) * (TMath::Sqrt((0.103*TMath::Exp(-0.0118*topGenPt) - 0.000134*topGenPt + 0.973) * (0.103*TMath::Exp(-0.0118*antitopGenPt) - 0.000134*antitopGenPt + 0.973))) + (topGenPt * antitopGenPt <= 0.)',
    'samples': ['top']
}

##########################################################################
# B-Tagging WP: https://btv-wiki.docs.cern.ch/ScaleFactors/Run3Summer22/
##########################################################################

# Algo / WP / WP cut
btagging_WPs = {
    "DeepFlavB" : {"loose": "0.0583", "medium": "0.3086", "tight": "0.7183", "xtight": "0.8111", "xxtight": "0.9512"},
    "RobustParTAK4B" : {"loose": "0.0849", "medium": "0.4319", "tight": "0.8482", "xtight": "0.9151", "xxtight": "0.9874"},
    "PNetB" : {"loose" : "0.0470", "medium" : "0.2450", "tight" : "0.6734", "xtight"  : "0.7862", "xxtight" : "0.9610"}
}

# Algo / SF name
btagging_SFs = {
    "DeepFlavB"      : "deepjet",
    "RobustParTAK4B" : "partTransformer",
    "PNetB"          : "partNet",
}

# Algorithm and WP selection
bAlgo = 'PNetB' # ['DeepFlavB','RobustParTAK4B','PNetB'] 
WP    = 'loose'     # ['loose','medium','tight','xtight','xxtight']

# Access information from dictionaries
bWP   = btagging_WPs[bAlgo][WP]

WP_eval = 'L' # ['L', 'M', 'T', 'XT', 'XXT']
tagger = 'particleNet' # ['deepJet', 'particleNet', 'robustParticleTransformer']

#################
### B-tagging ###
#################

# Fixed BTV wp

# btagging MC efficiencies and SFs are read through the btagSF{flavour} object:
# - the first argument is the MC btagging efficiency root file
# - the second argument is the year from which SFs are retrieved from the POG/BTV json-pog correctionlib directory; 
#   allowed options are = ['2022_Summer22', '2022_Summer22EE', '2023_Summer23', '2023_Summer23BPix']
# The btagSF{flavour}_{shift} constructor executes the actual computation
# In this you specify the WP for the computation and the tagger using the WP_eval and tagger strings.

# We assume that you have the efficiency maps root files in your configuration, as well as the evaluation macros
# If this is not the case, swap configurations with the proper path

# path = "your/path"

eff_map_year = '2022' # ['2022', '2022EE', '2023', '2023BPix', '2024']
year = 'Run3-22CDSep23-Summer22-NanoAODv12' # ['Run3-22CDSep23-Summer22-NanoAODv12', 'Run3-22EFGSep23-Summer22EE-NanoAODv12, 'Run3-23CSep23-Summer23-NanoAODv12', 'Run3-23DSep23-Summer23BPix-NanoAODv12', 'Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15']

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

# Number of hard (= gen-matched jets)
aliases['nHardJets'] = {
    'expr'    :  'Sum(Take(Jet_genJetIdx,CleanJet_jetIdx) >= 0 && Take(GenJet_pt,Take(Jet_genJetIdx,CleanJet_jetIdx)) > 25)',
    'samples' : mc
}

# B tagging selections and scale factors
aliases['bVeto'] = {
    'expr': f'Sum(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{bAlgo}, CleanJet_jetIdx) > {bWP}) == 0'
}

aliases['bReq'] = { 
    'expr': f'Sum(CleanJet_pt > 30. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{bAlgo}, CleanJet_jetIdx) > {bWP}) >= 1'
}


# data/MC scale factors
aliases['SFweight'] = {
    'expr': ' * '.join(['SFweight2l', 'LepWPCut', 'LepWPSF', 'btagSFbc', 'btagSFlight']),
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