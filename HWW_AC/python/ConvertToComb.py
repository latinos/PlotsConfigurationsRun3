
import sys
import re

name = sys.argv[1]

from m4C1V import coup_t as coup_4C1V
from m4C1V import model as model_4C1V

from m4C2V import coup_t as coup_4C2V
from m4C2V import model as model_4C2V

from m8C1V import coup_t as coup_8C1V
from m8C1V import model as model_8C1V

from m8C2V import coup_t as coup_8C2V
from m8C2V import model as model_8C2V
 
indent = 8
 
def BaseStructure(cv_vbf, cv_zh, cv_wh, cv_ggf):

 base = '''from HiggsAnalysis.CombinedLimit.PhysicsModel import * 

### base python class to study the Higgs coupling structure in the SMEFT Higgs basis 
   
class HWWSMEFT'''+name+'''(PhysicsModel):
    def __init__(self):

        self.info = 1

    def setModelBuilder(self, modelBuilder):

        PhysicsModel.setModelBuilder(self,modelBuilder)
        self.modelBuilder.doModelBOnly = False

    def getYieldScale(self,bin,proc):
        scaling=1.

        # SM treatment (CR or minor signal)  
        if   \"VBF_T1\"  in proc : scaling = \"scale_ewk_T1"
        elif \"ggZH_T1\" in proc : scaling = \"scale_ggf_T1"
        elif \"ZH_T1\"   in proc : scaling = \"scale_ewk_T1"
        elif \"WH_T1\"   in proc : scaling = \"scale_ewk_T1"
        elif \"ggF_T1\"  in proc : scaling = \"scale_ggf_T1"

        # EFT treatment 
        if   \"VBF_H\" in proc : scaling = \"scale_'''+cv_vbf+'''_\"+proc[4:]
        elif \"ZH_H\"  in proc : scaling = \"scale_'''+cv_zh+'''_\"+proc[3:]
        elif \"WH_H\"  in proc : scaling = \"scale_'''+cv_wh+'''_\"+proc[3:]
        elif \"ggF_H\" in proc : scaling = \"scale_'''+cv_ggf+'''_\"+proc[4:]

        if self.info == 1 :print(\"Will scale\", proc, \"in bin\", bin, \"by\", scaling)

        return scaling

    def setPhysicsOptions(self,physOptions):

        print(\"no input params\")

    def doParametersOfInterest(self): '''

 print(base)

def AddSimpleSMTerms(coup_t, ext_ggf): 

 print("\n"," "*(indent-1)+"# Final scaling terms for SM T1 signals","\n",)

 p = ""+coup_t[0]+"" # Assume 1st is SM coupling
 print(" "*indent+"self.modelBuilder.factory_(\"expr::scale_ewk_T1(\\\"pow(@0,4)*@1\\\","+p+", gammaH)\")")    
 print(" "*indent+"self.modelBuilder.factory_(\"expr::scale_ggf_T1(\\\"pow(@0,2)*@1\\\","+p+ext_ggf+", gammaH)\")")

def split3_at_nth_plus(expression, n1, n2):
  
   matches = [m.start() for m in re.finditer(r'\+', expression)]
   split_index1 = matches[n1 - 1]  # Get the nth occurrence index
   split_index2 = matches[n2 - 1]
   return expression[:split_index1], expression[split_index1 + 1: split_index2], expression[split_index2 + 1:]

def split4_at_nth_plus(expression, n1, n2, n3):
  
   matches = [m.start() for m in re.finditer(r'\+', expression)]
   split_index1 = matches[n1 - 1]  # Get the nth occurrence index
   split_index2 = matches[n2 - 1]
   split_index3 = matches[n3 - 1] 
   return expression[:split_index1], expression[split_index1 + 1: split_index2], expression[split_index2 + 1: split_index3], expression[split_index3 + 1:]  

