from mkShapesRDF.lib.search_files import SearchFiles

searchFiles = SearchFiles()

redirector = ""
useXROOTD = False

mcProduction = 'Summer22_130x_nAODv12_Full2022v12'
dataReco = 'Run2022_ReReco_nAODv12_Full2022v12'
mcSteps = 'MCl1loose2022v12__MCCorr2022v12_NoJER'
fakeSteps = 'DATAl1loose2022v12__fakeW'
dataSteps = 'DATAl1loose2022v12__fakeW'

##############################################
###### Tree base directory for the site ######
##############################################
treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/calderon/HWWNano'
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

#signals = ['GluGluHToWWTo2L2Nu_M125', 'VBFHToWWTo2L2Nu_M125']
#backgrounds = ['WToLNu-2Jets', 'TTToSemiLeptonic']
'''
for proc in signals + backgrounds:
    samplelist = [name for name, files in samples[proc]['name']]
    CombineBaseW(samples, proc, samplelist)
'''
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

mcCommonWeight = 'XSWeight*METFilter_Common*PromptGenLepMatch2l*SFweight'

###########################################
############# BACKGROUNDS ################
###########################################

###### WToLNu-2Jets #######

files = nanoGetSampleFiles(mcDirectory, 'WToLNu-2Jets')
samples['WJets'] = {
    'name': files,
    'weight': mcCommonWeight + '*8.174732641',
    'FilesPerJob': 2,
}

###### TTToSemiLeptonic #######

files = nanoGetSampleFiles(mcDirectory, 'TTToSemiLeptonic')
samples['TT_semilep'] = {
    'name': files,
    'weight': mcCommonWeight + '*8.174732641',
    'FilesPerJob': 2,
}

###########################################
################# SIGNALS #################
###########################################

###### GluGluHToWWTo2L2Nu_M125 #######
files = nanoGetSampleFiles(mcDirectory, 'GluGluHToWWTo2L2Nu_M125')
if files:
    samples['ggH_hww'] = {
        'name': files,
        'weight': mcCommonWeight + '*8.174732641',
        'FilesPerJob': 2,
    }
else:
    print("No files found for GluGluHToWWTo2L2Nu_M125")
'''
files = nanoGetSampleFiles(mcDirectory, 'GluGluHToWWTo2L2Nu_M125')
samples['ggH_hww'] = {
    'name': files,
    'weight': mcCommonWeight + '*8.174732641',
    'FilesPerJob': 2,
}
'''
###### VBFHToWWTo2L2Nu_M125 #######

files = nanoGetSampleFiles(mcDirectory, 'VBFHToWWTo2L2Nu_M125')
samples['qqH_hww'] = {
    'name': files,
    'weight': mcCommonWeight + '*8.174732641',
    'FilesPerJob': 2,
}
'''
for proc in signals + backgrounds:
    samplelist = [name for name, files in samples[proc]['name']]
    CombineBaseW(samples, proc, samplelist)
'''
###########################################
################## DATA ###################
###########################################
# Data section - modify as needed
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

    if (pd == "SingleMuon" and _ in ["D","E","F","G"]) or (pd == "Muon" and _ == "B"):
        continue
    
    print(datatag)

    files = nanoGetSampleFiles(dataDirectory, datatag)

    samples['DATA']['name'].extend(files)
    addSampleWeight(samples, 'DATA', datatag, DataTrig[pd])



###########################################  
################## FAKE ###################
###########################################
# Fake data section - modify as needed
samples['Fake'] = {
    'name': [],
    'weight': 'METFilter_DATA*fakeW',
    'weights': [],
    'isData': ['all'],
    'FilesPerJob': 15
}


for _, sd in DataRun:
  for pd in DataSets:
    tag = pd + '_' + sd

    if (pd == "SingleMuon" and _ in ["D","E","F","G"]) or (pd == "Muon" and _ == "B"):
        continue

    files = nanoGetSampleFiles(dataDirectory, tag)
        
    samples['Fake']['name'].extend(files)
    addSampleWeight(samples, 'Fake', tag, DataTrig[pd])

