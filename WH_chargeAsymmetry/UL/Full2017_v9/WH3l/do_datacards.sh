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
mkDatacards --outputDirDatacard ../datacards_original_signal_scale --skipMissingNuisance
cd -

cd configuration_SSSF
mkShapesRDF -c 1
mkDatacards --outputDirDatacard ../datacards_original_signal_scale --skipMissingNuisance
cd -

cd configuration_WZ0j
mkShapesRDF -c 1
mkDatacards --outputDirDatacard ../datacards_original_signal_scale --skipMissingNuisance
cd -

cd configuration_WZ1j
mkShapesRDF -c 1
mkDatacards --outputDirDatacard ../datacards_original_signal_scale --skipMissingNuisance
cd -

cd configuration_WZ2j
mkShapesRDF -c 1
mkDatacards --outputDirDatacard ../datacards_original_signal_scale --skipMissingNuisance
cd -

if [ "$DATE" != "" ]; then
	echo "Copying datacards to the web ..."
	mkdir -p /eos/user/n/ntrevisa/www/plots/${DATE}/2017/
	cp ~/index.php /eos/user/n/ntrevisa/www/plots/${DATE}/
	cp ~/index.php /eos/user/n/ntrevisa/www/plots/${DATE}/2017/
	cp ~/index.php datacards_original_signal_scale/
	cp -r datacards_original_signal_scale/ /eos/user/n/ntrevisa/www/plots/${DATE}/2017/
	echo "Done!"
fi
