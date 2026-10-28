
import sys
import time
import ROOT
import numpy
from math import sqrt
from math import pi
from numpy import sign
from ctypes import c_double
from array import array

from m4C1V import coup_t    as coup_t_4C1V
from m4C1V import model     as model_4C1V

from m4C2V import coup_t    as coup_t_4C2V
from m4C2V import model     as model_4C2V

from m8C1V import coup_t    as coup_t_8C1V
from m8C1V import model     as model_8C1V
from m8C1V import Hyps_zero as hypz_8C1V

from m8C2V import coup_t    as coup_t_8C2V
from m8C2V import model     as model_8C2V
from m8C2V import Hyps_zero as hypz_8C2V

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetPalette(ROOT.kRainBow)
ROOT.gROOT.SetBatch(True)

## used for SMEFT model

cw = 0.8768
sw = 0.4808
e2 = 0.0917
mZ = 91.2
mZ2  = mZ*mZ
L = 100.0
L2 = L*L
csw = cw*cw-sw*sw
alpha = e2/4*pi

# Used to define Fai. Based on HZZ decay gi = sqrt(sigma_1/sigma_i).
# Assume L^2 has been canceled out for k1 terms (Templates scaled by L^2 Or coupling matrix trick) 

gi_smeft = [1, 0.39446, 2.55052, -0.43638, 0.048, 0.053, 0.053, 0.054] # Zg/gg are AC -> same as SMEFT?
gi_ac    = [1, 1.6568,  2.55052, -1.21,    1,   1,   1,   1  ]

# Get standard names for couplings/fractions

ai_dict = {
 "a1": "a1",
 "a2": "a2",
 "a3": "a3",
 "k1": "k1",
 "g2": "a2^{#gamma#gamma}",
 "g3": "a3^{#gamma#gamma}",
 "z2": "a2^{Z#gamma}",
 "z3": "a3^{Z#gamma}",
}

fai_dict = {
 "a1": "#mu",
 "a2": "f_{a2}",
 "a3": "f_{a3}",
 "k1": "f_{#Lambda1}",
 "g2": "f_{a2^{#gamma#gamma}}",
 "g3": "f_{a3^{#gamma#gamma}}",
 "z2": "f_{a2^{Z#gamma}}",
 "z3": "f_{a3^{Z#gamma}}",
}

ci_dict = {
 "a1": "#deltac_{z}",
 "a2": "c_{zz}",
 "a3": "#tilde{c}_{zz}",
 "k1": "c_{z#Box}",
 "g2": "c_{#gamma#gamma}",
 "g3": "#tilde{c}_{#gamma#gamma}",
 "z2": "c_{Z#gamma}",
 "z3": "#tilde{c}_{Z#gamma}",
}

def getName(c, typ):

 if   typ == "fai" : n = fai_dict[c]
 elif typ ==  "ci" : n =  ci_dict[c]
 elif typ ==  "ai" : n =  ai_dict[c]

 return n

### get all the rewighting and model information

def GetCVRW(prod, rwgt):
 
 hyps_4C1V = []
 hyps_4C2V = []
 hyps_8C1V = []
 hyps_8C2V = []
 for i in range(0, 10) : hyps_4C1V.append("H"+str(i+1)+"")
 for i in range(0, 35) : hyps_4C2V.append("H"+str(i+1)+"")
 for i in range(0, 36) : hyps_8C1V.append("H"+str(i+1)+"")
 for i in range(0, 330): hyps_8C2V.append("H"+str(i+1)+"")
 
 hyps_reweight = []
 coup_t        = []
 model         = []
 hypz          = []

 for ip, p in enumerate(prod) :

  if rwgt[ip] == "4C1V" :
   hyps_reweight.append(hyps_4C1V)
   coup_t.append(coup_t_4C1V)
   model.append(model_4C1V)
   hypz.append([""])
  elif rwgt[ip] == "4C2V" :
   hyps_reweight.append(hyps_4C2V)
   coup_t.append(coup_t_4C2V)
   model.append(model_4C2V)
   hypz.append([""])
  elif rwgt[ip] == "8C1V" :
   hyps_reweight.append(hyps_8C1V)
   coup_t.append(coup_t_8C1V)
   model.append(model_8C1V)
   hypz.append(hypz_8C1V)
  elif rwgt[ip] == "8C2V" :
   hyps_reweight.append(hyps_8C2V)
   coup_t.append(coup_t_8C2V)
   model.append(model_8C2V)
   hypz.append(hypz_8C2V)
  else : sys.exit(""+rwgt[ip]+" not recognised!")

  print("For "+p+" will use "+rwgt[ip]+"")

 return hyps_reweight, coup_t, model, hypz
  
### Combine all reweighted samples for a given hypothesis ###

def GetAvgSumReweight(src, cat, var, prod, hyps_mc, hrw, bl, syst, mcstat):

 f = ROOT.TFile.Open(''+src+'', 'read')
 
 hlist = ROOT.TObjArray()
 for hmc in hyps_mc :
  
  hmcstr = ''+cat+'/'+var+'/histo_'+prod+'_'+hmc+''
  if not f.Get(""+hmcstr+""): sys.exit("Error : "+hmcstr+" not found in "+src+" ")
  
  hstr = ''+cat+'/'+var+'/histo_'+prod+'_'+hmc+'to'+hrw+''+syst+''
  if hmc == hrw :
   #continue #DM Use only RW Hyps 
   print("Including "+hmc+" MC")
   hstr = ''+cat+'/'+var+'/histo_'+prod+'_'+hmc+''+syst+'' 
  
  if not f.Get(""+hstr+""): sys.exit("Error : "+hstr+" not found in "+src+" ")
 
  h = f.Get(""+hstr+"")
  h.SetDirectory(0)

  for name, bin_num in bl:
   if name == hmc :
    print("Black list:", name," bin ", bin_num)
    h.SetBinContent(bin_num, 0.)
    h.SetBinError(bin_num, 1e10) # bin is essentially discounted from weighted average
     
  hlist.Add(h)
  
 f.Close()

 #print("Will combine ", len(hlist)," histograms (Average Sum) to "+hrw+"")

 AvgSum = hlist[0].Clone()
 AvgSum.SetDirectory(0)

 nh = len(hlist)
 for i in range(0, nh) : hlist[i].SetBit(ROOT.TH1.kIsAverage)
 for i in range(1, nh) : hlist[0].Add(hlist[i],1)

 for i in range(1, hlist[0].GetXaxis().GetNbins()+1):
  n = hlist[0].GetBinContent(i)
  if mcstat == 1 : e = hlist[0].GetBinError(i)
  else           : e = 0
  AvgSum.SetBinContent(i, n)
  AvgSum.SetBinError(i, e)
  
 hlist.Clear()
 
 return AvgSum

# Add statistically correlated histograms

