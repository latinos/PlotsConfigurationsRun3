#ifndef BDT_WHSS_TOPSEMILEPTONIC_V9
#define BDT_WHSS_TOPSEMILEPTONIC_V9

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


float BDT_WHSS_TopSemileptonic_v9(
  TString BDT_name,
  TString xml_file_name,
  float pt1,
  float pt2,
  float mll,
  float mjj,
  float mtw1,
  float mtw2,
  float ptll,
  float mlljj20_whss,
  float PuppiMET_pt,
  float dphill,
  float drll,
  float dphijj,
  float dphillmet,
  float dphilmet2,
  float dphijet1met,
  float jetpt1,
  RVecF Jet_btagDeepB,
  // float Jet_btagDeepB_0,
  // float Jet_btagDeepB_1,
  RVecI CleanJet_jetIdx){

  // Assign variables values 
  float pt1_             = pt1;
  float pt2_             = pt2;
  float mll_             = mll;
  float mjj_             = mjj;
  float mtw1_            = mtw1;
  float mtw2_            = mtw2;
  float ptll_            = ptll;
  float mlljj20_whss_    = mlljj20_whss;
  float PuppiMET_pt_     = PuppiMET_pt;
  float dphill_          = dphill;
  float drll_            = drll;
  float dphijj_          = dphijj;
  float dphillmet_       = dphillmet;
  float dphilmet2_       = dphilmet2;
  float dphijet1met_     = dphijet1met;
  float jetpt1_          = jetpt1;
  float Jet_btagDeepB_0_ = CleanJet_jetIdx[0]>=0 ? Jet_btagDeepB[CleanJet_jetIdx[0]] : -2;
  float Jet_btagDeepB_1_ = CleanJet_jetIdx[1]>=0 ? Jet_btagDeepB[CleanJet_jetIdx[1]] : -2;

  // float Jet_btagDeepB_0_ = Jet_btagDeepB_0;
  // float Jet_btagDeepB_1_ = Jet_btagDeepB_1;

  // Create reader object
  TMVA::Reader *reader = new TMVA::Reader( "!Color:Silent" );

  // Pass variables to the reader
  // reader->AddVariable("pt1            ", &pt1_            );
  // reader->AddVariable("pt2            ", &pt2_            );
  reader->AddVariable("mll            ", &mll_            );
  reader->AddVariable("mjj            ", &mjj_            );
  reader->AddVariable("mtw1           ", &mtw1_           );
  reader->AddVariable("mtw2           ", &mtw2_           );
  reader->AddVariable("ptll           ", &ptll_           );
  reader->AddVariable("mlljj20_whss   ", &mlljj20_whss_   );
  reader->AddVariable("PuppiMET_pt    ", &PuppiMET_pt_    );
  reader->AddVariable("dphill         ", &dphill_         );
  // reader->AddVariable("drll           ", &drll_           );
  reader->AddVariable("dphijj         ", &dphijj_         );
  reader->AddVariable("dphillmet      ", &dphillmet_      );
  reader->AddVariable("dphilmet2      ", &dphilmet2_      );
  reader->AddVariable("dphijet1met    ", &dphijet1met_    );

  // Variables with Alt$ values
  reader->AddVariable("Alt$(CleanJet_pt[0],0)",                     &jetpt1_         );
  reader->AddVariable("Alt$(Jet_btagDeepB[CleanJet_jetIdx[0]],-2)", &Jet_btagDeepB_0_);
  reader->AddVariable("Alt$(Jet_btagDeepB[CleanJet_jetIdx[1]],-2)", &Jet_btagDeepB_1_);
  // reader->AddVariable("jetpt1         ", &jetpt1_         );
  // reader->AddVariable("Jet_btagDeepB_0", &Jet_btagDeepB_0_);
  // reader->AddVariable("Jet_btagDeepB_1", &Jet_btagDeepB_1_);


  
  //  TString dir    = "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/extended/Training/dataset_Binary_0J_DF/weights/";
  // TString prefix = "TMVAClassification";
  
  // TString methodName = TString("BDTG4D3") + TString(" method");
  // TString weightfile = dir + prefix + TString("_") + TString("BDTG4D3") + TString(".weights.xml");

  // Tell the reader which xml file to read
  reader->BookMVA(BDT_name, xml_file_name);
  
  // Evaluate the BDT value
  float classifier = reader->EvaluateMVA(BDT_name);

  // Delete reader object
  delete reader;

  // Return BDT value
  return classifier;
    
}

#endif
