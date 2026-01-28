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

cd configuration_1j
mkShapesRDF -c 1
mkPlot --onlyPlot cratio --showIntegralLegend 1 --fileFormats png
cd -

cd configuration_1j_mm
mkShapesRDF -c 1
mkPlot --onlyPlot cratio --showIntegralLegend 1 --fileFormats png
cd -

cd configuration_2j
mkShapesRDF -c 1
mkPlot --onlyPlot cratio --showIntegralLegend 1 --fileFormats png
cd -

cd configuration_2j_mm
mkShapesRDF -c 1
mkPlot --onlyPlot cratio --showIntegralLegend 1 --fileFormats png
cd -

cp ~/index.php plots_WHSS_2016noHIPM_v9_chargeAsymmetry_Mu82_EleUL90/

if [ "$DATE" != "" ]; then
	echo "Copying plots to the web ..."
	mkdir -p /eos/user/n/ntrevisa/www/plots/${DATE}/2016noHIPM/
	cp ~/index.php /eos/user/n/ntrevisa/www/plots/${DATE}/
	cp ~/index.php /eos/user/n/ntrevisa/www/plots/${DATE}/2016noHIPM/
	cp -r plots_WHSS_2016noHIPM_v9_chargeAsymmetry_Mu82_EleUL90/ /eos/user/n/ntrevisa/www/plots/${DATE}/2016noHIPM/
	cp /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/WHSS_2016noHIPM_v9_chargeAsymmetry_Mu82_EleUL90/rootFile/plots_WHSS_2016noHIPM_v9_chargeAsymmetry_Mu82_EleUL90_DYflip_data.root /eos/user/n/ntrevisa/www/plots/${DATE}/2016noHIPM/
	echo "Done!"
fi
