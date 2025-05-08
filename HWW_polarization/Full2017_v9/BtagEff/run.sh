#!/bin/bash                                                                                                                                                                                                                                                                     
source /afs/cern.ch/work/s/sblancof/private/Run2Analysis/sendEOSJobs/start.sh
cd /afs/cern.ch/work/s/sblancof/private/Run2Analysis/sendEOSJobs/Full2017_v9/BtagEff

python doBtagEff.py
