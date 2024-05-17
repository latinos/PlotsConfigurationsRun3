# Configuration for OSSF signal region

### Plot distributions

Compile configuration and plot distributions:

    mkShapesRDF -c 1

    mkPlot --onlyPlot cratio --showIntegralLegend 1 --fileFormats png

### Produce datacards

Compile configuration and produce datacards:

    mkShapesRDF -c 1

    mkDatacards --outputDirDatacard ../datacards_original_signal_scale --skipMissingNuisance