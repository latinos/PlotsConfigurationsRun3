#ifndef ADNN
#define ADNN
#include <vector>

#include "TVector2.h"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"

#include "ROOT/RVec.hxx"


#include "generated_code_UL_vbf_adnn_even.h"
#include "generated_code_UL_vbf_adnn_odd.h"
#include "generated_code_UL_ggh_adnn_even.h"
#include "generated_code_UL_ggh_adnn_odd.h"

using namespace ROOT;
using namespace ROOT::VecOps;
// using namespace std;


RVecF adversarial_dnn(
        int nLepton,
        int nCleanJet,
        int Lepton_pdgId_1,
        int Lepton_pdgId_2,
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
        float m_l2j2,
        float D_VBF_QCD,
        float D_VBF_VH,
        float D_QCD_VH,
        float D_VBF_DY,
        int year,
        int ev_number
        ){
    RVecF adnns;
    adnns.reserve(2);
    
    float input[36];

    input[0] = mjj;
//   Ctot
    input[1] = log((abs(2*Lepton_eta_1-CleanJet_eta_1-CleanJet_eta_2)+abs(2*Lepton_eta_2-CleanJet_eta_1-CleanJet_eta_2))/(detajj));

    input[2] = detajj;
    input[3] = drll;

    input[4] = CleanJet_eta_1;
    input[5] = CleanJet_eta_2;
    input[6] = CleanJet_pt_1;
    input[7] = CleanJet_pt_2;
    input[8] = CleanJet_phi_1;
    input[9] = CleanJet_phi_2;

    input[10] = Lepton_eta_1;
    input[11] = Lepton_eta_2;
    input[12] = Lepton_pt_1;
    input[13] = Lepton_pt_2;
    input[14] = Lepton_phi_1;
    input[15] = Lepton_phi_2;

    input[16] = PuppiMET_pt;
    input[17] = PuppiMET_phi;

    input[18] = mth;
    input[19] = ptll;

    input[20] = m_l1j1;
    input[21] = m_l1j2;
    input[22] = m_l2j1;
    input[23] = m_l2j2;

    input[24] = mll;

    
    input[25] = qgl_1;
    input[26] = qgl_2;

    input[27] = D_VBF_QCD;
    input[28] = D_VBF_VH;
    input[29] = D_QCD_VH;
    input[30] = D_VBF_DY;

    
    input[31] = mTi;
    input[32] = ht;

    if (year == 2016) {
      input[33] = 1; //y_2016
      input[34] = 0; //y_2017
      input[35] = 0; //y_2018
    } else if (year == 2017) {
      input[33] = 0; //y_2016
      input[34] = 1; //y_2017
      input[35] = 0; //y_2018
    } else if (year == 2018) {
      input[33] = 0; //y_2016
      input[34] = 0; //y_2017
      input[35] = 1; //y_2018
    } 
 

    if (ev_number % 2 == 0) {
       adnns.push_back(guess_digit_VBF_odd(input));
       adnns.push_back(guess_digit_GGH_odd(input));
    } else {
        adnns.push_back(guess_digit_VBF_even(input));
        adnns.push_back(guess_digit_GGH_even(input));
    }

    
    return adnns;

}
  

#endif