def AddCorrHist(h1,h2,h2sc):

 corr=1
 nbins = h1.GetXaxis().GetNbins()

 ha = h1.Clone()
 ha.SetDirectory(0)

 ha2 = h2.Clone()
 ha2.SetDirectory(0)
 ha2.Scale(h2sc)

 for i in range(1, nbins+1):
  n1 = h1.GetBinContent(i)
  n2 = ha2.GetBinContent(i)
  if n1 == -0.0 : n1 = 0
  if n2 == -0.0 : n2 = 0
  n = n1 + n2
  er1 = h1.GetBinError(i)
  er2 = ha2.GetBinError(i)
  er = er1 + er2 # correlated 
  #er = sqrt(er1**2 + er2**2 + 2*er1*er2*corr)
  #if n1*n2<0 or n1*n2==0 : er = sqrt(abs(er1**2 + er2**2 - 2*er1*er2*corr))
  ha.SetBinContent(i, n)
  ha.SetBinError(i, er)

 return ha

# count coupling power in a given term

def CouplingPower(a, c):

 nC = 0
 if   c+"**4" in a : nC = 4
 elif c+"**3" in a : nC = 3
 elif c+"**2" in a : nC = 2
 elif c       in a : nC = 1

 return nC

# Create the hypotheses using the signal model histograms scaled by Mu and Fai (Also requires HZZ gi scaling)
# Bascially run 2 approach

def CreateHyp_Fai(h_f, hists, scales):

 gi = gi_smeft

 Mu  = h_f[0]
 Fa2 = h_f[1]
 Fa3 = h_f[2]
 Fk1 = h_f[3]
 Fa1 = 1 - abs(Fa2) - abs(Fa3) - abs(Fk1)
 a1 = gi[0]
 a2 = gi[1]
 a3 = gi[2]
 k1 = gi[3]

 if len(h_f) > 4 : # assuming 8C scenario
  Fz2 = h_f[4]
  Fz3 = h_f[5]
  Fg2 = h_f[6]
  Fg3 = h_f[7]
  Fa1 =  1 - abs(Fa2) - abs(Fa3) - abs(Fk1) - abs(Fz2) - abs(Fz3) - abs(Fg2) - abs(Fg3)
  z2 = gi[4]
  z3 = gi[5]
  g2 = gi[6]
  g3 = gi[7]

 h = hists[0].Clone()
 s = eval(scales[0])
 h.Scale(s)

 for i in range(1, len(hists)) :
  hi = hists[i].Clone()
  si = eval(scales[i])
  h = AddCorrHist(h, hi, si)

 return h

# Get coupling dependant Width Scale
# R Eqns use k1 and k2 - L1 set to 100 GeV in R calculations.
# R_WW, ZZ, Zg and gg are scaled by 2^2 to account for difference between Eqns (SM a1 = 2) and model (SM a1 = 1)
# (Solution adopted in : https://github.com/skyriacoCMS/HiggsAnalysis-CombinedLimit/blob/anomalous-couplings-histograms-merged/python/SpinZeroStructureAC.py)

# 2020/21 https://arxiv.org/abs/2002.09888

def GetWidthScale_run2(a1,a2,a3,k1):

 kappa=1.0
 kappa_tilde=0.0

 a1WW = a1
 a2WW = cw*cw*a2
 a3WW = cw*cw*a3
 k1WW = k1/csw - 2*sw*sw*L2*a2/(mZ2*csw)
 k2   = 2*sw*cw*k1/csw - 2*sw*cw*L2*a2/(mZ2*csw)

 sc = 2**2
 R_ZZ   = sc*(a1*a1/4. + 0.1695*k1*k1 + 0.09076*a2*a2 + 0.03809*a3*a3 + 0.8095*a1*k1/2. + 0.5046*a1*a2/2. + 0.2092*a2*k1 + 0.1023*k2*k2 + 0.1901*a1*k2/2. + 0.07429*k1*k2 + 0.04710*a2*k2)
 R_WW   = sc*(a1WW*a1WW/4. + 0.1320*k1WW*k1WW + 0.1944*a2WW*a2WW + 0.08075*a3WW*a3WW + 0.7204*a1WW*k1WW/2. + 0.7437*a1WW*a2WW/2. + 0.2774*k1WW*a2WW)
 R_Zgm  = sc*(1.118600*a1WW*a1WW/4. +0.0035*kappa*kappa -  0.125010*a1WW*kappa/2. + 0.000003*kappa*kappa - 0.00018*kappa*kappa + 0.003100*a1WW*kappa/2 +0.00126*kappa_tilde*kappa_tilde + 0.000005*kappa_tilde*kappa_tilde -0.00047*kappa_tilde*kappa_tilde)
 R_gmgm = sc*(1.6054*a1WW*a1WW/4. + 0.07312*kappa*kappa - 0.6854*a1WW*kappa/2. + 0.00002*kappa*kappa - 0.0018*kappa*kappa + 0.0085*a1WW*kappa/2. + 0.1699*kappa_tilde*kappa_tilde + 0.00002*kappa_tilde*kappa_tilde - 0.0031*kappa_tilde*kappa_tilde)

 R_gg = (1.1068*kappa*kappa + 0.0082*kappa*kappa - 0.1150*kappa*kappa + 2.5717*kappa_tilde*kappa_tilde + 0.0091*kappa_tilde*kappa_tilde - 0.1982*kappa_tilde*kappa_tilde)

 R_bb      = (kappa*kappa + kappa_tilde*kappa_tilde)
 R_cc      = (kappa*kappa + kappa_tilde*kappa_tilde)
 R_tautau  = (kappa*kappa + kappa_tilde*kappa_tilde)
 R_mumu    = (kappa*kappa + kappa_tilde*kappa_tilde)

 gammaH = (0.5824*R_bb + 0.2137*R_WW + 0.08187*R_gg + 0.06272*R_tautau + 0.02891*R_cc + 0.02619*R_ZZ + 0.002270*R_gmgm +  0.001533*R_Zgm + 0.0002176*R_mumu)/0.9998 # Sum of BR considered = 0.9998

 return gammaH

# 2021/22 https://arxiv.org/abs/2109.13363
# page 21 suggests -W-B (Madgraph, EFT Lhvv)conventions used here, so k2 int terms have difference sign wrt above run2 

