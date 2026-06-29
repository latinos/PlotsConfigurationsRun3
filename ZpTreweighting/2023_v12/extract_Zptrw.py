# =================================
# Danush Shekar (UIC), 9Dec25
# =================================
import json
import os
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
parser.add_argument('-n', type=int, default=0, help='Normalization method:\n1: Ratio of integral of MC over weights*MC.\n2: Normalize MC to data integral before calculating rw factor.')
parser.add_argument('-c', type=str, default="mm", help='Z decay channel.')
parser.add_argument('-nj', type=int, default=0, help='Jet bin category(number of jet bins).')
parser.add_argument('-i', '--input', default='mkShapes__ZpTreweighting.root', help='Path to the merged ROOT file (default: mkShapes__ZpTreweighting.root)')
parser.add_argument('--write-json', default=None, help='If given, write the updated dyZpTrw.json to this path after a successful fit (requires -f). The file is overwritten.')
parser.add_argument('--year', default='2022', help="Year key in the DYrew dict written to dyZpTrw.json (default: '2022')")
parser.add_argument('--sample-type', default='LO', help="Sample-type key in the DYrew dict written to dyZpTrw.json (default: 'LO')")
parser.add_argument('--plot-xrange', type=float, default=80, help='maximum X-axis range for the plots (default: 80)')
parser.add_argument('--fit-xrange', type=float, default=50, help='maximum X-axis range for the fits (default: 50)')
args = parser.parse_args()

root_file = ROOT.TFile(args.input)
channel = f"Z{args.c}_{args.nj}j"
zee_dir = root_file.Get(channel)
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

plot_range = [0, args.plot_xrange]
fit_range = [0, args.fit_xrange]

def calc_norm_factor(dy_hist, fitting_function, fit_params):
    numerator = 0.0
    denominator = 0.0
    first_bin = dy_hist.FindBin(fit_range[0])
    last_bin = dy_hist.FindBin(fit_range[1])
    print("\nNOTE: Using fit function (", fitting_function,") to calculate normalization factor.\n") # [0]*TMath::Erf((x-[1])/[2]) + [3]*x + [4]*x**2 + [5]
    for bin_idx in range(first_bin, last_bin + 1):
        mc_events = dy_hist.GetBinContent(bin_idx)
        # weight = histo_ratio.GetBinContent(bin_idx)
        binCenter = dy_hist.GetXaxis().GetBinCenter(bin_idx)
        weight = fit_params[0]*ROOT.TMath.Erf((binCenter - fit_params[1])/fit_params[2]) + fit_params[3]*binCenter + fit_params[4]*binCenter**2 + fit_params[5]
        numerator += mc_events
        denominator += mc_events * weight
    norm_factor = numerator / denominator if denominator != 0 else 1.0
    print("Normalization factor:", norm_factor)
    return norm_factor

# # Rebin hists
# histo_trueData.Rebin(4)
# histo_DY.Rebin(4)

# Calculate the integral/sum of histo_DY and histo_ratio for x axis in [0, fit_range[1])
integral_histo_DY = histo_DY.Integral(histo_DY.FindBin(fit_range[0]), histo_DY.FindBin(fit_range[1]) - 1)
integral_histo_DATA = histo_trueData.Integral(histo_trueData.FindBin(fit_range[0]), histo_trueData.FindBin(fit_range[1]) - 1)
norm_factor2 = integral_histo_DATA/integral_histo_DY
print("Normalization factor 2:", norm_factor2)
if args.n == 2:
    histo_DY.Scale(norm_factor2)
    integral_histo_DYscaled = histo_DY.Integral(histo_DY.FindBin(fit_range[0]), histo_DY.FindBin(fit_range[1]) - 1)

# Create a ratio plot of DATA to DY
histo_ratio = histo_trueData.Clone("histo_ratio")
histo_ratio.Divide(histo_DY)

integral_histo_ratio = histo_ratio.Integral(histo_ratio.FindBin(fit_range[0]), histo_ratio.FindBin(fit_range[1]) - 1)

