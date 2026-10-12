
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
