#include <cstdlib>
#include <iostream>
#include <string>
#include <cstring>
#include <list>
#include <algorithm>
#include <map>
#include <string_view>
#include <vector>

#include <fstream> 
#include <filesystem> 
#include <string> 

#include <math.h>
#include <dirent.h>
#include <sys/types.h>

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


/* 
This file calculates the r ratio as outlined in 
https://btv-wiki.docs.cern.ch/PerformanceCalibration/shapeCorrectionSFRecommendations/#general-information. 
Currently, it is implemented for the 2022 pre-EE era samples; however, it can be easily adapted for other eras and/or samples.
*/

std::map<std::string, std::vector<std::string>> samples = {
    {"ttbar", {"/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer22_130x_nAODv12_Full2022v12__OLD/MCl2loose2022v12__MCCorr2022v12JetScaling__l2tight/nanoLatino_TTTo2L2Nu__part*.root"}},
    {"WW", {"/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer22_130x_nAODv12_Full2022v12__OLD/MCl2loose2022v12__MCCorr2022v12JetScaling__l2tight/nanoLatino_WWTo2L2Nu__part*.root"}},
    {"DY", {"/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer22_130x_nAODv12_Full2022v12__OLD/MCl2loose2022v12__MCCorr2022v12JetScaling__l2tight/nanoLatino_DYto2L-2Jets_MLL-50__part*.root"}},
    {"WZ", {"/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer22_130x_nAODv12_Full2022v12__OLD/MCl2loose2022v12__MCCorr2022v12JetScaling__l2tight/nanoLatino_WZTo3LNu__part*.root"}},
    {"ggH", {"/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer22_130x_nAODv12_Full2022v12__OLD/MCl2loose2022v12__MCCorr2022v12JetScaling__l2tight/nanoLatino_GluGluHToWWTo2L2Nu_M125__part*.root"}},
    {"qqH", {"/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer22_130x_nAODv12_Full2022v12__OLD/MCl2loose2022v12__MCCorr2022v12JetScaling__l2tight/nanoLatino_VBFHToWWTo2L2Nu_M125__part*.root"}},
    {"tW", {
        "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer22_130x_nAODv12_Full2022v12__OLD/MCl2loose2022v12__MCCorr2022v12JetScaling__l2tight/nanoLatino_TbarWplusto2L2Nu__part*.root",
        "/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer22_130x_nAODv12_Full2022v12__OLD/MCl2loose2022v12__MCCorr2022v12JetScaling__l2tight/nanoLatino_TWminusto2L2Nu__part*.root"
    }}
};

std::map<std::string, std::map<std::string, double>> algo = {
    {"deepjet", {{"loose", 0.0583}, {"medium", 0.3086}, {"tight", 0.7183}}},
    {"partTransformer", {{"loose", 0.0849}, {"medium", 0.4319}, {"tight", 0.8482}}},
    {"partNet", {{"loose", 0.0470}, {"medium", 0.2450}, {"tight", 0.6734}}}
};


