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


### Prepare list of channels
WHSS_2018_HIGH_PT=mask_WH_SS_em_1j_minus_2018=1,mask_WH_SS_em_1j_plus_2018=1,mask_WH_SS_mm_1j_minus_2018=1,mask_WH_SS_mm_1j_plus_2018=1,mask_WH_SS_ee_1j_minus_2018=1,mask_WH_SS_ee_1j_plus_2018=1,mask_WH_SS_em_2j_minus_2018=1,mask_WH_SS_em_2j_plus_2018=1,mask_WH_SS_mm_2j_minus_2018=1,mask_WH_SS_mm_2j_plus_2018=1,mask_WH_SS_ee_2j_minus_2018=1,mask_WH_SS_ee_2j_plus_2018=1,mask_WH_SS_WZ_1j_2018=1,mask_WH_SS_WZ_2j_2018=1

WHSS_2018_EE_HIGH_PT=mask_WH_SS_ee_1j_minus_2018=1,mask_WH_SS_ee_1j_plus_2018=1,mask_WH_SS_ee_2j_minus_2018=1,mask_WH_SS_ee_2j_plus_2018=1

WHSS_2018_LOW_PT=mask_WH_SS_em_1j_minus_low_pt_2018=1,mask_WH_SS_em_1j_plus_low_pt_2018=1,mask_WH_SS_mm_1j_minus_low_pt_2018=1,mask_WH_SS_mm_1j_plus_low_pt_2018=1,mask_WH_SS_ee_1j_minus_low_pt_2018=1,mask_WH_SS_ee_1j_plus_low_pt_2018=1,mask_WH_SS_em_2j_minus_low_pt_2018=1,mask_WH_SS_em_2j_plus_low_pt_2018=1,mask_WH_SS_mm_2j_minus_low_pt_2018=1,mask_WH_SS_mm_2j_plus_low_pt_2018=1,mask_WH_SS_ee_2j_minus_low_pt_2018=1,mask_WH_SS_ee_2j_plus_low_pt_2018=1

WH3l_2018=mask_WH_3l_sssf_plus_2018=1,mask_WH_3l_sssf_minus_2018=1,mask_WH_3l_ossf_plus_2018=1,mask_WH_3l_ossf_minus_2018=1,mask_WH_3l_WZ_CR_0j_2018=1


WHSS_2017_HIGH_PT=mask_WH_SS_em_1j_minus_2017=1,mask_WH_SS_em_1j_plus_2017=1,mask_WH_SS_mm_1j_minus_2017=1,mask_WH_SS_mm_1j_plus_2017=1,mask_WH_SS_ee_1j_minus_2017=1,mask_WH_SS_ee_1j_plus_2017=1,mask_WH_SS_em_2j_minus_2017=1,mask_WH_SS_em_2j_plus_2017=1,mask_WH_SS_mm_2j_minus_2017=1,mask_WH_SS_mm_2j_plus_2017=1,mask_WH_SS_ee_2j_minus_2017=1,mask_WH_SS_ee_2j_plus_2017=1,mask_WH_SS_WZ_1j_2017=1,mask_WH_SS_WZ_2j_2017=1

WHSS_2017_EE_HIGH_PT=mask_WH_SS_ee_1j_minus_2017=1,mask_WH_SS_ee_1j_plus_2017=1,mask_WH_SS_ee_2j_minus_2017=1,mask_WH_SS_ee_2j_plus_2017=1

WHSS_2017_LOW_PT=mask_WH_SS_em_1j_minus_low_pt_2017=1,mask_WH_SS_em_1j_plus_low_pt_2017=1,mask_WH_SS_mm_1j_minus_low_pt_2017=1,mask_WH_SS_mm_1j_plus_low_pt_2017=1,mask_WH_SS_ee_1j_minus_low_pt_2017=1,mask_WH_SS_ee_1j_plus_low_pt_2017=1,mask_WH_SS_em_2j_minus_low_pt_2017=1,mask_WH_SS_em_2j_plus_low_pt_2017=1,mask_WH_SS=1

WH3l_2017=mask_WH_3l_sssf_plus_2017=1,mask_WH_3l_sssf_minus_2017=1,mask_WH_3l_ossf_plus_2017=1,mask_WH_3l_ossf_minus_2017=1,mask_WH_3l_WZ_CR_0j_2017=1


