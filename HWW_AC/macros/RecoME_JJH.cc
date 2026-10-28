#ifndef RECOME
#define RECOME

#include "TLorentzVector.h"
#include <iostream>
#include "ROOT/RVec.hxx"
#include <map>

//#include "/afs/cern.ch/work/d/dmoran/private/Run3AC/mkShapesRDF/JHUGenMELA/MELA/interface/Mela.h"

using namespace ROOT;
using namespace ROOT::VecOps;
using LorentzVectorM = ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float>>;

// Production based MEs for Kinematic discriminants

/////// VH corrections //////
// replace the true BW V shape with a parameterized one more suitable for smearing effects on jets.
// Average ME constant for int KDs, depends on mH

class RECOME_JJH{
public:

  TVar::Production prod;
  float nCleanJet,  nLepton;
  float PuppiMet_pt,  PuppiMet_phi;
  RVecF Lepton_pt,  Lepton_phi,  Lepton_eta, CleanJet_pt,  CleanJet_phi,  CleanJet_eta;

  Mela* mela;
  Double_t LHCsqrts_= 13.6, mh_= 125.;
  TVar::VerbosityLevel verbosity_ = TVar::SILENT;
  TVar::MatrixElement me_ = TVar::JHUGen;

  float cw  = 0.8768;
  float sw  = 0.4808;
  float mZ  = 91.2;
  float mZ2  = mZ*mZ;
  float L = 100.0;
  float L2 = L*L;
  float csw = cw*cw-sw*sw;

  // 9 couplings assuming a_ZZ = a_WW (AC approach)
  float GetHVVpME_AC(RVecF coups){

   float me = -999;

   mela->setProcess(TVar::SelfDefine_spin0, me_, prod);
   mela->selfDHzzcoupl[0][gHIGGS_VV_1][0]       = coups[0]; //a1 (SM)
   mela->selfDHzzcoupl[0][gHIGGS_VV_2][0]       = coups[1]; //a2
   mela->selfDHzzcoupl[0][gHIGGS_VV_4][0]       = coups[2]; //a3
   mela->selfDHzzcoupl[0][gHIGGS_VV_1_PRIME2][0]= coups[3]; //k1
   mela->selfDHzzcoupl[0][gHIGGS_ZA_1_PRIME2][0]= coups[4]; //k2Zg
   mela->selfDHzzcoupl[0][gHIGGS_ZA_2][0]       = coups[5]; //a2Zg
   mela->selfDHzzcoupl[0][gHIGGS_ZA_4][0]       = coups[6]; //a3Zg
   mela->selfDHzzcoupl[0][gHIGGS_AA_2][0]       = coups[7]; //a2gg
   mela->selfDHzzcoupl[0][gHIGGS_AA_4][0]       = coups[8]; //a3gg

   mela->computeProdP(me, true);

   return me;
  }

  // 8 couplings assuming a_ZZ and a_WW SMEFT relationships (k2Zg not independent)
  float GetHVVpME_SMEFT(RVecF coups){

    float me = -999;

    float a1   = coups[0];
    float a2   = coups[1];
    float a3   = coups[2];
    float k1   = coups[3];
    float a2Zg = coups[4];
    float a3Zg = coups[5];
    float a2gg = coups[6];
    float a3gg = coups[7];

    float a1WW = a1;
    float a2WW = cw*cw*a2 + sw*sw*a2gg + 2*sw*cw*a2Zg;
    float a3WW = cw*cw*a3 + sw*sw*a3gg + 2*sw*cw*a3Zg;
    float k1WW = k1/csw + 2*sw*sw*L2*(a2gg-a2)/(mZ2*csw) + 2*L2*(sw/cw)*(a2Zg/mZ2);
    float k2Zg = 2*sw*cw*k1/csw + 2*sw*cw*L2*(a2gg-a2)/(mZ2*csw) + 2*L2*(a2Zg/mZ2);

    mela->setProcess(TVar::SelfDefine_spin0, me_, prod);
    mela->differentiate_HWW_HZZ=true;
    mela->selfDHzzcoupl[0][gHIGGS_VV_1][0]       = a1;
    mela->selfDHwwcoupl[0][gHIGGS_VV_1][0]       = a1WW;
    mela->selfDHzzcoupl[0][gHIGGS_VV_2][0]       = a2;
    mela->selfDHwwcoupl[0][gHIGGS_VV_2][0]       = a2WW;
    mela->selfDHzzcoupl[0][gHIGGS_VV_4][0]       = a3;
    mela->selfDHwwcoupl[0][gHIGGS_VV_4][0]       = a3WW;
    mela->selfDHzzcoupl[0][gHIGGS_VV_1_PRIME2][0]= k1;
    mela->selfDHwwcoupl[0][gHIGGS_VV_1_PRIME2][0]= k1WW;
    mela->selfDHzzcoupl[0][gHIGGS_ZA_1_PRIME2][0]= k2Zg;
    mela->selfDHzzcoupl[0][gHIGGS_ZA_2][0]       = a2Zg;
    mela->selfDHzzcoupl[0][gHIGGS_ZA_4][0]       = a3Zg;
    mela->selfDHzzcoupl[0][gHIGGS_AA_2][0]       = a2gg;
    mela->selfDHzzcoupl[0][gHIGGS_AA_4][0]       = a3gg;

    mela->computeProdP(me, true);

    return me;

  }

