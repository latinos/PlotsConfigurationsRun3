#!/usr/bin/env python
from ROOT import TMVA, TFile, TTree, TCut, TChain
from subprocess import call
from os.path import isfile

import sys

import config_BDT as config

# Setup TMVA
def runJob(output_and_dataset_name = ""):
    TMVA.Tools.Instance()
    TMVA.PyMethodBase.PyInitialize()

    output = TFile.Open('TMVA{}.root'.format(output_and_dataset_name), 'RECREATE')
    factory = TMVA.Factory('TMVAClassification', output,'!V:!Silent:Color:DrawProgressBar:AnalysisType=Classification')
    # factory = TMVA.Factory('TMVAClassification', output,'!V:!Silent:Color:DrawProgressBar:Transformations=D,G:AnalysisType=Classification')

    dataloader = TMVA.DataLoader("dataset{}".format(output_and_dataset_name))

    for br in config.mvaVariables:
        dataloader.AddVariable(br)

    for sampleName, sample in config.samples.items():
        isData = config.structure[sampleName]['isData']
        if (isinstance(isData, int) and isData == 1) or (not isinstance(isData, int) and 'all' in isData):
            continue

        sample['tree'] = TChain("Events")
        print("Sample name: ", sampleName)
        for name, *location_weights in sample['name']:
            print("Sub-sample: ", name)
            locations = location_weights[0]
            # weights = location_weights[1] if len(location_weights) > 1 else None
            for loc in locations:
                print("file: ", loc)
                sample['tree'].Add(loc)

        if config.structure[sampleName]['isSignal']==1:
            dataloader.AddSignalTree(sample['tree'], 1.0)
        else:
            dataloader.AddBackgroundTree(sample['tree'], 1.0)
        # output_dim += 1
    # Reference: https://root.cern.ch/download/doc/tmva/TMVAUsersGuide.pdf
    # Train test dataset will contain less/equal events compared to signal and background trees. How these events are chosen is given by the next line. Event weights are given by Monte Carlo generators, and may turn out to be overall very small or large. To avoid artifacts due to this, TMVA can internally renormalise the signal and background training using NormMode.
    dataloader.PrepareTrainingAndTestTree(TCut(config.cut),'SplitMode=Random:NormMode=NumEvents:!V')
    # dataloader.PrepareTrainingAndTestTree(TCut(config.cut),'nTrain_Signal=100000:nTrain_Background=100000:SplitMode=Random:NormMode=NumEvents:!V')#SSSF

    factory.BookMethod(dataloader, TMVA.Types.kBDT, "BDTG4",   "!H:!V:NTrees=500:MinNodeSize=1.5%:BoostType=Grad:Shrinkage=0.05:UseBaggedBoost:GradBaggingFraction=0.5:nCuts=500:MaxDepth=2" )
    # factory.BookMethod(dataloader, TMVA.Types.kBDT, "BDTG4D3",   "!H:!V:NTrees=500:MinNodeSize=1.5%:BoostType=Grad:Shrinkage=0.05:UseBaggedBoost:GradBaggingFraction=0.5:nCuts=500:MaxDepth=3" )
    # factory.BookMethod(dataloader, TMVA.Types.kBDT, "BDTG4D4",   "!H:!V:NTrees=500:MinNodeSize=1.5%:BoostType=Grad:Shrinkage=0.05:UseBaggedBoost:GradBaggingFraction=0.5:nCuts=500:MaxDepth=4" )
    # factory.BookMethod(dataloader, TMVA.Types.kBDT, "BDTG4D5",   "!H:!V:NTrees=500:MinNodeSize=1.5%:BoostType=Grad:Shrinkage=0.05:UseBaggedBoost:GradBaggingFraction=0.5:nCuts=500:MaxDepth=5" )
    # factory.BookMethod(dataloader, TMVA.Types.kBDT, "BDTG4D6",   "!H:!V:NTrees=500:MinNodeSize=1.5%:BoostType=Grad:Shrinkage=0.05:UseBaggedBoost:GradBaggingFraction=0.5:nCuts=500:MaxDepth=6" )
    # factory.BookMethod(dataloader, TMVA.Types.kBDT, "BDTG4C3", "!H:!V:NTrees=500:MinNodeSize=1.5%:BoostType=Grad:Shrinkage=0.05:UseBaggedBoost:GradBaggingFraction=0.5:nCuts=300:MaxDepth=2" )
    # factory.BookMethod(dataloader, TMVA.Types.kBDT, "BDTG4SK01",   "!H:!V:NTrees=500:MinNodeSize=1.5%:BoostType=Grad:Shrinkage=0.01:UseBaggedBoost:GradBaggingFraction=0.5:nCuts=500:MaxDepth=2" )
    # factory.BookMethod(dataloader, TMVA.Types.kBDT, "BDTG4F07"    ,   "!H:!V:NTrees=500:MinNodeSize=1.5%:BoostType=Grad:Shrinkage=0.05:UseBaggedBoost:GradBaggingFraction=0.7:nCuts=500:MaxDepth=2" )
    # factory.BookMethod(dataloader, TMVA.Types.kBDT, "BDTG4SK01F07",   "!H:!V:NTrees=500:MinNodeSize=1.5%:BoostType=Grad:Shrinkage=0.01:UseBaggedBoost:GradBaggingFraction=0.7:nCuts=500:MaxDepth=2" )
    # Run training, test and evaluation
    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()

    output.Close()

if __name__ == "__main__":

    print("Input arguments: {}".format(sys.argv))
    if len(sys.argv) > 1:
        print("Suffix is: {}".format(sys.argv[1]))
        output_and_dataset = sys.argv[1]
        runJob(output_and_dataset)
        os.system("mv dataset dataset{}".format(output_and_dataset))
    else:
        print("No suffix, running with standard output name")
        runJob()
