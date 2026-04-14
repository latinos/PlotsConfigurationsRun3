#ifndef SNN_SIG_BKG
#define SNN_SIG_BKG

#include <vector>
#include <cmath>
#include <iostream>
#include "ROOT/RVec.hxx"

#include "generated_code_vbf_clf.h"

using namespace ROOT;
using namespace ROOT::VecOps;


RVecF vbf_clf(
    float detajj,
    float dphill,
    float drll,
    float mjj,
    float ht,
    float mth,
    float mll,
    float puppimet,
    float jeteta1,
    float jeteta2,
    float jetpt1,
    float jetpt2,
    float dphillmet,
    float ptll,
    float ctot,
    float mlj11,
    float mlj12,
    float mlj21,
    float mlj22,
    float eta1,
    float eta2,
    float pt1,
    float pt2
) {
    RVecF snn;
    float inputs[23];
    inputs[0]  = detajj;
    inputs[1]  = dphill;
    inputs[2]  = drll;
    inputs[3]  = mjj;
    inputs[4]  = ht;
    inputs[5]  = mth;
    inputs[6]  = mll;
    inputs[7]  = puppimet;
    inputs[8]  = jeteta1;
    inputs[9]  = jeteta2;
    inputs[10] = jetpt1;
    inputs[11] = jetpt2;
    inputs[12] = dphillmet;
    inputs[13] = ptll;
    inputs[14] = ctot;
    inputs[15] = mlj11;
    inputs[16] = mlj12;
    inputs[17] = mlj21;
    inputs[18] = mlj22;
    inputs[19] = eta1;
    inputs[20] = eta2;
    inputs[21] = pt1;
    inputs[22] = pt2;

    snn.push_back(guess_SigSNN(inputs, 0));
    snn.push_back(guess_SigSNN(inputs, 1));
    snn.push_back(guess_SigSNN(inputs, 2));
    snn.push_back(guess_SigSNN(inputs, 3));
    return snn;
}

#endif
