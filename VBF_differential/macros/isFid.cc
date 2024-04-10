#ifndef isFid
#define isFid

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
using namespace std;

int isFiducial(
                    int    nGenDressedLepton, 
		    RVecI  GenDressedLepton_pdgId,
		    RVecF  GenDressedLepton_pt,
		    RVecF  GenDressedLepton_eta,
		    RVecF  GenDressedLepton_phi,
		    RVecF  GenDressedLepton_mass,
		    RVecB  GenDressedLepton_hasTauAnc,
		    int    nGenJet,
		    RVecF  GenJet_pt,
		    RVecF  GenJet_eta,
		    RVecF  GenJet_phi,
		    RVecF  GenJet_mass,
        float GenMET_pt,
        float GenMET_phi
            ){


    unsigned nJ = nGenJet;
    unsigned nL = nGenDressedLepton;


    // Create vector of prompt gen leptons

    std::vector<unsigned> genleps{};
    genleps.reserve(nL);

    for (unsigned iL{0}; iL != nL; ++iL) {

        unsigned absId{static_cast<unsigned>(std::abs(GenDressedLepton_pdgId[iL]))};
        if (absId != 11 && absId != 13  )
            continue;

        if (GenDressedLepton_hasTauAnc[iL]) continue;
            
        genleps.push_back(iL);
    }

    // If there are no prompt leptons don't bother checking and just count the jets w/ pt > 30
    // Why not returning default value?

  if (genleps.size() == 0) {
    unsigned n{0};
    for (unsigned iJ{0}; iJ != nJ; ++iJ) {
      if (GenJet_pt[iJ] > 30.)
        ++n;
    }
    return -9999;
  }


  // Create prompt gen leptons 4-vectors

  std::vector<ROOT::Math::PtEtaPhiMVector> dressedLeptons{};
  for (unsigned iL : genleps) {
    dressedLeptons.push_back(
                             ROOT::Math::PtEtaPhiMVector(
                                                         GenDressedLepton_pt[iL],
                                                         GenDressedLepton_eta[iL],
                                                         GenDressedLepton_phi[iL],
                                                         GenDressedLepton_mass[iL]
                                                         )
                             );
  }


  // Do the actual cleaning, hacked to stop at 2

  // If there are less than 2 jets, return underflow value

  if(nJ < 2){
    return -9999;
  }

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
  if ( (n < 2) || (dressedLeptons.size() < 2) ) return -9999;
  else if ( dressedLeptons.size()>=2 && GenDressedLepton_pdgId[0] * GenDressedLepton_pdgId[1] != -11*13 ) return -9999;
  
  double pt3{-1};
  if (dressedLeptons.size() > 2) pt3 = dressedLeptons[2].pt();
  

  // Define additional useful variables (for fiducial region definition)

  TLorentzVector MET{};
  MET.SetPtEtaPhiM(GenMET_pt, 0., GenMET_phi, 0.);
  TLorentzVector l1{};
  l1.SetPtEtaPhiM(dressedLeptons[0].pt(), dressedLeptons[0].eta(), dressedLeptons[0].phi(), dressedLeptons[0].M());
  TLorentzVector l2{};
  l2.SetPtEtaPhiM(dressedLeptons[1].pt(), dressedLeptons[1].eta(), dressedLeptons[1].phi(), dressedLeptons[1].M());

  double mth_in = (MET + l1 + l2).Mt();
  double mth = TMath::Sqrt((l1+l2).Pt()*MET.Pt()*2*(1-TMath::Cos((l1+l2).DeltaPhi(MET))));

  bool isFid_ev = true;

  isFid_ev = isFid_ev && (l1.Pt() > 25.) && (l2.Pt() > 13.) && (pt3 < 10);
  isFid_ev = isFid_ev && (l1+l2).M() > 12; 
  isFid_ev = isFid_ev && (l1 + l2).Pt() > 30;  
  isFid_ev = isFid_ev && (j1.Pt() > 30.) && (j2.Pt() > 30.); 
  isFid_ev = isFid_ev && ((j1 + j2).M() > 120.); 
  isFid_ev = isFid_ev && (TMath::Abs(j1.Eta()) < 4.7) && (TMath::Abs(j2.Eta()) < 4.7); 
  isFid_ev = isFid_ev && (TMath::Abs(l1.Eta()) < 2.5) && (TMath::Abs(l2.Eta()) < 2.5); 
  isFid_ev = isFid_ev && mth>=60;
  

  if (isFid_ev){
    return 1;
  } else {
    return 0;

  }

  return -9999;

}

#endif