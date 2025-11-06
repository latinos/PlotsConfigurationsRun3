# Configuration file for charge asymmetry WHSS analysis using the UL 2016HIPM dataset

import sys,inspect

# Site definition
site = 'cern'
if any(machine in os.uname()[1] for machine in ['portal','bms']):
    site = 'kit'

# /afs/cern.ch/user/n/ntrevisa/work/latinos/Run3/PlotsConfigurationsRun3/WH_chargeAsymmetry/UL/2016HIPM_v9/WHSS/configuration_2j
configurations_nuisance = os.path.realpath(inspect.getfile(inspect.currentframe())) # this file
configurations_nuisance = os.path.dirname(configurations_nuisance) # configuration_2j
configurations_nuisance = os.path.dirname(configurations_nuisance) # WHSS
configurations_nuisance = os.path.dirname(configurations_nuisance) # 2016HIPM_v9
configurations_nuisance = os.path.dirname(configurations_nuisance) # UL

# Tag used to identify the configuration folder version
tag = 'WHSS_2016HIPM_v9_chargeAsymmetry_Mu82_EleUL90'

# File to use as runner script, default uses mkShapesRDF.shapeAnalysis.runner, otherwise specify path to script
runnerFile = "default"

# Output file name
outputFile = "plots_WHSS_2016HIPM_v9_chargeAsymmetry_Mu82_EleUL90_DYflip_data.root" # "mkShapes__{}.root".format(tag)

# Path to ouput folder
outputFolder = "/eos/user/" + os.getlogin()[0] + "/" + os.getlogin() + "/mkShapesRDF_rootfiles/" + tag + "/rootFile/"
if site == 'kit':
    outputFolder = '/ceph/' + os.getlogin() + "/mkShapesRDF_rootfiles/" + tag + "/rootFile/"

# Path to batch folder (used for condor submission)
batchFolder = "condor"

# Path to configuration folder (will contain all the compiled configuration files)
configsFolder = "configs"

# luminosity to normalize to (in 1/fb)
# https://github.com/latinos/LatinoAnalysis/blob/UL_production/NanoGardener/python/data/TrigMaker_cfg.py#L27 (#95 #165)
# 16.802739097 + 1.063261220 + 1.655228036 = 19.521228353 
lumi = 19.52

# File with dict of aliases to define
aliasesFile = "../aliases.py"

# File with dict of variables
variablesFile = "../variables.py"

# File with dict of cuts
cutsFile = "cuts.py"

# File with dict of samples
samplesFile = "samples.py"

# File with dict of samples for plotting
plotFile = 'plot.py' 

# File with dict of structure (used to define processes in combine)
structureFile = "structure.py"

# Nuisances file for mkDatacards and for mkShape
nuisancesFile = "../nuisances.py"

# Path to folder where to save plots
plotPath = '../plots_' + tag

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
