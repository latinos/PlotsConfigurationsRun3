#include <cstdlib>
#include <iostream>
#include <string>
#include <cstring>
#include <list>
#include <algorithm>
#include <map>
#include <string_view>

#include <math.h>
#include <dirent.h>
#include <sys/types.h>

#include <filesystem> 

#include "TH1.h"
#include "TH2.h"
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TSystem.h"
#include "TROOT.h"
#include "TObjString.h"
#include "TChain.h"
#include "TCut.h"
#include "TGraphAsymmErrors.h"
#include "TLorentzVector.h"
#include "TLine.h"
#include "TCanvas.h"
#include <TROOT.h>
#include <TStyle.h>


struct dataset {
  int year;
  std::map<std::string, std::string> samples;
  std::map<std::string, std::map<std::string, double>> algo;
};

dataset mkDataset(int year) {
  TH1::SetDefaultSumw2(true);
  dataset d;
  d.year    = year;
  if (year == 2022) {
    d.samples = {
        {"DY" , "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer22_130x_nAODv12_Full2022v12_OLD/MCl2loose2022v12__MCCorr2022v12JetScaling__l2tight/nanoLatino_DYto2L-2Jets_MLL-50__part*.root"}
    };
    d.algo = {
        {"DeepFlavB", {{"loose" , 0.0583}, {"medium" , 0.3086}, {"tight" , 0.7183}}},
        {"RobustParTAK4B", {{"loose", 0.0849}, {"medium", 0.4319}, {"tight", 0.8482}}},
        {"PNetB", {{"loose", 0.0470}, {"medium", 0.2450}, {"tight", 0.6734}}}
    };
  }

  for (auto const &elem : d.algo) {
    std::cout << elem.first << "\n";
    auto const &inner_map = elem.second;
    for (auto const [key, value] : inner_map) 
    {
      std::cout << key << value << "\n";
    }
  }
  return d;
}


