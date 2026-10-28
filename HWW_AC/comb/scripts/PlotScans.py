
import sys
import ROOT 
import numpy as np
import shutil
import math
from os import path
from array import array

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gROOT.SetBatch(True)

type = sys.argv[1]
print(" "+type+" ")

########################

def getGlobalMin(Dir,AC):

 file = "hists/"+Dir+"higgsCombineHVV_"+AC+".MultiDimFit.mH125.root" 

 src = path.realpath(""+file+"") 
 F = ROOT.TFile.Open(''+src+'', 'read')
 T = F.Get("limit")

 x, y = 0, 0

 for evt in T : 
 
  Fai = eval("evt."+AC+"")
  QE = evt.quantileExpected
  dNLL = evt.deltaNLL
  NLL  = evt.nll + evt.nll0
  if QE==-1 :
   x = Fai 
   y = 2*(dNLL+NLL)

 F.Close()
 return x, y
   

def getGraphWithGlobalMin(Dir, AC, V, ABS, R):

 file = "hists/"+Dir+"higgsCombineHVV_"+AC+V+".MultiDimFit.mH125.root"  

 src = path.realpath(""+file+"") 
 F = ROOT.TFile.Open(''+src+'', 'read')
 T = F.Get("limit")
 print(src)

 x1, y1 = array('d'), array('d')
 gMin = False
 print(AC)
 
 for evt in T :

  Fai = eval("evt."+AC+"")
  QE = evt.quantileExpected
  dNLL = evt.deltaNLL
  NLL  = evt.nll + evt.nll0

  if QE>-1 :
   x1.append(round(Fai,R))  
   if ABS is True : y1.append(2*(dNLL+NLL))
   else :           y1.append(2*dNLL)
  elif QE==-1 :
   gMin = True
   mFai = Fai 
   if ABS is True : mNLL = 2*(dNLL+NLL)
   else :           mNLL = 2*dNLL
  # End Tree loop

 if gMin is True :
  print(mFai, mNLL)
  x1.append(mFai)  
  y1.append(mNLL)

 n = len(x1)
 x1, y1 = zip(*sorted(zip(x1, y1)))

 #print(x1, y1)
 
 gr = ROOT.TGraph(n, np.array(x1), np.array(y1))

 F.Close()
 return x1, y1, gr
   
########################

def Plot2(AC, V, ABS,axis1,axis2,Max,label): 

 x1, y1, gr1 = getGraphWithGlobalMin("", AC, "", ABS, 5)
 gr1.SetMarkerColor(1)
 gr1.SetLineColor(4)
 gr1.SetLineWidth(2)
 gr1.SetMinimum(0)
 gr1.SetMaximum(Max)
 gr1.SetMarkerStyle(7)
 
 gr1.GetXaxis().SetTitle(''+label+'') 
 gr1.GetXaxis().SetTitleSize(0.05) 
 gr1.GetXaxis().SetLabelSize(0.03)
 gr1.GetXaxis().CenterTitle(1)
 gr1.GetYaxis().SetTitle('-2#Delta ln L') 
 gr1.GetYaxis().CenterTitle(1)
 gr1.GetYaxis().SetTitleSize(0.05)
 gr1.GetYaxis().SetTitleOffset(0.75)

 x1e, y1e, gr1e = getGraphWithGlobalMin("", AC, V, ABS, 5)
 gr1e.SetMarkerColor(1)
 gr1e.SetLineColor(4)
 gr1e.SetLineStyle(2)  
 gr1e.SetLineWidth(2)
 gr1e.SetMarkerStyle(7)

 line68 = ROOT.TLine(axis1,1.0,axis2,1.0)
 line95 = ROOT.TLine(axis1,3.84,axis2,3.84)
 line68.SetLineStyle(9)
 line95.SetLineStyle(9)
 line68.SetLineColor(ROOT.kBlack)
 line95.SetLineColor(ROOT.kBlack)

 tex68 = ROOT.TLatex(axis2-(0.3*axis2),1.2,"68% CL");
# tex68.SetNDC();
 tex68.SetTextFont(42);
 tex68.SetTextSize(0.03);
