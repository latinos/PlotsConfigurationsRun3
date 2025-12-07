#!/usr/bin/env python
import sys

import ROOT

import argparse
import collections
import os.path
import shutil
from textwrap import dedent


ROOT.gROOT.SetBatch(True)

argv = sys.argv
sys.argv = argv[:1]


# ----------------------------------------------------- DatacardFactory --------------------------------------


class DatacardFactory:
    # _logger = logging.getLogger('DatacardFactory')

    # _____________________________________________________________________________
    def __init__(self):
        self._fileIn = None
        self._skipMissingNuisance = False
        self.onlyVariables = None
        self.onlyCuts = None

    # _____________________________________________________________________________
    # a datacard for each "cut" and each "variable" will be produced, in separate sub-folders, names after "cut/variable"
    # _____________________________________________________________________________
    def makeDatacards(
        self,
        inputFile,
        outputDirDatacard,
        variables,
        cuts,
        samples,
        structureFile,
        nuisances,
    ):
        print("=======================")
        print("==== makeDatacards ====")
        print("=======================")

        print("\n")
        print(inputFile)

        if os.path.isdir(inputFile):
            # ONLY COMPATIBLE WITH OUTPUTS MERGED TO SAMPLE LEVEL!!
            self._fileIn = {}
            for sampleName in samples:
                self._fileIn[sampleName] = ROOT.TFile.Open(
                    inputFile + "/plots_%s_ALL_%s.root" % (self._tag, sampleName)
                )
                if not self._fileIn[sampleName]:
                    raise RuntimeError(
                        "Input file for sample " + sampleName + " missing"
                    )
        #else:
        #    self._fileIn = ROOT.TFile(inputFile, "READ")
        #    ROOT.gROOT.GetListOfFiles().Remove(self._fileIn)  # Speed up

        # categorize the sample names
        signal_ids = (
            collections.OrderedDict()
        )  # id map of alternative_signals + cumulative_signals
        alternative_signals = {
            0: [""],
        }
        cumulative_signals = []
        data = []
        background_ids = collections.OrderedDict()

        # divide the list of samples among signal, background and data
        isig = 0
        ibkg = 1
        for sampleName in samples:
            if sampleName not in list(structureFile.keys()):
                print("Sample", sampleName, "is not included in structure file")
                continue
            if structureFile[sampleName]["isSignal"] != 0:
                signal_ids[sampleName] = isig
                isig -= 1
            if structureFile[sampleName]["isSignal"] >= 2:
                if structureFile[sampleName]["isSignal"] not in alternative_signals.keys():
                    alternative_signals[structureFile[sampleName]["isSignal"]] = []                    
                alternative_signals[structureFile[sampleName]["isSignal"]].append(sampleName)
            if structureFile[sampleName]["isSignal"] == 1:
                cumulative_signals.append(sampleName)
            if structureFile[sampleName]["isData"] == 1:
                data.append(sampleName)
            if (
                structureFile[sampleName]["isSignal"] == 0
                and structureFile[sampleName]["isData"] == 0
            ):
                background_ids[sampleName] = ibkg
                ibkg += 1

        print("Number of Signals:             " + str(len(signal_ids)))
        print("Number of Alternative Signals: " + str(len(alternative_signals.keys()) - 1))
        print("Number of Cumulative Signals:  " + str(len(cumulative_signals)))
        print("Number of Backgrounds:         " + str(len(background_ids)))

        if not os.path.isdir(outputDirDatacard + "/"):
            os.makedirs(outputDirDatacard + "/")

        # loop over cuts. One directory per cut will be created
        for cutName in cuts:
            if self.onlyCuts and cutName not in self.onlyCuts:
                continue
            print("cut = ", cutName)
            try:
                shutil.rmtree(outputDirDatacard + "/" + cutName)
            except OSError:
                pass
            os.makedirs(outputDirDatacard + "/" + cutName)

            #
            # prepare the signals and background list of samples
            # after removing the ones not to be used in this specific phase space
            #
            cut_signals = []
            cut_backgrounds = []
            for snameList, idmap in [
                (cut_signals, signal_ids),
                (cut_backgrounds, background_ids),
            ]:
                for sampleName in idmap:
                    if (
                        "removeFromCuts" in structureFile[sampleName]
                        and cutName in structureFile[sampleName]["removeFromCuts"]
                    ):
                        # remove from the list
                        print(" remove ", sampleName, " from ", cutName)
                    else:
                        snameList.append(sampleName)

            print("  sampleNames = ", cut_signals + cut_backgrounds)

            # loop over variables
            for variableName, variable in variables.items():
                if "cuts" in variable and cutName not in variable["cuts"]:
                    continue
                if self.onlyVariables and variableName not in self.onlyVariables:
                    continue

                print("  variableName = ", variableName)
                tagNameToAppearInDatacard = cutName
                # e.g.    hww2l2v_13TeV_of0j
                #         to be defined in cuts.py

                os.makedirs(
                    outputDirDatacard + "/" + cutName + "/" + variableName,
                    exist_ok=True,
                )
                os.makedirs(
                    outputDirDatacard + "/" + cutName + "/" + variableName + "/shapes/",
                    exist_ok=True,
                )  # and the folder for the root files

                #self._outFile = ROOT.TFile.Open(
                #    outputDirDatacard
                #    + "/"
                #    + cutName
                #    + "/"
                #    + variableName
                #    + "/shapes/histos_"
                #    + tagNameToAppearInDatacard
                #    + ".root",
                #    "recreate",
                #)
                #ROOT.gROOT.GetListOfFiles().Remove(self._outFile)

                # prepare yields
                yieldsSig = {}
                yieldsBkg = {}
                yieldsData = {}

                # Bin to be killed
                # killBinSig = {}
                # killBinBkg = {}

                for snameList, yields in [
                    (cut_signals, yieldsSig),
                    (cut_backgrounds, yieldsBkg),
                    (data, yieldsData),
                ]:
                    for sampleName in snameList:

                        self._fileIn = ROOT.TFile(inputFile, "READ")
                        self._outFile = ROOT.TFile.Open(
                            outputDirDatacard
                            + "/"
                            + cutName
                            + "/"
                            + variableName
                            + "/shapes/histos_"
                            + tagNameToAppearInDatacard
                            + ".root",
                            "update",
                        )
                        ROOT.gROOT.GetListOfFiles().Remove(self._fileIn)
                        ROOT.gROOT.GetListOfFiles().Remove(self._outFile)
                        
                        histo = self._getHisto(cutName, variableName, sampleName)
                        histo.SetDirectory(self._outFile)

                        # get the integral == rate from histogram
                        if structureFile[sampleName]["isData"] == 1:
                            yields["data"] = histo.Integral()
                            histo.SetName("histo_Data")
                        else:
                            #                  if 'removeNegNomVal' in structureFile[sampleName] and structureFile[sampleName]['removeNegNomVal'] :
                            #                    for iBin in range(0,histo.GetNbinsX()+2) :
                            #                      BinContent = histo.GetBinContent(iBin)
                            #                      if BinContent < 0.1 and not BinContent == 0:
                            #                        print('Killing Bin :' , sampleName , iBin , BinContent)
                            #                        if not sampleName in killBinSig : killBinSig[sampleName] = []
                            #                        killBinSig[sampleName].append(iBin)
                            #                        histo.SetBinContent(iBin,0.)
                            if "scaleSampleForDatacard" in structure[sampleName]:
                                scaleFactor = 1.0
                                if (
                                    type(
                                        structure[sampleName]["scaleSampleForDatacard"]
                                    )
                                    is dict
                                ):
                                    try:
                                        scaleFactor = structure[sampleName][
                                            "scaleSampleForDatacard"
                                        ][cutName]
                                    except:
                                        pass
                                if (
                                    type(
                                        structure[sampleName]["scaleSampleForDatacard"]
                                    )
                                    is int
                                    or type(
                                        structure[sampleName]["scaleSampleForDatacard"]
                                    )
                                    is float
                                ):
                                    scaleFactor = structure[sampleName][
                                        "scaleSampleForDatacard"
                                    ]
                                histo.Scale(scaleFactor)

                            yields[sampleName] = histo.Integral()

                        #
                        # Remove statistical uncertainty from the histogram
                        # This may be used to suppress the effect on "autoMCstat" of a specific
                        # sample, by means of putting its uncertainty to 0
                        #
                        if (
                            "removeStatUnc" in structureFile[sampleName]
                            and structureFile[sampleName]["removeStatUnc"]
                        ):
                            self._removeStatUncertainty(histo)

                        self._outFile.cd()
                        histo.Write()

                        self._fileIn.Close()
                        self._outFile.Close()

                        del self._fileIn
                        del self._outFile
                        
                # Loop over alternative signal samples. One card per signal (there is always at least one entry (""))
                for signalKey in alternative_signals.keys():
                    
                    self._fileIn = ROOT.TFile(inputFile, "READ")
                    self._outFile = ROOT.TFile.Open(
                        outputDirDatacard
                        + "/"
                        + cutName
                        + "/"
                        + variableName
                        + "/shapes/histos_"
                        + tagNameToAppearInDatacard
                        + ".root",
                        "update",
                    )
                    ROOT.gROOT.GetListOfFiles().Remove(self._fileIn)
                    ROOT.gROOT.GetListOfFiles().Remove(self._outFile)
                    
                    if signalKey == 0:
                        signals = [
                            name for name in cumulative_signals if name in cut_signals
                        ]
                        alternativeSignalName = ""
                    else:
                        signals = [
                            signalName for signalName in alternative_signals[signalKey]
                        ] + [
                            name for name in cumulative_signals if name in cut_signals
                        ]
                        if "ggH" in alternative_signals[signalKey][0]:
                            alternativeSignalName = alternative_signals[signalKey][0].split("ggH_")[-1] 
                        else:
                            alternativeSignalName = alternative_signals[signalKey][0].split("qqH_")[-1]
                            
                    processes = signals + cut_backgrounds

                    print("    Alternative signal: " + str(alternativeSignalName))
                    alternativeSignalTitle = ""
                    if alternativeSignalName != "":
                        alternativeSignalTitle = "_" + str(alternativeSignalName)

                    # start creating the datacard
                    cardPath = (
                        outputDirDatacard
                        + "/"
                        + cutName
                        + "/"
                        + variableName
                        + "/datacard"
                        + alternativeSignalTitle
                        + ".txt"
                    )
                    print("    Writing to " + cardPath)
                    card = open(cardPath, "w")

                    print("      headers..")
                    card.write("## Shape input card\n")

                    card.write("imax 1 number of channels\n")
                    card.write("jmax * number of background\n")
                    card.write("kmax * number of nuisance parameters\n")

                    card.write("-" * 100 + "\n")
                    card.write("bin         %s" % tagNameToAppearInDatacard + "\n")
                    if len(data) == 0:
                        self._logger.warning("no data, no fun! ")
                        # raise RuntimeError('No Data found!')
                        yieldsData["data"] = 0

                    card.write("observation %.0f\n" % yieldsData["data"])

                    card.write(
                        "shapes  *           * "
                        + "shapes/histos_"
                        + tagNameToAppearInDatacard
                        + ".root"
                        + "     histo_$PROCESS histo_$PROCESS_$SYSTEMATIC"
                        + "\n"
                    )

                    card.write(
                        "shapes  data_obs           * "
                        + "shapes/histos_"
                        + tagNameToAppearInDatacard
                        + ".root"
                        + "     histo_Data"
                        + "\n"
                    )

                    #   shapes  *           * shapes/hww-19.36fb.mH125.of_vh2j_shape_mll.root     histo_$PROCESS histo_$PROCESS_$SYSTEMATIC
                    #   shapes  data_obs    * shapes/hww-19.36fb.mH125.of_vh2j_shape_mll.root     histo_Data

                    columndef = 30

                    # adapt column length to long bin names
                    if len(tagNameToAppearInDatacard) >= (columndef - 5):
                        columndef = len(tagNameToAppearInDatacard) + 7

                    for name in signals:
                        if len(name) >= (columndef - 5):
                            columndef = len(name) + 7

                    print("      processes and rates..")

                    card.write("bin".ljust(80))
                    card.write(
                        "".join(
                            [tagNameToAppearInDatacard.ljust(columndef)]
                            * (len(signals) + len(cut_backgrounds))
                        )
                        + "\n"
                    )

                    card.write("process".ljust(80))
                    card.write("".join(name.ljust(columndef) for name in signals))
                    card.write(
                        "".join(name.ljust(columndef) for name in cut_backgrounds)
                    )
                    card.write("\n")

                    card.write("process".ljust(80))
                    card.write(
                        "".join(
                            ("%d" % signal_ids[name]).ljust(columndef)
                            for name in signals
                        )
                    )
                    card.write(
                        "".join(
                            ("%d" % background_ids[name]).ljust(columndef)
                            for name in cut_backgrounds
                        )
                    )
                    card.write("\n")

                    card.write("rate".ljust(80))
                    card.write(
                        "".join(
                            ("%-.4f" % yieldsSig[name]).ljust(columndef)
                            for name in signals
                        )
                    )
                    card.write(
                        "".join(
                            ("%-.4f" % yieldsBkg[name]).ljust(columndef)
                            for name in cut_backgrounds
                        )
                    )
                    card.write("\n")

                    card.write("-" * 100 + "\n")

                    print("      nuisances..")

                    nuisanceGroups = collections.defaultdict(list)

                    # add normalization and shape nuisances
                    for nuisanceName, nuisance in nuisances.items():
                        if "type" not in nuisance:
                            raise RuntimeError(
                                "Nuisance "
                                + nuisanceName
                                + " is missing the type specification"
                            )

                        if nuisanceName == "stat" or nuisance["type"] == "rateParam":
                            # will deal with these later
                            continue

                        # check if a nuisance can be skipped because not in this particular cut
                        if "cuts" in nuisance and cutName not in nuisance["cuts"]:
                            continue

                        if nuisance["type"] in ["lnN", "lnU"]:
                            # why is adding CMS_ not the default for lnN/lnU? (Y.I. 2019.11.06)

                            entryName = nuisance["name"]
                            if (
                                "perRecoBin" in nuisance.keys()
                                and nuisance["perRecoBin"]
                            ):
                                entryName += "_" + cutName

                            card.write(entryName.ljust(80 - 20))

                            if (
                                "AsShape" in nuisance
                                and float(nuisance["AsShape"]) >= 1.0
                            ):
                                print(
                                    ">>>>>",
                                    nuisance["name"],
                                    " was derived as a lnN uncertainty but is being treated as a shape",
                                )
                                card.write(("shape").ljust(20))
                                for sampleName in processes:
                                    if (
                                        "cuts_samples" in nuisance
                                        and sampleName in nuisance["cuts_samples"]
                                        and cutName
                                        not in nuisance["cuts_samples"][sampleName]
                                    ):
                                        # If the cuts_samples options is there and the sample is inserted in the dictionary
                                        # check if the current cutName is included. Excluded the cuts not in the list
                                        print(
                                            "Removing nuisance ",
                                            nuisanceName,
                                            " for sample ",
                                            sampleName,
                                            " from cut ",
                                            cutName,
                                        )
                                        card.write(("-").ljust(columndef))
                                    elif (
                                        "all" in nuisance and nuisance["all"] == 1
                                    ) or (
                                        "samples" in nuisance
                                        and sampleName in nuisance["samples"]
                                    ):
                                        histo = self._getHisto(
                                            cutName, variableName, sampleName
                                        )

                                        histoUp = histo.Clone(
                                            "%s_%sUp"
                                            % (histo.GetName(), nuisance["name"])
                                        )
                                        histoDown = histo.Clone(
                                            "%s_%sDown"
                                            % (histo.GetName(), nuisance["name"])
                                        )
                                        histoUp.SetDirectory(self._outFile)
                                        histoDown.SetDirectory(self._outFile)

                                        if (
                                            "scaleSampleForDatacard"
                                            in structure[sampleName]
                                        ):
                                            scaleFactor = 1.0
                                            if (
                                                type(
                                                    structure[sampleName][
                                                        "scaleSampleForDatacard"
                                                    ]
                                                )
                                                is dict
                                            ):
                                                try:
                                                    scaleFactor = structure[sampleName][
                                                        "scaleSampleForDatacard"
                                                    ][cutName]
                                                except:
                                                    pass
                                            if (
                                                type(
                                                    structure[sampleName][
                                                        "scaleSampleForDatacard"
                                                    ]
                                                )
                                                is int
                                                or type(
                                                    structure[sampleName][
                                                        "scaleSampleForDatacard"
                                                    ]
                                                )
                                                is float
                                            ):
                                                scaleFactor = structure[sampleName][
                                                    "scaleSampleForDatacard"
                                                ]
                                            histoUp.Scale(scaleFactor)
                                            histoDown.Scale(scaleFactor)
                                        if "/" in nuisance["samples"][sampleName]:
                                            up, down = nuisance["samples"][
                                                sampleName
                                            ].split("/")
                                            histoUp.Scale(float(up))
                                            histoDown.Scale(float(down))
                                        else:
                                            histoUp.Scale(
                                                float(nuisance["samples"][sampleName])
                                            )
                                            histoDown.Scale(
                                                1.0
                                                / float(nuisance["samples"][sampleName])
                                            )

                                        self._outFile.cd()
                                        histoUp.Write()
                                        histoDown.Write()

                                        card.write("1.000".ljust(columndef))

                                    else:
                                        card.write(("-").ljust(columndef))

                            else:
                                card.write((nuisance["type"]).ljust(20))
                                if (
                                    "all" in nuisance and nuisance["all"] == 1
                                ):  # for all samples
                                    card.write(
                                        "".join(
                                            ("%-.4f" % nuisance["value"]).ljust(
                                                columndef
                                            )
                                            for _ in processes
                                        )
                                    )
                                else:
                                    # apply only to selected samples
                                    for sampleName in processes:
                                        if sampleName in nuisance["samples"]:
                                            # in this case nuisance['samples'] is a dict mapping sample name to nuisance values in string
                                            card.write(
                                                (
                                                    "%s"
                                                    % nuisance["samples"][sampleName]
                                                ).ljust(columndef)
                                            )
                                        else:
                                            card.write(("-").ljust(columndef))

                        elif nuisance["type"] == "shape":
                            #
                            # 'skipCMS' is a flag not to introduce "CMS" automatically in the name
                            #      of the nuisance.
                            #      It may be needed for combination purposes with ATLAS
                            #      and agreed upon for all CMS analyses.
                            #      For example: theoretical uncertainties on ggH with migration scheme 2017
                            #
                            if "skipCMS" in nuisance and nuisance["skipCMS"] == 1:
                                entryName = nuisance["name"]
                            else:
                                entryName = "CMS_" + nuisance["name"]

                            if (
                                "perRecoBin" in nuisance.keys()
                                and nuisance["perRecoBin"]
                            ):
                                entryName += "_" + cutName

                            card.write(entryName.ljust(80 - 20))

                            if "AsLnN" in nuisance and float(nuisance["AsLnN"]) >= 1.0:
                                print(
                                    ">>>>>",
                                    nuisance["name"],
                                    " was derived as a shape uncertainty but is being treated as a lnN",
                                )
                                card.write(("lnN").ljust(20))
                                for sampleName in processes:
                                    if (
                                        "cuts_samples" in nuisance
                                        and sampleName in nuisance["cuts_samples"]
                                        and cutName
                                        not in nuisance["cuts_samples"][sampleName]
                                    ):
                                        # If the cuts_samples options is there and the sample is inserted in the dictionary
                                        # check if the current cutName is included. Excluded the cuts not in the list
                                        print(
                                            "Removing nuisance ",
                                            nuisanceName,
                                            " for sample ",
                                            sampleName,
                                            " from cut ",
                                            cutName,
                                        )
                                        card.write(("-").ljust(columndef))
                                    elif (
                                        "all" in nuisance and nuisance["all"] == 1
                                    ) or (
                                        "samples" in nuisance
                                        and sampleName in nuisance["samples"]
                                    ):
                                        histo = self._getHisto(
                                            cutName, variableName, sampleName
                                        )
                                        histoUp = self._getHisto(
                                            cutName,
                                            variableName,
                                            sampleName,
                                            "_" + nuisance["name"] + "Up",
                                        )
                                        histoDown = self._getHisto(
                                            cutName,
                                            variableName,
                                            sampleName,
                                            "_" + nuisance["name"] + "Down",
                                        )

                                        if not histoUp or not histoDown:
                                            print(
                                                "Histogram for nuisance",
                                                nuisance["name"],
                                                "on sample",
                                                sampleName,
                                                "missing",
                                            )

                                            if self._skipMissingNuisance:
                                                card.write(("-").ljust(columndef))
                                                continue

                                        histoIntegral = histo.Integral()
                                        histoUpIntegral = histoUp.Integral()
                                        histoDownIntegral = histoDown.Integral()
                                        if (
                                            histoIntegral > 0.0
                                            and histoUpIntegral > 0.0
                                        ):
                                            diffUp = (
                                                (histoUpIntegral - histoIntegral)
                                                / histoIntegral
                                                / float(nuisance["AsLnN"])
                                            )
                                        else:
                                            diffUp = 0.0

                                        if (
                                            histoIntegral > 0.0
                                            and histoDownIntegral > 0.0
                                        ):
                                            diffDo = (
                                                (histoDownIntegral - histoIntegral)
                                                / histoIntegral
                                                / float(nuisance["AsLnN"])
                                            )
                                        else:
                                            diffDo = 0.0
                                        if (
                                            "symmetrize" in nuisance
                                            and nuisance["symmetrize"]
                                        ):
                                            diff = (diffUp - diffDo) * 0.5
                                            if diff >= 1.0:
                                                # can't symmetrize
                                                diffUp = diff * 2.0 - 0.999
                                                diffDo = -0.999
                                            elif diff <= -1.0:
                                                diffUp = -0.999
                                                diffDo = -diff * 2.0 - 0.999
                                            else:
                                                diffUp = diff
                                                diffDo = -diff

                                        lnNUp = 1.0 + diffUp
                                        lnNDo = 1.0 + diffDo

                                        #
                                        # avoid 0.00/XXX and XXX/0.00 in the lnN --> ill defined nuisance
                                        # if this happens put 0.00 ---> 1.00, meaning *no* effect of this nuisance
                                        #              Done like this because it is very likely what you are experiencing
                                        #              is a MC fluctuation in the varied sample, that is the up/down histogram has 0 entries!
                                        #
                                        #              NB: with the requirement "histoUpIntegral > 0" and "histoDownIntegral > 0" this should never happen,
                                        #                  except for some strange coincidence of "AsLnN" ...
                                        #                  This fix is left, just for sake of safety
                                        #
                                        if lnNUp == 0:
                                            lnNUp = 1.0
                                        if lnNDo == 0:
                                            lnNDo = 1.0

                                        if (
                                            abs(lnNUp - 1.0) < 5.0e-4
                                            and abs(lnNDo - 1.0) < 5.0e-4
                                        ):
                                            card.write(("-").ljust(columndef))
                                        else:
                                            card.write(
                                                (
                                                    ("%-.4f" % lnNUp)
                                                    + "/"
                                                    + ("%-.4f" % lnNDo)
                                                ).ljust(columndef)
                                            )
                                    else:
                                        card.write(("-").ljust(columndef))

                            else:
                                card.write("shape".ljust(20))
                                for sampleName in processes:
                                    if (
                                        "cuts_samples" in nuisance
                                        and sampleName in nuisance["cuts_samples"]
                                        and cutName
                                        not in nuisance["cuts_samples"][sampleName]
                                    ):
                                        # If the cuts_samples options is there and the sample is inserted in the dictionary
                                        # check if the current cutName is included. Excluded the cuts not in the list
                                        print(
                                            "Removing nuisance ",
                                            nuisanceName,
                                            " for sample ",
                                            sampleName,
                                            " from cut ",
                                            cutName,
                                        )
                                        card.write(("-").ljust(columndef))
                                    elif (
                                        "all" in nuisance and nuisance["all"] == 1
                                    ) or (
                                        "samples" in nuisance
                                        and sampleName in nuisance["samples"]
                                    ):
                                        # save the nuisance histograms in the root file
                                        if ("skipCMS" in nuisance.keys()) and nuisance[
                                            "skipCMS"
                                        ] == 1:
                                            suffixOut = None
                                        else:
                                            suffixOut = "_CMS_" + nuisance["name"]

                                        if (
                                            "perRecoBin" in nuisance.keys()
                                            and nuisance["perRecoBin"]
                                        ):
                                            if (
                                                "skipCMS" in nuisance.keys()
                                            ) and nuisance["skipCMS"] == 1:
                                                suffixOut = "_" + nuisance["name"]
                                            else:
                                                suffixOut = "_CMS_" + nuisance["name"]
                                            suffixOut += "_" + cutName

                                        symmetrize = (
                                            "symmetrize" in nuisance
                                            and nuisance["symmetrize"]
                                        )

                                        saved = self._saveNuisanceHistos(
                                            cutName,
                                            variableName,
                                            sampleName,
                                            "_" + nuisance["name"],
                                            suffixOut,
                                            symmetrize,
                                        )
                                        if saved:
                                            card.write("1.000".ljust(columndef))
                                        else:
                                            # saved can be false if skipMissingNuisance is true and histogram cannot be found
                                            card.write(("-").ljust(columndef))
                                    else:
                                        card.write(("-").ljust(columndef))

                        # closing block if type == lnN or shape
                        card.write("\n")

                        if "group" in nuisance:
                            nuisanceGroups[nuisance["group"]].append(entryName)

                    for group in sorted(nuisanceGroups.keys()):
                        card.write(
                            "%s group = %s\n" % (group, " ".join(nuisanceGroups[group]))
                        )

                    # done with normalization and shape nuisances.
                    # now add the stat nuisances
                    if "stat" in nuisances:
                        nuisance = nuisances["stat"]

                        if nuisance["type"] == "auto":
                            # use autoMCStats feature of combine
                            card.write(
                                "* autoMCStats "
                                + nuisance["maxPoiss"]
                                + "  "
                                + nuisance["includeSignal"]
                            )
                            #  nuisance ['maxPoiss'] =  Number of threshold events for Poisson modelling
                            #  nuisance ['includeSignal'] =  Include MC stat nuisances on signal processes (1=True, 0=False)
                            card.write("\n")

                        else:
                            # otherwise we process stat nuisances sample-by-sample
                            for sampleName in processes:
                                if sampleName not in nuisance["samples"]:
                                    continue

                                sampleNuisance = nuisance["samples"][sampleName]
                                sampleIndex = processes.index(sampleName)

                                if (
                                    sampleNuisance["typeStat"] == "uni"
                                ):  # unified approach
                                    # save the nuisance histograms in the root file
                                    saved = self._saveNuisanceHistos(
                                        cutName,
                                        variableName,
                                        sampleName,
                                        "stat",
                                        "_CMS_"
                                        + tagNameToAppearInDatacard
                                        + "_"
                                        + sampleName
                                        + "_stat",
                                    )

                                    if saved:
                                        card.write(
                                            (
                                                "CMS_"
                                                + tagNameToAppearInDatacard
                                                + "_"
                                                + sampleName
                                                + "_stat"
                                            ).ljust(80 - 20)
                                        )
                                        card.write((nuisance["type"]).ljust(20))

                                        # write the line in datacard. Only the column for this sample gets 1.000
                                        for idx in range(len(processes)):
                                            if idx == sampleIndex:
                                                card.write(("1.000").ljust(columndef))
                                            else:
                                                card.write(("-").ljust(columndef))

                                        card.write("\n")

                                elif sampleNuisance["typeStat"] == "bbb":  # bin-by-bin
                                    histoTemplate = self._getHisto(
                                        cutName, variableName, sampleName
                                    )
                                    for iBin in range(1, histoTemplate.GetNbinsX() + 1):
                                        if "correlate" in sampleNuisance:
                                            # specify the sample that is source of the variation
                                            tag = "_ibin" + sampleName + "_"
                                            correlate = list(
                                                sampleNuisance["correlate"]
                                            )  # list of sample names to correlate bin-by-bin with this sample
                                        else:
                                            tag = "_ibin_"
                                            correlate = []

                                        # save the nuisance histograms in the root file
                                        saved = self._saveNuisanceHistos(
                                            cutName,
                                            variableName,
                                            sampleName,
                                            tag + str(iBin) + "_stat",
                                            "_CMS_"
                                            + tagNameToAppearInDatacard
                                            + "_"
                                            + sampleName
                                            + "_ibin_"
                                            + str(iBin)
                                            + "_stat",
                                        )

                                        if not saved:
                                            continue

                                        for other in list(correlate):
                                            saved = self._saveNuisanceHistos(
                                                cutName,
                                                variableName,
                                                other,
                                                tag + str(iBin) + "_stat",
                                                "_CMS_"
                                                + tagNameToAppearInDatacard
                                                + "_"
                                                + sampleName
                                                + "_ibin_"
                                                + str(iBin)
                                                + "_stat",
                                            )
                                            if not saved:
                                                correlate.remove(other)

                                        card.write(
                                            (
                                                "CMS_"
                                                + tagNameToAppearInDatacard
                                                + "_"
                                                + sampleName
                                                + "_ibin_"
                                                + str(iBin)
                                                + "_stat"
                                            ).ljust(100 - 20)
                                        )
                                        card.write((nuisance["type"]).ljust(20))

                                        # write line in datacard. One line per sample per bin
                                        for idx in range(len(processes)):
                                            if (
                                                idx == sampleIndex
                                                or processes[idx] in correlate
                                            ):
                                                card.write(("1.000").ljust(columndef))
                                            else:
                                                card.write(("-").ljust(columndef))

                                        card.write("\n")

                    # now add the "rateParam" for the normalization
                    #  e.g.:            z_norm rateParam  htsearch zll 1
                    # see: https://twiki.cern.ch/twiki/bin/view/CMS/HiggsWG/SWGuideNonStandardCombineUses#Rate_Parameters
                    # 'rateParam' has a separate treatment -> it's just a line at the end of the datacard. It defines "free floating" samples
                    # I do it here and not before because I want the freee floating parameters at the end of the datacard
                    for nuisance in nuisances.values():
                        if nuisance["type"] != "rateParam":
                            continue

                        # check if a nuisance can be skipped because not in this particular cut
                        if "cuts" in nuisance and cutName not in nuisance["cuts"]:
                            continue

                        card.write(nuisance["name"].ljust(80 - 20))
                        card.write("rateParam".ljust(25))
                        card.write(
                            tagNameToAppearInDatacard.ljust(columndef)
                        )  # the bin
                        # there can be only 1 sample per rateParam
                        if len(nuisance["samples"]) != 1:
                            raise RuntimeError(
                                "Invalid rateParam: number of samples != 1"
                            )

                        sampleName, initialValue = list(nuisance["samples"].items())[0]
                        if sampleName not in samples:
                            raise RuntimeError(
                                "Invalid rateParam: unknown sample %s" % sampleName
                            )

                        card.write(sampleName.ljust(25))
                        card.write(("%-.4f" % float(initialValue)).ljust(columndef))
                        card.write("\n")

                    # now add other nuisances
                    # Are there other kind of nuisances I forgot?

                    card.write("-" * 100 + "\n")

                    card.write("\n")
                    card.close()

                    print("      done.")

                    self._fileIn.Close()
                    self._outFile.Close()
                    
                    del self._fileIn
                    del self._outFile
                    
                #self._outFile.Close()

        #if type(self._fileIn) is dict:
        #    for source in self._fileIn.values():
        #        source.Close()
        #else:
        #    self._fileIn.Close()

    # _____________________________________________________________________________
    def _saveNuisanceHistos(
        self,
        cutName,
        variableName,
        sampleName,
        suffixIn,
        suffixOut=None,
        symmetrize=False,
    ):
        histoUp = self._getHisto(cutName, variableName, sampleName, suffixIn + "Up")
        histoDown = self._getHisto(cutName, variableName, sampleName, suffixIn + "Down")

        if not histoUp or not histoDown:
            print(
                "Up/down histogram for",
                cutName,
                variableName,
                sampleName,
                suffixIn,
                "missing",
            )
            if self._skipMissingNuisance:
                return False
            # else let ROOT raise
        if "scaleSampleForDatacard" in structure[sampleName]:
            scaleFactor = 1.0
            if type(structure[sampleName]["scaleSampleForDatacard"]) is dict:
                try:
                    scaleFactor = structure[sampleName]["scaleSampleForDatacard"][
                        cutName
                    ]
                except:
                    pass
            if (
                type(structure[sampleName]["scaleSampleForDatacard"]) is int
                or type(structure[sampleName]["scaleSampleForDatacard"]) is float
            ):
                scaleFactor = structure[sampleName]["scaleSampleForDatacard"]
            histoUp.Scale(scaleFactor)
            histoDown.Scale(scaleFactor)

        if symmetrize:
            histoNom = self._getHisto(cutName, variableName, sampleName)
            histoDiff = histoUp.Clone("histoDiff")
            histoDiff.Add(histoDown, -1.0)
            histoDiff.Scale(0.5)
            histoUp.Reset()
            histoUp.Add(histoNom)
            histoUp.Add(histoDiff)
            histoDown.Reset()
            histoDown.Add(histoNom)
            histoDown.Add(histoDiff, -1.0)

        histoUp.SetDirectory(self._outFile)
        histoDown.SetDirectory(self._outFile)
        if suffixOut:
            histoUp.SetName("histo_%s%sUp" % (sampleName, suffixOut))
            histoDown.SetName("histo_%s%sDown" % (sampleName, suffixOut))

        self._outFile.cd()
        histoUp.Write()
        histoDown.Write()

        return True

    # _____________________________________________________________________________
    def _getHisto(self, cutName, variableName, sampleName, suffix=None):
        shapeName = "%s/%s/histo_%s" % (cutName, variableName, sampleName)
        if suffix:
            shapeName += suffix

        if type(self._fileIn) is dict:
            # by-sample ROOT file
            histo = self._fileIn[sampleName].Get(shapeName)
        else:
            # Merged single ROOT file
            histo = self._fileIn.Get(shapeName)

        if not histo:
            print(shapeName, "not found")
            #             if 'met' in variableName.lower() and 'met' in suffix.lower():
            #                 print(variableName, 'does not contain', suffix)
            #                 sys.exit()
            if suffix:
                print("Getting the nominal instead of varied")
                histo = self._getHisto(cutName, variableName, sampleName)
                histo.SetName(shapeName)
                return histo

        return histo

    # _____________________________________________________________________________
    def _removeStatUncertainty(self, histo):
        for iBin in range(0, histo.GetNbinsX() + 2):
            histo.SetBinError(iBin, 0.0)


