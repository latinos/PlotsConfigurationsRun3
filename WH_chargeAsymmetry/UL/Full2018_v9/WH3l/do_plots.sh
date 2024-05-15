#!/bin/bash

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
