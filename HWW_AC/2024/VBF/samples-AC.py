from mkShapesRDF.lib.search_files import SearchFiles
import os

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

#########################################
############ MC COMMON ##################
#########################################

mcCommonWeightNoMatch  = 'XSWeight*METFilter_Common*PromptGenLepMatch1l*SFweight'
mcCommonWeight         = 'XSWeight*METFilter_Common*PromptGenLepMatch2l*SFweight'

### ggH ###

files = nanoGetSampleFiles(mcDirectory, 'GluGluHToWWTo2L2Nu_M125')

samples['ggH_hww'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 100,
}

### VBF ####

files = nanoGetSampleFiles(mcDirectory, 'VBFHToWWTo2L2Nu_M125')

samples['qqH_hww'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 15, 
}

#### VBF EFT coupling signal hypotheses ###

# Signals to be considered for nuisances (Avoid running for all reweighting)
eft_ewksys = ['VBF_H0PM']
eft_ggfsys = []
   
hyps_mc = ["H0PM", "H0PH", "H0M", "H0L1", "H0PHf05", "H0Mf05", "H0L1f05", "H0LZgf05", "H0PHZgf05", "H0MZgf05", "H0PHggf05", "H0Mggf05"]

cvtype_VBF = "AC"
hyps_reweight = ["H0PM", "H0PH", "H0M", "H0L1", "H0PHf05", "H0Mf05", "H0L1f05", "H0LZgf05", "H0PHZgf05", "H0MZgf05", "H0PHggf05", "H0Mggf05"]

print(" Number of hypotheses for "+cvtype_VBF+" :", len(hyps_reweight))
print(hyps_reweight)

reweight_VBF = []

for hmc in hyps_mc :
 nfiles = 400
 if "VBF_"+hmc+"" in eft_ewksys : nfiles = 25
 samples['VBF_'+hmc+''] = {
   'name':   nanoGetSampleFiles(mcDirectory, 'VBF_'+hmc+'_ToWWTo2L2Nu'),
   'weight': mcCommonWeight+ '*VBF_'+hmc+'_N',
   'FilesPerJob': nfiles,
 }
 for hrw in hyps_reweight :
  if hmc == hrw : continue
  samples['VBF_'+hmc+'to'+hrw+''] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'VBF_'+hmc+'_ToWWTo2L2Nu'),
    'weight': mcCommonWeight+ '*VBF_'+hmc+'_N*'+ hmc+'to'+hrw+'_W',
    'FilesPerJob': 400,
  }
  reweight_VBF.append('VBF_'+hmc+'to'+hrw+'')