WHSS_2016noHIPM_HIGH_PT=mask_WH_SS_em_1j_minus_2016noHIPM=1,mask_WH_SS_em_1j_plus_2016noHIPM=1,mask_WH_SS_mm_1j_minus_2016noHIPM=1,mask_WH_SS_mm_1j_plus_2016noHIPM=1,mask_WH_SS_ee_1j_minus_2016noHIPM=1,mask_WH_SS_ee_1j_plus_2016noHIPM=1,mask_WH_SS_em_2j_minus_2016noHIPM=1,mask_WH_SS_em_2j_plus_2016noHIPM=1,mask_WH_SS_mm_2j_minus_2016noHIPM=1,mask_WH_SS_mm_2j_plus_2016noHIPM=1,mask_WH_SS_ee_2j_minus_2016noHIPM=1,mask_WH_SS_ee_2j_plus_2016noHIPM=1,mask_WH_SS_WZ_1j_2016noHIPM=1,mask_WH_SS_WZ_2j_2016noHIPM=1

WHSS_2016noHIPM_EE_HIGH_PT=mask_WH_SS_ee_1j_minus_2016noHIPM=1,mask_WH_SS_ee_1j_plus_2016noHIPM=1,mask_WH_SS_ee_2j_minus_2016noHIPM=1,mask_WH_SS_ee_2j_plus_2016noHIPM=1

WHSS_2016noHIPM_LOW_PT=mask_WH_SS_em_1j_minus_low_pt_2016noHIPM=1,mask_WH_SS_em_1j_plus_low_pt_2016noHIPM=1,mask_WH_SS_mm_1j_minus_low_pt_2016noHIPM=1,mask_WH_SS_mm_1j_plus_low_pt_2016noHIPM=1,mask_WH_SS_ee_1j_minus_low_pt_2016noHIPM=1,mask_WH_SS_ee_1j_plus_low_pt_2016noHIPM=1,mask_WH_SS_em_2j_minus_low_pt_2016noHIPM=1,mask_WH_SS_em_2j_plus_low_pt_2016noHIPM=1,mask_WH_SS_mm_2j_minus_low_pt_2016noHIPM=1,mask_WH_SS_mm_2j_plus_low_pt_2016noHIPM=1,mask_WH_SS_ee_2j_minus_low_pt_2016noHIPM=1,mask_WH_SS_ee_2j_plus_low_pt_2016noHIPM=1

WH3l_2016noHIPM=mask_WH_3l_sssf_plus_2016noHIPM=1,mask_WH_3l_sssf_minus_2016noHIPM=1,mask_WH_3l_ossf_plus_2016noHIPM=1,mask_WH_3l_ossf_minus_2016noHIPM=1,mask_WH_3l_WZ_CR_0j_2016noHIPM=1


WHSS_2016HIPM_HIGH_PT=mask_WH_SS_em_1j_minus_2016HIPM=1,mask_WH_SS_em_1j_plus_2016HIPM=1,mask_WH_SS_mm_1j_minus_2016HIPM=1,mask_WH_SS_mm_1j_plus_2016HIPM=1,mask_WH_SS_ee_1j_minus_2016HIPM=1,mask_WH_SS_ee_1j_plus_2016HIPM=1,mask_WH_SS_em_2j_minus_2016HIPM=1,mask_WH_SS_em_2j_plus_2016HIPM=1,mask_WH_SS_mm_2j_minus_2016HIPM=1,mask_WH_SS_mm_2j_plus_2016HIPM=1,mask_WH_SS_ee_2j_minus_2016HIPM=1,mask_WH_SS_ee_2j_plus_2016HIPM=1,mask_WH_SS_WZ_1j_2016HIPM=1,mask_WH_SS_WZ_2j_2016HIPM=1

WHSS_2016HIPM_EE_HIGH_PT=mask_WH_SS_ee_1j_minus_2016HIPM=1,mask_WH_SS_ee_1j_plus_2016HIPM=1,mask_WH_SS_ee_2j_minus_2016HIPM=1,mask_WH_SS_ee_2j_plus_2016HIPM=1

