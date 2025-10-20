# H > gluon gluon

ZH production of H>gg

### Load the mkShapesRDF environment

Here, we assume `PlotsConfigurationsRun3` was installed in the same directory as `mkShapesRDF`. E.g., let's assume we have a `Run3` directory where we installed both `mkShapesRDF` and `PlotsConfigurationsRun3`.

Then, we can source the `mkShapesRDF` environment using these commands:

    cd /afs/cern.ch/user/a/amassiro/work/Latinos/Framework/Hgg/Analysis/PlotsConfigurationsRun3/Hgg/2018UL

    cd ../../../mkShapesRDF/
    source start.sh
    cd -

    
(development folder)

    cd /afs/cern.ch/user/a/amassiro/work/Latinos/Framework/Hgg/Analysis/PlotsConfigurationsRun3/Hgg/2018UL
    cd /afs/cern.ch/user/a/amassiro/work/Latinos/Framework/mkShapesRDF/
    source start.sh
    cd -
    
    
### Compile the configuration folder

    mkShapesRDF -c 1

### Run the analysis

Produce histograms using batch:

    mkShapesRDF -o 0 -f . -b 1
    
    mkShapesRDF -c 1 -o 0 -f . -b 1
    
    mkShapesRDF --submit

Check jobs status:

    mkShapesRDF -o 1 -f .
    
    
    mkShapesRDF --check
    

Resubmit failed jobs:

    mkShapesRDF -o 1 -f . -r 1

    mkShapesRDF --resubmit 1
    
    
Options meanings:
- -o: operationMode:
    - 0 run analysis
    - 1 check batch output and errs
    - 2 merge root files
- -f: folder: it represents the path to the analysis folder
- -b: batch mode:
    - 0 (default) runs on local
    - 1 runs with condor
- -r: resubmit jobs:
    -1 resubmit finished jobs with errors
   - 2 resubmit running jobs

### Merge rootfiles

Once all the jobs have finished, you can merge them:

    mkShapesRDF -o 2 -f .

    mkShapesRDF --histoadd
    
### Plot distributions

    mkPlot
    mkPlot --onlyPlot cratio --showIntegralLegend 1 --fileFormats png   
    mkPlot --onlyPlot cratio --showIntegralLegend 1 --fileFormats png  --plotNormalizedDistributions
    

### to check kerberos

    klist
    

### make datacards
    
    mkDatacards --outputDirDatacard datacards

    mkDatacards --outputDirDatacard datacards --onlyVariables mjjbins,mjj   --onlyCuts Sig_opt4
    mkDatacards --outputDirDatacard datacards --onlyVariables mjjbins,mjj   --onlyCuts Sig_opt5future
    mkDatacards --outputDirDatacard datacards --onlyVariables mjjbins,mjj   --onlyCuts Sig_opt6future


    
