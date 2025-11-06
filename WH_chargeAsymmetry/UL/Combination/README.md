# WH charge asymmetry combination

Here we list the instructions needed to run the WH charge asymmetry analysis combination using Full Run 2 UL samples.


### Set up the environment:

We need to load combine. Since sourcing mkShapesRDF may introduce conflicts, remember not to source the `start.sh`.

	cd $HOME/work/combine/CMSSW_14_1_0_pre4/src/
	cmsenv
	cd -
	ulimit -s unlimited
	alias python=python3


### Combine datacards and fit:

Combine datacards:

	python script_combine_datacards_binning.py

Produce workspace and fit data to get results:

    bash do_fit.sh ${FINAL_STATE}

    bash do_fit_unblind.sh ${FINAL_STATE}

Final state can be, e.g.:

    bash do_fit.sh FullRun2_high_pt

    bash do_fit.sh Full2018_high_pt
    bash do_fit.sh Full2018_WHSS_high_pt
    bash do_fit.sh Full2018_WH3l

    bash do_fit.sh Full2017_high_pt
    bash do_fit.sh Full2017_WHSS_high_pt
    bash do_fit.sh Full2017_WH3l

    bash do_fit.sh 2016noHIPM_high_pt
    bash do_fit.sh 2016noHIPM_WHSS_high_pt
    bash do_fit.sh 2016noHIPM_WH3l

    bash do_fit.sh 2016HIPM_high_pt
    bash do_fit.sh 2016HIPM_WHSS_high_pt
    bash do_fit.sh 2016HIPM_WH3l

And for unblind fit:

    bash do_fit_unblind.sh FullRun2_high_pt

    bash do_fit_unblind.sh Full2018_high_pt
    bash do_fit_unblind.sh Full2018_WHSS_high_pt
    bash do_fit_unblind.sh Full2018_WH3l

    bash do_fit_unblind.sh Full2017_high_pt
    bash do_fit_unblind.sh Full2017_WHSS_high_pt
    bash do_fit_unblind.sh Full2017_WH3l

    bash do_fit_unblind.sh 2016noHIPM_high_pt
    bash do_fit_unblind.sh 2016noHIPM_WHSS_high_pt
    bash do_fit_unblind.sh 2016noHIPM_WH3l

    bash do_fit_unblind.sh 2016HIPM_high_pt
    bash do_fit_unblind.sh 2016HIPM_WHSS_high_pt
    bash do_fit_unblind.sh 2016HIPM_WH3l


### Goodness of Fit Test

Use bash script to run fit on real data and on 1000 toys:

	bash do_gof_test.sh ${FINAL_STATE} False

Final state can be, e.g.:

	FINAL_STATE=FullRun2

Once all jobs are done, use bash script to hadd them and produce the summary histogram:

	bash do_gof_test.sh ${FINAL_STATE} True


### Unblinded Impact Plots

Use bash script to perform initial fit and each fit to evaluate the impact of the individual nuisances:

	bash do_impact_plots.sh ${FINAL_STATE} False

Final state can be, e.g.:

	FINAL_STATE=FullRun2




Create a dedicated directory:

    mkdir -p Impact_unblind
	cd Impact_unblind/

Choose the worksapce and POI:

- Case asymmetry

    WORKSPACE=../Combination/WH_chargeAsymmetry_WH_Full2018_v9_binning.root
	POI=r_A
	PARAMETERS=r_S=1.3693,r_A=0.224,r_higgs=1
	RANGES=r_S=-5,5:r_A=-5,5
	NAME=Impacts_FullRun2_v9_binning

- Case inclusive signal strength:

    WORKSPACE=../Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning_WH_strength.root
	POI=r_WH
	PARAMETERS=r_WH=1,r_higgs=1
	RANGES=r_WH=-5,5
	NAME=Impacts_FullRun2_v9_binning_WH_strength

- Case separate signal strengths:

    WORKSPACE=../Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning_WH_plus_minus.root
	POI=r_WH_plus
	PARAMETERS=r_WH_plus=1,r_WH_minus=1,r_higgs=1
	RANGES=r_WH_plus=-5,5,r_WH_minus=-5,5
	NAME=Impacts_FullRun2_v9_binning_WH_plus_minus

Produce initial fit and fits for each nuisance:

    combineTool.py -M Impacts -d ${WORKSPACE} -m 125 --doInitialFit --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminDefaultMinimizerStrategy 0 --cminFallbackAlgo Minuit2,0:0.2 --stepSize 0.01 --cminPreScan

    combineTool.py -M Impacts -d ${WORKSPACE} -m 125 --doFits --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --job-mode=condor --freezeParameters r_higgs --sub-opts='+JobFlavour="workday"' --cminDefaultMinimizerStrategy 0 --cminFallbackAlgo Minuit2,Simplex,0:0.1 --stepSize 0.01 --cminPreScan

--cminFallbackAlgo Minuit2,0:0.2 --cminFallbackAlgo Minuit2,0:0.4 --X-rtd REMOVE_CONSTANT_ZERO_POINT=1 --robustFit 1

--cminPreFit 2 --cminPreScan

From outside the singularity:

    condor_submit condor_combine_task.sub

Once all the jobs are done:

    combineTool.py -M Impacts -d ${WORKSPACE} -m 125 -o ${NAME}.json --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs

    plotImpacts.py -i ${NAME}.json -o ${NAME} --blind

    rm combine_*
    rm condor_*
    rm higgsCombine_*
	
