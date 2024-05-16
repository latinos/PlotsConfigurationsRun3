#!/bin/bash

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
