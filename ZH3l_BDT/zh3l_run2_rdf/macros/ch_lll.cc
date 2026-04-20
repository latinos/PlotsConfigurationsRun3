#ifndef whchlll
#define whchlll


#include <vector>

#include "TVector2.h"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"

#include <iostream>
#include "ROOT/RVec.hxx"
#include "TLorentzVector.h"

using namespace ROOT;
using namespace ROOT::VecOps;

float ch_lll(int   nLepton,
			 RVecF Lepton_pt,
			 RVecF Lepton_eta,
			 RVecF Lepton_phi,
			 RVecF Lepton_pdgId){
  

  // Create default value
  float ch_lll = -9999.0;
  
  // Check that we have at least 3 good leptons
  if (nLepton < 3) return ch_lll;
  
  bool WH3l_ok = abs( abs(Lepton_pdgId[0])/Lepton_pdgId[0] + abs(Lepton_pdgId[1])/Lepton_pdgId[1] + abs(Lepton_pdgId[2])/Lepton_pdgId[2] ) <= 1;
  if (!WH3l_ok) return ch_lll;

  ch_lll = abs(Lepton_pdgId[0])/Lepton_pdgId[0] + abs(Lepton_pdgId[1])/Lepton_pdgId[1] + abs(Lepton_pdgId[2])/Lepton_pdgId[2];
  
  return ch_lll;
}


#endif
