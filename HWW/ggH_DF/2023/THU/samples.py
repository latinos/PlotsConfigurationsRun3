from mkShapesRDF.lib.search_files import SearchFiles
import os
import inspect
import sys

configurations = os.path.realpath(inspect.getfile(inspect.currentframe()))

searchFiles = SearchFiles()

redirector = ""
useXROOTD = False

mcProduction = 'Summer23_130x_nAODv12_Full2023v12'
mcSteps      = 'MCl2loose2023v12__MCCorr2023v12JetScaling__l2tight'
dataReco     = 'Run2023_Prompt_nAODv12_Full2023v12'
dataSteps    = 'DATAl2loose2023v12__l2loose'
fakeSteps    = 'DATAl2loose2023v12__l2loose'

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


mcDirectory   = makeMCDirectory()


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
    ['C','Run2024C-ReReco-v1'],
    ['D','Run2024D-ReReco-v1'],
    ['E','Run2024E-ReReco-v1'],
    ['F','Run2024F-Prompt-v1'],
    ['G','Run2024G-Prompt-v1'],
    ['H','Run2024H-Prompt-v1'],
    ['Iv1','Run2024I-Prompt-v1'],
    ['Iv2','Run2024I-Prompt-v2'],
]


DataSets = ['MuonEG','Muon0','Muon1','EGamma0','EGamma1']

DataTrig = {
    'MuonEG'  : 'Trigger_ElMu' ,
    'Muon0'   : '!Trigger_ElMu && (Trigger_sngMu || Trigger_dblMu)',
    'Muon1'   : '!Trigger_ElMu && (Trigger_sngMu || Trigger_dblMu)',
    'EGamma0' : '!Trigger_ElMu && !Trigger_sngMu && !Trigger_dblMu && (Trigger_sngEl || Trigger_dblEl)',
    'EGamma1' : '!Trigger_ElMu && !Trigger_sngMu && !Trigger_dblMu && (Trigger_sngEl || Trigger_dblEl)',
}

#########################################
############ MC COMMON ##################
#########################################

mcCommonWeight         = 'XSWeight'


# ggH
files = nanoGetSampleFiles(mcDirectory, 'GluGluHToWWTo2L2Nu_M125')

samples['ggH_hww'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 20,
}

# VBF
files = nanoGetSampleFiles(mcDirectory, 'VBFHToWWTo2L2Nu_M125')

samples['qqH_hww'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 20,
}