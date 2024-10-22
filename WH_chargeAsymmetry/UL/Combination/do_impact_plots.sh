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


### Default parameters. We may want to make them accessible as input parameters
WORKSPACE=../Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning_WH_strength.root
POI=r_WH
PARAMETERS=r_WH=1,r_higgs=1
RANGES=r_WH=-5,5
NAME=Impacts_${FINAL_STATE}_v9_binning_WH_strength


### Prepare list of channels
WHSS_2018_HIGH_PT=mask_WH_SS_em_1j_minus_2018=1,mask_WH_SS_em_1j_plus_2018=1,mask_WH_SS_mm_1j_minus_2018=1,mask_WH_SS_mm_1j_plus_2018=1,mask_WH_SS_ee_1j_minus_2018=1,mask_WH_SS_ee_1j_plus_2018=1,mask_WH_SS_em_2j_minus_2018=1,mask_WH_SS_em_2j_plus_2018=1,mask_WH_SS_mm_2j_minus_2018=1,mask_WH_SS_mm_2j_plus_2018=1,mask_WH_SS_ee_2j_minus_2018=1,mask_WH_SS_ee_2j_plus_2018=1,mask_WH_SS_WZ_1j_2018=1,mask_WH_SS_WZ_2j_2018=1

WHSS_2018_LOW_PT=mask_WH_SS_em_1j_minus_low_pt_2018=1,mask_WH_SS_em_1j_plus_low_pt_2018=1,mask_WH_SS_mm_1j_minus_low_pt_2018=1,mask_WH_SS_mm_1j_plus_low_pt_2018=1,mask_WH_SS_ee_1j_minus_low_pt_2018=1,mask_WH_SS_ee_1j_plus_low_pt_2018=1,mask_WH_SS_em_2j_minus_low_pt_2018=1,mask_WH_SS_em_2j_plus_low_pt_2018=1,mask_WH_SS_mm_2j_minus_low_pt_2018=1,mask_WH_SS_mm_2j_plus_low_pt_2018=1,mask_WH_SS_ee_2j_minus_low_pt_2018=1,mask_WH_SS_ee_2j_plus_low_pt_2018=1

WH3l_2018=mask_WH_3l_sssf_plus_2018=1,mask_WH_3l_sssf_minus_2018=1,mask_WH_3l_ossf_plus_2018=1,mask_WH_3l_ossf_minus_2018=1,mask_WH_3l_WZ_CR_0j_2018=1


WHSS_2017_HIGH_PT=mask_WH_SS_em_1j_minus_2017=1,mask_WH_SS_em_1j_plus_2017=1,mask_WH_SS_mm_1j_minus_2017=1,mask_WH_SS_mm_1j_plus_2017=1,mask_WH_SS_ee_1j_minus_2017=1,mask_WH_SS_ee_1j_plus_2017=1,mask_WH_SS_em_2j_minus_2017=1,mask_WH_SS_em_2j_plus_2017=1,mask_WH_SS_mm_2j_minus_2017=1,mask_WH_SS_mm_2j_plus_2017=1,mask_WH_SS_ee_2j_minus_2017=1,mask_WH_SS_ee_2j_plus_2017=1,mask_WH_SS_WZ_1j_2017=1,mask_WH_SS_WZ_2j_2017=1

WHSS_2017_LOW_PT=mask_WH_SS_em_1j_minus_low_pt_2017=1,mask_WH_SS_em_1j_plus_low_pt_2017=1,mask_WH_SS_mm_1j_minus_low_pt_2017=1,mask_WH_SS_mm_1j_plus_low_pt_2017=1,mask_WH_SS_ee_1j_minus_low_pt_2017=1,mask_WH_SS_ee_1j_plus_low_pt_2017=1,mask_WH_SS_em_2j_minus_low_pt_2017=1,mask_WH_SS_em_2j_plus_low_pt_2017=1,mask_WH_SS=1

WH3l_2017=mask_WH_3l_sssf_plus_2017=1,mask_WH_3l_sssf_minus_2017=1,mask_WH_3l_ossf_plus_2017=1,mask_WH_3l_ossf_minus_2017=1,mask_WH_3l_WZ_CR_0j_2017=1


WHSS_2016noHIPM_HIGH_PT=mask_WH_SS_em_1j_minus_2016noHIPM=1,mask_WH_SS_em_1j_plus_2016noHIPM=1,mask_WH_SS_mm_1j_minus_2016noHIPM=1,mask_WH_SS_mm_1j_plus_2016noHIPM=1,mask_WH_SS_ee_1j_minus_2016noHIPM=1,mask_WH_SS_ee_1j_plus_2016noHIPM=1,mask_WH_SS_em_2j_minus_2016noHIPM=1,mask_WH_SS_em_2j_plus_2016noHIPM=1,mask_WH_SS_mm_2j_minus_2016noHIPM=1,mask_WH_SS_mm_2j_plus_2016noHIPM=1,mask_WH_SS_ee_2j_minus_2016noHIPM=1,mask_WH_SS_ee_2j_plus_2016noHIPM=1,mask_WH_SS_WZ_1j_2016noHIPM=1,mask_WH_SS_WZ_2j_2016noHIPM=1

