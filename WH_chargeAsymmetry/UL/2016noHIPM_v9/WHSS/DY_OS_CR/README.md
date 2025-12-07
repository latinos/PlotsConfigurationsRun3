# WH charge asymmetry analysis

This configuration creates data-driven distributions to estimate the DY->ee contamination in the 2lSS signal region. Opposite-sign DY->ee events are selected in MC and weighted for the charge-flip probability, to obtain the expected distributions in the same-sign final state.

The instructions to run the analysis follow.

### Load the mkShapesRDF environment

Here, we assume `PlotsConfigurationsRun3` was installed in the same directory as `mkShapesRDF`. E.g., let's assume we have a `Run3` directory where we installed both `mkShapesRDF` and `PlotsConfigurationsRun3`.

Then, we can source the `mkShapesRDF` environment using these commands:

    cd ../../../mkShapesRDF/

    source start.sh

    cd -

### Produce distributions using mkShapesMulti.py in batch mode

Compile the configuration. Do it after every change to any file in this directory:

    mkShapesRDF -c 1

Produce histograms using batch:

    mkShapesRDF -c 1 -o 0 -f . -b 1

Check jobs status:

    mkShapesRDF -o 1 -f .

Resubmit failed jobs:

    mkShapesRDF -o 1 -f . -r 1		 		

Merge rootfiles:

    mkShapesRDF -o 2 -f .

Plot distributions:

    mkPlot --onlyPlot cratio --showIntegralLegend 1 --fileFormats png