def AddScalingTerms(model, coup_t, cv, ext_ggf): 

 print("\n"," "*(indent-1)+"# Final scaling terms for "+cv+" signal Hypotheses","\n",)
 
 for i in range(0, len(model)) :
  
  s = model[i]
  p = ""
  nC = 0
  for j in range(0, len(coup_t)) :
   c = coup_t[j]
   if c not in s : continue
   s = s.replace("("+c+"**4)","pow(@"+str(nC)+",4)") 
   s = s.replace("("+c+"**3)","pow(@"+str(nC)+",3)")
   s = s.replace("("+c+"**2)","pow(@"+str(nC)+",2)")
   s = s.replace(""+c+"","@"+str(nC)+"")
   p += ", "+c+ext_ggf+"" 
   nC = nC +1 
 
  if len(s) > 1000 :  # string too long for combine -> Split
   nterms = s.count(" + ")
   s1, s2, s3, s4 = split4_at_nth_plus(s, 30, 60, 90) #DM split3 used with 40, 80) and A,B,C  
   print(" "*indent+"#"+str(nterms)+" terms so split in 4 (A-D)")
   print(" "*indent+"self.modelBuilder.factory_(\"expr::EH"+str(i+1)+"A(\\\"("+s1+")*@"+str(nC)+"\\\""+p+", gammaH)\")")
   print(" "*indent+"self.modelBuilder.factory_(\"expr::EH"+str(i+1)+"B(\\\"("+s2+")*@"+str(nC)+"\\\""+p+", gammaH)\")")
   print(" "*indent+"self.modelBuilder.factory_(\"expr::EH"+str(i+1)+"C(\\\"("+s3+")*@"+str(nC)+"\\\""+p+", gammaH)\")")
   print(" "*indent+"self.modelBuilder.factory_(\"expr::EH"+str(i+1)+"D(\\\"("+s4+")*@"+str(nC)+"\\\""+p+", gammaH)\")")  
   print(" "*indent+"self.modelBuilder.factory_(\"expr::scale_"+cv+"_H"+str(i+1)+"(\\\"@0 + @1 + @2 + @3 \\\", EH"+str(i+1)+"A, EH"+str(i+1)+"B, EH"+str(i+1)+"C, EH"+str(i+1)+"D )\")")   
  else :
   print(" "*indent+"self.modelBuilder.factory_(\"expr::scale_"+cv+"_H"+str(i+1)+"(\\\"("+s+")*@"+str(nC)+"\\\""+p+", gammaH)\")")
    
def End():
   
 print("\n"," "*(indent-1)+"self.modelBuilder.doSet(\"POI\",poi)")

 print("\nHWWSMEFT"+name+" = HWWSMEFT"+name+"()")
    
# Careful with ordering in var

def CombVar(mv, eqn, var):
 
 p = ""
 for i in range(0, len(var)) : p += ", "+var[i]+"" 
 
 for i in range(0, len(var)) :
  v = var[i]
  if v != "" : eqn = eqn.replace(v, "@"+str(i)+"")  

 print(" "*indent+"self.modelBuilder.doVar('expr::"+mv+"(\""+eqn+"\""+p+")')")

def DeclareVar(p, ran):  

 print(" "*indent+"self.modelBuilder.doVar('"+p+ran+"')")

