#ifndef mlj
#define mlj

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
  
  RVecF m_lj_res; // Renamed to avoid shadowing the function name
  m_lj_res.reserve(4);

  // Guardrail 1: Dynamic loop bounds based on what's actually in the event
  unsigned int max_leptons = std::min<unsigned int>(2, Lepton_pt.size());
  unsigned int max_jets    = std::min<unsigned int>(2, CleanJet_pt.size());

  for (unsigned inL{0}; inL < max_leptons; ++inL) {
    TLorentzVector l{0., 0., 0., 0.};
    l.SetPtEtaPhiM(Lepton_pt[inL], Lepton_eta[inL], Lepton_phi[inL], 0.);

    for (unsigned inJ{0}; inJ < max_jets; ++inJ) {
      
      // Guardrail 2: Safely extract the mass index
      int mass_idx = CleanJet_jetIdx[inJ];
      float mass = 0.0;

      // Guardrail 3: Check that index is valid and within Jet_mass bounds
      if (mass_idx >= 0 && static_cast<size_t>(mass_idx) < Jet_mass.size()) {
        mass = Jet_mass[mass_idx];
      } else {
        // Fallback or warning if your variation dropped/mismatched the index
        mass = 0.0; 
      }

      TLorentzVector j{0., 0., 0., 0.};
      j.SetPtEtaPhiM(CleanJet_pt[inJ], CleanJet_eta[inJ], CleanJet_phi[inJ], mass);
      
      m_lj_res.push_back((l+j).M());
    }
  }

  // Optional: If you strictly need an RVecF of size 4 downstream even if physics objects are missing, 
  // pad the remaining slots with a placeholder like -999.0
  while (m_lj_res.size() < 4) {
    m_lj_res.push_back(-999.0);
  }

  return m_lj_res;
}

#endif