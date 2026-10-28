
from CouplingModelTools import AmpSqTerms, OrderAmpSq, PrintAmpSq, ZeroAmpSq, BuildHyps, k1LambdaScale, ZeroHyps, WriteHypsMap, GetAmpSqMatrix, GetInverseMatrix, PrintMatrix, BuildModel, AmpSq_EFTapprox, GetPseudoInverseMatrix

import sys
CV = str(sys.argv[1])

NoDirDec = ["z2","z3","g2","g3"] # For Higgs to WW SMEFT/AC
PseudoInv = 1 # Needed in some cases (e.g 8C x 4C )  
EFTApprox = 0 # Just keep SM, SM-BSM int, and pure BSM terms -> Not tested

#################### Basic Configuration
# Tested for 2,4,6 and 8 couplings (1 or 2 vertices)
# k1/k2 gets special treatment to cancel L^2

if   CV  == "8C1V" :    #-> SMEFT coupling Model study

 CoupP = [] 
 CoupD = ["a1","a2","a3","k1","z2","z3","g2","g3"]

elif CV  == "8C2V" :    #-> SMEFT coupling Model for VBF/ZH [8 HVV/Zg/gg couplings] HWW. Including 4 HZg/Hgg couplings in Decay vertex -> corresponding A^2 matrix has an inverse (helps to keep matrix diagonal). Some hypotheses are 0, e.g z/g^4 cant exist as HWW explxitly set to 0. 

 CoupP = ["a1","a2","a3","k1","z2","z3","g2","g3"] 
 CoupD = ["a1","a2","a3","k1","z2","z3","g2","g3"]
 
elif CV  == "6C2V" :    #-> SMEFT coupling Model for simplified ZH [6 HVV/Zg couplings] HWW. Including 2 HZg couplings in Decay vertex -> corresponding A^2 matrix has an inverse (helps to keep matrix diagonal). Some hypotheses are 0, e.g z/g^4 cant exist as HWW explxitly set to 0. 

 CoupP = ["a1","a2","a3","k1","z2","z3"] 
 CoupD = ["a1","a2","a3","k1","z2","z3"]
 
elif CV == "4C2V" :  #-> SMEFT Coupling Model for WH

 CoupP = ["a1","a2","a3","k1"]   
 CoupD = ["a1","a2","a3","k1"]
 
elif CV == "4C1V" :  #-> SMEFT coupling model for ggH 

 CoupP = [] 
 CoupD = ["a1","a2","a3","k1"] 

elif CV == "2C2V" :  #-> VBF/VH AC Coupling Model in Run 2 AC 

 CoupP = ["a1","a2"]
 CoupD = ["a1","a2"] 

elif CV  == "12C2V" :  #-> General Coupling model  

 CoupP = ["a1","z2","z3","kz","w2","w3","kw","k2","x2","x3","g2","g3"] 
 CoupD = ["a1","w2","w3","kw"]
 
else : sys.exit(" Couplings for "+CV+" not defined ")
 
###########################

CoupT = []
for c_i in CoupP : CoupT.append(c_i)
for c_i in CoupD : 
 if c_i not in CoupT : CoupT.append(c_i) 

print("\ncoup_t = ",CoupT)
 
ampSq = AmpSqTerms(CoupP, CoupD, CoupT)
if EFTApprox == 1 : ampSq = AmpSq_EFTapprox(ampSq, CoupT, CV) # worked with full 8C2V approach

ampSq_basic, ampSq = OrderAmpSq(ampSq, CoupT, CV)

print("\nAmpSq = ", ampSq)
print("\n# Number of terms : ", len(ampSq))

ampSq_z = ZeroAmpSq(ampSq, NoDirDec, CV) # No direct decay so pure a**4(a**2) doesnt exist for 2V(1V)
if len(ampSq_z) > 0 :
 print("\nAmpSq_zero = ", ampSq_z)
 print("\n# Number of non-zero terms : ",len(ampSq)-len(ampSq_z))
 
nH = len(ampSq)

hyps   = BuildHyps(CoupT, ampSq_basic, nH)
hypsL2 = k1LambdaScale(hyps, CoupT, -10000) # Scale k* terms by L^2, this way they have significant norm
hypsMT = k1LambdaScale(hyps, CoupT, -1)     # Use to build coupling Matrix, Trick to cancel out L^2 

print("\n# Number of Hypotheses needed/created :", nH,"/", len(hypsL2))
print("\nHyps =", hypsL2)

WriteHypsMap(hypsL2, CV)

hyps_z = ZeroHyps(hyps, CoupT, NoDirDec) # No direct decay
if len(hyps_z) > 0 :
 print("\nHyps_zero = ", hyps_z)
 print("\n# Number of non-zero hypotheses : ",len(hyps)-len(hyps_z))

MT = GetAmpSqMatrix(hypsMT, ampSq, CV, CoupT)

if PseudoInv == 1 : iM = GetPseudoInverseMatrix(MT) # pseudo inverse for X X Y couplings
else :              iM = GetInverseMatrix(MT)

#PrintMatrix(iM, "")

BuildModel(iM, ampSq) 


