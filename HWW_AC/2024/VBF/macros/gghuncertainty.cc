#ifndef GGH_UNCERTAINTY
#define GGH_UNCERTAINTY

#include <vector>
#include <string>

class GGHUncertainty {
public:
  GGHUncertainty() {
    g_sig0         = 30.117;
    g_sig1         = 12.928;
    g_sig_ge2      = 5.475;
    g_sig_ge1      = g_sig1 + g_sig_ge2;
    g_sig_tot      = g_sig0 + g_sig_ge1;
    g_sig_vbfTopo  = 0.630;
    g_sig_ge2noVBF = g_sig_ge2 - g_sig_vbfTopo;
    g_sig_ge1noVBF = g_sig_ge1 - g_sig_vbfTopo;
  }

  GGHUncertainty(const std::string& name) : GGHUncertainty() {
    if      (name == "ggH_mu")    vindex_ = 0;
    else if (name == "ggH_res")   vindex_ = 1;
    else if (name == "ggH_mig01") vindex_ = 2;
    else if (name == "ggH_mig12") vindex_ = 3;
    else if (name == "ggH_VBF2j") vindex_ = 4;
    else if (name == "ggH_VBF3j") vindex_ = 5;
    else if (name == "ggH_pT60")  vindex_ = 6;
    else if (name == "ggH_pT120") vindex_ = 7;
    else if (name == "ggH_qmtop") vindex_ = 8;
    else vindex_ = 0;
  }

  virtual ~GGHUncertainty() {}

  double operator()(unsigned char njets, float pt, int stxs) const {
    auto sfs = qcd_ggF_uncertSF_2017(static_cast<int>(njets), pt, stxs);
    return static_cast<double>(sfs.at(vindex_));
  }


  std::vector<float> qcd_ggF_uncert_2017(int Njets30, float pT, int STXS) const {
    std::vector<float> result = jetBinUnc(Njets30, STXS);
    result.push_back(pT60(pT, Njets30));
    result.push_back(pT120(pT, Njets30));
    result.push_back(qm_t(pT));
    return result;
  }

  std::vector<float> qcd_ggF_uncert_wg1(int Njets30, float pT, int STXS) const {
    std::vector<float> result = jetBinUnc(Njets30, STXS);
    
    // High pT uncertainty 
    float y1_1 = -0.12, y2_1 = 0.16, x2_1 = 150;
    float y1_ge2 = -0.12, y2_ge2 = 0.16, x2_ge2 = 225;
    float pTH_unc = 0.0;
    if      (Njets30 == 1) pTH_unc = interpol(pT, 0, y1_1, x2_1, y2_1);
    else if (Njets30 >= 2) pTH_unc = interpol(pT, 0, y1_ge2, x2_ge2, y2_ge2);
    result.push_back(pTH_unc);
    
    // finite top mass uncertainty
    result.push_back(qm_t(pT));
    
    return result;
  }

  std::vector<float> qcd_ggF_uncert_stxs(int Njets30, float pT, int STXS) const {
    std::vector<float> result = jetBinUnc(Njets30, STXS);
    float sig0_60 = 8.719, sig60_200 = 9.095, sig120_200 = 1.961, sig200_plus = 0.582;
    float sig0_120 = sig0_60 + sig60_200 - sig120_200;
    float Dsig60_200 = 1.055, Dsig120_200 = 0.206, Dsig200_plus = 0.0832;
    
    float dsig60 = 0, dsig120 = 0, dsig200 = 0;
    if (Njets30 >= 1) {
      if      (pT < 60)  dsig60 = -Dsig60_200 / sig0_60;
      else if (pT < 200) dsig60 =  Dsig60_200 / sig60_200;
      
      if      (pT < 120) dsig120 = -Dsig120_200 / sig0_120;
      else if (pT < 200) dsig120 =  Dsig120_200 / sig120_200;
      
      if (pT > 200) dsig200 = Dsig200_plus / sig200_plus;
    }
    result.push_back(dsig60);
    result.push_back(dsig120);
    result.push_back(dsig200);
    return result;
  }