def AddFaiEqns(ext_ggf):

 DeclareVar("muV",   "[1,  0, 1000]")
 DeclareVar("muF",   "[1,  0, 1000]")
 DeclareVar("Fa2",   "[0, -1, 1]")
 DeclareVar("Fa3",   "[0, -1, 1]")
 DeclareVar("Fk1",   "[0, -1, 1]")
 DeclareVar("Fz2",   "[0, -.99, .99]")
 DeclareVar("Fz3",   "[0, -.99, .99]")
 DeclareVar("Fg2",   "[0, -.99, .99]")
 DeclareVar("Fg3",   "[0, -.99, .99]")

 print("\n"," "*(indent-1)+"poi='muV,muF,Fa2,Fa3,Fk1,Fz2,Fz3,Fg2,Fg3'")
 print("\n"," "*(indent-1)+"# HVV Amplitude couplings from Fai","\n")
 
 ###DM Adopted this in run 2 to keep Sum of fractions = 1 
 # self.modelBuilder.doVar("expr::fa2(\"@0\", Fa2)") 
 # self.modelBuilder.doVar("expr::fa3(\"(1-abs(@0))*@1\", Fa2, Fa3)") 
 # self.modelBuilder.doVar("expr::fa4(\"(1-abs(@0))*(1-abs(@1))*@2\", Fa2, Fa3, Fa4)") 
 ### Not needed if we focus on small Fai I think
 
 CombVar("g_a2", "0.39446", [""])
 CombVar("g_a3", "2.55052", [""])
 CombVar("g_k1", "-0.43638",[""])
 CombVar("g_z2", "0.048",   [""]) # AC numbers same as SMEFT?
 CombVar("g_z3", "0.053",   [""])
 CombVar("g_g2", "0.053",   [""])
 CombVar("g_g3", "0.054",   [""])
 
 CombVar("gammaH", "1.0",   [""]) #DM With mu floating the width is redundant

 print()
 
 CombVar("smuV", "sign(1,muV)*sqrt(abs(muV))", ["muV"])
 CombVar("a1", "sqrt(1 -abs(Fa2) -abs(Fa3) -abs(Fk1) -abs(Fz2) -abs(Fz3) -abs(Fg2) -abs(Fg3))*smuV", ["Fa2", "Fa3", "Fk1", "Fz2", "Fz3", "Fg2", "Fg3", "smuV"])
 CombVar("a2", "g_a2*sign(1,Fa2)*sqrt(abs(Fa2))*smuV", ["g_a2", "Fa2", "smuV"])
 CombVar("a3", "g_a3*sign(1,Fa3)*sqrt(abs(Fa3))*smuV", ["g_a3", "Fa3", "smuV"]) 
 CombVar("k1", "g_k1*sign(1,Fk1)*sqrt(abs(Fk1))*smuV", ["g_k1", "Fk1", "smuV"])
 CombVar("z2", "g_z2*sign(1,Fz2)*sqrt(abs(Fz2))*smuV", ["g_z2", "Fz2", "smuV"]) 
 CombVar("z3", "g_z3*sign(1,Fz3)*sqrt(abs(Fz3))*smuV", ["g_z3", "Fz3", "smuV"]) 
 CombVar("g2", "g_g2*sign(1,Fg2)*sqrt(abs(Fg2))*smuV", ["g_g2", "Fg2", "smuV"]) 
 CombVar("g3", "g_g3*sign(1,Fg3)*sqrt(abs(Fg3))*smuV", ["g_g3", "Fg3", "smuV"])

 print("")
 
 CombVar("smuF", "sign(1,muF)*sqrt(abs(muF))", ["muF"])
 CombVar("a1"+ext_ggf+"", "sqrt(1 -abs(Fa2) -abs(Fa3) -abs(Fk1) -abs(Fz2) -abs(Fz3) -abs(Fg2) -abs(Fg3))*smuF", ["Fa2", "Fa3", "Fk1", "Fz2", "Fz3", "Fg2", "Fg3", "smuF"])
 CombVar("a2"+ext_ggf+"", "g_a2*sign(1,Fa2)*sqrt(abs(Fa2))*smuF", ["g_a2", "Fa2", "smuF"])
 CombVar("a3"+ext_ggf+"", "g_a3*sign(1,Fa3)*sqrt(abs(Fa3))*smuF", ["g_a3", "Fa3", "smuF"]) 
 CombVar("k1"+ext_ggf+"", "g_k1*sign(1,Fk1)*sqrt(abs(Fk1))*smuF", ["g_k1", "Fk1", "smuF"])
 #CombVar("z2"+ext_ggf+"", "g_z2*sign(1,Fz2)*sqrt(abs(Fz2))*smuF", ["g_z2", "Fz2", "smuF"]) # Assuming 4C1V for ggF
 #CombVar("z3"+ext_ggf+"", "g_z3*sign(1,Fz3)*sqrt(abs(Fz3))*smuF", ["g_z3", "Fz3", "smuF"]) 
 #CombVar("g2"+ext_ggf+"", "g_g2*sign(1,Fg2)*sqrt(abs(Fg2))*smuF", ["g_g2", "Fg2", "smuF"]) 
 #CombVar("g3"+ext_ggf+"", "g_g3*sign(1,Fg3)*sqrt(abs(Fg3))*smuF", ["g_g3", "Fg3", "smuF"]) 
 