def GetWidthScale(a1, a2, a3, k1, z2, z3, g2, g3):

 kappa=1.0
 kappa_tilde=0.0

 a1WW = a1
 a2WW = cw*cw*a2 + sw*sw*g2 + 2*sw*cw*z2
 a3WW = cw*cw*a3 + sw*sw*g3 + 2*sw*cw*z3
 k1WW = k1/csw + 2*sw*sw*L2*(g2-a2)/(mZ2*csw) + 2*L2*(sw/cw)*(z2/mZ2)
 k2   = 2*sw*cw*k1/csw + 2*sw*cw*L2*(g2-a2)/(mZ2*csw) + 2*L2*(z2/mZ2)

 sc = 2**2
 R_ZZ   = sc*(a1*a1/4. + 0.17*k1*k1 + 0.09*a2*a2 + 0.04*a3*a3 + 0.10*k2*k2 + 79.95*z2*z2 + 75.23*z3*z3 +29*g2*g2 + 29.47*g3*g3 + 0.81*a1*k1/2 + 0.5046*a1*a2/2 - 0.1901*a1*k2/2 - 1.56*a1*z2/2 + .06*a1*g2/2  + 0.21*a2*k1 - 0.07*k1*k2 -0.64*k1*z2 - 0.05*a2*k2 - 0.51*a2*z2 - 0.02*a2*g2 + 0.36*a3*z3 -0.57*a3*g3 + 1.8*k2*z2 - 0.05*k2*g2 -1.84*z2*g2 - 2.09*z3*g3)
 R_WW   = sc*(a1WW*a1WW/4. + 0.1320*k1WW*k1WW + 0.1944*a2WW*a2WW + 0.08075*a3WW*a3WW + 0.7204*a1WW*k1WW/2. + 0.7437*a1WW*a2WW/2. + 0.2774*k1WW*a2WW)

 kQz  = -(6*pi/alpha)*z2
 kQz_tilde = -(4*pi/alpha)*z3
 R_Zgm  = sc*(1.11965*a1WW*a1WW/4 - 0.12652*a1WW*kappa/2 + 0.00348*a1WW*kappa/2 -0.13021*a1WW*kQz/2 + 0.00357*kappa*kappa  + 0.000003*kappa*kappa - 0.00018*kappa*kappa + 0.00377*kQz*kQz + 0.00734*kappa*kQz - 0.00019*kappa*kQz +0.00849*kappa_tilde*kappa_tilde + 0.000004*kappa_tilde*kappa_tilde - 0.00025*kappa_tilde*kappa_tilde + 0.00883*kQz_tilde*kQz_tilde + 0.01723*kappa_tilde*kQz_tilde - 0.00024*kappa_tilde*kQz_tilde)

 kQg  = -(3*pi/alpha)*g2
 kQg_tilde = -(2*pi/alpha)*g3 
 R_gmgm = sc*(1.60932*a1WW*a1WW/4 - 0.69064*a1WW*kappa/2 + 0.00912*a1WW*kappa/2 - 0.49725*a1WW*kQg/2
        + 0.07404*kappa*kappa + 0.00002*kappa*kappa - 0.00186*kappa*kappa + 0.03841*kQg*kQg + 0.10666*kappa*kQg
        - 0.00136*kappa*kQg  + 0.20533*kappa_tilde*kappa_tilde + 0.00006*kappa_tilde*kappa_tilde - 0.003*kappa_tilde*kappa_tilde + 0.10252*kQg_tilde*kQg_tilde
        + 0.29018*kappa_tilde*kQg_tilde - 0.00202*kappa_tilde*kQg_tilde)

 R_gg = (1.1068*kappa*kappa + 0.0082*kappa*kappa - 0.1150*kappa*kappa + 2.5717*kappa_tilde*kappa_tilde + 0.0091*kappa_tilde*kappa_tilde - 0.1982*kappa_tilde*kappa_tilde)

 R_bb      = (kappa*kappa + kappa_tilde*kappa_tilde)
 R_cc      = (kappa*kappa + kappa_tilde*kappa_tilde)
 R_tautau  = (kappa*kappa + kappa_tilde*kappa_tilde)
 R_mumu    = (kappa*kappa + kappa_tilde*kappa_tilde)

 gammaH = (0.5824*R_bb + 0.2137*R_WW + 0.08187*R_gg + 0.06272*R_tautau + 0.02891*R_cc + 0.02619*R_ZZ + 0.002270*R_gmgm +  0.001533*R_Zgm + 0.0002176*R_mumu)/0.9998 # Sum of BR considered = 0.9998

 return gammaH

# Create the hypotheses using the signal model histograms (hypotheses/templates) scaled by model terms
# Assuming 4, 6 or 8 couplings

def CreateHyp_ai(h_a, hists, scales, doW):

 nC = len(h_a)
 
 a1 = h_a[0]
 a2 = h_a[1]
 a3 = h_a[2]
 k1 = h_a[3]
 z2 = 0
 z3 = 0
 g2 = 0
 g3 = 0
 
 if nC > 4 : z2 = h_a[4]
 if nC > 5 : z3 = h_a[5]
 if nC > 6 : g2 = h_a[6]
 if nC > 7 : g3 = h_a[7]

 h = hists[0].Clone()
 s = eval(scales[0])
 h.Scale(s)

 for i in range(1, len(hists)) :
  hi = hists[i].Clone()
  si = eval(scales[i])
  h = AddCorrHist(h, hi, si)

 if doW :
  #ws = GetWidthScale_run2(a1, a2, a3, k1)
  ws = GetWidthScale(a1, a2, a3, k1, z2, z3, g2, g3)
  h.Scale(1/ws)

 return h

# Convert from Higgs basis couplings to ai
# Scale cz coupling such that a1 = (cz + 1) which corresponds to model
# k1 has L^2 cancelled out (Signal model & contraints independent of Lambda choice)

def Convert_ciToai(h_c): # assume 4, 6  or 8 couplings

 nC = len(h_c)
 
 a1 =   (h_c[0] + 1)
 a2 = -1*h_c[1]*(e2/(2*sw*sw*cw*cw))
 a3 = -1*h_c[2]*(e2/(2*sw*sw*cw*cw))
 k1 =    h_c[3]*(e2/(sw*sw*mZ2))*L2
 
 if nC > 4: z2 = -1*h_c[4]*(e2/(2*sw*cw))
 if nC > 5: z3 = -1*h_c[5]*(e2/(2*sw*cw))
 if nC > 6: g2 = -1*h_c[6]*(e2/2)
 if nC > 7: g3 = -1*h_c[7]*(e2/2)

 if   nC == 4 : h_a = [a1, a2, a3, k1]
 elif nC == 6 : h_a = [a1, a2, a3, k1, z2, z3]
 elif nC == 8 : h_a = [a1, a2, a3, k1, z2, z3, g2, g3]
 else : sys.exit("convert_citoai treatment for "+str(nC)+" couplings not supported ")
 
 for i in range(0, len(h_a)) :
  if h_a[i] == -0 : h_a[i] = 0
  h_a[i] = round(h_a[i], 3)

 return h_a

# Convert from fractions fai to ai

def Convert_faiToai(h_f):

 nC = len(h_f)
 gi = gi_smeft

 sMu = sign(h_f[0])*sqrt(abs(h_f[0]))
 a2 = gi[1]*sign(h_f[1])*sqrt(abs(h_f[1]))*sMu
 a3 = gi[2]*sign(h_f[2])*sqrt(abs(h_f[2]))*sMu
 k1 = gi[3]*sign(h_f[3])*sqrt(abs(h_f[3]))*sMu

 if nC > 4 : z2 = gi[4]*sign(h_f[4])*sqrt(abs(h_f[4]))*sMu
 if nC > 5 : z3 = gi[5]*sign(h_f[5])*sqrt(abs(h_f[5]))*sMu
 if nC > 6 : g2 = gi[6]*sign(h_f[6])*sqrt(abs(h_f[6]))*sMu
 if nC > 7 : g3 = gi[7]*sign(h_f[7])*sqrt(abs(h_f[7]))*sMu
 
 if   nC == 4 :
  a1 = gi[0]*sqrt(1 - abs(h_f[1]) - abs(h_f[2]) - abs(h_f[3]))*sMu
  h_a = [a1, a2, a3, k1]
 elif nC == 6 :
  a1 = gi[0]*sqrt(1 - abs(h_f[1]) - abs(h_f[2]) - abs(h_f[3]) - abs(h_f[4]) - abs(h_f[5]))*sMu
  h_a = [a1, a2, a3, k1, z2, z3]
 elif nC == 8 :
  a1 = gi[0]*sqrt(1 - abs(h_f[1]) - abs(h_f[2]) - abs(h_f[3]) - abs(h_f[4]) - abs(h_f[5]) - abs(h_f[6]) - abs(h_f[7]))*sMu
  h_a = [a1, a2, a3, k1, z2, z3, g2, g3]
 else : sys.exit("convert_faitoai treatment for "+str(nC)+" couplings not supported ")

 for i in range(0, len(h_a)) :
  if h_a[i] == -0 : h_a[i] = 0
  h_a[i] = round(h_a[i], 3)

 return h_a

