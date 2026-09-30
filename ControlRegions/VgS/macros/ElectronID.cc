#include "ROOT/RVec.hxx"
#include <cmath>

using namespace ROOT;
using namespace ROOT::VecOps;

class ELID {
public:
  ELID() {}

  RVecB operator()(
      const RVecI& Lepton_pdgId,
      const RVecI& Lepton_electronIdx,
      const RVecF& Electron_eta,
      const RVecF& Electron_dxy,
      const RVecF& Electron_dz,
      const RVecI& Electron_cutBased,
      const RVecB& Electron_convVeto
  ) {
    RVecB out(Lepton_pdgId.size(), false);

    for (size_t i = 0; i < Lepton_pdgId.size(); ++i) {

      if (std::abs(Lepton_pdgId[i]) != 11) continue;

      int eidx = Lepton_electronIdx[i];

      float eta = std::abs(Electron_eta[eidx]);
      float dxy = std::abs(Electron_dxy[eidx]);
      float dz  = std::abs(Electron_dz[eidx]);

      bool ipCut = false;

      if (eta <= 1.479) {
        ipCut = dxy < 0.05 && dz < 0.10;
      } else {
        ipCut = dxy < 0.10 && dz < 0.20;
      }

      out[i] =
        eta < 2.5 &&
        ipCut &&
        Electron_cutBased[eidx] >= 4 &&
        Electron_convVeto[eidx]; 
    }
    
    return out;
  }
};


