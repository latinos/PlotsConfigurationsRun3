"""
Configuration file for mkShapesRDF script.

It's the only necessary python configuration file, all the other files are imported and defined by this one.

"""

#: tag used to identify the configuration folder version
tag = "new_vbf_16"

#: file to use as runner script, default uses mkShapesRDF.shapeAnalysis.runner, otherwise specify path to script
runnerFile = "default"

#: output file name
outputFile = "mkShapes__{}.root".format(tag)

#: path to ouput folder
outputFolder = "rootFiles"
#: path to batch folder (used for condor submission)
batchFolder = "condor"

#: path to configuration folder (will contain all the compiled configuration files)
configsFolder = "configs"

#: luminosity to normalize to (in 1/fb)
lumi = 36.33


#: file with dict of aliases to define
aliasesFile = "aliases.py"

#: file with dict of variables
variablesFile = "variables.py"

#: file with dict of cuts
cutsFile = "cuts.py"

#: file with dict of samples
samplesFile = "samples.py"

#: file with dict of samples
plotFile = "plot.py"

#: file with dict of structure (used to define combine processes)
structureFile = "structure.py"

# nuisances file for mkDatacards and for mkShape
nuisancesFile = "nuisances.py"

# minRatio = 0.5
# maxRatio = 1.5
# plotPath = "/eos/user/g/gpizzati/www/rdf/2016/"

#: path to folder where to save plots
plotPath = "plots"

#: this lines are executed right before the runner on the condor node
mountEOS = [
    # "export KRB5CCNAME=/home/gpizzati/krb5\n",
]

#: list of imports to import when compiling the whole configuration folder, it should not contain imports used by configuration.py
imports = ["os", "glob", ("collections", "OrderedDict"), "ROOT"]

#: list of files to compile
filesToExec = [
    samplesFile,
    aliasesFile,
    variablesFile,
    cutsFile,
    plotFile,
    nuisancesFile,
    structureFile,
]

#: list of variables to keep in the compiled configuration folder
varsToKeep = [
    "batchVars",
    "outputFolder",
    "batchFolder",
    "configsFolder",
    "outputFile",
    "runnerFile",
    "tag",
    "samples",
    "aliases",
    "variables",
    ("cuts", {"cuts": "cuts", "preselections": "preselections"}),
    ("plot", {"plot": "plot", "groupPlot": "groupPlot", "legend": "legend"}),
    "nuisances",
    "structure",
    "lumi",
    "mountEOS",
]

#: list of variables to keep in the batch submission script (script.py)
batchVars = varsToKeep[varsToKeep.index("samples") :]


varsToKeep += ['plotPath']
