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

Compute the DY-veto uncertainties:

    python doVetoUncertanty.py

Get the ggToWW (S+B+I) scale variation uncertainty as a function of the amount of ggWW. Copy the output in nuisances_ALL.py:

    python doGluGluRatios.py


Plot distributions:

    mkPlot ....

    plotCATstyle.py ....

Produce datacards. Here, using the correct normalization for the signals:

    mkDatacards

Combine datacards:

    cp combine/HiggsHelicity.py $HOME/work/combine/CMSSW_11_3_4/src/HiggsAnalysis/CombinedLimit/python/

    cp combine/doAnalysis.sh $HOME/work/combine/CMSSW_11_3_4/src/

    cmssw-cc7

    cd $HOME/work/combine/CMSSW_11_3_4/src/;cmsenv;cd -;ulimit -s unlimited

    scram b -j 4

    ./doAnalysis.sh


Datacard to workspace (doOnlyPolarization is the working version of the fit model for only shape variation):

    text2workspace.py datacard_combined.txt -m 125 -P HiggsAnalysis.CombinedLimit.HiggsHelicity:higgshelicity --PO doOnlyPolarization -o datacard_combined.root

Fit data to get impacts:

    combineTool.py -M Impacts -d datacard_combined.root -m 125 -t -1 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy=0 --setParameters r_LL=1,r_TT=1 --redefineSignalPOIs r_LL,r_TT --setParameterRanges r_LL=0,4:r_TT=0,4 --doInitialFit

    combineTool.py -M Impacts -d datacard_combined.root -m 125 -t -1 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy=0 --setParameters r_LL=1,r_TT=1 --redefineSignalPOIs r_LL,r_TT --setParameterRanges r_LL=0,4:r_TT=0,4 --doFits --job-mode=interactive --parallel=10

    combineTool.py -M Impacts -d datacard_combined.root -m 125 -t -1 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy=0 --setParameters r_LL=1,r_TT=1 --redefineSignalPOIs r_LL,r_TT --setParameterRanges r_LL=0,4:r_TT=0,4 -o impacts.json

    plotImpacts.py -i impacts.json -o impacts --POI r_LL

    plotImpacts.py -i impacts.json -o impacts --POI r_TT

If you want to submit the jobs to HTCondor (**Recommended**):

    combineTool.py -M Impacts -d datacard_combined.root -m 125 -t -1 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy=0 --setParameters r_LL=1,r_TT=1 --redefineSignalPOIs r_LL,r_TT --setParameterRanges r_LL=0,4:r_TT=0,4 --doInitialFit

    combineTool.py -M Impacts -d datacard_combined.root -m 125 -t -1 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy=0 --setParameters r_LL=1,r_TT=1 --redefineSignalPOIs r_LL,r_TT --setParameterRanges r_LL=0,4:r_TT=0,4 --doFits --job-mode=condor --parallel=1

    combineTool.py -M Impacts -d datacard_combined.root -m 125 -t -1 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy=0 --setParameters r_LL=1,r_TT=1 --redefineSignalPOIs r_LL,r_TT --setParameterRanges r_LL=0,4:r_TT=0,4 -o impacts.json

    plotImpacts.py -i impacts.json -o impacts --POI r_LL

    plotImpacts.py -i impacts.json -o impacts --POI r_TT

Generate 2D likelihood scans:

    combine -M MultiDimFit --algo grid --points 1000 --setParameters r_LL=1,r_TT=1 --redefineSignalPOIs r_LL,r_TT --setParameterRanges r_LL=0,4:r_TT=0,4 -t -1 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy=0 --verbose 1 -d datacard_combined.root -m 125

    or

    combine -M MultiDimFit --algo grid --points 1000 --setParameters r_LL=1,r_TT=1 --redefineSignalPOIs r_LL,r_TT --setParameterRanges r_LL=0,4:r_TT=0,4 -t -1 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy=0 --verbose 1 -d datacard_combined.root -m 125 --job-mode=condor --split 1


Once you have the likelihhod scans you can run the code in the notebook to produce the plots using the CAT recommended style for figures 


