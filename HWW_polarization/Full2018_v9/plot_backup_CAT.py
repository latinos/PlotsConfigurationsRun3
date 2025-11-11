#!/usr/bin/env pytho
import ROOT
import uproot
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import mplhep as hep
import os
import sys
import matplotlib.pyplot as plt
import mplhep as hep
from mkShapesRDF.shapeAnalysis.ConfigLib import ConfigLib
import mkShapesRDF.shapeAnalysis.latinos.LatinosUtils as utils
ROOT.gROOT.SetBatch(True)
ROOT.TH1.SetDefaultSumw2(True)
hep.style.use("CMS")
global cuts, plot
configsFolder = "configs"
ConfigLib.loadLatestPickle(os.path.abspath(configsFolder), globals())
print(dir())
print(globals().keys())
cuts = cuts["cuts"]
subsamplesmap = utils.flatten_samples(samples)
categoriesmap = utils.flatten_cuts(cuts)

#inputFile = outputFolder + "/" + outputFile
fileName = "/eos/user/s/sblancof/MC/rootFiles/mkShapes__WW_2018_complete.root"

cutName = "hww2l2v_13TeV_top_0j"
variableName = 'dphill'

plot_cfg = plot["groupPlot"]
plot_cfg["DATA"] = plot["plot"]["DATA"]

print("======================================")
print("   ")
print("   ")
print("        MAKE PLOTS (CAT STYLE)")
print("   ")
print("   ") 
print("======================================")


df = uproot.open(fileName)

fig, ax = plt.subplots()
hep.cms.label("Preliminary", ax=ax, data=True, loc=0)
hep.cms.lumitext(legend["lumi"]+" $fb^{-1}$               ", ax=ax)

histograms = {}
histogram_bkg = []
histogram_total = df[cutName+"/"+variableName+"/histo_top"].to_hist()*0.0
histogram_data = df[cutName+"/"+variableName+"/histo_top"].to_hist()*0.0

mynuisances = {}
nuisanceHistos_up = {}
nuisanceHistos_do = {}
nuisance_signal_up = {}
nuisance_signal_do = {}

labels = []
colors = []
signals = []

