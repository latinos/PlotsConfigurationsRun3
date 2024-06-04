#!/usr/bin/env python                                                                                                                                                                                                                                                         

import sys
import optparse
import copy
import collections
import os.path
import math
import logging
import tempfile
import subprocess
import fileinput
import argparse
import numpy as np
from sys import argv

def defaultParser():

    parser = argparse.ArgumentParser(add_help=False)
    
    parser.add_argument(
        "-Sub",
        "--Submit",
        action='store_true',
        help="Submit files",
        default=False,
    )
    
    return parser

def run(submit=False):


    prePath = os.path.abspath(os.path.dirname(__file__))

    if "examples" in prePath:
        prePath = prePath.split("examples/")[0]   ## Assume you work in processor folder
       
    path = prePath + "examples/WW_2022/condor/EGamma_Run2022G-Prompt-v1/"
    #path = prePath + "examples/Full2022_v12/condor/MuonEG_Run2022D-ReReco-v1/"
    #output_path = "/eos/user/s/sblancof/MC/rootFiles/"
    output_path = "rootFiles"
    jobDir = path

    cmd = "find {} -type d -name '*'".format(path)
    
    fnames = subprocess.check_output(cmd, shell=True).strip().split(b'\n')
    fnames = [fname.decode('ascii').split("EGamma_Run2022G-Prompt-v1/")[1] for fname in fnames] 
    
    failed_jobs = []
    error_files = []
    script_files = []
    total_jobs = []
    
    for fname in fnames:
        
        file_name = output_path + "/mkShapes__WW_2022__ALL__" + fname + ".root"
        error_file = jobDir + fname + "/" + "err.txt"
        script_file = jobDir + fname + "/" + "script.py"

        total_jobs.append(fname)
        if os.path.exists(file_name) or fname=="":
            continue
        else:
            print("ERROR: File does not exist in output folder")
            print("LABEL: " + fname)
            failed_jobs.append(fname)
            error_files.append(error_file)
            script_files.append(script_file)

    print("=========================")
    print("Ratio of failed jobs: " + str(len(failed_jobs)) + "/" + str(len(fnames)) + " = " + str(round(100*len(failed_jobs)/len(fnames), 2)) + "%")
    

    if submit:
        resubmit = """
universe = vanilla
executable = run.sh
arguments = $(Folder)
should_transfer_files = YES
transfer_input_files = $(Folder)/script.py, /afs/cern.ch/work/s/sblancof/private/Run3Analysis/mkShapesRDF/mkShapesRDF/include/headers.hh, /afs/cern.ch/work/s/sblancof/private/Run3Analysis/mkShapesRDF/mkShapesRDF/shapeAnalysis/runner.py
output = $(Folder)/out.txt
error  = $(Folder)/err.txt
log    = $(Folder)/log.txt
request_cpus   = 1
+JobFlavour = "microcentury"
queue 1 Folder in  RPLME_ALLSAMPLES"""
        
        resubmit = resubmit.replace("RPLME_ALLSAMPLES", " ".join(failed_jobs))
        
        with open(jobDir + "submit_failed.jdl", "w") as f:
            f.write(resubmit)
            
            
        proc = subprocess.Popen(
            f"cd {jobDir}; condor_submit submit_failed.jdl;", shell=True
        )
        
        proc.wait()


    #### Count failed files per category
    
    category_jobs = []
    for cat in failed_jobs:
        if "EE" in cat:
            category_jobs.append(cat.split("E_")[0]+"E")
        else:
            category_jobs.append(cat.split("_")[0])
    
    array, counts = np.unique(category_jobs, return_counts=True)

    total_cat = []
    for	cat in total_jobs:
        if "EE" in cat:
            total_cat.append(cat.split("E_")[0]+"E")
        else:
            total_cat.append(cat.split("_")[0])
        
    array_tot, counts_tot = np.unique(total_cat, return_counts=True)

    print("\n")
    print("\n")
    print("----------------- COUNT ----------------")
    for key in range(len(array)):
        print("Number of failed " + array[key] + "  ->  " + str(counts[key]))
        print("Number of total " + array[key] + "  ->  " + str(counts_tot[array_tot==array[key]][0]))
        print("Ratio -> " + str(counts[key]/counts_tot[array_tot==array[key]][0]))
        print("\n")

if __name__ == "__main__":
    parser = defaultParser()
    args = parser.parse_args()
    
    doSubmit = args.Submit

    run(doSubmit)
