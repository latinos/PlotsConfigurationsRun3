
#ifndef jet_veto_2016
#define jet_veto_2016

#include <vector>
#include "TLorentzVector.h"
#include "correction.h"
#include "ROOT/RVec.hxx"

using namespace ROOT;
using namespace ROOT::VecOps;


int Jet_Veto(
	      RVecF CleanJet_pt,
	      RVecF CleanJet_eta,
	      RVecF CleanJet_phi,
	      RVecF Jet_neEmEF,
	      RVecF Jet_chEmEF,
	      RVecI CleanJet_jetIdx){
  
  float tmp_value;  
  float cleanJet_EM;

  float eta,phi;
  
  string path_file = "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/Full2016_HIPM/jetvetomaps.json";
  auto csetJet_File = correction::CorrectionSet::from_file(path_file);
  correction::Correction::Ref cset_jet_Map = (correction::Correction::Ref) csetJet_File->at("Summer19UL16_V1"); 

  //cout << "Compute veto" << endl;
  
  for (int i=0; i<CleanJet_pt.size(); i++){
    phi = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{CleanJet_phi[i], 3.1415}), -3.1415});
    eta = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{CleanJet_eta[i], 5.19}), -5.19});
    
    cleanJet_EM = Jet_neEmEF[CleanJet_jetIdx[i]] + Jet_chEmEF[CleanJet_jetIdx[i]];    
    tmp_value = cset_jet_Map->evaluate({"jetvetomap", eta, phi});

    //cout << tmp_value << endl;

    if (cleanJet_EM<0.9 && CleanJet_pt[i]>15.0 && tmp_value!=0.0){
      //cout << "Rejected!!!" << endl;
      return 0;
    }
  }

  return 1;
}

#endif
