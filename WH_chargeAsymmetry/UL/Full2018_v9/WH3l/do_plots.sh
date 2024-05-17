#!/bin/bash

if [ $# -eq 0 ]; then
	echo "No arguments passed. Plots will not be copied on webpage"
else
	echo "We got some argument(s)"
	echo "==========================="
	echo "Number of arguments. : $#"
	echo "List of arguments... : $@"
	echo "Arg #1: date         : $1"
	echo "==========================="
	DATE=$1
fi

cd configuration_OSSF
mkShapesRDF -c 1
mkPlot --onlyPlot cratio --showIntegralLegend 1 --fileFormats png
cd -

cd configuration_SSSF
mkShapesRDF -c 1
mkPlot --onlyPlot cratio --showIntegralLegend 1 --fileFormats png
cd -

cd configuration_WZ0j
mkShapesRDF -c 1
mkPlot --onlyPlot cratio --showIntegralLegend 1 --fileFormats png
cd -

cd configuration_WZ1j
mkShapesRDF -c 1
mkPlot --onlyPlot cratio --showIntegralLegend 1 --fileFormats png
cd -

cd configuration_WZ2j
mkShapesRDF -c 1
mkPlot --onlyPlot cratio --showIntegralLegend 1 --fileFormats png
cd -

cp ~/index.php plots_WH3l_2018_v9_chargeAsymmetry_Mu82_EleUL90/

if [ "$DATE" != "" ]; then
	cp -r plots_WH3l_2018_v9_chargeAsymmetry_Mu82_EleUL90/ /eos/user/n/ntrevisa/www/plots/${DATE}/2018/
fi