### likelihood scan

    cd /afs/cern.ch/user/a/amassiro/work/Latinos/Framework/Hgg/Analysis/PlotsConfigurationsRun3/Hgg/2018UL
    cd /afs/cern.ch/user/a/amassiro/work/Combine/CMSSW_14_1_0_pre4/src/
    cmsenv
    cd -
    

    combine -M FitDiagnostics --rMin -300 --rMax 302  datacards/Sig_opt4/mjj/datacard.txt     -t -1        >   result.mcasimov.rfit.txt
    combine -M Significance     datacards/Sig_opt4/mjj/datacard.txt     -t -1        >   result.mcasimov.Significance.txt
    
    
    https://twiki.cern.ch/twiki/bin/view/CMS/HWWCombineTools
    https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsWG/SWGuideHiggsProjections
    
    lumiscale rateParam * * 1
    nuisance edit freeze lumiscale

    lumi 2018 = 59.83
    lumi run 2 ~ 140 = lumi(2018) *2.5
    lumi run 1+2+3 ~ 500 = lumi(2018) * 8.5
    
    
    
    combine -M Significance     datacards/Sig_opt4/mjj/datacard.txt     -t -1    --setParameters lumiscale=1     --expectSignal=1  >   result.mcasimov.Significance.2018.txt
    combine -M Significance     datacards/Sig_opt4/mjj/datacard.txt     -t -1    --setParameters lumiscale=2.5   --expectSignal=1  >   result.mcasimov.Significance.run2.txt
    combine -M Significance     datacards/Sig_opt4/mjj/datacard.txt     -t -1    --setParameters lumiscale=8.5   --expectSignal=1  >   result.mcasimov.Significance.run123.txt

    
    combine -M Significance     datacards/Sig_opt4/mjjbins/datacard.txt     -t -1    --setParameters lumiscale=1     --expectSignal=1  >   result.mcasimov.Significance.2018.txt
    combine -M Significance     datacards/Sig_opt4/mjjbins/datacard.txt     -t -1    --setParameters lumiscale=2.5   --expectSignal=1  >   result.mcasimov.Significance.run2.txt
    combine -M Significance     datacards/Sig_opt4/mjjbins/datacard.txt     -t -1    --setParameters lumiscale=8.5   --expectSignal=1  >   result.mcasimov.Significance.run123.txt
    combine -M Significance     datacards/Sig_opt4/mjjbins/datacard.txt     -t -1    --setParameters lumiscale=1000  --expectSignal=1  >   result.mcasimov.Significance.ahah.txt

    
    cat result.mcasimov.Significance.2018.txt  result.mcasimov.Significance.run2.txt result.mcasimov.Significance.run123.txt | grep "Significance:"
    cat result.mcasimov.Significance.2018.txt  result.mcasimov.Significance.run2.txt result.mcasimov.Significance.run123.txt result.mcasimov.Significance.ahah.txt | grep "Significance:"
    
    
    combine -M Significance     datacards/Sig_opt5future/mjj/datacard.txt     -t -1    --setParameters lumiscale=1     --expectSignal=1  >   result.mcasimov.Significance.2018.txt
    combine -M Significance     datacards/Sig_opt5future/mjj/datacard.txt     -t -1    --setParameters lumiscale=2.5   --expectSignal=1  >   result.mcasimov.Significance.run2.txt
    combine -M Significance     datacards/Sig_opt5future/mjj/datacard.txt     -t -1    --setParameters lumiscale=8.5   --expectSignal=1  >   result.mcasimov.Significance.run123.txt


    combine -M Significance     datacards/Sig_opt5future/mjjbins/datacard.txt     -t -1    --setParameters lumiscale=1     --expectSignal=1  >   result.mcasimov.Significance.2018.txt
    combine -M Significance     datacards/Sig_opt5future/mjjbins/datacard.txt     -t -1    --setParameters lumiscale=2.5   --expectSignal=1  >   result.mcasimov.Significance.run2.txt
    combine -M Significance     datacards/Sig_opt5future/mjjbins/datacard.txt     -t -1    --setParameters lumiscale=8.5   --expectSignal=1  >   result.mcasimov.Significance.run123.txt

    
    cat result.mcasimov.Significance.2018.txt  result.mcasimov.Significance.run2.txt result.mcasimov.Significance.run123.txt | grep "Significance:"

    
    combine -M Significance     datacards/Sig_opt5future/mjjbins/datacard.txt     -t -1    --setParameters lumiscale=1     --expectSignal=1  >   result.mcasimov.Significance.1.txt
    combine -M Significance     datacards/Sig_opt5future/mjjbins/datacard.txt     -t -1    --setParameters lumiscale=2     --expectSignal=1  >   result.mcasimov.Significance.2.txt
    combine -M Significance     datacards/Sig_opt5future/mjjbins/datacard.txt     -t -1    --setParameters lumiscale=4     --expectSignal=1  >   result.mcasimov.Significance.4.txt
    combine -M Significance     datacards/Sig_opt5future/mjjbins/datacard.txt     -t -1    --setParameters lumiscale=8     --expectSignal=1  >   result.mcasimov.Significance.8.txt
    combine -M Significance     datacards/Sig_opt5future/mjjbins/datacard.txt     -t -1    --setParameters lumiscale=20    --expectSignal=1  >   result.mcasimov.Significance.20.txt
    combine -M Significance     datacards/Sig_opt5future/mjjbins/datacard.txt     -t -1    --setParameters lumiscale=40    --expectSignal=1  >   result.mcasimov.Significance.40.txt

    
    cat result.mcasimov.Significance.1.txt  result.mcasimov.Significance.2.txt result.mcasimov.Significance.4.txt  result.mcasimov.Significance.8.txt  result.mcasimov.Significance.20.txt  result.mcasimov.Significance.40.txt | grep "Significance:"
    
    

    
    
    combine -M FitDiagnostics     datacards/Sig_opt5future/mjjbins/datacard.txt  --rMin -300 --rMax 13002   -t -1    --setParameters lumiscale=1     --expectSignal=10000  >   result.mcasimov.FitDiagnostics.1.txt
    combine -M FitDiagnostics     datacards/Sig_opt5future/mjjbins/datacard.txt  --rMin -300 --rMax 13002   -t -1    --setParameters lumiscale=2     --expectSignal=10000  >   result.mcasimov.FitDiagnostics.2.txt
    combine -M FitDiagnostics     datacards/Sig_opt5future/mjjbins/datacard.txt  --rMin -300 --rMax 13002   -t -1    --setParameters lumiscale=4     --expectSignal=10000  >   result.mcasimov.FitDiagnostics.4.txt
    combine -M FitDiagnostics     datacards/Sig_opt5future/mjjbins/datacard.txt  --rMin -300 --rMax 13002   -t -1    --setParameters lumiscale=8     --expectSignal=10000  >   result.mcasimov.FitDiagnostics.8.txt
    combine -M FitDiagnostics     datacards/Sig_opt5future/mjjbins/datacard.txt  --rMin -300 --rMax 13002   -t -1    --setParameters lumiscale=20    --expectSignal=10000  >   result.mcasimov.FitDiagnostics.20.txt
    combine -M FitDiagnostics     datacards/Sig_opt5future/mjjbins/datacard.txt  --rMin -300 --rMax 13002   -t -1    --setParameters lumiscale=40    --expectSignal=10000  >   result.mcasimov.FitDiagnostics.40.txt
    combine -M FitDiagnostics     datacards/Sig_opt5future/mjjbins/datacard.txt  --rMin -300 --rMax 13002   -t -1    --setParameters lumiscale=100   --expectSignal=10000  >   result.mcasimov.FitDiagnostics.100.txt
    combine -M FitDiagnostics     datacards/Sig_opt5future/mjjbins/datacard.txt  --rMin -300 --rMax 13002   -t -1    --setParameters lumiscale=200   --expectSignal=10000  >   result.mcasimov.FitDiagnostics.200.txt

    
    cat result.mcasimov.FitDiagnostics.1.txt  result.mcasimov.FitDiagnostics.2.txt result.mcasimov.FitDiagnostics.4.txt  result.mcasimov.FitDiagnostics.8.txt  result.mcasimov.FitDiagnostics.20.txt  result.mcasimov.FitDiagnostics.40.txt result.mcasimov.FitDiagnostics.100.txt  result.mcasimov.FitDiagnostics.200.txt  | grep "Best fit r:"
    
    

    
    combine -M FitDiagnostics     datacards/Sig_opt6future/mjj/datacard.txt  --rMin -300 --rMax 302   -t -1    --setParameters lumiscale=1     --expectSignal=100  >   result.mcasimov.FitDiagnostics.1.txt
    combine -M FitDiagnostics     datacards/Sig_opt6future/mjj/datacard.txt  --rMin -300 --rMax 302   -t -1    --setParameters lumiscale=2     --expectSignal=100  >   result.mcasimov.FitDiagnostics.2.txt
    combine -M FitDiagnostics     datacards/Sig_opt6future/mjj/datacard.txt  --rMin -300 --rMax 302   -t -1    --setParameters lumiscale=4     --expectSignal=100  >   result.mcasimov.FitDiagnostics.4.txt
    combine -M FitDiagnostics     datacards/Sig_opt6future/mjj/datacard.txt  --rMin -300 --rMax 302   -t -1    --setParameters lumiscale=8     --expectSignal=100  >   result.mcasimov.FitDiagnostics.8.txt
    combine -M FitDiagnostics     datacards/Sig_opt6future/mjj/datacard.txt  --rMin -300 --rMax 302   -t -1    --setParameters lumiscale=20    --expectSignal=100  >   result.mcasimov.FitDiagnostics.20.txt
    combine -M FitDiagnostics     datacards/Sig_opt6future/mjj/datacard.txt  --rMin -300 --rMax 302   -t -1    --setParameters lumiscale=40    --expectSignal=100  >   result.mcasimov.FitDiagnostics.40.txt
    combine -M FitDiagnostics     datacards/Sig_opt6future/mjj/datacard.txt  --rMin -300 --rMax 302   -t -1    --setParameters lumiscale=100   --expectSignal=100  >   result.mcasimov.FitDiagnostics.100.txt
    combine -M FitDiagnostics     datacards/Sig_opt6future/mjj/datacard.txt  --rMin -300 --rMax 302   -t -1    --setParameters lumiscale=200   --expectSignal=100  >   result.mcasimov.FitDiagnostics.200.txt

    
    cat result.mcasimov.FitDiagnostics.1.txt  result.mcasimov.FitDiagnostics.2.txt result.mcasimov.FitDiagnostics.4.txt  result.mcasimov.FitDiagnostics.8.txt  result.mcasimov.FitDiagnostics.20.txt  result.mcasimov.FitDiagnostics.40.txt result.mcasimov.FitDiagnostics.100.txt  result.mcasimov.FitDiagnostics.200.txt  | grep "Best fit r:"
    

    
    combine -M Significance     datacards/Sig_opt6future/mjj/datacard.txt   -t -1    --setParameters lumiscale=1     --expectSignal=100  >   result.mcasimov.Significance.1.txt
    combine -M Significance     datacards/Sig_opt6future/mjj/datacard.txt   -t -1    --setParameters lumiscale=2     --expectSignal=100  >   result.mcasimov.Significance.2.txt
    combine -M Significance     datacards/Sig_opt6future/mjj/datacard.txt   -t -1    --setParameters lumiscale=4     --expectSignal=100  >   result.mcasimov.Significance.4.txt
    combine -M Significance     datacards/Sig_opt6future/mjj/datacard.txt   -t -1    --setParameters lumiscale=8     --expectSignal=100  >   result.mcasimov.Significance.8.txt
    combine -M Significance     datacards/Sig_opt6future/mjj/datacard.txt   -t -1    --setParameters lumiscale=20    --expectSignal=100  >   result.mcasimov.Significance.20.txt
    combine -M Significance     datacards/Sig_opt6future/mjj/datacard.txt   -t -1    --setParameters lumiscale=40    --expectSignal=100  >   result.mcasimov.Significance.40.txt
    combine -M Significance     datacards/Sig_opt6future/mjj/datacard.txt   -t -1    --setParameters lumiscale=100   --expectSignal=100  >   result.mcasimov.Significance.100.txt
    combine -M Significance     datacards/Sig_opt6future/mjj/datacard.txt   -t -1    --setParameters lumiscale=200   --expectSignal=100  >   result.mcasimov.Significance.200.txt

    
    cat result.mcasimov.Significance.1.txt  result.mcasimov.Significance.2.txt result.mcasimov.Significance.4.txt  result.mcasimov.Significance.8.txt  result.mcasimov.Significance.20.txt  result.mcasimov.Significance.40.txt result.mcasimov.Significance.100.txt  result.mcasimov.Significance.200.txt  | grep "Significance:"
    
    
    
    combine -M Significance     datacards/Sig_opt6future/mjj/datacard.txt   -t -1    --setParameters lumiscale=1     --expectSignal=1  >   result.mcasimov.Significance.1.txt
    combine -M Significance     datacards/Sig_opt6future/mjj/datacard.txt   -t -1    --setParameters lumiscale=2     --expectSignal=1  >   result.mcasimov.Significance.2.txt
    combine -M Significance     datacards/Sig_opt6future/mjj/datacard.txt   -t -1    --setParameters lumiscale=4     --expectSignal=1  >   result.mcasimov.Significance.4.txt
    combine -M Significance     datacards/Sig_opt6future/mjj/datacard.txt   -t -1    --setParameters lumiscale=8     --expectSignal=1  >   result.mcasimov.Significance.8.txt
    combine -M Significance     datacards/Sig_opt6future/mjj/datacard.txt   -t -1    --setParameters lumiscale=20    --expectSignal=1  >   result.mcasimov.Significance.20.txt
    combine -M Significance     datacards/Sig_opt6future/mjj/datacard.txt   -t -1    --setParameters lumiscale=40    --expectSignal=1  >   result.mcasimov.Significance.40.txt
    combine -M Significance     datacards/Sig_opt6future/mjj/datacard.txt   -t -1    --setParameters lumiscale=100   --expectSignal=1  >   result.mcasimov.Significance.100.txt
    combine -M Significance     datacards/Sig_opt6future/mjj/datacard.txt   -t -1    --setParameters lumiscale=200   --expectSignal=1  >   result.mcasimov.Significance.200.txt

    
    cat result.mcasimov.Significance.1.txt  result.mcasimov.Significance.2.txt result.mcasimov.Significance.4.txt  result.mcasimov.Significance.8.txt  result.mcasimov.Significance.20.txt  result.mcasimov.Significance.40.txt result.mcasimov.Significance.100.txt  result.mcasimov.Significance.200.txt  | grep "Significance:"
    
    
    
    
    
    
    