# fitting_functions = ["[0]*x**6 + [1]*x**5 + [2]*x**4 + [3]*x**3 + [4]*x**2 + [5]*x + [6]", "[0]*([1]*TMath::Erf((x-[2])/[3]) + [4]*x + [5]*x**2)"]
fitting_functions = ["([0]*TMath::Erf((x-[1])/[2]) + [3]*x + [4]*TMath::Sq(x) + [5])"]
initial_guesses = [[0.0, 5.0, 10.0, 0.0, 0.0, 1.0]]
save_name_suffixes = [channel]
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
    histo_DY.GetXaxis().SetRangeUser(plot_range[0], plot_range[1])
    # Draw DY as reference, then data points
    # histo_DY.SetLineColor(ROOT.kBlue)
    histo_DY.SetStats(False)
    histo_DY.SetFillStyle(3344)
    histo_DY.SetFillColorAlpha(ROOT.kBlue, 0.1)
    histo_DY.Draw("HIST")
    histo_trueData.SetMarkerStyle(8)
    histo_trueData.SetMarkerColor(ROOT.kBlack)
    histo_trueData.SetMarkerSize(0.8)
    histo_trueData.GetXaxis().SetRangeUser(plot_range[0], plot_range[1])
    histo_trueData.Draw("E1 SAME")

    # CMS label
    label = ROOT.TLatex()
    label.SetNDC(True)
    label.SetTextSize(0.040)
    label.DrawLatex(0.12, 0.92, "#bf{CMS} #it{Preliminary}")
    label.DrawLatex(0.55, 0.92, "L = 8.2 fb^{-1} (#sqrt{s} = 13.6 TeV)")
    label.DrawLatex(0.15, 0.2, f"num(DY) events in ({fit_range[0]},{fit_range[1]}) GeV = {integral_histo_DY:.3f}")
    label.DrawLatex(0.15, 0.15, f"num(DATA) events in ({fit_range[0]},{fit_range[1]}) GeV = {integral_histo_DATA:.3f}")
    if args.n == 2:
        label.DrawLatex(0.15, 0.1, f"num(DY normalized) events in ({fit_range[0],fit_range[1]}) GeV = {integral_histo_DYscaled:.3f}")


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
    h_ratio_points.GetXaxis().SetRangeUser(plot_range[0], plot_range[1])

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
                            fit_range[0],#histo_ratio.GetXaxis().GetXmin(),
                            fit_range[1])#histo_ratio.GetXaxis().GetXmax())
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

        # Plot only until 50 GeV, the value after 50 GeV will be the fit function's value at 50 GeV
        fit_func.Draw("SAME") 
        const_val = fit_func.Eval(fit_range[1])
        const_func = ROOT.TF1("const_func", f"{const_val}", fit_range[1], plot_range[1]) # NOTE - assuming plot_range[1] is greater than fit_range[1]
        const_func.SetLineColor(ROOT.kRed)
        # const_func.SetLineStyle(ROOT.kDashed)
        const_func.Draw("L SAME")
        fit_func.Print("V") 
    c.SaveAs(f"ZpTreweighting_with_ratio_{savename}.pdf")
    c.Close()  # Close the canvas after saving
    # c.SaveAs(f"ZpTreweighting_with_ratio_{savename}.png")

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
        # Plot only until 50 GeV, the value after 50 GeV will be the fit function's value at 50 GeV
        fit_func.Draw("SAME")
        # Draw constant for x > 50 GeV
        const_val = fit_func.Eval(fit_range[1])
        const_func = ROOT.TF1("const_func", f"{const_val}", fit_range[1], plot_range[1]) # NOTE - assuming plot_range[1] is greater than fit_range[1]
        const_func.SetLineColor(ROOT.kRed)
        const_func.Draw("SAME")
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
            latex.DrawLatex(0.15, 0.35, f"f(x) = {func_formula}")
            latex.DrawLatex(0.15, 0.3, param_str)
            if args.n == 1:
                norm_factor = calc_norm_factor(histo_DY, fitfunc, param_values)
                latex.DrawLatex(0.15, 0.25, f"Normalization factor = {norm_factor:.2f}")
                print(f"Normalization factor = {norm_factor}")
            formula = fit_func.GetTitle()  # e.g., "[0]*x + [1]"
            n_params = fit_func.GetNpar()
            params = [fit_func.GetParameter(i) for i in range(n_params)]
            # Replace [i] with parameter values
            for i, p in enumerate(params):
                formula = formula.replace(f"[{i}]", f"{p:.3f}")
            print(f"Fit function with parameters: {formula}")

    c_ratio_only.SaveAs(f"ZpTreweighting_ratio_fit_{savename}.pdf")
    # c_ratio_only.SaveAs(f"ZpTreweighting_ratio_fit_{savename}.png")
    c_ratio_only.Close()  # Close the canvas after saving
print(f"Integral of DY histogram from {fit_range[0]} to {fit_range[1]} GeV: {integral_histo_DY}")
print(f"Integral of ratio histogram from {fit_range[0]} to {fit_range[1]} GeV: {integral_histo_ratio}")

# Update dyZpTrw.json 
if args.write_json is not None and args.f:
    wrote = False
    # 'fit_func', 'fit_result', 'fitfunc' are in scope from the last for-loop
    # iteration (Python loop variables persist after the loop).
    if fit_result and fit_result.IsValid():
        # Build a ROOT / C++ compatible formula string with full precision.
        root_formula = fitfunc  # e.g. "[0]*TMath::Erf(...) + [3]*x + [4]*x**2 + [5]"
        n_params = fit_func.GetNpar()
        params = [fit_func.GetParameter(i) for i in range(n_params)]
        const_val = fit_func.Eval(fit_range[1])
        for i, p in enumerate(params):
            root_formula = root_formula.replace(f"[{i}]", f"{p:.6f}")
        # Convert Python-style x**2 to ROOT / C++ TMath::Sq(x)
        # root_formula = root_formula.replace("x**2", "TMath::Sq(x)")
        # Tidy up double signs that can appear after parameter substitution
        root_formula = root_formula.replace("+ -", "- ")
        root_formula = root_formula.replace("- -", "+ ")
        piecewise_formula = f"({root_formula})*(x<{fit_range[1]}) + ({const_val:.6f})*(x>={fit_range[1]})"

        # Prepend the integral normalization factor if methodology 2 is chosen
        if args.n == 1:
            full_expr = f"{norm_factor}*{piecewise_formula}"
        else:
            full_expr = piecewise_formula

        # Read the existing JSON so other years/types are preserved.
        existing = {}
        if os.path.exists(args.write_json):
            try:
                with open(args.write_json) as _fj:
                    existing = json.load(_fj)
            except json.JSONDecodeError as _e:
                print(f"WARNING: Existing JSON file '{args.write_json}' is malformed "
                        f"({_e}); it will be overwritten.")
        # Update only the requested year / sample-type key.
        sample_key = f"{args.sample_type}_{args.nj}j"
        existing.setdefault(args.year, {})[sample_key] = full_expr

        with open(args.write_json, "w") as _fj:
            json.dump(existing, _fj, indent=4)
            _fj.write("\n")
        print(f"\nWrote updated dyZpTrw.json → {args.write_json}")
        print(f"  [{args.year}][{sample_key}]: {full_expr}")
        wrote = True
    else:
        print("\nWARNING: Fit did not converge; dyZpTrw.json was NOT updated.")