void genptll_vs_ptll(
    int year = 2022,
    std::string process = "DY",
    std::string algo = "DeepFlavB",
    std::string const WP = "loose"
){
    dataset d = mkDataset(year);
    std::cout << d.samples[process] << "\n";
    std::cout << d.algo[algo][WP] << "\n";
    double wp = d.algo[algo][WP];

    TH1::SetDefaultSumw2(true);  
    TString fname   = "pT2Dhist_" + std::to_string(year) + "_" + process + "_" + algo + "_" + WP + ".root";
    TString samples = d.samples[process];
    TFile* outfile = new TFile(fname, "RECREATE");
    
    TChain *Events = new TChain("Events");
    Events->Add(samples);

    Events->SetBranchStatus("*", 0);
    Events->SetBranchStatus("XSWeight", 1);
    Events->SetBranchStatus("nCleanJet", 1);
    Events->SetBranchStatus("nLepton", 1);
    Events->SetBranchStatus("Lepton_pt", 1);
    Events->SetBranchStatus("Lepton_eta", 1);
    Events->SetBranchStatus("Lepton_pdgId", 1);    
    Events->SetBranchStatus("mll", 1);
    Events->SetBranchStatus("ptll", 1);
    Events->SetBranchStatus("gen_ptll", 1);
        
    double XSWeight;
    Int_t nCleanJet;
    Int_t nLepton;
    float Lepton_pt[100];
    float Lepton_eta[100];
    int   Lepton_pdgId[100];
    Double_t mll, ptll;
    float gen_ptll;

    Events->SetBranchAddress("XSWeight", &XSWeight);
    Events->SetBranchAddress("nCleanJet", &nCleanJet);
    Events->SetBranchAddress("nLepton", &nLepton);
    Events->SetBranchAddress("Lepton_pt", Lepton_pt);
    Events->SetBranchAddress("Lepton_eta", Lepton_eta);
    Events->SetBranchAddress("Lepton_pdgId", Lepton_pdgId);
    Events->SetBranchAddress("mll", &mll);
    Events->SetBranchAddress("ptll", &ptll);
    Events->SetBranchAddress("gen_ptll", &gen_ptll);
    

    /*
    ptbins follows the BTV recommendation 
    https://btv-wiki.docs.cern.ch/PerformanceCalibration/fixedWPSFRecommendations/#b-tagging-efficiencies-in-simulation
    etabins can be changed to match one's needs
    */

    Float_t ptbins[11] =  {0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100};

    TH1F *ptll_pull = new TH1F{"ptll_pull", "ptll_pull", 100, -2, 2};
    ptll_pull->GetXaxis()->SetTitle("(reco ptll - gen ptll)/gen ptll");

    TH2F *genReco_pT_0j = new TH2F{"gen_vs_reco_pt_0j", "gen_vs_reco_pt_0j", 10, ptbins, 10, ptbins};
    genReco_pT_0j->GetYaxis()->SetTitle("p_{T} [GeV]");
    genReco_pT_0j->GetXaxis()->SetTitle("gen p_{T} [GeV]");

    TH2F *genReco_pT_1j = new TH2F{"gen_vs_reco_pt_1j", "gen_vs_reco_pt_1j", 10, ptbins, 10, ptbins};
    genReco_pT_1j->GetYaxis()->SetTitle("p_{T} [GeV]");
    genReco_pT_1j->GetXaxis()->SetTitle("gen p_{T} [GeV]");

    TH2F *genReco_pT_2j = new TH2F{"gen_vs_reco_pt_2j", "gen_vs_reco_pt_2j", 10, ptbins, 10, ptbins};
    genReco_pT_2j->GetYaxis()->SetTitle("p_{T} [GeV]");
    genReco_pT_2j->GetXaxis()->SetTitle("gen p_{T} [GeV]");

    TH2F *genReco_pT_3pj = new TH2F{"gen_vs_reco_pt_3pj", "gen_vs_reco_pt_3pj", 10, ptbins, 10, ptbins};
    genReco_pT_3pj->GetYaxis()->SetTitle("p_{T} [GeV]");
    genReco_pT_3pj->GetXaxis()->SetTitle("gen p_{T} [GeV]");

    TH2F *genReco_pT_inclJets = new TH2F{"gen_vs_reco_pt_inclJets", "gen_vs_reco_pt_inclJets", 10, ptbins, 10, ptbins};
    genReco_pT_inclJets->GetYaxis()->SetTitle("p_{T} [GeV]");
    genReco_pT_inclJets->GetXaxis()->SetTitle("gen p_{T} [GeV]");
    
    int entries = Events->GetEntries();
    for (unsigned int i = 0; i < Events->GetEntries(); i ++) 
    {
      Events->GetEntry(i);
      if (i%100000 == 0) 
      {
        std::cout << "Processing entry # " << i << " : " << ((float)i+1)*100/entries << " %\n";
      }
      // Preselection of the HWW analysis, change it if needed
      if (nLepton < 2 || Lepton_pt[0] < 25 || Lepton_pt[1] < 13 || Lepton_pt[2] > 10 || abs(Lepton_eta[0]) > 2.5 || abs(Lepton_eta[1]) > 2.5 || 
        mll < 60 || mll > 120 || Lepton_pdgId[0] * Lepton_pdgId[1] != -11 * 13) 
        continue;
      
      ptll_pull->Fill((ptll - gen_ptll)/gen_ptll, XSWeight);
      genReco_pT_inclJets->Fill(gen_ptll, ptll, XSWeight);
      if (nCleanJet == 0)
      {genReco_pT_0j->Fill(gen_ptll, ptll, XSWeight);}
      else if (nCleanJet == 1)
      {genReco_pT_1j->Fill(gen_ptll, ptll, XSWeight);}
      else if (nCleanJet == 2)
      {genReco_pT_2j->Fill(gen_ptll, ptll, XSWeight);}
      else if (nCleanJet >= 3)
      {genReco_pT_3pj->Fill(gen_ptll, ptll, XSWeight);}
    }
    ptll_pull->Write();
    genReco_pT_inclJets->Write();
    genReco_pT_0j->Write();
    genReco_pT_1j->Write();
    genReco_pT_2j->Write();
    genReco_pT_3pj->Write();

    auto normalize_columns = [](TH2F *h) {
      int nx = h->GetNbinsX();
      int ny = h->GetNbinsY();
      for (int ix = 1; ix <= nx; ++ix) { // ROOT bins start at 1
        double col_sum = 0.0;
        for (int iy = 1; iy <= ny; ++iy) {
          col_sum += h->GetBinContent(ix, iy);
        }
        if (col_sum > 0) {
          for (int iy = 1; iy <= ny; ++iy) {
            double val = h->GetBinContent(ix, iy);
            h->SetBinContent(ix, iy, val / col_sum);
          }
        }
      }
    };

    auto draw_and_save = [&](TH2F *h, const char *tag) {
      normalize_columns(h);
      // gStyle->SetOptStat(0);
      TCanvas *c = new TCanvas(Form("c_%s",tag), "",800,600);
      c->cd();
      h->Draw("COLZ");
      gPad->Update(); // Ensure stat box is created
      TPaveStats *st = (TPaveStats*)h->GetListOfFunctions()->FindObject("stats");
      if (st) {
          std::cout<<" Stat box found! "<<std::endl;
          st->SetX1NDC(0.15); // left
          st->SetX2NDC(0.45); // right
          st->SetY1NDC(0.7); // top
          st->SetY2NDC(0.9); // bottom
          st->Draw();
      }
      gPad->Update(); // Ensure stat box is created
      TString cname = Form("genReco_pT2Dhist_%s_%d_%s_%s_%s.png",
                          tag, year, process.c_str(), algo.c_str(), WP.c_str());
      c->SaveAs(cname);
      delete c;
    };

    TCanvas *c1 = new TCanvas("c1", "",800,600);
    c1->cd();
    ptll_pull->Draw();
    ptll_pull->Fit("gaus"); // Fit with Gaussian
    TString cname1 = "ptll_pull_" + std::to_string(year) + "_" + process + "_" + algo + "_" + WP + ".png";
    c1->SaveAs(cname1);
    delete c1;

    draw_and_save(genReco_pT_inclJets, "inclJets");
    draw_and_save(genReco_pT_0j, "0j");
    draw_and_save(genReco_pT_1j, "1j");
    draw_and_save(genReco_pT_2j, "2j");
    draw_and_save(genReco_pT_3pj,"3pj");


}
