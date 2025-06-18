# W polarization in Higgs to WW

This is the configuration for the analysis which is part of HIG-24-005. Measurement of the double polarization of W pairs in HWW events. Different flavor leptonic decay channel is targeted, in final states with 0, 1, or 2 jets. Both ggF and VBF production modes.

The instructions to run the analysis follow.

### Load the mkShapesRDF environment

Here, we assume `PlotsConfigurationsRun3` was installed in the same directory as `mkShapesRDF`. E.g., let's assume we have a `Run3` directory where we installed both `mkShapesRDF` and `PlotsConfigurationsRun3`.

Then, we can source the `mkShapesRDF` environment using these commands:

    cd ../../../mkShapesRDF/

    source start.sh

    cd -

### Produce distributions using mkShapesMulti.py in batch mode

**Warning: Probably the paths under aliases and configuration needs to be revisited and modified for your username**

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

**Important**

Combine Signal+Background+Interference into single process for ggF and VBF:

    python doCompleteGGF.py

Process the envelope uncertainties to get Up/Down variations:

    python doProcessEnvelope.py

Process tau-embedded veto uncertainties:

    python doVetoUncertainty.py

Get the ggToWW (S+B+I) scale variation uncertainty as a function of the amount of ggWW. Copy the output in nuisances_ALL.py:

    python doGluGluRatios.py


Plot distributions:

    mkPlot ....

Produce datacards. Here, using the correct normalization for the signals:

    mkDatacards

Combine datacards:

    cp combine/HiggsHelicity.py $HOME/work/combine/CMSSW_11_3_4/src/HiggsAnalysis/CombinedLimit/python/

    cp combine/doAnalysis.sh $HOME/work/combine/CMSSW_11_3_4/src/

    cmssw-cc7

    cd $HOME/work/combine/CMSSW_11_3_4/src/;cmsenv;cd -;ulimit -s unlimited

    scram b -j 4

    ./doAnalysis.sh

Fit data to get impacts:

    text2workspace.py datacard_combined.txt -m 125 -P HiggsAnalysis.CombinedLimit.HiggsHelicity:higgshelicity --PO doOnlyPolarization -o datacard_combined.root

    combineTool.py -M Impacts -d datacards/datacard_combined.root -m 125 -t -1 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy=0 --setParameters r_LL=1,r_TT=1 --redefineSignalPOIs r_LL,r_TT --setParameterRanges r_LL=0,4:r_TT=0,4 --doInitialFit

    combineTool.py -M Impacts -d datacards/datacard_combined.root -m 125 -t -1 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy=0 --setParameters r_LL=1,r_TT=1 --redefineSignalPOIs r_LL,r_TT --setParameterRanges r_LL=0,4:r_TT=0,4 --doFits --job-mode=interactive --parallel=10

    combineTool.py -M Impacts -d datacards/datacard_combined.root -m 125 -t -1 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy=0 --setParameters r_LL=1,r_TT=1 --redefineSignalPOIs r_LL,r_TT --setParameterRanges r_LL=0,4:r_TT=0,4 -o impacts.json

    plotImpacts.py -i impacts.json -o impacts --POI r_LL

    plotImpacts.py -i impacts.json -o impacts --POI r_TT

If you want to submit the jobs to HTCondor:

   combineTool.py -M Impacts -d datacard_combined.root -m 125 -t -1 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy=0 --setParameters r_LL=1,r_TT=1 --redefineSignalPOIs r_LL,r_TT --setParameterRanges r_LL=0,4:r_TT=0,4 --doInitialFit

    combineTool.py -M Impacts -d datacard_combined.root -m 125 -t -1 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy=0 --setParameters r_LL=1,r_TT=1 --redefineSignalPOIs r_LL,r_TT --setParameterRanges r_LL=0,4:r_TT=0,4 --doFits --job-mode=condor --parallel=1

    combineTool.py -M Impacts -d datacard_combined.root -m 125 -t -1 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy=0 --setParameters r_LL=1,r_TT=1 --redefineSignalPOIs r_LL,r_TT --setParameterRanges r_LL=0,4:r_TT=0,4 -o impacts.json

    plotImpacts.py -i impacts.json -o impacts --POI r_LL

    plotImpacts.py -i impacts.json -o impacts --POI r_TT

Generate 2D likelihood scans:

    combine -M MultiDimFit --algo grid --points 1000 --setParameters r_LL=1,r_TT=1 --redefineSignalPOIs r_LL,r_TT --setParameterRanges r_LL=0,4:r_TT=0,4 -t -1 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy=0 --verbose 1 -d datacards_HWW_2018/datacard_combined.root -m 125

    or

    combine -M MultiDimFit --algo grid --points 1000 --setParameters r_LL=1,r_TT=1 --redefineSignalPOIs r_LL,r_TT --setParameterRanges r_LL=0,4:r_TT=0,4 -t -1 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy=0 --verbose 1 -d datacards_HWW_2018/datacard_combined.root -m 125 --job-mode=condor --split-points 1


Once you have the likelihhod scans you can run the code in the notebook to produce the plots using the CAT recommended style for figures 




