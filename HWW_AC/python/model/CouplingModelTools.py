
import sys
import ROOT 
import numpy as np
import shutil
import math
from os import path
import random
import itertools
import random 

from sympy import Symbol
from sympy import sympify
from scipy import linalg
from mpmath import mp

##############################################################
# Build final signal models to be used with reweighted signal hypotheses

def BuildModel(iM, terms):

 print("\nmodel = [")

 for c in range(0,len(iM)):
  scale = "'"
  for r in range(0,len(iM)):
   n = float(iM[r, c])
   strn = GetStringNum(n)
   
   if abs(n) > 0 :

    if round(n,2) != 1.00 : scale += ""+terms[r]+"*"+strn+" + " 
    else :                  scale += ""+terms[r]+" + "
    
  scale = scale[:-3]
  print(""+scale+"',")
 print("]")

##############################

### Return an array of the amplitude squared (A²) terms for a given set of production and decay couplings ###
### Each term will be coupling(s) to the power of 4 : (c_prod*c_decay)² ### 

def AmpSqTerms(coup_p, coup_d, coup_t):
 
 nP = len(coup_p)
 nD = len(coup_d)
 nC = len(coup_t)

 ampSq = [] # Square the Prod*Decay A

 if nP > 0 and nD > 0 :
  for c_i in coup_p : 
   for c_j in coup_p : 
    for c_k in coup_d : 
     for c_l in coup_d : 
      ampSq.append(""+c_i+"*"+c_j+"*"+c_k+""+"*"+c_l+"") 

 elif nP > 0 and nD == 0 :
  for c_i in coup_p : 
   for c_j in coup_p : 
    ampSq.append(""+c_i+"*"+c_j+"") 

 elif nP == 0 and nD > 0 :
  for c_i in coup_d : 
   for c_j in coup_d : 
    ampSq.append(""+c_i+"*"+c_j+"") 

 ampSq_pow = [] # Organise by the power of the couplings

 for a in ampSq :
  a_pow = ""
  for c_i in coup_t : 
   n = a.count(""+c_i+"")
   if   n > 1 : a_pow += "*("+c_i+"**"+str(n)+")"  
   elif n > 0 : a_pow += "*"+c_i+""
  if a_pow.startswith("*") : a_pow = a_pow[1:]
  ampSq_pow.append(a_pow)

 ampSq_clean = [] # remove the double entries

 for a in ampSq_pow :
  if a not in ampSq_clean : ampSq_clean.append(a)

 return ampSq_clean

### A^2 to Fai

def getFaiExpression(ampSq, coup_t, cv): 

 fai = []
 
 for a in ampSq :
  if "2V" in cv : f = "pow(Mu,2)"
  else          : f = "Mu"  
  for c in coup_t :
   nc = CouplingPower(a, c)
   if   nc == 4 : f += "*pow(abs(F"+c+"),2)"                                                     
   elif nc == 3 :
    if c == "a1": f += "*pow(sqrt(abs(F"+c+")),3)"
    else        : f += "*sign(F"+c+")*pow(sqrt(abs(F"+c+")),3)"
   elif nc == 2 : f += "*abs(F"+c+")"
   elif nc == 1 :
    if c == "a1": f += "*sqrt(abs(F"+c+"))" 
    else        : f += "*sign(F"+c+")*sqrt(abs(F"+c+"))"
  f += "*"+a+""  
  fai.append(f)

 fa1 = "1" 
 for c in coup_t :
  if c != "a1": fa1 +=" - abs(F"+c+")"
  
 return fa1, fai

# count coupling power in a given term                                                                                            

def CouplingPower(a, c):

 nC = 0
 if   c+"**4" in a : nC = 4
 elif c+"**3" in a : nC = 3
 elif c+"**2" in a : nC = 2
 elif c       in a : nC = 1

 return nC

### Record which A² terms and hypotheses are really 0 becasue Z/g doesnt enter directly in decay vertex

