#include "TLorentzVector.h"

#include <iostream>
#include "ROOT/RVec.hxx"

#include "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/MelaAnalytics/EventContainer/interface/MELAEvent.h"
#include "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/IvyFramework/IvyAutoMELA/interface/IvyMELAHelpers.h"
#include "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/JHUGenMELA/MELA/interface/PDGHelpers.h"
#include "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/JHUGenMELA/MELA/interface/TUtil.hh"
#include "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/MelaAnalytics/EventContainer/interface/HiggsComparators.h"
#include "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/MelaAnalytics/EventContainer/interface/TopComparators.h"
#include "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/MelaAnalytics/CandidateLOCaster/interface/MELACandidateRecaster.h"
#include "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/JHUGenMELA/MELA/interface/Mela.h"

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


class GEN_INTERFERENCE{
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
  
  GEN_INTERFERENCE(){

    VVMode = MELAEvent::getCandidateVVModeFromString("WW");
    isGen = true;
    VVDecayMode = 0; // For both ggH and VBF

    LHCsqrts = 13.0;
    mh = 125.0;
    myVerbosity_ = TVar::SILENT; //TVar::DEBUG; TVar::SILENT

    mela = new Mela(LHCsqrts, mh, myVerbosity_);
  }

  RVecF operator()(int _nLHEPart,
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
    // cout << "====================================================" << endl;
    // TUtil::PrintCandidateSummary(genCand);
    // cout << "====================================================" << endl;
        
    float GG_SIG_kappaTopBot_1_ghz1_1_MCFM = -999.9;
    float GG_BSI_kappaTopBot_1_ghz1_1_MCFM = -999.9;
    float GG_BKG_MCFM = -999.9;

    float JJEW_SIG_ghv1_1_MCFM = -999.9;
    float JJEW_BSI_ghv1_1_MCFM = -999.9;
    float JJEW_BKG_MCFM = -999.9;
    float genMass = -999.9; 
        
    mela->setCandidateDecayMode(TVar::CandidateDecay_WW);
    mela->setCurrentCandidate(genCand);
    mela->selfDHzzcoupl[0/1][0][0]=1;
    mela->selfDHwwcoupl[0/1][0][0]=1;
    mela->selfDHggcoupl[0/1][0][0]=1;
    
    // gg -> H Signal
    
    mela->setProcess(TVar::HSMHiggs, TVar::MCFM, TVar::ZZGG);
    mela->setMelaHiggsMassWidth(125.0, 0.00407, 0);
    mela->computeP(GG_SIG_kappaTopBot_1_ghz1_1_MCFM, true);

    // gg -> (H) -> WW Total
    
    mela->setProcess(TVar::bkgWW_SMHiggs, TVar::MCFM, TVar::ZZGG);
    mela->setMelaHiggsMassWidth(125.0, 0.00407, 0);
    mela->computeP(GG_BSI_kappaTopBot_1_ghz1_1_MCFM, true);

    // gg -> WW background 
    
    mela->setProcess(TVar::bkgWW, TVar::MCFM, TVar::ZZGG);
    mela->setMelaHiggsMassWidth(125.0, 0.00407, 0);
    mela->computeP(GG_BKG_MCFM, true);

    
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
      
      RVecF results = {GG_SIG_kappaTopBot_1_ghz1_1_MCFM, GG_BSI_kappaTopBot_1_ghz1_1_MCFM, GG_BKG_MCFM, JJEW_SIG_ghv1_1_MCFM, JJEW_BSI_ghv1_1_MCFM, JJEW_BKG_MCFM, genMass};
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
    
    mela->selfDHzzcoupl[0/1][0][0]=1;
    mela->selfDHwwcoupl[0/1][0][0]=1;
    mela->selfDHggcoupl[0/1][0][0]=1;
    
    // VBF H Signal

    mela->setProcess(TVar::HSMHiggs, TVar::MCFM, TVar::JJEW);
    mela->setMelaHiggsMassWidth(125.0, 0.00407, 0);
    mela->computeProdDecP(JJEW_SIG_ghv1_1_MCFM, true);

    // VBF H+WW Total
    
    mela->setProcess(TVar::bkgWW_SMHiggs, TVar::MCFM, TVar::JJEW);
    mela->setMelaHiggsMassWidth(125.0, 0.00407, 0);
    mela->computeProdDecP(JJEW_BSI_ghv1_1_MCFM, true);

    // qqWW Background
    
    mela->setProcess(TVar::bkgWW, TVar::MCFM, TVar::JJEW);
    mela->setMelaHiggsMassWidth(125.0, 0.00407, 0);
    mela->computeProdDecP(JJEW_BKG_MCFM, true);
    
    //cout << "----- RESULTS VBF -----" << endl;
    //cout << "|ME| ggH Signal ->" << GG_SIG_kappaTopBot_1_ghz1_1_MCFM << endl;
    //cout << "|ME| ggH SBI    ->" << GG_BSI_kappaTopBot_1_ghz1_1_MCFM << endl;
    //cout << "|ME| ggH Bkg    ->" << GG_BKG_MCFM << endl;
    //cout << "|ME| VBF Signal ->" << JJEW_SIG_ghv1_1_MCFM << endl;
    //cout << "|ME| VBF SBI    ->" << JJEW_BSI_ghv1_1_MCFM << endl;
    //cout << "|ME| VBF Bkg    ->" << JJEW_BKG_MCFM << endl;

    genMass = (float)genCand->m();
    
    RVecF results = {GG_SIG_kappaTopBot_1_ghz1_1_MCFM, GG_BSI_kappaTopBot_1_ghz1_1_MCFM, GG_BKG_MCFM, JJEW_SIG_ghv1_1_MCFM, JJEW_BSI_ghv1_1_MCFM, JJEW_BKG_MCFM, genMass};
    mela->resetInputEvent();
    return results;
  }  
};
