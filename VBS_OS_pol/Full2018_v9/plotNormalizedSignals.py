import ROOT
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inputFile", help="input root file", default='rootfile.root')

args = parser.parse_args()
inputfile = args.inputFile 

variables = ['dnn_TTvsLL_16']
samples   = ['WWewk_CMWW_TT', 'WWewk_CMWW_TL', 'WWewk_CMWW_LT', 'WWewk_CMWW_LL']
histos    = {}
colors    = {
    'WWewk_CMWW_LL' : 800,
    'WWewk_CMWW_LT' : 802,
    'WWewk_CMWW_TL' : 804,
    'WWewk_CMWW_TT' : 806,
    }
rfile = ROOT.TFile.Open(inputfile)
ROOT.gStyle.SetOptStat(00000000)
for cat in [rdir.GetName() for rdir in rfile.GetDirectory('/').GetListOfKeys()]:
  print(cat)
  histos[cat] = {}
  for var in variables:
    histos[cat][var] = {}
    c = ROOT.TCanvas()
    c.cd()
    legend = ROOT.TLegend(0.2, 0.7, 0.4, 0.9)
    legend.SetLineColor(0)
    legend.SetFillStyle(0)
    ymin = []
    ymax = []
    for sample in samples:
      histos[cat][var][sample] = rfile.Get('/' + cat + '/' + var + '/histo_' + sample)
      histos[cat][var][sample].SetLineColor(colors[sample]) 
      histos[cat][var][sample].SetLineWidth(3)
      ymin.append(histos[cat][var][sample].GetMinimum()/histos[cat][var][sample].Integral())
      ymax.append(histos[cat][var][sample].GetMaximum()/histos[cat][var][sample].Integral())
      #histos[cat][var][sample].DrawNormalized('histo same')
      legend.AddEntry(histos[cat][var][sample], sample.strip('WWewk_CMWW'), 'f')
    for i,sample in enumerate(samples):
      if i == 0:
        print(min(ymin), max(ymax))
        #histos[cat][var][sample].GetYaxis().SetRangeUser(min(ymin)*0.5, max(ymax)*1.5)
        #histos[cat][var][sample].GetYaxis().SetAxisRange(0.05, 0.5, "Y")
        histos[cat][var][sample].GetXaxis().SetTitle(var)
        histos[cat][var][sample].SetMinimum(min(ymin)*0.5)
        histos[cat][var][sample].SetMaximum(max(ymax)*1.5)
      histos[cat][var][sample].DrawNormalized('histo same')

    legend.Draw('same')
    c.SaveAs('normalizedPlots/c_norm_' + cat + '_' + var + '.png')


