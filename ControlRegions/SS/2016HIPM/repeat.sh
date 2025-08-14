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

# Site definition
hostname=$(uname -a | awk '{print $2}')


if [ "$COMPILE" == "True" ]; then
	mkShapesRDF -c 1
	mkShapesRDF -o 0 -f . -b 1 -dR 1
fi
cd condor/SS_2016HIPM_v9/${SAMPLE}/
cp ../../../../../../../mkShapesRDF/mkShapesRDF/include/headers.hh ../../../../../../../mkShapesRDF/mkShapesRDF/shapeAnalysis/runner.py  .
python runner.py

if [[ "$hostname" == *portal* || "$hostname" == *bms* ]]; then
    echo "We are at KIT"
    cp output.root /ceph/${USER}/mkShapesRDF_rootfiles/SS_2016HIPM_v9/rootFile/mkShapes__SS_2016HIPM_v9__ALL__${SAMPLE}.root
else
    echo "We are on lxplus"
    cp output.root /eos/user/${USER:0:1}/${USER}/mkShapesRDF_rootfiles/SS_2016HIPM_v9/rootFile/mkShapes__SS_2016HIPM_v9__ALL__${SAMPLE}.root
fi

rm output.root
