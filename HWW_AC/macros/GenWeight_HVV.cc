
#ifndef GENWEIGHT
#define GENWEIGHT

#include "Mela.h"
#include "GenTools.h"

// Production + decay MEs for HWW AC sample reweighting

class GENWEIGHT_HVV{
public:

  string sig;
  string hyp1;
  string hyp2;
  string type;

  int   nLHEPart, nGenPart;
  RVecF LHEPart_pt, LHEPart_eta, LHEPart_phi;
  RVecF GenPart_pt, GenPart_eta, GenPart_phi;
  RVecI LHEPart_pdgId, LHEPart_status;
  RVecI GenPart_pdgId, GenPart_genPartIdxMother;
  float Generator_x1, Generator_x2;
  int   Generator_id1, Generator_id2;

  Mela* mela;
  Double_t LHCsqrts_= 13.6, mh_= 125.;
  TVar::VerbosityLevel verbosity_ = TVar::SILENT;
  TVar::MatrixElement me_ = TVar::JHUGen;

  float cw  = 0.8768;
  float sw  = 0.4808;
  float mZ  = 91.2;
  float mZ2  = mZ*mZ;
  float L = 100.0;
  float L2 = L*L;
  float csw = cw*cw-sw*sw;

  float GetHVVME(string sig, string hyp, string type, TVar::Production Prod){

    float me = -999;

    if(type == "AC"){ // MC sample hypotheses

     if(hyp.find("f05") != string::npos) hyp = sig+"_"+hyp;
     if(hyps_AC.find(hyp) == hyps_AC.end()){
      cerr << "SOMETHING WENT WRONG! Hypothesis not present in AC map : "<< hyp << endl;
      return -1;
     }
     RVecF a_h = hyps_AC.find(hyp)->second;
     me = GetHVVME_AC(a_h, Prod);

    }else{ // various coupling/vertex types used in SMEFT analysis

     std::map<std::string, RVecF> hyps_cv;
     
     if     (type == "8C2V")  hyps_cv = hyps_8C2V;
     else if(type == "8C1V")  hyps_cv = hyps_8C1V;
     else if(type == "4C2V")  hyps_cv = hyps_4C2V;  
     else if(type == "4C1V")  hyps_cv = hyps_4C1V; 
     else{
      std::cerr<< "SOMETHING WENT WRONG!, Type "+type+" is not supported "<<std::endl;
      return -1;
     }

     if(hyps_cv.find(hyp) == hyps_cv.end()){
      cerr << "SOMETHING WENT WRONG! Hypothesis not present in "+type+" map : "<< hyp << endl;
      return -1;
     } 
     RVecF a_h = hyps_cv.find(hyp)->second;
     if(type.find("4C") != std::string::npos) a_h.insert(a_h.end(), 4, 0.0f); // Adding 4 zeros for Zg/gg 
     me = GetHVVME_SMEFT(a_h, Prod);

    }

    return me;
  }

  //-> HVV gen level MEs - 9 couplings assuming a_ZZ = a_WW (AC approach)
  float GetHVVME_AC(RVecF coups, TVar::Production Prod){

    float me = -999;

    mela->setProcess(TVar::SelfDefine_spin0, me_, Prod);
    mela->differentiate_HWW_HZZ=false;
    mela->selfDHzzcoupl[0][gHIGGS_VV_1][0]       = coups[0]; //a1      - HSMHiggs
    mela->selfDHzzcoupl[0][gHIGGS_VV_2][0]       = coups[1]; //a2      - H0hplus
    mela->selfDHzzcoupl[0][gHIGGS_VV_4][0]       = coups[2]; //a3      - H0minus
    mela->selfDHzzcoupl[0][gHIGGS_VV_1_PRIME2][0]= coups[3]; //k1      - H0_g1prime2
    mela->selfDHzzcoupl[0][gHIGGS_ZA_1_PRIME2][0]= coups[4]; //k2Zg    - H0_Zgsg1prime2
    mela->selfDHzzcoupl[0][gHIGGS_ZA_2][0]       = coups[5]; //a2Zg    - H0_Zgs
    mela->selfDHzzcoupl[0][gHIGGS_ZA_4][0]       = coups[6]; //a3Zg    - H0_Zgs_PS
    mela->selfDHzzcoupl[0][gHIGGS_AA_2][0]       = coups[7]; //a2gg    - H0_gsgs
    mela->selfDHzzcoupl[0][gHIGGS_AA_4][0]       = coups[8]; //a3gg    - H0_gsgs_PS

    if(Prod==TVar::ZZINDEPENDENT)mela->computeP(me, false);
    else                         mela->computeProdP(me, false);

    return me;
  }

