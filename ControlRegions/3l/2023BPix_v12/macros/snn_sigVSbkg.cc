#ifndef SNN_SIG_BKG
#define SNN_SIG_BKG
#include <vector>

#include "TVector2.h"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"

#include <iostream>
#include "ROOT/RVec.hxx"

//#include "generated_code_dnn_TTVsOther.h"
#include "/afs/cern.ch/user/s/squinto/private/work/PlotsConfigurationsRun3/HWW/ggH_DF/2023/generated_codes/generated_code_snn.h"

using namespace ROOT;
using namespace ROOT::VecOps;
RVecF snn_SigVSBkg(
		    float   nvtx,
		    float   mll,
		    float   mth,
		    float   ptll,
		    float   drll,
		    float   dphill,
			float   Lepton_pt_1,
		    float   Lepton_pt_2,
		    float   Lepton_eta_1,
		    float   Lepton_eta_2,
		    float   Lepton_phi_1,
		    float   Lepton_phi_2,
		    float   PuppiMET_pt,
			float   njet,
            float   CleanJet_pt_1,
            float   CleanJet_pt_2,
            float   CleanJet_eta_1,
            float   CleanJet_eta_2
){
RVecF snn;
float inputs[20];
inputs[0]   = nvtx;
inputs[1]   = mll;
inputs[2]   = mth;
inputs[3]   = ptll;
inputs[4]   = drll;
inputs[5]   = dphill;
inputs[6]   = Lepton_pt_1;
inputs[7]   = Lepton_pt_2;
inputs[8]   = Lepton_eta_1;
inputs[9]   = Lepton_eta_2;
inputs[10]  = Lepton_phi_1;
inputs[11]  = Lepton_phi_2;
inputs[12]  = PuppiMET_pt;
inputs[13]  = njet;
inputs[14]  = CleanJet_pt_1;
inputs[15]  = CleanJet_pt_2;
inputs[16]  = CleanJet_eta_1;
inputs[17]  = CleanJet_eta_2;

snn.push_back(guess_SigSNN(inputs, 0));
snn.push_back(guess_SigSNN(inputs, 1));
//for(int i = 0; i < 20; i++) {
//	std::cout << inputs[i] << std::endl;
//}
//std::cout << "Now printing DNN values" << std::endl;
//std::cout << "DNN is SIG = " << dnn[0] << std::endl;
//std::cout << "DNN is BKG = " << dnn[1] << std::endl;
return snn;
}

#endif