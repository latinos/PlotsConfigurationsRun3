#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"
#include <map>
#include <set>
#include <list>

using namespace ROOT;
using namespace ROOT::VecOps;


class GENJJ{
public:

  int   nLHEPart, nGenPart;
  RVecF LHEPart_pt, LHEPart_eta, LHEPart_phi;
  RVecF GenPart_pt, GenPart_eta, GenPart_phi;
  RVecI LHEPart_pdgId, LHEPart_status;
  RVecI GenPart_pdgId, GenPart_genPartIdxMother;
  float Generator_x1, Generator_x2;
  int   Generator_id1, Generator_id2;

  GENJJ(){
  }

  RVecF operator()(int _nLHEPart, int _nGenPart,
		   RVecF _LHEPart_pt, RVecF _LHEPart_eta, RVecF _LHEPart_phi, RVecI _LHEPart_pdgId, RVecI _LHEPart_status,
		   RVecF _GenPart_pt, RVecF _GenPart_eta, RVecF _GenPart_phi, RVecI _GenPart_pdgId, RVecI _GenPart_genPartIdxMother,
		   float _Generator_x1, float _Generator_x2, int _Generator_id1, int _Generator_id2){

    nLHEPart = _nLHEPart;
    nGenPart = _nGenPart;
    LHEPart_pt = _LHEPart_pt; LHEPart_eta = _LHEPart_eta; LHEPart_phi = _LHEPart_phi;
    GenPart_pt = _GenPart_pt; GenPart_eta = _GenPart_eta; GenPart_phi = _GenPart_phi;
    LHEPart_pdgId = _LHEPart_pdgId; LHEPart_status = _LHEPart_status;
    GenPart_pdgId = _GenPart_pdgId; GenPart_genPartIdxMother = _GenPart_genPartIdxMother;
    Generator_x1 = _Generator_x1; Generator_id1 = _Generator_id1;
    Generator_x2 = _Generator_x2; Generator_id2 = _Generator_id2;

    RVecF Out;
    
    std::vector<int> jetindx;
    std::vector<int> lepindx;
    std::vector<int> neuindx;

    for (int i = 0; i < nLHEPart; i++) {
      int pid =  abs(LHEPart_pdgId[i]);
      if(((pid>0 && pid<7)||pid==21) && LHEPart_status[i]==1 && LHEPart_pt[i]>30){
       jetindx.push_back(i);
      }
      if((pid==11||pid==13||pid==15) && LHEPart_status[i]==1 && LHEPart_pt[i]>0){
       lepindx.push_back(i);
      }
      if((pid==12||pid==14||pid==16) && LHEPart_status[i]==1 && LHEPart_pt[i]>0){
       neuindx.push_back(i);
      }
    }

    int nJets  = jetindx.size();
    int nLeps  = lepindx.size();
    int nNeus  = neuindx.size();
    
    float dphi = -999;
    float mass = -999;
    float ll_mass = -999;
    float ll_pt = -999;
    float h_mass = -999;
    float h_pt = -999;

    if (nLeps==2 && nNeus==2){
      
      int il1 = lepindx[0];
      int il2 = lepindx[1];
      int in1 = neuindx[0];
      int in2 = neuindx[1];
	
      TLorentzVector L1(0.,0.,0.,0.);
      TLorentzVector L2(0.,0.,0.,0.);
      TLorentzVector N1(0.,0.,0.,0.);
      TLorentzVector N2(0.,0.,0.,0.);
      
      TLorentzVector LL(0.,0.,0.,0.);
      TLorentzVector H(0.,0.,0.,0.);
       
      L1.SetPtEtaPhiM(LHEPart_pt[il1], LHEPart_eta[il1], LHEPart_phi[il1], 0);
      L2.SetPtEtaPhiM(LHEPart_pt[il2], LHEPart_eta[il2], LHEPart_phi[il2], 0);
      N1.SetPtEtaPhiM(LHEPart_pt[in1], LHEPart_eta[in1], LHEPart_phi[in1], 0);
      N2.SetPtEtaPhiM(LHEPart_pt[in2], LHEPart_eta[in2], LHEPart_phi[in2], 0);

      LL = L1 + L2;
      H  = L1 + L2 + N1 + N2;
      ll_mass = LL.M();
      ll_pt   = LL.Pt();
      h_mass  = H.M();
      h_pt    = H.Pt();
	
    }
    
    if (nJets==2){
      
      int i1 = jetindx[0];
      int i2 = jetindx[1];
	
      TLorentzVector J1(0.,0.,0.,0.);
      TLorentzVector J2(0.,0.,0.,0.);
      TLorentzVector JJ(0.,0.,0.,0.);
       
      J1.SetPtEtaPhiM(LHEPart_pt[i1], LHEPart_eta[i1], LHEPart_phi[i1], 0);
      J2.SetPtEtaPhiM(LHEPart_pt[i2], LHEPart_eta[i2], LHEPart_phi[i2], 0);

      JJ = J1 + J2;   
      mass = JJ.M();
	
      dphi = J1.Eta() > J2.Eta()? J1.Phi()-J2.Phi():J2.Phi()-J1.Phi();
      float pi = 3.141592;
      if(dphi>pi) dphi = dphi - 2*pi;
      if(dphi<-pi) dphi = dphi + 2*pi;
 
    }

    Out.push_back(nJets); 
    Out.push_back(dphi);
    Out.push_back(mass);
    Out.push_back(ll_mass);
    Out.push_back(ll_pt);
    Out.push_back(h_mass);
    Out.push_back(h_pt);
 
    return Out;
  }
};
