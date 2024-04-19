from mkShapesRDF.lib.search_files import SearchFiles

searchFiles = SearchFiles()

redirector = ""
useXROOTD = False

mcProduction = 'Summer22_130x_nAODv12_Full2022v12'
dataReco = 'Run2022_ReReco_nAODv12_Full2022v12'
mcSteps = 'MCl1loose2022v12__MCCorr2022v12_NoJER'
fakeSteps = 'DATAl1loose2022v12__fakeW'
dataSteps = 'DATAl1loose2022v12__fakeW'

mcProduction2 = 'Summer22EE_130x_nAODv12_Full2022v12'
dataReco2 = 'Run2022EE_Prompt_nAODv12_Full2022v12'
mcSteps2 = 'MCl1loose2022EEv12__MCCorr2022EEv12_ReRecoE_PromptFG'
fakeSteps2 = 'DATAl1loose2022EFGv12__fakeW'
dataSteps2 = 'DATAl1loose2022EFGv12__fakeW'

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

mcDirectory2 = "/".join([treeBaseDir, mcProduction2, mcSteps2])
fakeDirectory2 = os.path.join(treeBaseDir, dataReco2, fakeSteps2)
dataDirectory2 = os.path.join(treeBaseDir, dataReco2, dataSteps2)

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

# SFweight does not include btag weights
mcCommonWeightNoMatch = 'XSWeight*METFilter_Common*SFweight'
mcCommonWeight = 'XSWeight*METFilter_Common*PromptGenLepMatch2l*SFweight'

#mcCommonWeight = 'XSWeight*METFilter_Common*SFweight'

###########################################
#############  BACKGROUNDS  ###############
###########################################

#### Lumi scale
## 8.174732641
## 27.0

###### DY #######

files = nanoGetSampleFiles(mcDirectory, 'DYto2L-2Jets_MLL-50') + \
        nanoGetSampleFiles(mcDirectory, 'DYto2L-2Jets_MLL-10to50')


samples['DY'] = {
    'name': files,
    #'weight': mcCommonWeight + '*8.174732641*( !(Sum(PhotonGen_isPrompt==1 && PhotonGen_pt>15 && abs(PhotonGen_eta)<2.6) > 0))',
    'weight': mcCommonWeight + '*8.174732641',
    'FilesPerJob': 2,
}

files = nanoGetSampleFiles(mcDirectory2, 'DYto2L-2Jets_MLL-50') + \
        nanoGetSampleFiles(mcDirectory2, 'DYto2L-2Jets_MLL-10to50')


samples['DY_EE'] = {
    'name': files,
    #'weight': mcCommonWeight + '*27.0*( !(Sum(PhotonGen_isPrompt==1 && PhotonGen_pt>15 && abs(PhotonGen_eta)<2.6) > 0))',
    'weight': mcCommonWeight + '*27.0',
    'FilesPerJob': 2,
}

###### Top #######

files = nanoGetSampleFiles(mcDirectory, 'TTTo2L2Nu') + \
        nanoGetSampleFiles(mcDirectory, 'ST_t-channel_top') + \
        nanoGetSampleFiles(mcDirectory, 'ST_t-channel_antitop') + \
        nanoGetSampleFiles(mcDirectory, 'ST_tW_top') + \
        nanoGetSampleFiles(mcDirectory, 'ST_tW_antitop')

samples['top'] = {
    'name': files,
    'weight': mcCommonWeight + '*8.174732641',
    'FilesPerJob': 2,
}

addSampleWeight(samples,'top','ST_tW_top','0.108')
addSampleWeight(samples,'top','ST_tW_antitop','0.108')

addSampleWeight(samples,'top','TTTo2L2Nu','Top_pTrw')

files = nanoGetSampleFiles(mcDirectory2, 'TTTo2L2Nu') + \
        nanoGetSampleFiles(mcDirectory2, 'ST_t-channel_top') + \
        nanoGetSampleFiles(mcDirectory2, 'ST_t-channel_antitop') + \
        nanoGetSampleFiles(mcDirectory2, 'ST_tW_top') + \
        nanoGetSampleFiles(mcDirectory2, 'ST_tW_antitop')

samples['top_EE'] = {
    'name': files,
    'weight': mcCommonWeight + '*27.0',
    'FilesPerJob': 2,
}

addSampleWeight(samples,'top_EE','ST_tW_top','0.108')
addSampleWeight(samples,'top_EE','ST_tW_antitop','0.108')

