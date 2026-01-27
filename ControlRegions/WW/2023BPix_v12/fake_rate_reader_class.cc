/*
  To have the complete formulas:
  https://github.com/latinos/LatinoAnalysis/blob/master/NanoGardener/python/modules/LeptonFakeWMaker.py
  https://github.com/latinos/LatinoAnalysis/blob/UL_production/NanoGardener/python/data/formulasToAdd_FAKE_Full2018v9.py
*/


#ifndef FAKERATEREADER
#define FAKERATEREADER

#include "TSystem.h"

#include <iostream>
#include <vector>
#include <utility>
#include <algorithm>
#include <iterator>

#include "TLorentzVector.h"
#include "TMath.h"

#include "TH2D.h"
#include "TFile.h"
#include <map>

#include "ROOT/RVec.hxx"

using namespace ROOT;
using namespace ROOT::VecOps;

using namespace std;

typedef std::map<std::string,std::map<std::string,std::string>> map_dict;

class fake_rate_reader {
public:
  fake_rate_reader(
    TString year,
    TString ele_WP,
    TString muon_WP,
    float ele_WP_number,
    float muon_WP_number,
    TString kind,
    uint nLeptons,
    TString electron_tight_charge,
    TString mkShapesRDF_base,
    TString fakerate_version
  );

  std::tuple<double, double> GetRate(TH2F* fake_rate_histo, double pt, double eta, double lepton_pt_max);
  float GetFR_2l(
    double pt1, double eta1, double pdg1, double isTight1,
    double pt2, double eta2, double pdg2, double isTight2,
    TH2F* fake_rate_ele_, TH2F* fake_rate_muon_, TString stat
  );
  float GetFR_3l(
    double pt1, double eta1, double pdg1, double isTight1,
    double pt2, double eta2, double pdg2, double isTight2,
    double pt3, double eta3, double pdg3, double isTight3,
    TH2F* fake_rate_ele_, TH2F* fake_rate_muon_, TString stat
  );

  TString      year_;
  unsigned int nLeptons_;
  TString      electron_tight_charge_;
  std::string  SF_type_;
  TString      ele_WP_;
  TString      muon_WP_;
  float        ele_WP_number_;
  float        muon_WP_number_;
  TString      kind_;

  RVecI Lepton_pdgId;
  RVecF Lepton_pt;
  RVecF Lepton_eta;
  RVecI Lepton_isTightMuon_cut_Tight_HWWW; // 2016 -> Lepton_isTightMuon_cut_Tight80x
  RVecI Lepton_isTightElectron_mvaFall17V2Iso_WP90;
  RVecF Lepton_mvaTTH_UL;
  RVecF Muon_mvaTTH;
  RVecI Lepton_muonIdx;
  RVecF CleanJet_pt;
  int   nCleanJet;

  map_dict fake_rate_reader_map_;

  TH2F* fake_rate_muon_10_;
  TH2F* fake_rate_muon_15_;
  TH2F* fake_rate_muon_20_;
  TH2F* fake_rate_muon_25_;
  TH2F* fake_rate_muon_30_;
  TH2F* fake_rate_muon_35_;
  TH2F* fake_rate_muon_45_;
  TH2F* fake_rate_ele_25_;
  TH2F* fake_rate_ele_35_;
  TH2F* fake_rate_ele_45_;
  TH2F* prompt_rate_muon_;
  TH2F* prompt_rate_ele_;
  TH2F* fake_rate_muon_25_EWK5Up_;
  TH2F* fake_rate_muon_25_EWK5Down_;
  TH2F* fake_rate_ele_35_EWK5Up_;
  TH2F* fake_rate_ele_35_EWK5Down_;

  int   isTight_[3];

