
#ifndef doHiggsPolarization
#define doHiggsPolarization

#include "TSystem.h"
#include "iostream"
#include "vector"
#include "TLorentzVector.h"
#include "TMath.h"
#include "TSystem.h"
#include <map>
#include "TString.h"

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

#include "ROOT/RVec.hxx"

using namespace ROOT;
using namespace ROOT::VecOps;

Double_t MW = 80.3579736098775;
Double_t WW = 2.084298998278219;
Double_t s2w = 0.22283820939806098;
Double_t c2w = 0.777161790601939;
Double_t cL= 4.0*sqrt(c2w/2.0);
Double_t cR = 0.0;

Double_t GF = ROOT::Math::sqrt(2)/(2*246*246);
Double_t gW = ROOT::Math::sqrt((GF/ROOT::Math::sqrt(2)) * 8 * MW*MW);
Double_t ghWW = gW*MW;

TVector3 rotinv(TVector3 p, TVector3 q){

  TVector3 pp(0.0, 0.0, 0.0);

  double qmodt = q.X()*q.X()+q.Y()*q.Y();
  double qmod = qmodt + q.Z()*q.Z();
  qmodt = TMath::Sqrt(qmodt);
  qmod = TMath::Sqrt(qmod);
  
  if (qmod==0.0){
    cout << "Error while rotation" << endl;
    return pp;
  }

  double cth = q.Z() / qmod;
  double sth = 1.0 - cth*cth;

  if (sth==0.0){
    pp = p;
    return pp;
  }

  sth = TMath::Sqrt(sth);
  
  if (qmodt==0.0){
    pp = p;
    return pp;
  }

  double cfi = q.X() / qmodt;
  double sfi = q.Y() / qmodt;

  double p1 = p.X();
  double p2 = p.Y();
  double p3 = p.Z();

  double pp1 = cth*cfi*p1+cth*sfi*p2-sth*p3;
  double pp2 = -sfi*p1+cfi*p2;
  double pp3 = sth*cfi*p1+sth*sfi*p2+cth*p3;
  
  pp.SetXYZ(pp1, pp2, pp3);
  return pp;
}


TLorentzVector boostinv(TLorentzVector q, TLorentzVector pboost){

  TLorentzVector qprime(0.0, 0.0, 0.0, 0.0); 

  double rmboost = pboost.E()*pboost.E() - pboost.X()*pboost.X() - pboost.Y()*pboost.Y() - pboost.Z()*pboost.Z();
  if (rmboost>0.0){
    rmboost = TMath::Sqrt(rmboost);
  }else{
    rmboost = 0.0;
  }
  
  double aux = (q.E()*pboost.E() - q.X()*pboost.X() - q.Y()*pboost.Y() - q.Z()*pboost.Z()) / rmboost ;
  double aaux = (aux+q.E()) / (pboost.E()+rmboost);
  
  double qprimeE = aux;
  double qprimeX = q.X() - aaux*pboost.X();
  double qprimeY = q.Y() - aaux*pboost.Y();
  double qprimeZ = q.Z() - aaux*pboost.Z();

  qprime.SetPxPyPzE(qprimeX, qprimeY, qprimeZ, qprimeE);
  
  return qprime;
}


Double_t distTheta00(Double_t costheta, Double_t costheta1){

  Double_t distTheta00_ = 16.0*(cR*cR*cR*cR + 2*cL*cL*cR*cR + cL*cL*cL*cL)*(1.0 - costheta*costheta)*(1.0 - costheta1*costheta1);
  return distTheta00_;  
}

Double_t distThetaLL(Double_t costheta, Double_t costheta1){

  Double_t distThetaLL_ = 4.0*(cR*cR*cR*cR*(1.0 + costheta)*(1.0 + costheta)*(1.0 + costheta1)*(1.0 + costheta1) + cL*cL*cR*cR*((1.0 + costheta)*(1.0 + costheta)*(1.0 - costheta1)*(1.0 - costheta1) + (1.0 - costheta)*(1.0 - costheta)*(1.0 + costheta1)*(1.0 + costheta1)) + cL*cL*cL*cL*(1.0 - costheta)*(1.0 - costheta)*(1.0 - costheta1)*(1.0 - costheta1));
  return distThetaLL_;
}

