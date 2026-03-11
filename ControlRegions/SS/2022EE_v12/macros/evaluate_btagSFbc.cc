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

#include "ROOT/RVec.hxx"
#include "TH2D.h"
#include "TFile.h"
#include "correction.h"

using namespace ROOT;
using namespace ROOT::VecOps;
using correction::CorrectionSet;

// --- BTag SF class ---
class btagSFbc {

  public:
    btagSFbc(TString eff_map, const std::string year);
    ~btagSFbc();

    TH2F* h_bjet_eff;
    TH2F* h_cjet_eff;
    
    std::unique_ptr<CorrectionSet> cset;
 
    float operator()(
        RVecF CleanJet_pt,
        RVecF CleanJet_eta,
        RVecI CleanJet_jetIdx,
        unsigned int nCleanJet,
        RVecI Jet_hadronFlavour,
        RVecF Jet_btag,
        const std::string WP,
        const std::string shift,
        const std::string tagger,
        const std::string year
      )
    {
        correction::Correction::Ref cset_btag_comb;
        correction::Correction::Ref cset_btag_wps;
        if (year == "2024")
        {
            cset_btag_comb = cset->at(tagger + "_kinfit");
            cset_btag_wps   = cset->at(tagger + "_wp_values");
        }
        else
        {
            cset_btag_comb = cset->at(tagger + "_comb");
            cset_btag_wps   = cset->at(tagger + "_wp_values");
        }
      
        float btag_sf = 1.;
        for (unsigned iJ{0}; iJ != nCleanJet; ++iJ) 
        {
          if (CleanJet_pt[iJ] <= 20. || std::abs(CleanJet_eta[iJ]) >= 2.5) continue;

          if (Jet_btag[CleanJet_jetIdx[iJ]] > cset_btag_wps->evaluate({WP})) 
          {
            if (Jet_hadronFlavour[CleanJet_jetIdx[iJ]] == 5)
              btag_sf *= cset_btag_comb->evaluate({shift, WP, 5, std::abs(CleanJet_eta[iJ]), CleanJet_pt[iJ]});
            else if (Jet_hadronFlavour[CleanJet_jetIdx[iJ]] == 4 && year != "2024")
              btag_sf *= cset_btag_comb->evaluate({shift, WP, 4, std::abs(CleanJet_eta[iJ]), CleanJet_pt[iJ]});
          }
          else
          {
            float btag_eff = getEff(CleanJet_pt[iJ], CleanJet_eta[iJ], Jet_hadronFlavour[CleanJet_jetIdx[iJ]]);
            if (btag_eff == 1.) continue;

            if (Jet_hadronFlavour[CleanJet_jetIdx[iJ]] == 5)
              btag_sf *= (1-btag_eff*cset_btag_comb->evaluate({shift, WP, 5, std::abs(CleanJet_eta[iJ]), CleanJet_pt[iJ]}))/(1-btag_eff);
            else if (Jet_hadronFlavour[CleanJet_jetIdx[iJ]] == 4 && year != "2024")
              btag_sf *= (1-btag_eff*cset_btag_comb->evaluate({shift, WP, 4, std::abs(CleanJet_eta[iJ]), CleanJet_pt[iJ]}))/(1-btag_eff);
          }
        }
        return btag_sf;
    }

  private:
    float getEff(float pt, float eta, int flavour);
  
};

btagSFbc::btagSFbc(TString eff_map, const std::string year) {

    // --- Patch graphics classes first ---
    //const char* graphicsClasses[] = { "TPaletteAxis", "TCanvas", "TFrame", "TAttBBox2D", "TBox" };
    //for (auto clsname : graphicsClasses) {
    //    if (TClass* cl = TClass::GetClass(clsname)) cl->IgnoreTObjectStreamer();
    //}

  std::string home = std::string(std::getenv("STARTPATH"));
  std::string to_replace = "start.sh";
  size_t start  = home.find(to_replace);
  size_t stop   = to_replace.length();
  home.replace(start, stop, "");
  
  if (year == "Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15")
    {
        cset = CorrectionSet::from_file("/cvmfs/cms-griddata.cern.ch/cat/metadata/BTV/" + year + "/latest/btagging_preliminary.json.gz");
    }
    else
    {
       cset = CorrectionSet::from_file("/cvmfs/cms-griddata.cern.ch/cat/metadata/BTV/" + year + "/latest/btagging.json.gz"); 
    }

  TFile *reff = TFile::Open(eff_map, "READ");
  if (!reff || reff->IsZombie()) {
      std::cerr << "Error opening file " << eff_map << std::endl;
      return;
  }

  //h_bjet_eff = (TH2F*)reff->Get("bjet_eff")->Clone();
  //h_cjet_eff = (TH2F*)reff->Get("cjet_eff")->Clone();
  h_bjet_eff = dynamic_cast<TH2F*>(reff->Get("bjet_eff"));
  if (h_bjet_eff) {
      h_bjet_eff = (TH2F*)h_bjet_eff->Clone();
      h_bjet_eff->SetDirectory(0);
  }
  h_cjet_eff = dynamic_cast<TH2F*>(reff->Get("cjet_eff"));
  if (h_cjet_eff) {
      h_cjet_eff = (TH2F*)h_cjet_eff->Clone();
      h_cjet_eff->SetDirectory(0);
  }
  reff->Close();
}

float btagSFbc::getEff(float pt, float eta, int flavour) {
  int xbin, ybin;
  float eff = 1.;
  if (flavour == 5) {
    xbin = h_bjet_eff->GetXaxis()->FindBin(pt);
    ybin = h_bjet_eff->GetYaxis()->FindBin(eta);
    eff  = h_bjet_eff->GetBinContent(xbin, ybin);
  }
  else if (flavour == 4) {
    if (!h_cjet_eff) return 1.0;
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

btagSFbc::~btagSFbc() {
  std::cout << "Cleaning up memory" << std::endl;
  if(h_bjet_eff) h_bjet_eff->Delete();
  if(h_cjet_eff) h_cjet_eff->Delete();
}

#endif