  float operator()(
    RVecI Lepton_pdgId,
    RVecF Lepton_pt,
    RVecF Lepton_eta,
    RVecI Lepton_isTightMuon_cut_Tight_HWWW,
    RVecI Lepton_isTightElectron_mvaFall17V2Iso_WP90,
    RVecF Lepton_mvaTTH_UL,
    RVecF Muon_mvaTTH,
    RVecI Lepton_muonIdx,
    RVecF CleanJet_pt,
    int   nCleanJet
  ) {
    double SF = 1.;

    isTight_[0] = 0;
    isTight_[1] = 0;
    isTight_[2] = 0;

    // Build tight lepton definitions
    for (unsigned int i = 0; i < nLeptons_; i++) {
      if (TMath::Abs(Lepton_pdgId[i]) == 11)
        if (Lepton_isTightElectron_mvaFall17V2Iso_WP90[i] == 1 && Lepton_mvaTTH_UL[i] > ele_WP_number_)
          isTight_[i] = 1;
      if (TMath::Abs(Lepton_pdgId[i]) == 13)
        if (Lepton_isTightMuon_cut_Tight_HWWW[i] == 1 && Muon_mvaTTH[Lepton_muonIdx[i]] > muon_WP_number_)
          isTight_[i] = 1;
    }

    // Case 2 leptons.  Here the fakewight is computed only for 1-jet bin and applied to all the jet bins.
    if (nLeptons_ == 2) {
      float fakeWeight_2l1j = GetFR_2l(
        Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
        Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
        fake_rate_ele_35_, fake_rate_muon_25_, "Nominal"
      );

      if (kind_ == "nominal") {
        return fakeWeight_2l1j;
      }

      // Calculate the per-event fake rate - EleUp
      if (kind_ == "EleUp") {
    
        float fakeWeight_2l1jElUp = GetFR_2l(
          Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
          Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
          fake_rate_ele_45_, fake_rate_muon_25_, "Nominal"
        );

        float fakeWeightEleUp = 0.;
        if (fakeWeight_2l1j != 0.){
          fakeWeightEleUp = fakeWeight_2l1jElUp / fakeWeight_2l1j;
        }
        return fakeWeightEleUp;
      }

      // Calculate the per-event fake rate - EleDown
      if (kind_ == "EleDown") {

        float fakeWeight_2l1jElDown = GetFR_2l(
          Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
          Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
          fake_rate_ele_25_, fake_rate_muon_25_, "Nominal"
        );

        float fakeWeightEleDown = 0.;
        if (fakeWeight_2l1j != 0.) {
          fakeWeightEleDown = fakeWeight_2l1jElDown / fakeWeight_2l1j;
        }
        return fakeWeightEleDown;
      }

      // Calculate the per-event fake rate - MuUp
      if (kind_ == "MuUp") {

        float fakeWeight_2l1jMuUp = GetFR_2l(
          Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
          Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
          fake_rate_ele_35_, fake_rate_muon_35_, "Nominal"
        );

        float fakeWeightMuUp = 0.;
        if (fakeWeight_2l1j != 0. ){
          fakeWeightMuUp = fakeWeight_2l1jMuUp / fakeWeight_2l1j;
        }
        return fakeWeightMuUp;
      }

      // Calculate the per-event fake rate - MuDown
      if (kind_ == "MuDown") {

        float fakeWeight_2l1jMuDown = GetFR_2l(
          Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
          Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
          fake_rate_ele_35_, fake_rate_muon_15_, "Nominal"
        );

        float fakeWeightMuDown = 0.;
        if (fakeWeight_2l1j != 0. ){
          fakeWeightMuDown = fakeWeight_2l1jMuDown / fakeWeight_2l1j;
        }
        return fakeWeightMuDown;
      }

      // Calculate the per-event fake rate - StatEleUp
      if (kind_ == "StatEleUp") {
    

        float fakeWeight_2l1jstatElUp = GetFR_2l(
          Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
          Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
          fake_rate_ele_35_, fake_rate_muon_25_, "ElUp"
        );

    

        float fakeWeightstatEleUp = 0.;
        if (fakeWeight_2l1j != 0. ){
          fakeWeightstatEleUp = fakeWeight_2l1jstatElUp / fakeWeight_2l1j;
        }
        return fakeWeightstatEleUp;
      }

      // Calculate the per-event fake rate - StatEleDown
      if (kind_ == "StatEleDown") {


        float fakeWeight_2l1jstatElDown = GetFR_2l(
          Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
          Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
          fake_rate_ele_35_, fake_rate_muon_25_, "ElDown"
        );


        float fakeWeightstatEleDown = 0.;
        if (fakeWeight_2l1j != 0. ){
          fakeWeightstatEleDown = fakeWeight_2l1jstatElDown / fakeWeight_2l1j;
        }
        return fakeWeightstatEleDown;
      }

      // Calculate the per-event fake rate - StatMuUp
      if (kind_ == "StatMuUp") {
    

        float fakeWeight_2l1jstatMuUp = GetFR_2l(
          Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
          Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
          fake_rate_ele_35_, fake_rate_muon_25_, "MuUp"
        );


        float fakeWeightstatMuUp = 0.;
        if (fakeWeight_2l1j != 0.) {
          fakeWeightstatMuUp = fakeWeight_2l1jstatMuUp / fakeWeight_2l1j;
        }
        return fakeWeightstatMuUp;
      }

      // Calculate the per-event fake rate - StatMuDown
      if (kind_ == "StatMuDown") {
        
        float fakeWeight_2l1jstatMuDown = GetFR_2l(
          Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
          Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
          fake_rate_ele_35_, fake_rate_muon_25_, "MuDown"
        );


        float fakeWeightstatMuDown = 0.;
        if (fakeWeight_2l1j != 0.) {
          fakeWeightstatMuDown = fakeWeight_2l1jstatMuDown / fakeWeight_2l1j;
        }
        return fakeWeightstatMuDown;
      }
      if (kind_ == "EWK5Up") {
        float w_up = GetFR_2l(
          Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
          Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
          fake_rate_ele_35_EWK5Up_,  
          fake_rate_muon_25_EWK5Up_, 
          "Nominal"
        );
        return (fakeWeight_2l1j != 0.f) ? (w_up / fakeWeight_2l1j) : 0.f;
      }

      if (kind_ == "EWK5Down") {
        float w_dn = GetFR_2l(
          Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
          Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
          fake_rate_ele_35_EWK5Down_,
          fake_rate_muon_25_EWK5Down_,
          "Nominal"
        );
        return (fakeWeight_2l1j != 0.f) ? (w_dn / fakeWeight_2l1j) : 0.f;
      }

      else
        return -1;
    }

    else if (nLeptons_ == 3) {
      // Calculate the per-event fake rate
      float fakeWeight_3l = GetFR_3l(
        Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
        Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
        Lepton_pt[2], Lepton_eta[2], Lepton_pdgId[2], isTight_[2],
        fake_rate_ele_35_, fake_rate_muon_35_, "Nominal"
      );

      if (kind_ == "nominal") return fakeWeight_3l;

      // Calculate the per-event fake rate - EleUp
      if (kind_ == "EleUp") {
        float fakeWeight_3lElUp = GetFR_3l(
          Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
          Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
          Lepton_pt[2], Lepton_eta[2], Lepton_pdgId[2], isTight_[2],
          fake_rate_ele_45_, fake_rate_muon_35_, "Nominal"
        );
        float fakeWeightEleUp = fakeWeight_3lElUp / fakeWeight_3l;
        return fakeWeightEleUp;
      }

      // Calculate the per-event fake rate - EleDown
      if (kind_ == "EleDown") {
        float fakeWeight_3lElDown = GetFR_3l(
          Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
          Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
          Lepton_pt[2], Lepton_eta[2], Lepton_pdgId[2], isTight_[2],
          fake_rate_ele_25_, fake_rate_muon_35_, "Nominal"
        );
        float fakeWeightEleDown = fakeWeight_3lElDown / fakeWeight_3l;
        return fakeWeightEleDown;
      }

      // Calculate the per-event fake rate - MuUp
      if (kind_ == "MuUp") {
        float fakeWeight_3lMuUp = GetFR_3l(
          Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
          Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
          Lepton_pt[2], Lepton_eta[2], Lepton_pdgId[2], isTight_[2],
          fake_rate_ele_35_, fake_rate_muon_45_, "Nominal"
        );
        float fakeWeightMuUp = fakeWeight_3lMuUp / fakeWeight_3l;
        return fakeWeightMuUp;
      }

      // Calculate the per-event fake rate - MuDown
      if (kind_ == "MuDown") {
        float fakeWeight_3lMuDown = GetFR_3l(
          Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
          Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
          Lepton_pt[2], Lepton_eta[2], Lepton_pdgId[2], isTight_[2],
          fake_rate_ele_35_, fake_rate_muon_25_, "Nominal"
        );
        float fakeWeightMuDown = fakeWeight_3lMuDown / fakeWeight_3l;
        return fakeWeightMuDown;
      }

      // Calculate the per-event fake rate - StatEleUp
      if (kind_ == "StatEleUp") {
        float fakeWeight_3lstatEleUp = GetFR_3l(
          Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
          Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
          Lepton_pt[2], Lepton_eta[2], Lepton_pdgId[2], isTight_[2],
          fake_rate_ele_35_, fake_rate_muon_35_, "ElUp"
        );
        float fakeWeightstatEleUp = fakeWeight_3lstatEleUp / fakeWeight_3l;
        return fakeWeightstatEleUp;
      }

      // Calculate the per-event fake rate - StatEleDown
      if (kind_ == "StatEleDown") {
        float fakeWeight_3lstatEleDown = GetFR_3l(
          Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
          Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
          Lepton_pt[2], Lepton_eta[2], Lepton_pdgId[2], isTight_[2],
          fake_rate_ele_35_, fake_rate_muon_35_, "ElDown"
        );
        float fakeWeightstatEleDown = fakeWeight_3lstatEleDown / fakeWeight_3l;
        return fakeWeightstatEleDown;
      }

      // Calculate the per-event fake rate - StatMuUp
      if (kind_ == "StatMuUp") {
        float fakeWeight_3lstatMuUp = GetFR_3l(
          Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
          Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
          Lepton_pt[2], Lepton_eta[2], Lepton_pdgId[2], isTight_[2],
          fake_rate_ele_35_, fake_rate_muon_35_, "MuUp"
        );
        float fakeWeightstatMuUp = fakeWeight_3lstatMuUp / fakeWeight_3l;
        return fakeWeightstatMuUp;
      }

      // Calculate the per-event fake rate - StatMuDown
      if (kind_ == "StatMuDown") {
        float fakeWeight_3lstatMuDown = GetFR_3l(
          Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
          Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
          Lepton_pt[2], Lepton_eta[2], Lepton_pdgId[2], isTight_[2],
          fake_rate_ele_35_, fake_rate_muon_35_, "MuDown"
        );
        float fakeWeightstatMuDown = fakeWeight_3lstatMuDown / fakeWeight_3l;
        return fakeWeightstatMuDown;
      }

      else {
        std::cout << "kind_ not known" << std::endl;
        return -1;
      }
    }

    else {
      std::cout << "nLeptons != [2,3] not implemented" << std::endl;
      return -1;
    }
  }

private:
  void loadSF2D(std::string filename);
  std::tuple<double, double> GetSF(double pt_in, double eta_in);
};


