from mkShapesRDF.lib.search_files import SearchFiles

searchFiles = SearchFiles()

redirector = ""
useXROOTD = False
dataset_samples = 'amassiro'

# MC:   /eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer22_130x_nAODv12_Full2022v12/MCl2loose2022v12__MCCorr2022v12JetScaling__l2tight
# DATA: /eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Run2022_ReReco_nAODv12_Full2022v12/DATAl2loose2022v12__l2tight

if dataset_samples == 'calderon':
    mcProduction = 'Summer22_130x_nAODv12_Full2022v12'
    mcSteps      = 'MCl2loose2022v12__MCCorr2022v12JetScaling__sblancof__l2tight'  # Using DYJetsToLL_M-50-LO from Calderon (DS, 22Nov25)
    dataReco     = 'Run2022_ReReco_nAODv12_Full2022v12'
    dataSteps    = 'DATAl2loose2022v12__sblancof__l2loose'
elif dataset_samples == 'amassiro':
    mcProduction = 'Summer22_130x_nAODv12_Full2022v12_OLD'
    mcSteps      = 'MCl2loose2022v12__MCCorr2022v12JetScaling__l2tight' # Using DYto2L-2Jets_MLL-50 from Amassiro (DS, 21Nov25)
    dataReco     = 'Run2022_ReReco_nAODv12_Full2022v12_OLD'
    dataSteps    = 'DATAl2loose2022v12__l2tight'

# fakeSteps    = 'DATAl1loose2022EFGv12__fakeW'

##############################################
###### Tree base directory for the site ######
##############################################
treeBaseDir = f'/eos/cms/store/group/phys_higgs/cmshww/{dataset_samples}/HWWNano'
limitFiles = -1 # For running on smaller set of samples (DS, 21Nov25)

def makeMCDirectory(var=""):
    _treeBaseDir = treeBaseDir + ""
    if redirector != "":
        _treeBaseDir = redirector + treeBaseDir
    if var == "":
        return "/".join([_treeBaseDir, mcProduction, mcSteps])
    else:
        return "/".join([_treeBaseDir, mcProduction, mcSteps + "__" + var])


mcDirectory   = makeMCDirectory()
# fakeDirectory = os.path.join(treeBaseDir, dataReco, fakeSteps)
dataDirectory = os.path.join(treeBaseDir, dataReco, dataSteps)

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
]

# ['E','Run2022E-Prompt-v1'],
# ['F','Run2022F-Prompt-v1'],
# ['G','Run2022G-Prompt-v1'],

DataSets = ['MuonEG','SingleMuon','Muon','EGamma']

# Putting for later: HLT selections (DS, 19Nov25)
DataTrig = {
    'MuonEG'         : ' Trigger_ElMu' ,
    'SingleMuon'     : '!Trigger_ElMu && Trigger_sngMu' ,
    'Muon'           : '!Trigger_ElMu && (Trigger_sngMu || Trigger_dblMu)',
    'EGamma'         : '!Trigger_ElMu && !Trigger_sngMu && !Trigger_dblMu && (Trigger_sngEl || Trigger_dblEl)'
}


#########################################
############ MC COMMON ##################
#########################################

# SFweight does not include btag weights
mcCommonWeightNoMatch = 'XSWeight*METFilter_Common*SFweight'
mcCommonWeight        = 'XSWeight*METFilter_Common*PromptGenLepMatch2l*SFweight'

#mcCommonWeight = 'XSWeight*METFilter_Common*SFweight'

###########################################
#############  BACKGROUNDS  ###############
###########################################

# DY
if dataset_samples == 'calderon':
    files = nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-50-LO')
elif dataset_samples == 'amassiro':
    files = nanoGetSampleFiles(mcDirectory, 'DYto2L-2Jets_MLL-50')


samples['DY'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 2,
}