WHSS_2016HIPM_LOW_PT=mask_WH_SS_em_1j_minus_low_pt_2016HIPM=1,mask_WH_SS_em_1j_plus_low_pt_2016HIPM=1,mask_WH_SS_mm_1j_minus_low_pt_2016HIPM=1,mask_WH_SS_mm_1j_plus_low_pt_2016HIPM=1,mask_WH_SS_ee_1j_minus_low_pt_2016HIPM=1,mask_WH_SS_ee_1j_plus_low_pt_2016HIPM=1,mask_WH_SS_em_2j_minus_low_pt_2016HIPM=1,mask_WH_SS_em_2j_plus_low_pt_2016HIPM=1,mask_WH_SS_mm_2j_minus_low_pt_2016HIPM=1,mask_WH_SS_mm_2j_plus_low_pt_2016HIPM=1,mask_WH_SS_ee_2j_minus_low_pt_2016HIPM=1,mask_WH_SS_ee_2j_plus_low_pt_2016HIPM=1

WH3l_2016HIPM=mask_WH_3l_sssf_plus_2016HIPM=1,mask_WH_3l_sssf_minus_2016HIPM=1,mask_WH_3l_ossf_plus_2016HIPM=1,mask_WH_3l_ossf_minus_2016HIPM=1,mask_WH_3l_WZ_CR_0j_2016HIPM=1


mkdir -p GoF

### Plot (after fit to data and toys are done)
if [ $PLOT == True ]; then
	
	hadd -f GoF/higgsCombine${FINAL_STATE}.GoodnessOfFit.mH120.toys.root GoF/higgsCombine${FINAL_STATE}.GoodnessOfFit.mH120.*.root
	
	combineTool.py -M CollectGoodnessOfFit --input GoF/higgsCombine${FINAL_STATE}.GoodnessOfFit.mH120.root GoF/higgsCombine${FINAL_STATE}.GoodnessOfFit.mH120.toys.root -m 120.0 -o GoF/GoF_${FINAL_STATE}.json
	
	plotGof.py GoF/GoF_${FINAL_STATE}.json --statistic saturated --mass 120.0 -o GoF/GoF_${FINAL_STATE} --title-right=${FINAL_STATE} --range 0 1000
	
	# Clean the mess
	rm GoF/combine*
	rm GoF/condor*
	rm GoF/higgsCombine${FINAL_STATE}.GoodnessOfFit.mH120*.root

