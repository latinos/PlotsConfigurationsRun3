
#include <vector>

#include "TVector2.h"
#include "TLorentzVector.h"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"

#include <iostream>
#include "ROOT/RVec.hxx"

#include <TMath.h>
#include <math.h>

#include "/afs/cern.ch/work/b/bcamaian/mkShapesRDF/momemta/include/momemta/ConfigurationReader.h"
#include "momemta/MoMEMta.h"
#include "momemta/Types.h"


#include "Math/Point3D.h"
#include "Math/Vector3D.h"
#include "Math/Vector4D.h"
#include "Math/Rotation3D.h"
#include "Math/EulerAngles.h"
#include "Math/AxisAngle.h"
#include "Math/Quaternion.h"
#include "Math/RotationX.h"
#include "Math/RotationY.h"
#include "Math/RotationZ.h"
#include "Math/RotationZYX.h"
#include "Math/LorentzRotation.h"
#include "Math/Boost.h"
#include "Math/BoostX.h"
#include "Math/BoostY.h"
#include "Math/BoostZ.h"
#include "Math/Transform3D.h"
#include "Math/Plane3D.h"
#include "Math/VectorUtil.h"
#include "TMatrixD.h"
#include "TVectorD.h"
#include "TMath.h"


using namespace ROOT;
using namespace ROOT::VecOps;

using namespace momemta;



void normalizeInput(LorentzVector& p4) {
  if (p4.M() > 0)
    return;

  // Increase the energy until M is positive                                                                                                                                 
  p4.SetE(p4.P());
  while (p4.M2() < 0) {
    double delta = p4.E() * 1e-5;
    p4.SetE(p4.E() + delta);
  };
}



RVecF MoMEMta_discriminant(float nCleanJet, float nLepton, float PuppiMet_pt, float PuppiMet_phi, float Lepton_pt_1, float Lepton_pt_2, float Lepton_phi_1, float Lepton_phi_2, float Lepton_eta_1, float Lepton_eta_2,float CleanJet_pt_1, float CleanJet_pt_2, float CleanJet_phi_1, float CleanJet_phi_2, float CleanJet_eta_1, float CleanJet_eta_2, float Lepton_pdgId_1, float Lepton_pdgId_2){

  RVecF mom_d;

  TLorentzVector L1(0.,0.,0.,0.);
  TLorentzVector L2(0.,0.,0.,0.);
  TLorentzVector LL(0.,0.,0.,0.);
  TLorentzVector NuNu(0.,0.,0.,0.);
  TLorentzVector Higgs(0.,0.,0.,0.);
  TLorentzVector J1(0.,0.,0.,0.);
  TLorentzVector J2(0.,0.,0.,0.);

  if(nCleanJet >= 2 && nLepton > 1){

    if (Lepton_pdgId_1*Lepton_pdgId_2 != -11*13) {
        mom_d.push_back(-9999.);
        return mom_d;
    }

    L1.SetPtEtaPhiM(Lepton_pt_1, Lepton_eta_1, Lepton_phi_1, 0.0);
    L2.SetPtEtaPhiM(Lepton_pt_2, Lepton_eta_2, Lepton_phi_2, 0.0);

    J1.SetPtEtaPhiM(CleanJet_pt_1, CleanJet_eta_1, CleanJet_phi_1, 0.0);
    J2.SetPtEtaPhiM(CleanJet_pt_2, CleanJet_eta_2, CleanJet_phi_2, 0.0);

    LL = L1 + L2;

    double nunu_px = PuppiMet_pt*cos(PuppiMet_phi);
    double nunu_py = PuppiMet_pt*sin(PuppiMet_phi);
    double nunu_pz = LL.Pz();
    double nunu_m = 30.0; //Why 30? --> https://indico.cern.ch/event/850505/contributions/3593915/                                                                                                         

    double nunu_e = sqrt(nunu_px*nunu_px + nunu_py*nunu_py + nunu_pz*nunu_pz + nunu_m*nunu_m);
    NuNu.SetPxPyPzE(nunu_px, nunu_py, nunu_pz, nunu_e);
    Higgs = LL + NuNu;


    momemta::Particle higgs { "higgs", LorentzVector(Higgs.Px(), Higgs.Py(), Higgs.Pz(), Higgs.E()), 25 }; // Higgs
    momemta::Particle Z { "Z", LorentzVector(Higgs.Px(), Higgs.Py(), Higgs.Pz(), Higgs.E()), 23 }; // Z, same 4 vector as Higgs                                                                            
    momemta::Particle jet1 { "jet1", LorentzVector(J1.Px(), J1.Py(), J1.Pz(), J1.E()), 1 };
    momemta::Particle jet2 { "jet2", LorentzVector(J2.Px(), J2.Py(), J2.Pz(), J2.E()), -1 };

    normalizeInput(higgs.p4);
    normalizeInput(Z.p4);
    normalizeInput(jet1.p4);
    normalizeInput(jet2.p4);


    logging::set_level(logging::level::off);

    // Higgs                                                                                                                                                                                               
    ConfigurationReader configuration_VBF("/afs/cern.ch/work/b/bcamaian/CMSSW_10_6_27/src/qqH_hww_ME/higgs_jets.lua");
    MoMEMta weight_VBF(configuration_VBF.freeze());

    // DY                                                                                                                                                                                                 
    ConfigurationReader configuration_DY("/afs/cern.ch/work/b/bcamaian/CMSSW_10_6_27/src/DY_ME/DY_ME.lua");
    MoMEMta weight_DY(configuration_DY.freeze());

    ParameterSet lua_parameters;
    lua_parameters.set("USE_TF", true);
    lua_parameters.set("USE_PERM", true);

    std::vector<std::pair<double, double>> weights_VBF = weight_VBF.computeWeights({higgs, jet1, jet2});
    std::vector<std::pair<double, double>> weights_DY = weight_DY.computeWeights({Z, jet1, jet2});

    double vbf = (double)weights_VBF.back().first;
    double dy = (double)weights_DY.back().first;

    mom_d.push_back( 150 * abs(vbf) / (150 * abs(vbf) + abs(dy)));
    return mom_d;


  }else{
    
    mom_d.push_back(-9999.9);
    return mom_d;

  }
}
