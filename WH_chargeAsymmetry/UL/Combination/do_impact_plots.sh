#!/bin/bash
if [ $# -eq 0 ];
then
  echo "$0: Missing arguments"
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


### Default parameters.
WORKSPACE=WORKSPACE # ../Combination/WH_chargeAsymmetry_WH_FullRun2_v9_high_pt_binning_WH_strength.root
POI=r_WH
PARAMETERS=r_WH=1,r_higgs=1
RANGES=r_WH=-2,3
NAME=Impacts_${FINAL_STATE}_v9_binning_blind_WH_strength


# Full Run2
if [ $FINAL_STATE == FullRun2 ]; then

	WORKSPACE=../Combination/WH_chargeAsymmetry_WH_FullRun2_v9_high_pt_binning_WH_strength.root
	POI=r_WH
	PARAMETERS=r_WH=1,r_higgs=1
	RANGES=r_WH=-2,3
	NAME=Impacts_${FINAL_STATE}_v9_binning_blind_WH_strength

# Full 2018
elif [ $FINAL_STATE == Full2018 ]; then

	WORKSPACE=../Combination/WH_chargeAsymmetry_WH_Full2018_v9_high_pt_binning_WH_strength.root
	POI=r_WH
	PARAMETERS=r_WH=1,r_higgs=1
	RANGES=r_WH=-3,4
	NAME=Impacts_${FINAL_STATE}_v9_binning_blind_WH_strength

# Full 2017
elif [ $FINAL_STATE == Full2017 ]; then

	WORKSPACE=../Combination/WH_chargeAsymmetry_WH_Full2017_v9_high_pt_binning_WH_strength.root
	POI=r_WH
	PARAMETERS=r_WH=1,r_higgs=1
	RANGES=r_WH=-3,4
	NAME=Impacts_${FINAL_STATE}_v9_binning_blind_WH_strength

# 2016noHIPM
elif [ $FINAL_STATE == 2016noHIPM ]; then

	WORKSPACE=../Combination/WH_chargeAsymmetry_WH_2016noHIPM_v9_high_pt_binning_WH_strength.root
	POI=r_WH
	PARAMETERS=r_WH=1,r_higgs=1
	RANGES=r_WH=-3,4
	NAME=Impacts_${FINAL_STATE}_v9_binning_blind_WH_strength
	
# 2016HIPM
elif [ $FINAL_STATE == 2016HIPM ]; then

	WORKSPACE=../Combination/WH_chargeAsymmetry_WH_2016HIPM_v9_high_pt_binning_WH_strength.root
	POI=r_WH
	PARAMETERS=r_WH=1,r_higgs=1
	RANGES=r_WH=-3,4
	NAME=Impacts_${FINAL_STATE}_v9_binning_blind_WH_strength

# Default case
else

 	echo "I still don't know this final state"
 	exit 1
	
fi

### Create directory and move into it:
mkdir -p Impact/

cd Impact/


# Plot (after all the jobs are done)
if [ $PLOT == True ]; then

	combineTool.py -M Impacts -d ${WORKSPACE} -m 125 -o ${NAME}.json --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs -n ${FINAL_STATE} -t -1

	plotImpacts.py -i ${NAME}.json -o ${NAME}

# Clean
elif [ $PLOT == Clean ]; then

	echo "Cleaning ..."
	
	rm combine_*
	rm higgsCombine_*
	rm condor_combine_*
	
	echo "Done cleaning!"

# Produce initial fit and fits for each nuisance:
else

	combineTool.py -M Impacts -d ${WORKSPACE} -m 125 --doInitialFit --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminDefaultMinimizerStrategy 0 --cminFallbackAlgo Minuit2,0:0.2 --stepSize 0.01 --cminPreScan -n ${FINAL_STATE}_blind -t -1

	combineTool.py -M Impacts -d ${WORKSPACE} -m 125 --doFits --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --job-mode=condor --freezeParameters r_higgs --sub-opts='+JobFlavour="workday"' --cminDefaultMinimizerStrategy 0 --cminFallbackAlgo Minuit2,0:0.01 --stepSize 0.01 --cminPreScan -n ${FINAL_STATE}_blind -t -1

fi
