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

#include "ROOT/RVec.hxx"
#include "TH2D.h"
#include "TFile.h"
#include "correction.h"

using namespace ROOT;
using namespace ROOT::VecOps;
using correction::CorrectionSet;

// --- BTag SF class for light jets ---
class btagSFlight {

  public:
    btagSFlight(TString eff_map, const std::string year);
    ~btagSFlight();

    TH2F* h_ljet_eff;
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
        correction::Correction::Ref cset_btag_light;
        correction::Correction::Ref cset_btag_wps;
        if (year == "2024")
        {
            cset_btag_light = cset->at(tagger + "_negtagDY");
            cset_btag_wps   = cset->at(tagger + "_wp_values");
        }
        else
        {
            cset_btag_light = cset->at(tagger + "_light");
            cset_btag_wps   = cset->at(tagger + "_wp_values");
        }
     
        float btag_sf = 1.;
        for (unsigned iJ{0}; iJ != nCleanJet; ++iJ) 
        {
            if (CleanJet_pt[iJ] <= 20. || std::abs(CleanJet_eta[iJ]) >= 2.5) continue;

            if (Jet_btag[CleanJet_jetIdx[iJ]] > cset_btag_wps->evaluate({WP})) 
            {
                if (Jet_hadronFlavour[CleanJet_jetIdx[iJ]] == 0) 
                    btag_sf *= cset_btag_light->evaluate({shift, WP, 0, std::abs(CleanJet_eta[iJ]), CleanJet_pt[iJ]});
            }
            else 
            {
                float btag_eff = getEff(CleanJet_pt[iJ], CleanJet_eta[iJ], Jet_hadronFlavour[CleanJet_jetIdx[iJ]]);
                if (btag_eff == 1.) continue;

                if (Jet_hadronFlavour[CleanJet_jetIdx[iJ]] == 0)
                    btag_sf *= (1-btag_eff*cset_btag_light->evaluate({shift, WP, 0, std::abs(CleanJet_eta[iJ]), CleanJet_pt[iJ]}))/(1-btag_eff);
            }
        }
        return btag_sf;
    }

  private:
    float getEff(float pt, float eta, int flavour);
};

btagSFlight::btagSFlight(TString eff_map, const std::string year) {
    
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
        h_ljet_eff = nullptr;
        return;
    }

    //h_ljet_eff = (TH2F*)reff->Get("ljet_eff")->Clone();
    //if (h_ljet_eff) h_ljet_eff->SetDirectory(0);
    //reff->Close();
    h_ljet_eff = dynamic_cast<TH2F*>(reff->Get("ljet_eff"));
    if (h_ljet_eff) {
      h_ljet_eff = (TH2F*)h_ljet_eff->Clone();
      h_ljet_eff->SetDirectory(0);
    }
}

float btagSFlight::getEff(float pt, float eta, int flavour) {
    if (flavour != 0 || !h_ljet_eff) return 1.;

    int xbin = h_ljet_eff->GetXaxis()->FindBin(pt);
    int ybin = h_ljet_eff->GetYaxis()->FindBin(eta);
    return h_ljet_eff->GetBinContent(xbin, ybin);
}

btagSFlight::~btagSFlight() {
    std::cout << "Cleaning up memory" << std::endl;
    if (h_ljet_eff) h_ljet_eff->Delete();
}

#endif
