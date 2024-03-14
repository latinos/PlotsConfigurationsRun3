import ROOT

polarizations = ['LT']#, 'LT', 'TL', 'TT']
variables =   { 'costheta_l1': 'cos(#theta^{*}_{l1,W1} )', 
                'costheta_l2': 'cos(#theta^{*}_{l2,W2} )'
              }
histos = {}
ROOT.gStyle.SetOptStat(0000000)
for var, name in variables.iteritems():
  print var
  histos[var] = {}
  c = ROOT.TCanvas()
  #c.cd()
  #c.Draw()
  #l = ROOT.TLegend(0.6001252, 0.7503075, 0.8998748, 0.900369, '', 'brNDC')
  l = ROOT.TLegend(0.15, 0.7503075, 0.3, 0.900369)
  for i,pol in enumerate(polarizations):
    print i,pol
    filename = 'VBS_WW_pol_' + pol + '.root'
    rfile = ROOT.TFile.Open(filename)
    histos[var][pol] = rfile.Get(var).Clone()
    histos[var][pol].GetXaxis().SetTitle(name)
    histos[var][pol].GetYaxis().SetTitle('a. u.')
    histos[var][pol].SetLineColor(i)
    histos[var][pol].Draw()
    histos[var][pol].DrawNormalized('same')
    l.AddEntry(histos[var][pol], pol, 'flep')
    #c.Update()
    #rfile.Close()
  #l.Draw('same')
  c.SaveAs("/eos/home-m/mlizzo/www/UL_production/Full2018_v9/VBS_WW_pol/" + var + ".png")
  #del c
  #del l