# Scan of Norm and Shapes Vs ai/Fai using build hypotheses

def NShape2D(src, cat, var, prod, model, coup_t, cX, cY, typ): 

 if "cr_" in cat : return
 
 R = [-1, 1, 0.2]  # DM
 if (typ == "ai" or typ == "ci") :
  if "g" in cX : R = [-10, 10, 0.5]
  else         : R = [-2, 2, 0.1]
 if  typ == "fai" : R = [-0.99, 0.99, 0.03] # .045

 nC = len(coup_t)
 ix = coup_t.index(cX)
 iy = coup_t.index(cY)
 tX = getName(cX, typ)
 tY = getName(cY, typ)

 f = ROOT.TFile.Open(''+src+'', 'read')

 hzero = []
 hists = []
 for i in range(0, len(model)) :
  hstr = ''+cat+'/'+var+'/histo_'+prod+'_H'+str(i+1)+'' 
  h = f.Get(""+hstr+"")
  if not h :
   h = f.Get(''+cat+'/'+var+'/histo_'+prod+'_H1') # dummy zero histograms so model works in a transparent way
   h.Scale(0)
   hzero.append('H'+str(i+1)+'')
  h.SetDirectory(0)
  hists.append(h)

 if len(hzero)>0 : print("\n2D No hyps : ", len(hzero), hzero, "Use dummy 0") 

 f.Close()

 xR = numpy.arange(R[0], R[1] + R[2], R[2])
 yR = numpy.arange(R[0], R[1] + R[2], R[2])
 for i in range(0, len(xR)) : xR[i] = round(xR[i], 3)
 for i in range(0, len(yR)) : yR[i] = round(yR[i], 3)

 graphN = ROOT.TGraph2D(len(xR)*len(yR))
 graphN.SetName("N")
 graphS = ROOT.TGraph2D(len(xR)*len(yR))
 graphS.SetName("S")

 k = -1
 minn = 10000
 mins = 10000

 for i in range(len(xR)):
  for j in range(len(yR)):

   k = k + 1
   x = xR[i]
   y = yR[j]
   hv = [0] * nC
   if typ == "fai" or typ == "ai" : hv[0]  = 1 # Mu or a1 always set to 1 (SM)
   hv[ix] = x
   hv[iy] = y

   Limit = 0
   if   typ == "fai" :
    if (abs(x) + abs(y)) > 1 : Limit = 1 
    else :
     ha = Convert_faiToai(hv)
     h  = CreateHyp_ai(ha, hists, model, False)  # Old approach with model_fai : h = CreateHyp_Fai(hv, hists, model)
     if abs(h.Integral()) < 0.0000001 : Limit = 1 # Can have very small norms at Fai edges so cant trust shape mean
   elif typ == "ci"  :
    ha = Convert_ciToai(hv)
    h  = CreateHyp_ai(ha, hists, model, True)
   elif typ == "ai"  :
    h  = CreateHyp_ai(hv, hists, model, True)

   if h.Integral() < 0.0 : Limit = 1   #DM Checks for badly defined hypotheses
   if "mix" in var : 
    if (h.GetMean() < -1 or h.GetMean() > 1) :
     Limit = 1
   elif "kd" in var :
    if (h.GetMean() < 0  or h.GetMean() > 1) :
     Limit = 1
     
   if Limit == 1 :
    graphN.SetPoint(k, x, y, numpy.nan)
    graphS.SetPoint(k, x, y, numpy.nan)
   else : 
    graphN.SetPoint(k, x, y, round(h.Integral(),3)) #DM I think this is ok for all scenarios 
    graphS.SetPoint(k, x, y, round(h.GetMean(),3))
    minn = min(minn, h.Integral()) 
    mins = min(mins, h.GetMean())
    
 graphN.SetNpx(500)
 graphN.SetNpy(500)
 canvas = ROOT.TCanvas('canvas_N'+cX+cY+'', '', 500, 500)
 graphN.SetTitle("Signal Norm; "+tX+"; "+tY+"; ")
 graphN.GetHistogram().GetXaxis().CenterTitle()
 graphN.GetHistogram().GetXaxis().SetTitleOffset(1.2)
 graphN.GetHistogram().GetYaxis().CenterTitle()
 graphN.GetHistogram().GetYaxis().SetTitleOffset(1.2)
 graphN.GetHistogram().GetZaxis().SetLabelSize(0.015)
 graphN.GetHistogram().SetMinimum(minn) 
 graphN.Draw("colz") # colzsurf1
 diamond = getDiamond(graphN) 
 if typ == "fai" : diamond.Draw("same")
 canvas.SaveAs("plots/N"+typ+cX+cY+"_"+cat+"_"+var+"_"+prod+".pdf")
 canvas.SaveAs("plots/N"+typ+cX+cY+"_"+cat+"_"+var+"_"+prod+".png")

 graphS.SetNpx(500)
 graphS.SetNpy(500)
 canvas = ROOT.TCanvas('canvas_S'+cX+cY+'', '', 500, 500)
 graphS.SetTitle("Signal shape; "+tX+"; "+tY+"; ")
 graphS.GetHistogram().GetXaxis().CenterTitle()
 graphS.GetHistogram().GetXaxis().SetTitleOffset(1.2)
 graphS.GetHistogram().GetYaxis().CenterTitle()
 graphS.GetHistogram().GetYaxis().SetTitleOffset(1.2)
 graphS.GetHistogram().GetZaxis().SetLabelSize(0.025)
 graphS.GetHistogram().SetMinimum(mins) 
 graphS.Draw("colz")
 if typ == "fai" : diamond.Draw("same") 
 canvas.SaveAs("plots/S"+typ+cX+cY+"_"+cat+"_"+var+"_"+prod+".pdf")
 canvas.SaveAs("plots/S"+typ+cX+cY+"_"+cat+"_"+var+"_"+prod+".png")

def getDiamond(graph):

 h2 = graph.GetHistogram();
 xMin = h2.GetXaxis().GetXmin();
 xMax = h2.GetXaxis().GetXmax();
 yMin = h2.GetYaxis().GetXmin();
 yMax = h2.GetYaxis().GetXmax();
 xMid = (xMax + xMin) / 2;
 yMid = (yMax + yMin) / 2;

 diamond = ROOT.TPolyLine(5)
 diamond.SetPoint(0, xMid, yMin)
 diamond.SetPoint(1, xMax, yMid)
 diamond.SetPoint(2, xMid, yMax)
 diamond.SetPoint(3, xMin, yMid)
 diamond.SetPoint(4, xMid, yMin)

 diamond.SetLineColor(ROOT.kWhite);
 diamond.SetLineWidth(2);

 return diamond


