
#ifndef GENTOOLS_H
#define GENTOOLS_H

#include "ROOT/RVec.hxx"
#include "TLorentzVector.h"
#include <vector>
#include <iostream>
#include <map>

#include <iostream>
#include <string>
#include <sstream>

using namespace ROOT;
using namespace ROOT::VecOps;
using LorentzVectorM = ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<float>>;

extern std::map<std::string, RVecF> hyps_AC;
extern std::map<std::string, RVecF> hyps_4C2V;
extern std::map<std::string, RVecF> hyps_4C1V;
extern std::map<std::string, RVecF> hyps_8C2V;
extern std::map<std::string, RVecF> hyps_8C1V;

//-> Order the index by pt
std::vector<int> pTorder(std::vector<int> old_Idx, RVecF LHEPart_pt);

//-> Find LHE particles (higher precision) with closest match to GenParticles : LHE <Idx, (pt, eta, phi, Id)>
std::map<int, std::vector<float>> getLHE(std::vector<int>& GenPart_Idx, RVecF GenPart_pt, RVecF GenPart_eta, RVecF GenPart_phi, RVecI GenPart_pdgId, int nLHEPart, RVecF LHEPart_pt, RVecF LHEPart_eta, RVecF LHEPart_phi, RVecI LHEPart_status, RVecI LHEPart_pdgId, string dec);

//-> Iterate over mothers to find Higgs

bool FromH(int pi, RVecI GenPart_genPartIdxMother, RVecI GenPart_pdgId);

//-> Remove rare additonal hadrons 
std::vector<int> RemoveAddHadron(std::vector<int> GenPart_Idx, RVecI GenPart_genPartIdxMother);

//-> Remove W -> gamma W -> e+ e- W                              
std::vector<int> RemoveGammaW(std::vector<int> GenPart_Idx, RVecI GenPart_pdgId, RVecI GenPart_genPartIdxMother);

#endif 
