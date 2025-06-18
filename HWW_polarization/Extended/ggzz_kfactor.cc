#ifndef GGZZ_KFACTOR
#define GGZZ_KFACTOR

#include "TSystem.h"

#include <iostream>
#include <vector>
#include <utility>
#include <algorithm>
#include <iterator>

#include "TLorentzVector.h"
#include "TMath.h"

#include "TH2D.h"
#include "TGraph.h"
#include "TFile.h"
#include <map>

#include "ROOT/RVec.hxx"

using namespace ROOT;
using namespace ROOT::VecOps;

using namespace std;

class ggzz_K_producer{
public:

  ggzz_K_producer();

  TGraph* ggzz_kfactor;
  TGraph* ggzz_kfactor_PDFScaleDn;
  TGraph* ggzz_kfactor_PDFScaleUp;
  TGraph* ggzz_kfactor_QCDScaleDn;
  TGraph* ggzz_kfactor_QCDScaleUp;
  TGraph* ggzz_kfactor_AsDn;
  TGraph* ggzz_kfactor_AsUp;
  TGraph* ggzz_kfactor_PDFReplicaDn;
  TGraph* ggzz_kfactor_PDFReplicaUp;

  TGraph* ggzz_kfactor_NNLO;
  TGraph* ggzz_kfactor_NNLO_PDFScaleDn;
  TGraph* ggzz_kfactor_NNLO_PDFScaleUp;
  TGraph* ggzz_kfactor_NNLO_QCDScaleDn;
  TGraph* ggzz_kfactor_NNLO_QCDScaleUp;
  TGraph* ggzz_kfactor_NNLO_AsDn;
  TGraph* ggzz_kfactor_NNLO_AsUp;
  TGraph* ggzz_kfactor_NNLO_PDFReplicaDn;
  TGraph* ggzz_kfactor_NNLO_PDFReplicaUp;

