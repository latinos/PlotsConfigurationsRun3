#ifndef SNN_SIG_BKG
#define SNN_SIG_BKG

#include <vector>
#include <cmath>
#include <iostream>
#include "ROOT/RVec.hxx"

#include "generated_code_dymva.h"

using namespace ROOT;
using namespace ROOT::VecOps;


RVecF dymva(
    float puppimet,
    float trkmet,
    float projtkmet,
    float divpuppimet,
    float jeteta1,
    float jeteta2,
    float jetpt1,
    float jetpt2,
    float mth,
    float dphillmet,
    float ptll,
    float mjj,
    float mll,
    float mtw2,
    float ptww,
    float dphijjmet,
    float dphil1tkmet,
    float dphil2tkmet,
    float dphill,
    float pt1,
    float pt2,
    float eta1,
    float eta2
) {
    RVecF snn;
    float inputs[23];
    inputs[0]  = puppimet;
    inputs[1]  = trkmet;
    inputs[2]  = projtkmet;
    inputs[3]  = divpuppimet;
    inputs[4]  = jeteta1;
    inputs[5]  = jeteta2;
    inputs[6]  = jetpt1;
    inputs[7]  = jetpt2;
    inputs[8]  = mth;
    inputs[9]  = dphillmet;
    inputs[10] = ptll;
    inputs[11] = mjj;
    inputs[12] = mll;
    inputs[13] = mtw2;
    inputs[14] = ptww;
    inputs[15] = dphijjmet;
    inputs[16] = dphil1tkmet;
    inputs[17] = dphil2tkmet;
    inputs[18] = dphill;
    inputs[19] = pt1;
    inputs[20] = pt2;
    inputs[21] = eta1;
    inputs[22] = eta2;

    snn.push_back(guess_SigSNN(inputs, 0));
    snn.push_back(guess_SigSNN(inputs, 1));
    return snn;
}

#endif
