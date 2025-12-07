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
		   RVecF CleanJet_phi
		){
  
  float deltaR = -999.0f;

  if (nLepton < 1) return deltaR;
  // Check if we have at least one jet candidate
  if (nCleanJet < 1) return deltaR;
  ROOT::Math::PtEtaPhiMVector LeptonVector(Lepton_pt[0],Lepton_eta[0],Lepton_phi[0],0);

  const int iJet = 0;

  if ((CleanJet_pt[iJet] > inputJetPt) && (abs(CleanJet_eta[iJet]) < 2.5)){ // if btagging: && (Jet_btagDeepFlavB[CleanJet_jetIdx[iJet]] > bWP)
	ROOT::Math::PtEtaPhiMVector CleanJetVector(CleanJet_pt[iJet],CleanJet_eta[iJet],CleanJet_phi[iJet],0);
	
	// Compute deltaR(lep,jet)
  	deltaR = ROOT::Math::VectorUtil::DeltaR(CleanJetVector,LeptonVector);
  }
  return deltaR;
}

#endif

