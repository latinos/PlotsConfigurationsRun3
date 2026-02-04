from mkShapesRDF.lib.search_files import SearchFiles

searchFiles = SearchFiles()

redirector = ""
useXROOTD = False

mcProduction = 'Summer23BPix_130x_nAODv12_Full2023BPixv12'
mcSteps      = 'MCl2loose2023BPixv12__MCCorr2023BPixv12JetScaling__l2tight'
dataReco     = 'Run2023BPix_Prompt_nAODv12_Full2023BPixv12'
dataSteps    = 'DATAl2loose2023BPixv12__l2loose'
fakeSteps    = 'DATAl2loose2023BPixv12__l2loose'

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
fakeDirectory = os.path.join(treeBaseDir, dataReco, fakeSteps)
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
    ['Dv1','Run2023D-Prompt-v1'],
    ['Dv2','Run2023D-Prompt-v2'],
]


DataSets = ['MuonEG','Muon0','Muon1','EGamma0','EGamma1']

DataTrig = {
    'MuonEG'         : 'Trigger_ElMu' ,
    'Muon0'           : '!Trigger_ElMu && (Trigger_sngMu || Trigger_dblMu)',
    'Muon1'           : '!Trigger_ElMu && (Trigger_sngMu || Trigger_dblMu)',
    'EGamma0'         : '!Trigger_ElMu && !Trigger_sngMu && !Trigger_dblMu && (Trigger_sngEl || Trigger_dblEl)',
    'EGamma1'         : '!Trigger_ElMu && !Trigger_sngMu && !Trigger_dblMu && (Trigger_sngEl || Trigger_dblEl)',
}

#########################################
############ MC COMMON ##################
#########################################

# SFweight does not include btag weights
mcCommonWeightNoMatch = 'XSWeight*METFilter_Common*SFweight'
mcCommonWeight        = 'XSWeight*METFilter_Common*PromptGenLepMatch2l*SFweight'


###########################################
#############  BACKGROUNDS  ###############
###########################################

# DY
files = nanoGetSampleFiles(mcDirectory, 'DYto2L-2Jets_MLL-50')
#files = nanoGetSampleFiles(mcDirectory, 'DYto2Tau-2Jets_MLL-50_0J') + \
#        nanoGetSampleFiles(mcDirectory, 'DYto2Tau-2Jets_MLL-50_1J') + \
#        nanoGetSampleFiles(mcDirectory, 'DYto2Tau-2Jets_MLL-50_2J')

samples['DY'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 10,
    }

# top
files = nanoGetSampleFiles(mcDirectory, 'TTTo2L2Nu') + \
        nanoGetSampleFiles(mcDirectory, 'TbarWplusto2L2Nu') + \
        nanoGetSampleFiles(mcDirectory, 'TWminusto2L2Nu') + \
        nanoGetSampleFiles(mcDirectory, 'ST_t-channel_top') + \
        nanoGetSampleFiles(mcDirectory, 'ST_t-channel_antitop') + \
        nanoGetSampleFiles(mcDirectory, 'ST_s-channel_plus') + \
        nanoGetSampleFiles(mcDirectory, 'ST_s-channel_minus')

samples['top'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 15,
}

addSampleWeight(samples,'top','TTTo2L2Nu','Top_pTrw')

# WW and ggWW
files = nanoGetSampleFiles(mcDirectory, 'WWTo2L2Nu')

samples['WW'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 20,
}

files = nanoGetSampleFiles(mcDirectory, 'GluGlutoContintoWWtoENuENu') + \
    nanoGetSampleFiles(mcDirectory, 'GluGlutoContintoWWtoENuMuNu') + \
    nanoGetSampleFiles(mcDirectory, 'GluGlutoContintoWWtoENuTauNu') +	\
    nanoGetSampleFiles(mcDirectory, 'GluGlutoContintoWWtoMuNuENu') +	\
    nanoGetSampleFiles(mcDirectory, 'GluGlutoContintoWWtoMuNuMuNu') +	\
    nanoGetSampleFiles(mcDirectory, 'GluGlutoContintoWWtoMuNuTauNu') +	\
    nanoGetSampleFiles(mcDirectory, 'GluGlutoContintoWWtoTauNuENu') +	\
    nanoGetSampleFiles(mcDirectory, 'GluGlutoContintoWWtoTauNuMuNu') +	\
    nanoGetSampleFiles(mcDirectory, 'GluGlutoContintoWWtoTauNuTauNu')