def ZeroHyps(hyps, coup_t, NoD):

 zero = [] 

 for i in range(0, len(hyps)) :
  h = hyps[i]
  Decay = 0
  for c in coup_t :
   if c in NoD : continue
   if h[coup_t.index(c)] > 0 :
    Decay = 1
  if Decay == 0 : zero.append("H"+str(i+1)+"")

 return zero

def AmpSq_EFTapprox(ampSq, coup_t, cv):

  approx = []

  Cp = 2
  if "2V" in cv : Cp = 4
  
  for i in range(0, len(ampSq)) :
   
   acc = 0
   a = ampSq[i]
   for c in coup_t :
    nC = CouplingPower(a, c)
    if c == "a1" :
     if nC > 0 : acc = 1 # accept SM and all SM-BSM interference terms
    else :
     if nC==Cp : acc = 1 # accept all quadratic pure terms for fit stability
   if acc == 1 : approx.append(a)  
     
  return approx

def ZeroAmpSq(ampSq, NoD, cv):
 
 zero = []

 Cp = 2
 if "2V" in cv : Cp = 4

 for i in range(0, len(ampSq)) :
  a = ampSq[i]
  nC = 0 # count the coupling contribution of z/g 
  for cs in NoD :
   nC += CouplingPower(a, cs)
  if nC == Cp : zero.append("T"+str(i+1)+"") # c^4(c^2) cant exist in 2V(1V) scenario
  
 return zero
 
### Order by the power of the couplings : a^4 (pure), a^3b, a^2bc, abcd, a^2b^2
### Also return basic terms up to abcd - non-repeating with respect to coupling content (power agnostic)
### Useful for building hypotheses

def OrderAmpSq(ampSq, coup_t, cv):
 
 ampSq_basic = [] 
 ampSq_rest  = []
 record      = []

 if   cv == "4C2V" or cv == "6C2V"  or cv == "8C2V" or cv == "12C2V" :      
  pows = ["**4","**3","**2","*","**2"]
  nump = [1    ,1    ,1    ,3   ,2   ]
 elif cv == "4C1V" or cv == "8C1V": 
  pows = ["**2","*"] 
  nump = [1    ,1  ]
 elif cv == "2C2V": 
  pows = ["**4","**3","**2"]
  nump = [1    ,1    ,2    ]
 else :  sys.exit(" Power ordering of A^2 not defined for "+cv+"") 
  
 for i in range(len(pows)) :
  for a in ampSq :
   np = a.count(pows[i])
   if np == nump[i] and a not in ampSq_basic and a not in ampSq_rest :
    c_str = ""
    for c in coup_t :
     if c in a : c_str += c
    if c_str not in record : # basic terms : Non repeating with respect to coupling content
     ampSq_basic.append(a)    
     record.append(c_str) 
    else :                   # rest terms
     ampSq_rest.append(a) 

 print("\n# Order of basic A^2 terms : ", record)

 ampSq_all = ampSq_basic.copy()
 ampSq_all.extend(ampSq_rest)
    
 return ampSq_basic, ampSq_all

# Save hypotheses to be used for reweighting

def WriteHypsMap(hyps, cv):

 with open('Hyps_'+cv+'.h', 'w') as file:   

  file.write("\n#include \"ROOT/RVec.hxx\"")
  file.write("\n#include <map>")
  file.write("\n#include <string>")
  file.write("\n")
  file.write("\nusing namespace ROOT;")
  file.write("\nusing namespace ROOT::VecOps;")
  file.write("\n")

  file.write("\nconst std::map<std::string, RVecF> hyps_"+cv+" = {")
  for i,h in enumerate(hyps):
   hstr = str(h) 
   file.write("\n{\"H"+str(i+1)+"\", {"+hstr[1:-1]+"}},")
  file.write("\n};")

# Print Inv Matrix to be recorded. Works for mpmath 