// Read fake and prompt rate histograms
fake_rate_reader::fake_rate_reader( TString year , TString ele_WP, TString muon_WP, float ele_WP_number, float muon_WP_number, TString kind, uint nLeptons, TString electron_tight_charge, TString mkShapesRDF_base, TString fakerate_version){

  cout << "Year:             " << year                  << endl;
  cout << "Ele WP:           " << ele_WP                << endl;
  cout << "Muon WP:          " << muon_WP               << endl;
  cout << "Ele WP number:    " << ele_WP_number         << endl;
  cout << "Muon WP number:   " << muon_WP_number        << endl;
  cout << "Kind:             " << kind                  << endl;
  cout << "nLeptons:         " << nLeptons              << endl;
  cout << "Ele tight charge: " << electron_tight_charge << endl;

  year_                  = year;
  ele_WP_                = ele_WP;
  muon_WP_               = muon_WP;
  ele_WP_number_         = ele_WP_number;
  muon_WP_number_        = muon_WP_number;
  kind_                  = kind;
  nLeptons_              = nLeptons;
  electron_tight_charge_ = electron_tight_charge; // ['std','ss']

  TString ele_tight_suffix = "";
  if (electron_tight_charge_ == "ss")
    ele_tight_suffix = "_SS";

  // std::string mkShapesRDF_base = std::getenv("CMSSW_BASE");
  // TString mkShapesRDF_base = "/afs/cern.ch/work/b/bcamaian/mkShapesRDF_el7";
  // mkShapesRDF_base = "/afs/cern.ch/user/n/ntrevisa/work/latinos/Run3/PlotsConfigurationsRun3/WH_chargeAsymmetry/UL/";
  
  // Fake rate input files
  TString fake_muon_file_name_10 = "/eos/user/s/squinto/FakeRate/2023BPix_v12/FakeRate_2023BPix_v12/cut_TightID_pfIsoTight_HWW_tthmva_67/MuonFR_jet10.root";
  TString fake_muon_file_name_15 = "/eos/user/s/squinto/FakeRate/2023BPix_v12/FakeRate_2023BPix_v12/cut_TightID_pfIsoTight_HWW_tthmva_67/MuonFR_jet15.root";
  TString fake_muon_file_name_20 = "/eos/user/s/squinto/FakeRate/2023BPix_v12/FakeRate_2023BPix_v12/cut_TightID_pfIsoTight_HWW_tthmva_67/MuonFR_jet20.root";
  TString fake_muon_file_name_25 = "/eos/user/s/squinto/FakeRate/2023BPix_v12/FakeRate_2023BPix_v12/cut_TightID_pfIsoTight_HWW_tthmva_67/MuonFR_jet25.root";
  TString fake_muon_file_name_30 = "/eos/user/s/squinto/FakeRate/2023BPix_v12/FakeRate_2023BPix_v12/cut_TightID_pfIsoTight_HWW_tthmva_67/MuonFR_jet30.root";
  TString fake_muon_file_name_35 = "/eos/user/s/squinto/FakeRate/2023BPix_v12/FakeRate_2023BPix_v12/cut_TightID_pfIsoTight_HWW_tthmva_67/MuonFR_jet35.root";
  TString fake_muon_file_name_45 = "/eos/user/s/squinto/FakeRate/2023BPix_v12/FakeRate_2023BPix_v12/cut_TightID_pfIsoTight_HWW_tthmva_67/MuonFR_jet45.root";

  if (year_ == "2016_HIPM" || year_ == "2016_noHIPM"){
    fake_muon_file_name_10 = mkShapesRDF_base + "/data/" + fakerate_version + "/" + year + "/cut_Tight80x_tthmva_" + muon_WP + "/MuonFR_jet10.root";
    fake_muon_file_name_15 = mkShapesRDF_base + "/data/" + fakerate_version + "/" + year + "/cut_Tight80x_tthmva_" + muon_WP + "/MuonFR_jet15.root";
    fake_muon_file_name_20 = mkShapesRDF_base + "/data/" + fakerate_version + "/" + year + "/cut_Tight80x_tthmva_" + muon_WP + "/MuonFR_jet20.root";
    fake_muon_file_name_25 = mkShapesRDF_base + "/data/" + fakerate_version + "/" + year + "/cut_Tight80x_tthmva_" + muon_WP + "/MuonFR_jet25.root";
    fake_muon_file_name_30 = mkShapesRDF_base + "/data/" + fakerate_version + "/" + year + "/cut_Tight80x_tthmva_" + muon_WP + "/MuonFR_jet30.root";
    fake_muon_file_name_35 = mkShapesRDF_base + "/data/" + fakerate_version + "/" + year + "/cut_Tight80x_tthmva_" + muon_WP + "/MuonFR_jet35.root";
    fake_muon_file_name_45 = mkShapesRDF_base + "/data/" + fakerate_version + "/" + year + "/cut_Tight80x_tthmva_" + muon_WP + "/MuonFR_jet45.root";
  }

  TString fake_ele_file_name_25  = "/eos/user/s/squinto/FakeRate/2023BPix_v12/FakeRate_2023BPix_v12/cutBased_LooseID_tthMVA_Run3/EleFR_jet25.root";
  TString fake_ele_file_name_35  = "/eos/user/s/squinto/FakeRate/2023BPix_v12/FakeRate_2023BPix_v12/cutBased_LooseID_tthMVA_Run3/EleFR_jet35.root";
  TString fake_ele_file_name_45  = "/eos/user/s/squinto/FakeRate/2023BPix_v12/FakeRate_2023BPix_v12/cutBased_LooseID_tthMVA_Run3/EleFR_jet45.root";

  // Prompt rate input files
  TString pr_muon_file_name = "/eos/user/s/squinto/FakeRate/2023BPix_v12/FakeRate_2023BPix_v12/cut_TightID_pfIsoTight_HWW_tthmva_67/MuonPR.root";
  if (year_ == "2016_HIPM" || year_ == "2016_noHIPM")
    pr_muon_file_name = mkShapesRDF_base + "/data/" + fakerate_version + "/" + year + "/cut_Tight80x_tthmva_" + muon_WP + "/MuonPR.root";
  TString pr_ele_file_name =  "/eos/user/s/squinto/FakeRate/2023BPix_v12/FakeRate_2023BPix_v12/cutBased_LooseID_tthMVA_Run3/ElePR.root";
  
  // Get fake and prompt rates  
  // Muons
  TFile* f_muon_10   = new TFile(fake_muon_file_name_10);
  fake_rate_muon_10_ = (TH2F*) f_muon_10 -> Get("FR_pT_eta_EWKcorr");

  TFile* f_muon_15   = new TFile(fake_muon_file_name_15);
  fake_rate_muon_15_ = (TH2F*) f_muon_15 -> Get("FR_pT_eta_EWKcorr");

  TFile* f_muon_20   = new TFile(fake_muon_file_name_20);
  fake_rate_muon_20_ = (TH2F*) f_muon_20 -> Get("FR_pT_eta_EWKcorr");

  TFile* f_muon_25   = new TFile(fake_muon_file_name_25);
  fake_rate_muon_25_ = (TH2F*) f_muon_25 -> Get("FR_pT_eta_EWKcorr");

  TFile* f_muon_30   = new TFile(fake_muon_file_name_30);
  fake_rate_muon_30_ = (TH2F*) f_muon_30 -> Get("FR_pT_eta_EWKcorr");

  TFile* f_muon_35   = new TFile(fake_muon_file_name_35);
  fake_rate_muon_35_ = (TH2F*) f_muon_35 -> Get("FR_pT_eta_EWKcorr");

  TFile* f_muon_45   = new TFile(fake_muon_file_name_45);
  fake_rate_muon_45_ = (TH2F*) f_muon_45 -> Get("FR_pT_eta_EWKcorr");

  TFile* f_muon_PR  = new TFile(pr_muon_file_name);
  prompt_rate_muon_ = (TH2F*) f_muon_PR -> Get("h_Muon_signal_pt_eta_bin");

  // Electrons
  TFile* f_ele_25   = new TFile(fake_ele_file_name_25);
  fake_rate_ele_25_ = (TH2F*) f_ele_25 -> Get("FR_pT_eta_EWKcorr");

  TFile* f_ele_35   = new TFile(fake_ele_file_name_35);
  fake_rate_ele_35_ = (TH2F*) f_ele_35 -> Get("FR_pT_eta_EWKcorr");

  TFile* f_ele_45   = new TFile(fake_ele_file_name_45);
  fake_rate_ele_45_ = (TH2F*) f_ele_45 -> Get("FR_pT_eta_EWKcorr");

  TFile* f_ele_PR = new TFile(pr_ele_file_name);
  prompt_rate_ele_ = (TH2F*) f_ele_PR -> Get("h_Ele_signal_pt_eta_bin");


  // Load the fake rate histograms for EWK5Up and EWK5Down variations
  fake_rate_muon_25_EWK5Up_   = (TH2F*) f_muon_25->Get("FR_pT_eta_EWKcorr_EWK5Up");
  fake_rate_muon_25_EWK5Down_ = (TH2F*) f_muon_25->Get("FR_pT_eta_EWKcorr_EWK5Down");

  // Ele 35
  fake_rate_ele_35_EWK5Up_    = (TH2F*) f_ele_35->Get("FR_pT_eta_EWKcorr_EWK5Up");
  fake_rate_ele_35_EWK5Down_  = (TH2F*) f_ele_35->Get("FR_pT_eta_EWKcorr_EWK5Down");
}