  RVecF operator()(int nLHEPart, RVecF LHEPart_pt, RVecF LHEPart_eta, RVecF LHEPart_phi, RVecF LHEPart_mass, RVecI LHEPart_pdgId, RVecI LHEPart_status){

    unsigned nPart = nLHEPart;
    int pdgId, nlep{0}, nnu{0};
    ROOT::Math::PtEtaPhiMVector WW;
    float lep1_pt{0.}, lep1_eta{0.}, lep1_phi{0.}, lep1_mass{0.};
    float lep2_pt{0.}, lep2_eta{0.}, lep2_phi{0.}, lep2_mass{0.};
    float nu1_pt{0.}, nu1_eta{0.}, nu1_phi{0.}, nu1_mass{0.};
    float nu2_pt{0.}, nu2_eta{0.}, nu2_phi{0.}, nu2_mass{0.};
    float Higgs_mass{0.};

    for (unsigned iPart{0}; iPart != nPart; ++iPart){
      if (LHEPart_status[iPart] != 1){continue;} //loop over outgoing particles only
      pdgId = std::abs(LHEPart_pdgId[iPart]);
      if((pdgId == 11) || (pdgId == 13) || (pdgId == 15) || (pdgId == 12) || (pdgId == 14) || (pdgId == 16)){ //built mWW from leptons and neutrinos as done for defining the MWW bins in MG samples
        ROOT::Math::PtEtaPhiMVector temp{LHEPart_pt[iPart], LHEPart_eta[iPart], LHEPart_phi[iPart], LHEPart_mass[iPart]};
        WW = WW + temp;
      }else{
        continue;
      }
    }

    Higgs_mass = WW.M();
    
    RVecF results = {1.0, 1.0, 1.0};
    
    float kfactor = 1.0;
    float kfactor_up = 0.0;
    float kfactor_dw = 0.0;

    float kfactor_nnlo = 1.0;
    float kfactor_nnlo_up = 0.0;
    float kfactor_nnlo_dw = 0.0;    
    
    kfactor      = ggzz_kfactor->Eval(Higgs_mass);
    kfactor_nnlo = ggzz_kfactor_NNLO->Eval(Higgs_mass);
      
    kfactor_up += ((ggzz_kfactor_PDFScaleUp->Eval(Higgs_mass) - kfactor) / kfactor)*((ggzz_kfactor_PDFScaleUp->Eval(Higgs_mass) - kfactor) / kfactor);
    kfactor_up += ((ggzz_kfactor_QCDScaleUp->Eval(Higgs_mass) - kfactor) / kfactor)*((ggzz_kfactor_QCDScaleUp->Eval(Higgs_mass) - kfactor) / kfactor);
    kfactor_up += ((ggzz_kfactor_AsUp->Eval(Higgs_mass) - kfactor) / kfactor)*((ggzz_kfactor_AsUp->Eval(Higgs_mass) - kfactor) / kfactor);
    kfactor_up += ((ggzz_kfactor_PDFReplicaUp->Eval(Higgs_mass) - kfactor) / kfactor)*((ggzz_kfactor_PDFReplicaUp->Eval(Higgs_mass) - kfactor) / kfactor);
    
    kfactor_dw += ((kfactor - ggzz_kfactor_PDFScaleDn->Eval(Higgs_mass)) / kfactor)*((kfactor - ggzz_kfactor_PDFScaleDn->Eval(Higgs_mass)) / kfactor);
    kfactor_dw += ((kfactor - ggzz_kfactor_QCDScaleDn->Eval(Higgs_mass)) / kfactor)*((kfactor - ggzz_kfactor_QCDScaleDn->Eval(Higgs_mass)) / kfactor);
    kfactor_dw += ((kfactor - ggzz_kfactor_AsDn->Eval(Higgs_mass)) / kfactor)*((kfactor - ggzz_kfactor_AsDn->Eval(Higgs_mass)) / kfactor);
    kfactor_dw += ((kfactor - ggzz_kfactor_PDFReplicaDn->Eval(Higgs_mass)) / kfactor)*((kfactor - ggzz_kfactor_PDFReplicaDn->Eval(Higgs_mass)) / kfactor);
    
    kfactor_nnlo_up += ((ggzz_kfactor_NNLO_PDFScaleUp->Eval(Higgs_mass) - kfactor_nnlo) / kfactor_nnlo)*((ggzz_kfactor_NNLO_PDFScaleUp->Eval(Higgs_mass) - kfactor_nnlo) / kfactor_nnlo);
    kfactor_nnlo_up += ((ggzz_kfactor_NNLO_QCDScaleUp->Eval(Higgs_mass) - kfactor_nnlo) / kfactor_nnlo)*((ggzz_kfactor_NNLO_QCDScaleUp->Eval(Higgs_mass) - kfactor_nnlo) / kfactor_nnlo);
    kfactor_nnlo_up += ((ggzz_kfactor_NNLO_AsUp->Eval(Higgs_mass) - kfactor_nnlo) / kfactor_nnlo)*((ggzz_kfactor_NNLO_AsUp->Eval(Higgs_mass) - kfactor_nnlo) / kfactor_nnlo);
    kfactor_nnlo_up += ((ggzz_kfactor_NNLO_PDFReplicaUp->Eval(Higgs_mass) - kfactor_nnlo) / kfactor_nnlo)*((ggzz_kfactor_NNLO_PDFReplicaUp->Eval(Higgs_mass) - kfactor_nnlo) / kfactor_nnlo);
    
    kfactor_nnlo_dw += ((kfactor_nnlo - ggzz_kfactor_NNLO_PDFScaleDn->Eval(Higgs_mass)) / kfactor_nnlo)*((kfactor_nnlo - ggzz_kfactor_NNLO_PDFScaleDn->Eval(Higgs_mass)) / kfactor_nnlo);
    kfactor_nnlo_dw += ((kfactor_nnlo - ggzz_kfactor_NNLO_QCDScaleDn->Eval(Higgs_mass)) / kfactor_nnlo)*((kfactor_nnlo - ggzz_kfactor_NNLO_QCDScaleDn->Eval(Higgs_mass)) / kfactor_nnlo);
    kfactor_nnlo_dw += ((kfactor_nnlo - ggzz_kfactor_NNLO_AsDn->Eval(Higgs_mass)) / kfactor_nnlo)*((kfactor_nnlo - ggzz_kfactor_NNLO_AsDn->Eval(Higgs_mass)) / kfactor_nnlo);
    kfactor_nnlo_dw += ((kfactor_nnlo - ggzz_kfactor_NNLO_PDFReplicaDn->Eval(Higgs_mass)) / kfactor_nnlo)*((kfactor_nnlo - ggzz_kfactor_NNLO_PDFReplicaDn->Eval(Higgs_mass)) / kfactor_nnlo);          
    
    kfactor_up = kfactor*TMath::Sqrt(kfactor_up);
    kfactor_dw = kfactor*TMath::Sqrt(kfactor_dw);
    
    kfactor_nnlo_up = kfactor_nnlo*TMath::Sqrt(kfactor_nnlo_up);
    kfactor_nnlo_dw = kfactor_nnlo*TMath::Sqrt(kfactor_nnlo_dw);
    
    results[0] = kfactor_nnlo;        
    results[1] = results[0] + kfactor_nnlo_up;
    results[2] = results[0] - kfactor_nnlo_dw;
    
    // cout << results << endl;

    return results;
    
  }
};

