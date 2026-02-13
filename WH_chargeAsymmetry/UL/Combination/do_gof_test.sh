#!/bin/bash
if [ $# -lt 3 ];
then
	echo "$0: Missing arguments 'final state':"
	echo ""
	echo "bash do_gof_test.sh FullRun2      WH_chargeAsymmetry_WH_FullRun2_v9_high_pt      \$PWD"
	echo "bash do_gof_test.sh FullRun2_WHSS WH_chargeAsymmetry_WH_FullRun2_v9_WHSS_high_pt \$PWD"
	echo "bash do_gof_test.sh FullRun2_WH3l WH_chargeAsymmetry_WH_FullRun2_v9_WH3l         \$PWD"
	echo ""
	echo "bash do_gof_test.sh 2017_2018      WH_chargeAsymmetry_WH_2017_2018_v9_high_pt      \$PWD"
	echo "bash do_gof_test.sh 2017_2018_WHSS WH_chargeAsymmetry_WH_2017_2018_v9_WHSS_high_pt \$PWD"
	echo "bash do_gof_test.sh 2017_2018_WH3l WH_chargeAsymmetry_WH_2017_2018_v9_WH3l         \$PWD"
	echo ""
	echo "bash do_gof_test.sh 2016noHIPM_2017_2018      WH_chargeAsymmetry_WH_2016noHIPM_2017_2018_v9_high_pt      \$PWD"
	echo "bash do_gof_test.sh 2016noHIPM_2017_2018_WHSS WH_chargeAsymmetry_WH_2016noHIPM_2017_2018_v9_WHSS_high_pt \$PWD"
	echo "bash do_gof_test.sh 2016noHIPM_2017_2018_WH3l WH_chargeAsymmetry_WH_2016noHIPM_2017_2018_v9_WH3l         \$PWD"
	echo ""
	echo "bash do_gof_test.sh 2016HIPM_2017_2018      WH_chargeAsymmetry_WH_2016HIPM_2017_2018_v9_high_pt      \$PWD"
	echo "bash do_gof_test.sh 2016HIPM_2017_2018_WHSS WH_chargeAsymmetry_WH_2016HIPM_2017_2018_v9_WHSS_high_pt \$PWD"
	echo "bash do_gof_test.sh 2016HIPM_2017_2018_WH3l WH_chargeAsymmetry_WH_2016HIPM_2017_2018_v9_WH3l         \$PWD"
	echo ""
	echo "bash do_gof_test.sh Full2016      WH_chargeAsymmetry_WH_Full2016_v9_high_pt      \$PWD"
	echo "bash do_gof_test.sh Full2016_WHSS WH_chargeAsymmetry_WH_Full2016_v9_WHSS_high_pt \$PWD"
	echo "bash do_gof_test.sh Full2016_WH3l WH_chargeAsymmetry_WH_Full2016_v9_WH3l         \$PWD"
	echo ""
	echo "bash do_gof_test.sh Full2018      WH_chargeAsymmetry_WH_Full2018_v9_high_pt      \$PWD"
	echo "bash do_gof_test.sh Full2018_WHSS WH_chargeAsymmetry_WH_Full2018_v9_WHSS_high_pt \$PWD"
	echo "bash do_gof_test.sh Full2018_WH3l WH_chargeAsymmetry_WH_Full2018_v9_WH3l         \$PWD"
	echo ""
	echo "bash do_gof_test.sh Full2017      WH_chargeAsymmetry_WH_Full2017_v9_high_pt      \$PWD"
	echo "bash do_gof_test.sh Full2017_WHSS WH_chargeAsymmetry_WH_Full2017_v9_WHSS_high_pt \$PWD"
	echo "bash do_gof_test.sh Full2017_WH3l WH_chargeAsymmetry_WH_Full2017_v9_WH3l         \$PWD"
	echo ""
	echo "bash do_gof_test.sh 2016noHIPM      WH_chargeAsymmetry_WH_2016noHIPM_v9_high_pt      \$PWD"
	echo "bash do_gof_test.sh 2016noHIPM_WHSS WH_chargeAsymmetry_WH_2016noHIPM_v9_WHSS_high_pt \$PWD"
	echo "bash do_gof_test.sh 2016noHIPM_WH3l WH_chargeAsymmetry_WH_2016noHIPM_v9_WH3l         \$PWD"
	echo ""
	echo "bash do_gof_test.sh 2016HIPM      WH_chargeAsymmetry_WH_2016HIPM_v9_high_pt      \$PWD"
	echo "bash do_gof_test.sh 2016HIPM_WHSS WH_chargeAsymmetry_WH_2016HIPM_v9_WHSS_high_pt \$PWD"
	echo "bash do_gof_test.sh 2016HIPM_WH3l WH_chargeAsymmetry_WH_2016HIPM_v9_WH3l         \$PWD"
	echo ""
  exit 1
else
  echo "We got some argument(s)"
  echo "============================="
  echo "Number of arguments      : $#"
  echo "List of arguments        : $@"
  echo "Arg #1: Final State      : $1"
  echo "Arg #2: Datacard         : $2"
  echo "Arg #3: Output directory : $3"
  echo "Arg #4: Variable         : $4"
  echo "Arg #5: POIs             : $5"
  echo "============================="
  FINAL_STATE=$1
  DATACARD=$2
  DIR=$3
  VARIABLE=binning
  if [ $# -eq 4 ]; then
	 VARIABLE=$4
  fi
  POIS=strength
  if [ $# -eq 5 ]; then
	 POIS=$4
  fi
fi

echo "                               "
echo "After processing:              "
echo "==============================="
echo "Final State      : $FINAL_STATE"
echo "Datacard         : $DATACARD   "
echo "Output directory : $DIR        "
echo "Variable         : $VARIABLE   "
echo "POIs             : $POIS       "
echo "==============================="


# Setting up environment
cd $HOME/work/combine/CMSSW_14_1_0_pre4/src/
eval `scramv1 ru -sh`
cd -
ulimit -s unlimited
alias python=python3

OPTMIZER_OPTIONS='--cminDefaultMinimizerTolerance 0.01 --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0'

# Fit case:
POI='--setParameters r_WH=1,r_higgs=1 --setParameterRanges r_WH=-10,10 --redefineSignalPOIs r_WH --freezeParameters r_higgs'
if [ $POIS == WH_plus_minus ]; then
	POI='--setParameters r_WH_plus=1,r_WH_minus=1 --setParameterRanges r_WH_plus=-10,10:r_WH_minus=-10,10 --redefineSignalPOIs r_WH_plus,r_WH_minus'
	FINAL_STATE=${FINAL_STATE}_plus_minus
fi

echo "--------------------------------------"
echo "Input parameters:"
echo "Final state:       " $FINAL_STATE
echo "POI setup:         " $POI
echo "Optimizer options: " $OPTMIZER_OPTIONS
echo "--------------------------------------"

### Prepare workspace from datacard
echo "Preparing workspace ..."

text2workspace.py \
Combination/${DATACARD}_${VARIABLE}.txt \
-o Combination/${DATACARD}_${VARIABLE}_WH_strength.root \
-P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
-m 125 \
--PO verbose \
--PO 'map=.*/ggH_hww:r_higgs[1,0.99,1.01]' \
--PO 'map=.*/qqH_hww:r_higgs[1,0.99,1.01]' \
--PO 'map=.*/ZH_hww:r_higgs[1,0.99,1.01]' \
--PO 'map=.*/ggZH_hww:r_higgs[1,0.99,1.01]' \
--PO 'map=.*/ttH_hww:r_higgs[1,0.99,1.01]' \
--PO 'map=.*/ggH_htt:r_higgs[1,0.99,1.01]' \
--PO 'map=.*/qqH_htt:r_higgs[1,0.99,1.01]' \
--PO 'map=.*/ZH_htt:r_higgs[1,0.99,1.01]' \
--PO 'map=.*/WH_h.*_plus:r_WH[1,-10.0,10.0]' \
--PO 'map=.*/WH_h.*_minus:r_WH[1,-10.0,10.0]'

echo "Workspace done!"

# Redefine DATACARD variable for the rest of the script
DATACARD=${DIR}/Combination/${DATACARD}_${VARIABLE}_WH_strength.root

### Create directories:
mkdir -p GoF
mkdir -p GoF_${FINAL_STATE}_${VARIABLE}

cp /afs/cern.ch/user/n/ntrevisa/public/utils/index.php GoF/

### Fit on data and 200 toys and then plotting
cd GoF_${FINAL_STATE}_${VARIABLE}

echo "Performing fit on data..."

combineTool.py -M GoodnessOfFit ${DATACARD} --algo=saturated ${POI} ${OPTMIZER_OPTIONS} -n _${FINAL_STATE}

echo "Done!"

echo "Performing fit on 1000 toys..."

combineTool.py -M GoodnessOfFit ${DATACARD} --algo=saturated -t 1 -s 0:199:1 --dry-run --job-mode=condor --sub-opts='+JobFlavour="workday"' ${POI} ${OPTMIZER_OPTIONS} -n $FINAL_STATE

# Modify the sh file in order to submit 200 jobs running 5 toys each
sed -i 's/-t 1/-t 5/g' condor_combine_task.sh

# Finally, submit jobs to condor
condor_submit condor_combine_task.sub

echo "Jobs submitted!"

# Check jobs
while true; do

	condor_q
	
	n_done=$(ls combine_task.*.out | wc -l)
	
	echo "Jobs done: $n_done / 200"

    if [[ "$n_done" -eq 200 ]]; then

		echo "All jobs done!"

		break

	fi

	sleep 10

done
	
echo "Done!"

echo "Preparing and plotting results..."

sleep 30

# Hadd output files from 100 jobs
hadd -f higgsCombine${FINAL_STATE}.GoodnessOfFit.mH120.toys.root higgsCombine${FINAL_STATE}.GoodnessOfFit.mH120.*.root

# Prepare json file
combineTool.py -M CollectGoodnessOfFit --input higgsCombine_${FINAL_STATE}.GoodnessOfFit.mH120.root higgsCombine${FINAL_STATE}.GoodnessOfFit.mH120.toys.root -m 120.0 -o ../GoF/GoF_${FINAL_STATE}_${VARIABLE}.json

# Plot results
plotGof.py ../GoF/GoF_${FINAL_STATE}_${VARIABLE}.json --statistic saturated --mass 120.0 -o ../GoF/GoF_${FINAL_STATE}_${VARIABLE} --title-right=${FINAL_STATE}_${VARIABLE}

echo "Done!"

cd ../

echo "Removing intermediate results..."

rm -rf GoF_${FINAL_STATE}_${VARIABLE}/

echo "All done!"