Compute significance for each POI. Floating both:

    combine -M Significance datacard_combined.root  -t -1 -m 125 --setParameters r_LL=1,r_TT=1 --redefineSignalPOIs r_LL
    
    combine -M Significance datacard_combined.root  -t -1 -m 125 --setParameters r_LL=1,r_TT=1 --redefineSignalPOIs r_TT

Fixing one to 1.0:

    combine -M Significance datacard_combined.root -m 125 -t -1 --X-rtd MINIMIZER_analytic --freezeParameters r_TT --cminDefaultMinimizerStrategy=0 --setParameters r_LL=1 --redefineSignalPOIs r_LL

    combine -M Significance datacard_combined.root -m 125 -t -1 --X-rtd MINIMIZER_analytic --freezeParameters r_LL --cminDefaultMinimizerStrategy=0 --setParameters r_TT=1 --redefineSignalPOIs r_TT

**Bonus**

Compute 2D likelihood scan with only statistical uncertainty:

    combineTool.py -d datacard_combined.root -M MultiDimFit --algo grid --points 1000 --freezeParameters allConstrainedNuisances --setParameters r_LL=1,r_TT=1 --redefineSignalPOIs r_LL,r_TT --setParameterRanges r_LL=0,2.25:r_TT=0,2.25 -t -1 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy=0 --verbose 1 -m 125 --split 1 --job-mode=condor

