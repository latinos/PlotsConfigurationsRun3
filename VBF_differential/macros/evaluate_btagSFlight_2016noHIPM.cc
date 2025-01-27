#ifndef BTAGLIGHTSF
#define BTAGLIGHTSF
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

class btagSFlight {

  public:
    btagSFlight(TString eff_map);
    ~btagSFlight();

    TH2F* h_ljet_eff;
    
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
      
      auto cset_deepJet_incl    = cset->at("deepJet_incl");
      auto cset_deepJet_wps     = cset->at("deepJet_wp_values");
     
      float btag_sf    = 1.;
      for (unsigned iJ{0}; iJ != nCleanJet; ++iJ) {
        if (CleanJet_pt[iJ] <= 30. || abs(CleanJet_eta[iJ]) >= 2.5) continue;
          if (Jet_btag[CleanJet_jetIdx[iJ]] > cset_deepJet_wps->evaluate({WP})) {
            if (Jet_hadronFlavour[CleanJet_jetIdx[iJ]] == 0) {
              btag_sf *= cset_deepJet_incl->evaluate({systematic, WP, 0, abs(CleanJet_eta[iJ]), CleanJet_pt[iJ]});
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
          if (Jet_hadronFlavour[CleanJet_jetIdx[iJ]] == 0) {
            btag_sf *= (1-btag_eff*cset_deepJet_incl->evaluate({systematic, WP, 0, abs(CleanJet_eta[iJ]), CleanJet_pt[iJ]}))/(1-btag_eff);
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

btagSFlight::btagSFlight(TString eff_map) {
  cset = CorrectionSet::from_file("/afs/cern.ch/work/b/bcamaian/mkShapesRDF_el7/mkShapesRDF/processor/data/jsonpog-integration/POG/BTV/2016postVFP_UL/btagging.json.gz");
 
  TFile *reff = TFile::Open(eff_map, "READ");
  h_ljet_eff  = (TH2F*)reff->Get("ljet_eff")->Clone();
  h_ljet_eff->SetDirectory(0);
  reff->Close();
}

float btagSFlight::getEff(float pt, float eta, int flavour) {
  int xbin, ybin;
  float eff;
  if (flavour == 0) {
    xbin = h_ljet_eff->GetXaxis()->FindBin(pt);
    ybin = h_ljet_eff->GetYaxis()->FindBin(eta);
    eff  = h_ljet_eff->GetBinContent(xbin, ybin);
  }
  else {
   eff   = 1.;
  }
  return eff;
}

btagSFlight::~btagSFlight(){
  std::cout << "Cleaning up memory" << std::endl;
  h_ljet_eff->Delete();
}
 
#endif
