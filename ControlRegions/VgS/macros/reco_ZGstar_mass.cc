
#ifndef RECO_ZGSTAR_MASS
#define RECO_ZGSTAR_MASS


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

float reco_ZGstar_mass(int   nLepton,
				   RVecF Lepton_pt,
				   RVecF Lepton_eta,
				   RVecF Lepton_phi,
				   RVecF Lepton_pdgId){

  // Create default value
  float ZGstar_mass = -9999.0; // default value for ZGstar mass
  
  // Check that we have at least 3 leptons
  if (nLepton < 3) return ZGstar_mass;

  
  // Initialize leptons 4-vectors
  std::vector<ROOT::Math::PtEtaPhiMVector> leptons_vector = {
	ROOT::Math::PtEtaPhiMVector(Lepton_pt[0],Lepton_eta[0],Lepton_phi[0],0),
	ROOT::Math::PtEtaPhiMVector(Lepton_pt[1],Lepton_eta[1],Lepton_phi[1],0),
	ROOT::Math::PtEtaPhiMVector(Lepton_pt[2],Lepton_eta[2],Lepton_phi[2],0)
  };

  // Loop over the three leptons
  // for (uint i = 0; i < 3; i++)
  // {
  //   for (uint j = i+1; j < 3; j++)
  //   {
  //     float deltaR = ROOT::Math::VectorUtil::DeltaR(leptons_vector[i], leptons_vector[j]);
  //     if (abs(Lepton_pdgId[i]) == abs(Lepton_pdgId[j]) && Lepton_pdgId[i]*Lepton_pdgId[j] < 0)
  //       if (deltaR < min_deltaR)
  //       {
  //         min_deltaR = deltaR;
  //         ZGstar_mass = (leptons_vector[i] + leptons_vector[j]).M();
  //       }
  //   }
  // }
  float deltaR12 = ROOT::Math::VectorUtil::DeltaR(leptons_vector[0], leptons_vector[1]);
  float deltaR13 = ROOT::Math::VectorUtil::DeltaR(leptons_vector[0], leptons_vector[2]);
  float deltaR23 = ROOT::Math::VectorUtil::DeltaR(leptons_vector[1], leptons_vector[2]);

  float min_deltaR = min(min(deltaR12, deltaR13), deltaR23);

  if (min_deltaR == deltaR12)
    ZGstar_mass = (leptons_vector[0] + leptons_vector[1]).M();
  else if (min_deltaR == deltaR13)
    ZGstar_mass = (leptons_vector[0] + leptons_vector[2]).M();
  else if (min_deltaR == deltaR23)
    ZGstar_mass = (leptons_vector[1] + leptons_vector[2]).M();

  return ZGstar_mass;
}


#endif