void btag_ratio(std::string process, std::string algo_name, std::string const WP) {

    // Validate process key
    if (samples.find(process) == samples.end()) {
        std::cerr << "Error: Process " << process << " not found in samples!\n";
        return;
    }

    // Validate algo_name key
    if (algo.find(algo_name) == algo.end()) {
        std::cerr << "Error: Algorithm " << algo_name << " not found in algo map!\n";
        return;
    }

    // Validate WP key, not really necessary at the moment but useful if we want to have a higher granularity in bins of btag score.
    if (algo[algo_name].find(WP) == algo[algo_name].end()) {
        std::cerr << "Error: WP " << WP << " not found for algorithm " << algo_name << "!\n";
        return;
    }

    double wp = algo[algo_name][WP];

    TH1::SetDefaultSumw2(true);
    std::vector<std::string> sample_paths = samples[process];
    std::cout << "Process: " << process << "\n";
    std::string folder_path = "btag_ratios/" + algo_name;
    std::filesystem::create_directories(folder_path);

    TString btagSF_branch = "Jet_btagSF_" + TString(algo_name) + "_shape";

    TChain *Events = new TChain("Events");
    for (const auto& path : sample_paths) {
        Events->Add(path.c_str());  
    }

    // Activate only necessary branches.
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
    Events->SetBranchStatus(btagSF_branch, 1);

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
    float Jet_btagSF_shape[100];

    Events->SetBranchAddress("XSWeight", &XSWeight);
    Events->SetBranchAddress("nCleanJet", &nCleanJet);
    Events->SetBranchAddress("CleanJet_pt", CleanJet_pt);
    Events->SetBranchAddress("CleanJet_eta", CleanJet_eta);
    Events->SetBranchAddress("CleanJet_jetIdx", CleanJet_jetIdx);
    Events->SetBranchAddress("Jet_hadronFlavour", Jet_hadronFlavour);
    Events->SetBranchAddress("nLepton", &nLepton);
    Events->SetBranchAddress("Lepton_pt", Lepton_pt);
    Events->SetBranchAddress("Lepton_eta", Lepton_eta);
    Events->SetBranchAddress("Lepton_pdgId", Lepton_pdgId);
    Events->SetBranchAddress("PuppiMET_pt", &PuppiMET_pt);
    Events->SetBranchAddress("mll", &mll);
    Events->SetBranchAddress("ptll", &ptll);
    Events->SetBranchAddress(btagSF_branch, &Jet_btagSF_shape);

    // Initialization of the total weights.
    double totalXSWeight = 0.0;
    double totalXSWeight_after = 0.0;
    double totalbXSWeight = 0.0;
    double totalcXSWeight = 0.0;
    double totallXSWeight = 0.0;
    double totalbtagWeight = 0.0;
    double totalctagWeight = 0.0;
    double totalltagWeight = 0.0;

    int entries = Events->GetEntries();

    for (unsigned int i = 0; i < entries; i++) {
        Events->GetEntry(i);
        if (i % 1000000 == 0) {
            std::cout << "Processing entry # " << i << " : " << ((float)i + 1) * 100 / entries << " %\n";
        }
        
        // Preselection of the HWW analysis, so that the calculation is done without any cut on the btag score.
        if (nLepton < 2 || Lepton_pt[0] < 25 || Lepton_pt[1] < 13 || Lepton_pt[2] > 10 ||
            Lepton_pdgId[0] * Lepton_pdgId[1] != -11 * 13 || PuppiMET_pt < 20 || mll < 12 || ptll < 30) 
            continue;
        

        double event_btagSF = 1.0, event_ctagSF = 1.0, event_ltagSF = 1.0, event_SF = 1.0;
        bool hasBjet = false, hasCjet = false, hasLjet = false;
        
        // The loop is done over all jets of an event and is split in jet flavour.
        // An overall calculation without this split is also performed.

        for (int j = 0; j < nCleanJet; j++)
        {
            int flavour = Jet_hadronFlavour[CleanJet_jetIdx[j]];
            double sf = Jet_btagSF_shape[CleanJet_jetIdx[j]];
            
            if (sf != 0) {
                // If an event has a b jet, its weight account to the total b-tag weight.
                if (flavour == 5) 
                {
                    hasBjet = true;
                    event_btagSF *= sf;
                }
                // If an event has a c jet, its weight account to the total c-tag weight.
                else if (flavour == 4) 
                {
                    hasCjet = true;
                    event_ctagSF *= sf;
                } 
                // If an event has a light jet, its weight account to the total light-tag weight.
                else if (flavour == 0) 
                {
                    hasLjet = true;
                    event_ltagSF *= sf;
                }
                //No selection per jet flavour in this last case.
                event_SF *= sf;
            }
        }
        
        // See comments inside the sf!=0 condition
        if (hasBjet)
        {
            totalbXSWeight += XSWeight;
            totalbtagWeight += XSWeight * event_btagSF;
        }
        if (hasCjet)
        {
            totalcXSWeight += XSWeight;
            totalctagWeight += XSWeight * event_ctagSF;
        }

        if (hasLjet)
        {
            totallXSWeight += XSWeight;
            totalltagWeight += XSWeight * event_ltagSF;
        }
        totalXSWeight += XSWeight;
        totalXSWeight_after += XSWeight * event_SF;
    
}

    // Print the ratios and save them in a .txt file.
    std::string filename = folder_path + "/" + process + "_" + algo_name + "_ratio.txt";
    std::ofstream outfile(filename);

    std::cout << "#### PROCESS : " << process << std::endl;
    std::cout << "#### ALGO : " << algo_name << std::endl;
    std::cout << "Total XSWeight no flavour: " << totalXSWeight << std::endl;
    std::cout << "Total XSWeight no flavour after: " << totalXSWeight_after << std::endl;
    std::cout << "Total bXSWeight: " << totalbXSWeight << std::endl;
    std::cout << "Total cXSWeight: " << totalcXSWeight << std::endl;
    std::cout << "Total lXSWeight: " << totallXSWeight << std::endl;
    std::cout << "Total btagWeight: " << totalbtagWeight << std::endl;
    std::cout << "Total ctagWeight: " << totalctagWeight << std::endl;
    std::cout << "Total ltagWeight: " << totalltagWeight << std::endl;
    std::cout << "Total ltagWeight: " << totalltagWeight << std::endl;
    std::cout << "Ratio totalXS: " << totalXSWeight/totalXSWeight_after << std::endl;
    std::cout << "Ratio bXSWeight/btagWeight: " << totalbXSWeight/totalbtagWeight << std::endl;
    std::cout << "Ratio cXSWeight/ctagWeight: " << totalcXSWeight/totalctagWeight << std::endl;
    std::cout << "Ratio lXSWeight/ltagWeight: " << totallXSWeight/totalltagWeight << std::endl;

    outfile << "#### PROCESS : " << process << std::endl;
    outfile << "#### ALGO : " << algo_name << std::endl;
    outfile << "Total XSWeight no flavour: " << totalXSWeight << std::endl;
    outfile << "Total XSWeight no flavour after: " << totalXSWeight_after << std::endl;
    outfile << "Total XSWeight no selection: " << totalXSWeight << std::endl;
    outfile << "Total bXSWeight: " << totalbXSWeight << std::endl;
    outfile << "Total cXSWeight: " << totalcXSWeight << std::endl;
    outfile << "Total lXSWeight: " << totallXSWeight << std::endl;
    outfile << "Total btagWeight: " << totalbtagWeight << std::endl;
    outfile << "Total ctagWeight: " << totalctagWeight << std::endl;
    outfile << "Total ltagWeight: " << totalltagWeight << std::endl;
    outfile << "Ratio totalXS: " << totalXSWeight/totalXSWeight_after << std::endl;
    outfile << "Ratio bXSWeight/btagWeight: " << totalbXSWeight/totalbtagWeight << std::endl;
    outfile << "Ratio cXSWeight/ctagWeight: " << totalcXSWeight/totalctagWeight << std::endl;
    outfile << "Ratio lXSWeight/ltagWeight: " << totallXSWeight/totalltagWeight << std::endl;
}