#ifndef EMBEDED_NORM
#define EMBEDED_NORM

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

class EmbededNormalization{
public:

  std::unique_ptr<correction::CorrectionSet> csetNorm;
  correction::Correction::Ref cset_muon_trig;
  correction::Correction::Ref cset_muon_normId;

  std::unique_ptr<correction::CorrectionSet> csetNorm_mu;
  std::unique_ptr<correction::CorrectionSet> csetNorm_ele;

  std::unique_ptr<correction::CorrectionSet> csetNorm_mu_tau;
  std::unique_ptr<correction::CorrectionSet> csetNorm_ele_tau;
  
  correction::Correction::Ref cset_muon_iso;
  correction::Correction::Ref cset_muon_id;
  correction::Correction::Ref cset_ele_iso;
  correction::Correction::Ref cset_ele_id;

  EmbededNormalization(string year) {

    if (year == "2018UL"){

      csetNorm = correction::CorrectionSet::from_file("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/DY_Embedded/embeddingselection_2018UL.json");

      cset_muon_trig = (correction::Correction::Ref) csetNorm->at("m_sel_trg_kit_ratio");
      cset_muon_normId = (correction::Correction::Ref) csetNorm->at("EmbID_pt_eta_bins");
      
      csetNorm_mu = correction::CorrectionSet::from_file("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/DY_Embedded/scale_factors_Muon_2018.json");
      csetNorm_ele = correction::CorrectionSet::from_file("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/DY_Embedded/scale_factors_EGamma_2018.json");
      
      csetNorm_mu_tau = correction::CorrectionSet::from_file("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/DY_Embedded/muon_2018UL.json");
      csetNorm_ele_tau = correction::CorrectionSet::from_file("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/DY_Embedded/electron_2018UL.json");
      
      cset_muon_id = (correction::Correction::Ref) csetNorm_mu_tau->at("ID_pt_eta_bins");
      cset_muon_iso  = (correction::Correction::Ref) csetNorm_mu->at("MuIso");
      
      cset_ele_id = (correction::Correction::Ref) csetNorm_ele_tau->at("ID90_pt_eta_bins");
      cset_ele_iso  = (correction::Correction::Ref) csetNorm_ele->at("EleIso");
    
    }else if(year == "2017UL"){

      csetNorm = correction::CorrectionSet::from_file("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/DY_Embedded/embeddingselection_2017UL.json");

      cset_muon_trig = (correction::Correction::Ref) csetNorm->at("m_sel_trg_kit_ratio");
      cset_muon_normId = (correction::Correction::Ref) csetNorm->at("EmbID_pt_eta_bins");

      csetNorm_mu = correction::CorrectionSet::from_file("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/DY_Embedded/scale_factors_Muon_2017.json");
      csetNorm_ele = correction::CorrectionSet::from_file("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/DY_Embedded/scale_factors_EGamma_2017.json");

      csetNorm_mu_tau = correction::CorrectionSet::from_file("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/DY_Embedded/muon_2017UL.json");
      csetNorm_ele_tau = correction::CorrectionSet::from_file("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/DY_Embedded/electron_2017UL.json");

      cset_muon_id = (correction::Correction::Ref) csetNorm_mu_tau->at("ID_pt_eta_bins");
      cset_muon_iso  = (correction::Correction::Ref) csetNorm_mu->at("MuIso");

      cset_ele_id = (correction::Correction::Ref) csetNorm_ele_tau->at("ID90_pt_eta_bins");
      cset_ele_iso  = (correction::Correction::Ref) csetNorm_ele->at("EleIso");
      
    }else if (year == "2016UL_noHIPM"){

      csetNorm = correction::CorrectionSet::from_file("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/DY_Embedded/embeddingselection_2016postVFPUL.json");

      cset_muon_trig = (correction::Correction::Ref) csetNorm->at("m_sel_trg_kit_ratio");
      cset_muon_normId = (correction::Correction::Ref) csetNorm->at("EmbID_pt_eta_bins");

      csetNorm_mu = correction::CorrectionSet::from_file("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/DY_Embedded/scale_factors_Muon_2016.json");
      csetNorm_ele = correction::CorrectionSet::from_file("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/DY_Embedded/scale_factors_EGamma_2016.json");

      csetNorm_mu_tau = correction::CorrectionSet::from_file("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/DY_Embedded/muon_2016postVFPUL.json");
      csetNorm_ele_tau = correction::CorrectionSet::from_file("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/DY_Embedded/electron_2016postVFPUL.json");

      cset_muon_id = (correction::Correction::Ref) csetNorm_mu_tau->at("ID_pt_eta_bins");
      cset_muon_iso  = (correction::Correction::Ref) csetNorm_mu->at("MuIso");

      cset_ele_id = (correction::Correction::Ref) csetNorm_ele_tau->at("ID90_pt_eta_bins");
      cset_ele_iso  = (correction::Correction::Ref) csetNorm_ele->at("EleIso");
      
    }else if (year == "2016UL_HIPM"){

      csetNorm = correction::CorrectionSet::from_file("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/DY_Embedded/embeddingselection_2016preVFPUL.json");

      cset_muon_trig = (correction::Correction::Ref) csetNorm->at("m_sel_trg_kit_ratio");
      cset_muon_normId = (correction::Correction::Ref) csetNorm->at("EmbID_pt_eta_bins");

      csetNorm_mu = correction::CorrectionSet::from_file("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/DY_Embedded/scale_factors_Muon_2016-HIPM.json");
      csetNorm_ele = correction::CorrectionSet::from_file("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/DY_Embedded/scale_factors_EGamma_2016-HIPM.json");

      csetNorm_mu_tau = correction::CorrectionSet::from_file("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/DY_Embedded/muon_2016preVFPUL.json");
      csetNorm_ele_tau = correction::CorrectionSet::from_file("/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/examples/extended/DY_Embedded/electron_2016preVFPUL.json");

      cset_muon_id = (correction::Correction::Ref) csetNorm_mu_tau->at("ID_pt_eta_bins");
      cset_muon_iso  = (correction::Correction::Ref) csetNorm_mu->at("MuIso");

      cset_ele_id = (correction::Correction::Ref) csetNorm_ele_tau->at("ID90_pt_eta_bins");
      cset_ele_iso  = (correction::Correction::Ref) csetNorm_ele->at("EleIso");

    }
  }

