
import sys
import os
import shutil
import importlib.util

from HypTools import CheckRewHyps, CompareRewSMToPwg, ShapeJHUToPWG, CreateRewHyps, SysToHyps, AddOtherTemplates, FilesForDCMaker, NShape, NShape2D, CheckSys, GetCVRW

######### input config ############

if len(sys.argv) < 2: raise RuntimeError("Missing required configuration input") 

cf_path = sys.argv[1]
spec = importlib.util.spec_from_file_location("config", cf_path)
cf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cf)

###################################

hyps_reweight, coup_t, model, hypz = GetCVRW(cf.prod, cf.rwgt)

print("Build EFT analysis ("+cf.ana+") for "+cf.tag+"")

var = cf.var
cat = cf.cat

src  = os.path.realpath("rootFiles/"+cf.tag+"/mkShapes__"+cf.tag+".root")
dst = os.path.realpath(""+cf.ana+"/rootFiles/"+cf.tag+"/mkShapes__"+cf.tag+".root")

if cf.Build == 1 :

 if os.path.isdir(""+cf.ana+""):
  sys.exit(""+cf.ana+" exists!")
 else:
  os.mkdir(""+cf.ana+"")
  os.mkdir(""+cf.ana+"/rootFiles/")
  os.mkdir(""+cf.ana+"/rootFiles/"+cf.tag+"") 

 for ic, c in enumerate(cat) :
  for v in var[ic]:

   for ip, p in enumerate(cf.prod) :
    scorr = ShapeJHUToPWG(src, c, v, p, cf.pwg[ip], cf.scorr[ip])
    CreateRewHyps(src, dst, c, v, p, cf.hyps_mc[ip], hyps_reweight[ip], hypz[ip], cf.SF[ip], scorr, cf.BL[ip], "")
    if cf.sys_type > 0 :
     for s in cf.sys_eft[ip] :  
      SysToHyps(src, dst, c, v, p, hyps_reweight[ip], hypz[ip], s+"Up",   cf.pwg[ip], cf.sys_type)
      SysToHyps(src, dst, c, v, p, hyps_reweight[ip], hypz[ip], s+"Down", cf.pwg[ip], cf.sys_type)  
   AddOtherTemplates(src, dst, c, v, cf.minorsig, 1)  
   AddOtherTemplates(src, dst, c, v, cf.other,    0)

if cf.Check > 0 : 
  
 for ic, c in enumerate(cat) :
  for v in var[ic]:
 
   for ip, p in enumerate(cf.prod) :

    ### Dependant on build Hyps (NShape SR only, works well for 1D distributions)

    #if not os.path.isdir(""+cf.ana+""): sys.exit(""+cf.ana+" does not exist!")
    #for cp in cf.pairs[ip] : NShape2D(dst, c, v, p, model[ip], coup_t[ip], cp[0],cp[1], "ci") # ci, fai, ai 
    #NShape(dst, c, v, p, model[ip], coup_t[ip], "ci", cf.minS, cf.maxS, cf.maxN)
    for s in cf.sys_eft[ip] : CheckSys(dst, c, v, p, hyps_reweight[ip], hypz[ip], s)
    
    ### Not build dependant

    scorr = ShapeJHUToPWG(src, c, v, p, cf.pwg[ip], cf.scorr[ip])
    #CheckRewHyps(src, c, v, p, cf.hyps_mc[ip], hyps_reweight[ip], hypz[ip], cf.SF[ip], scorr, cf.BL[ip], 0) 
    CompareRewSMToPwg(src, c, v, p, cf.hyps_mc[ip], cf.pwg[ip], cf.SF[ip], scorr, cf.BL[ip], cf.minorsig, 0)  
    
    
if cf.MakeDC == 1 :

 if not os.path.isdir(""+cf.ana+""): sys.exit(""+cf.ana+" does not exist!")

 for f in ["configuration","aliases","nuisances","plot"] : os.system("cp "+f+".py "+cf.ana+"/")
 
 for ic, c in enumerate(cat) :
  for v in var[ic] :
   
   FilesForDCMaker(dst, cf.ana, c, v, cf.other, cf.prod, cf.sys_type) 
   os.chdir(""+cf.ana+"/")
   os.system("mkShapesRDF -c 1 && mkDatacards")
   os.chdir("../")
 
  
 


