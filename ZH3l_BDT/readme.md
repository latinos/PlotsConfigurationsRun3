Building towards a set of codes for the ZH3l analysis using the PlotsConfigurationsRun3/RDF framework. Among the many changes we desire to implement, the following are the ones we're starting out with:
1. Make the Run2 codes of ZH3l analysis compatible with the Run3 framework (Relevant folder: zh3l_run2_rdf).
2. Train a sample BDT in Run3 framework using Run2 data, weights, and scale-factors (Relevant folder: zh3l_run2_bdt_rdf).
3. Setup a full working pipeline enabling a classification neural network in PlotsConfigurationsRun3 / mkShapesRDF for the ZH3l analysis.

Notes related to point 1 of the above list:
Most of the changes include switching to RDF compliant expressions, commands and functions.
Useful resource related to Run2->Run3 translation: https://indico.cern.ch/event/1201818/contributions/5180441/attachments/2567971/4427668/mkShapesRDF.pdf
Converting some functions in Run3 framework is pending and this has been put off for later. This means some nuisances (QCDscale and pdf) and base weights (for DY and ZZ samples) are not accurate.
10 out of 271 sample files were not processed owing to some segmentation faults (probably from corrupt/incorrect MC files).