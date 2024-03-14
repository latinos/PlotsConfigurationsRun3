#ifndef M_lj
#define M_lj
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
RVecF m_lj(
		    RVecF   CleanJet_pt,
		    RVecF   CleanJet_eta,
		    RVecF   CleanJet_phi,
		    RVecI   CleanJet_jetIdx,
		    RVecF   Jet_mass,
		    RVecF   Lepton_pt,
		    RVecF   Lepton_eta,
		    RVecF   Lepton_phi
        ){
  RVecF m_lj;
  m_lj.reserve(4);
  for (unsigned inL{0}; inL != 2; ++inL) {
    TLorentzVector l{0., 0., 0., 0.,};
    l.SetPtEtaPhiM(Lepton_pt[inL], Lepton_eta[inL], Lepton_phi[inL], 0.);
    for (unsigned inJ{0}; inJ != 2; ++inJ) {
      TLorentzVector j{0., 0., 0., 0.,};
      j.SetPtEtaPhiM(CleanJet_pt[inJ], CleanJet_eta[inJ], CleanJet_phi[inJ], Take(Jet_mass, CleanJet_jetIdx)[inJ]);
      m_lj.push_back((l+j).M());
    }
  }
  return m_lj;
}

#endif