Double_t distThetaRR(Double_t costheta, Double_t costheta1){

  Double_t distThetaRR_ = 4.0*(cR*cR*cR*cR*(1.0 - costheta)*(1.0 - costheta)*(1.0 - costheta1)*(1.0 - costheta1) + cL*cL*cR*cR*((1.0 + costheta)*(1.0 + costheta)*(1.0 - costheta1)*(1.0 - costheta1) + (1.0 - costheta)*(1.0 - costheta)*(1.0 + costheta1)*(1.0 + costheta1)) + cL*cL*cL*cL*(1.0 + costheta)*(1.0 + costheta)*(1.0 + costheta1)*(1.0 + costheta1));
  return distThetaRR_;
}

Double_t distTheta0L(Double_t costheta, Double_t costheta1, Double_t cosphi){

  Double_t sintheta = TMath::Sqrt(1.0-costheta*costheta);
  Double_t sintheta1 = TMath::Sqrt(1.0-costheta1*costheta1);

  Double_t disTheta0L_ = -16.0*( cR*cR*cR*cR*(1.0 + costheta)*(1.0 + costheta1) + cL*cL*cL*cL*(1.0 - costheta)*(1.0 - costheta1) - cL*cL*cR*cR*( (1.0 + costheta)*(1.0 - costheta1) + (1.0-costheta)*(1.0+costheta1)))*sintheta*sintheta1*cosphi;

  return disTheta0L_;
}

Double_t distTheta0R(Double_t costheta, Double_t costheta1, Double_t cosphi){

  Double_t sintheta = TMath::Sqrt(1.0-costheta*costheta);
  Double_t sintheta1 = TMath::Sqrt(1.0-costheta1*costheta1);

  Double_t disTheta0R_ =-16.0*( cR*cR*cR*cR*(1.0 - costheta)*(1.0 - costheta1) + cL*cL*cL*cL*(1.0 + costheta)*(1.0 + costheta1) - cL*cL*cR*cR*( (1.0 + costheta)*(1.0 - costheta1) + (1.0-costheta)*(1.0+costheta1)))*sintheta*sintheta1*cosphi;

  return disTheta0R_;
}

Double_t distThetaLR(Double_t costheta, Double_t costheta1, Double_t cosphi){

  Double_t sintheta = TMath::Sqrt(1.0-costheta*costheta);
  Double_t sintheta1 = TMath::Sqrt(1.0-costheta1*costheta1);
  Double_t cos2phi = 2.0*cosphi*cosphi -1.0;

  Double_t disThetaLR_ = 8.0*(cL*cL + cR*cR)*(cL*cL + cR*cR)*sintheta*sintheta*sintheta1*sintheta1*cos2phi;
  return disThetaLR_;
}


/**
######################################################
##                                                  ##
### COMPUTE POLARIZED WEIGHTS FOR H -> WW ANALYSIS ### 
##                                                  ##
######################################################
**/

