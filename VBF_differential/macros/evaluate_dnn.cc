#ifndef DNN_legacy
#define DNN_legacy
// #include <vector>

// #include "TVector2.h"
// #include "Math/Vector4Dfwd.h"
// #include "Math/GenVector/LorentzVector.h"
// #include "Math/GenVector/PtEtaPhiM4D.h"

#include "ROOT/RVec.hxx"


#include "generated_code_dnn.h"

using namespace ROOT;
using namespace ROOT::VecOps;


RVecF evaluate_dnn(
        float nLepton,
        float nCleanJet,
        float Lepton_pdgId_1,
        float Lepton_pdgId_2,
        float CleanJet_eta_1,
		float CleanJet_eta_2,
		float CleanJet_phi_1,
		float CleanJet_phi_2,
        float CleanJet_pt_1,
        float CleanJet_pt_2,
        float Lepton_eta_1,
        float Lepton_eta_2,
        float Lepton_phi_1,
        float Lepton_phi_2,
        float Lepton_pt_1,
        float Lepton_pt_2,
        float qgl_1,
        float qgl_2,
        float mjj,
        float mll,
        float ptll,
        float detajj,
        float dphill,
        float PuppiMET_pt,
        float PuppiMET_phi,
        float dphillmet,
        float drll,
        float ht,
        float mTi,
        float mth,  
        float m_l1j1,
        float m_l1j2,
        float m_l2j1,
        float m_l2j2
        ){ 
    RVecF dnn;
    dnn.reserve(2);
    
    float input[26];

    input[0] = mjj;
    input[1] = mll;
    input[2] = ptll;
    input[3] = detajj;
    input[4] = dphill;
    input[5] = PuppiMET_pt;
    input[6] = mTi;
    input[7] = dphillmet;
    input[8] = drll;
    input[9] = ht;
    input[10] = mth;
    input[11] = Lepton_pt_1;
    input[12] = Lepton_pt_2;
    input[13] = CleanJet_eta_1;
    input[14] = CleanJet_eta_2;
    input[15] = CleanJet_pt_1;
    input[16] = CleanJet_pt_2;
    input[17] = CleanJet_eta_1;
    input[18] = CleanJet_eta_2;
    input[19] = m_l1j1;
    input[20] = m_l1j2;
    input[21] = m_l2j1;
    input[22] = m_l2j2;
//   Ctot
    input[23] = log((abs(2*Lepton_eta_1-CleanJet_eta_1-CleanJet_eta_2)+abs(2*Lepton_eta_2-CleanJet_eta_1-CleanJet_eta_2))/(detajj));
    input[24] = qgl_1;
    input[25] = qgl_2;
    


    dnn.push_back(guess_digit_dnn(input, 0));
    dnn.push_back(guess_digit_dnn(input, 3));
    
    return dnn;

}
  

#endif