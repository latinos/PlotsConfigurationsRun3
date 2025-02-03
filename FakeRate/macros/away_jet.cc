#ifndef drlepjet
#define drlepjet


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

float drlj(float inputJetPt,
		   int   nLepton,
		   int   nCleanJet,
		   RVecF Lepton_pt,
		   RVecF Lepton_eta,
		   RVecF Lepton_phi,
		   RVecF CleanJet_pt,
		   RVecF CleanJet_eta,
		   RVecF CleanJet_phi){
  
  int   away_jet_index = -1;
  float deltaR = 0;

  // Define lepton vector
  if (nLepton < 1) return deltaR;
  ROOT::Math::PtEtaPhiMVector LeptonVector(Lepton_pt[0],Lepton_eta[0],Lepton_phi[0],0);

  // Check if we have at least one jet candidate
  if (nCleanJet < 1) return deltaR;

  // Loop over jets
  for (int iJet = 0; iJet < nCleanJet; ++iJet){

	if (CleanJet_pt[iJet]       < inputJetPt) continue;
	if (abs(CleanJet_eta[iJet]) > 2.5)        continue;
	  
	ROOT::Math::PtEtaPhiMVector CleanJetVector(CleanJet_pt[iJet],CleanJet_eta[iJet],CleanJet_phi[iJet],0);

	// Compute deltaR(lep,jet)
	deltaR = ROOT::Math::VectorUtil::DeltaR(CleanJetVector,LeptonVector);

	// If we find a valid candidate, break the loop
	if (deltaR > 1){
	  away_jet_index = iJet;
	  break;
	}
  }
  
  // std::cout << "deltaR value = " << deltaR << std::endl;
  return deltaR;
}

#endif
