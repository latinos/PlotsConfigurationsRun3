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
  if (year == 2022) 
  {
    d.samples = 
    {
        {"ttbar" , "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer22_130x_nAODv12_Full2022v12__OLD/MCl2loose2022v12__MCCorr2022v12JetScaling__l2tight/nanoLatino_TTTo2L2Nu__part*.root"},
        {"WW" , "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer22_130x_nAODv12_Full2022v12__OLD/MCl2loose2022v12__MCCorr2022v12JetScaling__l2tight/nanoLatino_WWTo2L2Nu__part*.root"},
        {"DY" , "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer22_130x_nAODv12_Full2022v12__OLD/MCl2loose2022v12__MCCorr2022v12JetScaling__l2tight/nanoLatino_DYto2L-2Jets_MLL-50__part*.root"}
    };
    d.algo = 
    {
        {"DeepFlavB", {{"loose" , 0.0583}, {"medium" , 0.3086}, {"tight" , 0.7183}}},
        {"RobustParTAK4B", {{"loose", 0.0849}, {"medium", 0.4319}, {"tight", 0.8482}}},
        {"PNetB", {{"loose", 0.0470}, {"medium", 0.2450}, {"tight", 0.6734}}}
    };
  }
  else if (year == 20222) 
  {
    d.samples = 
    {
        {"ttbar" , "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer22EE_130x_nAODv12_Full2022v12__OLD/MCl2loose2022EEv12__MCCorr2022EEv12JetScaling__l2tight/nanoLatino_TTTo2L2Nu__part*.root"},
        {"WW" , "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer22EE_130x_nAODv12_Full2022v12__OLD/MCl2loose2022EEv12__MCCorr2022EEv12JetScaling__l2tight/nanoLatino_WWTo2L2Nu__part*.root"},
        { "DY" , "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer22EE_130x_nAODv12_Full2022v12__OLD/MCl2loose2022EEv12__MCCorr2022EEv12JetScaling__l2tight/nanoLatino_DYto2L-2Jets_MLL-50__part*.root"}
    };
    d.algo = 
    {
        {"DeepFlavB", {{"loose" , 0.0614}, {"medium" , 0.3196}, {"tight" , 	0.7300}}},
        {"RobustParTAK4B",{{"loose", 0.0897}, {"medium", 	0.4510}, {"tight", 0.8604}}},
        {"PNetB",{{"loose", 0.0499}, {"medium", 0.2605}, {"tight", 0.6915}}}
    };
  }

  for (auto const &elem : d.algo) 
  {
    std::cout << elem.first << "\n";
    auto const &inner_map = elem.second;
    for (auto const [key, value] : inner_map) 
    {
      std::cout << key << value << "\n";
    }
  }
  return d;
}


