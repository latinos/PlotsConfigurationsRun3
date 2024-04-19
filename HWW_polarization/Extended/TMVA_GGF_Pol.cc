
#ifndef TMVA_GGF_Pol
#define TMVA_GGF_Pol

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

float TMVA_HWW_Pol(
		  int    nLepton,
		  RVecI  Lepton_pdgId,
		  RVecF  Lepton_pt,
		  RVecF  Lepton_eta,
		  RVecF  Lepton_phi,
		  float  mll,
		  float  ptll,
		  float  dphill,
		  float  mcollWW,
		  float  pTWW,
		  float  mtw1,
		  float  mtw2,
		  float  drll,
		  float  mth,
		  float  dphilmet,
		  float  mpmet,
		  float  detall
		  ){
  
  std::map<std::string,int> Use;
  Use["BDTG4D3"]       = 1;
  


  float dphilmet_user = dphilmet;
  float mpmet_user = mpmet;
  float mll_user = mll;
  float mth_user = mth;
  float mtw1_user = mtw1;
  float mtw2_user = mtw2;
  float mcollWW_user = mcollWW;
  float pTWW_user = pTWW;
  float pt1_user = Lepton_pt[0];
  float pt2_user = Lepton_pt[1];
  float eta1_user = Lepton_eta[0];
  float eta2_user = Lepton_eta[1];
  float phi1_user = Lepton_phi[0];
  float phi2_user = Lepton_phi[1];

  float ptll_user = ptll;
  float drll_user = drll;
  float detall_user = detall;
  float dphill_user = dphill;


  TMVA::Reader *reader_Pol = new TMVA::Reader( "!Color:Silent" );

  reader_Pol->AddVariable("mll", &mll_user);
  reader_Pol->AddVariable("mth", &mth_user);
  reader_Pol->AddVariable("mtw1", &mtw1_user);
  reader_Pol->AddVariable("mtw2", &mtw2_user);

  reader_Pol->AddVariable("mcollWW", &mcollWW_user);

  reader_Pol->AddVariable("ptll", &ptll_user);

  reader_Pol->AddVariable("pTWW", &pTWW_user);
  reader_Pol->AddVariable("lep_pt1", &pt1_user);
  reader_Pol->AddVariable("lep_pt2", &pt2_user);
  reader_Pol->AddVariable("lep_eta1", &eta1_user);
  reader_Pol->AddVariable("lep_eta2", &eta2_user);
  reader_Pol->AddVariable("lep_phi1", &phi1_user);
  reader_Pol->AddVariable("lep_phi2", &phi2_user);
  reader_Pol->AddVariable("dphilmet", &dphilmet_user);
  reader_Pol->AddVariable("dphill", &dphill_user);
  reader_Pol->AddVariable("detall", &detall_user);
  reader_Pol->AddVariable("drll", &drll_user);
  reader_Pol->AddVariable("mpmet", &mpmet_user);

  
  //TString dir    = "/afs/cern.ch/work/s/sblancof/public/CMSSW_10_6_10/src/PlotsConfigurations/Configurations/WW/Full2016_v7/DNN/dataset/weights/";
  TString dir    = "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/mkShapesRDF/examples/Full2017_v9/dataset_HWW_star/weights/";
  TString prefix = "TMVAClassification";
  
  TString methodName = TString("BDTG4D3") + TString(" method");
  TString weightfile = dir + prefix + TString("_") + TString("BDTG4D3") + TString(".weights.xml");
  reader_Pol->BookMVA( methodName, weightfile );
  
  float result_Pol = reader_Pol->EvaluateMVA(methodName);
  delete reader_Pol;
  return result_Pol;
    
}

#endif