  std::vector<float> qcd_ggF_uncert_jve(int Njets30, float pT, int STXS) const {
    std::vector<float> result;
    float D01 = g_sig_tot * 0.012, D12 = g_sig_ge1 * 0.057;
    
    result.push_back(0.039); // YR4 inclusive cross section
    
    float d01 = (Njets30 == 0) ? -D01 / g_sig0 : D01 / g_sig_ge1noVBF; 
    result.push_back(d01);
    
    float d12 = 0.0;
    if      (Njets30 == 1) d12 = -D12 / g_sig1;
    else if (Njets30 >= 2) d12 =  D12 / g_sig_ge2noVBF;
    result.push_back(d12);
    
    result.push_back(vbf_2j(STXS));
    result.push_back(vbf_3j(STXS));
    if (result.back() != 0.0) result[0] = result[1] = result[2] = 0.0;
    
    result.push_back(pT60(pT, Njets30));
    result.push_back(pT120(pT, Njets30));
    result.push_back(qm_t(pT));
    return result;
  }

private:
  int vindex_{0};

  float g_sig0{0}, g_sig1{0}, g_sig_ge2{0}, g_sig_ge1{0};
  float g_sig_tot{0}, g_sig_vbfTopo{0}, g_sig_ge2noVBF{0}, g_sig_ge1noVBF{0};

  float interpol(float x, float x1, float y1, float x2, float y2) const {
    if (x < x1) return y1;
    if (x > x2) return y2;
    return y1 + (y2 - y1) * (x - x1) / (x2 - x1);
  }

  std::vector<float> blptw(int Njets30) const {
    std::vector<float> sig({g_sig0, g_sig1, g_sig_ge2noVBF});
    std::vector<float> yieldUnc({ 1.12, 0.66, 0.42});
    std::vector<float> resUnc  ({ 0.03, 0.57, 0.42});
    std::vector<float> cut01Unc({-1.22, 1.00, 0.21});
    std::vector<float> cut12Unc({    0,-0.86, 0.86});

    float sf = 48.52 / 47.4;
    int jetBin = (Njets30 > 1 ? 2 : Njets30);
    float normFact = sf / sig[jetBin];

    return { yieldUnc[jetBin] * normFact, 
             resUnc[jetBin]   * normFact,
             cut01Unc[jetBin] * normFact,
             cut12Unc[jetBin] * normFact };
  }

  float vbf_2j(int STXS) const {
    if (STXS == 101 || STXS == 102) return 0.200;
    return 0.0;
  }

  float vbf_3j(int STXS) const {
    if (STXS == 101) return -0.320;
    if (STXS == 102) return  0.235;
    return 0.0;
  }

  float qm_t(float pT) const {
    return interpol(pT, 160, 0.0, 500, 0.37);
  }

  float pT120(float pT, int Njets30) const {
    if (Njets30 == 0) return 0;
    return interpol(pT, 90, -0.016, 160, 0.14);
  }

  float pT60(float pT, int Njets30) const {
    if (Njets30 == 0) return 0;
    if (Njets30 == 1) return interpol(pT, 20, -0.1, 100, 0.1);
    return interpol(pT, 0, -0.1, 180, 0.10);
  }

  std::vector<float> jetBinUnc(int Njets30, int STXS) const {
    std::vector<float> result = blptw(Njets30);
    result.push_back(vbf_2j(STXS));
    result.push_back(vbf_3j(STXS));
    if (result.back() != 0.0) {
      result[0] = result[1] = result[2] = result[3] = 0.0;
    }
    return result;
  }

  std::vector<float> unc2sf(const std::vector<float> &unc, float Nsigma) const {
    std::vector<float> sfs; 
    for (auto u : unc) sfs.push_back(1.0 + Nsigma * u); 
    return sfs;
  }

  std::vector<float> qcd_ggF_uncertSF_2017(int Njets30, float pT, int STXS_Stage1, float Nsigma = 1.0) const {
    return unc2sf(qcd_ggF_uncert_2017(Njets30, pT, STXS_Stage1), Nsigma);
  }
};

#endif