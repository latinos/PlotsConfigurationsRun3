#ifndef DBNN_SIG_BKG
#define DBNN_SIG_BKG

#include <vector>
#include <cmath>
#include <iostream>
#include "ROOT/RVec.hxx"

#include "generated_code_dbnn_consistent_no_mlj.h"

using namespace ROOT;
using namespace ROOT::VecOps;


RVecF dbnn_clf(
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
    float eta1,
    float eta2,
    float pt1,
    float pt2
) {

    RVecF dbnn;
    float inputs[19];
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
    inputs[15] = eta1;
    inputs[16] = eta2;
    inputs[17] = pt1;
    inputs[18] = pt2;

    dbnn.push_back(guess_SigDBNN(inputs, 0));
    dbnn.push_back(guess_SigDBNN(inputs, 1));
    dbnn.push_back(guess_SigDBNN(inputs, 2));
    dbnn.push_back(guess_SigDBNN(inputs, 3));
    return dbnn;
}

#endif