def PrintMatrix(m, cv):

 print("\niM"+cv+" = [")
 for r in range(0,len(m)):
  print("[",end='')
  for c in range(0,len(m)):
   n = float(m[r, c])
   strn = GetStringNum(n)
   
   if c < (len(m)-1) : print(strn,",",end='') 
   else :              print(strn,"]",end='')
                              
  if r < (len(m)-1) : print(",")
  else : print("]")

# linalg inverse of Matrix used in run 2. float machine epsilon is 1e-15 (can represent 0)
# Careful with 1/Lambda^x and rounding error -> Can be simillar size by coincidence (1/10000**4 = 1e-16) so need to be careful here
# Trick to mask potential rounding errors : M = GetAmpSqMatrix(hyps,   ampSq, CV); MT = GetAmpSqMatrix(hypsMT, ampSq, CV); iM_la = GetInverseMatrix_la(M, MT) 

def GetInverseMatrix_la(m, ml): 

 if linalg.det(m)  == 0 :  sys.exit("m determinant is zero so matrix does not have an inverse "+str(np.linalg.cond(m))+"")
 im  = linalg.inv(m)

 for r in range(0,len(m)): 
  for c in range(0,len(m)):
   if abs(im[r,c])< 10**-14 : im[r,c] = 0
    
 im[im != 0] = 1
 
 if linalg.det(ml)  == 0 : sys.exit("ml determinant is zero so matrix does not have an inverse "+str(np.linalg.cond(ml))+"")
 iml = linalg.inv(ml)

 iml_s = np.multiply(iml, im) 
  
 return iml_s

# Preference for getting matrix inverse  
# mpmath inverse of Matrix. Slower but provides higher precision and can use it to mitigate floating-point rounding errors more effectively.

def GetInverseMatrix(m):

 nH = len(m)
 
 decimals = 100 # Set decimal precision 
 mp.dps = decimals

 for r in range(0,nH):
  for c in range(0,nH):
   if abs(m[r][c]) < 10**-decimals : m[r][c] = 0 # just to be sure -0 has no effect

 M = mp.matrix(m)
 iM = M**-1

 mine = -999
 for r in range(0,nH): 
  for c in range(0,nH):
   if abs(iM[r,c]) < 10**-decimals : iM[r,c] = 0
   if abs(iM[r,c]) < abs(mine) and abs(iM[r,c]) > 0 : mine = abs(iM[r,c])

 if mine < .001 : print("WARNING iM min element is smaller than .001 : ", mine, "-> Check Matrix printing function")
   
 return iM

# Needed if above option doesnt work (e.g Different couplings in production and decay)

def GetPseudoInverseMatrix(m):

 nH = len(m)

 for r in range(0,nH):
  for c in range(0,nH):
   if abs(m[r][c]) < 10**-10 : m[r][c] = 0
 
 im = np.linalg.pinv(m)
 iM = mp.matrix(im)

 mine = -999
 for r in range(0,nH): 
  for c in range(0,nH):
   if abs(iM[r,c]) < 10**-10 : iM[r,c] = 0
   if abs(iM[r,c]) < abs(mine) and abs(iM[r,c]) > 0 : mine = abs(iM[r,c])
   
 if mine < .001 : print("WARNING iM min element is smaller than .001 : ", mine, "-> Check Matrix printing function")
   
 return iM

# Convert entries of mp.matrix to strings
# Assume smallest element of inverse matrix is not smalller than .001 (.3f below)
# {0:.2E} scientifc notation (Not needed for coupling studies so far)

def GetStringNum(n):

 if n == -0 : n = float(0)
 
 if n == 0 : strn = "{:.1f}".format(n)
 elif abs(n-round(n))<.000001 :  strn = "{:.1f}".format(round(n,1)) # integer test
 elif abs(n) < .01 :             strn = "{:.3f}".format(round(n,3))
 else :                          strn = "{:.2f}".format(round(n,2))
 
 return strn

