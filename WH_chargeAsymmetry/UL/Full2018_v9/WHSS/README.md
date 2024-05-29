 charge asymmetry analysis

This is an adaptation of the analysis which is part of HIG-20-013. It is used to measure the asymmetry in the prodution of W+H and W-H. Here, the 2-leptons final state (one of the W bosons decays hadronically) is inspected.

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

Update same-sign histogram file with opposite-sign DY distributions, weighted to take into account charge flip:

    bash do_DYee_estim_data.sh

Plot distributions:

    bash do_plots.sh

Produce datacards. Here, using the correct normalization for the signals:

    bash do_datacards.sh

Combine datacards:

    mkdir -p Combination

    cmssw-cc7

    cd $HOME/work/combine/CMSSW_11_3_4/src/;cmsenv;cd -;ulimit -s unlimited

    python script_datacards_binning_SS_CR.py

Fit data to get results:

    bash do_fit.sh

### Produce impact plots:

Prepare directory:

    mkdir -p Impact_plots

Select datacard to use and actually produce impact plots:

    cd Impact_plots

    combineTool.py -M Impacts -d ../Combination/WH_chargeAsymmetry_WH_SS_Full2018_v9_SS_CR.root -m 125 --doInitialFit -t -1 --setParameters r_S=1.3693,r_A=0.224,r_higgs=1 --setParameterRanges r_S=0,10:r_A=-1,1 --redefineSignalPOIs r_A --freezeParameters r_higgs

    combineTool.py -M Impacts -d ../Combination/WH_chargeAsymmetry_WH_SS_Full2018_v9_SS_CR.root -m 125 --doFits -t -1 --setParameters r_S=1.3693,r_A=0.224,r_higgs=1 --setParameterRanges r_S=0,10:r_A=-1,1 --redefineSignalPOIs r_A --job-mode condor --freezeParameters r_higgs --sub-opts='+JobFlavour="workday"'

From outside the singularity:

    condor_submit condor_combine_task.sub

Back to the singularity:

    combineTool.py -M Impacts -d ../Combination/WH_chargeAsymmetry_WH_SS_Full2018_v9_SS_CR.root -m 125 -t -1 -o impacts_WHSS_Full2018_binning.json --setParameters r_S=1.3693,r_A=0.224,r_higgs=1 --setParameterRanges r_S=0,10:r_A=-1,1 --redefineSignalPOIs r_A

    plotImpacts.py -i impacts_WHSS_Full2018_binning.json -o Impacts_WHSS_Full2018_binning

Remove the intermediate files:

    rm combine_*
    rm condor_*
    rm higgsCombine_*

Copy the plots on the web:

    DATE=2024_05_03

    mkdir -p /eos/user/n/ntrevisa/www/plots/${DATE}/2018/Impacts/

    cp ~/index.php /eos/user/n/ntrevisa/www/plots/${DATE}/2018/Impacts/

    cp impacts_WHSS_Full2018_binning.json Impacts_WHSS_Full2018_binning.pdf /eos/user/n/ntrevisa/www/plots/${DATE}/2018/Impacts/