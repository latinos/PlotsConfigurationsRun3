#!/usr/bin/env python
import ROOT
import uproot
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import mplhep as hep
import os
import sys
from sys import argv
import argparse
import matplotlib.pyplot as plt
import hist
from hist import Hist
import mplhep as hep
from mkShapesRDF.shapeAnalysis.ConfigLib import ConfigLib
import mkShapesRDF.shapeAnalysis.latinos.LatinosUtils as utils
ROOT.gROOT.SetBatch(True)
ROOT.TH1.SetDefaultSumw2(True)
hep.style.use("CMS")


def defaultParser():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument(
        "-c",
        "--onlyCut",
        type=str,
        help="Cut to process",
        required=False,
        default="",
    )
    
    parser.add_argument(
        "-p",
        "--onlyPlot",
        type=str,
        help="Plot style: c, ratio, sig or diff",
        required=False,
        default="c",
    )

    parser.add_argument(
        "-o",
        "--outDir",
        type=str,
        help="Output directory",
        required=False,
        default=f"./plots/",
    )

    parser.add_argument(
        "-i",
        "--inFile",
        type=str,
        help="Input file",
        required=False,
        default="",
    )

    return parser


def makePlots(samples, variables, nuisance, plot, cuts, lumi, onlyCut=[], plotStyle="c", inFile="", outDir=""):
    
    plotCuts = onlyCut if len(onlyCut)>0 else cuts
    

    print("======================================")
    print("   ")
    print("   ")
    print("        MAKE PLOTS (CAT STYLE)")
    print("   ")
    print("   ") 
    print("======================================")

    print("\n")
    print("Input file: " + inFile)
    df = uproot.open(inFile)

    plot_cfg = plot["groupPlot"]
    plot_cfg["DATA"] = plot["plot"]["DATA"]
    plot = plot["plot"]

    for cutName in plotCuts:
        
        print("------------- " + cutName + " -------------")
        
        for variableName in variables:
            
            print(variableName)

            fig, ax = plt.subplots()
            hep.cms.label("Preliminary", ax=ax, data=True, loc=0)
            hep.cms.lumitext(str(lumi)+" $fb^{-1}$               ", ax=ax)
            
            histograms = {}
            histogram_bkg = []
            histogram_stat = []

            histogram_sig = {}
            
            dummy_key = df[cutName+"/"+variableName].keys()[0]
            
            histogram_total = df[cutName+"/"+variableName+"/"+dummy_key].to_hist()*0.0
            histogram_totalBkg = df[cutName+"/"+variableName+"/"+dummy_key].to_hist()*0.0
            histogram_data = df[cutName+"/"+variableName+"/"+dummy_key].to_hist()*0.0
            
            mynuisances = {}
            nuisanceHistos_up = {}
            nuisanceHistos_do = {}
            nuisance_signal_up = {}
            nuisance_signal_do = {}
            nuisance_bkg_up = {}
            nuisance_bkg_do = {}
            
            labels = []
            colors = []
            signals = []
            backgrounds = []
            
            for plotName in plot_cfg.keys():
                
                histograms[plotName] = df[cutName+"/"+variableName+"/"+dummy_key].to_hist()*0.0
            
                if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"]==1:
                    nuisance_signal_up[plotName] = {}
                    nuisance_signal_do[plotName] = {}
                else:
                    nuisance_bkg_up[plotName] = {}
                    nuisance_bkg_do[plotName] = {}
                
                if "samples" in plot_cfg[plotName].keys():

                    for sampleName in plot_cfg[plotName]["samples"]:

                        scale = 1.0
                        if "scale" in plot[sampleName].keys():
                            scale = plot[sampleName]["scale"]
                        
                        if "cuts" in plot[sampleName].keys() and cutName in plot[sampleName]["cuts"]:
                            scale = float(plot[sampleName]["cuts"][cutName])                            
                            
                        histograms[plotName] += df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                        if "DATA" in sampleName:
                            continue
            
                        histogram_total += df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                        if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"]==0:
                            histogram_totalBkg += df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                            
                        #### Do nuisances chain -------
                        for nuisanceName, nuisance in nuisances.items():
                            
                            if nuisanceName not in nuisanceHistos_up.keys():
                                nuisanceHistos_up[nuisanceName] = df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * 0.0
                                nuisanceHistos_do[nuisanceName] = df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * 0.0
            
                            if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"]==1:
                                if nuisanceName not in nuisance_signal_up[plotName]:
                                    nuisance_signal_up[plotName][nuisanceName] = df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * 0.0
                                    nuisance_signal_do[plotName][nuisanceName] = df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * 0.0
                            else:
                                if nuisanceName not in nuisance_bkg_up[plotName]:
                                    nuisance_bkg_up[plotName][nuisanceName] = df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * 0.0
                                    nuisance_bkg_do[plotName][nuisanceName] = df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * 0.0
            
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
            
                                nuisanceHistos_up[nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * variations[0] * scale
                                nuisanceHistos_do[nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * variations[1] * scale
            
                                if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"]==1:
                                    nuisance_signal_up[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * variations[0] * scale
                                    nuisance_signal_do[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * variations[1] * scale
                                else:
                                    nuisance_bkg_up[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * variations[0] * scale
                                    nuisance_bkg_do[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * variations[1] * scale
            
                            else:
                                if "samples" in nuisance:
                                    if sampleName not in nuisance["samples"]:
                                        nuisanceHistos_up[nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                        nuisanceHistos_do[nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                        if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"]==1:
                                            nuisance_signal_up[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                            nuisance_signal_do[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                        else:
                                            nuisance_bkg_up[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                            nuisance_bkg_do[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName].to_hist() * scale
                                    else:
                                        if "name" in nuisance:
                                            nuisanceHistos_up[nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Up"].to_hist() * scale
                                            nuisanceHistos_do[nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Down"].to_hist() * scale
                                            if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"]==1:
                                                nuisance_signal_up[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Up"].to_hist() * scale
                                                nuisance_signal_do[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Down"].to_hist() * scale
                                            else:
                                                nuisance_bkg_up[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Up"].to_hist() * scale
                                                nuisance_bkg_do[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Down"].to_hist() * scale
                                        else:
                                            nuisanceHistos_up[nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Up"].to_hist() * scale
                                            nuisanceHistos_do[nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Down"].to_hist() * scale
                                            if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"]==1:
                                                nuisance_signal_up[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Up"].to_hist() * scale
                                                nuisance_signal_do[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Down"].to_hist() * scale
                                            else:
                                                nuisance_bkg_up[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Up"].to_hist() * scale
                                                nuisance_bkg_do[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Down"].to_hist() * scale
                                else:
                                    if "name" in nuisance:
                                        nuisanceHistos_up[nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Up"].to_hist() * scale
                                        nuisanceHistos_do[nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Down"].to_hist() * scale
                                        if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"]==1:
                                            nuisance_signal_up[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Up"].to_hist() * scale
                                            nuisance_signal_do[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Down"].to_hist() * scale
                                        else:
                                            nuisance_bkg_up[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Up"].to_hist() * scale
                                            nuisance_bkg_do[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisance["name"]+"Down"].to_hist() * scale
                                    else:
                                        nuisanceHistos_up[nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Up"].to_hist() * scale
                                        nuisanceHistos_do[nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Down"].to_hist() * scale
                                        if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"]==1:
                                            nuisance_signal_up[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Up"].to_hist() * scale
                                            nuisance_signal_do[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Down"].to_hist() * scale
                                        else:
                                            nuisance_bkg_up[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Up"].to_hist() * scale
                                            nuisance_bkg_do[plotName][nuisanceName] += df[cutName+"/"+variableName+"/histo_"+sampleName+ "_"+nuisanceName+"Down"].to_hist() * scale
            
                                
                #### End of nuisance chain ------
                
                elif "DATA" == plotName:
                    histograms[plotName] += df[cutName+"/"+variableName+"/histo_DATA"].to_hist()
                
                if "DATA" not in plotName:
                    histogram_stat.append(histograms[plotName])
                    if "isSignal" in plot_cfg[plotName] and plot_cfg[plotName]["isSignal"]==1:
                        signals.append(plotName)
                    else:
                        histogram_bkg.append(histograms[plotName])
                        backgrounds.append(plotName)
                        labels.append(plot_cfg[plotName]["nameHR"] + f" [{np.round(histograms[plotName].sum().value, 1)}]")
                        colors.append(plot_cfg[plotName]["colorPlt"])

            past_signals = [] # stack signals
            for signal in signals:
                histogram_sig[signal] = histogram_totalBkg + histograms[signal]
                for past_sig in past_signals:
                    histogram_sig[signal] += histograms[past_sig]                    
                past_signals.append(signal)
                
                
            #### Do plot ---------------
            # Bkg ------
            hep.histplot(histogram_bkg, stack=True, histtype='fill', ax=ax, color=colors, label=labels, alpha=0.7)
            # Signal ---
            for signal in signals:
                histogram_sig[signal].plot1d(ax=ax, stack=False, histtype='step', xerr=True, yerr=0.0, color=plot_cfg[signal]["colorPlt"], label=plot_cfg[signal]["nameHR"] + f" [{np.round(histograms[signal].sum().value, 1)}]")

            # Data -----
            data_var_up = histograms["DATA"].variances() * 0.0
            data_var_do = histograms["DATA"].variances() * 0.0
            for i in range(len(data_var_up)):
                data_var_up[i] = GetPoissError(histograms["DATA"].values()[i], 0, 1)
                data_var_do[i] = GetPoissError(histograms["DATA"].values()[i], 1, 0)
                
            if plot_cfg["DATA"]["isBlind"]==1:
                (histograms["DATA"]*0.0).plot1d(ax=ax, stack=False, histtype='errorbar', xerr=True, yerr=0.0, color='k', label = "Data", zorder=10)
            else:
                histograms["DATA"].plot1d(ax=ax, stack=False, histtype='errorbar', xerr=True, yerr=[data_var_do,data_var_up], color='k', label = "Data", zorder=10)
                
            nuisances_err2_up = histogram_total.variances() * 0.0
            nuisances_err2_do = histogram_total.variances() * 0.0
            for histo in histogram_stat:
                nuisances_err2_up += histo.variances()
                nuisances_err2_do += histo.variances()


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

                art = plt.Rectangle([x_low, nominal-var_do], abs(x_high-x_low), (var_up+var_do), linewidth=0, fill=None, hatch='///', edgecolor="dimgray")
                ax.add_artist(art)

                
            y_top = np.max([np.max(histograms["DATA"].values()), np.max(histogram_total.values())])
            if y_top == 0.0:
                y_top = 1.0
            ax.set_ylim([0, 2.5*y_top])
            
            ax.set_xlim(histograms["DATA"].axes.edges[0][0], histograms["DATA"].axes.edges[0][-1])
            
            ax.set_ylabel("Events")
            
            if plotStyle == "c":
                
                ax.set_xlabel(variables[variableName]["xaxis"])
                plt.savefig(outDir+"/c_"+cutName+"_"+variableName+".png")
                print("Info: png file "+ outDir+"/c_"+cutName+"_"+variableName+".png has been created \n")

                ax.set_ylim([0.1, 10000*y_top])
                ax.set_yscale("log")

                plt.savefig(outDir+"/log_c_"+cutName+"_"+variableName+".png")
                print("Info: png file "+ outDir+"/log_c_"+cutName+"_"+variableName+".png has been created \n")

            elif plotStyle == "diff":

                ax.set_xlabel("")

                handles, labels = ax.get_legend_handles_labels()
                ax.legend(handles[::-1], labels[::-1], ncols=2, fontsize="x-small", loc="upper center")

                #### Ratio Canvas ------
                xticks = ax.get_xticks()
                ax.tick_params(axis='x',which='both',bottom=False,top=False,labelbottom=False)

                yhax = hep.append_axes(ax=ax, size=1.5, pad=0.3, position="bottom")
                yhax.set_xlim(histograms["DATA"].axes.edges[0][0], histograms["DATA"].axes.edges[0][-1])
                #yhax.set_xticks(xticks)
                yhax.set_xlabel(variables[variableName]["xaxis"])
                yhax.set_ylabel("Signal", loc="center")

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

                plt.savefig(outDir+"/cDiff_"+cutName+"_"+variableName+".png")
                print("Info: png file "+ outDir+"/cDiff_"+cutName+"_"+variableName+".png has been created \n")

                ax.set_ylim([0.1, 10000*y_top])
                ax.set_yscale("log")

                plt.savefig(outDir+"/log_cDiff_"+cutName+"_"+variableName+".png")
                print("Info: png file "+ outDir+"/log_cDiff_"+cutName+"_"+variableName+".png has been created \n")
                
            elif plotStyle == "sig":                
            
                ax.set_xlabel("")
                
                handles, labels = ax.get_legend_handles_labels()
                ax.legend(handles[::-1], labels[::-1], ncols=2, fontsize="x-small", loc="upper center")
                
                #### Ratio Canvas ------
                
                xticks = ax.get_xticks()
                ax.tick_params(axis='x',which='both',bottom=False,top=False,labelbottom=False)
                
                yhax = hep.append_axes(ax=ax, size=1.5, pad=0.3, position="bottom")
                yhax.set_xlim(histograms["DATA"].axes.edges[0][0], histograms["DATA"].axes.edges[0][-1])
                #yhax.set_xticks(xticks)
                yhax.set_xlabel(variables[variableName]["xaxis"])
                yhax.set_ylabel("Signal", loc="center")
                

                nuisances_err2_up = histogram_total.variances() * 0.0
                nuisances_err2_do = histogram_total.variances() * 0.0
                for histName in backgrounds:
                    nuisances_err2_up += histograms[histName].variances()
                    nuisances_err2_do += histograms[histName].variances()

                    for nuisanceName in mynuisances.keys():

                        up = nuisance_bkg_up[histName][nuisanceName].values()
                        do = nuisance_bkg_do[histName][nuisanceName].values()

                        up_is_up = up > histograms[histName].values()

                        dup2 = np.square(up - histograms[histName].values())
                        ddo2 = np.square(do - histograms[histName].values())
                        nuisances_err2_up += np.where(up_is_up, dup2, ddo2)
                        nuisances_err2_do += np.where(up_is_up, ddo2, dup2)

                nuisances_err_up = np.sqrt(nuisances_err2_up)
                nuisances_err_do = np.sqrt(nuisances_err2_do)

                for i in range(len(histogram_total.values())):

                    nominal = 0.0
                    if histogram_totalBkg.values()[i] != 0.0:
                        var_up = nuisances_err_up[i]
                        var_do = nuisances_err_do[i]
                    else:
                        var_up = 0.0
                        var_do = 0.0
                    
                    x_center = histogram_total.axes.centers[0][i]
                    x_low = histogram_total.axes.edges[0][i]
                    x_high = histogram_total.axes.edges[0][i+1]

                    art = plt.Rectangle([x_low, nominal-var_do], abs(x_high-x_low), (var_up+var_do), linewidth=0, fill=None, hatch='///', edgecolor="dimgray")
                    yhax.add_artist(art)
                
                ymax = 0.0                
                past_signals = histogram_total * 0.0
                for signal in signals:
                    
                    if ymax < np.max((past_signals+histograms[signal]).values()):
                        ymax = np.max((past_signals+histograms[signal]).values())

                    nuisances_err2_up = histograms[signal].variances()
                    nuisances_err2_do = histograms[signal].variances()

                    (past_signals+histograms[signal]).plot1d(ax=yhax, histtype='step', color=plot_cfg[signal]["colorPlt"], yerr=0.0)

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

                        nominal = (past_signals+histograms[signal]).values()[i]
                        var_up = nuisances_err_up[i]
                        var_do = nuisances_err_do[i]

                        x_center = histograms[signal].axes.centers[0][i]
                        x_low = histograms[signal].axes.edges[0][i]
                        x_high = histograms[signal].axes.edges[0][i+1]

                        art = plt.Rectangle([x_low, nominal-var_do], abs(x_high-x_low), (var_up+var_do), alpha=0.3, facecolor=plot_cfg[signal]["colorPlt"], color=None)
                        yhax.add_artist(art)

                    past_signals += histograms[signal]
                
                yhax.set_ylim([0.0, 1.3*ymax])
                        
                plt.savefig(outDir+"/cSig_"+cutName+"_"+variableName+".png")
                print("Info: png file "+ outDir+"/cSig_"+cutName+"_"+variableName+".png has been created \n")

                ax.set_ylim([0.1, 10000*y_top])
                ax.set_yscale("log")

                plt.savefig(outDir+"/log_cSig_"+cutName+"_"+variableName+".png")
                print("Info: png file "+ outDir+"/log_cSig_"+cutName+"_"+variableName+".png has been created \n")
                
            elif plotStyle == "ratio":
                
                ax.set_xlabel("")
                
                handles, labels = ax.get_legend_handles_labels()
                ax.legend(handles[::-1], labels[::-1], ncols=2, fontsize="x-small", loc="upper center")
                
                #### Ratio Canvas ------
                
                xticks = ax.get_xticks()
                ax.tick_params(axis='x',which='both',bottom=False,top=False,labelbottom=False)
                
                yhax = hep.append_axes(ax=ax, size=1.5, pad=0.3, position="bottom")
                yhax.set_xlim(histograms["DATA"].axes.edges[0][0], histograms["DATA"].axes.edges[0][-1])
                #yhax.set_xticks(xticks) ### Buggy
                yhax.set_xlabel(variables[variableName]["xaxis"])
                yhax.set_ylabel("Data/Expected", loc="center")

                thData_ratio = Hist(histograms["DATA"].axes[0])
                ratio_var_up = histograms["DATA"].variances() * 0.0
                ratio_var_do = histograms["DATA"].variances() * 0.0

                for i in range(len(ratio_var_up)):
                    if histogram_total.values()[i]>0.0:
                        ratio = histograms["DATA"].values()[i] / histogram_total.values()[i]
                        
                        var_up = data_var_up[i] / histogram_total.values()[i]
                        var_do = data_var_do[i] / histogram_total.values()[i]
                    else:
                        ratio = 0.0
                        var_up = 0.0
                        var_do = 0.0
                    
                    thData_ratio[i] = ratio
                    ratio_var_up[i] = var_up
                    ratio_var_do[i] = var_do
                    
                if plot_cfg["DATA"]["isBlind"]==0:
                    thData_ratio.plot1d(ax=yhax, stack=False, histtype='errorbar', xerr=True, yerr=[ratio_var_do, ratio_var_up], color='k', label = "Data", zorder=10)
                                
                nuisances_err2_up = histogram_total.variances() * 0.0
                nuisances_err2_do = histogram_total.variances() * 0.0
                for histo in histogram_bkg:
                    nuisances_err2_up += histo.variances()
                    nuisances_err2_do += histo.variances()

                for nuisanceName in mynuisances.keys():

                    up = nuisanceHistos_up[nuisanceName].values()
                    do = nuisanceHistos_do[nuisanceName].values()

                    up_is_up = up > histogram_total.values()

                    dup2 = np.square(up - histogram_total.values())
                    ddo2 = np.square(do - histogram_total.values())
                    nuisances_err2_up += np.where(up_is_up, dup2, ddo2)
                    nuisances_err2_do += np.where(up_is_up, ddo2, dup2)

                for i in range(len(histogram_total.values())):

                    nominal = 1.0
                    if histogram_total.values()[i] != 0.0:
                        var_up = np.sqrt(nuisances_err2_up[i]) / histogram_total.values()[i]
                        var_do = np.sqrt(nuisances_err2_do[i]) / histogram_total.values()[i]
                    else:
                        var_up = 0.0
                        var_do = 0.0

                    x_center = histogram_total.axes.centers[0][i]
                    x_low = histogram_total.axes.edges[0][i]
                    x_high = histogram_total.axes.edges[0][i+1]

                    art = plt.Rectangle([x_low, nominal-var_do], abs(x_high-x_low), (var_up+var_do), linewidth=0, fill=None, hatch='///', edgecolor="dimgray")
                    yhax.add_artist(art)
            
                yhax.set_ylim([0.5, 1.5])
                yhax.plot([histograms["DATA"].axes.edges[0][0], histograms["DATA"].axes.edges[0][-1]], [1, 1], color='k', linewidth=2, linestyle=':')
                        
                plt.savefig(outDir+"/cratio_"+cutName+"_"+variableName+".png")
                print("Info: png file "+ outDir+"/cratio_"+cutName+"_"+variableName+".png has been created \n")

                ax.set_ylim([0.1, 10000*y_top])
                ax.set_yscale("log")

                plt.savefig(outDir+"/log_cratio_"+cutName+"_"+variableName+".png")
                print("Info: png file "+ outDir+"/log_cratio_"+cutName+"_"+variableName+".png has been created \n")

                
            #### Close figure
            plt.clf()
            plt.close(fig)
            
            
def GetPoissError(numberEvents, down, up):
        alpha = 1 - 0.6827
        L = 0
        if numberEvents != 0:
            L = ROOT.Math.gamma_quantile(alpha / 2, numberEvents, 1.0)
        U = 0
        if numberEvents == 0:
            #
            # Poisson error agreed in the CMS statistics committee
            # see: https://hypernews.cern.ch/HyperNews/CMS/get/statistics/263.html
            # and https://hypernews.cern.ch/HyperNews/CMS/get/HIG-16-042/32/1/1/1/1/1.html
            # and https://twiki.cern.ch/twiki/bin/viewauth/CMS/PoissonErrorBars
            # to avoid flip-flop.
            # The commented version would have created 1.147 for 0 observed events
            # while now we get 1.84 in the case of 0 observed events
            #
            U = ROOT.Math.gamma_quantile_c(alpha / 2, numberEvents + 1, 1.0)
            # U = ROOT.Math.gamma_quantile_c (alpha,numberEvents+1,1.)
            # print("u = ", U)
        else:
            U = ROOT.Math.gamma_quantile_c(alpha / 2, numberEvents + 1, 1.0)

        # the error
        L = numberEvents - L
        if numberEvents > 0:
            U = U - numberEvents
        # else :
        # U = 1.14 # --> bayesian interval Poisson with 0 events observed
        # 1.14790758039 from 10 lines above

        if up and not down:
            return U
        if down and not up:
            return L
        if up and down:
            return (L, U)
                
                
def main():
    
    parser = defaultParser()
    args = parser.parse_args()

    global cuts, plot
    configsFolder = "configs"
    ConfigLib.loadLatestPickle(os.path.abspath(configsFolder), globals())
    print(dir())
    print(globals().keys())
    cuts = cuts["cuts"]
    subsamplesmap = utils.flatten_samples(samples)
    categoriesmap = utils.flatten_cuts(cuts)
    
    onlyCut = args.onlyCut
    onlyPlot = args.onlyPlot
    outDir = args.outDir
    inFile = args.inFile
    
    if onlyPlot not in ["c", "ratio", "diff"]:
        print("Error: The only allowed plot styles are 'c', 'ratio', or 'diff' ")
        
    cuts_to_plot = []
    for cutName in cuts:
        if onlyCut in cutName:
            cuts_to_plot.append(cutName)
            
    if inFile == "":
        fileName = outputFolder + "/" + outputFile 
    else:
        fileName = inFile
            
    makePlots(samples, variables, nuisances, plot, cuts, lumi, onlyCut=cuts_to_plot, plotStyle=onlyPlot, inFile=fileName, outDir=outDir)
    

if __name__ == '__main__':
    main()
    print("DONE!")

