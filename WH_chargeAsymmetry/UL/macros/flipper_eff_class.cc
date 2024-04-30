#ifndef FLIPPER_EFF
#define FLIPPER_EFF

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

typedef std::map<std::string,std::map<std::string,std::string>> map_dict;

class flipper_eff{

public:

  flipper_eff( const char* year , const unsigned int nLep , std::string SF_type, std::string isTightCharge );
  ~flipper_eff();

  const char* year_;
  int nLeptons_;
  std::string SF_type_;
  std::string isTightCharge_;

  RVecF lepton_pt;
  RVecF lepton_eta;
  RVecI lepton_pdgId;

  map_dict flipper_map_;

  TH2D* h_sf_;
  TH2D* h_sf_syst_;
  
  void loadSF2D( std::string filename );

  double operator()(RVecF Lepton_pt, RVecF Lepton_eta, RVecI Lepton_pdgId) {
    lepton_pt     = Lepton_pt;
    lepton_eta    = Lepton_eta;
    lepton_pdgId  = Lepton_pdgId;

    // std::cout << "Lepton pT    = " << lepton_pt    << std::endl;
    // std::cout << "Lepton eta   = " << lepton_eta   << std::endl;
    // std::cout << "Lepton pdgId = " << lepton_pdgId << std::endl;
	
	std::vector<double> SF_vect {};
	std::vector<double> SF_err_vect {};

	// std::cout << "nLeptons_ = " << nLeptons_ << std::endl;
	
	// Loop over leptons
	for (unsigned int i = 0; i < nLeptons_; i++) {

	  // std::cout << "i value in loop = " << i << std::endl;
	  
	  // Consider only electrons (we don't have efficiencies for muons, as they are negligible)
	  if(abs(Lepton_pdgId[i]) == 11){
		// std::cout << "I have found an electron!" << std::endl;
		std::tuple<double, double> res_ttHMVA = GetSF(lepton_pt[i], abs(lepton_eta[i]));
		// std::cout << "Assigning values: " << std::get<0>(res_ttHMVA) << " and " << std::get<1>(res_ttHMVA) << std::endl;
		SF_vect.push_back(std::get<0>(res_ttHMVA));
		SF_err_vect.push_back(std::get<1>(res_ttHMVA));
		// std::cout << "Values assigned!" << std::endl;		
	  }
	}
  
	double SF=1.;
	double SF_err=0.;

	// std::cout << "SF_vect      = " << SF_vect        << std::endl;
	// std::cout << "SF_vect size = " << SF_vect.size() << std::endl;
	
	// We want efficiencies, not SFs --> Use formula:
	// P_tot = P1(1 - P2) + (1-P1)P2
	if (SF_vect.size() == 1) 
	  {
		SF = SF_vect[0];
		// std::cout << "Efficiency value in 1 electron case: " << SF << std::endl;
	  }
	else if (SF_vect.size() == 2)
	  {
		SF = SF_vect[0]*(1 - SF_vect[1]) + (1 - SF_vect[0])*SF_vect[1];
		// std::cout << "Efficiency value in 2 electrons case: " << SF << std::endl;
	  }
	else {} // do nothing 
	
	// for(auto x : SF_vect) SF *= x;
	
	// Variation
	// ??
	// Statistical error
	// for ( unsigned int i = 0 ; i < SF_vect.size() ; i++) 
	// SF_err += TMath::Power( SF_err_vect[i] , 2 ) / SF_vect[i];

	// Check if error propagation is correct
	if (SF_err_vect.size() == 1) 
	  {
		SF_err = SF_err_vect[0]*SF_err_vect[0];
	  }
	else if (SF_err_vect.size() == 2)
	  {
		SF_err = TMath::Power((1-2*SF_vect[1])*SF_err_vect[0], 2) + TMath::Power((1-2*SF_vect[0])*SF_err_vect[1], 2);
	  }
	else {} // do nothing

	if ( SF_type_.compare("Total_SF") == 0 ) { return SF; }
	else if ( SF_type_.compare("Total_SF_err") == 0 ) { return TMath::Sqrt( SF_err ); }
	else{ std::cout << "invalid option: please choose from [ Total_SF , Total_SF_err ]" << std::endl; return 0; }
  }

private:
  std::tuple<double,double> GetSF( double pt_in , double eta_in );

};

