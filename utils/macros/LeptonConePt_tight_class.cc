#ifndef LEPTON_CONEPT_TIGHT
#define LEPTON_CONEPT_TIGHT

#include <vector>
#include "ROOT/RVec.hxx"

using namespace ROOT;
using namespace ROOT::VecOps;

RVec<float> LeptonConePt_tight(RVecF Lepton_pt,
							   RVecI Lepton_pdgId,
							   RVecI Lepton_electronIdx,
							   RVecI Lepton_muonIdx,
							   RVecF Electron_jetRelIso,
							   RVecF Muon_jetRelIso,
							   RVecI Lepton_isTightElectron,
							   RVecI Lepton_isTightMuon
							   ) {

  // conept vector
  RVec<float> conept;
  
  for (size_t i = 0; i < Lepton_pt.size(); ++i) {

	float iso = 0.0;

	int pdgId = abs(Lepton_pdgId[i]);
	
	// conept element
	float cone_pt = Lepton_pt[i];

	// Case electron
	if (pdgId == 11 && Lepton_isTightElectron[i]) {
	  int idx = Lepton_electronIdx[i];
	  iso     = Electron_jetRelIso[idx];
	  cone_pt = 0.9 * Lepton_pt[i] * (1 + iso); 
	}
	// Case muon
	else if (pdgId == 13 && Lepton_isTightMuon[i]) {
	  int idx = Lepton_muonIdx[i];
	  iso = Muon_jetRelIso[idx];
	  cone_pt = 0.9 * Lepton_pt[i] * (1 + iso); 
	}

	conept.push_back(cone_pt);
  }
  return conept;
}

#endif