  //-> HVV gen level MEs - 8 couplings assuming a_ZZ and a_WW SMEFT relationships (k2Zg not independent)
  float GetHVVME_SMEFT(RVecF coups, TVar::Production Prod){

    float me = -999;

    float a1   = coups[0];
    float a2   = coups[1];
    float a3   = coups[2];
    float k1   = coups[3];
    float a2Zg = coups[4];
    float a3Zg = coups[5];
    float a2gg = coups[6];
    float a3gg = coups[7];

    float a1WW = a1;
    float a2WW = cw*cw*a2 + sw*sw*a2gg + 2*sw*cw*a2Zg;
    float a3WW = cw*cw*a3 + sw*sw*a3gg + 2*sw*cw*a3Zg;
    float k1WW = k1/csw + 2*sw*sw*L2*(a2gg-a2)/(mZ2*csw) + 2*L2*(sw/cw)*(a2Zg/mZ2);
    float k2Zg = 2*sw*cw*k1/csw + 2*sw*cw*L2*(a2gg-a2)/(mZ2*csw) + 2*L2*(a2Zg/mZ2);

    mela->setProcess(TVar::SelfDefine_spin0, me_, Prod);
    mela->differentiate_HWW_HZZ=true;
    mela->selfDHzzcoupl[0][gHIGGS_VV_1][0]       = a1;
    mela->selfDHwwcoupl[0][gHIGGS_VV_1][0]       = a1WW;
    mela->selfDHzzcoupl[0][gHIGGS_VV_2][0]       = a2;
    mela->selfDHwwcoupl[0][gHIGGS_VV_2][0]       = a2WW;
    mela->selfDHzzcoupl[0][gHIGGS_VV_4][0]       = a3;
    mela->selfDHwwcoupl[0][gHIGGS_VV_4][0]       = a3WW;
    mela->selfDHzzcoupl[0][gHIGGS_VV_1_PRIME2][0]= k1;
    mela->selfDHwwcoupl[0][gHIGGS_VV_1_PRIME2][0]= k1WW;
    mela->selfDHzzcoupl[0][gHIGGS_ZA_1_PRIME2][0]= k2Zg;
    mela->selfDHzzcoupl[0][gHIGGS_ZA_2][0]       = a2Zg;
    mela->selfDHzzcoupl[0][gHIGGS_ZA_4][0]       = a3Zg;
    mela->selfDHzzcoupl[0][gHIGGS_AA_2][0]       = a2gg;
    mela->selfDHzzcoupl[0][gHIGGS_AA_4][0]       = a3gg;

    if(Prod==TVar::ZZINDEPENDENT)mela->computeP(me, false);
    else                         mela->computeProdP(me, false);

    return me;

  }

  GENWEIGHT_HVV(){
    mela = new Mela(LHCsqrts_, mh_, verbosity_);
  }