// Read NLO/LO weights and fill histograms
ggzz_K_producer::ggzz_K_producer(){
  
  
  // input file
  // TString fileIn = "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/sendEOSJobs/HZZ_polarization/mkShapesRDF/Full2018v9/HOQCD_KFactors_gg_ZZ.root"; // NLO / LO
  //


  //// Version 2
  // Systs
  
  // kfactor_Nominal
  // kfactor_PDFScaleDn
  // kfactor_PDFScaleUp
  // kfactor_QCDScaleDn
  // kfactor_QCDScaleUp
  // kfactor_AsDn
  // kfactor_AsUp
  // kfactor_PDFReplicaDn
  // kfactor_PDFReplicaUp
  
  TString fileIn = "/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/Kfactor_Collected_ggHZZ_2l2l_NLO_NNPDF_NarrowWidth_13TeV.root";
  TString fileIn_NNLO = "/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/Kfactor_Collected_ggHZZ_2l2l_NNLO_NNPDF_NarrowWidth_13TeV.root";
  
  TFile* f_ggzz	= new TFile(fileIn);
  TFile* f_ggzz_NNLO = new TFile(fileIn_NNLO);
  
  ggzz_kfactor = (TGraph*)f_ggzz->Get("kfactor_Nominal");
  
  ggzz_kfactor_PDFScaleDn = (TGraph*)f_ggzz->Get("kfactor_PDFScaleDn");
  ggzz_kfactor_PDFScaleUp = (TGraph*)f_ggzz->Get("kfactor_PDFScaleUp");
  ggzz_kfactor_QCDScaleDn = (TGraph*)f_ggzz->Get("kfactor_QCDScaleDn");
  ggzz_kfactor_QCDScaleUp = (TGraph*)f_ggzz->Get("kfactor_QCDScaleUp");
  ggzz_kfactor_AsDn = (TGraph*)f_ggzz->Get("kfactor_AsDn");
  ggzz_kfactor_AsUp = (TGraph*)f_ggzz->Get("kfactor_AsUp");
  ggzz_kfactor_PDFReplicaDn = (TGraph*)f_ggzz->Get("kfactor_PDFReplicaDn");
  ggzz_kfactor_PDFReplicaUp = (TGraph*)f_ggzz->Get("kfactor_PDFReplicaUp");

  ggzz_kfactor_NNLO = (TGraph*)f_ggzz_NNLO->Get("kfactor_Nominal");

  ggzz_kfactor_NNLO_PDFScaleDn = (TGraph*)f_ggzz_NNLO->Get("kfactor_PDFScaleDn");
  ggzz_kfactor_NNLO_PDFScaleUp = (TGraph*)f_ggzz_NNLO->Get("kfactor_PDFScaleUp");
  ggzz_kfactor_NNLO_QCDScaleDn = (TGraph*)f_ggzz_NNLO->Get("kfactor_QCDScaleDn");
  ggzz_kfactor_NNLO_QCDScaleUp = (TGraph*)f_ggzz_NNLO->Get("kfactor_QCDScaleUp");
  ggzz_kfactor_NNLO_AsDn = (TGraph*)f_ggzz_NNLO->Get("kfactor_AsDn");
  ggzz_kfactor_NNLO_AsUp = (TGraph*)f_ggzz_NNLO->Get("kfactor_AsUp");
  ggzz_kfactor_NNLO_PDFReplicaDn = (TGraph*)f_ggzz_NNLO->Get("kfactor_PDFReplicaDn");
  ggzz_kfactor_NNLO_PDFReplicaUp = (TGraph*)f_ggzz_NNLO->Get("kfactor_PDFReplicaUp");
  

}
  

#endif
