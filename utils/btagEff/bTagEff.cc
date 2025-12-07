#include <cstdlib>
#include <iostream>
#include <string>
#include <map>
#include <filesystem>

#include "TH1.h"
#include "TH2.h"
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TChain.h"
#include "TCanvas.h"
#include "TStyle.h"

struct dataset {
    int year;
    std::map<std::string, std::string> samples;
    std::map<std::string, std::map<std::string, double>> algo;
};

// Manteniamo la tua definizione dei samples così com’è
dataset mkDataset(int year) {
    TH1::SetDefaultSumw2(true);
    dataset d;
    d.year = year;
  if (year == 2022) 
  {
    d.samples = 
    {
        {"ttbar" , "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer22_130x_nAODv12_Full2022v12/MCl2loose2022v12__MCCorr2022v12JetScaling__l2tight/nanoLatino_TTTo2L2Nu__part*.root"},
        {"tW" , "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer22_130x_nAODv12_Full2022v12/MCl2loose2022v12__MCCorr2022v12JetScaling__l2tight/nanoLatino_TWminusto2L2Nu__part*.root"},
        {"WW" , "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer22_130x_nAODv12_Full2022v12/MCl2loose2022v12__MCCorr2022v12JetScaling__l2tight/nanoLatino_WWTo2L2Nu__part*.root"},
        {"DY" , "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer22_130x_nAODv12_Full2022v12/MCl2loose2022v12__MCCorr2022v12JetScaling__l2tight/nanoLatino_DYto2L-2Jets_MLL-50__part*.root"}
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
        {"ttbar" , "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer22EE_130x_nAODv12_Full2022v12/MCl2loose2022EEv12__MCCorr2022EEv12JetScaling__l2tight/nanoLatino_TTTo2L2Nu__part*.root"},
        {"WW" , "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer22EE_130x_nAODv12_Full2022v12/MCl2loose2022EEv12__MCCorr2022EEv12JetScaling__l2tight/nanoLatino_WWTo2L2Nu__part*.root"},
        { "DY" , "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer22EE_130x_nAODv12_Full2022v12/MCl2loose2022EEv12__MCCorr2022EEv12JetScaling__l2tight/nanoLatino_DYto2L-2Jets_MLL-50__part*.root"}
    };
    d.algo = 
    {
        {"DeepFlavB", {{"loose" , 0.0614}, {"medium" , 0.3196}, {"tight" , 	0.7300}}},
        {"RobustParTAK4B",{{"loose", 0.0897}, {"medium", 	0.4510}, {"tight", 0.8604}}},
        {"PNetB",{{"loose", 0.0499}, {"medium", 0.2605}, {"tight", 0.6915}}}
    };
  }
  else if (year == 2023) 
  {
    d.samples = 
    {
        {"ttbar" , "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer23_130x_nAODv12_Full2023v12/MCl2loose2023v12__MCCorr2023v12JetScaling__l2tight/nanoLatino_TTTo2L2Nu__part*.root"},
        {"tW" , "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer23_130x_nAODv12_Full2023v12/MCl2loose2023v12__MCCorr2023v12JetScaling__l2tight/nanoLatino_TWminusto2L2Nu__part*.root"},
        {"WW" , "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer23_130x_nAODv12_Full2023v12/MCl2loose2023v12__MCCorr2023v12JetScaling__l2tight/nanoLatino_WWTo2L2Nu__part*.root"},
        {"DY" , "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer23_130x_nAODv12_Full2023v12/MCl2loose2023v12__MCCorr2023v12JetScaling__l2tight/nanoLatino_DYto2L-2Jets_MLL-50__part*.root"}
    };
    d.algo = 
    {
        {"DeepFlavB", {{"loose" , 0.0479}, {"medium" , 0.2431}, {"tight" , 0.6553}}},
        {"RobustParTAK4B", {{"loose", 0.0681}, {"medium", 0.3487}, {"tight", 	0.7969}}},
        {"PNetB", {{"loose", 0.0358}, {"medium", 0.1917}, {"tight", 0.6172}}}
    };
  }
  else if (year == 20232) 
  {
    d.samples = 
    {
        {"ttbar" , "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer23BPix_130x_nAODv12_Full2023BPixv12/MCl2loose2023BPixv12__MCCorr2023BPixv12JetScaling__l2tight/nanoLatino_TTTo2L2Nu__part*.root"},
        {"tW" , "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer23BPix_130x_nAODv12_Full2023BPixv12/MCl2loose2023BPixv12__MCCorr2023BPixv12JetScaling__l2tight/nanoLatino_TWminusto2L2Nu__part*.root"},
        {"WW" , "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer23BPix_130x_nAODv12_Full2023BPixv12/MCl2loose2023BPixv12__MCCorr2023BPixv12JetScaling__l2tight/nanoLatino_WWTo2L2Nu__part*.root"},
        {"DY" , "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer23BPix_130x_nAODv12_Full2023BPixv12/MCl2loose2023BPixv12__MCCorr2023BPixv12JetScaling__l2tight/nanoLatino_DYto2L-2Jets_MLL-50__part*.root"}
    };
    d.algo = 
    {
        {"DeepFlavB", {{"loose" , 0.0480}, {"medium" , 0.2435}, {"tight" , 0.6563}}},
        {"RobustParTAK4B", {{"loose", 0.0683}, {"medium", 0.3494}, {"tight", 0.7994}}},
        {"PNetB", {{"loose", 0.0359}, {"medium", 0.1919}, {"tight", 0.6133}}}
    };
  }
  else if (year == 2024) 
  {
  d.samples = 
    {
        {"ttbar" , "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer24_150x_nAODv15_Full2024v15/MCl2loose2024v15__MCCorr2024v15__JERFrom23BPix__l2tight/nanoLatino_TTTo2L2Nu__part*.root"},
        {"tW" , "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer23BPix_130x_nAODv12_Full2023BPixv12/MCl2loose2023BPixv12__MCCorr2023BPixv12JetScaling__l2tight/nanoLatino_TWminusto2L2Nu__part*.root"},
        {"WW" , "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer23BPix_130x_nAODv12_Full2023BPixv12/MCl2loose2023BPixv12__MCCorr2023BPixv12JetScaling__l2tight/nanoLatino_WWTo2L2Nu__part*.root"},
        {"DY" , "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer23BPix_130x_nAODv12_Full2023BPixv12/MCl2loose2023BPixv12__MCCorr2023BPixv12JetScaling__l2tight/nanoLatino_DYto2L-2Jets_MLL-50__part*.root"}
    };
    d.algo = 
    {
        {"UParTAK4", {{"loose" , 0.0246}, {"medium" , 0.1272}, {"tight" , 0.4648}}},
        {"RobustParTAK4B", {{"loose", 0.0683}, {"medium", 0.3494}, {"tight", 0.7994}}},
        {"PNetB", {{"loose", 0.0359}, {"medium", 0.1919}, {"tight", 0.6133}}}
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

void bTagEff(int year, std::string process, std::string algo, std::string WP) {
    dataset d = mkDataset(year);
    double wp = d.algo[algo][WP];

    TH1::SetDefaultSumw2(true);

    // Creazione directory base su eos
    std::string outdir = "/eos/user/s/squinto/btag/" + std::to_string(year) + "/";
    std::filesystem::create_directories(outdir + "efficiencies");

    std::string fname = outdir + "bTagEff_" + std::to_string(year) + "_" + process + "_" + algo + "_" + WP + ".root";
    TString samples = d.samples[process];
    TString btag = "Jet_btag" + algo;

    TFile* outfile = new TFile(fname.c_str(), "RECREATE");
    TChain *Events = new TChain("Events");
    Events->Add(samples);

    // Branches
    Events->SetBranchStatus("*",0);
    Events->SetBranchStatus("XSWeight",1);
    Events->SetBranchStatus("nCleanJet",1);
    Events->SetBranchStatus("CleanJet_pt",1);
    Events->SetBranchStatus("CleanJet_eta",1);
    Events->SetBranchStatus("CleanJet_jetIdx",1);
    Events->SetBranchStatus("Jet_hadronFlavour",1);
    Events->SetBranchStatus(btag,1);

    Events->SetBranchStatus("nLepton",1);
    Events->SetBranchStatus("Lepton_pt",1);
    Events->SetBranchStatus("Lepton_eta",1);
    Events->SetBranchStatus("Lepton_pdgId",1);
    Events->SetBranchStatus("PuppiMET_pt",1);
    Events->SetBranchStatus("mll",1);
    Events->SetBranchStatus("ptll",1);

    double XSWeight;
    Int_t nCleanJet;
    float CleanJet_pt[100];
    float CleanJet_eta[100];
    ULong64_t CleanJet_jetIdx[100];
    char Jet_hadronFlavour[100];
    float Jet_btag[100];

    Int_t nLepton;
    float Lepton_pt[100];
    float Lepton_eta[100];
    int Lepton_pdgId[100];
    Float_t PuppiMET_pt;
    Double_t mll, ptll;

    Events->SetBranchAddress("XSWeight",&XSWeight);
    Events->SetBranchAddress("nCleanJet",&nCleanJet);
    Events->SetBranchAddress("CleanJet_pt",CleanJet_pt);
    Events->SetBranchAddress("CleanJet_eta",CleanJet_eta);
    Events->SetBranchAddress("CleanJet_jetIdx",CleanJet_jetIdx);
    Events->SetBranchAddress("Jet_hadronFlavour",Jet_hadronFlavour);
    Events->SetBranchAddress(btag,Jet_btag);

    Events->SetBranchAddress("nLepton",&nLepton);
    Events->SetBranchAddress("Lepton_pt",Lepton_pt);
    Events->SetBranchAddress("Lepton_eta",Lepton_eta);
    Events->SetBranchAddress("Lepton_pdgId",Lepton_pdgId);
    Events->SetBranchAddress("PuppiMET_pt",&PuppiMET_pt);
    Events->SetBranchAddress("mll",&mll);
    Events->SetBranchAddress("ptll",&ptll);

    Float_t ptbins[10] = {20,30,50,70,100,140,200,300,600,1000};
    Float_t etabins[4] = {-2.5,-1.479,1.479,2.5};

    TH2F *bjet_den = new TH2F("bjet_den","bjet_den",9,ptbins,3,etabins);
    TH2F *bjet_num = new TH2F("bjet_num","bjet_num",9,ptbins,3,etabins);
    TH2F *cjet_den = new TH2F("cjet_den","cjet_den",9,ptbins,3,etabins);
    TH2F *cjet_num = new TH2F("cjet_num","cjet_num",9,ptbins,3,etabins);
    TH2F *ljet_den = new TH2F("ljet_den","ljet_den",9,ptbins,3,etabins);
    TH2F *ljet_num = new TH2F("ljet_num","ljet_num",9,ptbins,3,etabins);

    // Fill
    int entries = Events->GetEntries();
    for(int i=0;i<entries;i++){
        Events->GetEntry(i);

        if(nLepton<2 || Lepton_pt[0]<25 || Lepton_pt[1]<13 || Lepton_pt[2]>10 ||
           Lepton_pdgId[0]*Lepton_pdgId[1]!=-11*13 || PuppiMET_pt<20 || mll<12 || ptll<30)
            continue;

        for(int j=0;j<nCleanJet;j++){
            // b
            if(Jet_hadronFlavour[CleanJet_jetIdx[j]]==5){
                bjet_den->Fill(CleanJet_pt[j],CleanJet_eta[j],XSWeight);
                if(CleanJet_pt[j]>20 && std::abs(CleanJet_eta[j])<2.5 && Jet_btag[CleanJet_jetIdx[j]]>wp)
                    bjet_num->Fill(CleanJet_pt[j],CleanJet_eta[j],XSWeight);
            }
            // c
            if(Jet_hadronFlavour[CleanJet_jetIdx[j]]==4){
                cjet_den->Fill(CleanJet_pt[j],CleanJet_eta[j],XSWeight);
                if(CleanJet_pt[j]>20 && std::abs(CleanJet_eta[j])<2.5 && Jet_btag[CleanJet_jetIdx[j]]>wp)
                    cjet_num->Fill(CleanJet_pt[j],CleanJet_eta[j],XSWeight);
            }
            // l
            if(Jet_hadronFlavour[CleanJet_jetIdx[j]]==0){
                ljet_den->Fill(CleanJet_pt[j],CleanJet_eta[j],XSWeight);
                if(CleanJet_pt[j]>20 && std::abs(CleanJet_eta[j])<2.5 && Jet_btag[CleanJet_jetIdx[j]]>wp)
                    ljet_num->Fill(CleanJet_pt[j],CleanJet_eta[j],XSWeight);
            }
        }
    }

    // Efficienze
    gStyle->SetPaintTextFormat("2.3f");
    gStyle->SetOptStat(0);

    TCanvas *c = new TCanvas("c","c",800,600);

    auto draw_eff = [&](TH2F* num, TH2F* den, const std::string &flavour){
        TH2F* eff = (TH2F*) num->Clone((flavour+"_eff").c_str());
        eff->Divide(den);

        c->cd();
        gPad->SetLogx();
        eff->Draw("colz E TEXT");

        std::string cname = outdir + "efficiencies/" + flavour + "_eff_" +
                            std::to_string(year) + "_" + process + "_" + algo + "_" + WP + ".png";
        c->SaveAs(cname.c_str());
        eff->Write();
    };

    bjet_den->Write(); bjet_num->Write();
    cjet_den->Write(); cjet_num->Write();
    ljet_den->Write(); ljet_num->Write();

    draw_eff(bjet_num,bjet_den,"bjet");
    draw_eff(cjet_num,cjet_den,"cjet");
    draw_eff(ljet_num,ljet_den,"ljet");

    outfile->Close();
}

int main(int argc,char** argv){
    if(argc<5){
        std::cerr<<"Usage: "<<argv[0]<<" <year> <process> <algo> <WP>\n";
        return 1;
    }
    int year = std::atoi(argv[1]);
    std::string process = argv[2];
    std::string algo = argv[3];
    std::string WP = argv[4];

    bTagEff(year,process,algo,WP);
    return 0;
}
