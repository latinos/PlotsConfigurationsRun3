# Configuration file to produce initial root files -- has both merged and binned ggH samples

treeName = 'Events'
tag = 'RPV_ForNNTraining'
runnerFile = 'default'

# used by mkShape to define output directory for root files
# outputDir = 'rootFile_' + tag

outputFile    = "mkShapes__{}.root".format(tag)
outputFolder  = "rootFiles__{}".format(tag)
batchFolder   = 'condor'
configsFolder = 'configs'

# file with TTree aliases
aliasesFile = 'aliases.py'

# file with list of variables
variablesFile = 'variables.py'

# file with list of cuts
cutsFile = 'cuts.py' 

# file with list of samples
samplesFile = 'samples.py' 

# file with list of samples
plotFile = 'plot.py' 

# luminosity to normalize to (in 1/fb)
# https://github.com/latinos/LatinoAnalysis/blob/UL_production/NanoGardener/python/data/TrigMaker_cfg.py#L868 (874)
#  59.832475339
lumi =  59.83

# used by mkPlot to define output directory for plots
# different from "outputDir" to do things more tidy
#outputDirPlots = 'plots_' + tag
plotPath = 'plots_' + tag

# used by mkDatacards to define output directory for datacards
outputDirDatacard = 'datacards'

# structure file for datacard
structureFile = 'structure.py'

# nuisances file for mkDatacards and for mkShape
nuisancesFile = 'nuisances.py'

minRatio = 0.5
maxRatio = 1.5
plotPath      = "plots__{}".format(tag)

mountEOS=[]
imports = ["os", "glob", ("collections", "OrderedDict"), "ROOT"]
filesToExec = [
    samplesFile,
    aliasesFile,
    variablesFile,
    cutsFile,
    plotFile,
    nuisancesFile,
    structureFile,
]

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

batchVars = varsToKeep[varsToKeep.index("samples") :]

varsToKeep += ['minRatio', 'maxRatio', 'plotPath']
