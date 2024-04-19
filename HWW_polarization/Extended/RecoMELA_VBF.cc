#include "TLorentzVector.h"

#include <iostream>
#include "ROOT/RVec.hxx"

#include "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/mkShapesRDF/JHUGenMELA/MELA/interface/Mela.h"

using namespace ROOT;
using namespace ROOT::VecOps;
using LorentzVectorM = ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float>>;


class RECOMELA_VBF{
public:

  float nCleanJet,  nLepton;
  float PuppiMet_pt,  PuppiMet_phi;
  RVecF Lepton_pt,  Lepton_phi,  Lepton_eta, CleanJet_pt,  CleanJet_phi,  CleanJet_eta;
  RVecI Lepton_pdgId;
  Mela* mela;
  Double_t LHCsqrts_= 13., mh_= 125.;
  TVar::VerbosityLevel verbosity_ = TVar::SILENT;

   

  RECOMELA_VBF(){
    mela = new Mela(LHCsqrts_, mh_, verbosity_);
  }

  RVecF operator()(float _nCleanJet, float _nLepton, float _PuppiMet_pt, float _PuppiMet_phi,
		   RVecF _Lepton_pt, RVecF _Lepton_phi, RVecF _Lepton_eta,
		   RVecF _CleanJet_pt, RVecF _CleanJet_phi, RVecF _CleanJet_eta,
		   RVecI _Lepton_pdgId) {
    

    nCleanJet=_nCleanJet;  nLepton=_nLepton;  PuppiMet_pt=_PuppiMet_pt;
    PuppiMet_phi=_PuppiMet_phi;  
    Lepton_pt=_Lepton_pt;
    Lepton_phi=_Lepton_phi; Lepton_eta=_Lepton_eta;
    CleanJet_pt=_CleanJet_pt; CleanJet_phi=_CleanJet_phi; CleanJet_eta=_CleanJet_eta;
    Lepton_pdgId=_Lepton_pdgId;

    RVecF me;
    me.reserve(3);

    TLorentzVector L1(0.,0.,0.,0.);
    TLorentzVector L2(0.,0.,0.,0.);
    TLorentzVector LL(0.,0.,0.,0.);
    TLorentzVector NuNu(0.,0.,0.,0.);
    TLorentzVector Higgs(0.,0.,0.,0.);
    TLorentzVector J1(0.,0.,0.,0.);
    TLorentzVector J2(0.,0.,0.,0.);
     
    if(nCleanJet >= 2 && nLepton > 1){
   
      int absId1{static_cast<int>(Lepton_pdgId[0])};
      int absId2{static_cast<int>(Lepton_pdgId[1])};

      if (absId1*absId2 != -11*13) {
	me = {-9999., -9999., -9999.};
	return me;
      }

      L1.SetPtEtaPhiM(Lepton_pt[0], Lepton_eta[0], Lepton_phi[0], 0.0);
      L2.SetPtEtaPhiM(Lepton_pt[1], Lepton_eta[1], Lepton_phi[1], 0.0);
     
      J1.SetPtEtaPhiM(CleanJet_pt[0], CleanJet_eta[0], CleanJet_phi[0], 0.0);
      J2.SetPtEtaPhiM(CleanJet_pt[1], CleanJet_eta[1], CleanJet_phi[1], 0.0);

      LL = L1 + L2;
    
      double nunu_px = PuppiMet_pt*cos(PuppiMet_phi);
      double nunu_py = PuppiMet_pt*sin(PuppiMet_phi);
      double nunu_pz = LL.Pz();
      double nunu_m = 30.0; //Why 30? --> https://indico.cern.ch/event/850505/contributions/3593915/

      double nunu_e = sqrt(nunu_px*nunu_px + nunu_py*nunu_py + nunu_pz*nunu_pz + nunu_m*nunu_m);
      NuNu.SetPxPyPzE(nunu_px, nunu_py, nunu_pz, nunu_e);
      Higgs = LL + NuNu;
     
      SimpleParticleCollection_t daughter;
      SimpleParticleCollection_t associated;
      SimpleParticleCollection_t mother;
     
      daughter.push_back(SimpleParticle_t(25, Higgs));
     
      associated.push_back(SimpleParticle_t(0,J1));
      associated.push_back(SimpleParticle_t(0,J2));
     
      if (Higgs.Pt() == 0 || Higgs.M()==0 || Lepton_pt[0] < 10 || Lepton_pt[1] < 10 || CleanJet_pt[0] < 30 || CleanJet_pt[1] < 30){
	me = {-9999., -9999., -9999.};
	return me;
      }
      
      mela->setCandidateDecayMode(TVar::CandidateDecay_WW); //Decay to WW                                                                                                                                    
      mela->setInputEvent(&daughter, &associated, 0, false);
      mela->setCurrentCandidateFromIndex(0);
     
      float RecoLevel_me_VBF_hsm = 0.;
      float RecoLevel_me_QCD_hsm = 0.;
     
      mela->setProcess(TVar::HSMHiggs, TVar::JHUGen, TVar::JJVBF);
      mela->computeProdP(RecoLevel_me_VBF_hsm, true);
     
      mela->setProcess(TVar::HSMHiggs, TVar::JHUGen, TVar::JJQCD);
      mela->computeProdP(RecoLevel_me_QCD_hsm, true);
     
      float D_VBF_QCD = RecoLevel_me_VBF_hsm*RecoLevel_me_VBF_hsm / (RecoLevel_me_VBF_hsm*RecoLevel_me_VBF_hsm + RecoLevel_me_QCD_hsm*RecoLevel_me_QCD_hsm);
         
      //  compute D_VBF_VH
      float RecoLevel_me_Had_WH_hsm = 0.;
      float RecoLevel_me_Had_ZH_hsm = 0.;
      float RecoLevel_me_VH_hsm = 0.;

      mela->setProcess(TVar::HSMHiggs, TVar::JHUGen, TVar::Had_ZH);
      mela->computeProdP(RecoLevel_me_Had_ZH_hsm, true);

      mela->setProcess(TVar::HSMHiggs, TVar::JHUGen, TVar::Had_WH);
      mela->computeProdP(RecoLevel_me_Had_WH_hsm, true);

      RecoLevel_me_VH_hsm = RecoLevel_me_Had_ZH_hsm + RecoLevel_me_Had_WH_hsm;

      float D_VBF_VH = (RecoLevel_me_VBF_hsm * RecoLevel_me_VBF_hsm) / (RecoLevel_me_VBF_hsm * RecoLevel_me_VBF_hsm  + 1e16 * (RecoLevel_me_VH_hsm * RecoLevel_me_VH_hsm));
        
      //  compute D_QCD_VH

      float D_VH_QCD = (RecoLevel_me_VH_hsm * RecoLevel_me_VH_hsm) / ((RecoLevel_me_VH_hsm * RecoLevel_me_VH_hsm) + 1e-16 * (RecoLevel_me_QCD_hsm * RecoLevel_me_QCD_hsm));
         
      me = {D_VBF_QCD, D_VBF_VH, D_VH_QCD };
      mela->resetInputEvent();
      return me;
    }
    else {
      me = {-9999., -9999., -9999.};
      return me;
    }
  }
};