addSampleWeight(samples,'top_EE','TTTo2L2Nu','Top_pTrw')

###### WW ####### 

files = nanoGetSampleFiles(mcDirectory, 'WWTo2L2Nu')

samples['WW'] = {
    'name': files,
    'weight': mcCommonWeight + '*8.174732641', #+ '*1.03', ## To take into account missing ggWW
    'FilesPerJob': 2,
}


files = nanoGetSampleFiles(mcDirectory2, 'WWTo2L2Nu')

samples['WW_EE'] = {
    'name': files,
    'weight': mcCommonWeight + '*27.0', #+ '*1.03', ## To take into account missing ggWW
    'FilesPerJob': 2,
}


######
###### POLARIZATION
######

files = nanoGetSampleFiles(mcDirectory, 'WWTo2L2Nu_LL')
samples['WW_LL'] = {
    'name': files,
    'weight': mcCommonWeight + '*8.174732641',
    'FilesPerJob': 2,
}
files = nanoGetSampleFiles(mcDirectory2, 'WWTo2L2Nu_LL')
samples['WW_LL_EE'] = {
    'name': files,
    'weight': mcCommonWeight + '*27.0',
    'FilesPerJob': 2,
}

files = nanoGetSampleFiles(mcDirectory, 'WWTo2L2Nu_TT')
samples['WW_TT'] = {
    'name': files,
    'weight': mcCommonWeight + '*8.174732641',
    'FilesPerJob': 2,
}
files = nanoGetSampleFiles(mcDirectory2, 'WWTo2L2Nu_TT')
samples['WW_TT_EE'] = {
    'name': files,
    'weight': mcCommonWeight + '*27.0',
    'FilesPerJob': 2,
}


files = nanoGetSampleFiles(mcDirectory, 'WWTo2L2Nu_TL')
samples['WW_TL'] = {
    'name': files,
    'weight': mcCommonWeight + '*8.174732641',
    'FilesPerJob': 2,
}
files = nanoGetSampleFiles(mcDirectory2, 'WWTo2L2Nu_TL')
samples['WW_TL_EE'] = {
    'name': files,
    'weight': mcCommonWeight + '*27.0',
    'FilesPerJob': 2,
}

files = nanoGetSampleFiles(mcDirectory, 'WWTo2L2Nu_LT')
samples['WW_LT'] = {
    'name': files,
    'weight': mcCommonWeight + '*8.174732641',
    'FilesPerJob': 2,
}
files = nanoGetSampleFiles(mcDirectory2, 'WWTo2L2Nu_LT')
samples['WW_LT_EE'] = {
    'name': files,
    'weight': mcCommonWeight + '*27.0',
    'FilesPerJob': 2,
}


### -----------------------------------------------------------------------------------------


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
    'weight': mcCommonWeight + '*8.174732641',
    'FilesPerJob': 2,
}

files = nanoGetSampleFiles(mcDirectory2, 'GluGlutoContintoWWtoENuENu') + \
    nanoGetSampleFiles(mcDirectory2, 'GluGlutoContintoWWtoENuMuNu') + \
    nanoGetSampleFiles(mcDirectory2, 'GluGlutoContintoWWtoENuTauNu') +   \
    nanoGetSampleFiles(mcDirectory2, 'GluGlutoContintoWWtoMuNuENu') +    \
    nanoGetSampleFiles(mcDirectory2, 'GluGlutoContintoWWtoMuNuMuNu') +   \
    nanoGetSampleFiles(mcDirectory2, 'GluGlutoContintoWWtoMuNuTauNu') +  \
    nanoGetSampleFiles(mcDirectory2, 'GluGlutoContintoWWtoTauNuENu') +   \
    nanoGetSampleFiles(mcDirectory2, 'GluGlutoContintoWWtoTauNuMuNu') +  \
    nanoGetSampleFiles(mcDirectory2, 'GluGlutoContintoWWtoTauNuTauNu')

samples['ggWW'] = {
    'name': files,
    'weight': mcCommonWeight + '*27.0',
    'FilesPerJob': 2,
}


###### WGamma #######

#files = nanoGetSampleFiles(mcDirectory, '')
#
#samples['Wg'] = {
#    'name': files,
#    'weight': mcCommonWeight
#    'FilesPerJob': 2,
#}

###### Zgamma #######

###### ZgS #######



###### ZZ #######

