# H > gluon gluon

ZH production of H>gg, 2017


### Load the mkShapesRDF environment

Here, we assume `PlotsConfigurationsRun3` was installed in the same directory as `mkShapesRDF`. E.g., let's assume we have a `Run3` directory where we installed both `mkShapesRDF` and `PlotsConfigurationsRun3`.

Then, we can source the `mkShapesRDF` environment using these commands:

    cd /afs/cern.ch/user/a/amassiro/work/Latinos/Framework/Hgg/Analysis/PlotsConfigurationsRun3/Hgg/2017UL

    cd ../../../mkShapesRDF/
    source start.sh
    cd -

    
(development folder)

    cd /afs/cern.ch/user/a/amassiro/work/Latinos/Framework/Hgg/Analysis/PlotsConfigurationsRun3/Hgg/2017UL
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