# tex68.SetLineWidth(2);
 tex95 = ROOT.TLatex(axis2-(0.3*axis2),4,"95% CL");
 tex95.SetTextFont(42);
 tex95.SetTextSize(0.03);

 axis = gr1.GetXaxis();
 axis.SetLimits(axis1,axis2); 
 
 canvas = ROOT.TCanvas('canvas', '', 20000, 20000) 
 canvas.Divide(1)
 canvas.GetPad(1).SetPad("TopPad", "", 0.01, 0.01, 1.035, 1.035, 0, -1, 0) 
 canvas.GetPad(1).SetTopMargin(0.075); 
 canvas.GetPad(1).SetBottomMargin(0.116);
 canvas.GetPad(1).SetRightMargin(0.06);
 canvas.GetPad(1).SetLeftMargin(0.085);
 canvas.cd(1)

 tex = ROOT.TLatex(0.085,0.935,"#bf{CMS}") ###  #it{Preliminary}"); 
 tex.SetNDC();
 tex.SetTextFont(42);
 tex.SetTextSize(0.04);
 tex.SetLineWidth(2);
 texlumi = ROOT.TLatex(0.70,0.935,"x fb^{-1} (13 TeV)");
 texlumi.SetNDC();
 texlumi.SetTextFont(42);
 texlumi.SetTextSize(0.035);
 texlumi.SetLineWidth(2);
 
 gr1.Draw("LA") 
 gr1e.Draw("L SAME")
 canvas.Update()
 line95.Draw("P")
 line68.Draw("P")
 tex.Draw("sames")
 texlumi.Draw("sames")
 tex68.Draw("sames")
 tex95.Draw("sames")

 leg = ROOT.TLegend(0.40,0.68, 0.65, 0.88)
 leg.SetNColumns(1)
 leg.SetBorderSize(0)
 leg.SetTextSize(0.04)
 leg.SetTextFont(42)
 leg.SetFillColor(0)
 leg.AddEntry(gr1,"Float","l")
 leg.AddEntry(gr1e,"Fix","l")
 leg.Draw()

 canvas.SaveAs("plots/"+AC+"_OE.pdf")
 canvas.SaveAs("plots/"+AC+"_OE.png")

 #Fout = ROOT.TFile.Open("Graphs_"+AC+".root", 'RECREATE')
 #gr1.SetName("Observed")
 #gr1.Write()
 #gr1e.SetName("Expected")
 #gr1e.Write()
 #Fout.Close()

############################################1

if type == "Fai" :

 Plot2("muV",  "Fr", False,0,3, 10, "#mu_{Ewk}")
 Plot2("muF",  "Fr", False,0,3, 10, "#mu_{ggF}") 
 Plot2("Fa2",  "Fr", False,-0.6,0.6, 10, "F_{a2}")
 Plot2("Fa3",  "Fr", False,-0.2,0.2, 10, "F_{a3}")
 Plot2("Fk1",  "Fr", False,-0.2,0.6, 10, "F_{#Lambda1}")
 Plot2("Fg2",  "Fr", False,-.99,.99, 10, "F^{#gamma#gamma}_{a2}")
 Plot2("Fg3",  "Fr", False,-.99,.99, 10, "F^{#gamma#gamma}_{a3}")
 Plot2("Fz2",  "Fr", False,-.99,.99, 10, "F^{Z#gamma}_{a2}")
 Plot2("Fz3",  "Fr", False,-.99,.99, 10, "F^{Z#gamma}_{a3}")

elif type == "ciHB" :
 
 Plot2("cZ",  "Fr", False,-1,1, 10, "#deltac_{z}")
 Plot2("cZZ", "Fr", False,-2,2, 10, "c_{zz}")
 Plot2("cZZt","Fr", False,-2,2, 10, "#tilde{c}_{zz}")
 Plot2("cZB", "Fr", False,-0.5,0.5, 10, "c_{z#Box}")
 Plot2("cZg", "Fr", False,-3,3, 10, "c_{z#gamma}")
 Plot2("cZgt","Fr", False,-3,3, 10, "#tilde{c}_{z#gamma}")
 Plot2("cgg", "Fr", False,-10,10, 10, "c_{#gamma#gamma}")
 Plot2("cggt","Fr", False,-10,10, 10, "#tilde{c}_{#gamma#gamma}")

elif type == "ciWB" :
 
 Plot2("cHb",  "Fr", False,-10,10, 10, "c_{H#Box}")
 Plot2("cHD",  "Fr", False,-5,5, 10, "c_{HD}")
 Plot2("cHW",  "Fr", False,-3,3, 10, "c_{HW}")
 Plot2("cHWt", "Fr", False,-3,3, 10, "c_{H#tilde{W}}")
 Plot2("cHWB", "Fr", False,-10,10, 10, "c_{HWB}")
 Plot2("cHWBt","Fr", False,-10,10, 10, "c_{H#tilde{W}B}")
 Plot2("cHB",  "Fr", False,-5,5, 10, "c_{HB}")
 Plot2("cHBt", "Fr", False,-5,5, 10, "c_{H#tilde{B}}")

else : print("type not set correctly")




