#ifndef BTAGSF
#define BTAGSF
#include <vector>
#include <map>
#include <string>
#include <iostream>
#include "TVector2.h"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"
#include "TString.h"

#include <iostream>
#include "ROOT/RVec.hxx"
#include "TH2D.h"
#include "TFile.h"
#include "correction.h"

using namespace ROOT;
using namespace ROOT::VecOps;
using correction::CorrectionSet;

class btagSFbc {

  public:
    btagSFbc(TString eff_map);
    ~btagSFbc();

    TH2F* h_bjet_eff;
    TH2F* h_cjet_eff;
    
    std::unique_ptr<CorrectionSet> cset;
 
    float operator()(
		    RVecF         CleanJet_pt,
		    RVecF         CleanJet_eta,
		    RVecI         CleanJet_jetIdx,
		    unsigned int  nCleanJet,
        RVecI         Jet_hadronFlavour,
		    RVecF         Jet_btag,
        const string  WP,
        const string systematic
        ){
      
      auto cset_deepJet_mujets  = cset->at("deepJet_mujets");
      auto cset_deepJet_wps     = cset->at("deepJet_wp_values");
     
      float btag_sf    = 1.;
      for (unsigned iJ{0}; iJ != nCleanJet; ++iJ) {
        if (CleanJet_pt[iJ] <= 30. || abs(CleanJet_eta[iJ]) >= 2.5) continue;
          if (Jet_btag[CleanJet_jetIdx[iJ]] > cset_deepJet_wps->evaluate({WP})) {
            if (Jet_hadronFlavour[CleanJet_jetIdx[iJ]] == 5) {
              btag_sf *= cset_deepJet_mujets->evaluate({systematic, WP, 5, abs(CleanJet_eta[iJ]), CleanJet_pt[iJ]});
            }
            else if (Jet_hadronFlavour[CleanJet_jetIdx[iJ]] == 4) {
              btag_sf *= cset_deepJet_mujets->evaluate({systematic, WP, 4, abs(CleanJet_eta[iJ]), CleanJet_pt[iJ]});
            }
            else {
              continue;
            }
      }
      else {
        float btag_eff = getEff(CleanJet_pt[iJ], CleanJet_eta[iJ], Jet_hadronFlavour[CleanJet_jetIdx[iJ]]);
        if (btag_eff == 1.) {
          continue;
        }
        else {
          if (Jet_hadronFlavour[CleanJet_jetIdx[iJ]] == 5) {
            btag_sf *= (1-btag_eff*cset_deepJet_mujets->evaluate({systematic, WP, 5, abs(CleanJet_eta[iJ]), CleanJet_pt[iJ]}))/(1-btag_eff);
          }
          else if (Jet_hadronFlavour[CleanJet_jetIdx[iJ]] == 4) {
            btag_sf *= (1-btag_eff*cset_deepJet_mujets->evaluate({systematic, WP, 4, abs(CleanJet_eta[iJ]), CleanJet_pt[iJ]}))/(1-btag_eff);
          }
          else {
            continue;
          }
        }
      }
    }
    return btag_sf;
  }

  private:
    float getEff(float pt, float eta, int flavour);
  
};

btagSFbc::btagSFbc(TString eff_map) {
  cset = CorrectionSet::from_file("/afs/cern.ch/work/b/bcamaian/mkShapesRDF_el7/mkShapesRDF/processor/data/jsonpog-integration/POG/BTV/2016preVFP_UL/btagging.json.gz");
 
  TFile *reff = TFile::Open(eff_map, "READ");
  h_bjet_eff  = (TH2F*)reff->Get("bjet_eff")->Clone();
  h_cjet_eff  = (TH2F*)reff->Get("cjet_eff")->Clone();
  h_bjet_eff->SetDirectory(0);
  h_cjet_eff->SetDirectory(0);
  reff->Close();
}

float btagSFbc::getEff(float pt, float eta, int flavour) {
  int xbin, ybin;
  float eff;
  if (flavour == 5) {
    xbin = h_bjet_eff->GetXaxis()->FindBin(pt);
    ybin = h_bjet_eff->GetYaxis()->FindBin(eta);
    eff  = h_bjet_eff->GetBinContent(xbin, ybin);
  }
  else if (flavour == 4) {
    xbin = h_cjet_eff->GetXaxis()->FindBin(pt);
    ybin = h_cjet_eff->GetYaxis()->FindBin(eta);
    eff  = h_cjet_eff->GetBinContent(xbin, ybin);
  }
  else {
    eff   = 1.;
  }
  return eff;
}

btagSFbc::~btagSFbc(){
  std::cout << "Cleaning up memory" << std::endl;
  h_bjet_eff->Delete();
  h_cjet_eff->Delete();
}
 
#endif