for plotName in plot_cfg.keys():

    print(plotName)
    
    histograms[plotName] = df[cutName+"/"+variableName+"/histo_top"].to_hist()*0.0

    if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"]==1:
        nuisance_signal_up[plotName] = {}
        nuisance_signal_do[plotName] = {}
    
    if "samples" in plot_cfg[plotName].keys():
        print("----")
        for sampleName in plot_cfg[plotName]["samples"]:

            print(sampleName)
            
            histograms[plotName] += df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist()
            if "DATA" in sampleName:
                continue

            histogram_total += df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist()
                
            #### Do nuisances chain -------
            for nuisanceName, nuisance in nuisances.items():
                
                if nuisanceName not in nuisanceHistos_up.keys():
                    nuisanceHistos_up[nuisanceName] = df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * 0.0
                    nuisanceHistos_do[nuisanceName] = df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * 0.0

                if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"]==1:
                    if nuisanceName not in nuisance_signal_up[plotName]:
                        nuisance_signal_up[plotName][nuisanceName] = df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * 0.0
                        nuisance_signal_do[plotName][nuisanceName] = df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * 0.0

                if "cuts" in nuisance and cutName not in nuisance["cuts"]:
                    continue

                if "stat" in nuisanceName:
                    continue

                if "type" in nuisance.keys() and (nuisance["type"] == "rateParam" or nuisance["type"] == "lnU"):
                    continue
                else:
                    mynuisances[nuisanceName] = nuisances[nuisanceName]
                    
                if "type" in nuisance and nuisance["type"] == "lnN":
                    
                    if "samples" in nuisance:
                        if sampleName not in nuisance["samples"]:
                            values = "1.0"
                        else:
                            values = nuisance["samples"][sampleName]
                    else:
                        values = nuisance["value"]

                    if "/" in values:
                        variations = (float(values.split("/")[0]),float(values.split("/")[1]))
                    else:
                        variations = (float(values), 2.0 - float(values))

                    nuisanceHistos_up[nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * variations[0]
                    nuisanceHistos_do[nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * variations[1]

                    if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"]==1:
                        nuisance_signal_up[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * variations[0]
                        nuisance_signal_do[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * variations[1]

                else:
                    if "samples" in nuisance:
                        if sampleName not in nuisance["samples"]:
                            nuisanceHistos_up[nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist()
                            nuisanceHistos_do[nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist()
                            if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"]==1:
                                nuisance_signal_up[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist()
                                nuisance_signal_do[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist()
                        else:
                            if "name" in nuisance:
                                nuisanceHistos_up[nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Up"].to_hist()
                                nuisanceHistos_do[nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Down"].to_hist()
                                if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"]==1:
                                    nuisance_signal_up[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Up"].to_hist()
                                    nuisance_signal_do[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Down"].to_hist()
                            else:
                                nuisanceHistos_up[nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Up"].to_hist()
                                nuisanceHistos_do[nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Down"].to_hist()
                                if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"]==1:
                                    nuisance_signal_up[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Up"].to_hist()
                                    nuisance_signal_do[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Down"].to_hist()
                    else:
                        if "name" in nuisance:
                            nuisanceHistos_up[nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Up"].to_hist()
                            nuisanceHistos_do[nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Down"].to_hist()
                            if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"]==1:
                                nuisance_signal_up[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Up"].to_hist()
                                nuisance_signal_do[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Down"].to_hist()
                        else:
                            nuisanceHistos_up[nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Up"].to_hist()
                            nuisanceHistos_do[nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Down"].to_hist()
                            if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"]==1:
                                nuisance_signal_up[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Up"].to_hist()
                                nuisance_signal_do[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Down"].to_hist()

                    
    #### End of nuisance chain ------
                        
    elif "DATA" == plotName:
        histograms[plotName] += df[cutName+"/"+variableName+"/histo_DATA"].to_hist()

    if "DATA" not in plotName:
        labels.append(plot_cfg[plotName]["nameHR"] + f" [{np.round(histograms[plotName].sum().value, 1)}]")
        colors.append(plot_cfg[plotName]["colorPlt"])
        histogram_bkg.append(histograms[plotName])
        
    if plot_cfg[plotName]["isSignal"] == 1:
        signals.append(plotName)



#### Do plot
        
hep.histplot(histogram_bkg, stack=True, histtype='fill', ax=ax, color=colors, label=labels, alpha=0.7)
if plot_cfg["DATA"]["isBlind"]==1:
    (histograms["DATA"]*0.0).plot1d(ax=ax, stack=False, histtype='errorbar', xerr=True, yerr=None, color='k', label = "Data", zorder=10)
else:
    histograms["DATA"].plot1d(ax=ax, stack=False, histtype='errorbar', xerr=True, color='k', label = "Data", zorder=10)
    
nuisances_err2_up = histogram_total.variances()
nuisances_err2_do = histogram_total.variances()

for nuisanceName in mynuisances.keys():    

    up = nuisanceHistos_up[nuisanceName].values()
    do = nuisanceHistos_do[nuisanceName].values()
    
    up_is_up = up > histogram_total.values()
    
    dup2 = np.square(up - histogram_total.values())
    ddo2 = np.square(do - histogram_total.values())
    nuisances_err2_up += np.where(up_is_up, dup2, ddo2)
    nuisances_err2_do += np.where(up_is_up, ddo2, dup2)
    
nuisances_err_up = np.sqrt(nuisances_err2_up)
nuisances_err_do = np.sqrt(nuisances_err2_do)

for i in range(len(histogram_total.values())):
    
    nominal = histogram_total.values()[i]
    var_up = nuisances_err_up[i]
    var_do = nuisances_err_do[i]
        
    x_center = histogram_total.axes.centers[0][i]
    x_low = histogram_total.axes.edges[0][i]
    x_high = histogram_total.axes.edges[0][i+1]
    
    art = plt.Rectangle([x_low, nominal-var_do], abs(x_high-x_low), (var_up+var_do), alpha=0.3, facecolor="grey", color=None)
    ax.add_artist(art)

    
ax.set_ylim([0, 2.8*np.max(histograms["DATA"].values())])
ax.set_xlim(histograms["DATA"].axes.edges[0][0], histograms["DATA"].axes.edges[0][-1])

ax.set_ylabel("Events")
ax.set_xlabel("")

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles[::-1], labels[::-1], ncols=2, fontsize="x-small", loc="upper center")

#### Ratio Canvas ------

xticks = ax.get_xticks()
ax.tick_params(axis='x',which='both',bottom=False,top=False,labelbottom=False)

yhax = hep.append_axes(ax=ax, size=1.5, pad=0.1, position="bottom")
yhax.set_xlim(histograms["DATA"].axes.edges[0][0], histograms["DATA"].axes.edges[0][-1])
yhax.set_xticks(xticks)
yhax.set_xlabel(variableName)

ymax = 0.0

for signal in signals:
    
    if ymax < np.max(histograms[signal].values()):
        ymax = np.max(histograms[signal].values())
    
    histograms[signal].plot1d(ax=yhax, histtype='step', color=plot_cfg[signal]["colorPlt"], yerr=0.0)

    nuisances_err2_up = histograms[signal].variances()
    nuisances_err2_do = histograms[signal].variances()

    for nuisanceName in mynuisances.keys():
        
        up = nuisance_signal_up[signal][nuisanceName].values()
        do = nuisance_signal_do[signal][nuisanceName].values()
        
        up_is_up = up > histograms[signal].values()
        
        dup2 = np.square(up - histograms[signal].values())
        ddo2 = np.square(do - histograms[signal].values())
        nuisances_err2_up += np.where(up_is_up, dup2, ddo2)
        nuisances_err2_do += np.where(up_is_up, ddo2, dup2)
        
    nuisances_err_up = np.sqrt(nuisances_err2_up)
    nuisances_err_do = np.sqrt(nuisances_err2_do)


    for i in range(len(histograms[signal].values())):
    
        nominal = histograms[signal].values()[i]
        var_up = nuisances_err_up[i]
        var_do = nuisances_err_do[i]
        
        x_center = histograms[signal].axes.centers[0][i]
        x_low = histograms[signal].axes.edges[0][i]
        x_high = histograms[signal].axes.edges[0][i+1]
        
        art = plt.Rectangle([x_low, nominal-var_do], abs(x_high-x_low), (var_up+var_do), alpha=0.3, facecolor=plot_cfg[signal]["colorPlt"], color=None)
        yhax.add_artist(art)    

yhax.set_ylim([0.0, 1.3*ymax])
        

plt.savefig("/eos/user/s/sblancof/www/HiggsHelicity/RunII_UL/2018/CATPlots/c_"+cutName+"_"+variableName+".png")
