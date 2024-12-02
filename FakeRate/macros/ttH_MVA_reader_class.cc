#ifndef TTH_MVA_READER
#define TTH_MVA_READER

#include "ROOT/RVec.hxx"

using namespace ROOT;
using namespace ROOT::VecOps;


class ttH_MVA_reader{
  
public:
  
  ttH_MVA_reader(TString BDT_name_electron, TString xml_file_name_electron, TString BDT_name_muon, TString xml_file_name_muon);
  ~ttH_MVA_reader();
  
  // Variables needed to locate xml file with BDT weights
  TString BDT_name_electron_;
  TString xml_file_name_electron_;
  TString BDT_name_muon_;
  TString xml_file_name_muon_;
  
  // Variables needed to select the correct lepton
  int nLepton_;
  int Lepton_pdgId_;
  int Lepton_electronIdx_;
  int Electron_jetIdx_;
  int Lepton_muonIdx_;
  int Muon_jetIdx_;
  
  // Variables to be used to evaluate the BDT
  float event_;
  
  float Electron_mvaTTH_;
  float Electron_miniPFRelIso_all_;
  float Electron_mvaFall17V2noIso_WPL_;
  float Electron_lostHits_;
  float Electron_genPartFlav_; // --> using always 1
  float Electron_dxy_;
  float Electron_dz_;
  
  float Electron_pt_;
  float Electron_eta_;
  float Electron_pfRelIso03_all_;
  float Electron_miniPFRelIso_chg_;
  float Electron_miniRelIsoNeutral_;
  float Electron_jetNDauCharged_;
  float Electron_jetPtRelv2_;
  float Electron_jetPtRatio_;
  float Electron_jetBTagDeepFlavB_;
  float Electron_sip3d_;
  float Electron_log_dxy_;
  float Electron_log_dz_;
  float Electron_mvaFall17V2noIso_;

  float Muon_mvaTTH_;
  float Muon_miniPFRelIso_all_;
  float Muon_looseId_;
  float Muon_genPartFlav_; // --> using always 1
  float Muon_isGlobal_;
  float Muon_isTracker_;
  float Muon_isPFcand_;
  float Muon_mediumId_;
  float Muon_looseIdBis_;
  float Muon_dxy_;
  float Muon_dz_;

  float Muon_pt_;
  float Muon_eta_;
  float Muon_pfRelIso03_all_;
  float Muon_miniPFRelIso_chg_;
  float Muon_miniRelIsoNeutral_;
  float Muon_jetNDauCharged_;
  float Muon_jetPtRelv2_;
  float Muon_jetPtRatio_;
  float Muon_jetBTagDeepFlavB_;
  float Muon_sip3d_;
  float Muon_log_dxy_;
  float Muon_log_dz_;
  float Muon_segmentComp_;

  TMVA::Reader *reader_muon     = new TMVA::Reader();
  TMVA::Reader *reader_electron = new TMVA::Reader();
  