def AddWarsawBasisEqns():

 print("\n"," "*(indent-1)+"# EFT Higgs basis HVV couplings","\n")   
 
 DeclareVar("cHb",   "[0, -10, 10]")
 DeclareVar("cHD",   "[0, -5, 5]")
 DeclareVar("cHW",   "[0, -3, 3]")
 DeclareVar("cHWt",  "[0, -3, 3]")
 DeclareVar("cHWB",  "[0, -10, 10]")
 DeclareVar("cHWBt", "[0, -10, 10]")
 DeclareVar("cHB",   "[0, -5, 5]")
 DeclareVar("cHBt",  "[0, -5, 5]")

 print("\n"," "*(indent-1)+"poi='cHb,cHD,cHW,cHWt,cHWB,cHWBt,cHB,cHBt'")
 print("\n"," "*(indent-1)+"# HVV Amplitude couplings from EFT couplings","\n")

 CombVar("pi", "3.1416", [""])      
 CombVar("cw", "0.8768", [""])
 CombVar("sw", "0.4808", [""])
 CombVar("mZ", "91.2",   [""]) 
 CombVar("L",  "100",    [""])
 CombVar("e2", "0.0917", [""])
 CombVar("vL", "0.0605", [""]) # v^2/L^2 = 246^2/1000^2 =0.0605

 CombVar("mZ2",   "mZ*mZ",       ["mZ"])
 CombVar("L2",    "L*L",         ["L"]) 
 CombVar("csw",   "cw*cw-sw*sw", ["cw","sw"])
 CombVar("alpha", "e2/4*pi",     ["e2","pi"])

 print()

 CombVar("da1", "vL*(2*cHb + (6*e2/sw*sw)*cHWB + (1.5*(cw*cw/sw*sw) - 0.5)*cHD)", ["cHb", "cHWB", "cHD", "vL", "e2", "sw", "cw"])
 CombVar("a1",  "da1 + 1",                                                        ["da1"])
 CombVar("a2",  "-2*vL*(sw*sw*cHB + cw*cw*cHW + sw*cw*cHWB)",                     ["cHB", "cHWB", "cHW", "vL", "sw", "cw"])
 CombVar("a3",  "-2*vL*(sw*sw*cHBt + cw*cw*cHWt + sw*cw*cHWBt)",                  ["cHBt", "cHWt", "cHWBt", "vL", "sw", "cw"])
 CombVar("k1",  "vL*((-2*e2/sw*sw)*cHWB + (1 - (1/2*sw*sw))*cHD)",                ["cHWB", "cHD", "vL", "e2", "sw"])         
 CombVar("z2",  "-2*vL*(sw*cw*(cHW - cHB) + 0.5*(sw*sw - cw*cw)*cHWB)",           ["cHWB", "cHB", "cHW", "vL", "sw", "cw"])
 CombVar("z3",  "-2*vL*(sw*cw*(cHWt - cHBt) + 0.5*(sw*sw - cw*cw)*cHWBt)",        ["cHWt", "cHBt", "cHWBt", "vL", "sw", "cw"])
 CombVar("g2",  "-2*vL*(cw*cw*cHB + sw*sw*cHW - sw*cw*cHWB)",                     ["cHB", "cHWB", "cHW", "vL", "sw", "cw"])
 CombVar("g3",  "-2*vL*(cw*cw*cHBt + sw*sw*cHWt - sw*cw*cHWBt)",                  ["cHBt", "cHWt", "cHWBt", "vL", "sw", "cw"]) 
 
