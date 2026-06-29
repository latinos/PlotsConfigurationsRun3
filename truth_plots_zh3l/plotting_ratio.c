#include <TH1D.h>
#include <TFile.h>
#include <TCanvas.h>
#include <TPad.h>
#include <TLegend.h>
#include <TLine.h>
#include <TStyle.h>

const char* f1_name = "./qqZH_gen_plots.root";
const char* f2_name = "./ggZH_gen_plots.root";
// const char* f1 = "/eos/user/d/dshekar/MCsamplesForBDTzh3l/Summer22EE_130x_nAODv12_Full2022v12/MCl2loose2022EEv12__MCCorr2022EEv12JetScaling__l2tight/ZH_Zto2L_Hto2WtoLNu2Q_results//reco_plots_refinedWHadReco.root";
// const char* f2 = "/eos/user/d/dshekar/MCsamplesForBDTzh3l/Summer22EE_130x_nAODv12_Full2022v12/MCl2loose2022EEv12__MCCorr2022EEv12JetScaling__l2tight/GluGluZH_Zto2L_Hto2WtoLNu2Q_results//reco_plots_refinedWHadReco.root";
const char* histname = "h_dPhi_ZH";

gStyle->SetOptStat(0);

TFile *f1 = TFile::Open(f1_name);
TFile *f2 = TFile::Open(f2_name);

TH1D *h1 = (TH1D*)f1->Get(histname)->Clone("h1_clone");
TH1D *h2 = (TH1D*)f2->Get(histname)->Clone("h2_clone");

h1->SetDirectory(nullptr);
h2->SetDirectory(nullptr);

h1->SetStats(0);
h2->SetStats(0);

h1->SetLineColor(kRed+1);
h1->SetLineWidth(2);
h2->SetLineColor(kBlue+1);
h2->SetLineWidth(2);

h1->Scale(1.0 / h1->Integral());
h2->Scale(1.0 / h2->Integral());

TH1D *hRatio = (TH1D*)h1->Clone("hRatio");
hRatio->SetDirectory(nullptr);
hRatio->SetStats(0);
hRatio->Divide(h2);
hRatio->SetLineColor(kBlack);
hRatio->SetMarkerStyle(20);
hRatio->SetMarkerSize(0.8);

TCanvas *c = new TCanvas("c", "overlay with ratio", 800, 800);

TPad *pad1 = new TPad("pad1", "pad1", 0.0, 0.30, 1.0, 1.0);
pad1->SetBottomMargin(0.02);
pad1->SetLeftMargin(0.12);
pad1->SetRightMargin(0.04);
pad1->Draw();
pad1->cd();

h1->SetMinimum(0.0);
h1->SetMaximum(0.3);
h1->Draw("hist");
h2->Draw("hist same");

TLegend *leg = new TLegend(0.2, 0.5, 0.5, 0.7);
leg->SetBorderSize(0);
leg->SetFillStyle(0);
leg->AddEntry(h1, "qqZH", "l");
leg->AddEntry(h2, "GluGluZH", "l");
leg->Draw();

c->cd();

TPad *pad2 = new TPad("pad2", "pad2", 0.0, 0.05, 1.0, 0.30);
pad2->SetTopMargin(0.02);
pad2->SetBottomMargin(0.30);
pad2->SetLeftMargin(0.12);
pad2->SetRightMargin(0.04);
pad2->Draw();
pad2->cd();

hRatio->GetXaxis()->SetTitle(h1->GetXaxis()->GetTitle());
hRatio->GetYaxis()->SetTitle("Ratio");
hRatio->GetYaxis()->SetNdivisions(505);
hRatio->GetYaxis()->SetTitleSize(0.12);
hRatio->GetYaxis()->SetTitleOffset(0.45);
hRatio->GetYaxis()->SetLabelSize(0.10);
hRatio->GetXaxis()->SetTitleSize(0.12);
hRatio->GetXaxis()->SetLabelSize(0.10);
hRatio->SetMinimum(0.0);
hRatio->SetMaximum(2.0);
hRatio->Draw("ep");

TLine *line = new TLine(hRatio->GetXaxis()->GetXmin(), 1.0,
                        hRatio->GetXaxis()->GetXmax(), 1.0);
line->SetLineStyle(2);
line->SetLineWidth(2);
line->Draw("same");

pad2->RedrawAxis();
