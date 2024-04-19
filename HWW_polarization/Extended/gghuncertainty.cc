
#ifndef gghuncertainty
#define gghuncertainty

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


  
  //
  // typedef std::vector<float> std::vector<float>;  
  //   
  // The input kinematics should be based on the truth quantites of  
  // defined according to:     
  // https://svnweb.cern.ch/cern/wsvn/lhchiggsxs/repository/TemplateXS/HiggsTemplateCrossSections.h 
  // namely Higgs boson pT (in GeV!), jet multiplicity with 30 GeV pT threshold    
  // of jets built ignoring all stable particles originating from the Higgs boson decay 
  // and the Stage1 STXS category       
  // In the code above, these quanties are part of the HiggsClassification struct and called:  
  //   higgs.Pt(), jets30.size(), stage1_cat_pTjet30GeV  
  // Note: the stage 1 STXS index is only used to determine if the current event fulfil the
  //       VBF topology selection. I.e. only categories 
  //         GG2H_VBFTOPO_JET3VETO = 101, GG2H_VBFTOPO_JET3 = 102,
  //       are checked 
  // Dag Gillberg, March 21, 2017     


        
float g_sig0 = 30.117;
float g_sig1 = 12.928;
float g_sig_ge2 = 5.475;
float g_sig_ge1 = g_sig1+g_sig_ge2;
float g_sig_tot = g_sig0+g_sig_ge1;
float g_sig_vbfTopo = 0.630;
float g_sig_ge2noVBF = g_sig_ge2-g_sig_vbfTopo;
float g_sig_ge1noVBF = g_sig_ge1-g_sig_vbfTopo;
  
  
//---- Jet bin uncertainties  
std::vector<float> blptw(int Njets30) {
    
  static std::vector<float> sig({g_sig0,g_sig1,g_sig_ge2noVBF}); // NNLOPS subtracting VBF
  // BLPTW absolute uncertainties in pb 
  static vector<float> yieldUnc({ 1.12, 0.66, 0.42});
  static vector<float> resUnc  ({ 0.03, 0.57, 0.42});
  static vector<float> cut01Unc({-1.22, 1.00, 0.21});
  static vector<float> cut12Unc({    0,-0.86, 0.86});
  
  // account for missing EW+quark mass effects by scaling BLPTW total cross section to sigma(N3LO)    
  float sf = 48.52/47.4;
  int jetBin = (Njets30 > 1 ? 2 : Njets30);
  float normFact = sf/sig[jetBin];
  
  return { yieldUnc[jetBin]*normFact,
      resUnc[jetBin]*normFact,
      cut01Unc[jetBin]*normFact,
      cut12Unc[jetBin]*normFact };
}

float vbf_2j(int STXS) {
  if (STXS==101 || STXS == 102) return 0.200; // 20.0%                                                                                                                                                                                                                       
  return 0.0; // Events with no VBF topology have no VBF uncertainty
}

float vbf_3j(int STXS) {
  if (STXS==101) return -0.320; // GG2H_VBFTOPO_JET3VETO, tot unc 38%
  if (STXS==102) return  0.235; // GG2H_VBFTOPO_JET3, tot unc 30.4%
  return 0.0; // Events with no VBF topology have no VBF uncertainty 
}
  
float interpol(float x, float x1, float y1, float x2, float y2) {
  if (x<x1) return y1;
  if (x>x2) return y2;
  return y1+(y2-y1)*(x-x1)/(x2-x1);
}

float qm_t(float pT) {
  return interpol(pT,160,0.0,500,0.37);
}
  
// migration uncertaitny around the 120 GeV boundary  
float pT120(float pT, int Njets30) {
  if (Njets30==0) return 0;
  return interpol(pT,90,-0.016,160,0.14);
}
  
// migration uncertaitny around the 60 GeV boundary    
float pT60(float pT, int Njets30) {
  if (Njets30==0) return 0;
  if (Njets30==1) return interpol(pT,20,-0.1,100,0.1);
  return interpol(pT,0,-0.1,180,0.10); // >=2 jets 
}
  
  
std::vector<float> jetBinUnc(int Njets30, int STXS) {
  std::vector<float> result = blptw(Njets30);
  result.push_back(vbf_2j(STXS));
  result.push_back(vbf_3j(STXS));
  // set jet bin uncertainties to zero if we are in the VBF phase-space  
  if (result.back()!=0.0) result[0]=result[1]=result[2]=result[3]=0.0;
  return result;
}
  

std::vector<float> qcd_ggF_uncert_2017(int Njets30, float pT, int STXS) {
  std::vector<float> result = jetBinUnc(Njets30,STXS);
  result.push_back(pT60(pT,Njets30));
  result.push_back(pT120(pT,Njets30));
  result.push_back(qm_t(pT));
  return result;
}

// Gaussian uncertainty propagation
// event weihgt = 1.0 + 1-stdDev-fractional-uncertainty-amplitudie * NumberOfStdDev
std::vector<float> unc2sf(const std::vector<float> &unc, float Nsigma) {
  std::vector<float> sfs; for (auto u:unc) sfs.push_back(1.0+Nsigma*u); return sfs;
}


std::vector<float> qcd_ggF_uncertSF_2017(int Njets30, float pT, int STXS_Stage1, float Nsigma) {
  return unc2sf(qcd_ggF_uncert_2017(Njets30,pT,STXS_Stage1),Nsigma);
}
  
 


double GGHUncertainty(
                      string   name_,
                      char   HTXS_njets30,
                      float  HTXS_Higgs_pt,
                      int    HTXS_stage_1_pTjet30
                      ){

  
  int vindex_;

  if (name_ == "ggH_mu")
    vindex_ = 0;
  else if (name_ == "ggH_res")
    vindex_ = 1;
  else if (name_ == "ggH_mig01")
    vindex_ = 2;
  else if (name_ == "ggH_mig12")
    vindex_ = 3;
  else if (name_ == "ggH_pT60")
    vindex_ = 4;
  else if (name_ == "ggH_pT120")
    vindex_ = 5;
  else if (name_ == "ggH_VBF2j")
    vindex_ = 6;
  else if (name_ == "ggH_VBF3j")
    vindex_ = 7;
  else if (name_ == "ggH_qmtop")
    vindex_ = 8;


  std::vector<float> uncertainties;

  uncertainties = qcd_ggF_uncertSF_2017(HTXS_njets30, HTXS_Higgs_pt, HTXS_stage_1_pTjet30, 1.0);

  return uncertainties.at(vindex_);

}

#endif
