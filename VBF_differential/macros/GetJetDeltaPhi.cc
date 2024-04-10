#ifndef GetJetDeltaPhi
#define GetJetDeltaPhi


#include <vector>
#include "TLorentzVector.h"

#include "TVector2.h"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"

#include <iostream>

#include "ROOT/RVec.hxx"

using namespace ROOT;
using namespace ROOT::VecOps;


double JetDeltaPhi(
                    int    nCleanJet,
		                RVecF  CleanJet_eta,
		                RVecF  CleanJet_phi
                  ){

  int nJets = nCleanJet;
  if ((nJets > 1) && (TMath::Abs(CleanJet_eta[0])<4.7) && (TMath::Abs(CleanJet_eta[1])<4.7) ){

    double phi1{CleanJet_phi[0]};
    double phi2{CleanJet_phi[1]};

    double eta1{CleanJet_eta[0]};
    double eta2{CleanJet_eta[1]};

    double output;

    // Adjust dphijj definition according to
    // https://arxiv.org/pdf/2002.09888.pdf (eq. 47)
    if (eta1 > eta2)       output = phi1 - phi2;
    else if (eta1 <= eta2) output = phi2 - phi1;
    
    // To have delta_phi in (-pi, pi) interval
    // https://root.cern.ch/doc/master/TVector2_8cxx_source.html#l00103
    if (output >  TMath::Pi()) output -= 2*TMath::Pi();
    if (output <= -TMath::Pi()) output += 2*TMath::Pi();
    

    return output;
  }
  else
    return -9999.;
}

#endif