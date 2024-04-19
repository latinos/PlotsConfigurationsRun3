
#include <vector>
#include "TLorentzVector.h"
#include "correction.h"
#include "ROOT/RVec.hxx"
#include "TH2D.h"
#include "TFile.h"
#include <map>
#include <sstream>
#include <fstream>

using namespace ROOT;
using namespace ROOT::VecOps;

typedef std::map<std::string, std::map<std::string, std::string>> map_dict;


class fake_rate_reader{
public:

  TString year_; 
  unsigned int nLeptons_;
  TString electron_tight_charge_;
  std::string SF_type_;
  TString ele_WP_;
  TString muon_WP_;
  float ele_WP_number_;
  float muon_WP_number_;
  TString kind_;
  RVecI*   Lepton_pdgId,Lepton_isTightMuon_cut_Tight_HWWW,Lepton_isTightElectron_mvaFall17V2Iso_WP90_SS,Lepton_muonIdx,nCleanJet;
  RVecF* Lepton_pt,Lepton_eta,Lepton_mvaTTH_UL,Muon_mvaTTH,CleanJet_pt;
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
  int isTight_[3];

  fake_rate_reader(TString year , TString ele_WP, TString muon_WP, float ele_WP_number, float muon_WP_number, TString kind, uint nLeptons, TString electron_tight_charge) {

    year_ = year;
    ele_WP_  = ele_WP;
    muon_WP_ = muon_WP;
    ele_WP_number_ = ele_WP_number;
    muon_WP_number_ = muon_WP_number;
    kind_ = kind;
    electron_tight_charge_ = electron_tight_charge; // ['std','ss'] 

    TString ele_tight_suffix = "";
    
    // Fake rate input files
    TString fake_muon_file_name_10 = "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/extended/data/fakerate/" + year + "/cut_Tight_HWWW_tthmva_" + muon_WP + "/MuonFR_jet10.root";
    TString fake_muon_file_name_15 = "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/extended/data/fakerate/" + year + "/cut_Tight_HWWW_tthmva_" + muon_WP + "/MuonFR_jet15.root";
    TString fake_muon_file_name_20 = "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/extended/data/fakerate/" + year + "/cut_Tight_HWWW_tthmva_" + muon_WP + "/MuonFR_jet20.root";
    TString fake_muon_file_name_25 = "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/extended/data/fakerate/" + year + "/cut_Tight_HWWW_tthmva_" + muon_WP + "/MuonFR_jet25.root";
    TString fake_muon_file_name_30 = "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/extended/data/fakerate/" + year + "/cut_Tight_HWWW_tthmva_" + muon_WP + "/MuonFR_jet30.root";
    TString fake_muon_file_name_35 = "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/extended/data/fakerate/" + year + "/cut_Tight_HWWW_tthmva_" + muon_WP + "/MuonFR_jet35.root";
    TString fake_muon_file_name_45 = "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/extended/data/fakerate/" + year + "/cut_Tight_HWWW_tthmva_" + muon_WP + "/MuonFR_jet45.root";

    if (year_ == "2016_HIPM" || year_ == "2016_noHIPM"){
      fake_muon_file_name_10 = "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/extended/data/fakerate/" + year + "/cut_Tight80x_tthmva_" + muon_WP + "/MuonFR_jet10.root";
      fake_muon_file_name_15 = "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/extended/data/fakerate/" + year + "/cut_Tight80x_tthmva_" + muon_WP + "/MuonFR_jet15.root";
      fake_muon_file_name_20 = "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/extended/data/fakerate/" + year + "/cut_Tight80x_tthmva_" + muon_WP + "/MuonFR_jet20.root";
      fake_muon_file_name_25 = "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/extended/data/fakerate/" + year + "/cut_Tight80x_tthmva_" + muon_WP + "/MuonFR_jet25.root";
      fake_muon_file_name_30 = "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/extended/data/fakerate/" + year + "/cut_Tight80x_tthmva_" + muon_WP + "/MuonFR_jet30.root";
      fake_muon_file_name_35 = "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/extended/data/fakerate/" + year + "/cut_Tight80x_tthmva_" + muon_WP + "/MuonFR_jet35.root";
      fake_muon_file_name_45 = "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/extended/data/fakerate/" + year + "/cut_Tight80x_tthmva_" + muon_WP + "/MuonFR_jet45.root";
    }


    TString fake_ele_file_name_25  = "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/extended/data/fakerate/" + year + "/mvaFall17V2Iso_WP90" + ele_tight_suffix + "_tthmva_UL_" + ele_WP  + "/EleFR_jet25.root";
    TString fake_ele_file_name_35  = "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/extended/data/fakerate/" + year + "/mvaFall17V2Iso_WP90" + ele_tight_suffix + "_tthmva_UL_" + ele_WP  + "/EleFR_jet35.root";
    TString fake_ele_file_name_45  = "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/extended/data/fakerate/" + year + "/mvaFall17V2Iso_WP90" + ele_tight_suffix + "_tthmva_UL_" + ele_WP  + "/EleFR_jet45.root";
    
    // Prompt rate input files
    TString pr_muon_file_name = "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/extended/data/fakerate/" + year + "/cut_Tight_HWWW_tthmva_" + muon_WP + "/MuonPR.root";
    if (year_ == "2016_HIPM" || year_ == "2016_noHIPM")
      pr_muon_file_name = "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/extended/data/fakerate/" + year + "/cut_Tight80x_tthmva_" + muon_WP + "/MuonPR.root";
    TString pr_ele_file_name =  "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/extended/data/fakerate/" + year + "/mvaFall17V2Iso_WP90" + ele_tight_suffix + "_tthmva_UL_" + ele_WP  + "/ElePR.root";


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
  }

  
  std::tuple<double,double> GetRate(TH2F* fake_rate_histo,
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

  float GetFR_2l( double pt1 , double eta1, double pdg1, double isTight1,
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
      std::tuple<double,double> f = GetRate(fake_rate_ele_,    pt1, eta1,   35.);
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
    
    float sf = PF + FP + FF;
    
    return sf;
  }
  
  RVecF operator()(RVecI Lepton_pdgId, RVecF Lepton_pt, RVecF Lepton_eta, RVecF Lepton_mvaTTH_UL, RVecF Muon_mvaTTH,
		   RVecI Lepton_muonIdx, int nCleanJet, RVecF CleanJet_pt, RVecI Lepton_isTightMuon_cut_Tight_HWWW, RVecI Lepton_isTightElectron_mvaFall17V2Iso_WP90){


    RVecI Lepton_isTightMuon_cut_Tight80x = Lepton_isTightMuon_cut_Tight_HWWW;
    nLeptons_ = Lepton_pt.size();
    
    //// Evaluate
    
    double SF = 1.; 
    // uint nLeptons = 2;
    isTight_[0] = 0;
    isTight_[1] = 0;
    isTight_[2] = 0;
    
    // Build tight lepton definitions - Now hard-coded nLepton is 2
    for (unsigned int i = 0; i < nLeptons_ ; i++) {
      if (TMath::Abs(Lepton_pdgId[i]) == 11)
	if (Lepton_isTightElectron_mvaFall17V2Iso_WP90[i] == 1 && Lepton_mvaTTH_UL[i] > ele_WP_number_) 
	  isTight_[i] = 1;
      if (TMath::Abs(Lepton_pdgId[i]) == 13)
	if (Lepton_isTightMuon_cut_Tight_HWWW[i] == 1 && Muon_mvaTTH[Lepton_muonIdx[i]] > muon_WP_number_) 
	  isTight_[i] = 1;
    }
    
    // Case 2 leptons
    if (nLeptons_ == 2){
      
      // Calculate the per-event fake rate
      float fakeWeight_2l0j = GetFR_2l(Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
				       Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
				       fake_rate_ele_35_, fake_rate_muon_20_, "Nominal");
      
      float fakeWeight_2l1j = GetFR_2l(Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
				       Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
				       fake_rate_ele_35_, fake_rate_muon_25_, "Nominal");
      
      float fakeWeight_2l2j = GetFR_2l(Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
				       Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
				       fake_rate_ele_35_, fake_rate_muon_35_, "Nominal");
      
      float fakeWeight = fakeWeight_2l0j*( nCleanJet == 0 || CleanJet_pt[0] <  30) +
	fakeWeight_2l1j*((nCleanJet == 1 && CleanJet_pt[0] >= 30) ||
			 (nCleanJet >  1 && CleanJet_pt[0] >= 30  && CleanJet_pt[1] < 30)) +
	fakeWeight_2l2j*( nCleanJet >  1 && CleanJet_pt[1] >= 30);

      

      float fakeWeight_2l0jElUp = GetFR_2l(Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
					   Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
					   fake_rate_ele_45_, fake_rate_muon_20_, "Nominal");
      
      float fakeWeight_2l1jElUp = GetFR_2l(Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
					   Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
					   fake_rate_ele_45_, fake_rate_muon_25_, "Nominal");
      
      float fakeWeight_2l2jElUp = GetFR_2l(Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
					   Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
					   fake_rate_ele_45_, fake_rate_muon_35_, "Nominal");
      

      float fakeWeightEleUp = 0.;
      if (fakeWeight != 0.){
	float num = fakeWeight_2l0jElUp*( nCleanJet == 0 || CleanJet_pt[0] <  30) + 
	  fakeWeight_2l1jElUp*((nCleanJet == 1 && CleanJet_pt[0] >= 30) || 
			       (nCleanJet >  1 && CleanJet_pt[0] >= 30 && CleanJet_pt[1] < 30)) + 
	  fakeWeight_2l2jElUp*( nCleanJet >  1 && CleanJet_pt[1] >= 30);
	
	fakeWeightEleUp = num / fakeWeight;
      }


      float fakeWeight_2l0jElDown = GetFR_2l(Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
					     Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
					     fake_rate_ele_25_, fake_rate_muon_20_, "Nominal");
      
      float fakeWeight_2l1jElDown = GetFR_2l(Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
					     Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
					     fake_rate_ele_25_, fake_rate_muon_25_, "Nominal");
      
      float fakeWeight_2l2jElDown = GetFR_2l(Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
					     Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
					     fake_rate_ele_25_, fake_rate_muon_35_, "Nominal");
      
      float fakeWeightEleDown = 0.;
      if (fakeWeight != 0.){
	float num = fakeWeight_2l0jElDown*( nCleanJet == 0 || CleanJet_pt[0] <  30) + 
	  fakeWeight_2l1jElDown*((nCleanJet == 1 && CleanJet_pt[0] >= 30) || 
				 (nCleanJet >  1 && CleanJet_pt[0] >= 30 && CleanJet_pt[1] < 30)) + 
	  fakeWeight_2l2jElDown*( nCleanJet >  1 && CleanJet_pt[1] >= 30);
	
	fakeWeightEleDown = num / fakeWeight;
      }
      

      float fakeWeight_2l0jMuUp = GetFR_2l(Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
					   Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
					   fake_rate_ele_35_, fake_rate_muon_30_, "Nominal");
      
      float fakeWeight_2l1jMuUp = GetFR_2l(Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
					   Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
					   fake_rate_ele_35_, fake_rate_muon_35_, "Nominal");
      
      float fakeWeight_2l2jMuUp = GetFR_2l(Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
					   Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
					   fake_rate_ele_35_, fake_rate_muon_45_, "Nominal");
      
      float fakeWeightMuUp = 0.;
      if (fakeWeight != 0.){
	float num = fakeWeight_2l0jMuUp*( nCleanJet == 0 || CleanJet_pt[0] <  30) + 
	  fakeWeight_2l1jMuUp*((nCleanJet == 1 && CleanJet_pt[0] >= 30) || 
			       (nCleanJet >  1 && CleanJet_pt[0] >= 30 && CleanJet_pt[1] < 30)) + 
	  fakeWeight_2l2jMuUp*( nCleanJet >  1 && CleanJet_pt[1] >= 30);
	
	fakeWeightMuUp = num / fakeWeight;
      }
      

      float fakeWeight_2l0jMuDown = GetFR_2l(Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
					     Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
					     fake_rate_ele_35_, fake_rate_muon_10_, "Nominal");
      
      float fakeWeight_2l1jMuDown = GetFR_2l(Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
					     Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
					     fake_rate_ele_35_, fake_rate_muon_15_, "Nominal");
      
      float fakeWeight_2l2jMuDown = GetFR_2l(Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
					     Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
					     fake_rate_ele_35_, fake_rate_muon_25_, "Nominal");
      
      float fakeWeightMuDown = 0.;
      if (fakeWeight != 0.){
	float num = fakeWeight_2l0jMuDown*( nCleanJet == 0 || CleanJet_pt[0] <  30) + 
	  fakeWeight_2l1jMuDown*((nCleanJet == 1 && CleanJet_pt[0] >= 30) || 
				 (nCleanJet >  1 && CleanJet_pt[0] >= 30 && CleanJet_pt[1] < 30)) + 
	  fakeWeight_2l2jMuDown*( nCleanJet >  1 && CleanJet_pt[1] >= 30);
	
	fakeWeightMuDown = num / fakeWeight;
      }
      

      float fakeWeight_2l0jstatElUp = GetFR_2l(Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
					       Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
					       fake_rate_ele_35_, fake_rate_muon_20_, "ElUp");
      
      float fakeWeight_2l1jstatElUp = GetFR_2l(Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
					       Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
					       fake_rate_ele_35_, fake_rate_muon_25_, "ElUp");
      
      float fakeWeight_2l2jstatElUp = GetFR_2l(Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
					       Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
					       fake_rate_ele_35_, fake_rate_muon_35_, "ElUp");
      
      float fakeWeightstatEleUp = 0.;
      if (fakeWeight != 0.){
	float num = fakeWeight_2l0jstatElUp*( nCleanJet == 0 || CleanJet_pt[0] <  30) + 
	            fakeWeight_2l1jstatElUp*((nCleanJet == 1 && CleanJet_pt[0] >= 30) || 
					     (nCleanJet >  1 && CleanJet_pt[0] >= 30 && CleanJet_pt[1] < 30)) + 
                    fakeWeight_2l2jstatElUp*( nCleanJet >  1 && CleanJet_pt[1] >= 30);
	
	fakeWeightstatEleUp = num / fakeWeight;
      }

      float fakeWeight_2l0jstatElDown = GetFR_2l(Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
						 Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
						 fake_rate_ele_35_, fake_rate_muon_20_, "ElDown");
      
      float fakeWeight_2l1jstatElDown = GetFR_2l(Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
						 Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
						 fake_rate_ele_35_, fake_rate_muon_25_, "ElDown");
      
      float fakeWeight_2l2jstatElDown = GetFR_2l(Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
						 Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
						 fake_rate_ele_35_, fake_rate_muon_35_, "ElDown");
      
      float fakeWeightstatEleDown = 0.;
      if (fakeWeight != 0.){
	float num = fakeWeight_2l0jstatElDown*( nCleanJet == 0 || CleanJet_pt[0] <  30) + 
	            fakeWeight_2l1jstatElDown*((nCleanJet == 1 && CleanJet_pt[0] >= 30) || 
					       (nCleanJet >  1 && CleanJet_pt[0] >= 30 && CleanJet_pt[1] < 30)) + 
	            fakeWeight_2l2jstatElDown*( nCleanJet >  1 && CleanJet_pt[1] >= 30);
	
	fakeWeightstatEleDown = num / fakeWeight;
      }
      

      float fakeWeight_2l0jstatMuUp = GetFR_2l(Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
					       Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
					       fake_rate_ele_35_, fake_rate_muon_20_, "MuUp");
      
      float fakeWeight_2l1jstatMuUp = GetFR_2l(Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
					       Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
					       fake_rate_ele_35_, fake_rate_muon_25_, "MuUp");
      
      float fakeWeight_2l2jstatMuUp = GetFR_2l(Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
					       Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
					       fake_rate_ele_35_, fake_rate_muon_35_, "MuUp");
      
      float fakeWeightstatMuUp = 0.;
      if (fakeWeight != 0.){
		float num = fakeWeight_2l0jstatMuUp*( nCleanJet == 0 || CleanJet_pt[0] <  30) + 
                    fakeWeight_2l1jstatMuUp*((nCleanJet == 1 && CleanJet_pt[0] >= 30) || 
					     (nCleanJet >  1 && CleanJet_pt[0] >= 30 && CleanJet_pt[1] < 30)) + 
                    fakeWeight_2l2jstatMuUp*( nCleanJet >  1 && CleanJet_pt[1] >= 30);
	
		fakeWeightstatMuUp = num / fakeWeight;
      }


      float fakeWeight_2l0jstatMuDown = GetFR_2l(Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
						 Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
						 fake_rate_ele_35_, fake_rate_muon_20_, "MuDown");
      
      float fakeWeight_2l1jstatMuDown = GetFR_2l(Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
						 Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
						 fake_rate_ele_35_, fake_rate_muon_25_, "MuDown");
      
      float fakeWeight_2l2jstatMuDown = GetFR_2l(Lepton_pt[0], Lepton_eta[0], Lepton_pdgId[0], isTight_[0],
						 Lepton_pt[1], Lepton_eta[1], Lepton_pdgId[1], isTight_[1],
						 fake_rate_ele_35_, fake_rate_muon_35_, "MuDown");
      
      float fakeWeightstatMuDown = 0.;
      if (fakeWeight != 0.){
		float num = fakeWeight_2l0jstatMuDown*( nCleanJet == 0 || CleanJet_pt[0] <  30) + 
		  fakeWeight_2l1jstatMuDown*((nCleanJet == 1 && CleanJet_pt[0] >= 30) || 
					     (nCleanJet >  1 && CleanJet_pt[0] >= 30 && CleanJet_pt[1] < 30)) + 
		  fakeWeight_2l2jstatMuDown*( nCleanJet >  1 && CleanJet_pt[1] >= 30);
		
		fakeWeightstatMuDown = num / fakeWeight;
      }
      


      RVecF results = {fakeWeight,fakeWeightEleUp,fakeWeightEleDown,fakeWeightMuUp,fakeWeightMuDown,fakeWeightstatEleUp,fakeWeightstatEleDown,fakeWeightstatMuUp,fakeWeightstatMuDown};
      
      return results;
	
    }
    
    return {-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0,-1.0};
    
  }
};




