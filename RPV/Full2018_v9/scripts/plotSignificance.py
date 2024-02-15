from ROOT import *
from array import *
import CMS_lumi, tdrstyle
import sys

tdrstyle.setTDRStyle()

CMS_lumi.lumi_13TeV = "59.7 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "   Simulation"

iPos=0

def makeCanvas(name="c"):

  H_ref = 700
  W_ref = 800
  W = W_ref
  H  = H_ref

  canvas = TCanvas(name,name)

  # references for T, B, L, R
  T = 0.08*H_ref
  B = 0.12*H_ref
  L = 0.18*W_ref
  R = 0.05*W_ref

  canvas.SetFillColor(0)
  canvas.SetBorderMode(0)
  canvas.SetFrameFillStyle(0)
  canvas.SetFrameBorderMode(0)
  canvas.SetLeftMargin( L/W)
  canvas.SetRightMargin( R/W)
  canvas.SetTopMargin( T/H )
  canvas.SetBottomMargin( B/H )
  canvas.SetTickx(1)
  canvas.SetTicky(1)
 
  return canvas


def extract(file):
  expLimit = {}
  for line in file:
    if "Significance" in line:
      res = line.split()[1]
    elif "p-value" in line:
      res = line.split()[3] 
  return res 

def plotSignificance(directory,variable,mass,pvalue=True,model="RPV_sb700_chi400_sl350",cat="all"):

    xcentral = array("d") # masses
    ycentral = array("d") # limits
    xerr = array("d")

    for m in masses:
        if cat=="all":
            fitfile = directory+"/"+variable+"/pvalue_"+model+"_m"+str(m)+".out"
            CMS_lumi.extraText2 = "0+1+2 jets "
        else:
            fitfile = "/afs/cern.ch/work/l/lviliani/LatinosFramework13TeV_clean/CMSSW_7_6_3/src/LatinoAnalysis/ShapeAnalysis/PlotsConfigurations/Configurations/EXO/WWlvlv_VBF/combineFrozen_newbins/Significance."+cat+".ICHEP2016.mH"+m+"_"+model+".txt"
            CMS_lumi.extraText2 = cat.replace("jet"," jet ")
        try:
            fitFile = open(fitfile)
        except:
            print (fitfile, "missing")
            continue
        sig = extract(fitFile)
        xcentral.append(float(m))
        xerr.append(0)
        ycentral.append(float(sig))
    c1 = makeCanvas("c1")

    c1.SetLogy()
 
    graphcentral_mu = TGraph(len(xcentral),xcentral,ycentral)
    graphcentral_mu.SetLineStyle(1)
    graphcentral_mu.SetLineColor(kBlue)
    graphcentral_mu.SetMarkerStyle(20)
    graphcentral_mu.SetMarkerColor(kBlue)
 
    graphcentral_mu.SetTitle("")
    if pvalue: graphcentral_mu.GetYaxis().SetTitle("p-value")
    else: graphcentral_mu.GetYaxis().SetTitle("Significance (standard deviations)")
    graphcentral_mu.GetXaxis().SetTitle("M_{X} [GeV]")
    if variable=="chi_mass":
      graphcentral_mu.GetXaxis().SetRangeUser(180,600)
      line1 = TLine(180,0.317310507,600,0.317310507)
      line2 = TLine(180,0.045500264,600,0.045500264)
      line3 = TLine(180,0.002699796,600,0.002699796)
      line4 = TLine(180,0.000063342,600,0.000063342)
      line5 = TLine(180,0.000000573,600,0.000000573)
    elif variable=="sb_mass":
      graphcentral_mu.GetXaxis().SetRangeUser(250,800)
      line1 = TLine(250,0.317310507,800,0.317310507)
      line2 = TLine(250,0.045500264,800,0.045500264)
      line3 = TLine(250,0.002699796,800,0.002699796)
      line4 = TLine(250,0.000063342,800,0.000063342)
      line5 = TLine(250,0.000000573,800,0.000000573)
    elif variable=="slep_mass": 
      graphcentral_mu.GetXaxis().SetRangeUser(100,450)
      line1 = TLine(100,0.317310507,450,0.317310507)
      line2 = TLine(100,0.045500264,450,0.045500264)
      line3 = TLine(100,0.002699796,450,0.002699796)
      line4 = TLine(100,0.000063342,450,0.000063342)
      line5 = TLine(100,0.000000573,450,0.000000573)
 
    if pvalue: graphcentral_mu.GetYaxis().SetRangeUser(1E-9,0.5)
    else: graphcentral_mu.GetYaxis().SetRangeUser(0,100)
 
    line1.SetLineColor(kGray)
    line1.SetLineWidth(2)
    line1.SetLineStyle(9)
    line2.SetLineColor(kGray)
    line2.SetLineWidth(2)
    line2.SetLineStyle(9)
    line4.SetLineColor(kGray)
    line4.SetLineWidth(2)
    line4.SetLineStyle(9)
    line3.SetLineColor(kRed)
    line3.SetLineWidth(2)
    line3.SetLineStyle(9)
    line5.SetLineColor(kRed)
    line5.SetLineWidth(2)
    line5.SetLineStyle(9)
    graphcentral_mu.Draw("ALP")
    line1.Draw("same")
    line2.Draw("same")
    line3.Draw("same")
    line4.Draw("same")
    line5.Draw("same")
    CMS_lumi.CMS_lumi(c1, 4, iPos)
    gPad.RedrawAxis()
 
    c1.Print(directory+"/"+variable+"_toy"+model+"_pvalue_plot.pdf")
    a=input()


directory = sys.argv[1]
variable = sys.argv[2]

if variable=="chi_mass": masses = range(180, 600, 10)
elif variable=="sb_mass": masses = range(250, 800, 10)
elif variable=="slep_mass": masses = range(100, 450, 10)

plotSignificance(directory,variable,masses,pvalue=True,model="RPV_sb700_chi400_sl370")
