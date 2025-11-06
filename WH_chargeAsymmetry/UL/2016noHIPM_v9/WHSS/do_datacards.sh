#!/bin/bash

cd configuration_1j
mkShapesRDF -c 1
mkDatacards --outputDirDatacard ../datacards_original_signal_scale --skipMissingNuisance
cd -

cd configuration_1j_mm
mkShapesRDF -c 1
mkDatacards --outputDirDatacard ../datacards_original_signal_scale --skipMissingNuisance
cd -

cd configuration_2j
mkShapesRDF -c 1
mkDatacards --outputDirDatacard ../datacards_original_signal_scale --skipMissingNuisance
cd -

cd configuration_2j_mm
mkShapesRDF -c 1
mkDatacards --outputDirDatacard ../datacards_original_signal_scale --skipMissingNuisance
cd -
