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
fakeDirectoryMuon = os.path.join(treeBaseDir, dataRecoMuon, dataSteps)
dataDirectoryMuon = os.path.join(treeBaseDir, dataRecoMuon, dataSteps)
fakeDirectoryEGamma = os.path.join(treeBaseDir, dataRecoEGamma, dataSteps)
dataDirectoryEGamma = os.path.join(treeBaseDir, dataRecoEGamma, dataSteps)
fakeDirectoryMuonEG = os.path.join(treeBaseDir, dataRecoMuonEG, dataSteps)
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
    'MuonEG'   : 'Trigger_ElMu' ,
    'Muon0'    : '!Trigger_ElMu && (Trigger_sngMu || Trigger_dblMu)',
    'Muon1'    : '!Trigger_ElMu && (Trigger_sngMu || Trigger_dblMu)',
    'EGamma0'  : '!Trigger_ElMu && !Trigger_sngMu && !Trigger_dblMu && (Trigger_sngEl || Trigger_dblEl)',
    'EGamma1'  : '!Trigger_ElMu && !Trigger_sngMu && !Trigger_dblMu && (Trigger_sngEl || Trigger_dblEl)',
}

#########################################
############ MC COMMON ##################
#########################################

# SFweight does not include btag weights
mcCommonWeight1Match = 'XSWeight*METFilter_Common*PromptGenLepMatch1l*SFweight'
mcCommonWeight2Match = 'XSWeight*METFilter_Common*PromptGenLepMatch2l*SFweight'
mcCommonWeight       = 'XSWeight*METFilter_Common*PromptGenLepMatch3l*SFweight'


###########################################
#############  BACKGROUNDS  ###############
###########################################

# DY
files = nanoGetSampleFiles(mcDirectory, 'DYto2E-2Jets_MLL-10to50') + \
        nanoGetSampleFiles(mcDirectory, 'DYto2Mu-2Jets_MLL-10to50') + \
        nanoGetSampleFiles(mcDirectory, 'DYto2Tau-2Jets_MLL-10to50') +\
        nanoGetSampleFiles(mcDirectory, 'DYto2E-2Jets_MLL-50') + \
        nanoGetSampleFiles(mcDirectory, 'DYto2Mu-2Jets_MLL-50') + \
        nanoGetSampleFiles(mcDirectory, 'DYto2Tau-2Jets_MLL-50')

samples['DY'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 50
}

# top
files = nanoGetSampleFiles(mcDirectory, 'TTTo2L2Nu') + \
        nanoGetSampleFiles(mcDirectory, 'TbarWplusto2L2Nu') + \
        nanoGetSampleFiles(mcDirectory, 'TWminusto2L2Nu') + \
        nanoGetSampleFiles(mcDirectory, 'ST_t-channel_top') + \
        nanoGetSampleFiles(mcDirectory, 'ST_t-channel_antitop')

samples['top'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 30,
}

addSampleWeight(samples,'top','TTTo2L2Nu','Top_pTrw')

# WW and ggWW
files = nanoGetSampleFiles(mcDirectory, 'WWTo2L2Nu')

samples['WW'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 50,
}

files = nanoGetSampleFiles(mcDirectory, 'GluGlutoContintoWWtoENuENu') + \
        nanoGetSampleFiles(mcDirectory, 'GluGlutoContintoWWtoENuMuNu') + \
        nanoGetSampleFiles(mcDirectory, 'GluGlutoContintoWWtoENuTauNu') + \
        nanoGetSampleFiles(mcDirectory, 'GluGlutoContintoWWtoMuNuENu') + \
        nanoGetSampleFiles(mcDirectory, 'GluGlutoContintoWWtoMuNuMuNu') + \
        nanoGetSampleFiles(mcDirectory, 'GluGlutoContintoWWtoMuNuTauNu') + \
        nanoGetSampleFiles(mcDirectory, 'GluGlutoContintoWWtoTauNuENu') + \
        nanoGetSampleFiles(mcDirectory, 'GluGlutoContintoWWtoTauNuMuNu') + \
        nanoGetSampleFiles(mcDirectory, 'GluGlutoContintoWWtoTauNuTauNu')

samples['ggWW'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 50,
}

# WZ
files = nanoGetSampleFiles(mcDirectory, 'WZTo3LNu')

samples['WZ'] = {
    'name': files,
    'weight': mcCommonWeight + ' * (Gen_ZGstar_mass >= 50)',
    'FilesPerJob': 30,
}

