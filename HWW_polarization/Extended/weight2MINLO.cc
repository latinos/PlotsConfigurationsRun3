
#ifndef weight2MINLO
#define weight2MINLO

#include <vector>

#include "TVector2.h"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"

#include "TFile.h"
#include "TString.h"
#include "TGraph.h"

#include <string>
#include <unordered_map>

#include <iostream>
#include "ROOT/RVec.hxx"

using namespace ROOT;
using namespace ROOT::VecOps;


double Weight2MINLO(
		    const char *sourcePath, 
		    char   HTXS_njets30,
		    float  HTXS_Higgs_pt
		    ){


  std::array<std::unique_ptr<TGraph>, 4> weightSources_;

  TFile source = TFile(sourcePath);

  for (unsigned iJ{0}; iJ != 4; ++iJ)
    weightSources_[iJ].reset(static_cast<TGraph*>(source.Get(TString::Format("gr_NNLOPSratio_pt_powheg_%djet", iJ))));

  double pt = HTXS_Higgs_pt;

  unsigned char njets = HTXS_njets30;

  switch (njets) {
  case 0:
    return weightSources_[0]->Eval(std::min(pt, 125.));
  case 1:
    return weightSources_[1]->Eval(std::min(pt, 625.));
  case 2:
    return weightSources_[2]->Eval(std::min(pt, 800.));
  case 3:
    return weightSources_[3]->Eval(std::min(pt, 925.));
  default:
    return 1.;
  }

}

#endif