def AddHiggsBasisEqns():

 print("\n"," "*(indent-1)+"# EFT Higgs basis HVV couplings","\n")   
 
 DeclareVar("cZ",   "[0, -1, 1]")
 DeclareVar("cZZ",  "[0, -2, 2]")
 DeclareVar("cZZt", "[0, -2, 2]")
 DeclareVar("cZB",  "[0, -0.5, 0.5]")
 DeclareVar("cZg",  "[0, -3, 3]")
 DeclareVar("cZgt", "[0, -3, 3]")
 DeclareVar("cgg",  "[0, -10, 10]")
 DeclareVar("cggt", "[0, -10, 10]")

 print("\n"," "*(indent-1)+"poi='cZ,cZZ,cZZt,cZB,cZg,cZgt,cgg,cggt'")
 print("\n"," "*(indent-1)+"# HVV Amplitude couplings from EFT couplings","\n")
 
 CombVar("pi", "3.1416", [""])     
 CombVar("cw", "0.8768", [""])
 CombVar("sw", "0.4808", [""])
 CombVar("e2", "0.0917", [""])
 CombVar("mZ", "91.2",   [""])
 CombVar("L",  "100",    [""])

 CombVar("mZ2",   "mZ*mZ",       ["mZ"])
 CombVar("L2",    "L*L",         ["L"]) 
 CombVar("csw",   "cw*cw-sw*sw", ["cw","sw"])
 CombVar("alpha", "e2/4*pi",     ["e2","pi"])

 print()

 CombVar("a1", "cZ + 1",                       ["cZ"])
 CombVar("a2", "-1*cZZ*(e2/(2*sw*sw*cw*cw))",  ["cZZ", "e2", "sw", "cw"])
 CombVar("a3", "-1*cZZt*(e2/(2*sw*sw*cw*cw))", ["cZZt","e2", "sw", "cw"]) 
 CombVar("k1", "cZB*(e2/(sw*sw*mZ2))*L2",      ["cZB", "e2", "sw", "mZ2", "L2"])
 CombVar("z2", "-1*cZg*(e2/(2*sw*cw))",        ["cZg", "e2", "sw", "cw"])
 CombVar("z3", "-1*cZgt*(e2/(2*sw*cw))",       ["cZgt","e2", "sw", "cw"])
 CombVar("g2", "-1*cgg*(e2/2)",                ["cgg", "e2"])
 CombVar("g3", "-1*cggt*(e2/2)",               ["cggt", "e2"]) 
 