class list_maker:
    def __init__(self, var, sep=",", __type=None):
        self._type = __type
        self._var = var
        self._sep = sep

    def __call__(self, option, opt_str, value, parser):
        if not hasattr(parser.values, self._var):
            setattr(parser.values, self._var, [])

        try:
            array = value.split(self._sep)
            if self._type:
                array = [self._type(e) for e in array]
            setattr(parser.values, self._var, array)

        except:
            print("Malformed option (comma separated list expected):", value)


def defaultParser():
    sys.argv = argv

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--outputDirDatacard",
        dest="outputDirDatacard",
        help="output directory",
        default="./datacards",
    )
    parser.add_argument(
        "--skipMissingNuisance",
        dest="skipMissingNuisance",
        help="Don't write nuisance lines when histograms are missing",
        default=False,
        action="store_true",
    )
    parser.add_argument(
        "--onlyVariables",
        dest="onlyVariables",
        help="Only make datacards for the provided variables, list of variables comma separated",
        default="",
    )
    parser.add_argument(
        "--onlyCuts",
        dest="onlyCuts",
        help="Only make datacards for the provided cuts, list of cuts comma separated",
        default="",
    )
    return parser


def main():
    header = """
    --------------------------------------------------------------------------------------------------

    __ \          |                                 |       \  |         |
    |   |   _` |  __|   _` |   __|   _` |   __|  _` |      |\/ |   _` |  |  /   _ \   __|
    |   |  (   |  |    (   |  (     (   |  |    (   |      |   |  (   |    <    __/  |
    ____/  \__,_| \__| \__,_| \___| \__,_| _|   \__,_|     _|  _| \__,_| _|\_\ \___| _|

    --------------------------------------------------------------------------------------------------
    """
    header = dedent(header)
    print(header)
    parser = defaultParser()
    opt = parser.parse_args()

    onlyVariables = opt.onlyVariables
    if onlyVariables == "":
        onlyVariables = None
    else:
        onlyVariables = [s.strip() for s in onlyVariables.split(",")]

    onlyCuts = opt.onlyCuts
    if onlyCuts == "":
        onlyCuts = None
    else:
        onlyCuts = [s.strip() for s in onlyCuts.split(",")]

    global cuts, plot
    from mkShapesRDF.shapeAnalysis.ConfigLib import ConfigLib

    configsFolder = "configs"
    ConfigLib.loadLatestPickle(os.path.abspath(configsFolder), globals())
    print(dir())
    print(globals().keys())

    # unpacking of variables
    cuts = cuts["cuts"]
    inputFile = outputFolder + "/" + outputFile

    ROOT.TH1.SetDefaultSumw2(True)

    factory = DatacardFactory()
    factory._tag = tag
    factory._skipMissingNuisance = opt.skipMissingNuisance
    factory.onlyCuts = onlyCuts
    factory.onlyVariables = onlyVariables

    import mkShapesRDF.shapeAnalysis.latinos.LatinosUtils as utils

    subsamplesmap = utils.flatten_samples(samples)
    categoriesmap = utils.flatten_cuts(cuts)

    utils.update_variables_with_categories(variables, categoriesmap)
    utils.update_nuisances_with_subsamples(nuisances, subsamplesmap)
    utils.update_nuisances_with_categories(nuisances, categoriesmap)

    factory.makeDatacards(
        inputFile, opt.outputDirDatacard, variables, cuts, samples, structure, nuisances
    )


if __name__ == "__main__":
    main()
