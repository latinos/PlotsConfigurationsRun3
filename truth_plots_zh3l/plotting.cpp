#include <sstream>
#include <vector>
#include <string>
#include <fstream>
#include <iostream>
#include <algorithm>
#include <map>
#include <cmath>
#include "TFile.h"
#include "TH1D.h"
#include "TCanvas.h"
#include "TLegend.h"
#include "TLatex.h"
#include "TStyle.h"
#include "TSystem.h"
#include "TGraphAsymmErrors.h"
// Many modern ROOT environments bundle this. If not, download json.hpp
#include <nlohmann/json.hpp> 

using json = nlohmann::json;

const char* qqZH_refinedWs = "/eos/user/d/dshekar/MCsamplesForBDTzh3l/Summer22EE_130x_nAODv12_Full2022v12/MCl2loose2022EEv12__MCCorr2022EEv12JetScaling__l2tight/GluGluZH_Zto2L_Hto2WtoLNu2Q_results/reco_plots_refinedWHadReco-cutFlow.root";
const char* ggZH_refinedWs = "/eos/user/d/dshekar/MCsamplesForBDTzh3l/Summer22EE_130x_nAODv12_Full2022v12/MCl2loose2022EEv12__MCCorr2022EEv12JetScaling__l2tight/ZH_Zto2L_Hto2WtoLNu2Q_results/reco_plots_refinedWHadReco-cutFlow.root";
const char* WZ_refinedWs = "/eos/user/d/dshekar/MCsamplesForBDTzh3l/Summer22EE_130x_nAODv12_Full2022v12/MCl2loose2022EEv12__MCCorr2022EEv12JetScaling__l2tight/WZ_results/reco_plots_refinedWHadReco-cutFlow.root";

const char* qqZH_normalWs  = "/eos/user/d/dshekar/MCsamplesForBDTzh3l/Summer22EE_130x_nAODv12_Full2022v12/MCl2loose2022EEv12__MCCorr2022EEv12JetScaling__l2tight/GluGluZH_Zto2L_Hto2WtoLNu2Q_results/reco_plots_normalWHadReco-cutFlow.root";
const char* ggZH_normalWs  = "/eos/user/d/dshekar/MCsamplesForBDTzh3l/Summer22EE_130x_nAODv12_Full2022v12/MCl2loose2022EEv12__MCCorr2022EEv12JetScaling__l2tight/ZH_Zto2L_Hto2WtoLNu2Q_results/reco_plots_normalWHadReco-cutFlow.root";
const char* WZ_normalWs = "/eos/user/d/dshekar/MCsamplesForBDTzh3l/Summer22EE_130x_nAODv12_Full2022v12/MCl2loose2022EEv12__MCCorr2022EEv12JetScaling__l2tight/WZ_results/reco_plots_normalWHadReco-cutFlow.root";

void setHistStyle(TH1D* h, int color, int style)
{
    h->SetDirectory(nullptr);
    h->SetStats(0);
    h->SetLineColor(color);
    h->SetLineStyle(style);
    h->SetLineWidth(2);
}

TH1D* getHist(TFile* f, const char* name, const char* cloneName)
{
    TH1D* h = (TH1D*)f->Get(name);
    if (!h) {
        std::cerr << "Missing histogram: " << name << " in file " << f->GetName() << std::endl;
        return nullptr;
    }
    TH1D* hc = (TH1D*)h->Clone(cloneName);
    hc->SetDirectory(nullptr);
    return hc;
}

