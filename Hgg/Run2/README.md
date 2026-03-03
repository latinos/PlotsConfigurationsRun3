# H > gluon gluon, Full Run 2

ZH production of H>gg


Assume all histograms for different years are already produced.



### Merge the root files into one unique set

This will create a new root file with the hadd of the proper files, and the variations.

If the "up" ("down") variation is present in more than one year, then the different up/down histograms are added.

If a shape variation (a nuisance) is present only in one year, then the nominal for the years for which is missing will be used and hadd.

if a lnN is the same in all years, then it's used only once. It should be written explicitly in nuisances.py. Nothing to be done by mkMergeYears.

If a lnN is present only in one year, then the nuisance has to be transformed into a shape: the nominal sample for the specific year is copied, then it's scaled up/down according to the value in lnN, and lastly it's hadd to the nominal sample of the other years for which the nuisance is missing.


    mkMergeYears

### Run


(development folder)

    cd /afs/cern.ch/user/a/amassiro/work/Latinos/Framework/Hgg/Analysis/PlotsConfigurationsRun3/Hgg/Run2/
    cd /afs/cern.ch/user/a/amassiro/work/Latinos/Framework/mkShapesRDF/
    source start.sh
    cd -

### Merge

    mkMergeYears




### Plot distributions

    mkPlot
    mkPlot --onlyPlot cratio --showIntegralLegend 1 --fileFormats png
    mkPlot --onlyPlot cratio --showIntegralLegend 1 --fileFormats png  --plotNormalizedDistributions


### to check kerberos

    klist


### make datacards

    mkDatacards --outputDirDatacard datacards