void bTagEff(int year, std::string process, std::string algo, std::string const WP) 
{
    dataset d = mkDataset(year);
    std::cout << d.samples[process] << "\n";
    std::cout << d.algo[algo][WP] << "\n";
    double wp = d.algo[algo][WP];

    TH1::SetDefaultSumw2(true);  
    TString fname   = "bTagEff_" + std::to_string(year) + "_" + process + "_" + algo + "_" + WP + ".root";
    std::filesystem::create_directories("efficiencies");
    TString samples = d.samples[process];
    TString btag    = "Jet_btag" + algo;
    TFile* outfile = new TFile(fname, "RECREATE");
    
    TChain *Events = new TChain("Events");
    Events->Add(samples);

    Events->SetBranchStatus("*", 0);
    Events->SetBranchStatus("XSWeight", 1);
    Events->SetBranchStatus("nCleanJet", 1);
    Events->SetBranchStatus("CleanJet_pt", 1);
    Events->SetBranchStatus("CleanJet_eta", 1);
    Events->SetBranchStatus("CleanJet_jetIdx", 1);
    Events->SetBranchStatus("Jet_hadronFlavour", 1);
    Events->SetBranchStatus("nLepton", 1);
    Events->SetBranchStatus("Lepton_pt", 1);
    Events->SetBranchStatus("Lepton_eta", 1);
    Events->SetBranchStatus("Lepton_pdgId", 1);    
    Events->SetBranchStatus("PuppiMET_pt", 1);
    Events->SetBranchStatus("mll", 1);
    Events->SetBranchStatus("ptll", 1);
        
    double XSWeight;
    Int_t nCleanJet;
    float CleanJet_pt[100];
    float CleanJet_eta[100];
    ULong64_t   CleanJet_jetIdx[100];
    char   Jet_hadronFlavour[100];
    float Jet_btag[100];
    
    Int_t nLepton;
    float Lepton_pt[100];
    float Lepton_eta[100];
    int   Lepton_pdgId[100];
    Float_t PuppiMET_pt;
    Double_t mll, ptll;

    Events->SetBranchAddress("XSWeight", &XSWeight);
    Events->SetBranchAddress("nCleanJet", &nCleanJet);
    Events->SetBranchAddress("CleanJet_pt", CleanJet_pt);
    Events->SetBranchAddress("CleanJet_eta", CleanJet_eta);
    Events->SetBranchAddress("CleanJet_jetIdx", CleanJet_jetIdx);
    Events->SetBranchAddress("Jet_hadronFlavour", Jet_hadronFlavour);
    Events->SetBranchAddress(btag, Jet_btag);


    Events->SetBranchAddress("nLepton", &nLepton);
    Events->SetBranchAddress("Lepton_pt", Lepton_pt);
    Events->SetBranchAddress("Lepton_eta", Lepton_eta);
    Events->SetBranchAddress("Lepton_pdgId", Lepton_pdgId);
    Events->SetBranchAddress("PuppiMET_pt", &PuppiMET_pt);
    Events->SetBranchAddress("mll", &mll);
    Events->SetBranchAddress("ptll", &ptll);

    /*
    ptbins follows the BTV recommendation 
    https://btv-wiki.docs.cern.ch/PerformanceCalibration/fixedWPSFRecommendations/#b-tagging-efficiencies-in-simulation
    etabins can be changed to match one's needs
    */

    Float_t ptbins[10] =  {20, 30, 50, 70, 100, 140, 200, 300, 600, 1000};
    Float_t etabins[4] =  {-2.5, -1.479, 1.479, 2.5};
    
    TH2F *bjet_den = new TH2F{"bjet_den", "bjet_den", 9, ptbins, 3, etabins};
    bjet_den->GetXaxis()->SetTitle("p_{T} [GeV]");
    bjet_den->GetYaxis()->SetTitle("#eta");
    
    TH2F *bjet_num = new TH2F{"bjet_num", "bjet_num", 9, ptbins, 3, etabins};
    bjet_num->GetXaxis()->SetTitle("p_{T} [GeV]");
    bjet_num->GetYaxis()->SetTitle("#eta");

    TH2F *cjet_den = new TH2F{"cjet_den", "cjet_den", 9, ptbins, 3, etabins};
    cjet_den->GetXaxis()->SetTitle("p_{T} [GeV]");
    cjet_den->GetYaxis()->SetTitle("#eta");
    
    TH2F *cjet_num = new TH2F{"cjet_num", "cjet_num", 9, ptbins, 3, etabins};
    cjet_num->GetXaxis()->SetTitle("p_{T} [GeV]");
    cjet_num->GetYaxis()->SetTitle("#eta");

    TH2F *ljet_den = new TH2F{"ljet_den", "ljet_den", 9, ptbins, 3, etabins};
    ljet_den->GetXaxis()->SetTitle("p_{T} [GeV]");
    ljet_den->GetYaxis()->SetTitle("#eta");
    
    TH2F *ljet_num = new TH2F{"ljet_num", "ljet_num", 9, ptbins, 3, etabins};
    ljet_num->GetXaxis()->SetTitle("p_{T} [GeV]");
    ljet_num->GetYaxis()->SetTitle("#eta");

    
    int entries = Events->GetEntries();
    for (unsigned int i = 0; i < Events->GetEntries(); i ++) 
    {
      Events->GetEntry(i);
      if (i%1000000 == 0) 
      {
        std::cout << "Processing entry # " << i << " : " << ((float)i+1)*100/entries << " %\n";
      }
      // Preselection of the HWW analysis, change it if needed
      if (nLepton < 2 || Lepton_pt[0] < 25 || Lepton_pt[1] < 13 || Lepton_pt[2] > 10 ||
        Lepton_pdgId[0] * Lepton_pdgId[1] != -11 * 13 || PuppiMET_pt < 20 || mll < 12 || ptll < 30) 
        continue;
      
      for (unsigned int jet = 0; jet < nCleanJet; jet++) 
      {
        // b-jet
        if (Jet_hadronFlavour[CleanJet_jetIdx[jet]] == 5) 
        {
          bjet_den->Fill(CleanJet_pt[jet], CleanJet_eta[jet], XSWeight);
          // looser b-tag score related selection in the analysis, in our case bVeto selection
          if (CleanJet_pt[jet] > 20 && abs(CleanJet_eta[jet]) < 2.5 && Jet_btag[CleanJet_jetIdx[jet]] > wp) 
          { 
            bjet_num->Fill(CleanJet_pt[jet], CleanJet_eta[jet], XSWeight);
          }
        }
        // c-jet
        if (Jet_hadronFlavour[CleanJet_jetIdx[jet]] == 4) 
        {
          cjet_den->Fill(CleanJet_pt[jet], CleanJet_eta[jet], XSWeight);
          if (CleanJet_pt[jet] > 20 && abs(CleanJet_eta[jet]) < 2.5 && Jet_btag[CleanJet_jetIdx[jet]] > wp) 
          { 
            cjet_num->Fill(CleanJet_pt[jet], CleanJet_eta[jet], XSWeight);
          }
        }
        // light-jet
        if (Jet_hadronFlavour[CleanJet_jetIdx[jet]] == 0) 
        {
          ljet_den->Fill(CleanJet_pt[jet], CleanJet_eta[jet], XSWeight);
          if (CleanJet_pt[jet] > 20 && abs(CleanJet_eta[jet]) < 2.5 && Jet_btag[CleanJet_jetIdx[jet]] > wp)
          { 
            ljet_num->Fill(CleanJet_pt[jet], CleanJet_eta[jet], XSWeight);
          }
        }
      }
    }
    // Plotting and saving
    gStyle->SetPaintTextFormat("2.3f");
    gStyle->SetOptStat("000000000");
    TCanvas *c = new TCanvas();
    //c->cd();
    gPad = c->cd(1);
    gPad->SetLogx();

    bjet_den->Write();
    bjet_num->Write();
    TH2F* bjet_eff = (TH2F*) bjet_num->Clone("bjet_eff");
    bjet_eff->SetTitle("bjet efficiency");
    bjet_eff->Divide(bjet_den);
    bjet_eff->Draw("colz E TEXT");
    //gPad->SetLogX();
    TString cname = "efficiencies/bjet_eff_" + std::to_string(year) + "_" + process + "_" + algo + "_" + WP + ".png";
    c->SaveAs(cname);
    bjet_eff->Write();
    
    cjet_den->Write();
    cjet_num->Write();
    TH2F* cjet_eff = (TH2F*) cjet_num->Clone("cjet_eff");
    cjet_eff->SetTitle("cjet efficiency");
    cjet_eff->Divide(cjet_den);
    cjet_eff->Draw("colz E TEXT");
    cname = "efficiencies/cjet_eff_" + std::to_string(year) + "_" + process + "_" + algo + "_" + WP + ".png";
    c->SaveAs(cname);
    cjet_eff->Write();
    
    ljet_den->Write();
    ljet_num->Write();
    TH2F* ljet_eff = (TH2F*) ljet_num->Clone("ljet_eff");
    ljet_eff->SetTitle("ljet efficiency");
    ljet_eff->Divide(ljet_den);
    ljet_eff->Draw("colz E TEXT");
    cname = "efficiencies/ljet_eff_" + std::to_string(year) + "_"  + process + "_" + algo + "_" + WP + ".png";
    c->SaveAs(cname);
    ljet_eff->Write();
    
    outfile->Close();
}
