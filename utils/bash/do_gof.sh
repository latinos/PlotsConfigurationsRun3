#!/bin/bash
if [ $# -eq 0 ];
then
	echo "$0: Please add the target cut and variable and the datacard location. E.g.:"
	echo ""
	echo "bash do_gof.sh hww2l2v_13TeV_WH_SS_em_1j_SS_CR_plus_pt2ge20 mll ~/work/latinos/Run3_WH/PlotsConfigurationsRun3/ControlRegions/SS/Full2018_v9/datacards/"
	echo ""
  exit 1
else
  echo "We got some argument(s)"
  echo "=========================="
  echo "Number of arguments.  : $#"
  echo "List of arguments...  : $@"
  echo "Arg #1: Cut           : $1"
  echo "Arg #2: Variable      : $2"
  echo "Arg #3: Datacards:    : $3"
  echo "=========================="
  CUT=$1
  VARIABLE=$2
  DATACARD=$3
fi

cd $HOME/work/combine/CMSSW_14_1_0_pre4/src/
eval `scramv1 ru -sh`
cd -
ulimit -s unlimited
alias python=python3

### Create directory:
mkdir -p GoF
mkdir -p GoF_${CUT}_${VARIABLE}

cp /afs/cern.ch/user/n/ntrevisa/public/utils/index.php GoF/

### Fit on data and 100 toys
cd GoF_${CUT}_${VARIABLE}

echo "Performing fit on data..."

combineTool.py -M GoodnessOfFit ${DATACARD}/${CUT}/${VARIABLE}/datacard.txt --algo=saturated --setParameters r --setParameterRanges r=-5,5 --cminDefaultMinimizerTolerance 0.01 --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n _${CUT}_${VARIABLE}

echo "Done!"

echo "Performing fit on 100 toys..."

combineTool.py -M GoodnessOfFit ${DATACARD}/${CUT}/${VARIABLE}/datacard.txt --algo=saturated -t 100 --setParameters r --setParameterRanges r=-5,5 --cminDefaultMinimizerTolerance 0.01 --cminPreScan --cminPreFit 2 --cminDefaultMinimizerStrategy 0 -n _${CUT}_${VARIABLE}

echo "Done!"

echo "Preparing and plotting results..."

combineTool.py -M CollectGoodnessOfFit --input higgsCombine_${CUT}_${VARIABLE}.GoodnessOfFit.mH120.root higgsCombine_${CUT}_${VARIABLE}.GoodnessOfFit.mH120.123456.root -m 120.0 -o ../GoF/GoF_${CUT}_${VARIABLE}.json

plotGof.py ../GoF/GoF_${CUT}_${VARIABLE}.json --statistic saturated --mass 120.0 -o ../GoF/GoF_${CUT}_${VARIABLE} --title-right=${CUT}_${VARIABLE} --range 0 100

echo "Done!"

cd ../

echo "Removing intermediate results..."

rm -rf GoF_${CUT}_${VARIABLE}/

echo "All done!"
