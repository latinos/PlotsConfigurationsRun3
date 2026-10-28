#ifndef RECOKD
#define RECOKD

#include <iostream>
#include <fstream>
#include <cmath>
#include "ROOT/RVec.hxx"

#include "TFile.h"
#include "TString.h"
#include "TGraph.h"
#include "TSpline.h"

using namespace ROOT;
using namespace ROOT::VecOps;

// Production based KDs

class RECOKD_VBF{
public:
  RVecF me_vbf; RVecF me_qcd;
  
  RECOKD_VBF(){
  }

  RVecF operator()(RVecF _me_vbf, RVecF _me_qcd) {

    me_vbf = _me_vbf;
    me_qcd = _me_qcd;

    float h_mass     = me_vbf[0];
    float me_hsm     = me_vbf[1];
    float me_hp      = me_vbf[2];
    float me_hm      = me_vbf[3];
    float me_hl      = me_vbf[4];
    float me_hpzg    = me_vbf[5];
    float me_hmzg    = me_vbf[6];
    float me_hpgg    = me_vbf[7];
    float me_hmgg    = me_vbf[8];
    float me_mixhp   = me_vbf[9];
    float me_mixhm   = me_vbf[10];
    float me_mixhl   = me_vbf[11];
    float me_mixhpzg = me_vbf[12];
    float me_mixhmzg = me_vbf[13];
    float me_mixhpgg = me_vbf[14];
    float me_mixhmgg = me_vbf[15];

    float me_qcd_hsm    = me_qcd[1];

    float c   = 1.13932;  // Standard VBF AC gi 
    float g2  = 0.2719;   // Appropriate for SMEFT? 
    float g4  = 0.297979; 
    float L1  = 2158.21;
    
    float PZg = 0.200; // Taking gi from PHYSICAL REVIEW D 105, 096027 (2022)
    float MZg = 0.207;
    float Pgg = 0.124;
    float Mgg = 0.123;

    RVecF KDs;

    float kd_smvbf = 1/(1+((me_qcd_hsm*c)/me_hsm));
    float kd_hpvbf = 1/(1+((me_qcd_hsm*c)/(me_hp*pow(g2,2))));
    float kd_hmvbf = 1/(1+((me_qcd_hsm*c)/(me_hm*pow(g4,2))));
    float kd_hlvbf = 1/(1+((me_qcd_hsm*c)/(me_hl*pow(L1,2))));
    float kd_vbf   = max(max(kd_smvbf, kd_hmvbf), max(kd_hpvbf, kd_hlvbf));

    KDs.push_back(kd_vbf); //0

    float kd_hp      = 1/(1+(me_hsm/(me_hp*pow(g2,2))));
    float kd_hm      = 1/(1+(me_hsm/(me_hm*pow(g4,2))));
    float kd_hl      = 1/(1+(me_hsm/(me_hl*pow(L1,2))));
    float kd_hpzg    = 1/(1+(me_hsm/(me_hpzg*pow(PZg,2))));
    float kd_hmzg    = 1/(1+(me_hsm/(me_hmzg*pow(MZg,2))));
    float kd_hpgg    = 1/(1+(me_hsm/(me_hpgg*pow(Pgg,2))));
    float kd_hmgg    = 1/(1+(me_hsm/(me_hmgg*pow(Mgg,2))));
    float kd_mixhp   = (me_mixhp   - me_hsm - me_hp)/(2*sqrt(me_hsm*me_hp));
    float kd_mixhm   = (me_mixhm   - me_hsm - me_hm)/(2*sqrt(me_hsm*me_hm));
    float kd_mixhl   = (me_mixhl   - me_hsm - me_hl)/(2*sqrt(me_hsm*me_hl));
    float kd_mixhpzg = (me_mixhpzg - me_hsm - me_hpzg)/(2*sqrt(me_hsm*me_hpzg));
    float kd_mixhmzg = (me_mixhmzg - me_hsm - me_hmzg)/(2*sqrt(me_hsm*me_hmzg));
    float kd_mixhpgg = (me_mixhpgg - me_hsm - me_hpgg)/(2*sqrt(me_hsm*me_hpgg));
    float kd_mixhmgg = (me_mixhmgg - me_hsm - me_hmgg)/(2*sqrt(me_hsm*me_hmgg));

    KDs.push_back(kd_hp); //1
    KDs.push_back(kd_hm);
    KDs.push_back(kd_hl);
    KDs.push_back(kd_hpzg);
    KDs.push_back(kd_hmzg);
    KDs.push_back(kd_hpgg);
    KDs.push_back(kd_hmgg);//7
    KDs.push_back(kd_mixhp);//8
    KDs.push_back(kd_mixhm);
    KDs.push_back(kd_mixhl);//10
    KDs.push_back(kd_mixhpzg);
    KDs.push_back(kd_mixhmzg);
    KDs.push_back(kd_mixhpgg);
    KDs.push_back(kd_mixhmgg);//14

    KDs.push_back(kd_smvbf); 
    KDs.push_back(kd_hpvbf);
    KDs.push_back(kd_hmvbf);
      
    return KDs;

  }
};

#endif
