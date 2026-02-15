# =================================
# Danush Shekar (UIC), 9Dec25
# =================================
import ROOT
import mplhep as hep
import matplotlib.pyplot as plt
import numpy as np
from ROOT import TFitResultPtr
import argparse
# CMS plot style
hep.style.use("CMS")
style = hep.style.CMS
style["font.size"] = 18
plt.style.use(style)

parser = argparse.ArgumentParser(description='Extract data and fit with Gaussian.')
parser.add_argument('-f', action='store_true', help='Fit the ratio plot using Erf.')
args = parser.parse_args()

# root_file = ROOT.TFile("mkShapes__ZpTreweighting.root")
root_file = ROOT.TFile("mkShapes__beforeZpTreweighting_highLepPtThreshold_30_18.root")
zee_dir = root_file.Get("Zmm_0j")
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

# fitting_functions = ["[0]*x**6 + [1]*x**5 + [2]*x**4 + [3]*x**3 + [4]*x**2 + [5]*x + [6]", "[0]*([1]*TMath::Erf((x-[2])/[3]) + [4]*x + [5]*x**2)"]
fitting_functions = ["[0]*([1]*TMath::Erf((x-[2])/[3]) + [4]*x + [5]*x**2 + [6])"]
initial_guesses = [[1.0, 0.0, 5.0, 10.0, 0.0, 0.0, 1.0]]
save_name_suffixes = ["erf_poly2"]
for fitfunc, initguess, savename in zip(fitting_functions, initial_guesses, save_name_suffixes):
    c = ROOT.TCanvas("c", "c", 1000, 1000)
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
    histo_DY.GetYaxis().SetTitleOffset(0.8)
    histo_DY.GetYaxis().SetLabelSize(0.05)
    histo_DY.GetXaxis().SetRangeUser(0, 80)
    # Draw DY as reference, then data points
    # histo_DY.SetLineColor(ROOT.kBlue)
    histo_DY.SetStats(False)
    histo_DY.SetFillStyle(3344)
    histo_DY.SetFillColorAlpha(ROOT.kBlue, 0.1)
    histo_DY.Draw("HIST")
    histo_trueData.SetMarkerStyle(8)
    histo_trueData.SetMarkerColor(ROOT.kBlack)
    histo_trueData.SetMarkerSize(0.8)
    histo_trueData.GetXaxis().SetRangeUser(0, 80)
    histo_trueData.Draw("E1 SAME")

    # CMS label
    label = ROOT.TLatex()
    label.SetNDC(True)
    label.SetTextSize(0.040)
    label.DrawLatex(0.12, 0.92, "#bf{CMS} #it{Preliminary}")
    label.DrawLatex(0.55, 0.92, "L = 8.2 fb^{-1} (#sqrt{s} = 13.6 TeV)")

    leg = ROOT.TLegend(0.60, 0.70, 0.88, 0.88)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.AddEntry(histo_trueData, "Data - BG", "pe")
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

    h_ratio_points.GetYaxis().SetTitle("(Data-BG)/DY")
    h_ratio_points.GetYaxis().SetNdivisions(505)
    h_ratio_points.GetYaxis().SetTitleSize(0.12)
    h_ratio_points.GetYaxis().SetTitleOffset(0.30)
    h_ratio_points.GetYaxis().SetLabelSize(0.08)
    h_ratio_points.GetXaxis().SetTitle("p_{T}^{ll} [GeV]")
    h_ratio_points.GetXaxis().SetTitleSize(0.12)
    h_ratio_points.GetXaxis().SetLabelSize(0.10)
    h_ratio_points.GetXaxis().SetRangeUser(0, 80)

    h_ratio_points.SetMinimum(0.0)
    h_ratio_points.SetMaximum(2.0)

    h_ratio_points.Draw("E1")
    h_ratio_points.SetStats(False)

    # horizontal line at 1
    line = ROOT.TLine(h_ratio_points.GetXaxis().GetXmin(), 1.0,
                    h_ratio_points.GetXaxis().GetXmax(), 1.0)
    line.SetLineColor(ROOT.kGray+2)
    line.SetLineStyle(2)
    line.Draw("SAME")
    if args.f:
        # --- Fit the ratio with an error function ---
        # erf(x; p0, p1, p2, p3) = p0 + p1 * TMath::Erf((x - p2)/p3)
        fit_func = ROOT.TF1("fit_erf",
                            fitfunc,
                            histo_ratio.GetXaxis().GetXmin(),
                            80)#histo_ratio.GetXaxis().GetXmax())
        fit_func.SetParameters(*initguess)  # reasonable starting values
        fit_func.SetLineColor(ROOT.kRed)

        fit_result = h_ratio_points.Fit(fit_func, "RVS")  # fit only in the visible x-range
        if fit_result and fit_result.IsValid():
            chi2 = fit_result.Chi2()
            ndf = fit_result.Ndf()
            chi2_ndf = chi2 / ndf if ndf != 0 else float('inf')
            print(f" ============ Chi2/NDF: {chi2_ndf:.3f} ============")
            latex = ROOT.TLatex()
            latex.SetNDC(True)
            latex.SetTextSize(0.08)
            latex.SetTextColor(ROOT.kBlack)
            latex.DrawLatex(0.15, 0.55, f"#chi^{{2}}/ndf = {chi2_ndf:.2f}")
            func_formula = fit_func.GetTitle()  # or fit_func.GetExpFormula() for TF1
            param_values = [fit_func.GetParameter(i) for i in range(fit_func.GetNpar())]
            param_str = ", ".join([f"p{i}={v:.2f}" for i, v in enumerate(param_values)])
            # # Display fit function and parameters
            # latex.DrawLatex(0.15, 0.65, f"f(x) = {func_formula}")
            # latex.DrawLatex(0.15, 0.75, param_str)
        else:
            print("Fit failed or invalid - cannot compute Chi2/NDF")

        fit_func.Draw("SAME")
        fit_func.Print("V") 
    c.SaveAs(f"ZpTreweighting_with_ratio_{savename}.pdf")
    c.SaveAs(f"ZpTreweighting_with_ratio_{savename}.png")

    # Commented out as plot quality is very bad
    c_ratio_only = ROOT.TCanvas("c_ratio_only", "c_ratio_only", 800, 800)
    h_ratio_points.Draw("E1")
    h_ratio_points.GetYaxis().SetTitle("(Data-BG)/DY")
    h_ratio_points.GetYaxis().SetTitleSize(0.05)
    h_ratio_points.GetYaxis().SetTitleOffset(0.8)
    h_ratio_points.GetYaxis().SetLabelSize(0.04)
    h_ratio_points.GetXaxis().SetTitle("p_{T}^{ll} [GeV]")
    h_ratio_points.GetXaxis().SetTitleSize(0.05)
    h_ratio_points.GetXaxis().SetLabelSize(0.03)
    line.Draw("SAME")
    if args.f:    
        fit_func.Draw("SAME")
        if fit_result and fit_result.IsValid():
            latex = ROOT.TLatex()
            latex.SetNDC(True)
            latex.SetTextSize(0.025)
            latex.SetTextColor(ROOT.kBlack)
            latex.DrawLatex(0.15, 0.15, f"#chi^{{2}}/ndf = {chi2_ndf:.2f}")
            func_formula = fit_func.GetTitle()  # or fit_func.GetExpFormula() for TF1
            param_values = [fit_func.GetParameter(i) for i in range(fit_func.GetNpar())]
            param_str = ", ".join([f"p{i}={v:.2f}" for i, v in enumerate(param_values)])
            # Display fit function and parameters
            latex.DrawLatex(0.15, 0.25, param_str)
            latex.DrawLatex(0.15, 0.35, f"f(x) = {func_formula}")
    c_ratio_only.SaveAs(f"ZpTreweighting_ratio_fit_{savename}.pdf")
    c_ratio_only.SaveAs(f"ZpTreweighting_ratio_fit_{savename}.png")