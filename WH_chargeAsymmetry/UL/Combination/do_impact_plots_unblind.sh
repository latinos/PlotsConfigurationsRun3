#!/bin/bash
if [ $# -eq 0 ];
then
	echo "$0: Missing arguments 'final state':"
	echo ""
	echo "bash do_impact_plots_unblind.sh FullRun2"
	echo "bash do_impact_plots_unblind.sh FullRun2_WHSS"
	echo "bash do_impact_plots_unblind.sh FullRun2_WH3l"
	echo ""
	echo "bash do_impact_plots_unblind.sh Full2018"
	echo "bash do_impact_plots_unblind.sh Full2017"
	echo "bash do_impact_plots_unblind.sh 2016noHIPM"
	echo "bash do_impact_plots_unblind.sh 2016HIPM"
	echo ""
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
WORKSPACE=WORKSPACE # ../Combination/WH_chargeAsymmetry_WH_FullRun2_v9_high_pt_binning_WH_strength.root
POI=r_WH
PARAMETERS=r_WH=1,r_higgs=1
RANGES=r_WH=-10,10
NAME=Impacts_${FINAL_STATE}_v9_binning_WH_strength


# Full Run2
if [ $FINAL_STATE == FullRun2 ]; then

	WORKSPACE=../Combination/WH_chargeAsymmetry_WH_FullRun2_v9_high_pt_binning_WH_strength.root
	POI=r_WH
	PARAMETERS=r_WH=1,r_higgs=1
	RANGES=r_WH=-10,10
	NAME=Impacts_${FINAL_STATE}_v9_binning_WH_strength

# Full Run2 WHSS
elif [ $FINAL_STATE == FullRun2_WHSS ]; then

	WORKSPACE=../Combination/WH_chargeAsymmetry_WH_FullRun2_v9_WHSS_high_pt_binning_WH_strength.root
	POI=r_WH
	PARAMETERS=r_WH=1,r_higgs=1
	RANGES=r_WH=-10,10
	NAME=Impacts_${FINAL_STATE}_v9_binning_WH_strength
	
# Full Run2 WH3l
elif [ $FINAL_STATE == FullRun2_WH3l ]; then

	WORKSPACE=../Combination/WH_chargeAsymmetry_WH_FullRun2_v9_WH3l_binning_WH_strength.root
	POI=r_WH
	PARAMETERS=r_WH=1,r_higgs=1
	RANGES=r_WH=-10,10
	NAME=Impacts_${FINAL_STATE}_v9_binning_WH_strength
	
# Full 2018
elif [ $FINAL_STATE == Full2018 ]; then

	WORKSPACE=../Combination/WH_chargeAsymmetry_WH_Full2018_v9_high_pt_binning_WH_strength.root
	POI=r_WH
	PARAMETERS=r_WH=1,r_higgs=1
	RANGES=r_WH=-10,10
	NAME=Impacts_${FINAL_STATE}_v9_binning_WH_strength

# Full 2017
elif [ $FINAL_STATE == Full2017 ]; then

	WORKSPACE=../Combination/WH_chargeAsymmetry_WH_Full2017_v9_high_pt_binning_WH_strength.root
	POI=r_WH
	PARAMETERS=r_WH=1,r_higgs=1
	RANGES=r_WH=-10,10
	NAME=Impacts_${FINAL_STATE}_v9_binning_WH_strength

# 2016noHIPM
elif [ $FINAL_STATE == 2016noHIPM ]; then

	WORKSPACE=../Combination/WH_chargeAsymmetry_WH_2016noHIPM_v9_high_pt_binning_WH_strength.root
	POI=r_WH
	PARAMETERS=r_WH=1,r_higgs=1
	RANGES=r_WH=-10,10
	NAME=Impacts_${FINAL_STATE}_v9_binning_WH_strength
	
# 2016HIPM
elif [ $FINAL_STATE == 2016HIPM ]; then

	WORKSPACE=../Combination/WH_chargeAsymmetry_WH_2016HIPM_v9_high_pt_binning_WH_strength.root
	POI=r_WH
	PARAMETERS=r_WH=1,r_higgs=1
	RANGES=r_WH=-10,10
	NAME=Impacts_${FINAL_STATE}_v9_binning_WH_strength

# Default case
else

 	echo "I still don't know this final state. Here is the list of the available final states:"
	echo ""
	echo "bash do_impact_plots_unblind.sh FullRun2"
	echo "bash do_impact_plots_unblind.sh FullRun2_WHSS"
	echo "bash do_impact_plots_unblind.sh FullRun2_WH3l"
	echo ""
	echo "bash do_impact_plots_unblind.sh Full2018"
	echo "bash do_impact_plots_unblind.sh Full2017"
	echo "bash do_impact_plots_unblind.sh 2016noHIPM"
	echo "bash do_impact_plots_unblind.sh 2016HIPM"
	echo ""
 	exit 1
	
fi

### Create directory and move into it:
mkdir -p Impact_unblind/

cp ~/public/utils/index.php Impact_unblind/

cd Impact_unblind/


# Plot (after all the jobs are done)
if [ $PLOT == True ]; then

	combineTool.py -M Impacts -d ${WORKSPACE} -m 125 -o ${NAME}.json --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} -n ${FINAL_STATE} --freezeParameters r_higgs

	plotImpacts.py -i ${NAME}.json -o ${NAME} --blind

# Clean
elif [ $PLOT == Clean ]; then

	echo "Cleaning ..."
	
	rm combine_*
	rm higgsCombine_*
	rm condor_combine_*
	
	echo "Done cleaning!"

# Produce initial fit and fits for each nuisance:
else

	combineTool.py -M Impacts -d ${WORKSPACE} -m 125 --doInitialFit --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --cminDefaultMinimizerStrategy 0 --cminFallbackAlgo Minuit2,0:0.2 --stepSize 0.01 --cminPreScan -n ${FINAL_STATE} --freezeParameters r_higgs

	combineTool.py -M Impacts -d ${WORKSPACE} -m 125 --doFits --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --job-mode=condor --sub-opts='+JobFlavour="workday"' --cminDefaultMinimizerStrategy 0 --cminFallbackAlgo Minuit2,0:0.01 --stepSize 0.01 --cminPreScan -n ${FINAL_STATE} --freezeParameters r_higgs

fi
