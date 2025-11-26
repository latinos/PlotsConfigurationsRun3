# Plots used for fake rate: using prescaled triggers
mkShapesRDF -c 1
mkPlot --onlyPlot cratio --showIntegralLegend 1 --fileFormats png

# Plots used for prompt rate: using unprescaled triggers
cd unprescaled_cfg/
mkShapesRDF -c 1
mkPlot --onlyPlot cratio --showIntegralLegend 1 --fileFormats png
cd -
