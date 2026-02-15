import os
import copy
import inspect

configurations = os.path.realpath(inspect.getfile(inspect.currentframe())) # this file

aliases = {}
aliases = OrderedDict()

mc     = [skey for skey in samples if skey not in ('Fake', 'DATA', 'Dyemb', 'DATA_EG', 'DATA_Mu', 'DATA_EMu', 'Fake_EG', 'Fake_Mu', 'Fake_EMu')]
# Commented out as not used (DS, 19Nov25)
# mc_emb = [skey for skey in samples if skey not in ('Fake', 'DATA', 'DATA_Mu', 'DATA_EMu', 'Fake_EG', 'Fake_Mu', 'Fake_EMu')]

# Using LepSF2l__ele_cutBased_LooseID_tthMVA_Run3__mu_cut_TightID_pfIsoTight_HWW_tthmva_67 from latest git repo push (https://github.com/latinos/PlotsConfigurationsRun3/blob/f8a0f50dfe6301543203d9d260ad721204a2739f/ControlRegions/DY/2022_v12/aliases.py#L14-L15)
eleWP = 'cutBased_LooseID_tthMVA_Run3'
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
    'expr' : 'Sum(CleanJet_pt > 30 && CleanJet_pt < 50 && abs(CleanJet_eta) > 2.6 && abs(CleanJet_eta) < 3.1) == 0',
}

exec(open('dyZpTrw.py', "r").read())
aliases['DY_LO_ZpTrw'] = {
    'expr': '('+DYrew['2022']['LO'].replace('x', 'gen_Zpt')+')*(zeroJet)*(ptll < 50) + 1*(zeroJet)*(ptll >= 50)',
    'samples': ['DY']
}

########################################################################
# B-Tagging WP: https://btv-wiki.docs.cern.ch/ScaleFactors/Run3Summer22/
########################################################################

# Algo / WP / WP cut
btagging_WPs = {
    "DeepFlavB" : {
        "loose"    : "0.0583",
        "medium"   : "0.3086",
        "tight"    : "0.7183",
        "xtight"   : "0.8111",
        "xxtight"  : "0.9512",
    },
    "RobustParTAK4B" : {
        "loose"    : "0.0849",
        "medium"   : "0.4319",
        "tight"    : "0.8482",
        "xtight"   : "0.9151",
        "xxtight"  : "0.9874",
    },
    "PNetB" : {
        "loose"    : "0.0470",
        "medium"   : "0.2450",
        "tight"    : "0.6734",    
        "xtight"   : "0.7862",
        "xxtight"  : "0.9610",
    }
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
bSF   = btagging_SFs[bAlgo]

# # B tagging selections and scale factors
aliases['bVeto'] = {
    'expr': f'Sum(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{bAlgo}, CleanJet_jetIdx) > {bWP}) == 0'
}

aliases['bReq'] = { 
    'expr': f'Sum(CleanJet_pt > 30. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{bAlgo}, CleanJet_jetIdx) > {bWP}) >= 1'
}

# Commenting out, as this was not included in latest git repo (https://github.com/latinos/PlotsConfigurationsRun3/blob/f8a0f50dfe6301543203d9d260ad721204a2739f/ControlRegions/DY/2022_v12/aliases.py#L89-L104)
# aliases['bVetoSF'] = {
#     'expr': 'TMath::Exp(Sum(LogVec((CleanJet_pt>20 && abs(CleanJet_eta)<2.5)*Take(Jet_btagSF_{}_shape, CleanJet_jetIdx)+1*(CleanJet_pt<20 || abs(CleanJet_eta)>2.5))))'.format(bSF),
#     'samples': mc
# }

# aliases['bReqSF'] = {
#     'expr': 'TMath::Exp(Sum(LogVec((CleanJet_pt>30 && abs(CleanJet_eta)<2.5)*Take(Jet_btagSF_{}_shape, CleanJet_jetIdx)+1*(CleanJet_pt<30 || abs(CleanJet_eta)>2.5))))'.format(bSF),
#     'samples': mc
# }

# # Top control region
# aliases['topcr'] = {
#     'expr': 'mtw2>30 && mll>50 && ((zeroJet && !bVeto) || bReq)'
# }

# # WW control region
# aliases['wwcr'] = {
#     'expr': 'mth>60 && mtw2>30 && mll>100 && bVeto'
# }

# # Overall b tag SF
# aliases['btagSF'] = {
#     'expr': '(bVeto || (topcr && zeroJet))*bVetoSF + (topcr && !zeroJet)*bReqSF',
#     'samples': mc
# }

# # Systematic uncertainty variations
# for shift in ['jes','lf','hf','lfstats1','lfstats2','hfstats1','hfstats2','cferr1','cferr2']:

#     for targ in ['bVeto', 'bReq']:
#         alias = aliases['%sSF%sup' % (targ, shift)] = copy.deepcopy(aliases['%sSF' % targ])
#         alias['expr'] = alias['expr'].replace('btagSF_deepjet_shape', 'btagSF_deepjet_shape_up_%s' % shift)

#         alias = aliases['%sSF%sdown' % (targ, shift)] = copy.deepcopy(aliases['%sSF' % targ])
#         alias['expr'] = alias['expr'].replace('btagSF_deepjet_shape', 'btagSF_deepjet_shape_down_%s' % shift)

#     aliases['btagSF%sup' % shift] = {
#         'expr': aliases['btagSF']['expr'].replace('SF', 'SF' + shift + 'up'),
#         'samples': mc
#     }

#     aliases['btagSF%sdown' % shift] = {
#         'expr': aliases['btagSF']['expr'].replace('SF', 'SF' + shift + 'down'),
#         'samples': mc
#     }

##########################################################################
# End of b tagging
##########################################################################

# Data/MC scale factors and systematic uncertainties
aliases['SFweight'] = {
    # 'expr': ' * '.join(['SFweight2l', 'LepWPCut', 'LepWPSF','btagSF']),
    'expr': ' * '.join(['SFweight2l', 'LepWPCut', 'LepWPSF']),
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
