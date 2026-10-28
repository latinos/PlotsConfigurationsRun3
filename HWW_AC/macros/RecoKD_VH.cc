
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

class RECOKD_VH{
public:
  RVecF me_wh;  RVecF me_zh; RVecF me_qcd;
  bool add_vhkd = 0; // Not used in Run 2 (Didnt add anything)

  RECOKD_VH(){
    
  }

  RVecF operator()(RVecF _me_wh, RVecF _me_zh, RVecF _me_qcd) {

    me_wh = _me_wh;
    me_zh = _me_zh;
    me_qcd = _me_qcd;

    float h_mass        = me_wh[0];
    float me_wh_hsm     = me_wh[1];
    float me_wh_hp      = me_wh[2];
    float me_wh_hm      = me_wh[3];
    float me_wh_hl      = me_wh[4];
    float me_wh_mixhp   = me_wh[9];
    float me_wh_mixhm   = me_wh[10];
    float me_wh_mixhl   = me_wh[11];    
    float pjjSm_wh   = me_wh[16];
    float pjjTr_wh   = me_wh[17];
    float meAvg_wh   = me_wh[18];

    float me_zh_hsm     = me_zh[1];
    float me_zh_hp      = me_zh[2];
    float me_zh_hm      = me_zh[3];
    float me_zh_hl      = me_zh[4];
    float me_zh_hpzg    = me_zh[5];
    float me_zh_hmzg    = me_zh[6];
    float me_zh_hpgg    = me_zh[7];
    float me_zh_hmgg    = me_zh[8];
    float me_zh_mixhp   = me_zh[9];
    float me_zh_mixhm   = me_zh[10];
    float me_zh_mixhl   = me_zh[11];
    float me_zh_mixhpzg = me_zh[12]; //DM include for WH? (Mix MEs prob non 0?)
    float me_zh_mixhmzg = me_zh[13];
    float me_zh_mixhpgg = me_zh[14];
    float me_zh_mixhmgg = me_zh[15];
    float pjjSm_zh   = me_zh[16];
    float pjjTr_zh   = me_zh[17];
    float meAvg_zh   = me_zh[18];

    float me_qcd_hsm    = me_qcd[1];
    
    float cWH  = 4.59827e-07;  // Standard VBF AC gi 
    float g2WH = 0.0997925;   // Appropriate for SMEFT?  
    float g4WH = 0.12341; 
    float L1WH = 524.44; 
      
    float cZH   = 2.07945e-07; 
    float g2ZH  = 0.113355; 
    float g4ZH  = 0.144065; 
    float L1ZH  = 517.818; 
    float LZgZH = 644.474; 
    
    float g2VH  = 0.104503; 
    float g4VH  = 0.130395;
    float gLVH  = -522.303;
      
    float PZgZH = 0.141; // Taking gi from PHYSICAL REVIEW D 105, 096027 (2022)
    float MZgZH = 0.175;
    float PggZH = 0.655;
    float MggZH = 0.747;

    RVecF KDs;

    float kd_vh = -999;

    if (add_vhkd==1){

     float pjj_wh = pjjSm_wh/pjjTr_wh;
     float pjj_zh = pjjSm_zh/pjjTr_zh;

     float kd_smwh = 1/(1+((me_qcd_hsm*cWH)/(me_wh_hsm*pjj_wh)));
     float kd_smzh = 1/(1+((me_qcd_hsm*cZH)/(me_zh_hsm*pjj_zh)));
     float kd_smvh = max(kd_smwh, kd_smzh);

     float kd_hpwh = 1/(1+((me_qcd_hsm*cWH)/(me_wh_hp*pjj_wh*pow(g2WH,2))));
     float kd_hpzh = 1/(1+((me_qcd_hsm*cZH)/(me_zh_hp*pjj_zh*pow(g2ZH,2))));
     float kd_hpvh = max(kd_hpwh, kd_hpzh);

     float kd_hmwh = 1/(1+((me_qcd_hsm*cWH)/(me_wh_hm*pjj_wh*pow(g4WH,2))));
     float kd_hmzh = 1/(1+((me_qcd_hsm*cZH)/(me_zh_hm*pjj_zh*pow(g4ZH,2))));
     float kd_hmvh = max(kd_hmwh, kd_hmzh);

     float kd_hlwh = 1/(1+((me_qcd_hsm*cWH)/(me_wh_hl*pjj_wh*pow(L1WH,2))));
     float kd_hlzh = 1/(1+((me_qcd_hsm*cZH)/(me_zh_hl*pjj_zh*pow(L1ZH,2))));
     float kd_hlvh = max(kd_hlwh, kd_hlzh);

     kd_vh  = max(max(kd_smvh, kd_hpvh), max(kd_hmvh, kd_hlvh));

    }

    KDs.push_back(kd_vh); //0

    float kd_wh_hp = 1/(1+(me_wh_hsm/(me_wh_hp*pow(g2WH,2))));
    float kd_zh_hp = 1/(1+(me_zh_hsm/(me_zh_hp*pow(g2ZH,2))));
    float kd_hp    = max(kd_wh_hp, kd_zh_hp);

    float me_hsm   = (me_wh_hsm/meAvg_wh) + (me_zh_hsm/meAvg_zh);
    float me_hp    = (me_wh_hp/meAvg_wh) + (me_zh_hp/meAvg_zh);
    float me_mixhp = ((me_wh_mixhp - me_wh_hsm - me_wh_hp)/meAvg_wh) + ((me_zh_mixhp - me_zh_hsm - me_zh_hp)/meAvg_zh);
    float kd_mixhp = (me_mixhp*g2VH) / (me_hsm + (me_hp*pow(g2VH,2)));

    float kd_wh_hm  = 1/(1+(me_wh_hsm/(me_wh_hm*pow(g4WH,2))));
    float kd_zh_hm  = 1/(1+(me_zh_hsm/(me_zh_hm*pow(g4ZH,2))));
    float kd_hm     = max(kd_wh_hm, kd_zh_hm);
    
    float me_hm    = (me_wh_hm/meAvg_wh) + (me_zh_hm/meAvg_zh);
    float me_mixhm = ((me_wh_mixhm - me_wh_hsm - me_wh_hm)/meAvg_wh) + ((me_zh_mixhm - me_zh_hsm - me_zh_hm)/meAvg_zh);
    float kd_mixhm = (me_mixhm*g4VH) / (me_hsm + (me_hm*pow(g4VH,2)));

    float kd_wh_hl = 1/(1+(me_wh_hsm/(me_wh_hl*pow(L1WH,2))));
    float kd_zh_hl = 1/(1+(me_zh_hsm/(me_zh_hl*pow(L1ZH,2))));
    float kd_hl    = max(kd_wh_hl, kd_zh_hl);

    float me_hl    = (me_wh_hl/meAvg_wh) + (me_zh_hl/meAvg_zh);
    float me_mixhl = ((me_wh_mixhl - me_wh_hsm - me_wh_hl)/meAvg_wh) + ((me_zh_mixhl - me_zh_hsm - me_zh_hl)/meAvg_zh);
    float kd_mixhl = (me_mixhl*gLVH) / (me_hsm + (me_hl*pow(gLVH,2))); 

    // ZH vertex only
    float kd_hpzg  = 1/(1+(me_zh_hsm/(me_zh_hpzg*pow(PZgZH,2))));
    float kd_hmzg  = 1/(1+(me_zh_hsm/(me_zh_hmzg*pow(MZgZH,2))));
    float kd_hpgg  = 1/(1+(me_zh_hsm/(me_zh_hpgg*pow(PggZH,2))));
    float kd_hmgg  = 1/(1+(me_zh_hsm/(me_zh_hmgg*pow(MggZH,2))));

    KDs.push_back(kd_hp); //1
    KDs.push_back(kd_hm);
    KDs.push_back(kd_hl);
    KDs.push_back(kd_hpzg);
    KDs.push_back(kd_hmzg);
    KDs.push_back(kd_hpgg);
    KDs.push_back(kd_hmgg); //7
    KDs.push_back(kd_mixhp);
    KDs.push_back(kd_mixhm);
    KDs.push_back(kd_mixhl); 
    
    return KDs;

  }
};
