#include "TLorentzVector.h"
#include <vector>
#include "TVector2.h"
#include "TLorentzVector.h"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"
#include <iostream>
#include <TMath.h>
#include <math.h>
#include "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/extended/momemta/ConfigurationReader.h"
#include "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/extended/momemta/MoMEMta.h"
#include "/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/extended/momemta/Types.h"
#include <iostream>
#include "ROOT/RVec.hxx"

using namespace ROOT;
using namespace ROOT::VecOps;

using LorentzVectorM = ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float>>;

using namespace momemta;

class RecoMoMEMta_VBF{
public:

  RecoMoMEMta_VBF(){}

  void normalizeInput(LorentzVector& p4) {
    if (p4.M() > 0)
      return;

    p4.SetE(p4.P());
    while (p4.M2() < 0) {
      double delta = p4.E() * 1e-5;
      p4.SetE(p4.E() + delta);
    };
  }
  
  float operator()(float nCleanJet, float nLepton, float PuppiMet_pt, float PuppiMet_phi, float Lepton_pt0, float Lepton_pt1, float Lepton_phi0, float Lepton_phi1,float Lepton_eta0, float Lepton_eta1,float CleanJet_pt0, float CleanJet_pt1, float CleanJet_phi0, float CleanJet_phi1, float CleanJet_eta0, float CleanJet_eta1, float Lepton_pdg0, float Lepton_pdg1) {

    logging::set_level(logging::level::off);
    
    TLorentzVector L1(0.,0.,0.,0.);
    TLorentzVector L2(0.,0.,0.,0.);
    TLorentzVector LL(0.,0.,0.,0.);
    TLorentzVector NuNu(0.,0.,0.,0.);
    TLorentzVector Higgs(0.,0.,0.,0.);
    TLorentzVector J1(0.,0.,0.,0.);
    TLorentzVector J2(0.,0.,0.,0.);

    if(nCleanJet >= 2 && nLepton > 1){

      if (Lepton_pdg0*Lepton_pdg1 != -11*13) return -9999.;

      L1.SetPtEtaPhiM(Lepton_pt0, Lepton_eta0, Lepton_phi0, 0.0);
      L2.SetPtEtaPhiM(Lepton_pt1, Lepton_eta1, Lepton_phi1, 0.0);

      J1.SetPtEtaPhiM(CleanJet_pt0, CleanJet_eta0, CleanJet_phi0, 0.0);
      J2.SetPtEtaPhiM(CleanJet_pt1, CleanJet_eta1, CleanJet_phi1, 0.0);

      LL = L1 + L2;

      double nunu_px = PuppiMet_pt*cos(PuppiMet_phi);
      double nunu_py = PuppiMet_pt*sin(PuppiMet_phi);
      double nunu_pz = LL.Pz();
      double nunu_m = 30.0;


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

      // Higgs

      ConfigurationReader configuration_VBF("/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/qqH_hww_ME/higgs_jets.lua");
      MoMEMta weight_VBF(configuration_VBF.freeze());

      // DY 

      ConfigurationReader configuration_DY("/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/DY_ME/DY_ME.lua");
      MoMEMta weight_DY(configuration_DY.freeze());

      ParameterSet lua_parameters;
      lua_parameters.set("USE_TF", true);
      lua_parameters.set("USE_PERM", true);

      std::vector<std::pair<double, double>> weights_VBF = weight_VBF.computeWeights({higgs, jet1, jet2});
      std::vector<std::pair<double, double>> weights_DY = weight_DY.computeWeights({Z, jet1, jet2});

      float vbf = (float)weights_VBF.back().first;
      float dy = (float)weights_DY.back().first;

      return 150 * abs(vbf) / (150 * abs(vbf) + abs(dy));


    }else{

      return -9999.9;

    
    }
  }
};
