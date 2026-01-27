import ROOT
import mplhep as hep
import matplotlib.pyplot as plt
import numpy as np

# CMS plot style
hep.style.use("CMS")
style = hep.style.CMS
style["font.size"] = 13
plt.style.use(style)

root_file = ROOT.TFile("mkShapes__ZpTreweighting.root")
zee_dir = root_file.Get("Zee_0j")
ptll_dir = zee_dir.Get("ptll")

histo_DY = ptll_dir.Get("histo_DY")
histo_DATA = ptll_dir.Get("histo_DATA")
histo_top = ptll_dir.Get("histo_top")
histo_diboson = ptll_dir.Get("histo_diboson")
histo_SMhiggs = ptll_dir.Get("histo_SMhiggs")

# Subtract DY backgrounds from DATA
histo_trueData = histo_DATA.Clone("histo_trueData")  # Create a clone for the result
histo_trueData.Add(histo_top, -1)
histo_trueData.Add(histo_diboson, -1)
histo_trueData.Add(histo_SMhiggs, -1)

# Create a ratio plot of DATA to DY
histo_ratio = histo_trueData.Clone("histo_ratio")
histo_ratio.Divide(histo_DY)

c = ROOT.TCanvas("c", "c", 800, 800)
c.Divide(1,2)

# Top pad: main plot
pad1 = c.cd(1)
pad1.SetPad(0.0, 0.30, 1.0, 1.0)
pad1.SetBottomMargin(0.02)
pad1.SetLogy()   # if you want log-y

histo_DY.SetTitle("")
histo_DY.GetYaxis().SetTitle("Events / 5 GeV")
histo_DY.GetXaxis().SetLabelSize(0)
histo_DY.GetYaxis().SetTitleSize(0.06)
histo_DY.GetYaxis().SetTitleOffset(1.1)
histo_DY.GetYaxis().SetLabelSize(0.05)

# Draw DY as reference, then data points
histo_DY.SetLineColor(ROOT.kBlue)
histo_DY.SetStats(False)
histo_DY.SetFillColorAlpha(ROOT.kBlue, 0.1)
histo_DY.Draw("HIST")
histo_trueData.SetMarkerColor(ROOT.kBlack)  # Change marker color to red
histo_trueData.SetMarkerSize(1.3)  # Change marker color to red
histo_trueData.Draw("E1 SAME")

# CMS label
label = ROOT.TLatex()
label.SetNDC(True)
label.SetTextSize(0.040)
label.DrawLatex(0.12, 0.92, "#bf{CMS} #it{Preliminary}")
label.DrawLatex(0.55, 0.92, "#sqrt{s} = 13.6 TeV, L_{int} = 8.2 fb^{-1}")

leg = ROOT.TLegend(0.60, 0.70, 0.88, 0.88)
leg.SetBorderSize(0)
leg.SetFillStyle(0)
leg.AddEntry(histo_trueData, "Data", "pe")
leg.AddEntry(histo_DY,   "DY",       "f")
leg.Draw()

# Bottom pad: ratio
pad2 = c.cd(2)
pad2.SetPad(0.0, 0.0, 1.0, 0.30)
pad2.SetTopMargin(0.02)
pad2.SetBottomMargin(0.35)

h_ratio_points = histo_ratio.Clone("h_ratio_points")
h_ratio_points.SetTitle("")
h_ratio_points.SetMarkerStyle(20)
h_ratio_points.SetMarkerSize(0.8)
h_ratio_points.SetLineColor(ROOT.kBlack)
h_ratio_points.SetMarkerColor(ROOT.kBlack)

h_ratio_points.GetYaxis().SetTitle("Data/DY")
h_ratio_points.GetYaxis().SetNdivisions(505)
h_ratio_points.GetYaxis().SetTitleSize(0.10)
h_ratio_points.GetYaxis().SetTitleOffset(0.45)
h_ratio_points.GetYaxis().SetLabelSize(0.08)
h_ratio_points.GetXaxis().SetTitle("p_{T}^{ll} [GeV]")
h_ratio_points.GetXaxis().SetTitleSize(0.12)
h_ratio_points.GetXaxis().SetLabelSize(0.10)

h_ratio_points.SetMinimum(0.0)
h_ratio_points.SetMaximum(2.0)

h_ratio_points.Draw("E1")

# horizontal line at 1
line = ROOT.TLine(h_ratio_points.GetXaxis().GetXmin(), 1.0,
                  h_ratio_points.GetXaxis().GetXmax(), 1.0)
line.SetLineColor(ROOT.kGray+2)
line.SetLineStyle(2)
line.Draw("SAME")

# --- Fit the ratio with an error function ---
# erf(x; p0, p1, p2, p3) = p0 + p1 * TMath::Erf((x - p2)/p3)
fit_func = ROOT.TF1("fit_erf",
                    "[0]*([1]*TMath::Erf((x-[2])/[3]) + [4]*x + [5]*x*x + [6])",
                    histo_ratio.GetXaxis().GetXmin(),
                    histo_ratio.GetXaxis().GetXmax())
fit_func.SetParameters(1.0, 0.05, 10.0, 5.0, 0.0, 0.0, 1.0)  # reasonable starting values
fit_func.SetLineColor(ROOT.kRed)

h_ratio_points.Fit(fit_func, "R")  # fit only in the visible x-range
fit_func.Draw("SAME")

c.SaveAs("ZpTreweighting_main_plus_ratio.pdf")
c.SaveAs("ZpTreweighting_main_plus_ratio.png")

# --- Optional: save the ratio+fit alone in a separate figure ---
c_ratio_only = ROOT.TCanvas("c_ratio_only", "c_ratio_only", 800, 800)
h_ratio_points.Draw("E1")
h_ratio_points.GetYaxis().SetTitle("Data/DY")
h_ratio_points.GetXaxis().SetTitle("p_{T}^{ll} [GeV]")
line.Draw("SAME")
fit_func.Draw("SAME")
c_ratio_only.SaveAs("ZpTreweighting_ratio_fit.pdf")
c_ratio_only.SaveAs("ZpTreweighting_ratio_fit.png")