// Get fake rate and its statistical uncertainty
std::tuple<double,double> 
fake_rate_reader::GetRate(TH2F* fake_rate_histo,
			  double pt, 
			  double eta,
			  double lepton_pt_max){

  double aeta = abs(eta);
  int nbinsx  = fake_rate_histo->GetNbinsX();

  if (lepton_pt_max <= 0.){
    lepton_pt_max = fake_rate_histo->GetXaxis()->GetBinCenter(nbinsx);
  }

  double rate_value = fake_rate_histo->GetBinContent(fake_rate_histo->FindBin(min(pt, lepton_pt_max), aeta));
  double rate_error = fake_rate_histo->GetBinError  (fake_rate_histo->FindBin(min(pt, lepton_pt_max), aeta));
  
  std::tuple<double,double> rate_and_error = std::make_tuple(rate_value,rate_error);

  return rate_and_error;

}


// Get fake rate for 2-leptons events
// std::tuple<double,double>
float
fake_rate_reader::GetFR_2l( double pt1 , double eta1, double pdg1, double isTight1,
			    double pt2 , double eta2, double pdg2, double isTight2,
			    TH2F* fake_rate_ele_, TH2F*  fake_rate_muon_, 
			    TString stat
			    ){
  
  double p1  = 1.; // leading lepton prompt rate
  double f1  = 0.; // leading lepton fake rate
  double pE1 = 0.; // leading lepton prompt rate statistical uncertainty
  double fE1 = 0.; // leading lepton fake rate statistical uncertainty
  double prompt_probability1 = 1.;
  double fake_probability1   = 0.;

  double p2  = 1.; // sub-leading lepton prompt rate
  double f2  = 0.; // sub-leading lepton fake rate
  double pE2 = 0.; // sub-leading lepton prompt rate statistical uncertainty
  double fE2 = 0.; // sub-leading lepton fake rate statistical uncertainty
  double prompt_probability2 = 1.;
  double fake_probability2   = 0.;
  
  // Leading lepton
  // Case electron
  if (abs(pdg1) == 11){
    std::tuple<double,double> p = GetRate(prompt_rate_ele_,  pt1, eta1, -999.);
    p1  = std::get<0>(p);
    pE1 = std::get<1>(p);
    std::tuple<double,double> f = GetRate(fake_rate_ele_,    pt1, eta1,  35.);
    f1  = std::get<0>(f);
    fE1 = std::get<1>(f);

    if      (stat == "ElUp")   f1 = f1 + fE1;
    else if (stat == "ElDown") f1 = f1 - fE1; 
  }
  // case muon
  else if (abs(pdg1) == 13){
    std::tuple<double,double> p = GetRate(prompt_rate_muon_,  pt1, eta1, -999.);
    p1  = std::get<0>(p);
    pE1 = std::get<1>(p);
    std::tuple<double,double> f = GetRate(fake_rate_muon_,    pt1, eta1,   35.);
    f1  = std::get<0>(f);
    fE1 = std::get<1>(f);

    if      (stat == "MuUp")   f1 = f1 + fE1;
    else if (stat == "MuDown") f1 = f1 - fE1; 
  }

  // Sub-leading lepton
  // case electron
  if (abs(pdg2) == 11){
    std::tuple<double,double> p = GetRate(prompt_rate_ele_,  pt2, eta2, -999.);
    p2  = std::get<0>(p);
    pE2 = std::get<1>(p);
    std::tuple<double,double> f = GetRate(fake_rate_ele_,    pt2, eta2,   35.);
    f2  = std::get<0>(f);
    fE2 = std::get<1>(f);

    if      (stat == "ElUp")   f2 = f2 + fE2;
    else if (stat == "ElDown") f2 = f2 - fE2; 
  }
  // case muon
  else if (abs(pdg2) == 13){
    std::tuple<double,double> p = GetRate(prompt_rate_muon_,  pt2, eta2, -999.);
    p2  = std::get<0>(p);
    pE2 = std::get<1>(p);
    std::tuple<double,double> f = GetRate(fake_rate_muon_,    pt2, eta2,  35.);
    f2  = std::get<0>(f);
    fE2 = std::get<1>(f);

    if      (stat == "MuUp")   f2 = f2 + fE2;
    else if (stat == "MuDown") f2 = f2 - fE2; 
  }

  // std::cout << "Prompt rates = " << p1 << ", " << p2 << std::endl;
  // std::cout << "Fake rates   = " << f1 << ", " << f2 << std::endl;
	

  // Compute per-lepton probabilities
  int nTight = 0;
  if (isTight1 == 1){
    ++nTight;
    prompt_probability1 = p1*(1. - f1) / (p1 - f1);
    fake_probability1   = f1*(1. - p1) / (p1 - f1);
  }
  else{
    prompt_probability1 = p1*f1 / (p1 - f1);
    fake_probability1   = f1*p1 / (p1 - f1);
  }

  if (isTight2 == 1){
    ++nTight;
    prompt_probability2 = p2*(1. - f2) / (p2 - f2);
    fake_probability2   = f2*(1. - p2) / (p2 - f2);
  }
  else{
    prompt_probability2 = p2*f2 / (p2 - f2);
    fake_probability2   = f2*p2 / (p2 - f2);
  }
  
  // Per-event weight
  // Leading lepton prompt - sub-leading lepton fake
  float PF = prompt_probability1*fake_probability2;
  // Leading lepton fake - sub-leading lepton prompt
  float FP = fake_probability1*prompt_probability2;
  // Both leptons fake
  float FF = fake_probability1*fake_probability2;

  if (nTight == 1)
    FF *= -1.;
  else{
    PF *= -1.;
    FP *= -1.;
  }

  // std::cout << "nTight = " << nTight << std::endl;

  // std::cout << "prompt probability 1 = " << prompt_probability1 << std::endl;
  // std::cout << "prompt probability 2 = " << prompt_probability2 << std::endl;

  // std::cout << "fake probability 1 = " << fake_probability1 << std::endl;
  // std::cout << "fake probability 2 = " << fake_probability2 << std::endl;

  // std::cout << "PF = " << PF << std::endl;
  // std::cout << "FP = " << FP << std::endl;
  // std::cout << "FF = " << FF << std::endl;
  
  float sf = PF + FP + FF;

  return sf;
}

