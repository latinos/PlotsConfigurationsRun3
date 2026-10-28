#ifndef SNN_SIG_BKG
#define SNN_SIG_BKG

#include <vector>
#include <cmath>
#include <iostream>
#include "ROOT/RVec.hxx"

#include "generated_code_snn_ggf_simple.h"

using namespace ROOT;
using namespace ROOT::VecOps;


RVecF ggf_clf(
    float dphill,
    float drll,
    float mth,
    float mll,
    float puppimet,
    float jeteta1,
    float jeteta2,
    float jetpt1,
    float jetpt2,
    float dphillmet,
    float ptll,
    float eta1,
    float eta2,
    float pt1,
    float pt2
) {
    RVecF snn;
    float inputs[23];
    inputs[0]  = dphill;
    inputs[1]  = drll;
    inputs[2]  = mth;
    inputs[3]  = mll;
    inputs[4]  = puppimet;
    inputs[5]  = jeteta1;
    inputs[6]  = jeteta2;
    inputs[7] = jetpt1;
    inputs[8] = jetpt2;
    inputs[9] = dphillmet;
    inputs[10] = ptll;
    inputs[11] = eta1;
    inputs[12] = eta2;
    inputs[13] = pt1;
    inputs[14] = pt2;

    snn.push_back(guess_SigSNN(inputs, 0));
    return snn;
}

#endif