  float GetHGGpME(RVecF coups){

   float me = -999;

   mela->setProcess(TVar::SelfDefine_spin0, me_, prod);
   mela->selfDHggcoupl[0][gHIGGS_GG_2][0]= coups[0]; //a2 (SM)
   mela->selfDHggcoupl[0][gHIGGS_GG_4][0]= coups[1]; //a3

   mela->computeProdP(me, true);

   return me;
  }

  RECOME_JJH(){
    mela = new Mela(LHCsqrts_, mh_, verbosity_);
  }

  RVecF operator()(TVar::Production _prod,
		   float _nCleanJet, float _nLepton, float _PuppiMet_pt, float _PuppiMet_phi,
		   RVecF _Lepton_pt, RVecF _Lepton_phi, RVecF _Lepton_eta,
		   RVecF _CleanJet_pt, RVecF _CleanJet_phi, RVecF _CleanJet_eta) {

    prod = _prod;
    nCleanJet=_nCleanJet;  nLepton=_nLepton;  PuppiMet_pt=_PuppiMet_pt;
    PuppiMet_phi=_PuppiMet_phi;
    Lepton_pt=_Lepton_pt;
    Lepton_phi=_Lepton_phi; Lepton_eta=_Lepton_eta;
    CleanJet_pt=_CleanJet_pt; CleanJet_phi=_CleanJet_phi; CleanJet_eta=_CleanJet_eta;

    TLorentzVector L1(0.,0.,0.,0.);
    TLorentzVector L2(0.,0.,0.,0.);
    TLorentzVector LL(0.,0.,0.,0.);
    TLorentzVector NuNu(0.,0.,0.,0.);
    TLorentzVector Higgs(0.,0.,0.,0.);
    TLorentzVector J1(0.,0.,0.,0.);
    TLorentzVector J2(0.,0.,0.,0.);

    string sig;
    if(prod==TVar::JJQCD) sig = "ggf";
    else if(prod==TVar::JJVBF) sig = "vbf";
    else if(prod==TVar::Had_WH || prod==TVar::Had_ZH) sig = "vh";
    else std::cout<<"The signal production type has not been considered here "<<std::endl;

    RVecF MEs;

    if(nCleanJet >= 2 && nLepton > 1){

      L1.SetPtEtaPhiM(Lepton_pt[0], Lepton_eta[0], Lepton_phi[0], 0.0);
      L2.SetPtEtaPhiM(Lepton_pt[1], Lepton_eta[1], Lepton_phi[1], 0.0);

      J1.SetPtEtaPhiM(CleanJet_pt[0], CleanJet_eta[0], CleanJet_phi[0], 0.0); 
      J2.SetPtEtaPhiM(CleanJet_pt[1], CleanJet_eta[1], CleanJet_phi[1], 0.0);

      LL = L1 + L2;

      double nunu_px = PuppiMet_pt*cos(PuppiMet_phi);
      double nunu_py = PuppiMet_pt*sin(PuppiMet_phi);
      double nunu_pz = LL.Pz();
      double nunu_m = 30.0;

      double nunu_e = sqrt(nunu_px*nunu_px + nunu_py*nunu_py + nunu_pz*nunu_pz + nunu_m*nunu_m);
      NuNu.SetPxPyPzE(nunu_px, nunu_py, nunu_pz, nunu_e);
      Higgs = LL + NuNu;

      SimpleParticleCollection_t daughter;
      SimpleParticleCollection_t associated;
      SimpleParticleCollection_t mother;

      daughter.push_back(SimpleParticle_t(25, Higgs));

      associated.push_back(SimpleParticle_t(0,J1));
      associated.push_back(SimpleParticle_t(0,J2));

      mela->setCandidateDecayMode(TVar::CandidateDecay_Stable);
      mela->setInputEvent(&daughter, &associated, 0, 0);
      mela->setCurrentCandidateFromIndex(0);

      float h_mass   = Higgs.M();
      MEs.push_back(h_mass); //0

      if(sig == "ggf"){ // 2 Hgg couplings

       RVecF a2{1,0};
       RVecF a3{0,1};
       RVecF a2a3{1,1};

       float me_hsm   = GetHGGpME(a2);
       float me_hm    = GetHGGpME(a3);
       float me_mixhm = GetHGGpME(a2a3);

       MEs.push_back(me_hsm); //1
       MEs.push_back(me_hm);
       MEs.push_back(me_mixhm); //3

      }else{ // VBF/VH
       
       // SMEFT approach with 8 couplings
       RVecF a1   {1,0,0,0,0,0,0,0};
       RVecF a2   {0,1,0,0,0,0,0,0};
       RVecF a3   {0,0,1,0,0,0,0,0};
       RVecF k1   {0,0,0,1,0,0,0,0};
       RVecF z2   {0,0,0,0,1,0,0,0};
       RVecF z3   {0,0,0,0,0,1,0,0};
       RVecF g2   {0,0,0,0,0,0,1,0};
       RVecF g3   {0,0,0,0,0,0,0,1};
       RVecF a1a2 {1,1,0,0,0,0,0,0};
       RVecF a1a3 {1,0,1,0,0,0,0,0};
       RVecF a1k1 {1,0,0,1,0,0,0,0}; 
       RVecF a1z2 {1,0,0,0,1,0,0,0};
       RVecF a1z3 {1,0,0,0,0,1,0,0};
       RVecF a1g2 {1,0,0,0,0,0,1,0};
       RVecF a1g3 {1,0,0,0,0,0,0,1};

       float me_hsm     = GetHVVpME_SMEFT(a1);
       float me_hp      = GetHVVpME_SMEFT(a2);
       float me_hm      = GetHVVpME_SMEFT(a3);
       float me_hl      = GetHVVpME_SMEFT(k1);
       float me_hpzg    = GetHVVpME_SMEFT(z2);
       float me_hmzg    = GetHVVpME_SMEFT(z3);
       float me_hpgg    = GetHVVpME_SMEFT(g2);
       float me_hmgg    = GetHVVpME_SMEFT(g3);
       float me_mixhp   = GetHVVpME_SMEFT(a1a2);
       float me_mixhm   = GetHVVpME_SMEFT(a1a3);
       float me_mixhl   = GetHVVpME_SMEFT(a1k1); 
       float me_mixhpzg = GetHVVpME_SMEFT(a1z2);
       float me_mixhmzg = GetHVVpME_SMEFT(a1z3);
       float me_mixhpgg = GetHVVpME_SMEFT(a1g2);
       float me_mixhmgg = GetHVVpME_SMEFT(a1g3);
       
       MEs.push_back(me_hsm);//1
       MEs.push_back(me_hp);
       MEs.push_back(me_hm);
       MEs.push_back(me_hl);
       MEs.push_back(me_hpzg);
       MEs.push_back(me_hmzg);
       MEs.push_back(me_hpgg);
       MEs.push_back(me_hmgg);//8
       MEs.push_back(me_mixhp);//9
       MEs.push_back(me_mixhm);
       MEs.push_back(me_mixhl);//11 
       MEs.push_back(me_mixhpzg);
       MEs.push_back(me_mixhmzg);
       MEs.push_back(me_mixhpgg);
       MEs.push_back(me_mixhmgg);//15
 
      }

      if(sig == "vh"){ // VH corrections //

       float PjjSmeared = -999;
       float PjjTrue    = -999;
       float avgME      = -999;

       mela->setProcess(TVar::HSMHiggs, me_, prod);
       mela->computeDijetConvBW(PjjSmeared, false);
       mela->computeDijetConvBW(PjjTrue, true);
       mela->computeProdP(avgME, true);
       mela->getConstant(avgME); // call after computeProdP

       MEs.push_back(PjjSmeared); //16
       MEs.push_back(PjjTrue);
       MEs.push_back(avgME);//18
      
      }

      mela->resetInputEvent();
    }

    return MEs;

  }
};

#endif
