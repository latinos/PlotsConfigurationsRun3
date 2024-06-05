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
                        if nuisance["folderUp"] in usedFolders or nuisance["folderUp"]=="":
                            continue
                        usedFolders.append(nuisance["folderUp"])

                        friendsFiles += RunAnalysis.getNuisanceFiles(nuisance, files)

            tnom = RunAnalysis.getTTreeNomAndFriends(files, friendsFiles)
            
            #### --------- FIXME : Not needed if correct jets used
            self.inputFiles = tnom 

            if limit != -1:
                df = ROOT.RDataFrame(tnom)
                df = df.Range(limit)
            else:
                #ROOT.EnableImplicitMT()
                ROOT.EnableImplicitMT(1)
                df = ROOT.RDataFrame(tnom)


            ###### FIXME
            df = recomputeJets(self, df)
                
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
                        #ROOT.gInterpreter.Declare(
                        #    line.replace("RPLME_nThreads", str(df.GetNSlots()))
                        #)
                        ROOT.gROOT.ProcessLineSync(
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
        print("Loading systematic suffix!!!")
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


def recomputeJets(self, df):

    import correctionlib
    correctionlib.register_pyroot_binding()

    ### Jet maker

    ROOT.gInterpreter.Declare(
        """
        ROOT::RVecI sortedIndices(ROOT::RVecF variable){
        // return sortedIndices based on variable
        return Reverse(Argsort(variable));
        }
        """
    )

    
    df = df.Define("isMyCleanJet", "ROOT::RVecB(Jet_pt.size(), true)")

    df = df.Define("MyCleanJet_pt", "Jet_pt[isMyCleanJet]")
    df = df.Define("MyCleanJet_sorting", "sortedIndices(MyCleanJet_pt)")

    df = df.Define("MyCleanJet_jetIdx", "ROOT::VecOps::Range(nJet)[isMyCleanJet]")
    df = df.Redefine("MyCleanJet_jetIdx", "Take(MyCleanJet_jetIdx, MyCleanJet_sorting)")
    CleanJet_var = ["eta", "phi", "mass"]
    for prop in CleanJet_var:
        df = df.Define(f"MyCleanJet_{prop}", f"Jet_{prop}[isMyCleanJet]")
        df = df.Redefine(
            f"MyCleanJet_{prop}", f"Take(MyCleanJet_{prop}, MyCleanJet_sorting)"
        )


    ## LeptonSel

    ROOT.gInterpreter.Declare(
        """
        using namespace ROOT;
        using namespace ROOT::VecOps;
        
        ROOT::RVecB reduce_cond_any(ROOT::RVecB condition, uint size1, uint size2){
            ROOT::RVecB r;
            for (uint i = 0; i < size1; i++){
                bool c = false;
                for (uint j = 0; j < size2; j++){
                    if (condition[i * size2 + j]){
                        c = true;
                        break;
                    }
                }
                r.push_back(c);
            }
            return r;
        }

        RVecB propagateMask(RVecI Lepton_origIdx, RVecB mask, bool defaultValue){
        RVecB r {};

            for (uint i = 0; i < Lepton_origIdx.size(); i++){
                if (Lepton_origIdx[i] < 0){
                    r.push_back(defaultValue);
                } else {
                    r.push_back(mask[Lepton_origIdx[i]]);
                }
            }
            assert (Lepton_origIdx.size() == r.size());
            return r;
        /*
        does not work, why?
        RVecB r(Lepton_origIdx.size(), defaultValue);
        r[Lepton_origIdx >= 0] = Take(mask, Lepton_origIdx[Lepton_origIdx >= 0]);
        return r;
        */
        }
        """
    )
    
    df = df.Define(
            "LeptonMask_JC",
            "Lepton_pt >= 10",
    )
    df = df.Define("MyCleanJetMask", "MyCleanJet_eta <= 5.0")
    
    df = df.Define(
        "MyCleanJet_Lepton_comb",
        "ROOT::VecOps::Combinations(MyCleanJet_pt[MyCleanJetMask].size(), Lepton_pt[LeptonMask_JC].size())",
    )
        
    df = df.Define(
        "dR2",
        "ROOT::VecOps::DeltaR2( \
        Take(MyCleanJet_eta, MyCleanJet_Lepton_comb[0]), \
        Take(Lepton_eta, MyCleanJet_Lepton_comb[1]), \
        Take(MyCleanJet_phi, MyCleanJet_Lepton_comb[0]), \
        Take(Lepton_phi, MyCleanJet_Lepton_comb[1]) \
        )",
    )
        
    df = df.Define(
        "MyCleanJet_pass",
        "! reduce_cond_any(dR2<(0.3*0.3), MyCleanJet_pt[MyCleanJetMask].size(), Lepton_pt[LeptonMask_JC].size())",
    )
    
    branches = ["jetIdx", "pt", "eta", "phi", "mass"]

    for prop in branches:
        df = df.Redefine(
            f"MyCleanJet_{prop}", f"MyCleanJet_{prop}[MyCleanJetMask][MyCleanJet_pass]"
        )

    
    #### JetSel

    df = df.Redefine(
        "MyCleanJetMask",
        "MyCleanJet_pt >= 15.0 && MyCleanJet_eta <= 4.7 && Take(Jet_jetId, MyCleanJet_jetIdx) >= 2",
    )

    
    print(self.samples[0][1][0])
    isData = False
    isEE = False
    if "Run2022EE" in self.samples[0][1][0]:
        isData = True
        isEE = True
        pathToJson = "/afs/cern.ch/user/n/ntrevisa/work/latinos/Run3/mkShapesRDF/mkShapesRDF/processor/data/jetvetomaps/Run2022/jetvetomaps.json"
        globalTag = "Summer22EE_23Sep2023_RunEFG_V1"

    elif "Run2022_" in self.samples[0][1][0]:
        isData = True
        pathToJson = "/afs/cern.ch/user/n/ntrevisa/work/latinos/Run3/mkShapesRDF/mkShapesRDF/processor/data/jetvetomaps/Run2022/jetvetomaps.json"
        globalTag = "Summer22_23Sep2023_RunCD_V1"
        
    elif "Summer22EE" in self.samples[0][1][0]:
        isEE = True
        pathToJson = "/afs/cern.ch/user/n/ntrevisa/work/latinos/Run3/mkShapesRDF/mkShapesRDF/processor/data/jetvetomaps/Run2022/jetvetomaps.json"
        globalTag = "Summer22EE_23Sep2023_RunEFG_V1"

        JEC_era = "Summer22EE_22Sep2023_V2_MC"
        JER_era = "Summer22EEPrompt22_JRV1_MC"
        jet_object = "AK4PFPuppi"
        met_collections = ["PuppiMET", "MET", "RawMET"]
                
    else:
        pathToJson = "/afs/cern.ch/user/n/ntrevisa/work/latinos/Run3/mkShapesRDF/mkShapesRDF/processor/data/jetvetomaps/Run2022/jetvetomaps.json"
        globalTag = "Summer22_23Sep2023_RunCD_V1"

        JEC_era = "Summer22_22Sep2023_V2_MC"
        JER_era = "JR_Winter22Run3_V1_MC"
        jet_object = "AK4PFPuppi"
        met_collections = ["PuppiMET", "MET", "RawMET"]
        

    ROOT.gROOT.ProcessLine(
        f"""
        auto jetMaskFile = correction::CorrectionSet::from_file("{pathToJson}");
        correction::Correction::Ref cset_jet_Map = (correction::Correction::Ref) jetMaskFile->at("{globalTag}");
        """
    )


    ROOT.gInterpreter.Declare(
        """
        ROOT::RVecB getJetMask(ROOT::RVecF CleanJet_pt,ROOT::RVecF CleanJet_eta, ROOT::RVecF CleanJet_phi, ROOT::RVecF Jet_neEmEF,ROOT::RVecF Jet_chEmEF,ROOT::RVecI CleanJet_jetIdx){
            float tmp_value;
            float cleanJet_EM;
            float eta, phi;
            RVecB CleanJet_isNotVeto = RVecB(CleanJet_pt.size(), true);
            for (int i=0; i<CleanJet_pt.size(); i++){
                    phi = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{CleanJet_phi[i], 3.1415}), -3.1415});
                    eta = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{CleanJet_eta[i], 5.19}), -5.19});
                    
                    cleanJet_EM = Jet_neEmEF[CleanJet_jetIdx[i]] + Jet_chEmEF[CleanJet_jetIdx[i]];
                    tmp_value = cset_jet_Map->evaluate({"jetvetomap", eta, phi});
                    
                    if (cleanJet_EM<0.9 && CleanJet_pt[i]>15.0 && tmp_value!=0.0){
                            CleanJet_isNotVeto[i] = false;
                    }
            }
            return CleanJet_isNotVeto;
        }
        """
    )

    if isEE:
        ROOT.gInterpreter.Declare(
            """
            bool getEventMask(ROOT::RVecF CleanJet_pt,ROOT::RVecF CleanJet_eta, ROOT::RVecF CleanJet_phi, ROOT::RVecF Jet_neEmEF,ROOT::RVecF Jet_chEmEF,ROOT::RVecI CleanJet_jetIdx){
                float tmp_value;
                float cleanJet_EM;
                float eta,phi;
                for (int i=0; i<CleanJet_pt.size(); i++){
                        phi = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{CleanJet_phi[i], 3.1415}), -3.1415});
                        eta = ROOT::VecOps::Max(ROOT::RVecF{ROOT::VecOps::Min(ROOT::RVecF{CleanJet_eta[i], 5.19}), -5.19});
                        
                        cleanJet_EM = Jet_neEmEF[CleanJet_jetIdx[i]] + Jet_chEmEF[CleanJet_jetIdx[i]];
                        tmp_value = cset_jet_Map->evaluate({"jetvetomap_eep", eta, phi});
                        if (cleanJet_EM<0.9 && CleanJet_pt[i]>15.0 && tmp_value!=0.0){
                                return false;
                        }
                }
                return true;
            }
            """
        )
        
    df = df.Redefine(
        "MyCleanJetMask",
        "MyCleanJetMask && getJetMask(MyCleanJet_pt,MyCleanJet_eta,MyCleanJet_phi,Jet_neEmEF,Jet_chEmEF,MyCleanJet_jetIdx)"
    )

    
    if isEE:
        df = df.Define(
            "MyCleanEventMask",
            "getEventMask(MyCleanJet_pt,MyCleanJet_eta,MyCleanJet_phi,Jet_neEmEF,Jet_chEmEF,MyCleanJet_jetIdx)"
        )
        
        df = df.Filter("MyCleanEventMask")

    
    branches = ["jetIdx", "pt", "eta", "phi", "mass"]
    for prop in branches:
        df = df.Redefine(f"MyCleanJet_{prop}", f"MyCleanJet_{prop}[MyCleanJetMask]")


    if isData:
        return df



    ### CMSJMECalculator

    from CMSJMECalculators.jetdatabasecache import JetDatabaseCache
    jecDBCache = JetDatabaseCache("JECDatabase", repository="cms-jet/JECDatabase")
    jrDBCache = JetDatabaseCache("JRDatabase", repository="cms-jet/JRDatabase")

    txtL1JEC = jecDBCache.getPayload(JEC_era, "L1FastJet", jet_object)

    txtJECs = []
    txtJECs.append(txtL1JEC)
    txtJECs.append(jecDBCache.getPayload(JEC_era, "L2Relative", jet_object))
    txtJECs.append(jecDBCache.getPayload(JEC_era, "L3Absolute", jet_object))
    txtJECs.append(jecDBCache.getPayload(JEC_era, "L2L3Residual", jet_object))

    txtUnc = jecDBCache.getPayload(
        JEC_era, "UncertaintySources", jet_object, ""
    )

    txtPtRes = jrDBCache.getPayload(JER_era, "PtResolution", jet_object)
    txtSF = jrDBCache.getPayload(JER_era, "SF", jet_object)
    print("Path for SF:", txtSF)

    from CMSJMECalculators import loadJMESystematicsCalculators

    loadJMESystematicsCalculators()

    
    ### MET
    
    MET = "PuppiMET"
    ROOT.gInterpreter.ProcessLine(
        f"Type1METVariationsCalculator my{MET}" + "VarCalc{}"
    )
    calcMET = getattr(ROOT, f"my{MET}VarCalc")
    calcMET.setUnclusteredEnergyTreshold(15.0)
    # redo JEC, push_back corrector parameters for different levels
    jecParams = getattr(ROOT, "std::vector<JetCorrectorParameters>")()
    for txtJEC in txtJECs:
        jecParams.push_back(ROOT.JetCorrectorParameters(txtJEC))
    calcMET.setJEC(jecParams)
    
    jecL1Params = getattr(ROOT, "std::vector<JetCorrectorParameters>")()
    jecL1Params.push_back(ROOT.JetCorrectorParameters(txtL1JEC))
    calcMET.setL1JEC(jecL1Params)
    # calculate JES uncertainties (repeat for all sources)
    
    with open(txtUnc) as f:
        lines = f.read().split("\n")
        sources = [
            x for x in lines if x.startswith("[") and x.endswith("]")
        ]
        sources = [x[1:-1] for x in sources]

    for s in sources:
        jcp_unc = ROOT.JetCorrectorParameters(txtUnc, s)
        calcMET.addJESUncertainty(s, jcp_unc)

    # Smear jets, with JER uncertainty
    calcMET.setSmearing(
        txtPtRes,
        txtSF,
        True,
        False,
        -1.0,
        -1.0,  # decorrelate for different regions
    )  # use hybrid recipe, matching parameters
    calcMET.setIsT1SmearedMET(True)
    
    jesSources = calcMET.available()
    print("DEBUG module")
    skip = 1
    skip += 6 * 2
    # first are JERs, last two are unclustered unc.
    jesSources = jesSources[skip:-2][::2]
    jesSources = list(map(lambda k: str(k)[3:-2], jesSources))
    # jesSources = sorted(jesSources)
    jesSources = list(map(lambda k: "JES" + k, jesSources))
    #print(jesSources)
    
    # list of columns to be passed to myJetVarCal produce
    cols = []
    
    JetColl = "newJet3"
    
    df = df.Define("newJet3_pt", "MyCleanJet_pt")
    df = df.Define("newJet3_eta", "MyCleanJet_eta")
    df = df.Define("newJet3_phi", "MyCleanJet_phi")
    df = df.Define("newJet3_jetIdx", "MyCleanJet_jetIdx")
    
    cols.append(f"{JetColl}_pt")
    cols.append(f"{JetColl}_eta")
    cols.append(f"{JetColl}_phi")
    cols.append(f"Take(Jet_mass, {JetColl}_jetIdx)")
    cols.append(f"Take(Jet_rawFactor, {JetColl}_jetIdx)")
    cols.append(f"Take(Jet_area, {JetColl}_jetIdx)")
    cols.append(f"Take(Jet_muonSubtrFactor, {JetColl}_jetIdx)")
    cols.append(f"Take(Jet_neEmEF, {JetColl}_jetIdx)")
    cols.append(f"Take(Jet_chEmEF, {JetColl}_jetIdx)")
    cols.append(f"Take(Jet_jetId, {JetColl}_jetIdx)")
    
    # rho
    cols.append("Rho_fixedGridRhoFastjetAll")
    
    cols.append(f"Take(Jet_partonFlavour, {JetColl}_jetIdx)")
    # seed
    cols.append(
        f"(run<<20) + (luminosityBlock<<10) + event + 1 + int({JetColl}_eta.size()>0 ? {JetColl}_eta[0]/.01 : 0)"
    )
    
    # gen jet coll
    cols.append("GenJet_pt")
    cols.append("GenJet_eta")
    cols.append("GenJet_phi")
    cols.append("GenJet_mass")
    
    RawMET = "RawMET" if "Puppi" not in MET else "RawPuppiMET"
    #RawMET = MET
    cols.append(f"{RawMET}_phi")
    cols.append(f"{RawMET}_pt")
    
    cols.append("MET_MetUnclustEnUpDeltaX")
    cols.append("MET_MetUnclustEnUpDeltaY")
    
    df = df.Redefine('EmptyLowPtJet', 'ROOT::RVecF{}')
    #for _ in range(5):
    #    cols.append('EmptyLowPtJet')
    cols.append("CorrT1METJet_rawPt")
    cols.append("CorrT1METJet_eta")
    cols.append("CorrT1METJet_phi")
    cols.append("CorrT1METJet_area")
    cols.append("CorrT1METJet_muonSubtrFactor")
    cols.append("ROOT::RVecF {}")
    cols.append("ROOT::RVecF {}")
    
    df = df.Define(
        f"{MET}Vars", f"my{MET}VarCalc.produce({', '.join(cols)})"
    )
    
    df = df.Redefine(f"{MET}_pt", f"{MET}Vars.pt(0)")
    df = df.Redefine(f"{MET}_phi", f"{MET}Vars.phi(0)")

    _sources = []        
    _sources = [f"JER_{i}" for i in range(6)]
    _sources += jesSources
    sources = _sources.copy()
    METsources = _sources.copy()
    METsources += ["MET"]  # last one is the unclustered variation

    #print("\n")
    #print("MET uncertainties: ")
    #print(METsources)

    for variable in [MET + "_pt", MET + "_phi"]:
        for i, source in enumerate(METsources):
            up = f"{MET}Vars.{variable.split('_')[-1]}({2*i+1})"
            do = f"{MET}Vars.{variable.split('_')[-1]}({2*i+1+1})"
            
            df = df.Define(
                variable + f"_{source}up",
                up
            )
            df = df.Define(
                variable + f"_{source}do",
                do
            )
                
            #df = df.Vary(
            #    variable,
            #    "ROOT::RVecD{" + up + ", " + do + "}",
            #    ["up", "do"],
            #    source,
            #)
    
    ### JER
       
    ROOT.gInterpreter.ProcessLine("JetVariationsCalculator myJetVarCalc{}")
    calc = getattr(ROOT, "myJetVarCalc")

    jecParams = getattr(ROOT, "std::vector<JetCorrectorParameters>")()
    for txtJEC in txtJECs:
        jecParams.push_back(ROOT.JetCorrectorParameters(txtJEC))
    calc.setJEC(jecParams)
    # calculate JES uncertainties (repeat for all sources)
    
    with open(txtUnc) as f:
        lines = f.read().split("\n")
        sources = [x for x in lines if x.startswith("[") and x.endswith("]")]
        sources = [x[1:-1] for x in sources]
        
    for s in sources:
        jcp_unc = ROOT.JetCorrectorParameters(txtUnc, s)
        calc.addJESUncertainty(s, jcp_unc)
    
    calc.setSmearing(
        txtPtRes,
        txtSF,
        True,
        False,
        -1.0,
        -1.0,
    )
    jesSources = calc.available()
    skip = 1
    skip += 6 * 2
    jesSources = jesSources[skip:][::2]
    jesSources = list(map(lambda k: str(k)[3:-2], jesSources))
    jesSources = list(map(lambda k: "JES" + k, jesSources))
    
    # list of columns to be passed to myJetVarCal produce
    cols = []

    # nre reco jet coll
    JetColl = "newJet2"
    
    df = df.Define(f"{JetColl}_pt", "MyCleanJet_pt")
    df = df.Define(f"{JetColl}_eta", "MyCleanJet_eta")
    df = df.Define(f"{JetColl}_phi", "MyCleanJet_phi")
    df = df.Define(f"{JetColl}_jetIdx", "MyCleanJet_jetIdx")

    cols.append(f"{JetColl}_pt")
    cols.append(f"{JetColl}_eta")
    cols.append(f"{JetColl}_phi")
    cols.append("MyCleanJet_mass")
    cols.append(f"Take(Jet_rawFactor, {JetColl}_jetIdx)")
    cols.append(f"Take(Jet_area, {JetColl}_jetIdx)")
    cols.append(f"Take(Jet_jetId, {JetColl}_jetIdx)")
    
    # rho
    cols.append("Rho_fixedGridRhoFastjetAll")
    
    cols.append(f"Take(Jet_partonFlavour, {JetColl}_jetIdx)")
    
    # seed
    cols.append(
        f"(run<<20) + (luminosityBlock<<10) + event + 1 + int({JetColl}_eta.size()>0 ? {JetColl}_eta[0]/.01 : 0)"
    )

    # gen jet coll
    cols.append("GenJet_pt")
    cols.append("GenJet_eta")
    cols.append("GenJet_phi")
    cols.append("GenJet_mass")
    
    df = df.Define("jetVars", f'myJetVarCalc.produce({", ".join(cols)})')

    df = df.Redefine("MyCleanJet_pt", "jetVars.pt(0)")
    df = df.Redefine("MyCleanJet_mass", "jetVars.mass(0)")
    
    df = df.Redefine(
        "MyCleanJet_sorting",
        "ROOT::VecOps::Reverse(ROOT::VecOps::Argsort(MyCleanJet_pt))",
    )
    
    df = df.Redefine("MyCleanJet_pt", "Take( MyCleanJet_pt, MyCleanJet_sorting)")
    df = df.Redefine("MyCleanJet_eta", "Take( MyCleanJet_eta, MyCleanJet_sorting)")
    df = df.Redefine("MyCleanJet_phi", "Take( MyCleanJet_phi, MyCleanJet_sorting)")
    df = df.Redefine("MyCleanJet_mass", "Take( MyCleanJet_mass, MyCleanJet_sorting)")
    df = df.Redefine("MyCleanJet_jetIdx", "Take( MyCleanJet_jetIdx, MyCleanJet_sorting)")    

    _sources = []
    _sources = [f"JER_{i}" for i in range(6)]
    _sources += jesSources
    sources = _sources.copy()

    #print("\n")
    #print("JES uncertainties: ")
    #print(sources)
    
    for i, source in enumerate(sources):
        
        variations_pt = []
        variations_jetIdx = []
        variations_mass = []
        variations_phi = []
        variations_eta = []
        for j, tag in enumerate(["up", "down"]):
            variation_pt = f"jetVars.pt({2*i+1+j})"
            variation_mass = f"jetVars.mass({2*i+1+j})"
            df = df.Define(
                f"tmp_CleanJet_pt__JES_{source}_{tag}",
                variation_pt,
            )
            df = df.Define(
                f"tmp_CleanJet_pt__JES_{source}_{tag}_sorting",
                f"ROOT::VecOps::Reverse(ROOT::VecOps::Argsort(tmp_CleanJet_pt__JES_{source}_{tag}))",
            )
            variations_pt.append(
                f"Take(tmp_CleanJet_pt__JES_{source}_{tag}, tmp_CleanJet_pt__JES_{source}_{tag}_sorting)"
            )
            
            df = df.Define(
                f"MyCleanJet_cleanJetIdx_preJES_{source}_{tag}",
                f"tmp_CleanJet_pt__JES_{source}_{tag}_sorting",
            )
            
            variations_jetIdx.append(
                f"Take({JetColl}_jetIdx, tmp_CleanJet_pt__JES_{source}_{tag}_sorting)",
            )
            
            df = df.Define(
                f"tmp_CleanJet_mass__JES_{source}_{tag}",
                f"Take({variation_mass}, tmp_CleanJet_pt__JES_{source}_{tag}_sorting)",
            )
            variations_mass.append(f"tmp_CleanJet_mass__JES_{source}_{tag}")
            
            variations_phi.append(
                f"Take({JetColl}_phi, tmp_CleanJet_pt__JES_{source}_{tag}_sorting)"
            )
            variations_eta.append(
                f"Take({JetColl}_eta, tmp_CleanJet_pt__JES_{source}_{tag}_sorting)"
            )

            
        tags = ["up", "do"]
        
        df = df.Define(
            f"MyCleanJet_pt_{source}up",
            variations_pt[0]
        )
        df = df.Define(
	    f"MyCleanJet_pt_{source}do",
            variations_pt[1]
	)    

        df = df.Define(
            f"MyCleanJet_eta_{source}up",
            variations_eta[0]
        )
        df = df.Define(
            f"MyCleanJet_eta_{source}do",
            variations_eta[1]
        )

        df = df.Define(
            f"MyCleanJet_phi_{source}up",
            variations_phi[0]
        )
        df = df.Define(
            f"MyCleanJet_phi_{source}do",
            variations_phi[1]
        )

        df = df.Define(
            f"MyCleanJet_jetIdx_{source}up",
            variations_jetIdx[0]
        )
        df = df.Define(
            f"MyCleanJet_jetIdx_{source}do",
            variations_jetIdx[1]
        )

        df = df.Define(
            f"MyCleanJet_mass_{source}up",
            variations_mass[0]
        )
        df = df.Define(
            f"MyCleanJet_mass_{source}do",
            variations_mass[1]
        )

        '''
        df = df.Vary(
            "MyCleanJet_pt",
            "ROOT::RVec<ROOT::RVecF>{"
            + variations_pt[0]
            + ", "
            + variations_pt[1]
            + "}",
            tags,
            source,
        )
        
        df = df.Vary(
            "MyCleanJet_jetIdx",
            "ROOT::RVec<ROOT::RVecI>{" + variations_jetIdx[0]
            # + "CleanJet_jetIdx"
            + ", " + variations_jetIdx[1]
            # + "CleanJet_jetIdx"
            + "}",
            tags,
            source,
        )
        
        df = df.Vary(
            "MyCleanJet_mass",
            "ROOT::RVec<ROOT::RVecF>{" + variations_mass[0]
            # + "CleanJet_mass"
            + ", " + variations_mass[1]
            # + "CleanJet_mass"
            + "}",
            tags,
            source,
        )
        
        df = df.Vary(
            "MyCleanJet_phi",
            "ROOT::RVec<ROOT::RVecF>{" + variations_phi[0]
            # + "CleanJet_phi"
            + ", " + variations_phi[1]
            # + "CleanJet_phi"
            + "}",
            tags,
            source,
        )
        
        df = df.Vary(
            "MyCleanJet_eta",
            "ROOT::RVec<ROOT::RVecF>{" + variations_eta[0]
            # + "CleanJet_eta"
            + ", " + variations_eta[1]
            # + "CleanJet_eta"
            + "}",
            tags,
            source,
        )
        '''
        
    if isEE:
        era = 2022
        algo = "deepJet"
        selectedWPs = ["shape"]
        jesSystsForShape = ["jes","jesAbsoluteStat","jesAbsoluteScale","jesAbsoluteMPFBias","jesFragmentation","jesSinglePionECAL","jesSinglePionHCAL","jesFlavorQCD",
                            "jesRelativeJEREC1","jesRelativeJEREC2","jesRelativeJERHF","jesRelativePtBB","jesRelativePtEC1","jesRelativePtEC2","jesRelativePtHF","jesRelativeBal",
                            "jesRelativeSample","jesRelativeFSR","jesRelativeStatFSR","jesRelativeStatEC","jesRelativeStatHF","jesPileUpDataMC","jesPileUpPtRef","jesPileUpPtBB",
                            "jesPileUpPtEC1","jesPileUpPtEC2","jesPileUpPtHF"]

        mode = "shape"
        pathToJson = "/afs/cern.ch/user/n/ntrevisa/work/latinos/Run3/mkShapesRDF/mkShapesRDF/processor/data/scale_factors_BTV/Full2022EEv12/btagging_Summer22EE.json"

    else:

        era = 2022
        algo = "deepJet"
        selectedWPs = ["shape"]
        jesSystsForShape = ["jes","jesAbsoluteStat","jesAbsoluteScale","jesAbsoluteMPFBias","jesFragmentation","jesSinglePionECAL","jesSinglePionHCAL","jesFlavorQCD",
                            "jesRelativeJEREC1","jesRelativeJEREC2","jesRelativeJERHF","jesRelativePtBB","jesRelativePtEC1","jesRelativePtEC2","jesRelativePtHF","jesRelativeBal",
                            "jesRelativeSample","jesRelativeFSR","jesRelativeStatFSR","jesRelativeStatEC","jesRelativeStatHF","jesPileUpDataMC","jesPileUpPtRef","jesPileUpPtBB",
                            "jesPileUpPtEC1","jesPileUpPtEC2","jesPileUpPtHF"]

        mode = "shape"
        pathToJson = "/afs/cern.ch/user/n/ntrevisa/work/latinos/Run3/mkShapesRDF/mkShapesRDF/processor/data/scale_factors_BTV/Full2022v12/btagging_Summer22.json"
                                                                     



    max_abs_eta = """2.49999"""
    min_pt = """20.0001"""

    branch_algo = {"deepJet": "Jet_btagDeepFlavB", "particleNet": "Jet_btagPNetB", "robustParticleTransformer": "Jet_btagRobustParTAK4B"}
    branch_sfalgo = {"deepJet": "deepjet", "particleNet": "partNet", "robustParticleTransformer": "partTransformer"}
    
    branch_name = branch_algo[algo]
    branch_sfname = branch_sfalgo[algo]


    systs = []
    systs.append("up")
    systs.append("down")
    central_and_systs = ["central"]
    central_and_systs.extend(systs)
    
    systs_shape_corr = []
    for syst in [
            "lf",
            "hf",
            "hfstats1",
            "hfstats2",
            "lfstats1",
            "lfstats2",
            "cferr1",
            "cferr2"] + jesSystsForShape:
        systs_shape_corr.append("up_%s" % syst)
        systs_shape_corr.append("down_%s" % syst)
        central_and_systs_shape_corr = ["central"]
        central_and_systs_shape_corr.extend(systs_shape_corr)

    shape_syst = [
            "lf",
            "hf",
            "hfstats1",
            "hfstats2",
            "lfstats1",
            "lfstats2",
            "cferr1",
            "cferr2",
        ] + jesSystsForShape


    cset_btag_name = f"cset_btag_{era}_{mode}_{algo}"
    cset_btag_sf_name = f"cset_btag_sf_{era}_{mode}_{algo}"

    inputFileName = pathToJson
    
    if not hasattr(ROOT, cset_btag_name):
        # check if cset_btag is already defined
        
        ROOT.gROOT.ProcessLine(
            f"""
            auto {cset_btag_name} = correction::CorrectionSet::from_file("{inputFileName}");
            """
        )
        
    ### Load the correction given algo and mode  # noqa: E266
    if not hasattr(ROOT, cset_btag_sf_name):
        # check if cset_btag_sf is already defined
        s = f"""
        correction::Correction::Ref {cset_btag_sf_name} = (correction::Correction::Ref) {cset_btag_name}->at("{algo}_{mode}");
        """
    else:
        # if already defined store the new cset_btag_sf
        s = f"""
        {cset_btag_sf_name} = (correction::Correction::Ref) {cset_btag_name}->at("{algo}_{mode}");
        """


    ROOT.gROOT.ProcessLine(s)

    suffix = f"{mode}_{algo}"
    getbtagSF_shape_name = f"getbtagSF_shape_{suffix}"
    getbtagSF_wp_name = f"getbtagSF_wp_name_{suffix}"

    if mode == "shape":
        if not hasattr(ROOT, getbtagSF_shape_name):
            ROOT.gInterpreter.Declare(
                "ROOT::RVecF "
                + getbtagSF_shape_name
                + """
                (std::string syst, ROOT::RVecI flav, ROOT::RVecF eta, ROOT::RVecF pt, ROOT::RVecF btag){
                ROOT::RVecF sf(pt.size(), 1.0);
                
                for (unsigned int i = 0, n = pt.size(); i < n; ++i) {
                if (pt[i]<"""
                + min_pt
                + """ || abs(eta[i])>"""
                + max_abs_eta
                + """ || btag[i]<0.0 || isnan(btag[i]) || btag[i]>19.999){continue;}
                if (syst.find("jes") != std::string::npos && flav[i]!=0){continue;}
                if (syst.find("cferr") != std::string::npos){
                if (flav[i]==4){
                auto sf_tmp = """+cset_btag_sf_name+"""->evaluate({syst, abs(flav[i]), abs(eta[i]), pt[i], btag[i]});
                sf[i] = float(sf_tmp);
                }else{
                continue;
                }
                }else if (syst.find("hf") != std::string::npos || syst.find("lf") != std::string::npos){
                if (flav[i]==4){
                continue;
                }else{
                auto sf_tmp = """+cset_btag_sf_name+"""->evaluate({syst, abs(flav[i]), abs(eta[i]), pt[i], btag[i]});
                sf[i] = float(sf_tmp);
                }
                }else{
                auto sf_tmp = """+cset_btag_sf_name+"""->evaluate({syst, abs(flav[i]), abs(eta[i]), pt[i], btag[i]});
                sf[i] = float(sf_tmp);
                }
                }
                return sf;
                }
                """
            )

        for central_or_syst in central_and_systs_shape_corr:
            if central_or_syst == "central":
                df = df.Redefine(
                    f"Jet_btagSF_{branch_sfname}_shape",
                    f'{getbtagSF_shape_name}("{central_or_syst}", Jet_hadronFlavour, Jet_eta, Jet_pt, {branch_name})',
                )
            else:
                df = df.Redefine(
                    f"Jet_btagSF_{branch_sfname}_shape_{central_or_syst}",
                    f'{getbtagSF_shape_name}("{central_or_syst}", Jet_hadronFlavour, Jet_eta, Jet_pt, {branch_name})',
                )

                





    
    return df
    
if __name__ == "__main__":
    ROOT.gInterpreter.Declare('#include "headers.hh"')
    exec(open("script.py").read())
    runner = RunAnalysis(samples, aliases, variables, cuts, nuisances, lumi)
    runner.run()
