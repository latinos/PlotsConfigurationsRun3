#ifndef BDT_WH3L_SSSF_v9
#define BDT_WH3L_SSSF_v9

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


class BDT_WH3l_SSSF_v9{

public:

  BDT_WH3l_SSSF_v9( TString BDT_name, TString xml_file_name );
  ~BDT_WH3l_SSSF_v9();

  TString BDT_name_;
  TString xml_file_name_;

  float WH3l_dphilllmet_;
  float WH3l_mOSll_min_;
  float WH3l_ptOSll_min_;
  float WH3l_drOSll_min_;
  float WH3l_dphilmet_0_;
  float WH3l_dphilmet_1_;
  float WH3l_dphilmet_2_;
  float WH3l_ptWWW_;
  float PuppiMET_pt_;    
  float Lepton_pt_0_;    
  float Lepton_pt_1_;   
  float Lepton_pt_2_;

  TMVA::Reader *reader = new TMVA::Reader();
  
  double operator() ( float WH3l_dphilllmet,
					  RVecF WH3l_mOSll,
					  RVecF WH3l_ptOSll,
					  RVecF WH3l_drOSll,
					  RVecF WH3l_dphilmet,
					  float WH3l_ptWWW,
					  float PuppiMET_pt,
					  RVecF Lepton_pt){
	
	// Assign variables values
	WH3l_dphilllmet_ = WH3l_dphilllmet;
	WH3l_mOSll_min_  = std::min({WH3l_mOSll[0],  WH3l_mOSll[1],  WH3l_mOSll[2]});
	WH3l_ptOSll_min_ = std::min({WH3l_ptOSll[0], WH3l_ptOSll[1], WH3l_ptOSll[2]});
	WH3l_drOSll_min_ = std::min({WH3l_drOSll[0], WH3l_drOSll[1], WH3l_drOSll[2]});
	WH3l_dphilmet_0_ = WH3l_dphilmet[0];
	WH3l_dphilmet_1_ = WH3l_dphilmet[1];
	WH3l_dphilmet_2_ = WH3l_dphilmet[2];
	WH3l_ptWWW_      = WH3l_ptWWW;
	PuppiMET_pt_     = PuppiMET_pt;
	Lepton_pt_0_     = Lepton_pt[0];
	Lepton_pt_1_     = Lepton_pt[1];
	Lepton_pt_2_     = Lepton_pt[2];

	// Evaluate the classifier
	double classifier = reader->EvaluateMVA(BDT_name_);
	
	return classifier;
  }
  
};
	
BDT_WH3l_SSSF_v9::BDT_WH3l_SSSF_v9( TString BDT_name, TString xml_file_name ){

  std::cout << "BDT name:      " << BDT_name      << std::endl;
  std::cout << "xml file name: " << xml_file_name << std::endl;

  BDT_name_      = BDT_name;
  xml_file_name_ = xml_file_name;

  // Pass variables to the reader
  reader->AddVariable("WH3l_dphilllmet",                                  &WH3l_dphilllmet_);
  reader->AddVariable("MinIf$(WH3l_mOSll[],  WH3l_mOSll[Iteration$]>0)",  &WH3l_mOSll_min_);
  reader->AddVariable("MinIf$(WH3l_ptOSll[], WH3l_ptOSll[Iteration$]>0)", &WH3l_ptOSll_min_);
  reader->AddVariable("MinIf$(WH3l_drOSll[], WH3l_drOSll[Iteration$]>0)", &WH3l_drOSll_min_);
  reader->AddVariable("WH3l_dphilmet[0]",                                 &WH3l_dphilmet_0_);
  reader->AddVariable("WH3l_dphilmet[1]",                                 &WH3l_dphilmet_1_);
  reader->AddVariable("WH3l_dphilmet[2]",                                 &WH3l_dphilmet_2_);
  reader->AddVariable("WH3l_ptWWW",                                       &WH3l_ptWWW_);
  reader->AddVariable("PuppiMET_pt",                                      &PuppiMET_pt_);
  reader->AddVariable("Alt$(Lepton_pt[0],0)",                             &Lepton_pt_0_);
  reader->AddVariable("Alt$(Lepton_pt[1],0)",                             &Lepton_pt_1_);
  reader->AddVariable("Alt$(Lepton_pt[2],0)",                             &Lepton_pt_2_);

  reader->BookMVA(BDT_name, xml_file_name);
}

