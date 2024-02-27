#include <vector>

#include "TVector2.h"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"

#include "ROOT/RVec.hxx"

#include "model_rpv_mass_regression.h"

using namespace ROOT;
using namespace ROOT::VecOps;


RVecF RPVMassRegressionInference(
        float CleanJet_eta_0,
        float CleanJet_eta_1,
        float CleanJet_phi_0,
        float CleanJet_phi_1,
        float CleanJet_pt_0,
        float CleanJet_pt_1,
        float Lepton_eta_0,
        float Lepton_eta_1,
        float Lepton_phi_0,
        float Lepton_phi_1,
        float Lepton_pt_0,
        float Lepton_pt_1,
        float PuppiMET_phi,
        float PuppiMET_pt,
        float detajj,
        float detall,
        float dphijj,
        float dphilep1jet1,
        float dphilep2jet1,
        float dphill,
        float dphilljet,
        float dphillmet,
        float dphilmet,
        float dphilmet1,
        float dphilmet2,
        float dphiltkmet,
        float drll,
        float ht,
        float mR,
        float mT2,
        float mTi,
        float mindetajl,
        float mjj,
        float mll,
        float mpmet,
        float mth,
        float mtw1,
        float mtw2,
        float pTWW,
        float projpfmet,
        float projtkmet,
        float ptll
        ){

    RVecF masses;
    masses.reserve(3);
    float input[42];

    input[0]  = CleanJet_eta_0;   
    input[1]  = CleanJet_eta_1;
    input[2]  = CleanJet_phi_0;
    input[3]  = CleanJet_phi_1;
    input[4]  = CleanJet_pt_0;
    input[5]  = CleanJet_pt_1;
    input[6]  = Lepton_eta_0;
    input[7]  = Lepton_eta_1;
    input[8]  = Lepton_phi_0;
    input[9]  = Lepton_phi_1;
    input[10] = Lepton_pt_0;
    input[11] = Lepton_pt_1;
    input[12] = PuppiMET_phi;
    input[13] = PuppiMET_pt;
    input[14] = detajj;
    input[15] = detall;
    input[16] = dphijj;
    input[17] = dphilep1jet1;
    input[18] = dphilep2jet1;
    input[19] = dphill;
    input[20] = dphilljet;
    input[21] = dphillmet;
    input[22] = dphilmet;
    input[23] = dphilmet1;
    input[24] = dphilmet2;
    input[25] = dphiltkmet;
    input[26] = drll;
    input[27] = ht;
    input[28] = mR;
    input[29] = mT2;
    input[30] = mTi;
    input[31] = mindetajl;
    input[32] = mjj;
    input[33] = mll;
    input[34] = mpmet;
    input[35] = mth;
    input[36] = mtw1;
    input[37] = mtw2;
    input[38] = pTWW;
    input[39] = projpfmet;
    input[40] = projtkmet;
    input[41] = ptll;

    masses.push_back(guess_digit(input, 0));
    masses.push_back(guess_digit(input, 1));
    masses.push_back(guess_digit(input, 2));

    return masses;

}
  

