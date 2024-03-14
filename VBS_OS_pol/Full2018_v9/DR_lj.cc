#ifndef DR_lj
#define DR_lj
#include <vector>

#include "TVector2.h"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"

#include <iostream>
#include "ROOT/RVec.hxx"

using namespace ROOT;
using namespace ROOT::VecOps;
RVecF dr_lj(
		    RVecF   CleanJet_eta,
		    RVecF   CleanJet_phi,
		    RVecF   Lepton_eta,
		    RVecF   Lepton_phi
        ){
  RVecF dr_lj;
  dr_lj.reserve(4);
  for (unsigned inL{0}; inL != 2; ++inL) {
    for (unsigned inJ{0}; inJ != 2; ++inJ) {
      dr_lj.push_back(sqrt(pow((Lepton_eta[inL] - CleanJet_eta[inJ]),2) + pow((Lepton_phi[inL] - CleanJet_phi[inJ]),2)));
    }
  }
  return dr_lj;
}

#endif