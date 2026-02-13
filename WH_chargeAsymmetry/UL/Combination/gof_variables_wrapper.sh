#!/bin/bash
if [ $# -lt 1 ];
then
	echo "Please insert the variable to inspect:"
	echo ""
	echo "bash gof_variables_wrapper.sh pt1"
	echo "bash gof_variables_wrapper.sh pt2"
	echo "bash gof_variables_wrapper.sh mll"
	echo ""
	exit 1
else
  VARIABLE=$1
  echo "Variable: ${VARIABLE}"
fi

# Loading combine
cd $HOME/work/combine/CMSSW_14_1_0_pre4/src/
eval `scramv1 ru -sh`
cd -
ulimit -s unlimited
alias python=python3

# Combining datacards
python3 script_combine_datacards_variable.py $VARIABLE

# Testing 2016
bash do_gof_test.sh Full2016        WH_chargeAsymmetry_WH_Full2016_v9_high_pt   $PWD $VARIABLE
bash do_gof_test.sh 2016noHIPM      WH_chargeAsymmetry_WH_2016noHIPM_v9_high_pt $PWD $VARIABLE
bash do_gof_test.sh 2016HIPM        WH_chargeAsymmetry_WH_2016HIPM_v9_high_pt   $PWD $VARIABLE

bash do_gof_test.sh Full2016_WHSS   WH_chargeAsymmetry_WH_Full2016_v9_WHSS_high_pt   $PWD $VARIABLE
bash do_gof_test.sh 2016noHIPM_WHSS WH_chargeAsymmetry_WH_2016noHIPM_v9_WHSS_high_pt $PWD $VARIABLE
bash do_gof_test.sh 2016HIPM_WHSS   WH_chargeAsymmetry_WH_2016HIPM_v9_WHSS_high_pt   $PWD $VARIABLE

bash do_gof_test.sh Full2016_WH3l   WH_chargeAsymmetry_WH_Full2016_v9_WH3l   $PWD $VARIABLE
bash do_gof_test.sh 2016noHIPM_WH3l WH_chargeAsymmetry_WH_2016noHIPM_v9_WH3l $PWD $VARIABLE
bash do_gof_test.sh 2016HIPM_WH3l   WH_chargeAsymmetry_WH_2016HIPM_v9_WH3l   $PWD $VARIABLE