void plotOne(
    TFile* f_qq_ref,
    TFile* f_gg_ref,
    TFile* f_wz_ref,
    TFile* f_qq_norm,
    TFile* f_gg_norm,
    TFile* f_wz_norm,
    const char* hname
)
{
    TH1D* h_qq_ref  = getHist(f_qq_ref,  hname, "h_qq_ref");
    TH1D* h_gg_ref  = getHist(f_gg_ref,  hname, "h_gg_ref");
    TH1D* h_wz_ref  = getHist(f_wz_ref,  hname, "h_wz_ref");
    TH1D* h_qq_norm = getHist(f_qq_norm, hname, "h_qq_norm");
    TH1D* h_gg_norm = getHist(f_gg_norm, hname, "h_gg_norm");
    TH1D* h_wz_norm = getHist(f_wz_norm, hname, "h_wz_norm");

    if (!h_qq_ref || !h_gg_ref || !h_qq_norm || !h_gg_norm || !h_wz_norm || !h_wz_ref) return;
    TH1D* h_qq_ref_plot = (TH1D*)h_qq_ref->Clone("h_qq_ref_plot");
    TH1D* h_gg_ref_plot = (TH1D*)h_gg_ref->Clone("h_gg_ref_plot");
    TH1D* h_wz_ref_plot = (TH1D*)h_wz_ref->Clone("h_wz_ref_plot");
    TH1D* h_qq_norm_plot = (TH1D*)h_qq_norm->Clone("h_qq_norm_plot");
    TH1D* h_gg_norm_plot = (TH1D*)h_gg_norm->Clone("h_gg_norm_plot");
    TH1D* h_wz_norm_plot = (TH1D*)h_wz_norm->Clone("h_wz_norm_plot");

    auto norm = [](TH1D* h) {
        double integral = h->Integral();
        if (integral > 0) h->Scale(1.0 / integral);
        else std::cerr << "Warning: Histogram " << h->GetName() << " has zero integral, cannot normalize." << std::endl;
    };

    norm(h_qq_ref_plot);
    norm(h_gg_ref_plot);
    norm(h_wz_ref_plot);
    norm(h_qq_norm_plot);
    norm(h_gg_norm_plot);
    norm(h_wz_norm_plot);

    setHistStyle(h_qq_ref_plot, kRed+1, 1);
    setHistStyle(h_gg_ref_plot, kBlue+1, 1);
    setHistStyle(h_wz_ref_plot, kGreen+2, 1);
    setHistStyle(h_qq_norm_plot, kRed+1, 2);
    setHistStyle(h_gg_norm_plot, kBlue+1, 2);
    setHistStyle(h_wz_norm_plot, kGreen+2, 2);

    double ymax = std::max({
        h_qq_ref_plot->GetMaximum(),
        h_gg_ref_plot->GetMaximum(),
        h_wz_ref_plot->GetMaximum(),
        h_qq_norm_plot->GetMaximum(),
        h_gg_norm_plot->GetMaximum(),
        h_wz_norm_plot->GetMaximum()
    });

    TCanvas* c = new TCanvas(Form("c_%s", hname), hname, 800, 700);

    c->SetTopMargin(0.08);
    c->SetRightMargin(0.05);
    c->SetLeftMargin(0.12);
    c->SetBottomMargin(0.12);

    h_qq_ref_plot->SetMaximum(1.25 * ymax);
    h_qq_ref_plot->SetMinimum(0.0);
    h_qq_ref_plot->SetTitle(Form("%s;Bins;Normalized events", hname));

    // h_qq_ref_plot->SetStats(0);
    // h_gg_ref_plot->SetStats(0);
    // h_wz_ref_plot->SetStats(0);
    // h_qq_norm_plot->SetStats(0);
    // h_gg_norm_plot->SetStats(0);
    // h_wz_norm_plot->SetStats(0);
    h_qq_ref_plot->Draw("hist");
    h_gg_ref_plot->Draw("hist same");
    h_wz_ref_plot->Draw("hist same");
    h_qq_norm_plot->Draw("hist same");
    h_gg_norm_plot->Draw("hist same");
    h_wz_norm_plot->Draw("hist same");

    TLegend* leg = new TLegend(0.55, 0.65, 0.88, 0.88);
    leg->SetBorderSize(0);
    leg->SetFillStyle(0);
    leg->AddEntry(h_qq_ref_plot, Form("qqZH (refined, N=%.2f)", h_qq_ref->Integral()), "l");
    leg->AddEntry(h_gg_ref_plot, Form("GluGluZH (refined, N=%.2f)", h_gg_ref->Integral()), "l");
    leg->AddEntry(h_wz_ref_plot, Form("WZ (refined, N=%.2f)", h_wz_ref->Integral()), "l");
    leg->AddEntry(h_qq_norm_plot, Form("qqZH (normal, N=%.2f)", h_qq_norm->Integral()), "l");
    leg->AddEntry(h_gg_norm_plot, Form("GluGluZH (normal, N=%.2f)", h_gg_norm->Integral()), "l");
    leg->AddEntry(h_wz_norm_plot, Form("WZ (normal, N=%.2f)", h_wz_norm->Integral()), "l");

    leg->Draw();

    c->SaveAs(Form("plots/%s.png", hname));
    delete c;
}

std::vector<double> readCutflow(const std::string& path, const std::string& sample)
{
    std::vector<double> vals(7, 0.0);
    std::ifstream in(path);
    if (!in.is_open()) {
        std::cerr << "Cannot open " << path << std::endl;
        return vals;
    }

    json j;
    try {
        in >> j;
    } catch (...) {
        std::cerr << "Error parsing JSON " << path << std::endl;
        return vals;
    }

    if (!j.contains(sample) || !j[sample].is_array()) {
        std::cerr << "Missing or invalid sample key: " << sample << std::endl;
        return vals;
    }

    auto arr = j[sample];
    int n = std::min<int>(7, arr.size());
    for (int i = 0; i < n; ++i) {
        vals[i] = arr[i].get<double>();
    }
    return vals;
}