  float operator()(RVecF GenPart_pt, RVecF GenPart_eta, RVecF GenPart_phi, RVecF GenPart_pdgId, RVecI GenPart_genPartIdxMother, RVecF Lepton_pt, RVecF Lepton_eta, RVecF Lepton_phi, RVecI Lepton_pdgId, RVecI Lepton_muonIdx, RVecI Lepton_electronIdx, RVecI Muon_genPartIdx, RVecI Electron_genPartIdx){

    float embed_norm = 1.0;
    int itau = 0;
    
    float gt_1_pt = -99.9;
    float gt_1_eta = -99.9;
    float gt_2_pt = -99.9;
    float gt_2_eta = -99.9;
    
    for (unsigned int i=0; i<GenPart_pt.size(); i++){
      if (abs(GenPart_pdgId[i])==15){
	if (itau == 0){
	  gt_1_pt = GenPart_pt[i];
	  gt_1_eta = GenPart_eta[i];
	  embed_norm *= cset_muon_normId->evaluate({gt_1_pt, abs(gt_1_eta)});
	}else if (itau == 1){
	  gt_2_pt = GenPart_pt[i];
	  gt_2_eta = GenPart_eta[i];
	  embed_norm *= cset_muon_normId->evaluate({gt_2_pt, abs(gt_2_eta)});
	}else{
	  continue;
	}
	itau++;
      }
    }
    
    embed_norm *= cset_muon_trig->evaluate({gt_1_pt, abs(gt_1_eta), gt_2_pt, abs(gt_2_eta)});
    
    float mu_sf_id = 1.0;
    float mu_sf_iso = 1.0;
    float mu_sf_hlt = 1.0;
    
    float ele_sf_id = 1.0;
    float ele_sf_iso = 1.0;
    float ele_sf_hlt = 1.0;
    
    float lep_pt1 = 0.0;
    float lep_pt2 = 0.0;
    
    lep_pt1 = Lepton_pt[0]>10 ? Lepton_pt[0] : 10.01;
    lep_pt2 = Lepton_pt[1]>10 ? Lepton_pt[1] : 10.01;
    
    lep_pt1 = lep_pt1<100 ? lep_pt1 : 199.9;
    lep_pt2 = lep_pt2<100 ? lep_pt2 : 199.9;
    
    float lep_eta1 = 0.0;
    float lep_eta2 = 0.0;
    
    if (abs(Lepton_pdgId[0]) == 13){      
      lep_eta1 = Lepton_eta[0]<2.4 ? Lepton_eta[0] : 2.39;
      lep_eta1 = lep_eta1>-2.4 ? lep_eta1 : -2.39;
      
      mu_sf_id  = cset_muon_id->evaluate({lep_eta1, lep_pt1, "emb"});
      mu_sf_iso = cset_muon_iso->evaluate({lep_eta1, lep_pt1, "nominal"});
    }else{
      ele_sf_id  = cset_ele_id->evaluate({Lepton_eta[1], lep_pt2, "emb"});
      ele_sf_iso = cset_ele_iso->evaluate({Lepton_eta[1], lep_pt2, "nominal"});
    }
    
    if (abs(Lepton_pdgId[0]) == 11){
      ele_sf_id  = cset_ele_id->evaluate({Lepton_eta[0], lep_pt1, "emb"});
      ele_sf_iso = cset_ele_iso->evaluate({Lepton_eta[0], lep_pt1, "nominal"});
    }else{
      lep_eta2 = Lepton_eta[1]<2.4 ? Lepton_eta[1] : 2.39;
      lep_eta2 = lep_eta2>-2.4 ? lep_eta2 : -2.39;
      
      mu_sf_id  = cset_muon_id->evaluate({lep_eta2, lep_pt2, "emb"});
      mu_sf_iso = cset_muon_iso->evaluate({lep_eta2, lep_pt2, "nominal"});
    }
    
    if (mu_sf_iso>0)
      embed_norm *= mu_sf_iso;
    if (mu_sf_id>0)
      embed_norm *= mu_sf_id;
    if (ele_sf_iso>0)
      embed_norm *= ele_sf_iso;
    if (ele_sf_id>0)
      embed_norm *= ele_sf_id;    
    //embed_norm = embed_norm * mu_sf_iso * mu_sf_id * ele_sf_iso * ele_sf_id;        

    return embed_norm;        
  }
};

#endif
