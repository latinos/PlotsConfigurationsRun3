# Same-sign control region

This configuration allows to produce control plots for the two-leptons same-sign and the three-leptons control regions. They are used to check the description of the non-prompt leptons.

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

### Perform goodness of fit test

    python submit_gof.py

When all jobs are done:

    python plot_gof_summary.py
    
    rm -rf GoF_hww2l2v_13TeV_WH_SS_*