#!/bin/bash

if [ $# -eq 0 ]; then
	echo "$0: Missing arguments"
	exit 1
else
	echo "We got some argument(s)"
	echo "==========================="
	echo "Number of arguments. : $#"
	echo "List of arguments... : $@"
	echo "Arg #1: sample       : $1"
	echo "Arg #2: compile      : $2"
	echo "==========================="
	SAMPLE=$1
	COMPILE=$2
fi


if [ "$COMPILE" == "True" ]; then
	mkShapesRDF -c 1
	mkShapesRDF -o 0 -f . -b 1 -dR 1
fi
cd condor/WH3l_2016HIPM_v9_chargeAsymmetry_Mu82_EleUL90/${SAMPLE}/
cp ../../../../../../../../mkShapesRDF/mkShapesRDF/include/headers.hh ../../../../../../../../mkShapesRDF/mkShapesRDF/shapeAnalysis/runner.py  .
python runner.py
cp output.root /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/WH3l_2016HIPM_v9_chargeAsymmetry_Mu82_EleUL90/rootFile/mkShapes__WH3l_2016HIPM_v9_chargeAsymmetry_Mu82_EleUL90__ALL__${SAMPLE}.root
rm output.root