Copy plots on eos:

    cd ..

    DATE=2024_05_03

    mkdir -p /eos/user/n/ntrevisa/www/plots/${DATE}/FullRun2/Unblinding/
    cp ~/index.php /eos/user/n/ntrevisa/www/plots/${DATE}/FullRun2/Unblinding/
    cp Impact_unblind/impacts_FullRun2_v9_binning.json /eos/user/n/ntrevisa/www/plots/${DATE}/FullRun2/Unblinding/
    cp Impact_unblind/Impact_FullRun2_v9_binning.pdf /eos/user/n/ntrevisa/www/plots/${DATE}/FullRun2/Unblinding/

Addiitonal combine commands:

	--cminDefaultMinimizerStrategy 0
	--robustFit 1
    --freezeParameters allConstrainedNuisances,r_higgs
    --X-rtd FITTER_NEW_CROSSING_ALGO
    --X-rtd FITTER_NEVER_GIVE_UP
    --X-rtd FITTER_BOUND
    --cminFallbackAlgo Minuit2,0:0.2 --cminFallbackAlgo Minuit2,0:0.4 --X-rtd REMOVE_CONSTANT_ZERO_POINT=1


### Produce post-fit plots

    bash do_postfit_plots.sh binning Combination/FitResults_binning_unblind_FD.root 2018
    bash do_postfit_plots.sh binning Combination/FitResults_binning_unblind_FD.root 2017
    bash do_postfit_plots.sh binning Combination/FitResults_binning_unblind_FD.root 2016noHIPM
    bash do_postfit_plots.sh binning Combination/FitResults_binning_unblind_FD.root 2016HIPM



### Old

GoF: Run fit on real data:

	combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreFit 2 --cminPreScan --cminDefaultMinimizerStrategy 0

GoF: Run fit on many MC toys:

	combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated -t 1 -s 0:1000:1  --job-mode=condor --sub-opts='+JobFlavour="workday"' --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreFit 2 --cminPreScan --cminDefaultMinimizerStrategy 0

Run fit on real data:

	combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreFit 2 --cminPreScan --cminDefaultMinimizerStrategy 0

Run fit on many MC toys:

	combineTool.py -M GoodnessOfFit ${WORKSPACE} --algo=saturated -t 1 -s 0:1000:1  --job-mode=condor --sub-opts='+JobFlavour="workday"' --setParameters ${PARAMETERS} --setParameterRanges ${RANGES} --redefineSignalPOIs ${POI} --freezeParameters r_higgs --cminPreFit 2 --cminPreScan --cminDefaultMinimizerStrategy 0

From outside the singularity:

    condor_submit condor_combine_task.sub

Once all the jobs are done:

	hadd higgsCombine.GoF.root higgsCombine.Test.GoodnessOfFit.mH120.*root

Produce plot comparing toys distribution and actual fit:

    cd ..

    python GoF.py

	cp GoF/GoF.pdf GoF/GoF.png /eos/user/n/ntrevisa/www/plots/2024_05_03/FullRun2/Unblinding/

Clean the mess:

    rm GoF/combine*
    rm GoF/condor*
	rm GoF/higgsCombine.Test.GoodnessOfFit.mH120.*.root


### Produce Impact Plots

Prepare directory:

    mkdir -p Impact_plots

Actually produce impact plots:

    cd Impact_plots

Using r_A as POI:

    combineTool.py -M Impacts -d ../Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.root -m 125 --doInitialFit -t -1 --setParameters r_S=1.3693,r_A=0.224,r_higgs=1 --setParameterRanges r_S=0,10:r_A=-1,1 --redefineSignalPOIs r_A --freezeParameters r_higgs

    combineTool.py -M Impacts -d ../Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.root -m 125 --doFits -t -1 --setParameters r_S=1.3693,r_A=0.224,r_higgs=1 --setParameterRanges r_S=0,10:r_A=-1,1 --redefineSignalPOIs r_A --job-mode=condor --freezeParameters r_higgs --sub-opts='+JobFlavour="workday"'

    combineTool.py -M Impacts -d ../Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.root -m 125 -t -1 -o impacts_FullRun2_v9_binning.json --setParameters r_S=1.3693,r_A=0.224,r_higgs=1 --setParameterRanges r_S=0,10:r_A=-1,1 --redefineSignalPOIs r_A --freezeParameters r_higgs

    plotImpacts.py -i impacts_FullRun2_v9_binning.json -o Impact_FullRun2_v9_binning

    rm combine_*
    rm condor_*
    rm higgsCombine_*

Copy the plots on the web:

    DATE=2024_05_03

    mkdir -p /eos/user/n/ntrevisa/www/plots/${DATE}/FullRun2/Impacts/

    cp ~/index.php /eos/user/n/ntrevisa/www/plots/${DATE}/FullRun2/
    cp ~/index.php /eos/user/n/ntrevisa/www/plots/${DATE}/FullRun2/Impacts/

    cp impacts_FullRun2_v9_binning.json Impact_FullRun2_v9_binning.pdf /eos/user/n/ntrevisa/www/plots/${DATE}/FullRun2/Impacts/

### Produce Likelihood scan

	bash do_LH_scan.sh

