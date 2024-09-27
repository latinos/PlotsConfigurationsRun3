from mkShapesRDF.lib.search_files import SearchFiles

searchFiles = SearchFiles()

redirector = ""
useXROOTD  = False

# Data and MC directories
mcProduction = 'Summer22EE_130x_nAODv12_Full2022v12'
mcSteps      = 'MCl2loose2022EEv12__MCCorr2022EEv12__lepID'
# dataReco     = 'Run2022EE_Prompt_nAODv12_Full2022v12'
# fakeSteps    = 'DATAl1loose2022EFGv12__fakeW'
# dataSteps    = 'DATAl2loose2022EEv12__l2tight'

##############################################
###### Tree base directory for the site ######
##############################################
treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'

limitFiles = -1

def makeMCDirectory(var=""):
    _treeBaseDir = treeBaseDir + ""
    if redirector != "":
        _treeBaseDir = redirector + treeBaseDir
    if var == "":
        return "/".join([_treeBaseDir, mcProduction, mcSteps])
    else:
        return "/".join([_treeBaseDir, mcProduction, mcSteps + "__" + var])


mcDirectory = makeMCDirectory()
#fakeDirectory = os.path.join(treeBaseDir, dataReco, fakeSteps)
#dataDirectory = os.path.join(treeBaseDir, dataReco, dataSteps)

samples = {}

def nanoGetSampleFiles(path, name):
    _files = searchFiles.searchFiles(path, name, redirector=redirector)
    if limitFiles != -1 and len(_files) > limitFiles:
        return [(name, _files[:limitFiles])]
    else:
        return [(name, _files)]


def CombineBaseW(samples, proc, samplelist):
    _filtFiles = list(filter(lambda k: k[0] in samplelist, samples[proc]["name"]))
    _files = list(map(lambda k: k[1], _filtFiles))
    _l = list(map(lambda k: len(k), _files))
    leastFiles = _files[_l.index(min(_l))]
    dfSmall = ROOT.RDataFrame("Runs", leastFiles)
    s = dfSmall.Sum("genEventSumw").GetValue()
    f = ROOT.TFile(leastFiles[0])
    t = f.Get("Events")
    t.GetEntry(1)
    xs = t.baseW * s

    __files = []
    for f in _files:
        __files += f
    df = ROOT.RDataFrame("Runs", __files)
    s = df.Sum("genEventSumw").GetValue()
    newbaseW = str(xs / s)
    weight = newbaseW + "/baseW"

    for iSample in samplelist:
        addSampleWeight(samples, proc, iSample, weight)


def addSampleWeight(samples, sampleName, sampleNameType, weight):
    obj = list(filter(lambda k: k[0] == sampleNameType, samples[sampleName]["name"]))[0]
    samples[sampleName]["name"] = list(
        filter(lambda k: k[0] != sampleNameType, samples[sampleName]["name"])
    )
    if len(obj) > 2:
        samples[sampleName]["name"].append(
            (obj[0], obj[1], obj[2] + "*(" + weight + ")")
        )
    else:
        samples[sampleName]["name"].append((obj[0], obj[1], "(" + weight + ")"))


################################################
############ DATA DECLARATION ##################
################################################

DataRun = [
    ['B','Run2022B-ReReco-v1'],
    ['C','Run2022C-ReReco-v1'],
    ['D','Run2022D-ReReco-v1'],
    ['E','Run2022E-Prompt-v1'],
    ['F','Run2022F-Prompt-v1'],
    ['G','Run2022G-Prompt-v1'],
]

DataSets = ['MuonEG','SingleMuon','Muon','EGamma']

DataTrig = {
    'MuonEG'         : ' Trigger_ElMu' ,
    'SingleMuon'     : '!Trigger_ElMu && Trigger_sngMu' ,
    'Muon'           : '!Trigger_ElMu && (Trigger_sngMu || Trigger_dblMu)',
    'EGamma'         : '!Trigger_ElMu && !Trigger_sngMu && !Trigger_dblMu && (Trigger_sngEl || Trigger_dblEl)'
}


#########################################
############ MC COMMON ##################
#########################################

# Overall SF weights
mcCommonWeight = 'XSWeight*METFilter_Common'

###########################################
############### BACKGROUNDS ###############
###########################################

### W + Jets
files = nanoGetSampleFiles(mcDirectory, 'WToLNu-2Jets')

samples['WJets'] = {
    'name'        : files,
    'weight'      : mcCommonWeight,
    'FilesPerJob' : 2,
}

### Top SemiLeptonic
files = nanoGetSampleFiles(mcDirectory, 'TTToSemiLeptonic')

samples['TTToSemiLeptonic'] = {
    'name'        : files,
    'weight'      : mcCommonWeight,
    'FilesPerJob' : 2,
}

#####################################
############ SIGNALS  ###############
#####################################

### WW
files = nanoGetSampleFiles(mcDirectory, 'WWTo2L2Nu')

samples['WW'] = {
    'name'        : files,
    'weight'      : mcCommonWeight,
    'FilesPerJob' : 2,
}

###### ggF Higgs #######
files = nanoGetSampleFiles(mcDirectory, 'GluGluHToWWTo2L2Nu_M125')

samples['ggH_hww'] = {
    'name'        : files,
    'weight'      : mcCommonWeight,
    'FilesPerJob' : 2,
}
