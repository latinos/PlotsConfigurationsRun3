from mkShapesRDF.lib.search_files import SearchFiles

searchFiles = SearchFiles()

redirector = ""
useXROOTD = False

mcProduction   = 'Summer24_150x_nAODv15_Full2024v15'
mcSteps        = 'MCl2loose2024v15__MCCorr2024v15__JERFrom23BPix__l2tight'
dataRecoMuon   = 'Run2024_ReRecoCDE_PromptFGHI_nAODv15_Full2024v15_Muon'
dataRecoEGamma = 'Run2024_ReRecoCDE_PromptFGHI_nAODv15_Full2024v15_EGamma'
dataRecoMuonEG = 'Run2024_ReRecoCDE_PromptFGHI_nAODv15_Full2024v15_MuonEG'
dataSteps      = 'DATAl2loose2024v15__l2loose'

##############################################
###### Tree base directory for the site ######
##############################################
treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'
treeBaseSignalDir = '/eos/user/m/mwulansa/mkShapesRDF_signalPostProcessingMay2026'

# limitFiles = -1
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
dataDirectoryMuon = os.path.join(treeBaseDir, dataRecoMuon, dataSteps)
dataDirectoryEGamma = os.path.join(treeBaseDir, dataRecoEGamma, dataSteps)
dataDirectoryMuonEG = os.path.join(treeBaseDir, dataRecoMuonEG, dataSteps)

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
    ['I','Run2024I-Prompt-v1'],
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

# SFweight does not include btag weights
mcCommonWeightNoMatch = 'XSWeight*METFilter_Common*SFweight'
mcCommonWeight        = 'XSWeight*METFilter_Common*PromptGenLepMatch2l*SFweight'

#mcCommonWeight = 'XSWeight*METFilter_Common*SFweight'


#########################################                                                                                                                      
############ SIGNAL ##################                                                                                                                    
#########################################                                                                                                                    

signalDirectory = "/".join([treeBaseSignalDir, mcProduction, mcSteps])

files = nanoGetSampleFiles(signalDirectory, 'WminusH_WtoLNu_Hto2WtoLNu2Q_M-125')
samples['WminusH'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 1,
}

# files = nanoGetSampleFiles(signalDirectory, 'WplusH_WtoLNu_Hto2WtoLNu2Q_M-125')
# samples['WplusH'] = {
#     'name': files,
#     'weight': mcCommonWeight,
#     'FilesPerJob': 1,
# }

# ###########################################
# #############  BACKGROUNDS  ###############
# ###########################################

# # DY

# files = nanoGetSampleFiles(mcDirectory, 'DYto2E-2Jets_MLL-50') + \
#         nanoGetSampleFiles(mcDirectory, 'DYto2Mu-2Jets_MLL-50') + \
#         nanoGetSampleFiles(mcDirectory, 'DYto2Tau-2Jets_MLL-50')

# samples['DY'] = {
#     'name': files,
#     'weight': mcCommonWeight,
#     'FilesPerJob': 80,
# }

# # Top

# files = nanoGetSampleFiles(mcDirectory, 'TTTo2L2Nu') + \
#         nanoGetSampleFiles(mcDirectory, 'TbarWplusto2L2Nu') + \
#         nanoGetSampleFiles(mcDirectory, 'TWminusto2L2Nu') + \
#         nanoGetSampleFiles(mcDirectory, 'ST_t-channel_antitop') + \
#         nanoGetSampleFiles(mcDirectory, 'ST_t-channel_top')

# samples['top'] = {
#     'name': files,
#     'weight': mcCommonWeight,
#     'FilesPerJob': 50,
# }


# # WW
# files = nanoGetSampleFiles(mcDirectory, 'WWTo2L2Nu')

# samples['WW'] = {
#     'name': files,
#     'weight': mcCommonWeight,
#     'FilesPerJob': 20,
# }

# # WZ
# files = nanoGetSampleFiles(mcDirectory, 'WZTo3LNu')

# samples['WZ'] = {
#     'name': files,
#     'weight': mcCommonWeight,
#     'FilesPerJob': 2,
# }

# ###########################################
# ################## DATA ###################
# ###########################################

# samples['DATA'] = { 
#     'name': [],  
#     'weight': 'LepWPCut*METFilter_DATA',     
#     'weights': [], 
#     'isData': ['all'], 
#     'FilesPerJob': 15 
# } 

# for _, sd in DataRun:
#   for pd in DataSets:
#     datatag = pd + '_' + sd

#     if 'Muon' in datatag:
#         files = nanoGetSampleFiles(dataDirectoryMuon, datatag)
#     if 'EGamma' in datatag:
#         files = nanoGetSampleFiles(dataDirectoryEGamma, datatag)
#     if 'MuonEG' in datatag:
#         files = nanoGetSampleFiles(dataDirectoryMuonEG, datatag)
    
#     print(datatag)

#     samples['DATA']['name'].extend(files)
#     addSampleWeight(samples, 'DATA', datatag, DataTrig[pd])