  float operator()(const char* _sig, const char* _hyp1, const char* _hyp2, const char* _type,
		   int _nLHEPart, int _nGenPart,
		   RVecF _LHEPart_pt, RVecF _LHEPart_eta, RVecF _LHEPart_phi, RVecI _LHEPart_pdgId, RVecI _LHEPart_status,
		   RVecF _GenPart_pt, RVecF _GenPart_eta, RVecF _GenPart_phi, RVecI _GenPart_pdgId, RVecI _GenPart_genPartIdxMother,
		   float _Generator_x1, float _Generator_x2, int _Generator_id1, int _Generator_id2) {

    std::stringstream sigst;
    sigst << _sig;
    sig = sigst.str();

    std::stringstream hyp1st;
    hyp1st << _hyp1;
    hyp1 = hyp1st.str();

    std::stringstream hyp2st;
    hyp2st << _hyp2;
    hyp2 = hyp2st.str();

    std::stringstream typest;
    typest << _type;
    type = typest.str();

    nLHEPart = _nLHEPart;
    nGenPart = _nGenPart;
    LHEPart_pt = _LHEPart_pt; LHEPart_eta = _LHEPart_eta; LHEPart_phi = _LHEPart_phi;
    GenPart_pt = _GenPart_pt; GenPart_eta = _GenPart_eta; GenPart_phi = _GenPart_phi;
    LHEPart_pdgId = _LHEPart_pdgId; LHEPart_status = _LHEPart_status;
    GenPart_pdgId = _GenPart_pdgId; GenPart_genPartIdxMother = _GenPart_genPartIdxMother;
    Generator_x1 = _Generator_x1; Generator_id1 = _Generator_id1;
    Generator_x2 = _Generator_x2; Generator_id2 = _Generator_id2;

    std::vector<int> HDecay_Idx;
    for(int i = 0; i < nGenPart; i++){ // Get Index of 4 H->WW decay particles (Gen level)

     if (TMath::Abs(GenPart_pdgId[i]) >= 21) continue;
     int mi = GenPart_genPartIdxMother[i];
     if (mi == -1) continue;
     if (TMath::Abs(GenPart_pdgId[mi]) != 24) continue;
     if (FromH(i, GenPart_genPartIdxMother, GenPart_pdgId) == false) continue;

     HDecay_Idx.push_back(i);
    }

    if(HDecay_Idx.size() != 4) HDecay_Idx = RemoveGammaW(HDecay_Idx, GenPart_pdgId, GenPart_genPartIdxMother);
    if(HDecay_Idx.size() != 4) HDecay_Idx = RemoveAddHadron(HDecay_Idx, GenPart_genPartIdxMother);

    std::map<int, std::vector<float>> HDecay_LHE = getLHE(HDecay_Idx, GenPart_pt, GenPart_eta, GenPart_phi, GenPart_pdgId, nLHEPart, LHEPart_pt, LHEPart_eta, LHEPart_phi, LHEPart_status, LHEPart_pdgId, "all");
    
    if(HDecay_LHE.size()!=4){
      std::cout<< "SOMETHING WENT WRONG!, WW final state "<< HDecay_LHE.size() <<std::endl;
      for(auto pLHE: HDecay_LHE){std::cout<< pLHE.second[0] <<" "<< pLHE.second[1] <<" "<< pLHE.second[2] <<" "<< pLHE.second[3] <<std::endl;}
    }
    
    std::vector<TLorentzVector> daughters;
    std::vector<int> daughters_Id;
    
    for(auto pLHE: HDecay_LHE){

     if(abs(pLHE.second[3])<10 && sig == "vbf")continue; // VBF HWW->2l2nu :
     // this will catch the 1 event in VBF H0L1 with u&s quarks
      
     TLorentzVector d;
     float mass = 0;
     if(std::abs(pLHE.second[3])==11) mass = 0.0005;
     if(std::abs(pLHE.second[3])==13) mass = 0.106;
     if(std::abs(pLHE.second[3])==15) mass = 1.77686; 
     d.SetPtEtaPhiM(pLHE.second[0], pLHE.second[1], pLHE.second[2], mass);
     
     daughters.push_back(d);
     daughters_Id.push_back(pLHE.second[3]);  
    }

    if(daughters.size()!=4){std::cout<< "SOMETHING WENT WRONG!, WW daughters "<< daughters.size() <<std::endl;}
    
    std::vector<TLorentzVector> mothers;
    std::vector<int> mothers_Id;

    TLorentzVector incoming1;
    TLorentzVector incoming2;
    incoming1.SetPxPyPzE(0.,0., Generator_x1*6800, Generator_x1*6800);
    incoming2.SetPxPyPzE(0.,0.,-1*Generator_x2*6800, Generator_x2*6800);
    mothers.push_back(incoming1);
    mothers.push_back(incoming2);
    mothers_Id.push_back(Generator_id1);
    mothers_Id.push_back(Generator_id2);

    std::vector<TLorentzVector> associated;
    std::vector<int> associated_Id;
    TVar::Production prodM;

    if(sig == "zh" || sig == "wh"){ // associated production information

     std::vector<int> Assoc_Idx;
     for(int i = 0; i < nGenPart; i++){
      int p_Id = TMath::Abs(GenPart_pdgId[i]);
      if(p_Id >= 21) continue;
      if(FromH(i, GenPart_genPartIdxMother, GenPart_pdgId) == true) continue;
      int mi = GenPart_genPartIdxMother[i];
      if(mi == -1) continue;

      if(TMath::Abs(GenPart_pdgId[mi]) == 23 && sig == "zh"){
       Assoc_Idx.push_back(i);
       if(p_Id > 0 && p_Id < 6)        prodM = TVar::Had_ZH;
       else if(p_Id > 10 && p_Id < 19) prodM = TVar::Lep_ZH;

      }else if(TMath::Abs(GenPart_pdgId[mi]) == 24 && sig == "wh"){
       Assoc_Idx.push_back(i);
       if(p_Id > -1 && p_Id < 6)       prodM = TVar::Had_WH;
       else if(p_Id > 10 && p_Id < 19) prodM = TVar::Lep_WH;
      }
     }

     if(Assoc_Idx.size() != 2 && sig == "wh") Assoc_Idx = RemoveGammaW(Assoc_Idx, GenPart_pdgId, GenPart_genPartIdxMother);
     if(Assoc_Idx.size() != 2)                Assoc_Idx = RemoveAddHadron(Assoc_Idx, GenPart_genPartIdxMother);

     std::map<int, std::vector<float>> Assoc_LHE = getLHE(Assoc_Idx, GenPart_pt, GenPart_eta, GenPart_phi, GenPart_pdgId, nLHEPart, LHEPart_pt, LHEPart_eta, LHEPart_phi, LHEPart_status, LHEPart_pdgId, "all");
     if(Assoc_LHE.size()!=2) std::cout<< "SOMETHING WENT WRONG!, VH final state "<< Assoc_LHE.size() <<std::endl;

     for(auto pLHE: Assoc_LHE){
      TLorentzVector a;
      a.SetPtEtaPhiM(pLHE.second[0], pLHE.second[1], pLHE.second[2], 0.0);
      associated.push_back(a);
      associated_Id.push_back(pLHE.second[3]);
     }
    }else if(sig == "vbf"){

     std::vector<int> LHEPart_Idx;
     prodM = TVar::JJVBF;

     for(int i = 0; i < nLHEPart; i++){
      int p_Id = TMath::Abs(LHEPart_pdgId[i]);
      if(((p_Id > 0 && p_Id < 6) ||p_Id==21) && LHEPart_status[i]==1) LHEPart_Idx.push_back(i);
     }
     
     LHEPart_Idx = pTorder(LHEPart_Idx, LHEPart_pt);
     if(LHEPart_Idx.size()!=2) std::cout<< "SOMETHING WENT WRONG!, VBF final state "<< LHEPart_Idx.size() <<std::endl;

     for(int ij: LHEPart_Idx){
      TLorentzVector j;
      j.SetPtEtaPhiM(LHEPart_pt[ij], LHEPart_eta[ij], LHEPart_phi[ij], 0.0);
      associated.push_back(j);
      associated_Id.push_back(LHEPart_pdgId[ij]);
     }
    }

    SimpleParticleCollection_t daughters_coll;
    SimpleParticleCollection_t associated_coll;
    SimpleParticleCollection_t mothers_coll;

    for(size_t i = 0; i < daughters.size(); ++i){  daughters_coll.push_back( SimpleParticle_t(daughters_Id[i], daughters[i])); }
    for(size_t i = 0; i < associated.size(); ++i){ associated_coll.push_back(SimpleParticle_t(associated_Id[i], associated[i])); }
    for(size_t i = 0; i < mothers.size(); ++i){    mothers_coll.push_back(   SimpleParticle_t(mothers_Id[i], mothers[i])); }

    mela->setCandidateDecayMode(TVar::CandidateDecay_WW);
    mela->setInputEvent(&daughters_coll, &associated_coll, &mothers_coll, 1);
    mela->setCurrentCandidateFromIndex(0);

    // get MEs and calculate weight //

    float weight;

    TVar::Production decayM = TVar::ZZINDEPENDENT;
    float dme_h1 = GetHVVME(sig, hyp1, "AC", decayM);
    float dme_h2 = GetHVVME(sig, hyp2, type, decayM);

    weight = dme_h2/dme_h1; 
      
    if(std::isnan(dme_h1)) std::cout<< "SOMETHING WENT WRONG?, Decay ME is nan " <<std::endl;

    if(sig == "vbf" || sig == "zh" || sig == "wh"){

     float pme_h1 = GetHVVME(sig, hyp1, "AC", prodM);
     float pme_h2 = GetHVVME(sig, hyp2, type, prodM);

     weight = (dme_h2*pme_h2)/(dme_h1*pme_h1);
     
     if(std::isnan(pme_h1)) std::cout<< "SOMETHING WENT WRONG?, Prod ME is nan " <<std::endl;
    }
    
    mela->resetInputEvent();
    return weight;

  }
};

#endif