  std::vector<float> operator()(int   nLepton,
								RVecI Lepton_pdgId,
								RVecI Lepton_electronIdx,
								RVecI Electron_jetIdx,
								int   event,
								RVecF Electron_mvaTTH,
								RVecF Electron_mvaFall17V2noIso_WPL,
								RVecF Electron_lostHits,
								// char  Electron_genPartFlav,
								RVecF Electron_pt,
								RVecF Electron_eta,
								RVecF Electron_pfRelIso03_all,
								RVecF Electron_miniPFRelIso_chg,
								RVecF Electron_miniPFRelIso_all,
								RVecI Electron_jetNDauCharged,
								RVecF Electron_jetPtRelv2,
								RVecF Electron_jetRelIso,
								RVecF Jet_btagDeepFlavB,
								RVecF Electron_sip3d,
								RVecF Electron_dxy,
								RVecF Electron_dz,
								RVecF Electron_mvaFall17V2noIso,
								RVecI Lepton_muonIdx,
								RVecI Muon_jetIdx,
								RVecF Muon_mvaTTH,
								RVecF Muon_looseId,
								// char  Muon_genPartFlav,
								RVecF Muon_isGlobal,
								RVecF Muon_isTracker,
								RVecF Muon_isPFcand,
								RVecF Muon_mediumId,
								RVecF Muon_pt,
								RVecF Muon_eta,
								RVecF Muon_pfRelIso03_all,
								RVecF Muon_miniPFRelIso_chg,
								RVecF Muon_miniPFRelIso_all,
								RVecI Muon_jetNDauCharged,
								RVecF Muon_jetPtRelv2,
								RVecF Muon_jetRelIso,
								RVecF Muon_sip3d,
								RVecF Muon_dxy,
								RVecF Muon_dz,
								RVecF Muon_segmentComp){

	// Define output vector
	std::vector<float> Lepton_mva;
	float classifier = 0;

	nLepton_ = nLepton;
	
	// Loop over leptons
	for (int iLep = 0; iLep < nLepton_; ++iLep){
	  
	  Lepton_pdgId_ = Lepton_pdgId[iLep];
	  
	  // Case electron
	  if (abs(Lepton_pdgId_) == 11 || Lepton_pdgId_ == 11 || Lepton_pdgId_ == -11){
		
		// std::cout << "The electron particle Id is " << Lepton_pdgId_ << std::endl;

		Lepton_electronIdx_ = Lepton_electronIdx[iLep];
		Electron_jetIdx_    = Electron_jetIdx[iLep];

		// Variables to be used to evaluate the BDT
		event_                         = event;
		Electron_mvaTTH_               = Electron_mvaTTH[Lepton_electronIdx_];
		Electron_miniPFRelIso_all_     = Electron_miniPFRelIso_all[Lepton_electronIdx_];
		Electron_mvaFall17V2noIso_WPL_ = Electron_mvaFall17V2noIso_WPL[Lepton_electronIdx_];
		Electron_lostHits_             = Electron_lostHits[Lepton_electronIdx_];
		Electron_genPartFlav_          = 1, // Electron_genPartFlav[Lepton_electronIdx_]; // '1'
		Electron_dxy_                  = Electron_dxy[Lepton_electronIdx_];
		Electron_dz_                   = Electron_dz[Lepton_electronIdx_];

		Electron_pt_                   = Electron_pt[Lepton_electronIdx_];
		Electron_eta_                  = Electron_eta[Lepton_electronIdx_];
		Electron_pfRelIso03_all_       = Electron_pfRelIso03_all[Lepton_electronIdx_];
		Electron_miniPFRelIso_chg_     = Electron_miniPFRelIso_chg[Lepton_electronIdx_];
		Electron_miniRelIsoNeutral_    = Electron_miniPFRelIso_all[Lepton_electronIdx_] - Electron_miniPFRelIso_chg[Lepton_electronIdx_]; // event.Electron_miniPFRelIso_all[eleID] - event.Electron_miniPFRelIso_chg[eleID]'
		Electron_jetNDauCharged_       = Electron_jetNDauCharged[Lepton_electronIdx_];
		Electron_jetPtRelv2_           = Electron_jetPtRelv2[Lepton_electronIdx_];
		Electron_jetPtRatio_           = min(1. / (1 + Electron_jetRelIso[Lepton_electronIdx_]), 1.5); // 'min(1. / (1 + event.Electron_jetRelIso[eleID]), 1.5)'
		Electron_jetBTagDeepFlavB_     = Electron_jetIdx_ > -1 ? Jet_btagDeepFlavB[Electron_jetIdx_] : 0; // 'event.Jet_btagDeepFlavB[event.Electron_jetIdx[eleID]] if event.Electron_jetIdx[eleID] > -1 else 0'
		Electron_sip3d_                = Electron_sip3d[Lepton_electronIdx_];
		Electron_log_dxy_              = log(abs(Electron_dxy[Lepton_electronIdx_])); // 'math.log(abs(event.Electron_dxy[eleID]))'
		Electron_log_dz_               = log(abs(Electron_dz[Lepton_electronIdx_]));  // 'math.log(abs(event.Electron_dz[eleID]))'
		Electron_mvaFall17V2noIso_     = Electron_mvaFall17V2noIso[Lepton_electronIdx_];

		// // Comparing variables
		// std::cout << "Comparing variables ... "   << std::endl;
		// std::cout << "Electron pT: "              << Electron_pt_               << ", " << Electron_pt[Lepton_electronIdx_]  << ", " << Electron_pt[iLep]  << std::endl;
		// std::cout << "Electron eta: "             << Electron_eta_              << ", " << Electron_eta[Lepton_electronIdx_] << ", " << Electron_eta[iLep] << std::endl;
		// std::cout << "Electron pfreliso03all: "   << Electron_pfRelIso03_all_   << ", " << Electron_pfRelIso03_all[Lepton_electronIdx_] << std::endl;
		// std::cout << "Electron minipfrelisochg: " << Electron_miniPFRelIso_all[Lepton_electronIdx_] << " - " << Electron_miniPFRelIso_chg[Lepton_electronIdx_] << ", " << Electron_miniPFRelIso_all[Lepton_electronIdx_] - Electron_miniPFRelIso_chg[Lepton_electronIdx_] << std::endl;
		// std::cout << "Electron jetNDauCharged: "  << Electron_jetNDauCharged_   << ", " << Electron_jetNDauCharged[Lepton_electronIdx_] << std::endl;
		// std::cout << "Electron jetptrelv2: "      << Electron_jetPtRelv2_       << ", " << Electron_jetPtRelv2[Lepton_electronIdx_] << std::endl;
		// std::cout << "Electron jetBTagDeepFlavB: "<< Electron_jetBTagDeepFlavB_ << ", " << Jet_btagDeepFlavB[Electron_jetIdx_] << std::endl;
		// std::cout << "Electron jetptratio: "      << Electron_jetPtRatio_       << ", " << min(1. / (1 + Electron_jetRelIso[Lepton_electronIdx_]), 1.5) << std::endl;
		// std::cout << "Electron sip3d: "           << Electron_sip3d_            << ", " << Electron_sip3d[Lepton_electronIdx_] << std::endl;
		// std::cout << "Electron dxy: "             << Electron_dxy[Lepton_electronIdx_] << " --> log: " << log(abs(Electron_dxy[Lepton_electronIdx_])) << std::endl;
		// std::cout << "Electron dz: "              << Electron_dz[Lepton_electronIdx_]  << " --> log: " << log(abs(Electron_dz[Lepton_electronIdx_])) << std::endl;
		// std::cout << "Electron mvaIso: "          << Electron_mvaIso[Lepton_electronIdx_] << ", " << Electron_mvaIso[iLep] << std::endl;
		
		// Evaluate the classifier
		classifier = reader_electron->EvaluateMVA(BDT_name_electron_);
		// std::cout << "Classifier value (electron) = " << classifier << std::endl;
	  }
	  // Case muon
	  else if (abs(Lepton_pdgId_) == 13 || Lepton_pdgId_ == 13 || Lepton_pdgId_ == -13){
		
		// std::cout << "The muon particle Id is " << Lepton_pdgId_ << std::endl;

		Lepton_muonIdx_ = Lepton_muonIdx[iLep];
		Muon_jetIdx_    = Muon_jetIdx[iLep];
		
		// Variables to be used to evaluate the BDT
		event_                  = event;
		Muon_mvaTTH_            = Muon_mvaTTH[Lepton_muonIdx_];
		Muon_miniPFRelIso_all_  = Muon_miniPFRelIso_all[Lepton_muonIdx_];
		Muon_looseId_           = Muon_looseId[Lepton_muonIdx_];
		Muon_genPartFlav_       = 1, // Muon_genPartFlav[Lepton_muonIdx_]; // '1'
		Muon_isGlobal_          = Muon_isGlobal[Lepton_muonIdx_];
		Muon_isTracker_         = Muon_isTracker[Lepton_muonIdx_];
		Muon_isPFcand_          = Muon_isPFcand[Lepton_muonIdx_];
		Muon_mediumId_          = Muon_mediumId[Lepton_muonIdx_];
		Muon_looseIdBis_        = Muon_looseId[Lepton_muonIdx_];
		Muon_dxy_               = Muon_dxy[Lepton_muonIdx_];
		Muon_dz_                = Muon_dz[Lepton_muonIdx_];
		
		Muon_pt_                = Muon_pt[Lepton_muonIdx_];
		Muon_eta_               = Muon_eta[Lepton_muonIdx_];
		Muon_pfRelIso03_all_    = Muon_pfRelIso03_all[Lepton_muonIdx_];
		Muon_miniPFRelIso_chg_  = Muon_miniPFRelIso_chg[Lepton_muonIdx_];
		Muon_miniRelIsoNeutral_ = Muon_miniPFRelIso_all[Lepton_muonIdx_] - Muon_miniPFRelIso_chg[Lepton_muonIdx_]; // event.Muon_miniPFRelIso_all[muonid] - event.Muon_miniPFRelIso_chg[muonid]'
		Muon_jetNDauCharged_    = Muon_jetNDauCharged[Lepton_muonIdx_];
		Muon_jetPtRelv2_        = Muon_jetPtRelv2[Lepton_muonIdx_];
		Muon_jetPtRatio_        = min(1. / (1 + Muon_jetRelIso[Lepton_muonIdx_]), 1.5); // 'min(1. / (1 + event.Muon_jetRelIso[muonid]), 1.5)'
		Muon_jetBTagDeepFlavB_  = Muon_jetIdx_ > -1 ? Jet_btagDeepFlavB[Muon_jetIdx_] : 0; // 'event.Jet_btagDeepFlavB[event.Muon_jetIdx[muonid]] if event.Muon_jetIdx[muonid] > -1 else 0'
		Muon_sip3d_             = Muon_sip3d[Lepton_muonIdx_];
		Muon_log_dxy_           = log(abs(Muon_dxy[Lepton_muonIdx_])); // 'math.log(abs(event.Muon_dxy[muonid]))'
		Muon_log_dz_            = log(abs(Muon_dz[Lepton_muonIdx_]));  // 'math.log(abs(event.Muon_dz[muonid]))'
		Muon_segmentComp_       = Muon_segmentComp[Lepton_muonIdx_];

		// Evaluate the classifier
		classifier = reader_muon->EvaluateMVA(BDT_name_muon_);
		// std::cout << "Classifier value (muon) = " << classifier << std::endl;
	  }
	  // Default case
	  else {
		std::cout << "This is not an electron nor a muon: I'll assign a default value of -999" << std::endl;
		std::cout << "The particle Id is " << Lepton_pdgId_ << std::endl;
		classifier = -999.0;
	  }

	  Lepton_mva.emplace_back(classifier);
	  
	}
	return Lepton_mva;
  }
  
};

  ttH_MVA_reader::ttH_MVA_reader( TString BDT_name_electron, TString xml_file_name_electron, TString BDT_name_muon, TString xml_file_name_muon){
	
	std::cout << "BDT name electron:      " << BDT_name_electron      << std::endl;
	std::cout << "xml file name electron: " << xml_file_name_electron << std::endl;
	
	BDT_name_electron_      = BDT_name_electron;
	xml_file_name_electron_ = xml_file_name_electron;
	
	std::cout << "BDT name muon:      " << BDT_name_muon      << std::endl;
	std::cout << "xml file name muon: " << xml_file_name_muon << std::endl;
	
	BDT_name_muon_      = BDT_name_muon;
	xml_file_name_muon_ = xml_file_name_muon;
	
	// Pass variables to the reader
	///////////////////////////////
	
	// Variable to evaluate the BDT - electron
	reader_electron->AddSpectator("event",                                                                                     &event_);
	reader_electron->AddSpectator("Electron_mvaTTH",			                                                               &Electron_mvaTTH_);
	reader_electron->AddSpectator("Electron_miniPFRelIso_all",	                                                               &Electron_miniPFRelIso_all_);
	reader_electron->AddSpectator("Electron_mvaFall17V2noIso_WPL",                                                             &Electron_mvaFall17V2noIso_WPL_);
	reader_electron->AddSpectator("Electron_lostHits",			                                                               &Electron_lostHits_);
	reader_electron->AddSpectator("Electron_genPartFlav",		                                                               &Electron_genPartFlav_);
	reader_electron->AddSpectator("Electron_dxy",				                                                               &Electron_dxy_);
	reader_electron->AddSpectator("Electron_dz",                                                                               &Electron_dz_);                  

	reader_electron->AddVariable("Electron_pt",                                                                                &Electron_pt_);
	reader_electron->AddVariable("Electron_eta",                                                                               &Electron_eta_);
	reader_electron->AddVariable("Electron_pfRelIso03_all",                                                                    &Electron_pfRelIso03_all_);
	reader_electron->AddVariable("Electron_miniPFRelIso_chg",                                                                  &Electron_miniPFRelIso_chg_);
	reader_electron->AddVariable("Electron_miniRelIsoNeutral := Electron_miniPFRelIso_all - Electron_miniPFRelIso_chg",        &Electron_miniRelIsoNeutral_);
	reader_electron->AddVariable("Electron_jetNDauCharged",                                                                    &Electron_jetNDauCharged_);
	reader_electron->AddVariable("Electron_jetPtRelv2",                                                                        &Electron_jetPtRelv2_);
	reader_electron->AddVariable("Electron_jetPtRatio := min(1 / (1 + Electron_jetRelIso), 1.5)",                              &Electron_jetPtRatio_);
	reader_electron->AddVariable("Electron_jetBTagDeepFlavB := Electron_jetIdx > -1 ? Jet_btagDeepFlavB[Electron_jetIdx] : 0", &Electron_jetBTagDeepFlavB_);
	reader_electron->AddVariable("Electron_sip3d",                                                                             &Electron_sip3d_);
	reader_electron->AddVariable("Electron_log_dxy := log(abs(Electron_dxy))",                                                 &Electron_log_dxy_);
	reader_electron->AddVariable("Electron_log_dz  := log(abs(Electron_dz))",                                                  &Electron_log_dz_);
	reader_electron->AddVariable("Electron_mvaFall17V2noIso",                                                                  &Electron_mvaFall17V2noIso_);
	
	reader_electron->BookMVA(BDT_name_electron, xml_file_name_electron);
	
	// Variable to evaluate the BDT - muon
	reader_muon->AddSpectator("event",                  &event_);
	reader_muon->AddSpectator("Muon_mvaTTH",            &Muon_mvaTTH_);
	reader_muon->AddSpectator("Muon_miniPFRelIso_all",  &Muon_miniPFRelIso_all_);
	reader_muon->AddSpectator("Muon_looseId",           &Muon_looseId_);
	reader_muon->AddSpectator("Muon_genPartFlav",       &Muon_genPartFlav_);
	reader_muon->AddSpectator("Muon_isGlobal",          &Muon_isGlobal_);
	reader_muon->AddSpectator("Muon_isTracker",         &Muon_isTracker_);
	reader_muon->AddSpectator("Muon_isPFcand",          &Muon_isPFcand_);
	reader_muon->AddSpectator("Muon_mediumId",          &Muon_mediumId_);
	reader_muon->AddSpectator("Muon_looseId",           &Muon_looseId_);
	reader_muon->AddSpectator("Muon_dxy",               &Muon_dxy_);
	reader_muon->AddSpectator("Muon_dz",                &Muon_dz_);

	reader_muon->AddVariable("Muon_pt",                                                                        &Muon_pt_);
	reader_muon->AddVariable("Muon_eta",                                                                       &Muon_eta_);
	reader_muon->AddVariable("Muon_pfRelIso03_all",                                                            &Muon_pfRelIso03_all_);
	reader_muon->AddVariable("Muon_miniPFRelIso_chg",                                                          &Muon_miniPFRelIso_chg_);
	reader_muon->AddVariable("Muon_miniRelIsoNeutral := Muon_miniPFRelIso_all - Muon_miniPFRelIso_chg",        &Muon_miniRelIsoNeutral_);
	reader_muon->AddVariable("Muon_jetNDauCharged",                                                            &Muon_jetNDauCharged_);
	reader_muon->AddVariable("Muon_jetPtRelv2",                                                                &Muon_jetPtRelv2_);
	reader_muon->AddVariable("Muon_jetPtRatio := min(1 / (1 + Muon_jetRelIso), 1.5)",                          &Muon_jetPtRatio_);
	reader_muon->AddVariable("Muon_jetBTagDeepFlavB := Muon_jetIdx > -1 ? Jet_btagDeepFlavB[Muon_jetIdx] : 0", &Muon_jetBTagDeepFlavB_);
	reader_muon->AddVariable("Muon_sip3d",                                                                     &Muon_sip3d_);
	reader_muon->AddVariable("Muon_log_dxy := log(abs(Muon_dxy))",                                             &Muon_log_dxy_);
	reader_muon->AddVariable("Muon_log_dz  := log(abs(Muon_dz))",                                              &Muon_log_dz_);
	reader_muon->AddVariable("Muon_segmentComp",                                                               &Muon_segmentComp_);
	
	reader_muon->BookMVA(BDT_name_muon, xml_file_name_muon);
	
  }
  
  ttH_MVA_reader::~ttH_MVA_reader(){
	
	std::cout << "Deleting reader" << std::endl;
	
	reader_electron->Delete();
	reader_muon->Delete();
  }

#endif
