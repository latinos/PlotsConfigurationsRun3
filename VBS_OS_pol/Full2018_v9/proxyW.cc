#ifndef PROXY_W
#define PROXY_W
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
RVecF proxyW(
		    RVecF   Lepton_pt,
		    RVecF   Lepton_eta,
		    RVecF   Lepton_phi,
		    float   PuppiMET_pt,
		    float   PuppiMET_phi
        ){
  RVecF proxyW;
  proxyW.reserve(2);
  for (unsigned inL{0}; inL != 2; ++inL) {
    TLorentzVector l{0., 0., 0., 0.,};
    TLorentzVector MET{0., 0., 0., 0.,};
    l.SetPtEtaPhiM(Lepton_pt[inL], Lepton_eta[inL], Lepton_phi[inL], 0.);
    MET.SetPtEtaPhiM(PuppiMET_pt, 0., PuppiMET_phi, 0.);
    proxyW.push_back((l + MET).M());
  }
  return proxyW;
}

#endif
