# WH charge asymmetry analysis

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

Plot distributions:

    mkPlot --onlyPlot cratio --showIntegralLegend 1 --fileFormats png

### Perform goodness of fit test

Create datacards:

    mkDatacards

Produce workspaces:

    mkdir -p GoF

    cd GoF/

    VARIABLE=mjj
    FINAL_STATE=mm_2j_SS_CR_plus
    OUT_NAME=_${FINAL_STATE}_${VARIABLE}

    combineTool.py -M T2W -m 125 \
        -o datacard.root \
	-i ../datacards/hww2l2v_13TeV_WH_SS_${FINAL_STATE}_pt2ge20/${VARIABLE}/datacard.txt \
	--channel-masks \
	-P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
        --PO 'map=.*/WH_h.*_plus:r_WH[1,-10.0,10.0]' \
        --PO 'map=.*/WH_h.*_minus:r_WH[1,-10.0,10.0]'

Perform fit on real data:

    combineTool.py -M GoodnessOfFit ../datacards/hww2l2v_13TeV_WH_SS_${FINAL_STATE}_pt2ge20/${VARIABLE}/datacard.root \
        --algo=saturated \
	--setParameters r_WH=1 \
	--setParameterRanges r_WH=-5,5 \
	--redefineSignalPOIs r_WH \
	-n ${OUT_NAME}

Produce toys based on the predictions:

    combineTool.py -M GoodnessOfFit ../datacards/hww2l2v_13TeV_WH_SS_${FINAL_STATE}_pt2ge20/${VARIABLE}/datacard.root \
        --algo=saturated \
	-t 1 \
	-s 0:10:1 \
	--dry-run \
	--job-mode=condor \
	--setParameters r_WH=1 \
	--setParameterRanges r_WH=-5,5 \
	--redefineSignalPOIs r_WH \
	-n ${OUT_NAME}

Modify the sh file in order to submit 10 jobs running the 100 toys

    sed -i 's/-t 1/-t 10/g' condor_combine_task.sh

If you run on the KIT machines, remember to adapt the submission file to the HTCondor requirements, by adding these lines to the top of `condor_combine_task.sub`:

    text_to_add=$'universe         = container\ncontainer_image  = /cvmfs/unpacked.cern.ch/registry.hub.docker.com/cverstege/alma9-gridjob:latest'

    printf "%s\n" "$text_to_add" | cat - condor_combine_task.sub > temp && mv temp condor_combine_task.sub

Submit the jobs to condor

    condor_submit condor_combine_task.sub

Once all jobs are done, merge the output and plot the results:

    hadd -f higgsCombine_${OUT_NAME}.GoodnessOfFit.mH120.toys.root higgsCombine${OUT_NAME}.GoodnessOfFit.mH120.*.root

    combineTool.py -M CollectGoodnessOfFit --input higgsCombine${OUT_NAME}.GoodnessOfFit.mH120.root higgsCombine_${OUT_NAME}.GoodnessOfFit.mH120.toys.root -m 125 -o GoF_${OUT_NAME}.json
	
    plotGof.py GoF_${OUT_NAME}.json --statistic saturated --mass 120.0 -o GoF_${OUT_NAME} --title-right=${OUT_NAME} --range 0 200

Clean the mess:

    rm combine*
    rm condor*
    rm higgsCombine*
