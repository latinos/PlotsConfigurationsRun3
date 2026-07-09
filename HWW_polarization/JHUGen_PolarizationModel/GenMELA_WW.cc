#include "TLorentzVector.h"

#include <iostream>
#include "ROOT/RVec.hxx"

#include "/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/MelaAnalytics/EventContainer/interface/MELAEvent.h"
#include "/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/IvyFramework/IvyAutoMELA/interface/IvyMELAHelpers.h"
#include "/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/JHUGenMELA/MELA/interface/PDGHelpers.h"
#include "/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/JHUGenMELA/MELA/interface/TUtil.hh"
#include "/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/MelaAnalytics/EventContainer/interface/HiggsComparators.h"
#include "/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/MelaAnalytics/EventContainer/interface/TopComparators.h"
#include "/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/MelaAnalytics/CandidateLOCaster/interface/MELACandidateRecaster.h"
#include "/eos/user/s/sblancof/Run2Analysis/mkShapesRDF/JHUGenMELA/MELA/interface/Mela.h"

#include <vector>
#include <string>
#include <cstdio>
#include <cmath>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>

#include "Mela.h"
#include "ZZMatrixElement.h"
#include "VectorPdfFactory.h"
#include "TensorPdfFactory.h"
#include "RooqqZZ_JHU_ZgammaZZ_fast.h"
#include "RooqqZZ_JHU.h"
#include "SuperMELA.h"
#include "TUtilHelpers.hh"
#include "MELAStreamHelpers.hh"

#include "RooMsgService.h"
#include "TFile.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TH3F.h"
#include "TGraph.h"
#include "TSpline.h"
#include "TString.h"

using namespace RooFit;
using MELAStreamHelpers::MELAout;
using MELAStreamHelpers::MELAerr;

using namespace ROOT;
using namespace ROOT::VecOps;
using namespace std;
using LorentzVectorM = ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float>>;


class GEN_POLARIZATION{
public:
  
  int nLHEPart;
  RVecF LHEPart_pt;
  RVecF LHEPart_eta;
  RVecF LHEPart_phi;
  RVecF LHEPart_mass;
  RVecI LHEPart_incomingpz;
  RVecI LHEPart_pdgId;
  RVecI LHEPart_status;
  RVecI LHEPart_spin;

  RVecI GenPart_genPartIdxMother;
  RVecI GenPart_pdgId;
  RVecI GenPart_status;
  RVecF GenPart_pt;
  RVecF GenPart_eta;
  RVecF GenPart_phi;
  RVecF GenPart_mass;

  float Generator_x1;
  float Generator_x2;
  int Generator_id1;
  int Generator_id2;

  bool recast();
  
  MELAEvent::CandidateVVMode VVMode;
  bool isGen;
  int VVDecayMode;

  double LHCsqrts;
  double mh;
  TVar::VerbosityLevel myVerbosity_;
  Mela* mela;

  float M_Z = 91.1876;
  float M_W = 80.399;
  float M_H = 125.0;
  float Gf = 1.16639e-5;
  float vev = 1.0 / sqrt(Gf*sqrt(2.0));
  float gwsq = 4.0 * M_W*M_W / (vev*vev);  
  
  float a1 = M_Z*M_Z/(vev*vev);
  float a2;
  float fL; 
  
  GEN_POLARIZATION(float f_L){

    VVMode = MELAEvent::getCandidateVVModeFromString("WW");
    isGen = true;
    VVDecayMode = 0; // For both ggH and VBF

    LHCsqrts = 13.6;
    mh = 125.0;
    myVerbosity_ = TVar::SILENT; //TVar::DEBUG; TVar::SILENT

    mela = new Mela(LHCsqrts, mh, myVerbosity_);

    fL = f_L;
    if (f_L == 1.0) {
      a1 = 0.0;
    }
    
  }