samples['ggWW'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 15,
}

# WZ
files = nanoGetSampleFiles(mcDirectory, 'WZTo3LNu')

samples['WZ'] = {
    'name': files,
    'weight': mcCommonWeight + ' * (Gen_ZGstar_mass >= 50)',
    'FilesPerJob': 5,
}

files = nanoGetSampleFiles(mcDirectory, 'ZZ')

samples['ZZ'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 5,
}

# Vg/Vgstar
        
files = nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_MLL-4to50_PTG-10to100') + \
        nanoGetSampleFiles(mcDirectory, 'WGtoLNuG-1J_PTG10to100') + \
        nanoGetSampleFiles(mcDirectory, 'WGtoLNuG-1J_PTG100to200') + \
        nanoGetSampleFiles(mcDirectory, 'WGtoLNuG-1J_PTG200to400') + \
        nanoGetSampleFiles(mcDirectory, 'WGtoLNuG-1J_PTG400to600') + \
        nanoGetSampleFiles(mcDirectory, 'WGtoLNuG-1J_PTG600') + \
        nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_MLL-4to50_PTG-100to200') + \
        nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_MLL-4to50_PTG-200') + \
        nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_MLL-50_PTG-10to100') + \
        nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_MLL-50_PTG-100to200') + \
        nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_MLL-50_PTG-200to400') + \
        nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_MLL-50_PTG-400to600') + \
        nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_MLL-50_PTG-600')

samples['Vg'] = {
    'name': files,
    'weight': mcCommonWeight + '*(Gen_ZGstar_mass <= 0)',
    'FilesPerJob': 50,
}

files += nanoGetSampleFiles(mcDirectory, "WZTo3LNu")

samples['VgS'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 50,
}

addSampleWeight(samples, 'VgS', "DYGto2LG-1Jets_MLL-4to50_PTG-10to100", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
addSampleWeight(samples, 'VgS', "DYGto2LG-1Jets_MLL-4to50_PTG-100to200", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
addSampleWeight(samples, 'VgS', "DYGto2LG-1Jets_MLL-4to50_PTG-200", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
addSampleWeight(samples, 'VgS', "DYGto2LG-1Jets_MLL-50_PTG-10to100", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
addSampleWeight(samples, 'VgS', "DYGto2LG-1Jets_MLL-50_PTG-100to200", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
addSampleWeight(samples, 'VgS', "DYGto2LG-1Jets_MLL-50_PTG-200to400", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
addSampleWeight(samples, 'VgS', "DYGto2LG-1Jets_MLL-50_PTG-400to600", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
addSampleWeight(samples, 'VgS', "DYGto2LG-1Jets_MLL-50_PTG-600", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
addSampleWeight(samples, 'VgS', "WGtoLNuG-1J_PTG10to100", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
addSampleWeight(samples, 'VgS', "WGtoLNuG-1J_PTG100to200", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
addSampleWeight(samples, 'VgS', "WGtoLNuG-1J_PTG200to400", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
addSampleWeight(samples, 'VgS', "WGtoLNuG-1J_PTG400to600", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
addSampleWeight(samples, 'VgS', "WGtoLNuG-1J_PTG600", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
addSampleWeight(samples, 'VgS', "WZTo3LNu", "(Gen_ZGstar_mass >= 4 && Gen_ZGstar_mass < 50)")

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

###########################################
################## FAKE ###################
###########################################

samples['Fake'] = {
    'name': [],
    'weight': 'METFilter_DATA*fakeW',
    'weights': [],
    'isData': ['all'],
    'FilesPerJob': 15
}


for _, sd in DataRun:
  for pd in DataSets:
    datatag = pd + '_' + sd

    files = nanoGetSampleFiles(fakeDirectory, datatag)
    samples['Fake']['name'].extend(files)
    addSampleWeight(samples, 'Fake', datatag, DataTrig[pd])