// Load efficiencies from files
flipper_eff::flipper_eff( const char* year , const unsigned int nLep, std::string SF_type, std::string isTightCharge = "false" ) {

  std::cout << "Year:          " << year          << std::endl;
  std::cout << "nLep:          " << nLep          << std::endl;
  std::cout << "SF type:       " << SF_type       << std::endl;
  std::cout << "isTightCharge: " << isTightCharge << std::endl;

  year_          = year;
  nLeptons_      = nLep;
  SF_type_       = SF_type;
  isTightCharge_ = isTightCharge;

  // std::string cmssw_base = std::getenv("CMSSW_BASE");
  // Path to start.sh (e.g. /afs/cern.ch/user/n/ntrevisa/work/latinos/Run3/mkShapesRDF/start.sh)
  std::string mkShapesRDF_base = std::getenv("STARTPATH");
  // std::cout << "mkShapesRDF_base = " << mkShapesRDF_base << std::endl;

  mkShapesRDF_base.erase(mkShapesRDF_base.end()-20,mkShapesRDF_base.end());
  // std::cout << "mkShapesRDF_base w/o 'mkShapesRDF/start.sh' = " << mkShapesRDF_base << std::endl;

  // Here, we assume you installed PlotsConfigurationsRun3 in the same directory as mkShapesRDF
  // E.g. /afs/cern.ch/user/n/ntrevisa/work/latinos/Run3/
  //std::string mkShapesRDF_base = start_path + "/../../Run3/PlotsConfigurationsRun3/WH_chargeAsymmetry/UL/data/";
  std::string relative_path = "PlotsConfigurationsRun3/WH_chargeAsymmetry/UL/data/";
  mkShapesRDF_base.append(relative_path);
  // std::cout << "mkShapesRDF_base final version = " << mkShapesRDF_base << std::endl;  
  
  // Build map of SF files names
  map_dict flipper_map;

  // map
  if (isTightCharge == "false"){
    flipper_map["UL_2016HIPM"]["HWW_ttHMVA"]   = mkShapesRDF_base + "chargeflip/2016HIPM/chargeFlip_SF.root";
    flipper_map["UL_2016noHIPM"]["HWW_ttHMVA"] = mkShapesRDF_base + "chargeflip/2016noHIPM/chargeFlip_SF.root";
    flipper_map["UL_2017"]["HWW_ttHMVA"]       = mkShapesRDF_base + "chargeflip/2017/chargeFlip_SF.root";
    flipper_map["UL_2018"]["HWW_ttHMVA"]       = mkShapesRDF_base + "chargeflip/2018/chargeFlip_SF.root";
  }
  else{
    flipper_map["2016"]["HWW_ttHMVA"] = mkShapesRDF_base + "/src/LatinoAnalysis/NanoGardener/python/data/scale_factor/Full2016v7/chargeFlip_2016_v7_SF_tightCharge.root"; // file doesn't exist!
    flipper_map["2017"]["HWW_ttHMVA"] = mkShapesRDF_base + "/src/LatinoAnalysis/NanoGardener/python/data/scale_factor/Full2017v7/chargeFlip_2017_v7_SF_tightCharge.root"; // file doesn't exist!
    flipper_map["2018"]["HWW_ttHMVA"] = mkShapesRDF_base + "/src/LatinoAnalysis/NanoGardener/python/data/scale_factor/Full2018v7/chargeFlip_2018_v7_SF_tightCharge.root"; // file doesn't exist!
  }

  flipper_map_ = flipper_map;

//   // load histogram
//   loadSF2D( flipper_map_[year_]["HWW_ttHMVA"] );
// }

// // Load efficiencies from TH2F
// void flipper_eff::loadSF2D( std::string filename ){

  // TFile f(filename.c_str());

  // std::cout << "File name = " << flipper_map[year_]["HWW_ttHMVA"] << std::endl;
  
  TFile f(flipper_map[year_]["HWW_ttHMVA"].c_str());

  float eta_bins[] {0., 1.444, 2.5};
  float pt_bins[]  {10., 20., 200.};

  // h_sf_      = new TH2D("", "", 2, eta_bins, 2, pt_bins);
  // h_sf_syst_ = new TH2D("", "", 2, eta_bins, 2, pt_bins);


  // Data eff
  h_sf_      = (TH2D*)f.Get("data");
  h_sf_syst_ = (TH2D*)f.Get("data_sys");
  h_sf_->SetDirectory(0);
  h_sf_syst_->SetDirectory(0);

  // std::cout << "First bin of h_sf_ = " << h_sf_->GetBinContent(1,1);

  // for(int i=1; i<=2; i++){
  //   for(int j=1; j<=2; j++){
  //     h_sf_->SetBinContent(     i, j, tmp_sf  -> GetBinContent(i, j));
  //     h_sf_syst_->SetBinContent(i, j, tmp_sys -> GetBinContent(i, j));
  // 	}
  // }

  // // // Data eff
  // // Effmap_.insert(std::make_pair( "data"       , h_sf       ));
  // // Effmap_.insert(std::make_pair( "data_sys"   , h_sf_sys   ));

  f.Close();
}

std::tuple<double,double>
flipper_eff::GetSF( double pt_in , double eta_in ){

  double eta_temp = eta_in;
  double pt_temp  = pt_in;

  double eta_max = 2.49;
  double pt_max = 199.;
  double pt_min = 10.;
  
  // std::cout << "Setting correct pt,eta values ..." << std::endl;

  if( eta_temp > eta_max ){ eta_temp = eta_max; }
  if( pt_temp < pt_min   ){ pt_temp = pt_min; }
  if( pt_temp > pt_max   ){ pt_temp = pt_max; }

  // std::cout << "Values set!" << std::endl;

  // Data eff
  // double sf     = Effmap_["data"].GetBinContent(    Effmap_["data"].FindBin(eta_in, pt_in));
  // double sf_sys = Effmap_["data_sys"].GetBinContent(Effmap_["data_sys"].FindBin(eta_in, pt_in));

  // Data eff
  double sf     = h_sf_      -> GetBinContent(h_sf_     -> FindBin(eta_temp, pt_temp));
  double sf_sys = h_sf_syst_ -> GetBinContent(h_sf_syst_-> FindBin(eta_temp, pt_temp));

  // std::cout << "I got the efficiencies values!" << std::endl;

  std::tuple<double,double> sfs = {sf, sf_sys};
  return sfs;
}
	  
flipper_eff::~flipper_eff(){

  std::cout << "Doing histogram cleanup" << std::endl;

  h_sf_->Delete();
  h_sf_syst_->Delete();
}

#endif