  std::vector<RVecF> operator()(int _nLHEPart,
				RVecF _LHEPart_pt,
				RVecF _LHEPart_eta,
				RVecF _LHEPart_phi,
				RVecF _LHEPart_mass,
				RVecI _LHEPart_incomingpz,
				RVecI _LHEPart_pdgId,
				RVecI _LHEPart_status,
				RVecI _LHEPart_spin,
				RVecI _GenPart_genPartIdxMother,
				RVecI _GenPart_pdgId,
				RVecI _GenPart_status,
				RVecF _GenPart_pt,
				RVecF _GenPart_eta,
				RVecF _GenPart_phi,
				RVecF _GenPart_mass,
				float _Generator_x1,
				float _Generator_x2,
				int _Generator_id1,
				int _Generator_id2) {
    
    Generator_x1 = _Generator_x1;
    Generator_x2 = _Generator_x2;

    Generator_id1 = _Generator_id1;
    Generator_id2 = _Generator_id2;

    nLHEPart = _nLHEPart;
    LHEPart_pt = _LHEPart_pt;
    LHEPart_eta = _LHEPart_eta;
    LHEPart_phi = _LHEPart_phi;
    LHEPart_mass = _LHEPart_mass;
    LHEPart_incomingpz = _LHEPart_incomingpz;
    LHEPart_pdgId = _LHEPart_pdgId;
    LHEPart_status = _LHEPart_status;
    LHEPart_spin = _LHEPart_spin;

    GenPart_genPartIdxMother = _GenPart_genPartIdxMother;
    GenPart_pdgId = _GenPart_pdgId;
    GenPart_status = _GenPart_status;
    GenPart_pt = _GenPart_pt;
    GenPart_eta = _GenPart_eta;
    GenPart_phi = _GenPart_phi;
    GenPart_mass = _GenPart_mass;

    //std::cout << "" << std::endl;
    //std::cout << "New event ---------------------" << std::endl;
    //std::cout << "" << std::endl;
    
    std::vector<MELAParticle> melaParticlesList;

    std::vector<TLorentzVector> incoming;
    std::vector<int> incomingIDs;
    std::vector<TLorentzVector>	outgoing;
    std::vector<int> outgoingIDs;

    TLorentzVector Higgs;
    bool first = true;
    bool areLeptons = false;
    
    for (int p = 0; p < nLHEPart; p++){
      TLorentzVector tmp;
      if (LHEPart_status[p] == 1){ // outgoing

	//cout << "Is stable!" << endl;
	//cout << LHEPart_pdgId[p] << endl;
	//cout << LHEPart_mass[p] << endl;

	if (abs(LHEPart_pdgId[p])>=11 && abs(LHEPart_pdgId[p])<=16){
	  areLeptons = true;
	}
	
	tmp.SetPtEtaPhiM(LHEPart_pt[p], LHEPart_eta[p], LHEPart_phi[p], LHEPart_mass[p]);
	if (first && abs(LHEPart_pdgId[p])<17 && abs(LHEPart_pdgId[p])>10){
	  Higgs = tmp;
	  first = false;
	}else if (abs(LHEPart_pdgId[p])<17 && abs(LHEPart_pdgId[p])>10){
	  Higgs = Higgs + tmp;
	}
	outgoing.push_back(tmp);
	outgoingIDs.push_back(LHEPart_pdgId[p]);
      }else if(LHEPart_status[p] == -1){

	//cout <<	"Is unstable!" << endl;
	//cout <<	LHEPart_pdgId[p] << endl;
	//cout << LHEPart_incomingpz[p] << endl;

	tmp.SetPxPyPzE(0.0, 0.0, LHEPart_incomingpz[p], abs(LHEPart_incomingpz[p]));
        incoming.push_back(tmp);
        incomingIDs.push_back(LHEPart_pdgId[p]);
      }      
    }
    
    SimpleParticle_t tempPart;
    MELAParticle tempMela;

    for (int idx=0; idx<outgoing.size(); idx++){
      tempPart = SimpleParticle_t(outgoingIDs[idx], outgoing[idx]);
      tempMela = MELAParticle(tempPart.first, tempPart.second);
      tempMela.setGenStatus(1);
      melaParticlesList.push_back(tempMela);
    }

    for	(int idx=0; idx<incoming.size(); idx++){
      tempPart = SimpleParticle_t(incomingIDs[idx], incoming[idx]);
      tempMela = MELAParticle(tempPart.first, tempPart.second);
      tempMela.setGenStatus(-1);
      melaParticlesList.push_back(tempMela);
    }
    
    MELAEvent* LHEEvent = new MELAEvent();
    std::vector<MELAParticle> writtenGenCands;
    std::vector<MELAParticle> writtenGenTopCands;
    bool ThereIsHiggs = false;

    for (auto& part : melaParticlesList){
      if (part.genStatus == -1){
	LHEEvent->addMother(&part);
      }else{
	if (PDGHelpers::isALepton(part.id)){
	  LHEEvent->addLepton(&part);
	}else if(PDGHelpers::isANeutrino(part.id)){
	  LHEEvent->addNeutrino(&part);
	}else if(PDGHelpers::isAKnownJet(part.id) && PDGHelpers::isATopQuark(part.id) == false){
	  LHEEvent->addJet(&part);
	}else if(PDGHelpers::isAPhoton(part.id)){
	  LHEEvent->addPhoton(&part);
	}else if(PDGHelpers::isAHiggs(part.id)){
	  writtenGenCands.push_back(part);
	  ThereIsHiggs = true;
	  if (VVMode==MELAEvent::UndecayedMode && (part.genStatus==1 || part.genStatus==2)){
	    LHEEvent->addIntermediate(&part);
	  }
	}else if(PDGHelpers::isATopQuark(part.id)){
	  writtenGenTopCands.push_back(part);
	  if (part.genStatus==1){
	    LHEEvent->addIntermediate(&part);
	  }
	}else{
	  cout << "FATAL: UNIDENTIFIED PARTICLE IN THE FINAL STATE" << endl;
	  cout << "ID: " << part.id << endl;
	}
      }
    }

    LHEEvent->constructTopCandidates();

    std::vector<MELATopCandidate_t*> matchedTops;
    for (auto& writtenGenTopCand : writtenGenTopCands){
      MELATopCandidate_t* tmpCand = TopComparators::matchATopToParticle(*LHEEvent, &writtenGenTopCand);
      if (tmpCand){
	matchedTops.push_back(tmpCand);
      }
    }
    for (auto& tmpCand : LHEEvent->getTopCandidates()){
      if (std::find(matchedTops.begin(), matchedTops.end(), tmpCand) != matchedTops.end()){
	tmpCand->setSelected(false);
      }
    }
    
    LHEEvent->constructVVCandidates(VVMode, VVDecayMode);
    LHEEvent->addVVCandidateAppendages();
    
    bool ThereIsCand = false;
    MELACandidate* genCand;

    bool doVBF = false;
    bool gluonsIn = false;
    std::vector<MELAParticle*> LHEmothers = LHEEvent->getMothers();
    for (auto& part : LHEmothers){
      if (part->id!=21)
	doVBF = true;
      if (part->id==21)
	gluonsIn = true;
    }
    
    if (ThereIsHiggs){
      for (auto& writtenGenCand : writtenGenCands){
        MELACandidate* tmpCand = HiggsComparators::matchAHiggsToParticle(*LHEEvent, &writtenGenCand);
	if (tmpCand){
	  if (!ThereIsCand){
	    genCand = tmpCand;
	    ThereIsCand = true;
	  }else{
	    genCand = HiggsComparators::candComparator(genCand, tmpCand, HiggsComparators::BestZ1ThenZ2ScSumPt, VVMode);
	  }
	}
      }
    }else{
      genCand = HiggsComparators::candidateSelector(*LHEEvent, HiggsComparators::BestZ1ThenZ2ScSumPt, VVMode);
    }
    
    // MAKE THE IvyAutoMELA CALL 
    //cout << "====================================================" << endl;
    //TUtil::PrintCandidateSummary(genCand);
    //cout << "====================================================" << endl;

    float m1 = -1.0;
    float m2;

    std::vector<MELAParticle*> LHEbosons = LHEEvent->getIntermediates();
    for (auto& part : LHEbosons){
      
      //std::cout << part->id << std::endl; ///// Check --------
      
      if (abs(part->id) == 23){
	if (m1 == -1.0)
	  m1 = part->m();
	else{
	  m2 = part->m();
	  if (m1<m2){
	    m2 = m1;
	    m1 = part->m();
	  }
	}
      }
    }

    mela->selfDHzzcoupl[0/1][0][0]=1;
    mela->selfDHwwcoupl[0/1][0][0]=1;
    mela->selfDHggcoupl[0/1][0][0]=1;    
    mela->setCandidateDecayMode(TVar::CandidateDecay_WW);
    mela->setCurrentCandidate(genCand);

    float qH;
    float mV1;
    float mV2;
    float costheta1;
    float costheta2;
    float Phi;
    float costhetastar;
    float Phi1;

    mela->setProcess(TVar::HSMHiggs, TVar::JHUGen, TVar::ZZINDEPENDENT);
    mela->setMelaHiggsMassWidth(125.0, 0.00407, 0);
    mela->computeDecayAngles(qH, mV1, mV2, costheta1, costheta2, Phi, costhetastar, Phi1);

    float genMass;
    genMass = (float)genCand->m();

    /////////
    ///////// PREPARE OUTPUT FOR MELAcalc.py
    /////////
    
    RVecF LHEDaughterId;
    RVecF LHEDaughterPt;
    RVecF LHEDaughterEta;
    RVecF LHEDaughterPhi;
    RVecF LHEDaughterMass;

    RVecF LHEAssociatedParticlePt;
    RVecF LHEAssociatedParticleEta;
    RVecF LHEAssociatedParticlePhi;
    RVecF LHEAssociatedParticleMass;
    RVecF LHEAssociatedParticleId;

    RVecF LHEMotherId;
    RVecF LHEMotherPz;
    RVecF LHEMotherE;

    std::vector<MELAParticle*> LHEDaughters = genCand->getSortedDaughters();
    for (auto& part : LHEDaughters){
      LHEDaughterId.push_back((float)part->id);
      LHEDaughterPt.push_back(part->pt());
      LHEDaughterEta.push_back(part->eta());
      LHEDaughterPhi.push_back(part->phi());
      LHEDaughterMass.push_back(part->m());
    }

    std::vector<MELAParticle*> LHEAssociated = genCand->getAssociatedJets();
    for (auto& part : LHEAssociated){
      LHEAssociatedParticleId.push_back((float)part->id);
      LHEAssociatedParticlePt.push_back(part->pt());
      LHEAssociatedParticleEta.push_back(part->eta());
      LHEAssociatedParticlePhi.push_back(part->phi());
      LHEAssociatedParticleMass.push_back(part->m());
    }

    std::vector<MELAParticle*> LHEMothers = LHEEvent->getMothers();
    for (auto& part : LHEMothers){
      LHEMotherId.push_back((float)part->id);
      LHEMotherPz.push_back(part->z());
      LHEMotherE.push_back(part->t());
    }

    RVecF otherVars = {qH, mV1, mV2, costheta1, costheta2, Phi, costhetastar, Phi1, genMass};

    std::vector<RVecF> results_to_return = {
      LHEDaughterId,
      LHEDaughterPt,
      LHEDaughterEta,
      LHEDaughterPhi,
      LHEDaughterMass,
      LHEAssociatedParticlePt,
      LHEAssociatedParticleEta,
      LHEAssociatedParticlePhi,
      LHEAssociatedParticleMass,
      LHEAssociatedParticleId,
      LHEMotherId,
      LHEMotherPz,
      LHEMotherE,
      otherVars
    };

    return results_to_return;
  
    /**
    doVBF = false;
    if (!doVBF){ // skip VBF computation

      //cout << "Skip VBF Interference!" << endl;
      
      //cout << "----- RESULTS -----" << endl;
      //cout << "|ME| ggH Signal ->" << GG_SIG_kappaTopBot_1_ghz1_1_MCFM << endl;
      //cout << "|ME| ggH SBI    ->" << GG_BSI_kappaTopBot_1_ghz1_1_MCFM << endl;
      //cout << "|ME| ggH Bkg    ->" << GG_BKG_MCFM << endl;
      //cout << "|ME| VBF Signal ->" << JJEW_SIG_ghv1_1_MCFM << endl;
      //cout << "|ME| VBF SBI    ->" << JJEW_BSI_ghv1_1_MCFM << endl;
      //cout << "|ME| VBF Bkg    ->" << JJEW_BKG_MCFM << endl;

      genMass = (float)genCand->m();

      if (std::isnan(GG_SIG_azh1_azh2_JHUGen)) GG_SIG_azh1_azh2_JHUGen = 0.0;
      
      RVecF results = {GG_SIG_azh1_azh2_JHUGen, qH, m1, m2, costheta1, costheta2, Phi, costhetastar, Phi1, genMass};
      mela->resetInputEvent();
      return results;
    }
    
    //// Some tricks for VBF production
    TVar::Production candScheme=TVar::JJVBF;
    MELACandidateRecaster* recaster =  new MELACandidateRecaster(candScheme);
    MELACandidate* genCand_VBF;
      
    std::vector<MELAParticle*> associated_MELA = genCand->getAssociatedJets();
    bool gluonsOut = false;
    for (auto& part: associated_MELA){
      if (part->id == 21)
	gluonsOut = true;
    }    

    // Check gluons
    if (gluonsOut && !gluonsIn){
      // cout << "DO RECAST!" << endl;

      recaster->copyCandidate(genCand, genCand_VBF); 
      recaster->reduceJJtoQuarks(genCand_VBF);
      mela->setCurrentCandidate(genCand_VBF);
      
    }else{
      mela->setCurrentCandidate(genCand);
    }
    
    mela->setProcess(TVar::SelfDefine_spin0,TVar::JHUGen, TVar::JJEW);
    mela->setMelaHiggsMassWidth(125.0, 0.00407, 0);
    mela->computeP(GG_SIG_azh1_azh2_JHUGen, true);
    mela->computeDecayAngles(qH, m1, m2, costheta1, costheta2, Phi, costhetastar, Phi1);

    genMass = (float)genCand->m();

    if (std::isnan(GG_SIG_azh1_azh2_JHUGen)) GG_SIG_azh1_azh2_JHUGen = 0.0;

    RVecF results = {GG_SIG_azh1_azh2_JHUGen, qH, m1, m2, costheta1, costheta2, Phi, costhetastar, Phi1, genMass};
    mela->resetInputEvent();
    return results;
   
    **/
  }
};
