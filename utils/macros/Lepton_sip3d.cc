#ifndef LEPTON_SIP3D
#define LEPTON_SIP3D

#include <vector>
#include "ROOT/RVec.hxx"

using namespace ROOT;
using namespace ROOT::VecOps;

RVec<float> LeptonSIP3D( RVecI Lepton_pdgId,
                         RVecI Lepton_electronIdx,
                         RVecI Lepton_muonIdx,
                         RVecF Electron_sip3d,
                         RVecF Muon_sip3d) {
    RVec<float> sip3d;

    for (size_t i = 0; i < Lepton_pdgId.size(); ++i) {
        float sip = -9999.0; // Default value for SIP if not found
        int pdgId = abs(Lepton_pdgId[i]);

        if (pdgId == 11) {
            int idx = Lepton_electronIdx[i];
            sip = Electron_sip3d[idx];
        } else if (pdgId == 13) {
            int idx = Lepton_muonIdx[i];
            sip = Muon_sip3d[idx];
        }
        sip3d.push_back(sip);
    }
    return sip3d;
}

#endif