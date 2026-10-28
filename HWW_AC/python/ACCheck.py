
import sys
import os
import shutil
import importlib.util

from HypTools import CheckRewHyps, CompareRewSMToPwg, CheckACNorms, ShapeJHUToPWG

######### input config ############

if len(sys.argv) < 2: raise RuntimeError("Missing required configuration input") 

cf_path = sys.argv[1]
spec = importlib.util.spec_from_file_location("config", cf_path)
cf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cf)

###################################

print("Check AC analysis for "+cf.tag+"")

var = cf.var
cat = cf.cat

src  = os.path.realpath("rootFiles/"+cf.tag+"/mkShapes__"+cf.tag+".root")
 
for ic, c in enumerate(cat) :
 for v in var[ic]:
 
  for ip, p in enumerate(cf.prod) :

   CheckACNorms(src, c, v, p, cf.hyps_mc[ip])
   scorr = ShapeJHUToPWG(src, c, v, p, cf.pwg[ip], cf.scorr[ip])
   CheckRewHyps(src, c, v, p, cf.hyps_mc[ip], cf.rwgt[ip], [], cf.SF[ip], scorr, cf.BL[ip], 0) 
   CompareRewSMToPwg(src, c, v, p, cf.hyps_mc[ip], cf.pwg[ip], cf.SF[ip], scorr, cf.BL[ip], cf.minorsig, 1)  
    
    


  
 