Compute 2D likelihood scan with experimental and statistical uncertainties:

    combineTool.py -d datacard_combined.root -M MultiDimFit --algo grid --points 1000 --freezeParameters CMS_CMS_top_pT_reweighting,CMS_PS_WH_hww_FSR,CMS_PS_WH_hww_ISR,CMS_PS_hww_FSR,CMS_PS_hww_ISR,CMS_QCDscale_VV,CMS_QCDscale_WWewk,CMS_QCDscale_top_0j,CMS_QCDscale_top_1j,CMS_QCDscale_top_2j,CMS_WH_hww_UE,CMS_fake_syst,CMS_hww_CRSR_accept_DY,CMS_hww_CRSR_accept_WW,CMS_hww_CRSR_accept_top,CMS_hww_UE,CMS_hww_WgStarScale,CMS_hww_pdf_WW_eigen1,CMS_hww_pdf_WW_eigen10,CMS_hww_pdf_WW_eigen100,CMS_hww_pdf_WW_eigen11,CMS_hww_pdf_WW_eigen12,CMS_hww_pdf_WW_eigen13,CMS_hww_pdf_WW_eigen14,CMS_hww_pdf_WW_eigen15,CMS_hww_pdf_WW_eigen16,CMS_hww_pdf_WW_eigen17,CMS_hww_pdf_WW_eigen18,CMS_hww_pdf_WW_eigen19,CMS_hww_pdf_WW_eigen2,CMS_hww_pdf_WW_eigen20,CMS_hww_pdf_WW_eigen21,CMS_hww_pdf_WW_eigen22,CMS_hww_pdf_WW_eigen23,CMS_hww_pdf_WW_eigen24,CMS_hww_pdf_WW_eigen25,CMS_hww_pdf_WW_eigen26,CMS_hww_pdf_WW_eigen27,CMS_hww_pdf_WW_eigen28,CMS_hww_pdf_WW_eigen29,CMS_hww_pdf_WW_eigen3,CMS_hww_pdf_WW_eigen30,CMS_hww_pdf_WW_eigen31,CMS_hww_pdf_WW_eigen32,CMS_hww_pdf_WW_eigen33,CMS_hww_pdf_WW_eigen34,CMS_hww_pdf_WW_eigen35,CMS_hww_pdf_WW_eigen36,CMS_hww_pdf_WW_eigen37,CMS_hww_pdf_WW_eigen38,CMS_hww_pdf_WW_eigen39,CMS_hww_pdf_WW_eigen4,CMS_hww_pdf_WW_eigen40,CMS_hww_pdf_WW_eigen41,CMS_hww_pdf_WW_eigen42,CMS_hww_pdf_WW_eigen43,CMS_hww_pdf_WW_eigen44,CMS_hww_pdf_WW_eigen45,CMS_hww_pdf_WW_eigen46,CMS_hww_pdf_WW_eigen47,CMS_hww_pdf_WW_eigen48,CMS_hww_pdf_WW_eigen49,CMS_hww_pdf_WW_eigen5,CMS_hww_pdf_WW_eigen50,CMS_hww_pdf_WW_eigen51,CMS_hww_pdf_WW_eigen52,CMS_hww_pdf_WW_eigen53,CMS_hww_pdf_WW_eigen54,CMS_hww_pdf_WW_eigen55,CMS_hww_pdf_WW_eigen56,CMS_hww_pdf_WW_eigen57,CMS_hww_pdf_WW_eigen58,CMS_hww_pdf_WW_eigen59,CMS_hww_pdf_WW_eigen6,CMS_hww_pdf_WW_eigen60,CMS_hww_pdf_WW_eigen61,CMS_hww_pdf_WW_eigen62,CMS_hww_pdf_WW_eigen63,CMS_hww_pdf_WW_eigen64,CMS_hww_pdf_WW_eigen65,CMS_hww_pdf_WW_eigen66,CMS_hww_pdf_WW_eigen67,CMS_hww_pdf_WW_eigen68,CMS_hww_pdf_WW_eigen69,CMS_hww_pdf_WW_eigen7,CMS_hww_pdf_WW_eigen70,CMS_hww_pdf_WW_eigen71,CMS_hww_pdf_WW_eigen72,CMS_hww_pdf_WW_eigen73,CMS_hww_pdf_WW_eigen74,CMS_hww_pdf_WW_eigen75,CMS_hww_pdf_WW_eigen76,CMS_hww_pdf_WW_eigen77,CMS_hww_pdf_WW_eigen78,CMS_hww_pdf_WW_eigen79,CMS_hww_pdf_WW_eigen8,CMS_hww_pdf_WW_eigen80,CMS_hww_pdf_WW_eigen81,CMS_hww_pdf_WW_eigen82,CMS_hww_pdf_WW_eigen83,CMS_hww_pdf_WW_eigen84,CMS_hww_pdf_WW_eigen85,CMS_hww_pdf_WW_eigen86,CMS_hww_pdf_WW_eigen87,CMS_hww_pdf_WW_eigen88,CMS_hww_pdf_WW_eigen89,CMS_hww_pdf_WW_eigen9,CMS_hww_pdf_WW_eigen90,CMS_hww_pdf_WW_eigen91,CMS_hww_pdf_WW_eigen92,CMS_hww_pdf_WW_eigen93,CMS_hww_pdf_WW_eigen94,CMS_hww_pdf_WW_eigen95,CMS_hww_pdf_WW_eigen96,CMS_hww_pdf_WW_eigen97,CMS_hww_pdf_WW_eigen98,CMS_hww_pdf_WW_eigen99,CMS_hww_pdf_top_eigen1,CMS_hww_pdf_top_eigen10,CMS_hww_pdf_top_eigen100,CMS_hww_pdf_top_eigen11,CMS_hww_pdf_top_eigen12,CMS_hww_pdf_top_eigen13,CMS_hww_pdf_top_eigen14,CMS_hww_pdf_top_eigen15,CMS_hww_pdf_top_eigen16,CMS_hww_pdf_top_eigen17,CMS_hww_pdf_top_eigen18,CMS_hww_pdf_top_eigen19,CMS_hww_pdf_top_eigen2,CMS_hww_pdf_top_eigen20,CMS_hww_pdf_top_eigen21,CMS_hww_pdf_top_eigen22,CMS_hww_pdf_top_eigen23,CMS_hww_pdf_top_eigen24,CMS_hww_pdf_top_eigen25,CMS_hww_pdf_top_eigen26,CMS_hww_pdf_top_eigen27,CMS_hww_pdf_top_eigen28,CMS_hww_pdf_top_eigen29,CMS_hww_pdf_top_eigen3,CMS_hww_pdf_top_eigen30,CMS_hww_pdf_top_eigen31,CMS_hww_pdf_top_eigen32,CMS_hww_pdf_top_eigen33,CMS_hww_pdf_top_eigen34,CMS_hww_pdf_top_eigen35,CMS_hww_pdf_top_eigen36,CMS_hww_pdf_top_eigen37,CMS_hww_pdf_top_eigen38,CMS_hww_pdf_top_eigen39,CMS_hww_pdf_top_eigen4,CMS_hww_pdf_top_eigen40,CMS_hww_pdf_top_eigen41,CMS_hww_pdf_top_eigen42,CMS_hww_pdf_top_eigen43,CMS_hww_pdf_top_eigen44,CMS_hww_pdf_top_eigen45,CMS_hww_pdf_top_eigen46,CMS_hww_pdf_top_eigen47,CMS_hww_pdf_top_eigen48,CMS_hww_pdf_top_eigen49,CMS_hww_pdf_top_eigen5,CMS_hww_pdf_top_eigen50,CMS_hww_pdf_top_eigen51,CMS_hww_pdf_top_eigen52,CMS_hww_pdf_top_eigen53,CMS_hww_pdf_top_eigen54,CMS_hww_pdf_top_eigen55,CMS_hww_pdf_top_eigen56,CMS_hww_pdf_top_eigen57,CMS_hww_pdf_top_eigen58,CMS_hww_pdf_top_eigen59,CMS_hww_pdf_top_eigen6,CMS_hww_pdf_top_eigen60,CMS_hww_pdf_top_eigen61,CMS_hww_pdf_top_eigen62,CMS_hww_pdf_top_eigen63,CMS_hww_pdf_top_eigen64,CMS_hww_pdf_top_eigen65,CMS_hww_pdf_top_eigen66,CMS_hww_pdf_top_eigen67,CMS_hww_pdf_top_eigen68,CMS_hww_pdf_top_eigen69,CMS_hww_pdf_top_eigen7,CMS_hww_pdf_top_eigen70,CMS_hww_pdf_top_eigen71,CMS_hww_pdf_top_eigen72,CMS_hww_pdf_top_eigen73,CMS_hww_pdf_top_eigen74,CMS_hww_pdf_top_eigen75,CMS_hww_pdf_top_eigen76,CMS_hww_pdf_top_eigen77,CMS_hww_pdf_top_eigen78,CMS_hww_pdf_top_eigen79,CMS_hww_pdf_top_eigen8,CMS_hww_pdf_top_eigen80,CMS_hww_pdf_top_eigen81,CMS_hww_pdf_top_eigen82,CMS_hww_pdf_top_eigen83,CMS_hww_pdf_top_eigen84,CMS_hww_pdf_top_eigen85,CMS_hww_pdf_top_eigen86,CMS_hww_pdf_top_eigen87,CMS_hww_pdf_top_eigen88,CMS_hww_pdf_top_eigen89,CMS_hww_pdf_top_eigen9,CMS_hww_pdf_top_eigen90,CMS_hww_pdf_top_eigen91,CMS_hww_pdf_top_eigen92,CMS_hww_pdf_top_eigen93,CMS_hww_pdf_top_eigen94,CMS_hww_pdf_top_eigen95,CMS_hww_pdf_top_eigen96,CMS_hww_pdf_top_eigen97,CMS_hww_pdf_top_eigen98,CMS_hww_pdf_top_eigen99,QCDscale_V,QCDscale_VH,QCDscale_ggVV,QCDscale_ggZH,QCDscale_gg_ACCEPT,QCDscale_qqH,QCDscale_qqbar_ACCEPT,QCDscale_ttH,THU_ggH_Mig01,THU_ggH_Mig12,THU_ggH_Mu,THU_ggH_PT120,THU_ggH_PT60,THU_ggH_Res,THU_ggH_VBF2j,THU_ggH_VBF3j,THU_ggH_qmtop,THU_qqH_EWK,THU_qqH_JET01,THU_qqH_Mjj1000,THU_qqH_Mjj120,THU_qqH_Mjj1500,THU_qqH_Mjj350,THU_qqH_Mjj60,THU_qqH_Mjj700,THU_qqH_PTH200,THU_qqH_PTH25,THU_qqH_YIELD,pdf_Higgs_gg,pdf_Higgs_gg_ACCEPT,pdf_Higgs_qqbar,pdf_Higgs_qqbar_ACCEPT,pdf_Higgs_ttH,pdf_gg_ACCEPT,pdf_qqbar,singleTopToTTbar --setParameters r_LL=1,r_TT=1 --redefineSignalPOIs r_LL,r_TT --setParameterRanges r_LL=0,2.25:r_TT=0,2.25 -t -1 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy=0 --verbose 1 -m 125 --split 1 --job-mode=condor