def AddWidthEqns(): 

 print("\n"," "*(indent-1)+"# SU2xU1 relationship","\n")
 
 CombVar("a1WW", "a1", ["a1"])
 CombVar("a2WW", "cw*cw*a2 + sw*sw*g2 + 2*sw*cw*z2", ["cw", "sw", "a2", "g2", "z2"])
 CombVar("a3WW", "cw*cw*a3 + sw*sw*g3 + 2*sw*cw*z3", ["cw", "sw", "a3", "g3", "z3"])
 CombVar("k1WW", "k1/csw + 2*sw*sw*L2*(g2-a2)/(mZ2*csw) + 2*L2*(sw/cw)*(z2/mZ2)",["csw", "cw", "sw", "L2", "mZ2", "k1", "a2", "g2", "z2"]) 
 CombVar("k2",    "2*sw*cw*k1/csw + 2*sw*cw*L2*(g2-a2)/(mZ2*csw) + 2*L2*(z2/mZ2)",["csw", "cw", "sw", "L2", "mZ2", "k1", "a2", "g2", "z2"])

 print("\n"," "*(indent-1)+"# Width equations","\n",)

 CombVar("kappa", "1.0", [""])
 CombVar("kappa_tilde", "0.0", [""])
 CombVar("R_ZZ",  "4*(a1*a1/4. + 0.17*k1*k1 + 0.09*a2*a2 + 0.04*a3*a3 + 0.10*k2*k2 + 79.95*z2*z2 + 75.23*z3*z3 +29*g2*g2 + 29.47*g3*g3 + 0.81*a1*k1/2 + 0.5046*a1*a2/2 - 0.1901*a1*k2/2 - 1.56*a1*z2/2 + .06*a1*g2/2  + 0.21*a2*k1 - 0.07*k1*k2 -0.64*k1*z2 - 0.05*a2*k2 - 0.51*a2*z2 - 0.02*a2*g2 + 0.36*a3*z3 -0.57*a3*g3 + 1.8*k2*z2 - 0.05*k2*g2 -1.84*z2*g2 - 2.09*z3*g3)", ["a1", "k1", "k2", "a2", "a3", "z2", "z3", "g2", "g3"])
 
 CombVar("R_WW", "4*(a1WW*a1WW/4. + 0.1320*k1WW*k1WW + 0.1944*a2WW*a2WW + 0.08075*a3WW*a3WW + 0.7204*a1WW*k1WW/2. + 0.7437*a1WW*a2WW/2. + 0.2774*k1WW*a2WW)", ["a1WW", "k1WW", "a2WW", "a3WW"])

 CombVar("kQz",       "-(6*pi/alpha)*z2", ["pi", "alpha", "z2"])
 CombVar("kQz_tilde", "-(4*pi/alpha)*z3", ["pi", "alpha", "z3"])                  
 CombVar("R_Zgm", "4*(1.11965*a1WW*a1WW/4 - 0.12652*a1WW*kappa/2 + 0.00348*a1WW*kappa/2 -0.13021*a1WW*kQz/2 + 0.00357*kappa*kappa  + 0.000003*kappa*kappa - 0.00018*kappa*kappa + 0.00377*kQz*kQz + 0.00734*kappa*kQz - 0.00019*kappa*kQz +0.00849*kappa_tilde*kappa_tilde + 0.000004*kappa_tilde*kappa_tilde - 0.00025*kappa_tilde*kappa_tilde + 0.00883*kQz_tilde*kQz_tilde + 0.01723*kappa_tilde*kQz_tilde - 0.00024*kappa_tilde*kQz_tilde)", ["a1WW", "kappa_tilde", "kappa", "kQz_tilde", "kQz" ])

 CombVar("kQg",       "-(3*pi/alpha)*g2", ["pi", "alpha", "g2"])
 CombVar("kQg_tilde", "-(2*pi/alpha)*g3", ["pi", "alpha", "g3"])                 
 CombVar("R_gmgm", "4*(1.60932*a1WW*a1WW/4 - 0.69064*a1WW*kappa/2 + 0.00912*a1WW*kappa/2 - 0.49725*a1WW*kQg/2 + 0.07404*kappa*kappa + 0.00002*kappa*kappa - 0.00186*kappa*kappa + 0.03841*kQg*kQg + 0.10666*kappa*kQg - 0.00136*kappa*kQg  + 0.20533*kappa_tilde*kappa_tilde + 0.00006*kappa_tilde*kappa_tilde - 0.003*kappa_tilde*kappa_tilde + 0.10252*kQg_tilde*kQg_tilde + 0.29018*kappa_tilde*kQg_tilde - 0.00202*kappa_tilde*kQg_tilde)", ["a1WW", "kappa_tilde", "kappa", "kQg_tilde", "kQg"])

 CombVar("R_gg", "1.1068*kappa*kappa + 0.0082*kappa*kappa - 0.1150*kappa*kappa + 2.5717*kappa_tilde*kappa_tilde + 0.0091*kappa_tilde*kappa_tilde - 0.1982*kappa_tilde*kappa_tilde", ["kappa_tilde", "kappa"])

 CombVar("R_kk", "kappa*kappa + kappa_tilde*kappa_tilde", ["kappa_tilde","kappa"])

 CombVar("gammaH", "1/((0.5824*R_kk + 0.2137*R_WW + 0.08187*R_gg + 0.06272*R_kk + 0.02891*R_kk + 0.02619*R_ZZ + 0.002270*R_gmgm +  0.001533*R_Zgm + 0.0002176*R_kk)/0.9998)", ["R_kk", "R_WW", "R_gg", "R_ZZ", "R_gmgm", "R_Zgm"])

##########  Run config builder you want here ################# 

BaseStructure("8C2V", "8C2V", "4C2V", "4C1V") # EFT signal type for VBF, ZH, WH, ggF

ext_ggf = ""

if name == "Fai" :
 ext_ggf = "F"
 AddFaiEqns(ext_ggf)
elif name == "ciHB" : 
 AddHiggsBasisEqns()
 AddWidthEqns()
elif name == "ciWB" : 
 AddWarsawBasisEqns()
 AddWidthEqns()
else : sys.exit(""+name+" not recognised")
 
AddSimpleSMTerms(coup_8C2V, ext_ggf)

AddScalingTerms(model_8C2V, coup_8C2V, "8C2V", "")
AddScalingTerms(model_4C2V, coup_4C2V, "4C2V", "")
AddScalingTerms(model_4C1V, coup_4C1V, "4C1V", ext_ggf)

End()   