RVecF DoHiggsPolarizationWeight(
		      RVecF   GenPart_pt,
		      RVecF   GenPart_eta,
		      RVecF   GenPart_phi,
		      RVecF   GenPart_mass,
		      RVecI   GenPart_pdgId,
		      RVecI   GenPart_status,
		      RVecI   GenPart_genPartIdxMother
		      ){

  
  Double_t MW = 80.3579736098775;
  Double_t WW = 2.084298998278219;
  Double_t s2w = 0.22283820939806098;
  Double_t c2w = 0.777161790601939;
  Double_t cL= 4.0*sqrt(c2w/2.0);
  Double_t cR = 0.0;

  Double_t GF = ROOT::Math::sqrt(2)/(2*246*246);
  Double_t gW = ROOT::Math::sqrt((GF/ROOT::Math::sqrt(2)) * 8 * MW*MW);
  Double_t ghWW = gW*MW;

  Double_t LHCsqrts_= 13., mh_= 125.;
  
  ROOT::Math::PtEtaPhiEVector genWp;
  ROOT::Math::PtEtaPhiEVector genWm;
  ROOT::Math::PtEtaPhiEVector genlp;
  ROOT::Math::PtEtaPhiEVector genlm;
  ROOT::Math::PtEtaPhiEVector gennup;
  ROOT::Math::PtEtaPhiEVector gennum;
  ROOT::Math::PtEtaPhiEVector genH;
  TLorentzVector vector_lp; 
  TLorentzVector vector_lm; 
  TLorentzVector vector_nup;
  TLorentzVector vector_num;
  TLorentzVector vector_Wp; 
  TLorentzVector vector_Wm;
  
  TLorentzVector WP;
  TLorentzVector WM;
  TLorentzVector H;
  
       
  Int_t number_elec = 0;
  Int_t number_muon = 0;
  Int_t number_tau = 0;
  
  Int_t pos_wp = 999;
  Int_t pos_wm = 999;
  
  Int_t mother_pos = 0;

  unsigned int nGen = GenPart_pt.size();
    
  for (unsigned int p = 0; p < nGen; p++){

    // Leptons
    
    mother_pos = GenPart_genPartIdxMother[p];
    //if (GenPart_pdgId->At(p)==11 && GenPart_status->At(p)==1 && GenPart_pdgId->At(mother_pos)==-24){
    if (GenPart_pdgId[p]==11 && GenPart_pdgId[mother_pos]==-24 && GenPart_pdgId[GenPart_genPartIdxMother[mother_pos]]!=15){

      pos_wm = mother_pos;
      number_elec++;
      vector_lm.SetPtEtaPhiM(GenPart_pt[p], GenPart_eta[p], GenPart_phi[p], 0.0);
      genlm.SetCoordinates(GenPart_pt[p], GenPart_eta[p], GenPart_phi[p], vector_lm.E());

      //}else if (GenPart_pdgId->At(p)==-11 && GenPart_status->At(p)==1 && GenPart_pdgId->At(mother_pos)==24){
    }else if (GenPart_pdgId[p]==-11 && GenPart_pdgId[mother_pos]==24 && GenPart_pdgId[GenPart_genPartIdxMother[mother_pos]]!=-15){

      pos_wp = mother_pos;
      number_elec++;
      vector_lp.SetPtEtaPhiM(GenPart_pt[p], GenPart_eta[p], GenPart_phi[p], 0.0);
      genlp.SetCoordinates(GenPart_pt[p], GenPart_eta[p], GenPart_phi[p], vector_lp.E());    

      //}else if (GenPart_pdgId->At(p)==13 && GenPart_status->At(p)==1 && GenPart_pdgId->At(mother_pos)==-24){
    }else if (GenPart_pdgId[p]==13 && GenPart_pdgId[mother_pos]==-24 && GenPart_pdgId[GenPart_genPartIdxMother[mother_pos]]!=15){

      pos_wm = mother_pos;
      number_muon++;
      vector_lm.SetPtEtaPhiM(GenPart_pt[p], GenPart_eta[p], GenPart_phi[p], 0.0);
      genlm.SetCoordinates(GenPart_pt[p], GenPart_eta[p], GenPart_phi[p], vector_lm.E());

      //}else if (GenPart_pdgId->At(p)==-13 && GenPart_status->At(p)==1 && GenPart_pdgId->At(mother_pos)==24){
    }else if (GenPart_pdgId[p]==-13 && GenPart_pdgId[mother_pos]==24 && GenPart_pdgId[GenPart_genPartIdxMother[mother_pos]]!=-15){

      pos_wp = mother_pos;
      number_muon++;
      vector_lp.SetPtEtaPhiM(GenPart_pt[p], GenPart_eta[p], GenPart_phi[p], 0.0);
      genlp.SetCoordinates(GenPart_pt[p], GenPart_eta[p], GenPart_phi[p], vector_lp.E());    

    }else if (GenPart_pdgId[p]==15 && GenPart_pdgId[mother_pos]==-24){

      pos_wm = mother_pos;
      number_tau++;
      vector_lm.SetPtEtaPhiM(GenPart_pt[p], GenPart_eta[p], GenPart_phi[p], 0.0);
      genlm.SetCoordinates(GenPart_pt[p], GenPart_eta[p], GenPart_phi[p], vector_lm.E());

    }else if (GenPart_pdgId[p]==-15 && GenPart_pdgId[mother_pos]==24){

      pos_wp = mother_pos;
      number_tau++;
      vector_lp.SetPtEtaPhiM(GenPart_pt[p], GenPart_eta[p], GenPart_phi[p], 0.0);
      genlp.SetCoordinates(GenPart_pt[p], GenPart_eta[p], GenPart_phi[p], vector_lp.E());

    }


    // Neutrinos

    
    //if (GenPart_pdgId->At(p)==-12 && GenPart_status->At(p)==1 && GenPart_pdgId->At(mother_pos)==-24){
    if (GenPart_pdgId[p]==-12 && GenPart_pdgId[mother_pos]==-24 && GenPart_pdgId[GenPart_genPartIdxMother[mother_pos]]!=15){ 

      vector_num.SetPtEtaPhiM(GenPart_pt[p], GenPart_eta[p], GenPart_phi[p], 0.0);
      gennum.SetCoordinates(GenPart_pt[p], GenPart_eta[p], GenPart_phi[p], vector_num.E());

      //}else if (GenPart_pdgId->At(p)==12 && GenPart_status->At(p)==1 && GenPart_pdgId->At(mother_pos)==24){
    }else if (GenPart_pdgId[p]==12 && GenPart_pdgId[mother_pos]==24 && GenPart_pdgId[GenPart_genPartIdxMother[mother_pos]]!=-15){ 

      vector_nup.SetPtEtaPhiM(GenPart_pt[p], GenPart_eta[p], GenPart_phi[p], 0.0);
      gennup.SetCoordinates(GenPart_pt[p], GenPart_eta[p], GenPart_phi[p], vector_nup.E());    

      //}else if (GenPart_pdgId->At(p)==-14 && GenPart_status->At(p)==1 && GenPart_pdgId->At(mother_pos)==-24){
    }else if (GenPart_pdgId[p]==-14 && GenPart_pdgId[mother_pos]==-24 && GenPart_pdgId[GenPart_genPartIdxMother[mother_pos]]!=15){ 

      vector_num.SetPtEtaPhiM(GenPart_pt[p], GenPart_eta[p], GenPart_phi[p], 0.0);
      gennum.SetCoordinates(GenPart_pt[p], GenPart_eta[p], GenPart_phi[p], vector_num.E());

      //}else if (GenPart_pdgId->At(p)==14 && GenPart_status->At(p)==1 && GenPart_pdgId->At(mother_pos)==24){
    }else if (GenPart_pdgId[p]==14 && GenPart_pdgId[mother_pos]==24 && GenPart_pdgId[GenPart_genPartIdxMother[mother_pos]]!=-15){ 

      vector_nup.SetPtEtaPhiM(GenPart_pt[p], GenPart_eta[p], GenPart_phi[p], 0.0);
      gennup.SetCoordinates(GenPart_pt[p], GenPart_eta[p], GenPart_phi[p], vector_nup.E());    

    }else if (GenPart_pdgId[p]==-16 && GenPart_pdgId[mother_pos]==-24){

      vector_num.SetPtEtaPhiM(GenPart_pt[p], GenPart_eta[p], GenPart_phi[p], 0.0);
      gennum.SetCoordinates(GenPart_pt[p], GenPart_eta[p], GenPart_phi[p], vector_num.E());

    }else if (GenPart_pdgId[p]==16 && GenPart_pdgId[mother_pos]==24){

      vector_nup.SetPtEtaPhiM(GenPart_pt[p], GenPart_eta[p], GenPart_phi[p], 0.0);
      gennup.SetCoordinates(GenPart_pt[p], GenPart_eta[p], GenPart_phi[p], vector_nup.E());

    }

  } // End loop over particles


  
  // Assign the four-vector of the Ws
  vector_Wp.SetPtEtaPhiM(GenPart_pt[pos_wp], GenPart_eta[pos_wp], GenPart_phi[pos_wp], GenPart_mass[pos_wp]); // W plus
  genWp.SetCoordinates(GenPart_pt[pos_wp], GenPart_eta[pos_wp], GenPart_phi[pos_wp], vector_Wp.E());
      
  vector_Wm.SetPtEtaPhiM(GenPart_pt[pos_wm], GenPart_eta[pos_wm], GenPart_phi[pos_wm], GenPart_mass[pos_wm]); // W minus
  genWm.SetCoordinates(GenPart_pt[pos_wm], GenPart_eta[pos_wm], GenPart_phi[pos_wm], vector_Wm.E());
  
  
  //if (number_elec!=1 || number_muon!=1 || pos_wp==999 || pos_wm==999){
  //return  -999;
  //}

  if (((number_elec==0 || number_muon==0) && number_tau==0) || pos_wp==999 || pos_wm==999){
    return  RVecF(4, -9999.9);
  }

  // Boost over lepton from the Ws reference frame
  // Compute theta star  

  WP = vector_lp + vector_nup;
  WM = vector_lm + vector_num;
  H = WP + WM;

  // Leptons in the Lab frame
  TLorentzVector L11 = vector_lp;
  TLorentzVector L12 = vector_nup;
  TLorentzVector L21 = vector_num;
  TLorentzVector L22 = vector_lm;


  TLorentzVector L114l = boostinv(L11, H);
  TLorentzVector L124l = boostinv(L12, H);
  TLorentzVector L214l = boostinv(L21, H);
  TLorentzVector L224l = boostinv(L22, H);

  TLorentzVector WP4l = boostinv(WP, H);
  TLorentzVector WM4l = boostinv(WM, H);

  TLorentzVector L11V = boostinv(L114l, WP4l);
  TLorentzVector L21V = boostinv(L214l, WM4l);

  
  Double_t rmodwp = TMath::Sqrt(WP4l.X()*WP4l.X() + WP4l.Y()*WP4l.Y() + WP4l.Z()*WP4l.Z());
  Double_t rmodwm = TMath::Sqrt(WM4l.X()*WM4l.X() + WM4l.Y()*WM4l.Y() + WM4l.Z()*WM4l.Z());
  Double_t rmod11 = TMath::Sqrt(L11V.X()*L11V.X() + L11V.Y()*L11V.Y() + L11V.Z()*L11V.Z());
  Double_t rmod21 = TMath::Sqrt(L21V.X()*L21V.X() + L21V.Y()*L21V.Y() + L21V.Z()*L21V.Z());

  Double_t sprodwp = WP4l.X()*L11V.X() + WP4l.Y()*L11V.Y() + WP4l.Z()*L11V.Z();
  Double_t sprodwm = WM4l.X()*L21V.X() + WM4l.Y()*L21V.Y() + WM4l.Z()*L21V.Z();

  Double_t costhetawp = sprodwp / (rmodwp*rmod11);
  Double_t costhetawm = sprodwm / (rmodwm*rmod21);

  TVector3 p3wp = WP4l.Vect();
  TVector3 p3wm = WM4l.Vect();
  TVector3 p3l11 = L114l.Vect();
  TVector3 p3l21 = L214l.Vect();

  // Rotation
  //TVector3 p3l11R = p3l11;
  //TVector3 p3l21R = p3l21;

  //p3l11R.RotateUz(p3wp);
  //p3l21R.RotateUz(p3wp);

  TVector3 p3l11R = rotinv(p3l11, p3wp);
  TVector3 p3l21R = rotinv(p3l21, p3wp);
  

  Double_t pt11 = TMath::Sqrt(p3l11R.X()*p3l11R.X() + p3l11R.Y()*p3l11R.Y());
  Double_t pt21 = TMath::Sqrt(p3l21R.X()*p3l21R.X() + p3l21R.Y()*p3l21R.Y());
  
  
  Double_t cosphi = (p3l11R.X()*p3l21R.X() + p3l11R.Y()*p3l21R.Y()) / (pt11*pt21);
  Double_t dphill = TMath::ACos(cosphi);
  

  /**
  // https://arxiv.org/pdf/2105.07972.pdf
  
  /////////////////////////////////////
  //             |ALL|^2             //
  /////////////////////////////////////

  
  Double_t K = ((H.M()*H.M() - WP.M()*WP.M() - WM.M()*WM.M()) / (2 * WP.M() * WM.M()));


  Double_t ALL2 = K*K * 16*(cR*cR*cR*cR + 2*(cL*cL)*(cR*cR) + cL*cL*cL*cL)*(1.0-costhetawp*costhetawp)*(1.0-costhetawm*costhetawm);

  /////////////////////////////////////
  //             |A++|^2             //
  /////////////////////////////////////

  // Z Decay
  //Double_t plus1 = cL*cL*cL*cL * (1 + ROOT::Math::cos(theta_Wp_star))*(1 + ROOT::Math::cos(theta_Wp_star)) * (1 + ROOT::Math::cos(theta_Wm_star))*(1 + ROOT::Math::cos(theta_Wm_star));
  //Double_t plus2 = cR*cR*cR*cR * (1 - ROOT::Math::cos(theta_Wp_star))*(1 - ROOT::Math::cos(theta_Wp_star)) * (1 - ROOT::Math::cos(theta_Wm_star))*(1 - ROOT::Math::cos(theta_Wm_star));
  //Double_t plus3 = cR*cR*cL*cL * (1 + ROOT::Math::cos(theta_Wp_star))*(1 + ROOT::Math::cos(theta_Wp_star)) * (1 - ROOT::Math::cos(theta_Wm_star))*(1 - ROOT::Math::cos(theta_Wm_star));
  //Double_t plus4 = cR*cR*cL*cL * (1 - ROOT::Math::cos(theta_Wp_star))*(1 - ROOT::Math::cos(theta_Wp_star)) * (1 + ROOT::Math::cos(theta_Wm_star))*(1 + ROOT::Math::cos(theta_Wm_star));
  //
  //Double_t App2 = P1 * P2 * (plus1 + plus2 + plus3 + plus4);
  
  // W Decay
  Double_t plus1 = 4*cR*cR*cR*cR * (1 + costhetawp) * (1 + costhetawp) * (1 + costhetawm) * (1 + costhetawm);
  Double_t plus2 = 4*cL*cL*cL*cL * (1 - costhetawp) * (1 - costhetawp) * (1 - costhetawm) * (1 - costhetawm);
  Double_t plus3 = 4*cL*cL*cR*cR * (1 + costhetawp) * (1 + costhetawp) * (1 - costhetawm) * (1 - costhetawm);
  Double_t plus4 = 4*cR*cR*cL*cL * (1 - costhetawp) * (1 - costhetawp) * (1 + costhetawm) * (1 + costhetawm);

  Double_t App2 = plus1 + plus2 + plus3 + plus4;


  /////////////////////////////////////
  //             |A--|^2             //
  /////////////////////////////////////
  

  // Z Decay
  //Double_t minus1 = cL*cL*cL*cL * (1 - ROOT::Math::cos(theta_Wp_star))*(1 - ROOT::Math::cos(theta_Wp_star)) * (1 - ROOT::Math::cos(theta_Wm_star))*(1 - ROOT::Math::cos(theta_Wm_star));
  //Double_t minus2 = cR*cR*cR*cR * (1 + ROOT::Math::cos(theta_Wp_star))*(1 + ROOT::Math::cos(theta_Wp_star)) * (1 + ROOT::Math::cos(theta_Wm_star))*(1 + ROOT::Math::cos(theta_Wm_star));
  //Double_t minus3 = cR*cR*cL*cL * (1 + ROOT::Math::cos(theta_Wp_star))*(1 + ROOT::Math::cos(theta_Wp_star)) * (1 - ROOT::Math::cos(theta_Wm_star))*(1 - ROOT::Math::cos(theta_Wm_star));
  //Double_t minus4 = cR*cR*cL*cL * (1 - ROOT::Math::cos(theta_Wp_star))*(1 - ROOT::Math::cos(theta_Wp_star)) * (1 + ROOT::Math::cos(theta_Wm_star))*(1 + ROOT::Math::cos(theta_Wm_star));
  
  //Double_t Amm2 = P1 * P2 * (minus1 + minus2 + minus3 + minus4);

  // W Decay
  Double_t minus1 = 4*cR*cR*cR*cR * (1 - costhetawp) * (1 - costhetawp) * (1 - costhetawm) * (1 - costhetawm);
  Double_t minus2 = 4*cL*cL*cL*cL * (1 + costhetawp) * (1 + costhetawp) * (1 + costhetawm) * (1 + costhetawm);
  Double_t minus3 = 4*cL*cL*cR*cR * (1 - costhetawp) * (1 - costhetawp) * (1 + costhetawm) * (1 + costhetawm);
  Double_t minus4 = 4*cR*cR*cL*cL * (1 + costhetawp) * (1 + costhetawp) * (1 - costhetawm) * (1 - costhetawm);

  Double_t Amm2 = minus1+ minus2+ minus3+ minus4;
  

  /////////////////////////////////////
  //            2Re(ALL++)           //
  /////////////////////////////////////

  Double_t sinthetawp = TMath::Sqrt(1.0-costhetawp*costhetawp);
  Double_t sinthetawm = TMath::Sqrt(1.0-costhetawm*costhetawm);


  Double_t LLpp1 = cL*cL*cL*cL * (1 - costhetawp) * (1 - costhetawm);
  Double_t LLpp2 = cR*cR*cR*cR * (1 + costhetawp) * (1 + costhetawm);
  Double_t LLpp3 = cL*cL*cR*cR * (1 + costhetawp) * (1 - costhetawm);
  Double_t LLpp4 = cR*cR*cL*cL * (1 - costhetawp) * (1 + costhetawm);

  Double_t ReALLpp = -16.0 * K * (LLpp1+LLpp2+LLpp3+LLpp4) * sinthetawp * sinthetawm * cosphi;


  /////////////////////////////////////
  //            2Re(ALL--)           //
  /////////////////////////////////////

  Double_t LLmm1 = cL*cL*cL*cL * (1 + costhetawp) * (1 + costhetawm);
  Double_t LLmm2 = cR*cR*cR*cR * (1 - costhetawp) * (1 - costhetawm);
  Double_t LLmm3 = cL*cL*cR*cR * (1 - costhetawp) * (1 + costhetawm);
  Double_t LLmm4 = cR*cR*cL*cL * (1 + costhetawp) * (1 - costhetawm);

  Double_t ReALLmm = -16.0 * K * (LLmm1+LLmm2+LLmm3+LLmm4) * sinthetawp * sinthetawm * cosphi;


  /////////////////////////////////////
  //            2Re(A++--)           //
  /////////////////////////////////////

  Double_t cos2phi = 2.0*cosphi*cosphi - 1.0;

  Double_t ReAppmm = 8.0 * ((cL*cL + cR*cR)*(cL*cL + cR*cR)) * sinthetawp*sinthetawp * sinthetawm*sinthetawm * cos2phi;
  
  
  /////////////////////////////////////
  //             |ATT|^2             //
  /////////////////////////////////////
  
  Double_t ATT2 = App2 + Amm2 + ReAppmm;
  **/



  Double_t Q1 = H.E()*H.E() - H.X()*H.X() - H.Y()*H.Y() - H.Z()*H.Z();
  Double_t Q2 = WP.E()*WP.E() - WP.X()*WP.X() - WP.Y()*WP.Y() - WP.Z()*WP.Z();
  Double_t Q3 = WM.E()*WM.E() - WM.X()*WM.X() - WM.Y()*WM.Y() - WM.Z()*WM.Z();
  Double_t epsfact = (Q1-Q2-Q3)/TMath::Sqrt(Q2*Q3)*0.5;

  Double_t K = epsfact;

  Double_t ALL2 = epsfact*epsfact * distTheta00(costhetawp, costhetawm);
  Double_t App2 = distThetaLL(costhetawp, costhetawm);
  Double_t Amm2 = distThetaRR(costhetawp, costhetawm);
  Double_t ReALLpp = epsfact*distTheta0L(costhetawp, costhetawm, cosphi);
  Double_t ReALLmm = epsfact*distTheta0R(costhetawp, costhetawm, cosphi);
  Double_t ReAppmm = distThetaLR(costhetawp, costhetawm, cosphi);

  Double_t ATT2 = App2 + Amm2 + ReAppmm;

  // Final weights  
  float weight_LL = (float)(ALL2 / (ALL2 + ATT2 + ReALLpp + ReALLmm));
  
  float weight_TT = (float)(ATT2 / (ALL2 + ATT2 + ReALLpp + ReALLmm));

  float weight_Int = (float)((ReALLpp + ReALLmm) / (ALL2 + ATT2 + ReALLpp + ReALLmm));

  float weight_TTInt = (float)((ATT2 + ReALLpp + ReALLmm) / (ALL2 + ATT2 + ReALLpp + ReALLmm));

  float weight_woInt = (float)((ALL2 + ATT2  + ReALLpp + ReALLmm) / (ALL2 + ATT2));

  //cout << "LL Weight --> " << weight_LL << endl;  

  RVecF results = {weight_LL, weight_TT, weight_Int, weight_TTInt};
  return results;
    
}  


#endif
