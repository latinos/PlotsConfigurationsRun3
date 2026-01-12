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

cp ~/index.php plots_WH3l_2016HIPM_v9_chargeAsymmetry_Mu82_EleUL90/

if [ "$DATE" != "" ]; then
	echo "Copying plots to the web ..."
	mkdir -p /eos/user/n/ntrevisa/www/plots/${DATE}/2016HIPM/
	cp ~/index.php /eos/user/n/ntrevisa/www/plots/${DATE}/
	cp ~/index.php /eos/user/n/ntrevisa/www/plots/${DATE}/2016HIPM/
	cp -r plots_WH3l_2016HIPM_v9_chargeAsymmetry_Mu82_EleUL90/ /eos/user/n/ntrevisa/www/plots/${DATE}/2016HIPM/
	cp /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/WH3l_2016HIPM_v9_chargeAsymmetry_Mu82_EleUL90/rootFile/mkShapes__WH3l_2016HIPM_v9_chargeAsymmetry_Mu82_EleUL90.root /eos/user/n/ntrevisa/www/plots/${DATE}/2016HIPM/
	echo "Done!"
fi
