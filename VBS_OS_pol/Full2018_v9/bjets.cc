
#include <vector>

#include "TVector2.h"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"

#include <iostream>
#include "ROOT/RVec.hxx"

using namespace ROOT;
using namespace ROOT::VecOps;
RVecF bJet_pt(
		    int     nCleanJet,
		    RVecF   CleanJet_pt,
		    RVecF   CleanJet_eta,
        RVecI   CleanJet_jetIdx,
		    RVecF   Jet_btagDeepB,
        float   bJetWP
        ){
  unsigned nJ = nCleanJet;
  RVecF bJet_pt;
  bJet_pt.reserve(nCleanJet);
  for (unsigned inJ{0}; inJ != nJ; ++inJ) {
    if (abs(CleanJet_eta[inJ]) < 2.5 && CleanJet_pt[inJ] > 20. && Take(Jet_btagDeepB, CleanJet_jetIdx)[inJ] > bJetWP) {
      bJet_pt.push_back(CleanJet_pt[inJ]);
    }
    else bJet_pt.push_back(0.);
  }
  bJet_pt = Sort(bJet_pt);
  bJet_pt = Reverse(bJet_pt);
  return bJet_pt;
}
