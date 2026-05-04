#ifndef MT2 
#define MT2
#include <vector>

#include "TVector2.h"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"

#include <iostream>
#include <TMath.h>
#include "ROOT/RVec.hxx"
#include "TLorentzVector.h"

#include <algorithm>
#include <TMinuit.h>

using namespace ROOT;
using namespace ROOT::VecOps;
std::vector<double>* VectX = new std::vector<double>;
void functionMT2(int& npar, double* d, double& r, double par[], int flag){
 int n = VectX->size();
 double maxmt2 = 0.0;
 
 
 double px1 = VectX->at(0);
 double py1 = VectX->at(1);
 double px2 = VectX->at(2);
 double py2 = VectX->at(3);
 double metx = VectX->at(4);
 double mety = VectX->at(5);
 
 double met1    = par[0];
 double metphi1 = par[1];
 double metx1 = met1 * cos (metphi1);
 double mety1 = met1 * sin (metphi1);
 
 double metx2 = metx - metx1;
 double mety2 = mety - mety1;
 double met2 = sqrt(metx2*metx2 + mety2*mety2);
 
 double p1 = sqrt(px1*px1 + py1*py1);
 double p2 = sqrt(px2*px2 + py2*py2);
 double mt1 = 2. * p1 * met1 * (1.-(px1*metx1+py1*mety1)/(p1*met1));
 double mt2 = 2. * p2 * met2 * (1.-(px2*metx2+py2*mety2)/(p2*met2));
 
 if (mt1>mt2) maxmt2 = mt1;
 else maxmt2 = mt2;
 
 r = sqrt(maxmt2);
}

float mT2(
		    RVecF   Lepton_pt,
		    RVecF   Lepton_eta,
		    RVecF   Lepton_phi,
		    float   PuppiMET_pt,
		    float   PuppiMET_phi
        ){
  float mT2;
  float xPI = 3.14159266;

  if (Lepton_pt.size() < 2) {
        return -9999.; 
  } else if(Lepton_pt[0] < 0 || Lepton_pt[1] < 0) {
        return -9999.; 
  }

  TLorentzVector L1{0., 0., 0., 0.,};
  TLorentzVector L2{0., 0., 0., 0.,};
  TLorentzVector MET{0., 0., 0., 0.,};
  L1.SetPtEtaPhiM(Lepton_pt[0], Lepton_eta[0], Lepton_phi[0], 0.);
  L2.SetPtEtaPhiM(Lepton_pt[1], Lepton_eta[1], Lepton_phi[1], 0.);
  MET.SetPtEtaPhiM(PuppiMET_pt, 0., PuppiMET_phi, 0.);
  float met = MET.E();

  if (VectX->size() != 6) {
   VectX->push_back( L1.X()  );
   VectX->push_back( L1.Y()  );
   VectX->push_back( L2.X()  );
   VectX->push_back( L2.Y()  );
   VectX->push_back( MET.X() );
   VectX->push_back( MET.Y() );
  }
  else {
   VectX->at(0) = L1.X()  ;
   VectX->at(1) = L1.Y()  ;
   VectX->at(2) = L2.X()  ;
   VectX->at(3) = L2.Y()  ;
   VectX->at(4) = MET.X() ;
   VectX->at(5) = MET.Y() ;
  }

  const int nParametri = 2;
  TMinuit minuit(nParametri);
  minuit.SetFCN(functionMT2);
  minuit.SetPrintLevel(-1); // quiet
  double par[nParametri]={met/2.,0.0};
  double stepSize[nParametri]={met/100.,0.001};
  double minVal[nParametri]={met/100.,0.0};
  double maxVal[nParametri]={30.*met,2.*xPI};
  string parName[nParametri]={"met1","metphi1"};
  for (int i=0; i<nParametri; i++){
   minuit.DefineParameter(i,parName[i].c_str(),par[i],stepSize[i],minVal[i],maxVal[i]);
  }
  minuit.Migrad();

  mT2 = minuit.fAmin;
  return mT2;
}

#endif
