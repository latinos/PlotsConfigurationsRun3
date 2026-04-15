#ifndef DNN_SIG_BKG
#define DNN_SIG_BKG
#include <vector>

#include "TVector2.h"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"

#include <iostream>
#include "ROOT/RVec.hxx"

//#include "generated_code_dnn_SigVsBkg.h"
#include "generated_code_dnn_emu_SigVsBkg.h"

using namespace ROOT;
using namespace ROOT::VecOps;
RVecF dnn_SigVsBkg(
		    float   CleanJet_eta_1,
		    float   CleanJet_eta_2,
		    float   CleanJet_phi_1,
		    float   CleanJet_phi_2,
		    float   CleanJet_pt_1,
		    float   CleanJet_pt_2,
		    float   Lepton_eta_1,
		    float   Lepton_eta_2,
		    float   Lepton_phi_1,
		    float   Lepton_phi_2,
		    float   Lepton_pt_1,
		    float   Lepton_pt_2,
        float   Rpt,
        float   Zepp_l1,
        float   Zepp_l2,
        float   Zepp_ll,
        float   detajj,
        float   detall,
        float   dphijj,
        float   dphilep1jet1, 
        float   dphilep1jet2, 
        float   dphilep1jj,   
        float   dphilep2jet1,
        float   dphilep2jet2, 
        float   dphilep2jj,   
        float   dphill,     
        float   dphilljet,   
        float   dphilljetjet,
        float   dphillmet,   
        float   dphilmet1,   
        float   dphilmet2,   
        float   dr_l1j1,     
        float   dr_l1j2,     
        float   dr_l2j1,     
        float   dr_l2j2,     
        float   drll,       
        float   ht,
        float   m2ljj30,
        float   mT2,
        float   mTi,
        float   m_l1j1,
        float   m_l1j2,
        float   m_l2j1,
        float   m_l2j2,
        float   mcoll,
        float   mcollWW,
        float   mjj,
        float   mll,
        float   mtw1,
        float   mtw2,
        float   PuppiMET_phi,
        float   proxyW_l1,
        float   proxyW_l2,
        float   PuppiMET_pt,
        float   ptll,
        float   recoil,
        float   yll
        ){
  RVecF dnn;
  float inputs[57];
  inputs[0]   = CleanJet_eta_1;
  inputs[1]   = CleanJet_eta_2;
  inputs[2]   = CleanJet_phi_1;
  inputs[3]   = CleanJet_phi_2;
  inputs[4]   = CleanJet_pt_1;
  inputs[5]   = CleanJet_pt_2;
  inputs[6]   = Lepton_eta_1;
  inputs[7]   = Lepton_eta_2;
  inputs[8]   = Lepton_phi_1;
  inputs[9]   = Lepton_phi_2;
  inputs[10]  = Lepton_pt_1;
  inputs[11]  = Lepton_pt_2;
  inputs[12]  = Rpt;
  inputs[13]  = Zepp_l1;
  inputs[14]  = Zepp_l2;
  inputs[15]  = Zepp_ll;
  inputs[16]  = detajj;
  inputs[17]  = detall;
  inputs[18]  = dphijj;
  inputs[19]  = dphilep1jet1;
  inputs[20]  = dphilep1jet2;
  inputs[21]  = dphilep1jj;
  inputs[22]  = dphilep2jet1;
  inputs[23]  = dphilep2jet2;
  inputs[24]  = dphilep2jj;
  inputs[25]  = dphill;
  inputs[26]  = dphilljet;
  inputs[27]  = dphilljetjet;
  inputs[28]  = dphillmet;
  inputs[29]  = dphilmet1;  
  inputs[30]  = dphilmet2;
  inputs[31]  = dr_l1j1;
  inputs[32]  = dr_l1j2;
  inputs[33]  = dr_l2j1;
  inputs[34]  = dr_l2j2;
  inputs[35]  = drll;
  inputs[36]  = ht;
  inputs[37]  = m2ljj30;
  inputs[38]  = mT2;
  inputs[39]  = mTi;
  inputs[40]  = m_l1j1;
  inputs[41]  = m_l1j2;
  inputs[42]  = m_l2j1;
  inputs[43]  = m_l2j2;
  inputs[44]  = mcoll;
  inputs[45]  = mcollWW;
  inputs[46]  = mjj;
  inputs[47]  = mll;
  inputs[48]  = mtw1;
  inputs[49]  = mtw2;  
  inputs[50]  = PuppiMET_phi;
  inputs[51]  = proxyW_l1;
  inputs[52]  = proxyW_l2;
  inputs[53]  = PuppiMET_pt;
  inputs[54]  = ptll;
  inputs[55]  = recoil;
  inputs[56]  = yll;
  dnn.push_back(guess_VBS(inputs, 0));
  dnn.push_back(guess_VBS(inputs, 1));

  //for(int i = 0; i < 57; i++) {
  //  std::cout << inputs[i] << std::endl;
  //}
  //std::cout << "Now printing DNN values" << std::endl;
  //std::cout << "DNN is VBS = " << dnn[0] << std::endl;
  //std::cout << "DNN is BKG = " << dnn[1] << std::endl;
  return dnn;
}

#endif
