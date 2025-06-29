# PlotsConfigurationsRun3

Plot configuration for Run 3, based on RDF 

### Install

We suggest to install `PlotsConfigurationsRun3` in the same directory where you installed `mkShapesRDF`. Once there, download the configurations using:

    git clone git@github.com:latinos/PlotsConfigurationsRun3.git

### Install Combine

If you use `PlotsConfigurationsRun3`, you will probably need to produce histograms and plots, but also datacards to perform fits. The standard tool is `Combine`. To install it, you can follow the instructions in the [combine home page](https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/latest/#installation-instructions) or follow the instructions here. We suggest to install combine in the directory where you installed `mkShapesRDF` and `PlotsConfigurationsRun3`.

    cmsrel CMSSW_14_1_0_pre4

    cd CMSSW_14_1_0_pre4/src
    
    cmsenv

    git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit

    cd HiggsAnalysis/CombinedLimit

    git fetch origin

    git checkout v10.2.1

    scramv1 b clean; scramv1 b

To use combine, deactivate the `mkShapesRDF` virtual environment, and `cmsenv` into the `CMSSW` directory where you installed combine:

    deactivate

    cd <your_working_directory>/CMSSW_14_1_0_pre4/src/

    cmsenv