def NShape(src, cat, var, prod, model, coup_t, typ, minS, maxS, maxN):

 if "cr_" in cat : return
  
 graphsS = []
 graphsN = []

 nC = len(coup_t)
 
 for i in range(0, nC) : 
  graphS, graphN = NShape1D(src, cat, var, prod, model, coup_t, coup_t[i], typ)
  graphsS.append(graphS)
  graphsN.append(graphN)

 colors = ["cyan", "black", "black", "blue", "red", "red", "green", "green"]
 styles = [1, 1, 2, 1, 1, 2, 1, 2] 
  
 canvas = ROOT.TCanvas('canvas_N', '', 500, 500)
 legend = ROOT.TLegend(0.82, 0.5, 0.95, 0.95)
 
 for i in range(0, nC) :
  g = graphsN[i]
  g.SetLineWidth(2)
  g.SetLineColor(colors[i])
  g.SetLineStyle(styles[i])
  tX = getName(coup_t[i], typ)
  if i > 0 : legend.AddEntry(g, tX, "l") # exclude SM
  if i == 1 :
   g.SetTitle("Signal Norm")
   g.GetXaxis().SetTitle(""+typ+"")
   g.GetXaxis().CenterTitle()
   g.GetXaxis().SetTitleOffset(1.2)
   g.SetMinimum(0)
   g.SetMaximum(maxN)
   g.Draw("ALP")
  else :
   g.Draw("SAME")
 
 legend.Draw()
 canvas.Update()
 
 canvas.SaveAs("plots/N"+typ+"_"+cat+"_"+var+"_"+prod+".pdf")
 canvas.SaveAs("plots/N"+typ+"_"+cat+"_"+var+"_"+prod+".png")

 if "kd_" in var :
  minS = 0
  maxS = 1
 if "mix" in var : minS = -1
 
 canvas = ROOT.TCanvas('canvas_S', '', 500, 500)
 legend = ROOT.TLegend(0.82, 0.5, 0.95, 0.95)
 
 for i in range(0, nC) :
  g = graphsS[i]
  g.SetLineWidth(2)
  g.SetLineColor(colors[i])
  g.SetLineStyle(styles[i])
  tX = getName(coup_t[i], typ)
  if i > 0 : legend.AddEntry(g, tX, "l") # exclude SM
  if i == 1 :
   g.SetTitle("Signal Shape")
   g.GetXaxis().SetTitle(""+typ+"")
   g.GetXaxis().CenterTitle()
   g.GetXaxis().SetTitleOffset(1.2)
   g.SetMinimum(minS)
   g.SetMaximum(maxS)
   g.Draw("ALP")
  else :
   g.Draw("SAME")
 
 legend.Draw()
 canvas.Update()
 
 canvas.SaveAs("plots/S"+typ+"_"+cat+"_"+var+"_"+prod+".pdf")
 canvas.SaveAs("plots/S"+typ+"_"+cat+"_"+var+"_"+prod+".png")

def CheckSys(src, cat, var, prod, hyps_reweight, hypz, syst): 
   
 f = ROOT.TFile.Open(''+src+'', 'read')

 if "cr_" in cat : hyps = ["T1"] # Just SM in CR
 else            : hyps = hyps_reweight
 
 nhyps = len(hyps)

 for i in range(0, nhyps): 
  hrw = hyps[i]
  if hrw not in hypz :
   
   hstr = ""+cat+"/"+var+"/histo_"+prod+"_"+hrw+""

   if not f.Get(""+hstr+"_"+syst+"Up") : return
   
   h   = f.Get(""+hstr+"")
   hup = f.Get(""+hstr+"_"+syst+"Up")
   hdn = f.Get(""+hstr+"_"+syst+"Down")

   h.SetDirectory(0)
   h.SetLineColor(ROOT.kBlack)
   hup.SetDirectory(0)
   hup.SetLineColor(ROOT.kRed)
   hdn.SetDirectory(0)
   hdn.SetLineColor(ROOT.kGreen)

   canvas = ROOT.TCanvas('canvas'+hrw+'', '', 500, 500)
   h.Draw("hist")
   hup.Draw("same hist")
   hdn.Draw("same hist")
 
   canvas.SaveAs("plots/Sys_"+cat+"_"+var+"_"+prod+hrw+"_"+syst+".pdf")
   canvas.SaveAs("plots/Sys_"+cat+"_"+var+"_"+prod+hrw+"_"+syst+".png")
 
def NShape1D(src, cat, var, prod, model, coup_t, cX, typ):

 R = [-20, 20, 0.4] # 10, 0.2
 #if (typ == "ai" or typ == "ci") and "g" in cX : R = [-10, 10, 0.5]
 if  typ == "fai" : R = [-0.99, 0.99, 0.03]

 nC = len(coup_t)
 ix = coup_t.index(cX)
 tX = getName(cX, typ)

 f = ROOT.TFile.Open(''+src+'', 'read')

 hzero = []
 hists = []
 for i in range(0, len(model)) :
  hstr = ''+cat+'/'+var+'/histo_'+prod+'_H'+str(i+1)+''
  h = f.Get(""+hstr+"")
  if not h :
   h = f.Get(''+cat+'/'+var+'/histo_'+prod+'_H1') # dummy zero histograms so model works in a transparent way
   h.Scale(0)
   hzero.append('H'+str(i+1)+'')
  h.SetDirectory(0)
  hists.append(h)

 #if len(hzero)>0 : print("\n1D No hyps : ", len(hzero), hzero, "Use dummy 0") 
  
 f.Close()

 xR = numpy.arange(R[0], R[1] + R[2], R[2])
 for i in range(0, len(xR)) : xR[i] = round(xR[i], 3)

 graphN = ROOT.TGraph(len(xR))
 graphN.SetName("N"+tX+"")
 graphS = ROOT.TGraph(len(xR))
 graphS.SetName("S"+tX+"")

 k = 0
 for i in range(len(xR)):
  x = xR[i]
  hv = [0] * nC
  if typ == "fai" or typ == "ai" : hv[0]  = 1 # Mu or a1 always set to 1 (SM)
  hv[ix] = x

  if   typ == "fai" :
   ha = Convert_faiToai(hv)
   h  = CreateHyp_ai(ha, hists, model, False)
  elif typ == "ci"  :
   ha = Convert_ciToai(hv)
   h  = CreateHyp_ai(ha, hists, model, True) 
  elif typ == "ai"  :
   h  = CreateHyp_ai(hv, hists, model, True)
  
  graphN.SetPoint(k, x, round(h.Integral(),3))
  graphS.SetPoint(k, x, round(h.GetMean(),3))
  k = k + 1

 return graphS, graphN 

# As a test of the template extraction try to recreate the hypotheses using the templates scaled by the couplings