files = nanoGetSampleFiles(mcDirectory, 'ZZTo4L') + \
        nanoGetSampleFiles(mcDirectory, 'ZZTo2L2Nu') + \
        nanoGetSampleFiles(mcDirectory, 'ZZTo2L2Q') + \
        nanoGetSampleFiles(mcDirectory, 'ZZTo2Q2Nu')

samples['ZZ'] = {
    'name': files,
    'weight': mcCommonWeight + '*8.174732641',
    'FilesPerJob': 2,
}

files = nanoGetSampleFiles(mcDirectory2, 'ZZTo4L') + \
        nanoGetSampleFiles(mcDirectory2, 'ZZTo2L2Nu') + \
        nanoGetSampleFiles(mcDirectory2, 'ZZTo2L2Q') + \
        nanoGetSampleFiles(mcDirectory2, 'ZZTo2Q2Nu')

samples['ZZ_EE'] = {
    'name': files,
    'weight': mcCommonWeight + '*27.0',
    'FilesPerJob': 2,
}

###### WZ #######

files = nanoGetSampleFiles(mcDirectory, 'WZTo3LNu')

samples['WZ'] = {
    'name': files,
    'weight': mcCommonWeight + '*8.174732641',
    'FilesPerJob': 2,
}

files = nanoGetSampleFiles(mcDirectory2, 'WZTo3LNu')

samples['WZ_EE'] = {
    'name': files,
    'weight': mcCommonWeight + '*27.0',
    'FilesPerJob': 2,
}

#addSampleWeight(samples, 'WZ', 'WZTo3LNu', '(0.601644*58.59/4.666)')

###### VVV #######
files = nanoGetSampleFiles(mcDirectory, 'ZZZ') + \
        nanoGetSampleFiles(mcDirectory, 'WZZ') + \
        nanoGetSampleFiles(mcDirectory, 'WWZ') + \
        nanoGetSampleFiles(mcDirectory, 'WWW')

samples['VVV'] = {
    'name': files,
    'weight': mcCommonWeight + '*8.174732641',
    'FilesPerJob': 2,
}

files = nanoGetSampleFiles(mcDirectory2, 'ZZZ') + \
        nanoGetSampleFiles(mcDirectory2, 'WZZ') + \
        nanoGetSampleFiles(mcDirectory2, 'WWZ') + \
        nanoGetSampleFiles(mcDirectory2, 'WWW')

samples['VVV_EE'] = {
    'name': files,
    'weight': mcCommonWeight + '*27.0',
    'FilesPerJob': 2,
}


###### ggH Higgs #######
files = nanoGetSampleFiles(mcDirectory, 'GluGluHToWWTo2L2Nu_M125')

samples['ggH_hww'] = {
    'name': files,
    'weight': mcCommonWeight + '*8.174732641',
    'FilesPerJob': 2,
}

files = nanoGetSampleFiles(mcDirectory2, 'GluGluHToWWTo2L2Nu_M125')

samples['ggH_hww_EE'] = {
    'name': files,
    'weight': mcCommonWeight + '*27.0',
    'FilesPerJob': 2,
}

files = nanoGetSampleFiles(mcDirectory, 'VBFHToWWTo2L2Nu_M125')

samples['qqH_hww'] = {
    'name': files,
    'weight': mcCommonWeight + '*8.174732641',
    'FilesPerJob': 2,
}

files = nanoGetSampleFiles(mcDirectory2, 'VBFHToWWTo2L2Nu_M125')

samples['qqH_hww_EE'] = {
    'name': files,
    'weight': mcCommonWeight + '*27.0',
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

    if (pd == "SingleMuon" and _ in ["D","E","F","G"]) or (pd == "Muon" and _ == "B"):
        continue
    
    print(datatag)

    if (_ in ["E","F","G"]):
        files = nanoGetSampleFiles(dataDirectory2, datatag)
    else:
        files = nanoGetSampleFiles(dataDirectory, datatag)

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
    tag = pd + '_' + sd

    if (pd == "SingleMuon" and _ in ["D","E","F","G"]) or (pd == "Muon" and _ == "B"):
        continue

    if (_ in ["E","F","G"]):
        files = nanoGetSampleFiles(dataDirectory2, tag)
    else:
        files = nanoGetSampleFiles(dataDirectory, tag)
        
    samples['Fake']['name'].extend(files)
    addSampleWeight(samples, 'Fake', tag, DataTrig[pd])


    