void plotCutflowComparison()
{
    gStyle->SetOptStat(0);
    gSystem->mkdir("plots", kTRUE);

    std::vector<std::string> labels = {
        "All",
        "Lepton pre-sel",
        "mll veto",
        "Z window",
        "Zg veto",
        "Jet pre-sel",
        "Signal region"
    };

    const char* refinedJson = "/eos/user/d/dshekar/MCsamplesForBDTzh3l/Summer22EE_130x_nAODv12_Full2022v12/MCl2loose2022EEv12__MCCorr2022EEv12JetScaling__l2tight/WZ_results/recoPlot_refined_cutFlow.json";
    // cutflow in WZ folder contains results from all three samples as it was the last sample to be analyzed.

    auto c1 = readCutflow(refinedJson, "ZH_Zto2L_Hto2WtoLNu2Q");
    auto c2 = readCutflow(refinedJson, "GluGluZH_Zto2L_Hto2WtoLNu2Q");
    auto c3 = readCutflow(refinedJson, "WZ");

    auto normalize = [](std::vector<double>& v) {
        if (!v.empty() && v[0] != 0.0) {
            double n0 = v[0];
            for (auto& x : v) x /= n0;
        }
    };

    normalize(c1);
    normalize(c2);
    normalize(c3);

    TGraph* g1 = new TGraph(7);
    TGraph* g2 = new TGraph(7);
    TGraph* g3 = new TGraph(7);

    for (int i = 0; i < 7; ++i) {
        g1->SetPoint(i, i, c1[i]);
        g2->SetPoint(i, i, c2[i]);
        g3->SetPoint(i, i, c3[i]);
    }

    g1->SetLineColor(kRed+1);
    g1->SetMarkerColor(kRed+1);
    g1->SetMarkerStyle(20);
    g1->SetMarkerSize(1.1);
    g1->SetLineWidth(2);

    g2->SetLineColor(kBlue+1);
    g2->SetMarkerColor(kBlue+1);
    g2->SetMarkerStyle(21);
    g2->SetMarkerSize(1.1);
    g2->SetLineWidth(2);

    g3->SetLineColor(kGreen+2);
    g3->SetMarkerColor(kGreen+2);
    g3->SetMarkerStyle(22);
    g3->SetMarkerSize(1.1);
    g3->SetLineWidth(2);

    TCanvas* c = new TCanvas("c_cutflow", "cutflow", 1000, 700);
    c->SetBottomMargin(0.28);
    c->SetLeftMargin(0.12);
    c->SetGridx();
    c->SetGridy();

    TH1F* frame = c->DrawFrame(-0.5, 0.0, 6.5, 1.2);
    frame->SetTitle("Refined cutflow normalized to first bin; ;Normalized events");

    frame->GetXaxis()->SetLabelSize(0);
    frame->GetXaxis()->SetTickSize(0);

    g1->Draw("PL SAME");
    g2->Draw("PL SAME");
    g3->Draw("PL SAME");

    for (int i = 0; i < 7; ++i) {
        TLatex* t = new TLatex(i, -0.08, labels[i].c_str());
        t->SetTextAlign(23);
        t->SetTextSize(0.03);
        t->SetTextAngle(35);
        t->Draw();
    }

    TLegend* leg = new TLegend(0.55, 0.70, 0.88, 0.88);
    leg->SetBorderSize(0);
    leg->SetFillStyle(0);
    leg->AddEntry(g1, "GluGluZH", "lp");
    leg->AddEntry(g2, "qqZH", "lp");
    leg->AddEntry(g3, "WZ", "lp");
    leg->Draw();

    c->SaveAs("plots/cutflow_comparison.png");
}

void plotting()
{
    gStyle->SetOptStat(0);

    TFile* f_qq_ref  = TFile::Open(qqZH_refinedWs);
    TFile* f_gg_ref  = TFile::Open(ggZH_refinedWs);
    TFile* f_wz_ref  = TFile::Open(WZ_refinedWs);
    TFile* f_qq_norm = TFile::Open(qqZH_normalWs);
    TFile* f_gg_norm = TFile::Open(ggZH_normalWs);
    TFile* f_wz_norm = TFile::Open(WZ_normalWs);

    if (!f_qq_ref || !f_gg_ref || !f_qq_norm || !f_gg_norm || !f_wz_norm || !f_wz_ref) {
        std::cerr << "Error opening one or more input files." << std::endl;
        return;
    }

    std::vector<const char*> hnames = {
        "h_E_lep1",
        "h_E_lep2",
        "h_E_lep3",
        "h_pT_lep1",
        "h_pT_lep2",
        "h_pT_lep3",
        "h_pZ_lep1",
        "h_pZ_lep2",
        "h_pZ_lep3",
        "h_nJets",
        "h_E_Jet1",
        "h_E_Jet2",
        "h_pT_Jet1",
        "h_pT_Jet2",
        "h_pZ_Jet1",
        "h_pZ_Jet2",
        "h_eTmiss",
        "h_Hmass_T",
        "h_Zmass",
        "h_Whadmass",
        "h_Wlepmass",
        // "h_angle_WW",
        "h_dPhi_WW",
        // "h_angle_ZH",
        "h_dPhi_ZH"
    };

    gSystem->mkdir("plots", kTRUE);

    for (const auto& hname : hnames) {
        plotOne(f_qq_ref, f_gg_ref, f_qq_norm, f_gg_norm, f_wz_norm, f_wz_ref, hname);
    }

    plotCutflowComparison();
}