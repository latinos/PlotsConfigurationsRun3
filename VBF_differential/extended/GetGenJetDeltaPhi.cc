#ifndef GetGenJetDeltaPhi
#define GetGenJetDeltaPhi


#include <vector>
#include "TLorentzVector.h"

#include "TVector2.h"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"

#include <iostream>

#include "ROOT/RVec.hxx"

using namespace ROOT;
using namespace ROOT::VecOps;


double GenJetDeltaPhi(
        int    nLeptonGen, 
		    RVecB  LeptonGen_isPrompt, 
		    RVecI  LeptonGen_pdgId,
		    RVecF  LeptonGen_pt,
		    RVecF  LeptonGen_eta,
		    RVecF  LeptonGen_phi,
		    RVecF  LeptonGen_mass,
		    int    nPhotonGen,
		    RVecF  PhotonGen_pt,
		    RVecF  PhotonGen_eta,
		    RVecF  PhotonGen_phi,
		    RVecF  PhotonGen_mass,
		    int    nGenJet,
		    RVecF  GenJet_pt,
		    RVecF  GenJet_eta,
		    RVecF  GenJet_phi,
		    RVecF  GenJet_mass
        ){


    unsigned nJ = nGenJet;
    unsigned nL = nLeptonGen;


    // Create vector of prompt gen leptons

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

    // If there are no prompt leptons don't bother checking and just count the jets w/ pt > 30
    // Why not returning default value?

  if (iPromptL.size() == 0) {
    unsigned n{0};
    for (unsigned iJ{0}; iJ != nJ; ++iJ) {
      if (GenJet_pt[iJ] > 30.)
        ++n;
    }
  }

  
  // Create prompt gen leptons 4-vectors

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

  // Add to prompt gen leptons the closest gen photon 4-vector 
  // if close enough (dR < 0.09) - FSR

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
  
  



  // Do the actual cleaning, hacked to stop at 2

  // If there are less than 2 jets, return underflow value

  if(nJ < 2) return -9999;

  TLorentzVector j1{}; // clean gen jet 1 & 2
  TLorentzVector j2{};

  // Loop opver prompt gen jets and check overlap with prompt gen leptons
  // If there is no overlap, keep the jet (up to two jets kept)

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
      if (dEta * dEta + dPhi * dPhi < 0.16) {
        overlap = true;
        break;
      }
    }
    if (!overlap) {
      if (n == 0) { j1.SetPtEtaPhiM(GenJet_pt[iJ], GenJet_eta[iJ], GenJet_phi[iJ], GenJet_mass[iJ]); }
      else if (n == 1){ j2.SetPtEtaPhiM(GenJet_pt[iJ], GenJet_eta[iJ], GenJet_phi[iJ], GenJet_mass[iJ]); }
      ++n;
    }
  }
  if ( (n < 2) || (nL < 2) ) return -9999;
    

  float phi1 = j1.Phi();
  float phi2 = j2.Phi();

  float eta1 = j1.Eta();
  float eta2 = j2.Eta();

    // Adjust dphijj definition according to
    // https://arxiv.org/pdf/2002.09888.pdf (eq. 47)

  float output=-9999;
  if (eta1 > eta2)       output = phi1 - phi2;
  else if (eta1 <= eta2) output = phi2 - phi1;

    // std::cout<<"Leading  gen-jet phi = "<<j1.Phi();
    // std::cout<<", Trailing gen-jet phi = "<<j2.Phi()<<std::endl;

    // To have delta_phi in (-pi, pi) interval
    // https://root.cern.ch/doc/master/TVector2_8cxx_source.html#l00103
  if (output >  TMath::Pi()) output = output - 2*TMath::Pi();
  if (output < -TMath::Pi()) output = output + 2*TMath::Pi();

  return output;

}

#endif