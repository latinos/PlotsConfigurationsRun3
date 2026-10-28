#ifndef LEPTON_CONEPT
#define LEPTON_CONEPT

#include <vector>
#include "ROOT/RVec.hxx"

using namespace ROOT;
using namespace ROOT::VecOps;

RVec<float> LeptonConePt(RVecF Lepton_pt,
                         RVecI Lepton_pdgId,
                         RVecI Lepton_electronIdx,
                         RVecI Lepton_muonIdx,
                         RVecF Electron_jetRelIso,
                         RVecF Muon_jetRelIso) {

  RVec<float> conept;
  
  for (size_t i = 0; i < Lepton_pt.size(); ++i) {
	float iso = 0.0;
	int pdgId = abs(Lepton_pdgId[i]);
	
	if (pdgId == 11) {
	  int idx = Lepton_electronIdx[i];
	  iso = Electron_jetRelIso[idx];
	} else if (pdgId == 13) {
	  int idx = Lepton_muonIdx[i];
	  iso = Muon_jetRelIso[idx];
	}
	conept.push_back(0.9 * Lepton_pt[i] * (1 + iso));
  }
  return conept;
}

#endif
