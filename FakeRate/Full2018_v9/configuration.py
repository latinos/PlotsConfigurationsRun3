# Configuration file for fake rate measurement using the UL 2018 dataset

# Tag used to identify the configuration folder version
tag = 'Fake_Full2018_v9'

# File to use as runner script, default uses mkShapesRDF.shapeAnalysis.runner, otherwise specify path to script
runnerFile = "default"

# Output file name
outputFile = "mkShapes__{}.root".format(tag)

# Path to ouput folder
outputFolder = "/eos/user/" + os.getlogin()[0] + "/" + os.getlogin() + "/mkShapesRDF_rootfiles/" + tag + "/rootFile/"
if 'portal' in os.uname()[1]:
    outputFolder = '/ceph/' + os.getlogin() + "/mkShapesRDF_rootfiles/" + tag + "/rootFile/"

# Path to batch folder (used for condor submission)
batchFolder = "condor"

# Path to configuration folder (will contain all the compiled configuration files)
configsFolder = "configs"

# Luminosity to normalize to (in 1/fb)
lumi = 1

# File with dict of aliases to define
aliasesFile = "aliases.py"

# File with dict of variables
variablesFile = "variables.py"

# File with dict of cuts
cutsFile = "cuts.py"

# File with dict of samples
samplesFile = "samples.py"

# File with dict of samples for plotting
plotFile = 'plot.py' 

# File with dict of structure (used to define processes in combine)
structureFile = "structure.py"

# Nuisances file for mkDatacards and for mkShape
nuisancesFile = "nuisances.py"

# Path to folder where to save plots
plotPath = 'plots_' + tag

# This lines are executed right before the runner on the condor node
mountEOS = []

# List of imports to import when compiling the whole configuration folder, it should not contain imports used by configuration.py
imports = ["os", "glob", ("collections", "OrderedDict"), "ROOT"]

# List of files to compile
filesToExec = [
    samplesFile,
    aliasesFile,
    variablesFile,
    cutsFile,
    plotFile,
    nuisancesFile,
    structureFile,
]

# List of variables to keep in the compiled configuration folder
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
]

# List of variables to keep in the batch submission script (script.py)
batchVars = varsToKeep[varsToKeep.index("samples") :]

varsToKeep += ['plotPath']