files = nanoGetSampleFiles(mcDirectory, 'ZZ')

samples['ZZ'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 5,
}

### Vg/Vgstar

# Wg
files = nanoGetSampleFiles(mcDirectory, 'WGtoLNuG-1J_PTG100')

samples['Wg'] = {
    'name': files,
    'weight': mcCommonWeight1Match + '*(Gen_ZGstar_mass <= 0)',
    'FilesPerJob': 30,
}

# Zg
files = nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_Bin-MLL-50') + \
        nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_Bin-MLL-4to50')

samples['Zg'] = {
    'name': files,
    'weight': mcCommonWeight2Match + '*(Gen_ZGstar_mass <= 0)',
    'FilesPerJob': 30,
}

# WgS
files = nanoGetSampleFiles(mcDirectory, 'WGtoLNuG-1J_PTG100') + \
        nanoGetSampleFiles(mcDirectory, "WZTo3LNu")

samples['WgS'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 30,
}

addSampleWeight(samples, 'WgS', "WGtoLNuG-1J_PTG100", "(Gen_ZGstar_mass > 0  && Gen_ZGstar_mass < 4)")
addSampleWeight(samples, 'WgS', "WZTo3LNu",           "(Gen_ZGstar_mass >= 4 && Gen_ZGstar_mass < 50)")

# ZgS
files = nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_Bin-MLL-50') + \
        nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_Bin-MLL-4to50')

samples['ZgS'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 30,
}

addSampleWeight(samples, 'ZgS', "DYGto2LG-1Jets_Bin-MLL-50",    "(Gen_ZGstar_mass > 0  && Gen_ZGstar_mass < 4)")
addSampleWeight(samples, 'ZgS', "DYGto2LG-1Jets_Bin-MLL-4to50", "(Gen_ZGstar_mass > 0  && Gen_ZGstar_mass < 4)")


# Multiboson
files = nanoGetSampleFiles(mcDirectory, 'WWW') + \
        nanoGetSampleFiles(mcDirectory, 'WWZ') + \
        nanoGetSampleFiles(mcDirectory, 'WZZ') + \
        nanoGetSampleFiles(mcDirectory, 'ZZZ')  

samples['VVV'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 5,
}


# # ggH
# files = nanoGetSampleFiles(mcDirectory, 'GluGluHToWWTo2L2Nu_M125')

# samples['ggH_hww'] = {
#     'name': files,
#     'weight': mcCommonWeight,
#     'FilesPerJob': 10,
# }

# # VBF
# files = nanoGetSampleFiles(mcDirectory, 'VBFHToWWTo2L2Nu_M125')

# samples['qqH_hww'] = {
#     'name': files,
#     'weight': mcCommonWeight,
#     'FilesPerJob': 10,
# }

###########################################
################## DATA ###################
###########################################

samples['DATA'] = { 
    'name': [],  
    'weight': 'LepWPCut*METFilter_DATA',     
    'weights': [], 
    'isData': ['all'], 
    'FilesPerJob': 100
} 

for _, sd in DataRun:
  for pd in DataSets:
    datatag = pd + '_' + sd

    if datatag.startswith('MuonEG'):
        files = nanoGetSampleFiles(dataDirectoryMuonEG, datatag)
    elif datatag.startswith('Muon'):
        files = nanoGetSampleFiles(dataDirectoryMuon, datatag)
    elif datatag.startswith('EGamma'):
        files = nanoGetSampleFiles(dataDirectoryEGamma, datatag)
    
    print(datatag)

    samples['DATA']['name'].extend(files)
    addSampleWeight(samples, 'DATA', datatag, DataTrig[pd])

###########################################
################## FAKE ###################
###########################################

samples['Fake'] = {
    'name': [],
    'weight': 'METFilter_DATA*fakeW',
    'weights': [],
    'isData': ['all'],
    'FilesPerJob': 100
}

for _, sd in DataRun:
  for pd in DataSets:
    datatag = pd + '_' + sd

    if datatag.startswith('MuonEG'):
        files = nanoGetSampleFiles(fakeDirectoryMuonEG, datatag)
    elif datatag.startswith('Muon'):
        files = nanoGetSampleFiles(fakeDirectoryMuon, datatag)
    elif datatag.startswith('EGamma'):
        files = nanoGetSampleFiles(fakeDirectoryEGamma, datatag)

    samples['Fake']['name'].extend(files)
    addSampleWeight(samples, 'Fake', datatag, DataTrig[pd])