else
	
	
	### Create workspace and perform fit
	cd GoF/
	
	# Full Run 2
	if [ $FINAL_STATE == FullRun2 ]; then
		
		echo "FullRun2"

		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n FullRun2
		
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated -t 1 -s 0:100:1 --dry-run --job-mode=condor --sub-opts='+JobFlavour="workday"' --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n FullRun2


	# Full Run 2: use WH3l channel and for WHSS channel only high pT mm and em
	elif [ $FINAL_STATE == FullRun2_mm_em_no_low_pt ]; then

		echo "FullRun2_mm_em_no_low_pt"
		
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n FullRun2_mm_em_no_low_pt --setParametersForFit ${WHSS_2018_LOW_PT},${WHSS_2017_LOW_PT},${WHSS_2016noHIPM_LOW_PT},${WHSS_2016HIPM_LOW_PT},${WHSS_2018_EE_HIGH_PT},${WHSS_2017_EE_HIGH_PT},${WHSS_2016noHIPM_EE_HIGH_PT},${WHSS_2016HIPM_EE_HIGH_PT}
		
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated -t 1 -s 0:100:1 --dry-run --job-mode=condor --sub-opts='+JobFlavour="workday"' --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n FullRun2_mm_em_no_low_pt --setParametersForFit ${WHSS_2018_LOW_PT},${WHSS_2017_LOW_PT},${WHSS_2016noHIPM_LOW_PT},${WHSS_2016HIPM_LOW_PT},${WHSS_2018_EE_HIGH_PT},${WHSS_2017_EE_HIGH_PT},${WHSS_2016noHIPM_EE_HIGH_PT},${WHSS_2016HIPM_EE_HIGH_PT}
		
		
		###########
		
		# Full 2018
	elif [ $FINAL_STATE == Full2018 ]; then
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n Full2018 --setParametersForFit ${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
		
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated -t 1 -s 0:100:1 --dry-run --job-mode=condor --sub-opts='+JobFlavour="workday"' --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n Full2018 --setParametersForFit ${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
		
		# Full 2018 no low pT
	elif [ $FINAL_STATE == Full2018_no_low_pt ]; then
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n Full2018_no_low_pt --setParametersForFit ${WHSS_2018_LOW_PT},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}

		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated -t 1 -s 0:100:1 --dry-run --job-mode=condor --sub-opts='+JobFlavour="workday"' --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n Full2018_no_low_pt --setParametersForFit ${WHSS_2018_LOW_PT},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
		
		# Full 2018 WHSS
	elif [ $FINAL_STATE == Full2018_WHSS ]; then
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n Full2018_WHSS --setParametersForFit ${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
		
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated -t 1 -s 0:100:1 --dry-run --job-mode=condor --sub-opts='+JobFlavour="workday"' --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n Full2018_WHSS --setParametersForFit ${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
		
		# Full 2018 WHSS no low pT
	elif [ $FINAL_STATE == Full2018_WHSS_no_low_pt ]; then
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n Full2018_WHSS_no_low_pt --setParametersForFit ${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
		
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated -t 1 -s 0:100:1 --dry-run --job-mode=condor --sub-opts='+JobFlavour="workday"' --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n Full2018_WHSS_no_low_pt --setParametersForFit ${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
		
		
		# Full 2018 WH3l
	elif [ $FINAL_STATE == Full2018_WH3l ]; then
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n Full2018_WH3l --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
		
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated -t 1 -s 0:100:1 --dry-run --job-mode=condor --sub-opts='+JobFlavour="workday"' --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n Full2018_WH3l --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
		
		###########

		# Full 2017
	elif [ $FINAL_STATE == Full2017 ]; then
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n Full2017 --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
		
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated -t 1 -s 0:100:1 --dry-run --job-mode=condor --sub-opts='+JobFlavour="workday"' --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n Full2017 --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
		
		# Full 2017 no low pT
	elif [ $FINAL_STATE == Full2017_no_low_pt ]; then
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n Full2017_no_low_pt --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_LOW_PT},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
		
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated -t 1 -s 0:100:1 --dry-run --job-mode=condor --sub-opts='+JobFlavour="workday"' --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n Full2017_no_low_pt --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_LOW_PT},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
		
		# Full 2017 WHSS
	elif [ $FINAL_STATE == Full2017_WHSS ]; then
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n Full2017_WHSS --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
		
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated -t 1 -s 0:100:1 --dry-run --job-mode=condor --sub-opts='+JobFlavour="workday"' --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n Full2017_WHSS --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
		
		# Full 2017 WHSS no low pT
	elif [ $FINAL_STATE == Full2017_WHSS_no_low_pt ]; then
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n Full2017_WHSS_no_low_pt --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
		
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated -t 1 -s 0:100:1 --dry-run --job-mode=condor --sub-opts='+JobFlavour="workday"' --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n Full2017_WHSS_no_low_pt --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
		
		# Full 2017 WH3l
	elif [ $FINAL_STATE == Full2017_WH3l ]; then
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n Full2017_WH3l --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
		
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated -t 1 -s 0:100:1 --dry-run --job-mode=condor --sub-opts='+JobFlavour="workday"' --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n Full2017_WH3l --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
		
		###########
		
		# 2016 no HIPM
	elif [ $FINAL_STATE == 2016noHIPM ]; then
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n 2016noHIPM --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}

		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated -t 1 -s 0:100:1 --dry-run --job-mode=condor --sub-opts='+JobFlavour="workday"' --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n 2016noHIPM --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
		
		# 2016 no HIPM no low pT
	elif [ $FINAL_STATE == 2016noHIPM_no_low_pt ]; then
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n 2016noHIPM_no_low_pt --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_LOW_PT},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
		
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated -t 1 -s 0:100:1 --dry-run --job-mode=condor --sub-opts='+JobFlavour="workday"' --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n 2016noHIPM_no_low_pt --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_LOW_PT},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
		
		# 2016 no HIPM WHSS
	elif [ $FINAL_STATE == 2016noHIPM_WHSS ]; then
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n 2016noHIPM_WHSS --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
		
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated -t 1 -s 0:100:1 --dry-run --job-mode=condor --sub-opts='+JobFlavour="workday"' --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n 2016noHIPM_WHSS --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
		
		# 2016 no HIPM WHSS no low pT
	elif [ $FINAL_STATE == 2016noHIPM_WHSS_no_low_pt ]; then
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n 2016noHIPM_WHSS_no_low_pt --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
		
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated -t 1 -s 0:100:1 --dry-run --job-mode=condor --sub-opts='+JobFlavour="workday"' --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n 2016noHIPM_WHSS_no_low_pt --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
	
		# 2016 no HIPM WH3l
	elif [ $FINAL_STATE == 2016noHIPM_WH3l ]; then
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n 2016noHIPM_WH3l --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}

		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated -t 1 -s 0:100:1 --dry-run --job-mode=condor --sub-opts='+JobFlavour="workday"' --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n 2016noHIPM_WH3l --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
		
		###########
		
		# 2016 HIPM
	elif [ $FINAL_STATE == 2016HIPM ]; then
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n 2016HIPM --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM}
		
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated -t 1 -s 0:100:1 --dry-run --job-mode=condor --sub-opts='+JobFlavour="workday"' --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n 2016HIPM --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM}
		
		# 2016 HIPM no low pT
	elif [ $FINAL_STATE == 2016HIPM_no_low_pt ]; then
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n 2016HIPM_no_low_pt --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_LOW_PT}
		
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated -t 1 -s 0:100:1 --dry-run --job-mode=condor --sub-opts='+JobFlavour="workday"' --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n 2016HIPM_no_low_pt --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_LOW_PT}
	
		# 2016 HIPM WHSS
	elif [ $FINAL_STATE == 2016HIPM_WHSS ]; then
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n 2016HIPM_WHSS --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WH3l_2016HIPM}

		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated -t 1 -s 0:100:1 --dry-run --job-mode=condor --sub-opts='+JobFlavour="workday"' --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n 2016HIPM_WHSS --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WH3l_2016HIPM}
		
		# 2016 HIPM WHSS no low pT
	elif [ $FINAL_STATE == 2016HIPM_WHSS_no_low_pt ]; then
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n 2016HIPM_WHSS_no_low_pt --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
		
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated -t 1 -s 0:100:1 --dry-run --job-mode=condor --sub-opts='+JobFlavour="workday"' --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n 2016HIPM_WHSS_no_low_pt --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
		
		# 2016 HIPM WH3l
	elif [ $FINAL_STATE == 2016HIPM_WH3l ]; then
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n 2016HIPM_WH3l --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT}
		
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated -t 1 -s 0:100:1 --dry-run --job-mode=condor --sub-opts='+JobFlavour="workday"' --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n 2016HIPM_WH3l --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT}
		
		###########
		
		# no 2018
	elif [ $FINAL_STATE == no_2018 ]; then
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n no_2018 --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018}

		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated -t 1 -s 0:100:1 --dry-run --job-mode=condor --sub-opts='+JobFlavour="workday"' --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n no_2018 --setParametersForFit ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018}
		
		# no 2017
	elif [ $FINAL_STATE == no_2017 ]; then
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n no_2017 --setParametersForFit ${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017}
		
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated -t 1 -s 0:100:1 --dry-run --job-mode=condor --sub-opts='+JobFlavour="workday"' --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n no_2017 --setParametersForFit ${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017}
		
		# no 2016noHIPM
	elif [ $FINAL_STATE == no_2016noHIPM ]; then
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n no_2016noHIPM --setParametersForFit ${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM}
		
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated -t 1 -s 0:100:1 --dry-run --job-mode=condor --sub-opts='+JobFlavour="workday"' --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n no_2016noHIPM --setParametersForFit ${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM}
		
# no 2016HIPM
	elif [ $FINAL_STATE == no_2016noHIPM ]; then
		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n no_2016HIPM --setParametersForFit ${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}

		combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated -t 1 -s 0:100:1 --dry-run --job-mode=condor --sub-opts='+JobFlavour="workday"' --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n no_2016HIPM --setParametersForFit ${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
		
		###########
	
	else
		echo "I still don't know this final state"
		exit 1
	fi

	# Modify the sh file in order to submit 100 jobs running 10 toys each
	sed -i 's/-t 1/-t 10/g' condor_combine_task.sh

	# Finally, submit jobs to condor
	condor_submit condor_combine_task.sub

	cd -

fi
