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


class BDT_WHSS_TopSemileptonic_v9{

public:

  BDT_WHSS_TopSemileptonic_v9( TString BDT_name, TString xml_file_name );
  ~BDT_WHSS_TopSemileptonic_v9();

  TString BDT_name_;
  TString xml_file_name_;

  float mll_;
  float mjj_;
  float mtw1_;
  float mtw2_;
  float ptll_;
  float mlljj20_whss_;
  float PuppiMET_pt_;
  float dphill_;
  float dphijj_;
  float dphillmet_;
  float dphilmet2_;
  float dphijet1met_;
  float jetpt1_;
  float Jet_btagDeepB_0_;
  float Jet_btagDeepB_1_;

  TMVA::Reader *reader = new TMVA::Reader();
  
  // RVecF jet_btagDeepB;
  // RVecI cleanJet_jetIdx;

  double operator()( float mll,
					 float mjj,
					 float mtw1,
					 float mtw2,
					 float ptll,
					 float mlljj20_whss,
					 float PuppiMET_pt,
					 float dphill,
					 float dphijj,
					 float dphillmet,
					 float dphilmet2,
					 float dphijet1met,
					 RVecF cleanJet_pt,
					 RVecF jet_btagDeepB,
					 RVecI cleanJet_jetIdx){

	// Assign variables values 
	mll_             = mll;
	mjj_             = mjj;
	mtw1_            = mtw1;
	mtw2_            = mtw2;
	ptll_            = ptll;
	mlljj20_whss_    = mlljj20_whss;
	PuppiMET_pt_     = PuppiMET_pt;
	dphill_          = dphill;
	dphijj_          = dphijj;
	dphillmet_       = dphillmet;
	dphilmet2_       = dphilmet2;
	dphijet1met_     = dphijet1met;
	jetpt1_          = cleanJet_pt[0];
	Jet_btagDeepB_0_ = cleanJet_jetIdx[0]>=0 ? jet_btagDeepB[cleanJet_jetIdx[0]] : -2;
	Jet_btagDeepB_1_ = cleanJet_jetIdx[1]>=0 ? jet_btagDeepB[cleanJet_jetIdx[1]] : -2;

	// Evaluate the classifier
	double classifier = reader->EvaluateMVA(BDT_name_);

	return classifier;
  }

};

BDT_WHSS_TopSemileptonic_v9::BDT_WHSS_TopSemileptonic_v9( TString BDT_name, TString xml_file_name ){

  std::cout << "BDT name:      " << BDT_name      << std::endl;
  std::cout << "xml file name: " << xml_file_name << std::endl;

  BDT_name_      = BDT_name;
  xml_file_name_ = xml_file_name;
  
  // Pass variables to the reader
  reader->AddVariable("mll            ", &mll_            );
  reader->AddVariable("mjj            ", &mjj_            );
  reader->AddVariable("mtw1           ", &mtw1_           );
  reader->AddVariable("mtw2           ", &mtw2_           );
  reader->AddVariable("ptll           ", &ptll_           );
  reader->AddVariable("mlljj20_whss   ", &mlljj20_whss_   );
  reader->AddVariable("PuppiMET_pt    ", &PuppiMET_pt_    );
  reader->AddVariable("dphill         ", &dphill_         );
  reader->AddVariable("dphijj         ", &dphijj_         );
  reader->AddVariable("dphillmet      ", &dphillmet_      );
  reader->AddVariable("dphilmet2      ", &dphilmet2_      );
  reader->AddVariable("dphijet1met    ", &dphijet1met_    );
  // Variables with Alt$ values
  reader->AddVariable("Alt$(CleanJet_pt[0],0)",                     &jetpt1_         );
  reader->AddVariable("Alt$(Jet_btagDeepB[CleanJet_jetIdx[0]],-2)", &Jet_btagDeepB_0_);
  reader->AddVariable("Alt$(Jet_btagDeepB[CleanJet_jetIdx[1]],-2)", &Jet_btagDeepB_1_);

  reader->BookMVA(BDT_name, xml_file_name);
}

BDT_WHSS_TopSemileptonic_v9::~BDT_WHSS_TopSemileptonic_v9(){
  
  std::cout << "Deleting reader" << std::endl;
  
  reader->Delete();
}

#endif
