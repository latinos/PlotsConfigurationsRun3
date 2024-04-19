
#ifndef TMVA_GGF_1J
#define TMVA_GGF_1J

#include <vector>
#include "TVector2.h"
#include "TLorentzVector.h"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"
#include <iostream>
#include <TMath.h>
#include <math.h>

#include "Math/Point3D.h"
#include "Math/Vector3D.h"
#include "Math/Vector4D.h"
#include "Math/Rotation3D.h"
#include "Math/EulerAngles.h"
#include "Math/AxisAngle.h"
#include "Math/Quaternion.h"
#include "Math/RotationX.h"
#include "Math/RotationY.h"
#include "Math/RotationZ.h"
#include "Math/RotationZYX.h"
#include "Math/LorentzRotation.h"
#include "Math/Boost.h"
#include "Math/BoostX.h"
#include "Math/BoostY.h"
#include "Math/BoostZ.h"
#include "Math/Transform3D.h"
#include "Math/Plane3D.h"
#include "Math/VectorUtil.h"
#include "TMatrixD.h"
#include "TVectorD.h"
#include "TMath.h"

#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TSystem.h"
#include "TROOT.h"
#include "TStopwatch.h"

#include "TMVA/Tools.h"
#include "TMVA/Reader.h"
#include "TMVA/MethodCuts.h"

#include "ROOT/RVec.hxx"

using namespace ROOT;
using namespace ROOT::VecOps;


float TMVA_HWW_1J(
		  int    nLepton,
		  int    nCleanJet,
		  RVecI  Lepton_pdgId,
		  RVecF  Lepton_pt,
		  RVecF  Lepton_eta,
		  RVecF  Lepton_phi,
		  RVecF  CleanJet_pt,
		  RVecF  CleanJet_eta,
		  RVecF  CleanJet_phi,
		  float  mjj,
		  float  mll,
		  float  ptll,
		  float  detajj,
		  float  dphill,
		  float  dphijjmet,
		  float  mtw1,
		  float  mtw2,
		  float  drll,
		  float  mth,
		  float  PuppiMET_pt,
		  float  PuppiMET_phi,
		  RVecI  CleanJet_jetIdx,
		  RVecF  Jet_btagDeepFlavB,
		  float  dphilmet1,
		  float  dphilmet2,
		  float dphilep1jet1,
		  float dphilep2jet1,
		  float  mpmet,
		  float  detall
		  ){
  
  std::map<std::string,int> Use;
  Use["BDTG4D3"]       = 1;
  
  unsigned njet = nCleanJet;
    
  float Jet_btagDeepFlavB_CleanJet_jetIdx_0_;
  float Jet_btagDeepFlavB_CleanJet_jetIdx_1_;
  if (njet==0){
    
  }else if (njet == 1){
    int jetIdx0 = CleanJet_jetIdx[0];
    Jet_btagDeepFlavB_CleanJet_jetIdx_0_ = jetIdx0 >= 0 ? Jet_btagDeepFlavB[jetIdx0] : 0.0;
  }
  else {
    int jetIdx0 = CleanJet_jetIdx[0];
    int jetIdx1 = CleanJet_jetIdx[1];
    Jet_btagDeepFlavB_CleanJet_jetIdx_0_ = jetIdx0 >= 0 ? Jet_btagDeepFlavB[jetIdx0] : 0.0;
    Jet_btagDeepFlavB_CleanJet_jetIdx_1_ = jetIdx1 >= 0 ? Jet_btagDeepFlavB[jetIdx1] : 0.0;
  }

  float dphilmet1_user = dphilmet1;
  float dphilmet2_user = dphilmet2;
  float mpmet_user = mpmet;
  float mll_user = mll;
  float mth_user = mth;
  float mtw1_user = mtw1;
  float mtw2_user = mtw2;
  float ptll_user = ptll;
  float drll_user = drll;
  float detall_user = detall;
  float dphill_user = dphill;
  float PuppiMET_pt_user = PuppiMET_pt;
  float PuppiMET_phi_user = PuppiMET_phi;
  float dphilep1jet1_user = dphilep1jet1;
  float dphilep2jet1_user = dphilep2jet1;
  float btag_user = (float)Jet_btagDeepFlavB_CleanJet_jetIdx_0_;
  float btag_user_1 = (float)Jet_btagDeepFlavB_CleanJet_jetIdx_1_;
    
  TMVA::Reader *reader_1j = new TMVA::Reader( "!Color:Silent" );
  
  reader_1j->AddVariable("mll", &mll_user);
  reader_1j->AddVariable("mth", &mth_user);
  reader_1j->AddVariable("mtw1", &mtw1_user);
  reader_1j->AddVariable("mtw2", &mtw2_user);
  reader_1j->AddVariable("ptll", &ptll_user);
  reader_1j->AddVariable("drll", &drll_user);
  reader_1j->AddVariable("dphilmet1", &dphilmet1_user);
  reader_1j->AddVariable("dphilmet2", &dphilmet2_user);
  reader_1j->AddVariable("dphill", &dphill_user);
  reader_1j->AddVariable("PuppiMET_pt", &PuppiMET_pt_user);
  reader_1j->AddVariable("PuppiMET_phi", &PuppiMET_phi_user);
  reader_1j->AddVariable("detall", &detall_user);
  reader_1j->AddVariable("mpmet", &mpmet_user);
  reader_1j->AddVariable("dphilep1jet1", &dphilep1jet1_user);
  reader_1j->AddVariable("dphilep2jet1", &dphilep2jet1_user);
  reader_1j->AddVariable("btagDeepFlavB", &btag_user);  

  TString dir    = "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/extended/Training/dataset_Binary_1J_DF/weights/";
  TString prefix = "TMVAClassification";
  
  TString methodName = TString("BDTG4D3") + TString(" method");
  TString weightfile = dir + prefix + TString("_") + TString("BDTG4D3") + TString(".weights.xml");
  reader_1j->BookMVA( methodName, weightfile );
  
  float result_1J = reader_1j->EvaluateMVA(methodName);
  delete reader_1j;
  return result_1J;    
}

#endif