// Get fake rate for 3-leptons events
// std::tuple<double,double>
float
fake_rate_reader::GetFR_3l( double pt1 , double eta1, double pdg1, double isTight1,
			    double pt2 , double eta2, double pdg2, double isTight2,
			    double pt3 , double eta3, double pdg3, double isTight3,
			    TH2F* fake_rate_ele_, TH2F*  fake_rate_muon_, 
			    TString stat
			    ){
  
  double p1  = 1.; // leading lepton prompt rate
  double f1  = 0.; // leading lepton fake rate
  double pE1 = 0.; // leading lepton prompt rate statistical uncertainty
  double fE1 = 0.; // leading lepton fake rate statistical uncertainty
  double prompt_probability1 = 1.;
  double fake_probability1   = 0.;

  double p2  = 1.; // sub-leading lepton prompt rate
  double f2  = 0.; // sub-leading lepton fake rate
  double pE2 = 0.; // sub-leading lepton prompt rate statistical uncertainty
  double fE2 = 0.; // sub-leading lepton fake rate statistical uncertainty
  double prompt_probability2 = 1.;
  double fake_probability2   = 0.;

  double p3  = 1.; // third lepton prompt rate
  double f3  = 0.; // third lepton fake rate
  double pE3 = 0.; // third lepton prompt rate statistical uncertainty
  double fE3 = 0.; // third lepton fake rate statistical uncertainty
  double prompt_probability3 = 1.;
  double fake_probability3   = 0.;
  
  // Leading lepton
  // Case electron
  if (abs(pdg1) == 11){
    std::tuple<double,double> p = GetRate(prompt_rate_ele_,  pt1, eta1, -999.);
    p1  = std::get<0>(p);
    pE1 = std::get<1>(p);
    std::tuple<double,double> f = GetRate(fake_rate_ele_,    pt1, eta1,  35.);
    f1  = std::get<0>(f);
    fE1 = std::get<1>(f);

    if      (stat == "ElUp")   f1 = f1 + fE1;
    else if (stat == "ElDown") f1 = f1 - fE1; 
  }
  // case muon
  else if (abs(pdg1) == 13){
    std::tuple<double,double> p = GetRate(prompt_rate_muon_,  pt1, eta1, -999.);
    p1  = std::get<0>(p);
    pE1 = std::get<1>(p);
    std::tuple<double,double> f = GetRate(fake_rate_muon_,    pt1, eta1,   35.);
    f1  = std::get<0>(f);
    fE1 = std::get<1>(f);

    if      (stat == "MuUp")   f1 = f1 + fE1;
    else if (stat == "MuDown") f1 = f1 - fE1; 
  }

  // Sub-leading lepton
  // case electron
  if (abs(pdg2) == 11){
    std::tuple<double,double> p = GetRate(prompt_rate_ele_,  pt2, eta2, -999.);
    p2  = std::get<0>(p);
    pE2 = std::get<1>(p);
    std::tuple<double,double> f = GetRate(fake_rate_ele_,    pt2, eta2,   35.);
    f2  = std::get<0>(f);
    fE2 = std::get<1>(f);

    if      (stat == "ElUp")   f2 = f2 + fE2;
    else if (stat == "ElDown") f2 = f2 - fE2; 
  }
  // case muon
  else if (abs(pdg2) == 13){
    std::tuple<double,double> p = GetRate(prompt_rate_muon_,  pt2, eta2, -999.);
    p2  = std::get<0>(p);
    pE2 = std::get<1>(p);
    std::tuple<double,double> f = GetRate(fake_rate_muon_,    pt2, eta2,  35.);
    f2  = std::get<0>(f);
    fE2 = std::get<1>(f);

    if      (stat == "MuUp")   f2 = f2 + fE2;
    else if (stat == "MuDown") f2 = f2 - fE2; 
  }

  // Third lepton
  // case electron
  if (abs(pdg3) == 11){
    std::tuple<double,double> p = GetRate(prompt_rate_ele_,  pt3, eta3, -999.);
    p3  = std::get<0>(p);
    pE3 = std::get<1>(p);
    std::tuple<double,double> f = GetRate(fake_rate_ele_,    pt3, eta3,   35.);
    f3  = std::get<0>(f);
    fE3 = std::get<1>(f);

    if      (stat == "ElUp")   f3 = f3 + fE3;
    else if (stat == "ElDown") f3 = f3 - fE3; 
  }
  // case muon
  else if (abs(pdg3) == 13){
    std::tuple<double,double> p = GetRate(prompt_rate_muon_,  pt3, eta3, -999.);
    p3  = std::get<0>(p);
    pE3 = std::get<1>(p);
    std::tuple<double,double> f = GetRate(fake_rate_muon_,    pt3, eta3,  35.);
    f3  = std::get<0>(f);
    fE3 = std::get<1>(f);

    if      (stat == "MuUp")   f3 = f3 + fE3;
    else if (stat == "MuDown") f3 = f3 - fE3; 
  }

  // Compute per-lepton probabilities
  int nTight = 0;
  if (isTight1 == 1){
    ++nTight;
    prompt_probability1 = p1*(1. - f1) / (p1 - f1);
    fake_probability1   = f1*(1. - p1) / (p1 - f1);
  }
  else{
    prompt_probability1 = p1*f1 / (p1 - f1);
    fake_probability1   = f1*p1 / (p1 - f1);
  }

  if (isTight2 == 1){
    ++nTight;
    prompt_probability2 = p2*(1. - f2) / (p2 - f2);
    fake_probability2   = f2*(1. - p2) / (p2 - f2);
  }
  else{
    prompt_probability2 = p2*f2 / (p2 - f2);
    fake_probability2   = f2*p2 / (p2 - f2);
  }

  if (isTight3 == 1){
    ++nTight;
    prompt_probability3 = p3*(1. - f3) / (p3 - f3);
    fake_probability3   = f3*(1. - p3) / (p3 - f3);
  }
  else{
    prompt_probability3 = p3*f3 / (p3 - f3);
    fake_probability3   = f3*p3 / (p3 - f3);
  }

  // Per-event weight
  // Letters indicate wether the lepton is prompt (P) or fake (F)

  float PPF = prompt_probability1*prompt_probability2*fake_probability3;
  float PFP = prompt_probability1*fake_probability2*prompt_probability3;
  float FPP = fake_probability1*prompt_probability2*prompt_probability3;

  float PFF = prompt_probability1*fake_probability2*fake_probability3;
  float FPF = fake_probability1*prompt_probability2*fake_probability3;
  float FFP = fake_probability1*fake_probability2*prompt_probability3;

  float FFF = fake_probability1*fake_probability2*fake_probability3;

  if (nTight == 1 || nTight == 3){
    PPF *= -1.;
    PFP *= -1.;
    FPP *= -1.;
    FFF *= -1.;
  }
  else{
    PFF *= -1.;
    FPF *= -1.;
    FFP *= -1.;
  }

  float sf = PPF+PFP+FPP + PFF+FPF+FFP + FFF;

  return sf;

}

#endif