from mkShapesRDF.lib.search_files import SearchFiles

searchFiles = SearchFiles()

redirector = ""
useXROOTD = False

mcProduction = 'Summer23_130x_nAODv12_Full2023v12'
mcSteps      = 'MCl2loose2023v12__MCCorr2023v12JetScaling__l2tight'
dataReco     = 'Run2023_Prompt_nAODv12_Full2023v12'
dataSteps    = 'DATAl2loose2023v12__l2tight'
fakeSteps    = 'DATAl1loose2023v12'

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
    ['Cv1','Run2023C-Prompt-v1'],
    ['Cv2','Run2023C-Prompt-v2'],
    ['Cv3','Run2023C-Prompt-v3'],
    ['Cv4','Run2023C-Prompt-v4'],
]


DataSets = ['MuonEG','Muon0','Muon1','EGamma0','EGamma1']

DataTrig = {
    'MuonEG'          : 'Trigger_ElMu' ,
    #'SingleMuon'     : '!Trigger_ElMu && Trigger_sngMu' ,
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

    ##########
    ### DY ###
    ##########
    ##########
    ### DY ###
    ##########
files = nanoGetSampleFiles(mcDirectory, 'DYto2L-2Jets_MLL-50')
#files = nanoGetSampleFiles(mcDirectory, 'DYto2Tau-2Jets_MLL-50_0J') + \
#        nanoGetSampleFiles(mcDirectory, 'DYto2Tau-2Jets_MLL-50_1J') + \
#        nanoGetSampleFiles(mcDirectory, 'DYto2Tau-2Jets_MLL-50_2J')

samples['DY'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 10,
    }

    ####################
    ### ttbar and tW ###
    ####################

files = nanoGetSampleFiles(mcDirectory, 'TTTo2L2Nu') + \
        nanoGetSampleFiles(mcDirectory, 'TbarWplusto2L2Nu') + \
        nanoGetSampleFiles(mcDirectory, 'TWminusto2L2Nu')

samples['top'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 1,
}

addSampleWeight(samples,'top','TTTo2L2Nu','Top_pTrw')


    ##########
    ### WW ###
    ########## 

files = nanoGetSampleFiles(mcDirectory, 'WWTo2L2Nu')

samples['WW'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 2,
}

    ############
    ### ggWW ###
    ############

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
    'FilesPerJob': 8,
}

    ##########
    ### WZ ###
    ##########

files = nanoGetSampleFiles(mcDirectory, 'WZTo3LNu')

samples['WZ'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 2,
}

    ##########
    ### Vg ###
    ##########

files = nanoGetSampleFiles(mcDirectory, 'WGtoLNuG-1J_PTG10to100') + \
    nanoGetSampleFiles(mcDirectory, 'WGtoLNuG-1J_PTG100to200') + \
    nanoGetSampleFiles(mcDirectory, 'WGtoLNuG-1J_PTG200to400') +	\
    nanoGetSampleFiles(mcDirectory, 'WGtoLNuG-1J_PTG400to600') +	\
    nanoGetSampleFiles(mcDirectory, 'WGtoLNuG-1J_PTG600')

samples['Vg'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 5,
}

    ###########
    ### ggH ###
    ###########

files = nanoGetSampleFiles(mcDirectory, 'GluGluHToWWTo2L2Nu_M125')

samples['ggH_hww'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 2,
}

    ###########
    ### VBF ###
    ###########

files = nanoGetSampleFiles(mcDirectory, 'VBFHToWWTo2L2Nu_M125')

samples['qqH_hww'] = {
    'name': files,
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


    #############
    ### Fakes ###
    #############


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