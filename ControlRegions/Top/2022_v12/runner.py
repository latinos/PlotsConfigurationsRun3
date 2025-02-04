from copy import deepcopy
import sys
import ROOT
from array import array
from mkShapesRDF.lib.parse_cpp import ParseCpp

ROOT.gROOT.SetBatch(True)
ROOT.TH1.SetDefaultSumw2(True)


class RunAnalysis:
    r"""Class athat craeates ``dfs`` and runs the analysiss"""

    @staticmethod
    def splitSamples(samples, useFilesPerJob=True):
        r"""static methods, takes a dictionary of samples and split them based on their weights and max num. of files

        Parameters
        ----------
            samples : dict
                dictionary of samples
            useFilesPerJob : bool, optional, default: True
                if you want to further split the samples based on max num. of files.

        Returns
        -------
            `list of tuple`
                each tuple will have a lenght of 5 (6 if subsamples are present), where the first element is the name of the sample, the second the list of files, the third the weight, and the fourth the index of this tuple compared to the other tuples of the same sample type, the fifth will be the isData flag (True if the sample is data, False otherwise). If subsamples are present, the sixth element will be the dict of subsamples
        """
        # will contain all the different samples splitted based on their weights and max num. of files
        splittedSamples = []
        for sampleName in list(samples.keys()):
            types = (
                {}
            )  # this will contain the the different type of files with their special weights for this sampleName
            # recall that samples[sampleName]['name'] contain a list of tuples, where a single tuple can have a size of 2 or 3:
            # first position for name of the process (DYJetsToLL_M-50), second list of files, third a possible special weight
            for filesType in samples[sampleName]["name"]:
                # no special weight (will use '1'), and at least one file found
                if len(filesType) == 2 and len(filesType[1]) > 0:
                    if "1" not in list(types.keys()):
                        types["1"] = []
                    types["1"].append(filesType + ("1.0",))
                elif len(filesType) == 3 and len(filesType[1]) > 0:
                    if filesType[2] not in list(types.keys()):
                        types[filesType[2]] = []
                    types[filesType[2]].append(filesType)
                else:
                    print("Error", sampleName, filesType, file=sys.stderr)
                    print(
                        "Either the sample proc you specified has no files, or the weight had problems",
                        file=sys.stderr,
                    )
                    sys.exit()

            i = 0
            for _type in list(types.keys()):
                # split files based on FilesPerJob or include them all
                __files = list(map(lambda k: k[1], types[_type]))
                # flatted list of files
                __files = [item for sublist in __files for item in sublist]
                if useFilesPerJob:
                    dim = samples[sampleName].get("FilesPerJob", len(__files))
                else:
                    dim = len(__files)
                __files = [__files[j : j + dim] for j in range(0, len(__files), dim)]
                for ___files in __files:
                    # the weights for these files will be the product of the weight inside this sampele (i.e. samples[sampleName]['weight'])
                    # and the product of the special weights that is in common to all of those files (i.e. sampleType[0])
                    # the common special weight can be retrived from the first of the list of files with this weight
                    # remember that the tuple has always size 3 now, the last position is for the special weight
                    weight = (
                        "( "
                        + samples[sampleName]["weight"]
                        + " ) * ( "
                        + types[_type][0][2]
                        + " )"
                    )
                    isData = samples[sampleName].get("isData", False)
                    sampleType = (sampleName, ___files, weight, i, isData)
                    if "subsamples" in list(samples[sampleName].keys()):
                        sampleType += (samples[sampleName]["subsamples"],)
                    splittedSamples.append(sampleType)
                    i += 1
        return splittedSamples

    @staticmethod
    def getTTreeNomAndFriends(fnom, friends):
        """Create a TChain with the nominal files and the friends files (nuisances TTrees with varied branches)

        Args:
            fnom (list): list of nominal files
            friends (list of list): list of list of friends files

        Returns:
            TChain: TChain with nominal files and friends files
        """
        tnom = ROOT.TChain("Events")
        for f in fnom:
            tnom.Add(f)
        for friend in friends:
            _tfriend = ROOT.TChain("Events")
            for f in friend:
                _tfriend.Add(f)
            tnom.AddFriend(_tfriend)
        return tnom

    @staticmethod
    def getNuisanceFiles(nuisance, files):
        """Searches in the provided nuisance folder for the files with the same name of the nominal files

        Args:
            nuisance (dict): dict with the nuisance information
            files (list): list of nominal files

        Returns:
            list of list: list with the down and up varied list of files
        """
        _files = list(map(lambda k: k.split("/")[-1], files))
        nuisanceFilesDown = list(
            map(lambda k: nuisance["folderDown"] + "/" + k, _files)
        )
        nuisanceFilesUp = list(map(lambda k: nuisance["folderUp"] + "/" + k, _files))
        return [nuisanceFilesDown, nuisanceFilesUp]

    @staticmethod
    def index_sub(string, sub):
        try:
            return string.index(sub)
        except ValueError:
            return -10000

    def __init__(
        self,
        samples,
        aliases,
        variables,
        cuts,
        nuisances,
        lumi,
        limit=-1,
        outputFileMap="output.root",
    ):
        r"""
        Stores arguments in the class attributes and creates all the RDataFrame objects

        Parameters
        ----------

            samples : `list of tuple`
                same type as the return of the splitSamples method
            aliases : dict
                dict of aliases
            variables : dict
                dict of variables
            cuts : dict
                dict of cuts, contains two keys (preselections: str, cuts: dict)
            nuisances : dict
                dict of nuisances
            lumi : float
                lumi in fb-1
            limit : int, optional, default: -1
                limit of events to be processed
            outputFileMap : str, optional, defaults: 'output.root'
                full path + filename of the output root file.

        Returns
        -------
            None

        """
        self.samples = samples
        self.aliases = aliases
        self.variables = variables
        self.preselections = cuts["preselections"]
        mergedCuts = {}
        for cut in list(cuts["cuts"].keys()):
            __cutExpr = ""
            if type(cuts["cuts"][cut]) == dict:
                __cutExpr = cuts["cuts"][cut]["expr"]
                for cat in list(cuts["cuts"][cut]["categories"].keys()):
                    mergedCuts[cut + "_" + cat] = {"parent": cut}
                    mergedCuts[cut + "_" + cat]["expr"] = (
                        __cutExpr + " && " + cuts["cuts"][cut]["categories"][cat]
                    )
            elif type(cuts["cuts"][cut]) == str:
                __cutExpr = cuts["cuts"][cut]
                mergedCuts[cut] = {"expr": __cutExpr, "parent": cut}
        self.cuts = mergedCuts
        self.nuisances = nuisances
        self.lumi = lumi
        self.limit = limit
        self.outputFileMap = outputFileMap
        self.remappedVariables = {}

        self.dfs = {}
        r"""
        dfs is a dictionary containing as keys the sampleNames. The structure should look like this:

        ..  code-block:: python

            dfs = {
                'DY':{
                    0: {
                        'df': obj,
                        'columnNames': [...],
                        'usedVariables': [...],
                        'ttree': obj2, # needed otherwise seg fault in root
                    },
                }
            }

        """

        usedVariables = set()
        usedVariables = usedVariables.union(
            ParseCpp.listOfVariables(ParseCpp.parse(self.preselections))
        )
        for cut in mergedCuts.keys():
            usedVariables = usedVariables.union(
                ParseCpp.listOfVariables(ParseCpp.parse(mergedCuts[cut]["expr"]))
            )
        for var in variables.keys():
            if "name" in variables[var].keys():
                __var = variables[var]["name"].split(":")
                __vars = list(
                    map(lambda k: ParseCpp.listOfVariables(ParseCpp.parse(k)), __var)
                )
                for __v in __vars:
                    usedVariables = usedVariables.union(__v)

            elif "tree" in variables[var].keys():
                for branch in variables[var]["tree"].keys():
                    usedVariables = usedVariables.union(
                        ParseCpp.listOfVariables(
                            ParseCpp.parse(variables[var]["tree"][branch])
                        )
                    )
            else:
                print("Cannot process variable ", var, " nuisances might be faulty")

        # sample here is a tuple, first el is the sampleName, second list of files,
        # third the special weight, forth is the index of tuple for the same sample,
        # fifth if present the dict of subsamples
        for sample in samples:
            files = sample[1]
            sampleName = sample[0]
            friendsFiles = []
            usedFolders = []
            for nuisance in self.nuisances.values():
                if sampleName not in nuisance.get("samples", {sampleName: []}):
                    continue
                if nuisance.get("type", "") == "shape":
                    if nuisance.get("kind", "") == "suffix":
                        if nuisance["folderUp"] in usedFolders:
                            continue
                        usedFolders.append(nuisance["folderUp"])

                        friendsFiles += RunAnalysis.getNuisanceFiles(nuisance, files)

            tnom = RunAnalysis.getTTreeNomAndFriends(files, friendsFiles)

            if limit != -1:
                df = ROOT.RDataFrame(tnom)
                df = df.Range(limit)
            else:
                ROOT.EnableImplicitMT()
                df = ROOT.RDataFrame(tnom)
            if sampleName not in self.dfs.keys():
                self.dfs[sample[0]] = {}
            self.dfs[sampleName][sample[3]] = {
                "df": df,
                "ttree": tnom,
                "usedVariables": list(usedVariables),
            }
            self.dfs[sampleName][sample[3]]["columnNames"] = list(
                map(lambda k: str(k), df.GetColumnNames())
            )

        self.definedAliases = {}

        print("\n\nLoaded dataframes\n\n")

    def loadAliases(self, afterNuis=False):
        """
        Load aliases in the dataframes. It does not create the special alias ``weight`` for which a special method is used.

        Parameters
        ----------
            afterNuis : bool, optional, default: False
                if True, only aliases with the key ``afterNuis`` set to True will be loaded

        """
        aliases = self.aliases
        for sampleName in self.dfs.keys():
            for index in self.dfs[sampleName].keys():
                df = self.dfs[sampleName][index]["df"]

                define_string = "df"
                usedVariables = set(self.dfs[sampleName][index]["usedVariables"])
                for alias in list(aliases.keys()):
                    # only load aliases needed for nuisances!
                    # if beforeNuis
                    if (afterNuis) != (aliases[alias].get("afterNuis", False)):
                        if "expr" in aliases[alias]:
                            usedVariables = usedVariables.union(
                                ParseCpp.listOfVariables(
                                    ParseCpp.parse(aliases[alias]["expr"])
                                )
                            )
                        continue

                    if "samples" in list(aliases[alias]):
                        if sampleName not in aliases[alias]["samples"]:
                            continue
                    if alias in self.dfs[sampleName][index]["columnNames"]:
                        if alias != aliases[alias].get("expr", ""):
                            print(
                                f"Alias {alias} cannot be defined, column with that name already exists"
                            )
                            sys.exit()
                        else:
                            # since the alias key is equal to expr there's no need to keep the alias
                            del self.aliases[alias]
                            continue

                    for line in aliases[alias].get("linesToAdd", []):
                        # RPLME_nThreads is used to set the number of threads
                        ROOT.gInterpreter.Declare(
                            line.replace("RPLME_nThreads", str(df.GetNSlots()))
                        )

                    for line in aliases[alias].get("linesToProcess", []):
                        # RPLME_nThreads is used to set the number of threads
                        exec(line, globals())

                    if "expr" in list(aliases[alias].keys()):
                        define_string += (
                            f".Define('{alias}', '{aliases[alias]['expr']}') \\\n\t"
                        )
                        usedVariables = usedVariables.union(
                            ParseCpp.listOfVariables(
                                ParseCpp.parse(aliases[alias]["expr"])
                            )
                        )

                    elif "exprSlot" in list(aliases[alias].keys()):
                        args = aliases[alias]["exprSlot"]
                        args[0] = args[0].replace("RPLME_nThreads", str(df.GetNSlots()))
                        define_string += (
                            f".DefineSlot('{alias}', '{args[0]}', [ {args[1]} ]) \\\n\t"
                        )
                        usedVariables = usedVariables.union(
                            ParseCpp.listOfVariables(
                                ParseCpp.parse(aliases[alias]["exprSlot"][1])
                            )
                        )

                    elif "class" in list(aliases[alias].keys()):
                        define_string += f".Define('{alias}', '{aliases[alias]['class']} ( {aliases[alias].get('args', '')}  )') \\\n\t"

                df1 = eval(define_string)
                self.dfs[sampleName][index]["df"] = df1

                stringPrint = "before nuisances"
                if afterNuis:
                    stringPrint = "after nuisances"
                print(
                    f"\n\nLoaded all aliases {stringPrint} for {sampleName} index {index}\n\n"
                )

                self.dfs[sampleName][index]["usedVariables"] = list(usedVariables)

                self.dfs[sampleName][index]["columnNames"] = list(
                    map(lambda k: str(k), df1.GetColumnNames())
                )

    def loadAliasWeight(self):
        """
        Loads only the special alias ``weight`` in the dataframes.
        """
        samples = self.samples
        aliases = self.aliases
        for sampleName in self.dfs.keys():
            for index in self.dfs[sampleName].keys():
                df = self.dfs[sampleName][index]["df"]  # noqa: F841

                # Define the most importante alias: the weight!
                sample = list(
                    filter(lambda k: k[0] == sampleName and k[3] == index, samples)
                )[0]
                weight = sample[2]
                isData = sample[4]

                if not isData:
                    aliases["weight"] = {"expr": str(self.lumi) + " * " + weight}
                else:
                    aliases["weight"] = {"expr": weight}

                print("\n\n", sampleName, "\n\n", aliases["weight"])

                # load the alias weight
                define_string = "df"

                alias = "weight"

                if alias in self.dfs[sampleName][index]["columnNames"]:
                    print(
                        f"Alias {alias} cannot be defined, column with that name already exists"
                    )
                    sys.exit()

                define_string += (
                    f".Define('{alias}', '{aliases[alias]['expr']}') \\\n\t"
                )

                df1 = eval(define_string)
                self.dfs[sampleName][index]["df"] = df1

                print(f"\n\nLoaded alias weight for {sampleName} index {index}\n\n")

                self.dfs[sampleName][index]["columnNames"].append("weight")

    def loadSystematicsSuffix(self):
        """
        Loads systematics of type ``suffix`` in the dataframes.
        """
        for sampleName in self.dfs.keys():
            for index in self.dfs[sampleName].keys():
                df = self.dfs[sampleName][index]["df"]
                columnNames = self.dfs[sampleName][index]["columnNames"]
                nuisances = self.nuisances
                # nuisance key is not used
                for _, nuisance in list(nuisances.items()):
                    if sampleName not in nuisance.get("samples", {sampleName: []}):
                        continue
                    if nuisance.get("type", "") == "shape":
                        if nuisance.get("kind", "") == "suffix":
                            variation = nuisance["mapDown"]
                            variedCols = list(
                                filter(lambda k: k.endswith(variation), columnNames)
                            )
                            if len(variedCols) == 0:
                                print(f"No varied columns for {variation}")
                                sys.exit()
                            baseCols = list(
                                map(
                                    lambda k: k[
                                        RunAnalysis.index_sub(k, "Events.")
                                        + len("Events.") : -len("_" + variation)
                                    ],
                                    variedCols,
                                )
                            )
                            for baseCol in baseCols:
                                if (
                                    baseCol
                                    not in self.dfs[sampleName][index]["usedVariables"]
                                ):
                                    # baseCol is never used -> useless to register variation
                                    continue
                                if "bool" not in str(df.GetColumnType(baseCol)).lower():
                                    varNameDown = (
                                        baseCol
                                        + "_"
                                        + nuisance["mapDown"]
                                        + "*"
                                        + nuisance["samples"][sampleName][1]
                                    )
                                    varNameUp = (
                                        baseCol
                                        + "_"
                                        + nuisance["mapUp"]
                                        + "*"
                                        + nuisance["samples"][sampleName][0]
                                    )
                                else:
                                    varNameDown = baseCol + "_" + nuisance["mapDown"]
                                    varNameUp = baseCol + "_" + nuisance["mapUp"]

                                _type = df.GetColumnType(baseCol)
                                expr = (
                                    ParseCpp.RVecExpression(_type)
                                    + "{"
                                    + f"{varNameDown}, {varNameUp}"
                                    + "}"
                                )
                                df = df.Vary(
                                    baseCol,
                                    expr,
                                    variationTags=["Down", "Up"],
                                    variationName=nuisance["name"],
                                )

                        elif nuisance.get("kind", "") == "weight":
                            continue
                        else:
                            print("Unsupported nuisance")
                            sys.exit()
                self.dfs[sampleName][index]["df"] = df

    def loadSystematicsReweights(self):
        """
        Loads systematics of type ``suffix`` in the dataframes.
        """
        for sampleName in self.dfs.keys():
            for index in self.dfs[sampleName].keys():
                df = self.dfs[sampleName][index]["df"]
                columnNames = self.dfs[sampleName][index]["columnNames"]
                nuisances = self.nuisances
                # nuisance key is not used
                for _, nuisance in list(nuisances.items()):
                    if sampleName not in nuisance.get("samples", {sampleName: []}):
                        continue
                    if nuisance.get("type", "") == "shape":
                        if nuisance.get("kind", "") == "weight":
                            weights = nuisance["samples"].get(sampleName, None)
                            if weights is not None:
                                variedNames = []
                                if weights[0] not in columnNames:
                                    df = df.Define(nuisance["name"] + "_up", weights[0])
                                    variedNames.append(nuisance["name"] + "_up")
                                else:
                                    variedNames.append(weights[0])

                                if weights[1] not in columnNames:
                                    df = df.Define(
                                        nuisance["name"] + "_down", weights[1]
                                    )
                                    variedNames.append(nuisance["name"] + "_down")
                                else:
                                    variedNames.append(weights[1])

                                if df.GetColumnType("weight") == "double":
                                    expr = (
                                        "ROOT::RVecD"
                                        + "{ weight * (double)"
                                        + f"{variedNames[1]}, weight * (double) {variedNames[0]}"
                                        + "}"
                                    )
                                elif df.GetColumnType("weight") == "float":
                                    expr = (
                                        "ROOT::RVecF"
                                        + "{ weight * (float)"
                                        + f"{variedNames[1]}, weight * (float) {variedNames[0]}"
                                        + "}"
                                    )
                                else:
                                    print(
                                        "Weight column has unknown type:",
                                        df.GetColumnType("weight"),
                                        "while varied is: ",
                                        df.GetColumnType(variedNames[1]),
                                    )
                                    sys.exit()

                                df = df.Vary(
                                    "weight",
                                    expr,
                                    variationTags=["Down", "Up"],
                                    variationName=nuisance["name"],
                                )
                        elif nuisance.get("kind", "") == "suffix":
                            continue
                        else:
                            print("Unsupported nuisance")
                            sys.exit()
                self.dfs[sampleName][index]["df"] = df

    def loadVariables(self):
        """
        Loads variables (not the ones with the 'tree' key in them),
        and checks if they are already in the dataframe columns,
        if so it adds ``__`` at the beginning of the name.

        Since variables are shared but not the aliases,
        it could happen that a variable's name or expression is already defined
        for a given df but not for another one ->
        need to determine a common and compatible set of variables for all the many dfs.

        This is done by gathering the largest set of column names.
        """

        bigColumnNames = set()
        for sampleName in self.dfs.keys():
            for index in self.dfs[sampleName].keys():
                columnNames = self.dfs[sampleName][index]["columnNames"]
                bigColumnNames = bigColumnNames.union(set(columnNames))

        for sampleName in self.dfs.keys():
            for index in self.dfs[sampleName].keys():
                for var in list(self.variables.keys()):
                    if "tree" in self.variables[var].keys():
                        continue
                    if var in bigColumnNames and var != self.variables[var]["name"]:
                        # here I want to define a variable whose key is already in the column name list
                        # and its expression is different from its name
                        # therefore we will either create a Define or an Alias

                        # need to rename the new variable!
                        prefix = "__"
                        nVar = prefix + var
                        while nVar in bigColumnNames:
                            prefix += "__"
                            nVar = prefix + var
                        # print("changing variable", var, "to " + nVar)
                        self.remappedVariables[nVar] = prefix
                        self.variables[nVar] = deepcopy(self.variables[var])
                        del self.variables[var]

        for sampleName in self.dfs.keys():
            for index in self.dfs[sampleName].keys():
                df = self.dfs[sampleName][index]["df"]
                for var in list(self.variables.keys()):
                    if "tree" in self.variables[var].keys():
                        continue
                    for i, _var in enumerate(self.variables[var]["name"].split(":")):
                        n = var if i == 0 else var + f"_{i}"

                        if _var not in bigColumnNames:
                            # the variable expr does not exist, create it
                            df = df.Define(n, _var)
                        elif n not in bigColumnNames:
                            # the variable expr exists in the df, but not the variable key
                            # use alias
                            df = df.Alias(n, _var)
                        elif n == _var and n in bigColumnNames:
                            # since the variable name and expression are equal and are already present in the df don't do anything
                            pass
                        else:
                            # FIXME
                            print("Error, cannot define variable")
                            sys.exit()
                self.dfs[sampleName][index]["df"] = df
                self.dfs[sampleName][index]["columnNames"] = list(
                    map(lambda k: str(k), df.GetColumnNames())
                )

    def loadBranches(self):
        """
        Loads branches (the ones specified in an ``alias`` with the ``tree`` key in them),
        and checks if they are already in the dataframe columns,
        if so it adds ``__`` at the beginning of the name.

        Since variables are shared but not the aliases,
        it could happen that a variable's name or expression is already defined
        for a given df but not for another one ->
        need to determine a common and compatible set of variables for all the many dfs.

        This is done by gathering the largest set of column names.
        """

        bigColumnNames = set()
        for sampleName in self.dfs.keys():
            for index in self.dfs[sampleName].keys():
                columnNames = self.dfs[sampleName][index]["columnNames"]
                bigColumnNames = bigColumnNames.union(set(columnNames))

        for sampleName in self.dfs.keys():
            for index in self.dfs[sampleName].keys():
                for var in list(self.variables.keys()):
                    if "tree" not in self.variables[var].keys():
                        continue
                    for branch in list(self.variables[var]["tree"].keys()):
                        if (
                            branch in bigColumnNames
                            and branch != self.variables[var]["tree"][branch]
                        ):
                            # here I want to define a variable whose key is already in the column name list
                            # and its expression is different from its name
                            # therefore we will either create a Define or an Alias

                            # need to rename the new variable!
                            prefix = "__"
                            nVar = prefix + branch
                            while nVar in bigColumnNames:
                                prefix += "__"
                                nVar = prefix + branch
                            # print("changing variable", branch, "to " + nVar)
                            self.remappedVariables[nVar] = prefix
                            self.variables[var]["tree"][nVar] = self.variables[var][
                                "tree"
                            ][branch]
                            del self.variables[var]["tree"][branch]

        for sampleName in self.dfs.keys():
            for index in self.dfs[sampleName].keys():
                df = self.dfs[sampleName][index]["df"]
                for var in list(self.variables.keys()):
                    if "tree" not in self.variables[var].keys():
                        continue
                    for branch in self.variables[var]["tree"].keys():
                        # print("working on defining branch", branch)
                        if self.variables[var]["tree"][branch] not in bigColumnNames:
                            # the variable expr does not exist, create it
                            # print("define the branch")
                            df = df.Define(branch, self.variables[var]["tree"][branch])
                        elif branch not in bigColumnNames:
                            # the variable expr exists in the df, but not the variable key
                            # use alias
                            # print("define an alias to the branch")
                            df = df.Alias(branch, self.variables[var]["tree"][branch])
                        elif (
                            branch == self.variables[var]["tree"][branch]
                            and branch in bigColumnNames
                        ):
                            # since the variable name and expression are equal and are already present in the df don't do anything
                            pass
                        else:
                            # FIXME
                            print("Error, cannot define variable")
                            sys.exit()
                self.dfs[sampleName][index]["df"] = df
                self.dfs[sampleName][index]["columnNames"] = list(
                    map(lambda k: str(k), df.GetColumnNames())
                )

    def createResults(self):
        """
        Create empty dictionary for results, will store all the different histos
        """
        self.results = {}
        for cut in self.cuts.keys():
            self.results[cut] = {}
            for variable in self.variables.keys():
                self.results[cut][variable] = {}

    def splitSubsamples(self):
        """
        Split samples into subsamples if needed

        After this method the ``dfs`` attribute will be modified to contain the subsamples names instead of the original sample name
        """
        sampleNames = set(
            list(map(lambda k: k[0], list(filter(lambda k: len(k) == 6, self.samples))))
        )
        for sampleName in sampleNames:
            _sample = list(filter(lambda k: k[0] == sampleName, self.samples))[0]
            for subsample in list(_sample[5].keys()):
                self.dfs[sampleName + "_" + subsample] = {}
                for index in self.dfs[sampleName].keys():
                    self.dfs[sampleName + "_" + subsample][index] = {
                        "parent": sampleName
                    }
                    self.dfs[sampleName + "_" + subsample][index]["df"] = self.dfs[
                        sampleName
                    ][index]["df"].Filter(_sample[5][subsample])
                    self.dfs[sampleName + "_" + subsample][index][
                        "columnNames"
                    ] = self.dfs[sampleName][index]["columnNames"]
                    self.dfs[sampleName + "_" + subsample][index]["ttree"] = self.dfs[
                        sampleName
                    ][index]["ttree"]

            del self.dfs[sampleName]

    def create_cuts_vars(self):
        """
        Defines ``Histo1D`` for each variable and cut and dataframe. It also creates dictionary for variations through ``VariationsFor()``
        """
        mergedCuts = self.cuts
        variables = self.variables
        for sampleName in self.dfs.keys():
            for index in self.dfs[sampleName].keys():
                df = self.dfs[sampleName][index]["df"]

                for cut in mergedCuts.keys():
                    df_cat = df.Filter(mergedCuts[cut]["expr"])
                    opts = ROOT.RDF.RSnapshotOptions()
                    opts.fLazy = True

                    for var in list(variables.keys()):
                        if "tree" in variables[var].keys():
                            if not mergedCuts[cut]["parent"] in variables[var]["cuts"]:
                                # del df_cat
                                continue

                            outpath = self.outputFileMap
                            if self.outputFileMap != "output.root":
                                outfileName = (
                                    ".".join(
                                        self.outputFileMap.split("/")[-1].split(".")[
                                            :-1
                                        ]
                                    )
                                    + f"__ALL__{cut}_{sampleName}_{str(index)}.root"
                                )
                                outpath = (
                                    "/".join(self.outputFileMap.split("/")[:-1])
                                    + "/"
                                    + outfileName
                                )
                            else:
                                outpath = f"output_{cut}_{sampleName}_{str(index)}.root"

                            # _h = df_cat.Snapshot(cut + '/' + sampleName, outpath, list(self.variables[var]['tree'].keys()), opts)

                            # FIXME always save the weight!
                            _h = df_cat.Snapshot(
                                "Events",
                                outpath,
                                list(self.variables[var]["tree"].keys()) + ["weight"],
                                opts,
                            )
                        else:
                            vs = variables[var]["name"].split(":")

                            histRange = []
                            if len(variables[var]["range"]) == len(vs):
                                # bin endges are provided by the user
                                for ax in variables[var]["range"]:
                                    histRange.extend([len(ax) - 1, array("d", ax)])
                            else:
                                histRange = variables[var]["range"]

                            histRange = tuple(histRange)

                            if len(vs) == 1:
                                _h = df_cat.Histo1D(
                                    (cut + "_" + var, "") + histRange, var, "weight"
                                )
                            elif len(vs) == 2:
                                varNames = []
                                for i, _var in enumerate(vs):
                                    n = var if i == 0 else var + f"_{i}"
                                    varNames.append(n)

                                _h = df_cat.Histo2D(
                                    (cut + "_" + var, "") + histRange,
                                    *varNames,
                                    "weight",
                                )
                            else:
                                print("Unknown dimension of histo for variable", var)
                                sys.exit()
                        if sampleName not in self.results[cut][var].keys():
                            self.results[cut][var][sampleName] = {}
                        self.results[cut][var][sampleName][index] = _h

                for cut in mergedCuts.keys():
                    for var in list(variables.keys()):
                        if "tree" not in variables[var].keys():
                            _s = self.results[cut][var][sampleName][index]
                            _s_var = ROOT.RDF.Experimental.VariationsFor(_s)
                            self.results[cut][var][sampleName][index] = _s_var

    def convertResults(self):
        """
        Gather resulting histograms and fold them if needed.

        Systematics are also saved.
        """
        mergedCuts = self.cuts
        variables = self.variables
        for sampleName in self.dfs.keys():
            for index in self.dfs[sampleName].keys():
                for cut in mergedCuts.keys():
                    for var in list(variables.keys()):
                        if "tree" in variables[var].keys():
                            # no need to process SnapShots
                            continue
                        _s_var = self.results[cut][var][sampleName][index]
                        _histos = {}
                        for _variation in list(map(lambda k: str(k), _s_var.GetKeys())):
                            _h_name = _variation.replace(":", "")
                            _h = 0
                            _h = _s_var[_variation]
                            fold = variables[var].get("fold", 0)
                            if fold == 1 or fold == 3:
                                _h.SetBinContent(
                                    1, _h.GetBinContent(0) + _h.GetBinContent(1)
                                )
                                _h.SetBinContent(0, 0)
                            if fold == 2 or fold == 3:
                                lastBin = _h.GetNbinsX()
                                _h.SetBinContent(
                                    lastBin,
                                    _h.GetBinContent(lastBin)
                                    + _h.GetBinContent(lastBin + 1),
                                )
                                _h.SetBinContent(lastBin + 1, 0)
                            _histos[_h_name] = _h.Clone()
                            # del _h
                        # del self.results[cut][var][sampleName]['object']
                        # replace the object with the dictionary of histos
                        self.results[cut][var][sampleName][index] = _histos

    def saveResults(self):
        """
        Save results in a root file.

        If ``Snapshot`` were created will merge them in a output file.

        """

        f = ROOT.TFile(self.outputFileMap, "recreate")

        toBeDeleted = []
        openedFiles = []
        openedTrees = []
        for sampleName in self.dfs.keys():
            for index in self.dfs[sampleName].keys():
                for cut in self.cuts.keys():
                    for var in list(self.variables.keys()):
                        if "tree" in self.variables[var].keys():
                            if (
                                not self.cuts[cut]["parent"]
                                in self.variables[var]["cuts"]
                            ):
                                continue

                            if self.outputFileMap != "output.root":
                                outfileName = (
                                    ".".join(
                                        self.outputFileMap.split("/")[-1].split(".")[
                                            :-1
                                        ]
                                    )
                                    + f"__ALL__{cut}_{sampleName}_{str(index)}.root"
                                )
                                outpath = (
                                    "/".join(self.outputFileMap.split("/")[:-1])
                                    + "/"
                                    + outfileName
                                )
                            else:
                                outpath = f"output_{cut}_{sampleName}_{str(index)}.root"
                            _f = ROOT.TFile(outpath)
                            openedFiles.append(_f)

                            if _f.GetListOfKeys().Contains("Events"):
                                t = _f.Get("Events")
                                openedTrees.append(t)
                                f.cd("/")
                                folder = f"trees/{cut}/{sampleName}/"
                                # print("Creating dir", folder, outpath)
                                toBeDeleted.append(outpath)
                                ROOT.gDirectory.mkdir(folder, "", True)
                                ROOT.gDirectory.cd("/" + folder)
                                t.CloneTree().Write()
                            else:
                                print(
                                    "No TTree was created for",
                                    cut,
                                    var,
                                    sampleName,
                                    index,
                                    "even if requested",
                                    file=sys.stderr,
                                )

        f.cd("/")

        for cut_cat in list(self.results.keys()):
            _cut_cat = f.mkdir(cut_cat)
            for var in list(self.results[cut_cat].keys()):
                if "tree" in self.variables[var].keys():
                    continue
                _var = ""
                if var in list(self.remappedVariables.keys()):
                    # remove the __ at the beginning
                    _var = var[len(self.remappedVariables[var]) :]
                else:
                    _var = var

                _cut_cat.mkdir(_var)
                f.cd("/" + cut_cat + "/" + _var)
                for sampleName in list(self.results[cut_cat][var].keys()):
                    # should first merge histos
                    mergedHistos = {}
                    for index in list(self.results[cut_cat][var][sampleName].keys()):
                        for hname in list(
                            self.results[cut_cat][var][sampleName][index].keys()
                        ):
                            if hname not in mergedHistos.keys():
                                mergedHistos[hname] = self.results[cut_cat][var][
                                    sampleName
                                ][index][hname].Clone()
                            else:
                                mergedHistos[hname].Add(
                                    self.results[cut_cat][var][sampleName][index][hname]
                                )

                    for hname in mergedHistos.keys():
                        if hname == "nominal":
                            mergedHistos[hname].SetName("histo_" + sampleName)
                        else:
                            mergedHistos[hname].SetName(
                                "histo_" + sampleName + "_" + hname
                            )
                        mergedHistos[hname].Write()
        f.Close()

        # clean snapshot files
        proc = ""
        for _file in toBeDeleted:
            proc += f" rm {_file}; "
        import subprocess

        _proc = subprocess.Popen(proc, shell=True)
        _proc.wait()

        # print(proc)

    def mergeSaveResults(self):
        f = ROOT.TFile(self.outputFileMap, "recreate")
        for cut_cat in list(self.results.keys()):
            _cut_cat = f.mkdir(cut_cat)
            for var in list(self.results[cut_cat].keys()):
                if "tree" in self.variables[var].keys():
                    # no need to process SnapShots
                    continue
                _cut_cat.mkdir(var)
                f.cd("/" + cut_cat + "/" + var)
                for sampleName in list(self.results[cut_cat][var].keys()):
                    # should first merge histos
                    mergedHistos = {}
                    for index in list(self.results[cut_cat][var][sampleName].keys()):
                        for hname in list(
                            self.results[cut_cat][var][sampleName][index].keys()
                        ):
                            if hname not in mergedHistos.keys():
                                mergedHistos[hname] = self.results[cut_cat][var][
                                    sampleName
                                ][index][hname].Clone()
                            else:
                                mergedHistos[hname].Add(
                                    self.results[cut_cat][var][sampleName][index][hname]
                                )

                    for hname in mergedHistos.keys():
                        if hname == "nominal":
                            mergedHistos[hname].SetName("histo_" + sampleName)
                        else:
                            mergedHistos[hname].SetName(
                                "histo_" + sampleName + "_" + hname
                            )
                        mergedHistos[hname].Write()
        f.Close()

    def mergeAndSaveResults(self):
        f = ROOT.TFile(self.outputFileMap, "recreate")
        for cut_cat in list(self.results.keys()):
            _cut_cat = f.mkdir(cut_cat)
            for var in list(self.results[cut_cat].keys()):
                if "tree" in self.variables[var].keys():
                    # no need to process SnapShots
                    continue
                _cut_cat.mkdir(var)
                f.cd("/" + cut_cat + "/" + var)
                for sampleName in list(self.results[cut_cat][var].keys()):
                    # should first merge histos
                    mergedHistos = {}
                    for index in list(self.results[cut_cat][var][sampleName].keys()):
                        for hname in list(
                            self.results[cut_cat][var][sampleName][index].keys()
                        ):
                            if hname not in mergedHistos.keys():
                                mergedHistos[hname] = self.results[cut_cat][var][
                                    sampleName
                                ][index][hname].Clone()
                            else:
                                mergedHistos[hname].Add(
                                    self.results[cut_cat][var][sampleName][index][hname]
                                )

                    for hname in mergedHistos.keys():
                        if hname == "nominal":
                            mergedHistos[hname].SetName("histo_" + sampleName)
                        else:
                            mergedHistos[hname].SetName(
                                "histo_" + sampleName + "_" + hname
                            )
                        mergedHistos[hname].Write()
        f.Close()

    def run(self):
        """
        Runs the analysis:

        1. load the aliases without the ``afterNuis`` option
        2. load the ``suffix`` systematics

        3. load the alias ``weight``
        4. load the reweight systematics (they need the ``weight`` to be defined)

        5. finally load the suffix systematics with the ``afterNuis`` option


        After this important procedure it filters with ``preselection`` the many ``dfs``, loads systematics
        loads ``variables``, creates the results dict, splits the samples, creates the cuts/var histos, runs the dataframes
        and saves results.
        """
        # load all aliases needed before nuisances of type suffix
        self.loadAliases()
        self.loadSystematicsSuffix()

        # load alias weight needed before nuisances of type weight
        self.loadAliasWeight()
        self.loadSystematicsReweights()

        # load all aliases remaining
        self.loadAliases(True)

        # apply preselections
        for sampleName in self.dfs.keys():
            for index in self.dfs[sampleName].keys():
                self.dfs[sampleName][index]["df"] = self.dfs[sampleName][index][
                    "df"
                ].Filter("(" + self.preselections + ") && abs(weight) > 0.0")

        self.loadVariables()
        self.loadBranches()
        print("loaded all variables")
        self.createResults()
        print("created empty results dict")
        self.splitSubsamples()
        print("splitted samples")
        self.create_cuts_vars()
        print("created cuts")

        """
        # FIXME RunGraphs can't handle results of VaraitionsFor, ask Vincenzo about it

        # collect all the dataframes and run them
        dfs = []
        for cut in self.cuts.keys():
            for var in self.variables.keys():
                for sampleName in self.dfs.keys():
                    for index in self.dfs[sampleName].keys():
                        # dfs.append(self.results[cut][var][sampleName][index])
                        dfs.extend(
                            list(self.results[cut][var][sampleName][index].values()))
        ROOT.RDF.RunGraphs(dfs)
        """

        counts = []
        # register number of events in each df
        for sampleName in self.dfs.keys():
            for index in self.dfs[sampleName].keys():
                counts.append(self.dfs[sampleName][index]["df"].Count())

        snapshots = []
        for cut in self.cuts.keys():
            for var in self.variables.keys():
                if (
                    len(self.results[cut].get(var, [])) == 0
                    or "tree" not in self.variables[var].keys()
                ):
                    # no snapshots for this combination of cut variable
                    continue

                for sampleName in self.dfs.keys():
                    for index in self.dfs[sampleName].keys():
                        # dfs.append(self.results[cut][var][sampleName][index])
                        snapshots.append(self.results[cut][var][sampleName][index])

        if len(snapshots) != 0:
            ROOT.RDF.RunGraphs(snapshots)

        for count in counts:
            print("Number of events passing preselections:", count.GetValue())

        self.convertResults()
        self.saveResults()


if __name__ == "__main__":
    ROOT.gInterpreter.Declare('#include "headers.hh"')
    exec(open("script.py").read())
    runner = RunAnalysis(samples, aliases, variables, cuts, nuisances, lumi)
    runner.run()
