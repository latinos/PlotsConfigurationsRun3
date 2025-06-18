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

    parser.add_argument(
        "-MC",
        "--Sample",
        type=str,
        help="Production name to run",
        required=False,
        default=None,
    )

    return parser

def run(submit=False, onlySample=None):


    prePath = os.path.abspath(os.path.dirname(__file__))

    if "sendEOSJobs" in prePath:
        prePath = prePath.split("sendEOSJobs/")[0]   ## Assume you work in processor folder


    path = prePath + "sendEOSJobs/Full2016_noHIPM/condor/DoubleEG_Run2016H_UL2016-v1/"
    #path = prePath + "sendEOSJobs/Full2016_noHIPM/condor/WW_2016_postVFP_complete/"
    output_path = "/eos/user/s/sblancof/MC/rootFiles/"
    jobDir = path

    cmd = "find {} -type d -name '*'".format(path)
    if onlySample:
        cmd = "find {} -type d -name '{}*'".format(path,onlySample)
        print(cmd)

    fnames = subprocess.check_output(cmd, shell=True).strip().split(b'\n')
    fnames = [fname.decode('ascii').split("DoubleEG_Run2016H_UL2016-v1/")[1] for fname in fnames]
    #fnames = [fname.decode('ascii').split("WW_2016_postVFP_complete/")[1] for fname in fnames]
    
    failed_jobs = []
    error_files = []
    script_files = []
    
    for fname in fnames:

        if onlySample:
            if not fname.startswith(onlySample):
                continue
        
        file_name = output_path + "/mkShapes__WW_2016_postVFP_complete__ALL__" + fname + ".root"

        error_file = jobDir + fname + "/" + "err.txt"
        script_file = jobDir + fname + "/" + "script.py"

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
transfer_input_files = $(Folder)/script.py, /afs/cern.ch/work/s/sblancof/private/Run2Analysis/mkShapesRDF/mkShapesRDF/include/headers.hh, /afs/cern.ch/work/s/sblancof/private/Run2Analysis/mkShapesRDF/mkShapesRDF/shapeAnalysis/runner.py, /afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/Full2017_v9/NNLOPS_reweight.root,/afs/cern.ch/work/s/sblancof/private/Run2Analysis/AlmaLinux9_mkShapes/mkShapesRDF/examples/Full2016_noHIPM/jetvetomaps.json,/afs/cern.ch/work/s/sblancof/private/Run2Analysis/sendEOSJobs/jsonpog-integration/POG/BTV/2016postVFP_UL/btagging.json.gz,/afs/cern.ch/work/s/sblancof/private/Run2Analysis/sendEOSJobs/Full2016_noHIPM/BtagEff/bTagEff_2016_postVFP_ttbar_DeepFlavB_loose.root
output = $(Folder)/out.txt
error  = $(Folder)/err.txt
log    = $(Folder)/log.txt
request_cpus   = 1
+JobFlavour = "testmatch"
requirements = (OpSysAndVer =?= "AlmaLinux9")
queue 1 Folder in  RPLME_ALLSAMPLES"""
        
        resubmit = resubmit.replace("RPLME_ALLSAMPLES", " ".join(failed_jobs))
        
        with open(jobDir + "submit_failed.jdl", "w") as f:
            f.write(resubmit)
            
            
        proc = subprocess.Popen(
            f"cd {jobDir}; condor_submit submit_failed.jdl;", shell=True
        )
        
        proc.wait()


if __name__ == "__main__":
    parser = defaultParser()
    args = parser.parse_args()
    
    doSubmit = args.Submit
    onlySample = args.Sample

    run(doSubmit, onlySample)
