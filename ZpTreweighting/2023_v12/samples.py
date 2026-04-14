from mkShapesRDF.lib.search_files import SearchFiles

searchFiles = SearchFiles()
redirector = ""

useXROOTD = False

# MC:   /eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer22_130x_nAODv12_Full2022v12/MCl2loose2022v12__MCCorr2022v12JetScaling__l2tight
# DATA: /eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Run2022_ReReco_nAODv12_Full2022v12/DATAl2loose2022v12__l2tight
mcProduction = 'Summer23_130x_nAODv12_Full2023v12_OLD' # new datasets were produced around 11Apr26, using old datasets to compare with prior results (DS, 13Apr26)
mcSteps      = 'MCl2loose2023v12__MCCorr2023v12JetScaling__l2tight' # Using DYto2L-2Jets_MLL-50 from Amassiro (DS, 21Nov25)
dataReco     = 'Run2023_Prompt_nAODv12_Full2023v12_OLD'  # new datasets were produced around 11Apr26, using old datasets to compare with prior results (DS, 13Apr26)
dataSteps    = 'DATAl2loose2023v12__l2loose' # Choose l2loose sample but apply tight selections in analysis (eleWP and muWP)

# fakeSteps    = 'DATAl1loose2022EFGv12__fakeW'

##############################################
###### Tree base directory for the site ######
##############################################
treeBaseDir = f'/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'
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

# Putting for later: HLT selections (DS, 19Nov25)
DataRun = [
    ['Cv1','Run2023C-Prompt-v1'],
    ['Cv2','Run2023C-Prompt-v2'],
    ['Cv3','Run2023C-Prompt-v3'],
    ['Cv4','Run2023C-Prompt-v4'],
]


DataSets = ['MuonEG','Muon0','Muon1','EGamma0','EGamma1']

DataTrig = {
    'MuonEG'          : 'Trigger_ElMu' ,
    'Muon0'           : '!Trigger_ElMu && (Trigger_sngMu || Trigger_dblMu)',
    'Muon1'           : '!Trigger_ElMu && (Trigger_sngMu || Trigger_dblMu)',
    'EGamma0'         : '!Trigger_ElMu && !Trigger_sngMu && !Trigger_dblMu && (Trigger_sngEl || Trigger_dblEl)',
    'EGamma1'         : '!Trigger_ElMu && !Trigger_sngMu && !Trigger_dblMu && (Trigger_sngEl || Trigger_dblEl)'
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
files = nanoGetSampleFiles(mcDirectory, 'DYto2L-2Jets_MLL-50')


samples['DY'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 2,
}

addSampleWeight(samples,'DY','DYto2L-2Jets_MLL-50','DY_NLO_ZpTrw')

# remove backgrounds from data for ZpT reweighting:
top_samples = ['TTTo2L2Nu', 'TWminusto2L2Nu', 'TbarWplusto2L2Nu']#, 'ST_tW_top']
diboson_samples = ['WWTo2L2Nu', 'WZTo3LNu', 'GluGlutoContintoWWtoENuENu', 'GluGlutoContintoWWtoENuMuNu', 'GluGlutoContintoWWtoENuTauNu', 'GluGlutoContintoWWtoMuNuENu', 'GluGlutoContintoWWtoMuNuMuNu', 'GluGlutoContintoWWtoMuNuTauNu', 'GluGlutoContintoWWtoTauNuENu', 'GluGlutoContintoWWtoTauNuMuNu', 'GluGlutoContintoWWtoTauNuTauNu', 'WGtoLNuG-1J_PTG10to100', 'WGtoLNuG-1J_PTG100to200', 'WGtoLNuG-1J_PTG200to400', 'WGtoLNuG-1J_PTG400to600', 'WGtoLNuG-1J_PTG600']
higgs_samples = ['GluGluHToWWTo2L2Nu_M125', 'VBFHToWWTo2L2Nu_M125']

samples['top'] = {
    'name': 
            nanoGetSampleFiles(mcDirectory, 'ST_t-channel_top') + \
            nanoGetSampleFiles(mcDirectory, 'ST_t-channel_antitop') + \
            nanoGetSampleFiles(mcDirectory, 'ST_s-channel_plus') + \
            nanoGetSampleFiles(mcDirectory, 'ST_s-channel_minus') + \
            nanoGetSampleFiles(mcDirectory, 'ST_tW_top') + \
            nanoGetSampleFiles(mcDirectory, 'ST_tW_antitop') + \
            nanoGetSampleFiles(mcDirectory, 'TTTo2L2Nu') + \
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

    files = nanoGetSampleFiles(dataDirectory, datatag)
    
    print(datatag)

    samples['DATA']['name'].extend(files)
    addSampleWeight(samples, 'DATA', datatag, DataTrig[pd])