def CheckRewHypsfromTemps(src, dst, cat, var, prod, hyps_mc, AmpSq, hyps_c):

 f = ROOT.TFile.Open(''+dst+'', 'read')
 nH = len(hyps_c)

 temps = []
 for i in range(0, nH) :
  tstr = ''+cat+'/'+var+'/histo_'+prod+'_T'+str(i+1)+''
  t = f.Get(""+tstr+"")
  if not t : sys.exit("Error : "+tstr+" not found in "+dst+" ")
  t.SetDirectory(0)
  nk1 = CouplingPower(AmpSq[i], "k1")
  if nk1 > 0 : t.Scale(1/(10000**nk1)) # Undo the L^2 scaling for this test (wither in templates creation or in matrix) 
  temps.append(t)

 f.Close()

 for i in range(0, nH) :
  hv = hyps_c[i]
  h = CreateHyp_ai(hv, temps, AmpSq, False)
  hO = GetAvgSumReweight(src, cat, var, prod, hyps_mc, "H"+str(i+1)+"", bl, "", 1)
  hO, hO_e, leg = PrepareHistE(hO, var, prod, "H"+str(i+1)+" "+str(hv)+"")
  hO.SetMaximum(1.5*h.GetMaximum())
  hO.SetMinimum(0)

  canvas = ROOT.TCanvas('canvas_'+str(i)+'', '', 500, 500)
  hO.Draw("hist")
  hO_e.Draw("same E2")
  h.Draw("same hist")
  leg.Draw()
  canvas.SaveAs("plots/HypFromTemp_"+cat+"_"+var+"_"+prod+"_H"+str(i+1)+".pdf")
  canvas.SaveAs("plots/HypFromTemp_"+cat+"_"+var+"_"+prod+"_H"+str(i+1)+".png")

# Create signal hypotheses using reweighting
# For CR just use H1 and rename T1 for combine signal model

def CreateRewHyps(src, dst, cat, var, prod, hyps_mc, hyps_reweight, hypz, sf, scorr, bl, syst):

 if syst != "" : syst = "_"+syst

 if "cr_" in cat : hyps_reweight = ["H1"] # just SM in CR 

 nhyps = len(hyps_reweight)
 print("\nCreate "+prod+" H"+syst+" to "+cat+"/"+var+" ["+str(nhyps)+" Hyps]")
  
 hyps = [] # all reweighted hypotheses 
 for i in range(0, nhyps): 
  hrw = hyps_reweight[i]
  if hrw not in hypz :
   hyp = GetAvgSumReweight(src, cat, var, prod, hyps_mc, hrw, bl, syst, 0) 
   hyp.Scale(sf)
   hyp.Multiply(scorr)
   if "cr_" in cat : hyp.SetName("histo_"+prod+"_T"+str(i+1)+syst+"") # rename T1
   else            : hyp.SetName("histo_"+prod+"_H"+str(i+1)+syst+"")
   hyps.append(hyp)
  
 print("#Hyps "+prod+" (non-zero) :", len(hyps))

 fout = ROOT.TFile.Open(''+dst+'', 'update')
 if not fout.GetDirectory(''+cat+'/'+var+'/') : ROOT.gDirectory.mkdir(''+cat+'/'+var+'/')
 fout.cd(''+cat+'/'+var+'/')

 for i in range(0, len(hyps)): hyps[i].Write()
  
 fout.Close()

# Build shape systematics for EFT signal hypotheses 
 
def SysToHyps(src, dst, cat, var, prod, hyps_reweight, hypz, syst, pwg_mc, sys_type):

  if sys_type == 1 : hyps_reweight = ["H1"]
  if "cr_" in cat :  hyps_reweight = ["T1"]
  
  ref = prod+"_H0PM" 
  if "QCDscale_qqH" in syst : ref = pwg_mc # weights not in jhugen  
  
  fin = ROOT.TFile.Open(''+src+'', 'read')
  h_str    = ''+cat+'/'+var+'/histo_'+ref+'' 
  hsys_str = ''+cat+'/'+var+'/histo_'+ref+'_'+syst+''
  if not fin.Get(""+h_str+"") : return 
  if not fin.Get(""+hsys_str+"") : return 
  h    = fin.Get(""+h_str+"") 
  hsys = fin.Get(""+hsys_str+"")
  h.SetDirectory(0)
  hsys.SetDirectory(0)
  hsys.Divide(h)
  fin.Close()
  
  f = ROOT.TFile.Open(''+dst+'', 'read')

  nhyps = len(hyps_reweight)
 
  print("\nCopy Sys "+prod+" "+ref+"_"+syst+" to "+cat+"/"+var+" ["+str(nhyps)+" Hyps]")

  hyps = [] 
  for i in range(0, nhyps):

   hrw = hyps_reweight[i]
   if hrw not in hypz :
   
    hs = f.Get(''+cat+'/'+var+'/histo_'+prod+'_'+hrw+'')
    hs.SetDirectory(0)
    hs.Multiply(hsys)
    hs.SetName("histo_"+prod+"_"+hrw+"_"+syst+"")
    hyps.append(hs)
  
  print("#Hyps "+prod+" (non-zero) :", len(hyps))
     
  f.Close() 
 
  fout = ROOT.TFile.Open(''+dst+'', 'update')
  fout.cd(''+cat+'/'+var+'/')
  for i in range(0, len(hyps)): hyps[i].Write()
  fout.Close()
  
 
# Create templates using reweighted hypotheses and inverse of A² matrix

def CreateTemps(src, dst, cat, var, prod, hyps_mc, hyps_reweight, iM, AmpSq, bl):

 Plot = False

 Hzero = []
 hyps = [] # all reweighted hypotheses 
 for i in range(0, len(hyps_reweight)): 
  hrw = hyps_reweight[i]
  hyp = GetAvgSumReweight(src, cat, var, prod, hyps_mc, hrw, bl, "", 0)
  if hyp.Integral() == 0 : Hzero.append("H"+str(i+1)+"")
  hyps.append(hyp)
 print("Zero Hyp : ", len(Hzero), Hzero) 

 n_temps = len(AmpSq)

 temps = [] # Determine templates from hypotheses and inverse of A² matrix
 for r in range(0, n_temps):
  t = hyps[0].Clone()
  t.Scale(iM[r][0])
  for c in range(1,n_temps):
   tc = hyps[c].Clone()
   t = AddCorrHist(t, tc, iM[r][c])
  temps.append(t)

 fout = ROOT.TFile.Open(''+dst+'', 'update')
 if not fout.GetDirectory(''+cat+'/'+var+'/') : ROOT.gDirectory.mkdir(''+cat+'/'+var+'/')
 fout.cd(''+cat+'/'+var+'/')

 Tzero = []
 for i in range(0, n_temps): # Write temps to file
  temps[i].SetName("histo_"+prod+"_T"+str(i+1)+"")
  nk1 = CouplingPower(AmpSq[i], "k1")
  #DM if nk1 > 0 : temps[i].Scale(10000**nk1) # Scale k1 terms if L² not cancelled with Matrix trick (Small norms set to 0 in Combine)
  if temps[i].Integral() == 0 : Tzero.append("T"+str(i+1)+"")
  temps[i].Write()
 print("Zero T : ", len(Tzero), Tzero)
  
 fout.Close()

 if Plot == True : # plot for checks
  for i in range(0, n_temps):
   canvas = ROOT.TCanvas('canvas_'+str(i)+'', '', 500, 500)
   a = AmpSq[i]
   T, T_e, leg = PrepareHistE(temps[i], var, prod, "T"+str(i+1)+" "+a+"")

   T.Draw("hist")
   T_e.Draw("same E2")
   leg.Draw()

   canvas.SaveAs("plots/"+cat+"_"+var+"_"+prod+"_T"+str(i+1)+".pdf")
   canvas.SaveAs("plots/"+cat+"_"+var+"_"+prod+"_T"+str(i+1)+".png")

