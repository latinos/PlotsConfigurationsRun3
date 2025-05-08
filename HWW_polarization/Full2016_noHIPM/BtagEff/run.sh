#!/bin/bash                                                                                                                                                                                                                                                                     
source /afs/cern.ch/work/s/sblancof/private/Run2Analysis/sendEOSJobs/start.sh
cd /afs/cern.ch/work/s/sblancof/private/Run2Analysis/sendEOSJobs/Full2016_noHIPM/BtagEff

python doBtagEff.py
