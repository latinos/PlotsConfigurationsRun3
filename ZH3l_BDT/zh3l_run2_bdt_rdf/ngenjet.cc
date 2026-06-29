
#ifndef ngenjet
#define ngenjet

#include <vector>

#include "TVector2.h"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"

#include <iostream>
#include "ROOT/RVec.hxx"

using namespace ROOT;
using namespace ROOT::VecOps;
double CountGenJet(
		    int          nLeptonGen, 
		    RVecB  LeptonGen_isPrompt, 
		    RVecI  LeptonGen_pdgId,
		    RVecF  LeptonGen_pt,
		    RVecF  LeptonGen_eta,
		    RVecF  LeptonGen_phi,
		    RVecF  LeptonGen_mass,
		    int         nPhotonGen,
		    RVecF  PhotonGen_pt,
		    RVecF  PhotonGen_eta,
		    RVecF  PhotonGen_phi,
		    RVecF  PhotonGen_mass,
		    int         nGenJet,
		    RVecF  GenJet_pt,
		    RVecF  GenJet_eta,
		    RVecF  GenJet_phi
		    ){
  unsigned nJ = nGenJet;

  unsigned nL = nLeptonGen;

  std::vector<unsigned> iPromptL{};
  iPromptL.reserve(nL);

  for (unsigned iL{0}; iL != nL; ++iL) {
    if (!LeptonGen_isPrompt[iL])
      continue;

    unsigned absId{static_cast<unsigned>(std::abs(LeptonGen_pdgId[iL]))};
    if (absId != 11 && absId != 13)
      continue;

    iPromptL.push_back(iL);
  }

  if (iPromptL.size() == 0) {
    unsigned n{0};
    for (unsigned iJ{0}; iJ != nJ; ++iJ) {
      if (GenJet_pt[iJ] > 30.)
        ++n;
    }
    return n;
  }

  std::vector<ROOT::Math::PtEtaPhiMVector> dressedLeptons{};
  for (unsigned iL : iPromptL) {
    dressedLeptons.push_back(
			     ROOT::Math::PtEtaPhiMVector(
							 LeptonGen_pt[iL],
							 LeptonGen_eta[iL],
							 LeptonGen_phi[iL],
            LeptonGen_mass[iL]
							 )
			     );
  }
  
  unsigned nP = nPhotonGen;

  for (unsigned iP{0}; iP != nP; ++iP) {
    double minDR2{1000.};
    int iDMin{-1};
    for (unsigned iD{0}; iD != iPromptL.size(); ++iD) {
      unsigned iL{iPromptL[iD]};
      double dEta{LeptonGen_eta[iL] - PhotonGen_eta[iP]};
      double dPhi{TVector2::Phi_mpi_pi(LeptonGen_phi[iL] - PhotonGen_phi[iP])};
      double dR2{dEta * dEta + dPhi * dPhi};
      if (dR2 < minDR2) {
        minDR2 = dR2;
        iDMin = iD;
      }
    }

    if (minDR2 < 0.09)
      dressedLeptons[iDMin] += ROOT::Math::PtEtaPhiMVector(
							   PhotonGen_pt[iP],
							   PhotonGen_eta[iP],
							   PhotonGen_phi[iP],
							   PhotonGen_mass[iP]);
  }

  unsigned n{0};
  for (unsigned iJ{0}; iJ != nJ; ++iJ) {
    if (GenJet_pt[iJ] < 30.)
      continue;

    bool overlap{false};
    for (auto& p4 : dressedLeptons) {
      if (p4.pt() < 10.)
        continue;

      double dEta{p4.eta() - GenJet_eta[iJ]};
      double dPhi{TVector2::Phi_mpi_pi(p4.phi() - GenJet_phi[iJ])};
      if (dEta * dEta + dPhi * dPhi < 0.016) {
        overlap = true;
        break;
      }
    }
    if (!overlap)
      ++n;
  }
  return n;
}

#endif