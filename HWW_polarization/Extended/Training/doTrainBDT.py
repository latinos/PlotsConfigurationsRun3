import ROOT
import pandas as pd
import uproot
import numpy as np
import pandas as pd

from ROOT import TMVA, TFile, TTree, TCut, TChain
from subprocess import call
from os.path import isfile
import subprocess



input_signal = []
input_bkg = []
    
input_signal.append(ROOT.TFile.Open("ntuples_Sig_binary_2j.root"))    
input_bkg.append(ROOT.TFile.Open("ntuples_bkg_binary_2j.root"))

#input_signal.append(ROOT.TFile.Open("ntuples_binary_LL_0j.root"))
#input_bkg.append(ROOT.TFile.Open("ntuples_binary_TT_0j.root"))

input_tree_signal = []
for i in input_signal:
    if i==None:
        continue
    input_tree_signal.append(i.Get("Events"))

input_tree_bkg =[]
for i in input_bkg:
    if i==None:
        continue
    input_tree_bkg.append(i.Get("Events"))


dataloader = TMVA.DataLoader('dataset_Binary_2J_DF')

for j in input_tree_signal:
    dataloader.AddSignalTree(j)

for j in input_tree_bkg:
    if(j.GetEntries()==0):
        continue
    dataloader.AddBackgroundTree(j)


output = TFile.Open('TMVA_Binary_2J_DF.root', 'RECREATE')

factory = TMVA.Factory('TMVAClassification', output,
        '!V:!Silent:Color:DrawProgressBar:AnalysisType=Classification')


#dataloader.AddVariable('lep_pt1')
#dataloader.AddVariable('lep_pt2')
#dataloader.AddVariable('lep_phi1')
#dataloader.AddVariable('lep_phi2')
#dataloader.AddVariable('lep_eta1')
#dataloader.AddVariable('lep_eta2')
dataloader.AddVariable('mll')
dataloader.AddVariable('mth')
dataloader.AddVariable('mtw1')
dataloader.AddVariable('mtw2')
dataloader.AddVariable('ptll')
dataloader.AddVariable('drll')
dataloader.AddVariable('dphilmet1')
dataloader.AddVariable('dphilmet2')
dataloader.AddVariable('dphill')
dataloader.AddVariable('PuppiMET_pt')
dataloader.AddVariable('PuppiMET_phi')
dataloader.AddVariable('detall')
dataloader.AddVariable('mpmet')              
# 1-Jet ---
#dataloader.AddVariable('dphilep1jet1')       
#dataloader.AddVariable('dphilep2jet1')  
#dataloader.AddVariable('btagDeepFlavB')
# 2-Jet ---
#dataloader.AddVariable('mjj')           
#dataloader.AddVariable('Ctot')          
#dataloader.AddVariable('detajj')        
#dataloader.AddVariable('dphilep1jet1')  
#dataloader.AddVariable('dphilep2jet1')  
#dataloader.AddVariable('dphilep1jet2')  
#dataloader.AddVariable('dphilep2jet2')    
#dataloader.AddVariable('btagDeepFlavB')   
#dataloader.AddVariable('btagDeepFlavB_1') 
#dataloader.AddVariable('D_VBF_QCD')       
#dataloader.AddVariable('D_VBF_VH')        
#dataloader.AddVariable('D_QCD_VH')        
#dataloader.AddVariable('D_VBF_DY')   

#dataloader.PrepareTrainingAndTestTree(TCut("(!TMath::IsNaN(D_VBF_QCD)) && (!TMath::IsNaN(D_VBF_VH)) && (!TMath::IsNaN(D_QCD_VH)) && (!TMath::IsNaN(D_VBF_DY))"),'SplitMode=Random::SplitSeed=10:NormMode=EqualNumEvents')

dataloader.PrepareTrainingAndTestTree(TCut(""),'SplitMode=Random::SplitSeed=10:NormMode=EqualNumEvents')

factory.BookMethod(dataloader, TMVA.Types.kBDT, "BDTG4D3",   "!H:!V:NTrees=800:MinNodeSize=1.5%:BoostType=Grad:Shrinkage=0.05:UseBaggedBoost:GradBaggingFraction=0.5:nCuts=500:MaxDepth=5" );  

#factory.BookMethod(dataloader, TMVA.Types.kBDT, "BDTB4D3",   "!H:!V:NTrees=800:MinNodeSize=1.5%:BoostType=Bagging:Shrinkage=0.05:UseBaggedBoost:GradBaggingFraction=0.5:nCuts=500:MaxDepth=5" );  

factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()

output.Close()
