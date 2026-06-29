#ifndef whmlll
#define whmlll


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

float m_lll(int   nLepton,
			RVecF Lepton_pt,
			RVecF Lepton_eta,
			RVecF Lepton_phi,
			RVecF Lepton_pdgId){


  // Create default value
  float mlll = -9999.0;
  
  // Check that we have at least 3 good leptons
  if (nLepton < 3) return mlll;

  bool WH3l_ok = abs( abs(Lepton_pdgId[0])/Lepton_pdgId[0] + abs(Lepton_pdgId[1])/Lepton_pdgId[1] + abs(Lepton_pdgId[2])/Lepton_pdgId[2] ) <= 1;
  if (!WH3l_ok) return mlll;

  // Initialize leptons 4-vectors
  std::vector<ROOT::Math::PtEtaPhiMVector> leptons_vector = {
	ROOT::Math::PtEtaPhiMVector(Lepton_pt[0],Lepton_eta[0],Lepton_phi[0],0),
	ROOT::Math::PtEtaPhiMVector(Lepton_pt[1],Lepton_eta[1],Lepton_phi[1],0),
	ROOT::Math::PtEtaPhiMVector(Lepton_pt[2],Lepton_eta[2],Lepton_phi[2],0)
  };

  mlll = (leptons_vector[0] + leptons_vector[1] + leptons_vector[2]).M();

  return mlll;
  
}


#endif
