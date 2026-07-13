from mkShapesRDF.lib.search_files import SearchFiles

searchFiles = SearchFiles()

redirector = ""
useXROOTD = False

mcProduction = 'Summer22_130x_nAODv12_Full2022v12'
mcSteps      = 'MCl2loose2022v12__MCCorr2022v12JetScaling__l2tight'
dataReco     = 'Run2022_ReReco_nAODv12_Full2022v12'
dataSteps    = 'DATAl2loose2022v12__l2loose'
fakeSteps    = 'DATAl2loose2022v12__l2loose'

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
    ['C','Run2022C-ReReco-v1'],
    ['D','Run2022D-ReReco-v1'],
]

DataSets = ['MuonEG','Muon','EGamma']

DataTrig = {
    'MuonEG'         : 'Trigger_ElMu' ,
    'Muon'           : '!Trigger_ElMu && (Trigger_sngMu || Trigger_dblMu)',
    'EGamma'         : '!Trigger_ElMu && !Trigger_sngMu && !Trigger_dblMu && (Trigger_sngEl || Trigger_dblEl)'
}

#########################################
############ MC COMMON ##################
#########################################

mcCommonWeightNoMatch  = 'XSWeight*METFilter_Common*PromptGenLepMatch1l*SFweight'
mcCommonWeight         = 'XSWeight*METFilter_Common*PromptGenLepMatch2l*SFweight'


###########################################
#############  BACKGROUNDS  ###############
###########################################

# DY
files = nanoGetSampleFiles(mcDirectory, 'DYto2Tau-2Jets_MLL-50_0J') + \
        nanoGetSampleFiles(mcDirectory, 'DYto2Tau-2Jets_MLL-50_1J') + \
        nanoGetSampleFiles(mcDirectory, 'DYto2Tau-2Jets_MLL-50_2J')

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
    'FilesPerJob': 3,
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

# VZ
files = nanoGetSampleFiles(mcDirectory, 'WZTo3LNu') + \
        nanoGetSampleFiles(mcDirectory, 'ZZ')

samples['VZ'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 30,
}

addSampleWeight(samples, 'VZ', "WZTo3LNu", "Gen_ZGstar_mass >= 50")

# Vg/Vgstar

# Vg
files = nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_MLL-4to50_PTG-10to100_ext1') + \
        nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_MLL-4to50_PTG-100to200') + \
        nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_MLL-4to50_PTG-200') + \
        nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_MLL-50_PTG-10to100') + \
        nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_MLL-50_PTG-100to200') + \
        nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_MLL-50_PTG-200to400') + \
        nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_MLL-50_PTG-400to600') + \
        nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_MLL-50_PTG-600') + \
        nanoGetSampleFiles(mcDirectory, 'WGtoLNuG-1J')


samples['Vg'] = {
    'name': files,
    'weight': mcCommonWeightNoMatch + '*(Gen_ZGstar_mass <= 0)',
    'FilesPerJob': 50,
}

# Vg*
files = nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_MLL-4to50_PTG-10to100_ext1') + \
        nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_MLL-4to50_PTG-100to200') + \
        nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_MLL-4to50_PTG-200') + \
        nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_MLL-50_PTG-10to100') + \
        nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_MLL-50_PTG-100to200') + \
        nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_MLL-50_PTG-200to400') + \
        nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_MLL-50_PTG-400to600') + \
        nanoGetSampleFiles(mcDirectory, 'DYGto2LG-1Jets_MLL-50_PTG-600') + \
        nanoGetSampleFiles(mcDirectory, 'WGtoLNuG-1J') + \
        nanoGetSampleFiles(mcDirectory, "WZTo3LNu") 
        
samples['VgS'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 50,
}

addSampleWeight(samples, 'VgS', "DYGto2LG-1Jets_MLL-4to50_PTG-10to100_ext1", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
addSampleWeight(samples, 'VgS', "DYGto2LG-1Jets_MLL-4to50_PTG-100to200", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
addSampleWeight(samples, 'VgS', "DYGto2LG-1Jets_MLL-4to50_PTG-200", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
addSampleWeight(samples, 'VgS', "DYGto2LG-1Jets_MLL-50_PTG-10to100", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
addSampleWeight(samples, 'VgS', "DYGto2LG-1Jets_MLL-50_PTG-100to200", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
addSampleWeight(samples, 'VgS', "DYGto2LG-1Jets_MLL-50_PTG-200to400", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
addSampleWeight(samples, 'VgS', "DYGto2LG-1Jets_MLL-50_PTG-400to600", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
addSampleWeight(samples, 'VgS', "DYGto2LG-1Jets_MLL-50_PTG-600", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
addSampleWeight(samples, 'VgS', "WGtoLNuG-1J", "(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4)")
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

samples['Fake']['subsamples'] = {
  'e': 'abs(Lepton_pdgId[1]) == 11',
  'm': 'abs(Lepton_pdgId[1]) == 13'
}
