#!/bin/bash
if [ $# -eq 0 ];
then
  echo "$0: Missing arguments 'final state':"
	echo ""
	echo "bash do_gof_test.sh FullRun2"
	echo "bash do_gof_test.sh Full2018"
	echo "bash do_gof_test.sh Full2017"
	echo "bash do_gof_test.sh 2016noHIPM"
	echo "bash do_gof_test.sh 2016HIPM"
  exit 1
else
  echo "We got some argument(s)"
  echo "=========================="
  echo "Number of arguments.  : $#"
  echo "List of arguments...  : $@"
  echo "Arg #1: Final State   : $1"
  echo "Arg #2: Produce plots : $2"
  echo "=========================="
  FINAL_STATE=$1
  PLOT=$2
fi

cd $HOME/work/combine/CMSSW_14_1_0_pre4/src/
eval `scramv1 ru -sh`
cd -
ulimit -s unlimited
alias python=python3

### Default parameters
WORKSPACE=WORKSPACE # ../Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning_WH_strength.root
POI=r_WH
PARAMETERS=r_WH=1,r_higgs=1
RANGES=r_WH=-5,5

# Full Run 2
if [ $FINAL_STATE == FullRun2 ]; then
	
	WORKSPACE=../Combination/WH_chargeAsymmetry_WH_FullRun2_v9_high_pt_binning_WH_strength.root
	POI=r_WH
	PARAMETERS=r_WH=1,r_higgs=1
	RANGES=r_WH=-5,5
	NAME=${FINAL_STATE}_WH_strength

# Full 2018
elif [ $FINAL_STATE == Full2018 ]; then

	WORKSPACE=../Combination/WH_chargeAsymmetry_WH_Full2018_v9_high_pt_binning_WH_strength.root
	POI=r_WH
	PARAMETERS=r_WH=1,r_higgs=1
	RANGES=r_WH=-5,5
	NAME=${FINAL_STATE}_WH_strength

# Full 2017
elif [ $FINAL_STATE == Full2017 ]; then

	WORKSPACE=../Combination/WH_chargeAsymmetry_WH_Full2017_v9_high_pt_binning_WH_strength.root
	POI=r_WH
	PARAMETERS=r_WH=1,r_higgs=1
	RANGES=r_WH=-5,5
	NAME=${FINAL_STATE}_WH_strength

# 2016noHIPM
elif [ $FINAL_STATE == 2016noHIPM ]; then

	WORKSPACE=../Combination/WH_chargeAsymmetry_WH_2016noHIPM_v9_high_pt_binning_WH_strength.root
	POI=r_WH
	PARAMETERS=r_WH=1,r_higgs=1
	RANGES=r_WH=-5,5
	NAME=${FINAL_STATE}_WH_strength

# 2016HIPM
elif [ $FINAL_STATE == 2016HIPM ]; then
	
	WORKSPACE=../Combination/WH_chargeAsymmetry_WH_2016HIPM_v9_high_pt_binning_WH_strength.root
	POI=r_WH
	PARAMETERS=r_WH=1,r_higgs=1
	RANGES=r_WH=-5,5
	NAME=${FINAL_STATE}_WH_strength

# Default case
else
	echo "I still don't know this final state. This is the list of available final states:"
	echo ""
	echo "bash do_gof_test.sh FullRun2"
	echo "bash do_gof_test.sh Full2018"
	echo "bash do_gof_test.sh Full2017"
	echo "bash do_gof_test.sh 2016noHIPM"
	echo "bash do_gof_test.sh 2016HIPM"
	exit 1
fi

### Create directory:
mkdir -p GoF

cp /afs/cern.ch/user/n/ntrevisa/public/utils/index.php GoF/

### Plot (after fit to data and toys are done)
if [ $PLOT == True ]; then
	
	hadd -f GoF/higgsCombine${FINAL_STATE}.GoodnessOfFit.mH120.toys.root GoF/higgsCombine${FINAL_STATE}.GoodnessOfFit.mH120.*.root
	
	combineTool.py -M CollectGoodnessOfFit --input GoF/higgsCombine${FINAL_STATE}.GoodnessOfFit.mH120.root GoF/higgsCombine${FINAL_STATE}.GoodnessOfFit.mH120.toys.root -m 120.0 -o GoF/GoF_${FINAL_STATE}.json
	
	plotGof.py GoF/GoF_${FINAL_STATE}.json --statistic saturated --mass 120.0 -o GoF/GoF_${FINAL_STATE} --title-right=${FINAL_STATE} --range 0 1000
	
	echo "Cleaning ..."

	# Clean the mess
	rm GoF/combine*
	rm GoF/condor*
	rm GoF/higgsCombine${FINAL_STATE}.GoodnessOfFit.mH120*.root

	echo "Done cleaning!"
	
else
	
	### Fit on data and 100 toys
	cd GoF/
	
	combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n $FINAL_STATE
		
	combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated -t 1 -s 0:100:1 --dry-run --job-mode=condor --sub-opts='+JobFlavour="workday"' --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n $FINAL_STATE

		
	# Modify the sh file in order to submit 100 jobs running 10 toys each
	sed -i 's/-t 1/-t 10/g' condor_combine_task.sh

	# Finally, submit jobs to condor
	condor_submit condor_combine_task.sub

	cd -

fi