### Get Histogram with error and legend

def PrepareHistE(h, var, prod, hrw):

 h.GetXaxis().SetTitle(""+var+"")
 h.SetLineColor(ROOT.kRed)
 h.SetFillColor(ROOT.kRed)
 h.SetLineWidth(2)

 h_e = h.Clone()
 h_e.SetFillStyle(3001)
 h_e.SetFillColor(ROOT.kGray+2)
 h_e.SetMarkerSize(.01)

 leg = ROOT.TLegend(0.5,0.5,0.7,0.92)
 leg.SetBorderSize(0)
 leg.SetTextSize(0.04)
 leg.SetTextFont(42)
 leg.SetFillColor(0)
 leg.SetFillStyle(0)
 leg.SetHeader(""+prod+" "+hrw+"","C");
 leg.AddEntry(h,"Reweighted ("+str(round(h.Integral(),1))+")","f")

 return h, h_e, leg

### Make and plot reweighted hypothesis. 

def CheckRewHyps(src, cat, var, prod, hyps_mc, hyps_reweight, hypz, sf, scorr, bl, typeplot): 

 if "cr_" in cat : hyps_reweight = ["H1"] # Just SM in CR
 
 for i in range(0, len(hyps_reweight)) :

  hrw = hyps_reweight[i]
  if hrw in hypz : continue
  havg = GetAvgSumReweight(src, cat, var, prod, hyps_mc, hrw, bl, "", 1)
  havg.Scale(sf)
  havg.Multiply(scorr)
  
  canvas = ROOT.TCanvas('canvas_'+hrw+'', '', 500, 500)

  h, h_e, leg = PrepareHistE(havg, var, prod, hrw)

  h.SetMaximum(1.5*h.GetMaximum())
  h.SetMinimum(0)
  h.Draw("hist")
  h_e.Draw("same E2")

  if typeplot == 1 : # include all individual reweightings. 

   f = ROOT.TFile.Open(''+src+'', 'read')
   for i, hmc in enumerate(hyps_mc) :  

    hmcstr = ''+cat+'/'+var+'/histo_'+prod+'_'+hmc+''
    if not f.Get(""+hmcstr+""): sys.exit("Error : "+hmcstr+" not found in "+src+" ")
  
    hstr = ''+cat+'/'+var+'/histo_'+prod+'_'+hmc+'to'+hrw+''
    if hmc == hrw :
     #continue #DM
     print("Including "+hmc+" MC ")
     hstr = ''+cat+'/'+var+'/histo_'+prod+'_'+hmc+'' 
  
    if not f.Get(""+hstr+""): sys.exit("Error : "+hstr+" not found in "+src+" ")
    
    h = f.Get(""+hstr+"") 
    h.SetDirectory(0)
    h.Scale(sf)
    h.Multiply(scorr)
    h.SetLineColor(i+1) 
    h.SetLineWidth(2) 
    h.Draw("same e")
    leg.AddEntry(h,""+hmc+"","l")  
   f.Close()
    
  else : # 0 : compare to MC if present 
  
   if hrw in hyps_mc :
    f = ROOT.TFile.Open(''+src+'', 'read')
    hmcstr = ''+cat+'/'+var+'/histo_'+prod+'_'+hrw+''
    hmc = f.Get(''+hmcstr+'')
    if not hmc : sys.exit("Error : "+hmcstr+" not found")
    hmc.SetDirectory(0)
    hmc.Scale(sf)
    hmc.Multiply(scorr)
    hmc.SetLineWidth(2)
    hmc.SetLineColor(ROOT.kBlack)
    hmc.SetMarkerColor(ROOT.kBlack)
    f.Close()
    hmc.Draw("same e")
    leg.AddEntry(hmc,"MC","l")

  leg.Draw()

  canvas.SaveAs("plots/"+cat+"_"+var+"_"+prod+"_"+hrw+".pdf")
  canvas.SaveAs("plots/"+cat+"_"+var+"_"+prod+"_"+hrw+".png")


### Shape Correction for D_x(CP/Int/VBF) jhugen -> powheg
  
def ShapeJHUToPWG(src, cat, var, prod, pwg_mc, app):

 canvas = ROOT.TCanvas('canvas_pwg', '', 500, 500)

 f = ROOT.TFile.Open(''+src+'', 'read')
 pwgstr = ''+cat+'/'+var+'/histo_'+pwg_mc+''
 hpwg = f.Get(''+pwgstr+'')
 jhustr = ''+cat+'/'+var+'/histo_'+prod+'_H0PM'
 hjhu = f.Get(''+jhustr+'')
 if not hpwg : sys.exit("Error : "+pwgstr+" not found")
 if not hjhu : sys.exit("Error : "+jhustr+" not found")
 hpwg.SetDirectory(0)
 hpwg.SetLineWidth(2)
 hpwg.SetLineColor(ROOT.kBlack)
 hpwg.SetMarkerColor(ROOT.kBlack) 
 hjhu.SetDirectory(0)
 scale = hpwg.Integral()/hjhu.Integral()
 hjhu.Scale(scale) # just a shape correction

 if app ==1 :
  for i in range(0, hjhu.GetNbinsX() + 1): hjhu.SetBinError(i, 0.0)
  hpwg.Divide(hjhu)
 else       :
  hpwg.Divide(hpwg) # dummy -> no shape corection
  for i in range(0, hpwg.GetNbinsX() + 1): hpwg.SetBinError(i, 0.0)
 
 hpwg.Draw("e")
 
 canvas.SaveAs("plots/JHUtoPWGShape_"+cat+"_"+var+"_"+prod+".pdf")
 canvas.SaveAs("plots/JHUtoPWGShape_"+cat+"_"+var+"_"+prod+".png")

 f.Close() 
 return hpwg

### Make reweighted SM hypothesis and compare to jhugen and powheg ##

