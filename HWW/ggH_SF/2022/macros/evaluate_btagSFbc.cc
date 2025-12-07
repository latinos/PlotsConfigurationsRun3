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

// Following the recommendations https://btv-wiki.docs.cern.ch/PerformanceCalibration/fixedWPSFRecommendations/

class btagSFbc {

  public:
    btagSFbc(TString eff_map, const string year);
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
        const string shift,
        const string tagger
      )
      {
      
        auto cset_btag_mujets  = cset->at(tagger + "_mujets");
        auto cset_btag_wps     = cset->at(tagger + "_wp_values");
      
        float btag_sf    = 1.;
        for (unsigned iJ{0}; iJ != nCleanJet; ++iJ) 
        {
          if (CleanJet_pt[iJ] <= 20. || abs(CleanJet_eta[iJ]) >= 2.5) continue;
          // The jet is tagged
          if (Jet_btag[CleanJet_jetIdx[iJ]] > cset_btag_wps->evaluate({WP})) 
          {
            // c-jets are treated together with b jets
            if (Jet_hadronFlavour[CleanJet_jetIdx[iJ]] == 5)
            {
              btag_sf *= cset_btag_mujets->evaluate({shift, WP, 5, abs(CleanJet_eta[iJ]), CleanJet_pt[iJ]});
            }
            else if (Jet_hadronFlavour[CleanJet_jetIdx[iJ]] == 4)
            {
              btag_sf *= cset_btag_mujets->evaluate({shift, WP, 4, abs(CleanJet_eta[iJ]), CleanJet_pt[iJ]});
            }
            else 
            {
              continue;
            }
          }
          // The jet is not tagged
          else
          {
            float btag_eff = getEff(CleanJet_pt[iJ], CleanJet_eta[iJ], Jet_hadronFlavour[CleanJet_jetIdx[iJ]]);
            if (btag_eff == 1.) 
            {
              continue;
            }
            else 
            {
              if (Jet_hadronFlavour[CleanJet_jetIdx[iJ]] == 5) 
              {
                btag_sf *= (1-btag_eff*cset_btag_mujets->evaluate({shift, WP, 5, abs(CleanJet_eta[iJ]), CleanJet_pt[iJ]}))/(1-btag_eff);
              }
              else if (Jet_hadronFlavour[CleanJet_jetIdx[iJ]] == 4) 
              {
                btag_sf *= (1-btag_eff*cset_btag_mujets->evaluate({shift, WP, 4, abs(CleanJet_eta[iJ]), CleanJet_pt[iJ]}))/(1-btag_eff);
              }
              else 
              {
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

btagSFbc::btagSFbc(TString eff_map, const string year) {
  std::string home;
  home          = std::string(std::getenv("STARTPATH"));
  std::string to_replace  = "start.sh";
  size_t start  = home.find(to_replace);
  size_t stop   = to_replace.length();
  home.replace(start, stop, "");
  
  cset = CorrectionSet::from_file(home + "/mkShapesRDF/processor/data/jsonpog-integration/POG/BTV/" + year + "/btagging.json.gz");
 
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
  if (flavour == 5) 
  {
    xbin = h_bjet_eff->GetXaxis()->FindBin(pt);
    ybin = h_bjet_eff->GetYaxis()->FindBin(eta);
    eff  = h_bjet_eff->GetBinContent(xbin, ybin);
  }
  else if (flavour == 4) 
  {
    xbin = h_cjet_eff->GetXaxis()->FindBin(pt);
    ybin = h_cjet_eff->GetYaxis()->FindBin(eta);
    eff  = h_cjet_eff->GetBinContent(xbin, ybin);
  }
  else 
  {
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