# print the A² terms

def PrintAmpSq(ampSq):
 
 as_str = "# AmpSq = ["
 for a in ampSq : as_str += " "+a+","  
 as_str = as_str.rstrip(as_str[-1])
 as_str += "]"

 print("\n"+as_str+"")
 
### Construct the A² matrix from the hypothesis array ###
### Matrix : hypotheses (row) * A² terms (column) ###

def GetAmpSqMatrix(hyp, ampSq, cv, coup_t):

 as_str = "["
 for a in ampSq : as_str += " "+a+","  
 as_str = as_str.rstrip(as_str[-1])
 as_str += "]"
 
 M = [] 
 for h in hyp :
  row = GetAmpSqValues(h, as_str, coup_t)
  M.append(row)

 return M

def GetAmpSqValues(h, as_str, coup_t):

 coup_dec = {cname: h[i] for i, cname in enumerate(coup_t)} # declare all coupling values
 
 ampsq_vals = eval(as_str,{}, coup_dec) # evaluate A² terms
 
 return ampsq_vals

## Build list of hypotheses for large number of coupling #####
# cval is vale of coupling in hyp when "on", s_req is the number of couplings which are on in hyp, val is the new value of the coupling being changed                                          
def AddHypsXc(hyp, cval, s_req, val, pos):

 hyp_add = []  
 for i in range(len(hyp)):
  h = hyp[i].copy()
  sum = 0
  for j in h : sum = sum+j
  if sum == s_req :
   first = h.index(cval) 
   if pos == "first"  : i1 = first
   if pos == "second" : i1 = h.index(cval, first + 1) 
   if pos == "last"   : i1 = len(h) - h[::-1].index(cval) - 1  
   h[i1] =  val 
   hyp_add.append(h)
  
 return hyp_add

def BuildHyps(coup_t, Asq, nH):

 nC = len(coup_t)
 hyps = []

 cval = 1.0
 
 for a in Asq  : 
  h = [0] * nC
  for c in coup_t :
   if c in a : h[coup_t.index(c)] = cval 
  hyps.append(h)

 hyp_2p5  = AddHypsXc(hyps, cval, cval*2, cval/2, "last")   # 2 c, new val 0.5 (c/2) 
 hyp_2p25 = AddHypsXc(hyps, cval, cval*2, cval/4, "last")   # 2 c, new val 0.25 (c/4)
 hyp_3p5s = AddHypsXc(hyps, cval, cval*3, cval/2, "second") # 3 c, new val 0.5 (c/2)
 hyp_3p5  = AddHypsXc(hyps, cval, cval*3, cval/2, "last")   # 3 c, new val 0.5 (c/2)

 hyps.extend(hyp_2p5)
 hyps.extend(hyp_2p25)
 hyps.extend(hyp_3p5s)
 hyps.extend(hyp_3p5)

 """ # Test 
 for i in range(len(hyps)):
  h = hyps[i]
  sum = 0
  for j in h : sum = sum+j
  if h[0]==cval and sum == 2 :
   first = h.index(cval)
   i1 = h.index(cval, first + 1)
   h[i1] = 0.25
 """
   
 if len(hyps) > nH : 
  nrem = len(hyps)-nH
  #print("\n# Will delete the last ",nrem," hypotheses")
  del hyps[-nrem:]
 
 return hyps

# Scale k*/L1^2 by some factor so the hypotheses have a normalisation ~ 1
# Use to cancel L^2

def k1LambdaScale(hyp, coup_t, scale):

 hyp_add = []  
 for i in range(len(hyp)):
  h = hyp[i].copy()
  hyp_add.append(h)

 for k in ["k1", "kz", "kw", "k2"]: 
  if k in coup_t :
   ik = coup_t.index(k)   
   for h in hyp_add : h[ik] = h[ik]*scale
  
  #else : print("\n# k not present so will not scale by Lambda")
  
 return hyp_add