def CompareRewSMToPwg(src, cat, var, prod, hyps_mc, pwg_mc, sf, scorr, bl, msig, ac):

 rwsm = "H1"
 if ac == 1 : rwsm = "H0PM" 
 
 havg = GetAvgSumReweight(src, cat, var, prod, hyps_mc, rwsm, bl, "", 1)
 havg.Scale(sf)
 havg.Multiply(scorr)
 
 canvas = ROOT.TCanvas('canvas_pwg', '', 500, 500)

 h, h_e, leg = PrepareHistE(havg, var, prod, rwsm)

 h.SetMaximum(1.5*h.GetMaximum())
 h.SetMinimum(0)
 h.Draw("hist")
 h_e.Draw("same E2")

 f = ROOT.TFile.Open(''+src+'', 'read')
 pwgstr = ''+cat+'/'+var+'/histo_'+pwg_mc+''
 hpwg = f.Get(''+pwgstr+'')
 jhustr = ''+cat+'/'+var+'/histo_'+prod+'_H0PM'
 hjhu = f.Get(''+jhustr+'')
 if not hpwg : sys.exit("Error : "+pwgstr+" not found")
 hpwg.SetDirectory(0)
 hpwg.SetLineWidth(2)
 hpwg.SetLineColor(ROOT.kBlack)
 hpwg.SetMarkerColor(ROOT.kBlack)
 if not hjhu : print(""+jhustr+" not found")
 else :
  hjhu.SetDirectory(0)
  hjhu.SetLineWidth(2)
  hjhu.SetLineColor(ROOT.kBlue)
  hjhu.SetMarkerColor(ROOT.kBlue)
  hjhu.Scale(sf)
  hjhu.Multiply(scorr)
  hjhu.Draw("same e")
  leg.AddEntry(hjhu,"JHUGen","l")
  print("JHU -> Powheg :", round(hpwg.Integral()/hjhu.Integral(),2))
 f.Close()
 hpwg.Draw("same e")
 leg.AddEntry(hpwg,"Powheg","l")
 leg.Draw()

 print("RW -> Powheg :", round(hpwg.Integral()/havg.Integral(),2))

 canvas.SaveAs("plots/JHUtoPWG_"+cat+"_"+var+"_"+prod+".pdf")
 canvas.SaveAs("plots/JHUtoPWG_"+cat+"_"+var+"_"+prod+".png")

 print("Normalisation of SM signals")
 
 print(""+prod+" norm (EFT treatment) :", round(hpwg.Integral(),2))
 f = ROOT.TFile.Open(''+src+'', 'read')
 for ms in msig :
  hms = f.Get(''+cat+'/'+var+'/histo_'+ms+'')
  print(""+ms+" : ", round(hms.Integral(),2))
 f.Close()
 
def AddOtherTemplates(src, dst, cat , var, othertemp, msig):

 if len(othertemp) == 0 : return
 
 f = ROOT.TFile.Open(''+src+'', 'read')
 HistList = ROOT.TObjArray()
 HistNameList = []

 f.cd(""+cat+"/"+var+"/")
 d = ROOT.gDirectory
 for ih in d.GetListOfKeys():
  h = ih.ReadObj()
  if any("histo_"+x in h.GetName() for x in othertemp) :
   if h.GetName() not in HistNameList :
    h.SetDirectory(0)
    if msig == 1 : # change name to T1 for signal model
     name = h.GetName()
     if   "qqH_hww"  in name : name = name.replace("qqH_hww",  "VBF_T1")
     elif "ggH_hww"  in name : name = name.replace("ggH_hww",  "ggF_T1") 
     elif "WH_hww"   in name : name = name.replace("WH_hww",   "WH_T1")
     elif "ZH_hww"   in name : name = name.replace("ZH_hww",   "ZH_T1")   
     elif "ggZH_hww" in name : name = name.replace("ggZH_hww", "ggZH_T1") 
     else : sys.exit(""+name+" not considered a (minor) signal!?")
     h.SetName(name)
    HistList.Add(h)
    HistNameList.append(h.GetName())
      
 f.Close()

 if len(HistList)==0 : print("\nAddOtherTemplates : Nothing found for ", cat, var," in ", src)
 else                :

  print("\nAdd : ", HistNameList, "to "+cat+"/"+var+"")

  fout = ROOT.TFile.Open(''+dst+'', 'update')
  fout.cd(""+cat+"/"+var+"/")
  HistList.Write()
  fout.Close()

def FilesForDCMaker(dst, ana, cat, var, oth, prod, sys_type):
 
 print("\nMake datacard for "+cat+"/"+var+" \n") 

 prod_all = ["ggF", "VBF", "WH", "ggZH", "ZH"]
 
 fout = ROOT.TFile.Open(''+dst+'', 'read')

 sig     = []
 eft_ggf = []
 eft_ewk = []
 
 fout.cd(""+cat+"/"+var+"/")
 d = ROOT.gDirectory
 for ih in d.GetListOfKeys():
  h = ih.ReadObj()
  name = h.GetName()
  if "Up" in name or "Down" in name : continue
  
  for p in prod_all :
   if "_"+p+"_H" in name or "_"+p+"_T" in name :
    name = name.replace("histo_","")
    
    if name not in sig : sig.append(name) 
    
    if p in prod : # eft signal   
     if "ggF" in name     and name not in eft_ggf : eft_ggf.append(name)      
     if "ggF" not in name and name not in eft_ewk : eft_ewk.append(name)
     
 fout.Close()

 if      sys_type == 0 :
  eft_ggf = []
  eft_ewk = []
 elif sys_type == 1 :
  eft_ggf = [s for s in eft_ggf if s.endswith(("T1", "H1"))]
  eft_ewk = [s for s in eft_ewk if s.endswith(("T1", "H1"))]
   
 print("DC prep, Signals found :", sig)
 print("DC prep, ggF EFT Signals with full nuissances :", eft_ggf)
 print("DC prep, Ewk EFT Signals with full nuissances :", eft_ewk) 
 
 with open(""+ana+"/samples.py", "w") as f:

  f.write("samples = {}\n")
  for p in prod: f.write("reweight_"+p+" = []\n")
  for o in oth : f.write("samples['"+o+"'] = {}\n")
  for s in sig : f.write("samples['"+s+"'] = {}\n")
  f.write("eft_ewksys = "+str(eft_ewk)+" \n")
  f.write("eft_ggfsys = "+str(eft_ggf)+" \n")  
    
 with open(""+ana+"/variables.py", "w") as f:

  f.write("variables = {}\n")
  f.write("variables['"+var+"'] = {'cuts' : ['"+cat+"']}\n")

 with open(""+ana+"/cuts.py", "w") as f:

  f.write("cuts = {}\n")
  f.write("preselections = ''\n")
  f.write("cuts['"+cat+"'] = {}\n") 

 with open(""+ana+"/structure.py", "w") as f:

  f.write("structure = {}\n")
  for s in sig :    f.write("structure['"+s+"'] = { 'isSignal' : 1, 'isData'   : 0}\n")
  for o in oth : 
   if "DATA" in o : f.write("structure['"+o+"'] = { 'isSignal' : 0, 'isData'   : 1}\n")
   else           : f.write("structure['"+o+"'] = { 'isSignal' : 0, 'isData'   : 0}\n")


def CheckACNorms(src, cat, var, prod, hyps_mc):

 f = ROOT.TFile.Open(''+src+'', 'read')

 for h in hyps_mc :

  if h == "H0PM" : continue

  acstr = ''+cat+'/'+var+'/histo_'+prod+'_'+h
  hac = f.Get(''+acstr+'')
  
  smstr = ''+cat+'/'+var+'/histo_'+prod+'_H0PMto'+h
  hsm = f.Get(''+smstr+'')
 
  int1 = hac.Integral()
  int2 = hsm.Integral()

  norm_factor = int2/int1
  
  print("--------------------------------------------------")
  print("Normalization factor "+h+"     = "+str(norm_factor)+"")

 f.Close()

