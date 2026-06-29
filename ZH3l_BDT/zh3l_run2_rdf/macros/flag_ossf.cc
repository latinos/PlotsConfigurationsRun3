#ifndef flagossf
#define flagossf


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

bool flag_ossf(int   nLepton,
			   RVecF Lepton_pt,
			   RVecF Lepton_eta,
			   RVecF Lepton_phi,
			   RVecF Lepton_pdgId){
  
  // Create default value
  bool flag_OSSF = false;
  
  // Check that we have at least 3 good leptons
  if (nLepton < 3) return flag_OSSF;

  bool WH3l_ok = abs( abs(Lepton_pdgId[0])/Lepton_pdgId[0] + abs(Lepton_pdgId[1])/Lepton_pdgId[1] + abs(Lepton_pdgId[2])/Lepton_pdgId[2] ) <= 1;
  if (!WH3l_ok) return flag_OSSF;

  // Initialize leptons 4-vectors
  std::vector<ROOT::Math::PtEtaPhiMVector> leptons_vector = {
	ROOT::Math::PtEtaPhiMVector(Lepton_pt[0],Lepton_eta[0],Lepton_phi[0],0),
	ROOT::Math::PtEtaPhiMVector(Lepton_pt[1],Lepton_eta[1],Lepton_phi[1],0),
	ROOT::Math::PtEtaPhiMVector(Lepton_pt[2],Lepton_eta[2],Lepton_phi[2],0)
  };

  // Compute minimum difference |mll - mZ|
  float minmllDiffToZ = 9999.0;
  for (uint i = 0; i < 3; i++){
	for (uint j = i+1; j < 3; j++){
	  if ( Lepton_pdgId[i] + Lepton_pdgId[j] != 0 ) continue;
	  float mllDiffToZ = abs( (leptons_vector[i] + leptons_vector[j]).M() - 91.1876 );
	  if ( mllDiffToZ < minmllDiffToZ ) minmllDiffToZ = mllDiffToZ;
	}
  }

  if (minmllDiffToZ != 9999.0) flag_OSSF = true;

  return flag_OSSF;
}


#endif
