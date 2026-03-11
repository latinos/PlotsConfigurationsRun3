import ROOT
import pandas as pd
import numpy as np
import uproot
import subprocess
import os

ROOT.EnableImplicitMT()

fnames = []
#path = "/eos/cms/store/group/phys_higgs/cmshww/calderon/HWWNano/Summer22EE_130x_nAODv12_Full2022v12/MCl1loose2022EEv12__MCCorr2022EEv12/"
path = "/eos/cms/store/group/phys_higgs/cmshww/calderon/HWWNano/Run2022EE_Prompt_nAODv12_Full2022v12/DATAl1loose2022EEv12__fakeW/"

cmd = ("find {} -name '*.root'").format(path)
fnames = subprocess.check_output(cmd, shell=True).strip().split(b'\n')
fnames = [fname.decode('ascii') for fname in fnames]

print("TEST INPUT FILES!!!!")
print("Will look for corrupted files")

total = len(fnames)
failed = 0
failed_files = []


for fname in fnames:
    print(fname)
    outp = ""
    num = os.path.getsize(fname)
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
             outp = "%3.1f %s" % (num, x)
             break
        num /= 1024.0
    print("size: " + outp)
    try:
        df = ROOT.RDataFrame("Events", fname)
        print(df.Count().GetValue())
    except:
        print("Warning: possible corrupted file!")
        print("-----------------------------------------------")
        failed += 1
        failed_files.append(fname)

        
print("Finished, number of corrupted files:")
print(failed)
print("Total number of files:")
print(total)
print("Failed files:")
print(failed_files)

for fname in failed_files:
    print("eos rm " + fname)
    os.system("eos rm " + fname)

print("DONE!")
  