WHSS_2016noHIPM_LOW_PT=mask_WH_SS_em_1j_minus_low_pt_2016noHIPM=1,mask_WH_SS_em_1j_plus_low_pt_2016noHIPM=1,mask_WH_SS_mm_1j_minus_low_pt_2016noHIPM=1,mask_WH_SS_mm_1j_plus_low_pt_2016noHIPM=1,mask_WH_SS_ee_1j_minus_low_pt_2016noHIPM=1,mask_WH_SS_ee_1j_plus_low_pt_2016noHIPM=1,mask_WH_SS_em_2j_minus_low_pt_2016noHIPM=1,mask_WH_SS_em_2j_plus_low_pt_2016noHIPM=1,mask_WH_SS_mm_2j_minus_low_pt_2016noHIPM=1,mask_WH_SS_mm_2j_plus_low_pt_2016noHIPM=1,mask_WH_SS_ee_2j_minus_low_pt_2016noHIPM=1,mask_WH_SS_ee_2j_plus_low_pt_2016noHIPM=1

WH3l_2016noHIPM=mask_WH_3l_sssf_plus_2016noHIPM=1,mask_WH_3l_sssf_minus_2016noHIPM=1,mask_WH_3l_ossf_plus_2016noHIPM=1,mask_WH_3l_ossf_minus_2016noHIPM=1,mask_WH_3l_WZ_CR_0j_2016noHIPM=1


WHSS_2016HIPM_HIGH_PT=mask_WH_SS_em_1j_minus_2016HIPM=1,mask_WH_SS_em_1j_plus_2016HIPM=1,mask_WH_SS_mm_1j_minus_2016HIPM=1,mask_WH_SS_mm_1j_plus_2016HIPM=1,mask_WH_SS_ee_1j_minus_2016HIPM=1,mask_WH_SS_ee_1j_plus_2016HIPM=1,mask_WH_SS_em_2j_minus_2016HIPM=1,mask_WH_SS_em_2j_plus_2016HIPM=1,mask_WH_SS_mm_2j_minus_2016HIPM=1,mask_WH_SS_mm_2j_plus_2016HIPM=1,mask_WH_SS_ee_2j_minus_2016HIPM=1,mask_WH_SS_ee_2j_plus_2016HIPM=1,mask_WH_SS_WZ_1j_2016HIPM=1,mask_WH_SS_WZ_2j_2016HIPM=1

WHSS_2016HIPM_LOW_PT=mask_WH_SS_em_1j_minus_low_pt_2016HIPM=1,mask_WH_SS_em_1j_plus_low_pt_2016HIPM=1,mask_WH_SS_mm_1j_minus_low_pt_2016HIPM=1,mask_WH_SS_mm_1j_plus_low_pt_2016HIPM=1,mask_WH_SS_ee_1j_minus_low_pt_2016HIPM=1,mask_WH_SS_ee_1j_plus_low_pt_2016HIPM=1,mask_WH_SS_em_2j_minus_low_pt_2016HIPM=1,mask_WH_SS_em_2j_plus_low_pt_2016HIPM=1,mask_WH_SS_mm_2j_minus_low_pt_2016HIPM=1,mask_WH_SS_mm_2j_plus_low_pt_2016HIPM=1,mask_WH_SS_ee_2j_minus_low_pt_2016HIPM=1,mask_WH_SS_ee_2j_plus_low_pt_2016HIPM=1

WH3l_2016HIPM=mask_WH_3l_sssf_plus_2016HIPM=1,mask_WH_3l_sssf_minus_2016HIPM=1,mask_WH_3l_ossf_plus_2016HIPM=1,mask_WH_3l_ossf_minus_2016HIPM=1,mask_WH_3l_WZ_CR_0j_2016HIPM=1


### Create directory and move into it:
mkdir -p Impact_unblind/

cd Impact_unblind/


# Plot (after all the jobs are done)
if [ $PLOT == True ]; then

	combineTool.py -M Impacts -d ${WORKSPACE} -m 125 -o ${NAME}.json --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs -n ${FINAL_STATE}

	plotImpacts.py -i ${NAME}.json -o ${NAME} --blind

else

	# Produce initial fit and fits for each nuisance:
	if [ $FINAL_STATE == FullRun2 ]; then

		combineTool.py -M Impacts -d ${WORKSPACE} -m 125 --doInitialFit --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminDefaultMinimizerStrategy 0 --cminFallbackAlgo Minuit2,0:0.2 --stepSize 0.01 --cminPreScan -n ${FINAL_STATE}

		combineTool.py -M Impacts -d ${WORKSPACE} -m 125 --doFits --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --job-mode=condor --freezeParameters r_higgs --sub-opts='+JobFlavour="workday"' --cminDefaultMinimizerStrategy 0 --cminFallbackAlgo Minuit2,0:0.01 --stepSize 0.01 --cminPreScan -n ${FINAL_STATE}
		
		###########
		
		# Full 2018
	elif [ $FINAL_STATE == Full2018 ]; then

		combineTool.py -M Impacts -d ${WORKSPACE} -m 125 --doInitialFit --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminDefaultMinimizerStrategy 0 --cminFallbackAlgo Minuit2,0:0.2 --stepSize 0.01 --cminPreScan -n ${FINAL_STATE} --setParametersForFit ${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}

		combineTool.py -M Impacts -d ${WORKSPACE} -m 125 --doFits --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --job-mode=condor --freezeParameters r_higgs --sub-opts='+JobFlavour="workday"' --cminDefaultMinimizerStrategy 0 --cminFallbackAlgo Minuit2,0:0.01 --stepSize 0.01 --cminPreScan -n ${FINAL_STATE} --setParametersForFit ${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}

	else
		echo "I still don't know this final state"
		exit 1
	fi

	cd -

fi