BDT_WH3l_SSSF_v9::~BDT_WH3l_SSSF_v9(){
  
  std::cout << "Deleting reader" << std::endl;
  
  reader->Delete();
}

#endif
	

  // float BDT_WH3l_SSSF_v9(TString BDT_name, TString xml_file_name, float WH3l_dphilllmet, RVecF WH3l_mOSll, RVecF WH3l_ptOSll, RVecF WH3l_drOSll, RVecF WH3l_dphilmet, float WH3l_ptWWW, float PuppiMET_pt, RVecF Lepton_pt){

//   // Assign variables values
//   float WH3l_dphilllmet_ = WH3l_dphilllmet;
//   float WH3l_mOSll_min_  = std::min({WH3l_mOSll[0],  WH3l_mOSll[1],  WH3l_mOSll[2]});
//   float WH3l_ptOSll_min_ = std::min({WH3l_ptOSll[0], WH3l_ptOSll[1], WH3l_ptOSll[2]});
//   float WH3l_drOSll_min_ = std::min({WH3l_drOSll[0], WH3l_drOSll[1], WH3l_drOSll[2]});
//   // float WH3l_ZVeto_      = WH3l_ZVeto;
//   // float WH3l_mtlmet_1_   = WH3l_mtlmet[1];
//   // float WH3l_mtlmet_2_   = WH3l_mtlmet[2];
//   float WH3l_dphilmet_0_ = WH3l_dphilmet[0];
//   float WH3l_dphilmet_1_ = WH3l_dphilmet[1];
//   float WH3l_dphilmet_2_ = WH3l_dphilmet[2];
//   float WH3l_ptWWW_      = WH3l_ptWWW;
//   float PuppiMET_pt_     = PuppiMET_pt;
//   float Lepton_pt_0_     = Lepton_pt[0];
//   float Lepton_pt_1_     = Lepton_pt[1];
//   float Lepton_pt_2_     = Lepton_pt[2];
  
//   // Create reader object
//   TMVA::Reader *reader = new TMVA::Reader( "!Color:Silent" ); 
  
//   // Pass variables to the reader
//   reader->AddVariable("WH3l_dphilllmet",                                  &WH3l_dphilllmet_);
//   reader->AddVariable("MinIf$(WH3l_mOSll[],  WH3l_mOSll[Iteration$]>0)",  &WH3l_mOSll_min_);
//   reader->AddVariable("MinIf$(WH3l_ptOSll[], WH3l_ptOSll[Iteration$]>0)", &WH3l_ptOSll_min_);
//   reader->AddVariable("MinIf$(WH3l_drOSll[], WH3l_drOSll[Iteration$]>0)", &WH3l_drOSll_min_);
//   // reader->AddVariable("WH3l_ZVeto",                                       &WH3l_ZVeto_);
//   // reader->AddVariable("WH3l_mtlmet[1]",                                   &WH3l_mtlmet_1_);
//   // reader->AddVariable("WH3l_mtlmet[2]",                                   &WH3l_mtlmet_2_);
//   reader->AddVariable("WH3l_dphilmet[0]",                                 &WH3l_dphilmet_0_);
//   reader->AddVariable("WH3l_dphilmet[1]",                                 &WH3l_dphilmet_1_);
//   reader->AddVariable("WH3l_dphilmet[2]",                                 &WH3l_dphilmet_2_);
//   reader->AddVariable("WH3l_ptWWW",                                       &WH3l_ptWWW_);
//   reader->AddVariable("PuppiMET_pt",                                      &PuppiMET_pt_);
//   reader->AddVariable("Alt$(Lepton_pt[0],0)",                             &Lepton_pt_0_);
//   reader->AddVariable("Alt$(Lepton_pt[1],0)",                             &Lepton_pt_1_);
//   reader->AddVariable("Alt$(Lepton_pt[2],0)",                             &Lepton_pt_2_);

//   // Tell the reader which xml file to read
//   reader->BookMVA(BDT_name, xml_file_name);
  
//   // Evaluate the BDT value
//   float classifier = reader->EvaluateMVA(BDT_name);

//   // Delete reader object
//   delete reader;

//   // Return BDT value
//   return classifier;
    
// }

// #endif
