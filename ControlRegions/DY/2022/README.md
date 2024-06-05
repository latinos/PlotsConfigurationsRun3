# DY Control Region

This configuration is used to plot the DY control region looking at 2022 data. In particular, it is used to investigate the observed disagreement between data and simulation in the so-called `horns region`.

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

### Bonus: run jobs interactively

Compile, prepare scripts using a dry-run, and then run interactively one job:

    bash repeat.sh <SAMPLE_FILE-NUMBER> True

E.g.,

    bash repeat.sh DATA_0 True

Just run on pre-existing scripts:

    bash repeat.sh DATA_0