# remove backgrounds from data for ZpT reweighting:
top_samples = ['TTTo2L2Nu', 'TWminusto2L2Nu', 'TbarWplusto2L2Nu']#, 'ST_tW_top']
diboson_samples = ['WWTo2L2Nu', 'WZTo3LNu', 'GluGlutoContintoWWtoENuENu', 'GluGlutoContintoWWtoENuMuNu', 'GluGlutoContintoWWtoENuTauNu', 'GluGlutoContintoWWtoMuNuENu', 'GluGlutoContintoWWtoMuNuMuNu', 'GluGlutoContintoWWtoMuNuTauNu', 'GluGlutoContintoWWtoTauNuENu', 'GluGlutoContintoWWtoTauNuMuNu', 'GluGlutoContintoWWtoTauNuTauNu', 'WGtoLNuG-1J_PTG10to100', 'WGtoLNuG-1J_PTG100to200', 'WGtoLNuG-1J_PTG200to400', 'WGtoLNuG-1J_PTG400to600', 'WGtoLNuG-1J_PTG600']
higgs_samples = ['GluGluHToWWTo2L2Nu_M125', 'VBFHToWWTo2L2Nu_M125']

samples['top'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'TTTo2L2Nu') + \
            nanoGetSampleFiles(mcDirectory, 'TWminusto2L2Nu') + \
            nanoGetSampleFiles(mcDirectory, 'TbarWplusto2L2Nu'),
    'weight': mcCommonWeight,
    'FilesPerJob': 2,
}

samples['diboson'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'WWTo2L2Nu') + \
            nanoGetSampleFiles(mcDirectory, 'WZTo3LNu') + \
            nanoGetSampleFiles(mcDirectory, 'GluGlutoContintoWWtoENuENu') + \
            nanoGetSampleFiles(mcDirectory, 'GluGlutoContintoWWtoENuMuNu') + \
            nanoGetSampleFiles(mcDirectory, 'GluGlutoContintoWWtoENuTauNu') + \
            nanoGetSampleFiles(mcDirectory, 'GluGlutoContintoWWtoMuNuENu') + \
            nanoGetSampleFiles(mcDirectory, 'GluGlutoContintoWWtoMuNuMuNu') + \
            nanoGetSampleFiles(mcDirectory, 'GluGlutoContintoWWtoMuNuTauNu') + \
            nanoGetSampleFiles(mcDirectory, 'GluGlutoContintoWWtoTauNuENu') + \
            nanoGetSampleFiles(mcDirectory, 'GluGlutoContintoWWtoTauNuMuNu') + \
            nanoGetSampleFiles(mcDirectory, 'GluGlutoContintoWWtoTauNuTauNu') + \
            nanoGetSampleFiles(mcDirectory, 'WGtoLNuG-1J_PTG10to100') + \
            nanoGetSampleFiles(mcDirectory, 'WGtoLNuG-1J_PTG100to200') + \
            nanoGetSampleFiles(mcDirectory, 'WGtoLNuG-1J_PTG200to400') + \
            nanoGetSampleFiles(mcDirectory, 'WGtoLNuG-1J_PTG400to600') + \
            nanoGetSampleFiles(mcDirectory, 'WGtoLNuG-1J_PTG600'),
    'weight': mcCommonWeight,
    'FilesPerJob': 2,
}

samples['SMhiggs'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'GluGluHToWWTo2L2Nu_M125') + \
            nanoGetSampleFiles(mcDirectory, 'VBFHToWWTo2L2Nu_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 2,
}


###########################################
################## DATA ###################
###########################################

samples['DATA'] = { 
    'name': [],  
    'weight': 'LepWPCut*METFilter_DATA',     
    'weights': [], 
    'isData': ['all'], 
    'FilesPerJob': 15 
} 

for _, sd in DataRun:
  for pd in DataSets:
    datatag = pd + '_' + sd

    if (pd == "SingleMuon" and _ in ["D"]) or (pd == "Muon" and _ == "B"):
        continue
    files = nanoGetSampleFiles(dataDirectory, datatag)
    
    print(datatag)

    samples['DATA']['name'].extend(files)
    addSampleWeight(samples, 'DATA', datatag, DataTrig[pd])
