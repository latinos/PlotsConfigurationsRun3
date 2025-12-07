import ROOT
import uproot
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplhep as hep
import os
import sys
import matplotlib.pyplot as plt
import mplhep as hep
hep.style.use("CMS")


fileName = "/eos/user/s/sblancof/MC/rootFiles/mkShapes__WW_2018_complete.root"
file = ROOT.TFile.Open('/eos/user/s/sblancof/MC/rootFiles/mkShapes__WW_2018_complete.root')
cutName = "hww2l2v_13TeV_top_2j"
variableName = 'mll'

histo_test = file.Get(cutName+'/'+variableName+'/histo_top')

nbins = histo_test.GetXaxis().GetNbins()
xmin = histo_test.GetXaxis().GetXmin()
xmax = histo_test.GetXaxis().GetXmax()

variables = {}

variables[variableName] = {   'name'  : variableName,
                          'range' : (nbins, xmin, xmax),                                                                                                                                                                                        
                          'xaxis' : variableName,
                          'fold'  : 3}



fig, ax = plt.subplots()
hep.cms.label("Preliminary", ax=ax, data=True, loc=0)
hep.cms.lumitext("59.7 $fb^{-1}$               ", ax=ax)

df = uproot.open(fileName)

histograms = {}
histogram_total = df[cutName+"/"+variableName+"/histo_top"].to_hist()*0.0

for plotName in plot_cfg.keys():
    
    histograms[plotName] = df[cutName+"/"+variableName+"/histo_top"].to_hist()*0.0
    
    for sampleName in plot_cfg[plotName]["samples"]:
        
        histograms[plotName] += df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist()
        histogram_total += df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist()
    
    if "isData" not in plot_cfg[plotName].keys():
        histograms[plotName].plot1d(ax=ax, stack=True, histtype='fill', sort='label', label=plot_cfg[plotName]["nameHR"] + f" [{np.round(histograms[plotName].sum().value, 1)}]", alpha=0.6)
    elif plot_cfg[plotName]["isData"] == 0:
        histograms[plotName].plot1d(ax=ax, stack=True, histtype='fill', sort='label', label=plot_cfg[plotName]["nameHR"] + f" [{np.round(histograms[plotName].sum().value, 1)}]", alpha=0.6)
    elif plot_cfg[plotName]["isData"] == 1:
        histograms[plotName].plot1d(ax=ax, stack=False, histtype='errorbar', color='k', label = "Data" + f" [{np.round(histograms[plotName].sum().value, 1)}]", zorder=10)
    else:
        histograms[plotName].plot1d(ax=ax, stack=True, histtype='fill', sort='label', label=plot_cfg[plotName]["nameHR"] + f" [{np.round(histograms[plotName].sum().value, 1)}]", alpha=0.6)

histogram_total.plot1d(ax=ax, stack=False)
        
ax.set_ylabel("Events")

plt.legend()
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1])
