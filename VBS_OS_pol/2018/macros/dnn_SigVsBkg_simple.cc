#ifndef DNN_SIG_BKG
#define DNN_SIG_BKG
#include <vector>

#include "TVector2.h"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"

#include <iostream>
#include "ROOT/RVec.hxx"

using namespace ROOT;
using namespace ROOT::VecOps;
RVecF dnn_SigVsBkg_simple(
		    float   CleanJet_eta_1,
		    float   CleanJet_eta_2
        ){
  RVecF dnn;
  return dnn;
}

#endif
