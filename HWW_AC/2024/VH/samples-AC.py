from mkShapesRDF.lib.search_files import SearchFiles
import os
import inspect
import sys

configurations = os.path.realpath(inspect.getfile(inspect.currentframe()))

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
limitFiles = 1

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


hxs_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(configurations)))) + '/utils/data/lhc-hxswg-YR5/'
sys.path.append(hxs_path)
cwd = os.getcwd()
os.chdir(hxs_path)
from HiggsXSection import HiggsXSection
HiggsXS = HiggsXSection()
os.chdir(cwd)

print("XS ",HiggsXS.GetHiggsProdXS('ggH','125.38'),HiggsXS.GetHiggsProdXS('vbfH','125.38'),HiggsXS.GetHiggsProdXS('WH','125.38'),HiggsXS.GetHiggsProdXS('HWplus','125.38'),HiggsXS.GetHiggsProdXS('HWminus','125.38'),HiggsXS.GetHiggsProdXS('ggZH','125.38'),HiggsXS.GetHiggsProdXS('qqZH','125.38'),HiggsXS.GetHiggsProdXS('ttH','125.38'))

#########################################
############ MC COMMON ##################
#########################################

mcCommonWeightNoMatch  = 'XSWeight*METFilter_Common*PromptGenLepMatch1l*SFweight'
mcCommonWeight         = 'XSWeight*METFilter_Common*PromptGenLepMatch2l*SFweight'

### ggH -> WW
files = nanoGetSampleFiles(mcDirectory, 'GluGluHToWWTo2L2Nu_M125')

samples['ggH_hww'] = {
    'name': files,
    'weight': f"{mcCommonWeight} * {HiggsXS.GetHiggsProdXS('ggH', '125.38')} / 51.960",
    'FilesPerJob': 400,
}

### VBF H->WW
files = nanoGetSampleFiles(mcDirectory, 'VBFHToWWTo2L2Nu_M125')

samples['qqH_hww'] = {
    'name': files,
    'weight': f"{mcCommonWeight} * {HiggsXS.GetHiggsProdXS('vbfH', '125.38')} / 4.067",
    'FilesPerJob': 20,
}

### ZH H->WW
files = nanoGetSampleFiles(mcDirectory, 'ZH_Zto2L_Hto2Wto2L2Nu_M125') + \
        nanoGetSampleFiles(mcDirectory, 'ZH_Zto2Q_Hto2Wto2L2Nu_M125') 

samples['ZH_hww'] = {
    'name':   files,
    'weight': f"{mcCommonWeight} * {HiggsXS.GetHiggsProdXS('qqZH', '125.38')} / 0.8014",
    'FilesPerJob': 20,
}

files = nanoGetSampleFiles(mcDirectory, 'GluGluZH_Zto2L_Hto2Wto2L2Nu_M125') + \
        nanoGetSampleFiles(mcDirectory, 'GluGluZH_Zto2Q_Hto2Wto2L2Nu_M125') 

samples['ggZH_hww'] = {
    'name':   files,
    'weight': f"{mcCommonWeight} * {HiggsXS.GetHiggsProdXS('ggZH', '125.38')} / 0.1347",
    'FilesPerJob': 20,
}

### WH H->WW
files = nanoGetSampleFiles(mcDirectory, 'HWplusJ_HToWWTo2L2Nu_WToLNu_M125') + \
        nanoGetSampleFiles(mcDirectory, 'HWplusJ_HToWWTo2L2Nu_WTo2Q_M125')  + \
        nanoGetSampleFiles(mcDirectory, 'HWminusJ_HToWWTo2L2Nu_WToLNu_M125') + \
        nanoGetSampleFiles(mcDirectory, 'HWminusJ_HToWWTo2L2Nu_WTo2Q_M125') 

samples['WH_hww'] = {
    'name':   files,
    'weight': mcCommonWeight,
    'FilesPerJob': 20,
}

addSampleWeight(samples, 'WH_hww', "HWplusJ_HToWWTo2L2Nu_WToLNu_M125", f"{HiggsXS.GetHiggsProdXS('HWplus', '125.38')} / 0.8801")
addSampleWeight(samples, 'WH_hww', "HWplusJ_HToWWTo2L2Nu_WTo2Q_M125", f"{HiggsXS.GetHiggsProdXS('HWplus', '125.38')} / 0.8801")
addSampleWeight(samples, 'WH_hww', "HWminusJ_HToWWTo2L2Nu_WToLNu_M125", f"{HiggsXS.GetHiggsProdXS('HWminus', '125.38')} / 0.5620")
addSampleWeight(samples, 'WH_hww', "HWminusJ_HToWWTo2L2Nu_WTo2Q_M125", f"{HiggsXS.GetHiggsProdXS('HWminus', '125.38')} / 0.5620")

###########################################
##      AC/EFT Analysis specific (VH)   ##
###########################################

# Signals to be considered for nuisances (Avoid running for all reweighting)
eft_ewksys  = ['ZH_H0PM','WH_H0PM']
eft_ggfsys = []

hyps_mc = ["H0PM", "H0PH", "H0M", "H0L1", "H0PHf05", "H0Mf05", "H0L1f05", "H0LZgf05", "H0PHZgf05", "H0MZgf05", "H0PHggf05", "H0Mggf05"]

cvtype_ZH = "AC"
hyps_reweight = ["H0PM", "H0PH", "H0M", "H0L1", "H0PHf05", "H0Mf05", "H0L1f05", "H0LZgf05", "H0PHZgf05", "H0MZgf05", "H0PHggf05", "H0Mggf05"]

print(" Number of ZH hypotheses for "+cvtype_ZH+" :", len(hyps_reweight))
print(hyps_reweight)

reweight_ZH = []

for hmc in hyps_mc :
 nfiles = 400
 #if "ZH_"+hmc+"" in eft_ewksys : nfiles = 100   
 samples['ZH_'+hmc+''] = {
   'name':   nanoGetSampleFiles(mcDirectory, 'ZH_'+hmc+'_ToWWTo2L2Nu'),
   'weight': mcCommonWeight+ '*ZH_'+hmc+'_N',
   'FilesPerJob': nfiles,
 }
 for hrw in hyps_reweight :
  if hmc == hrw : continue
  samples['ZH_'+hmc+'to'+hrw+''] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'ZH_'+hmc+'_ToWWTo2L2Nu'),
    'weight': mcCommonWeight+ '*ZH_'+hmc+'_N*ZH_'+hmc+'to'+hrw+'_W',
    'FilesPerJob': 400,
  }
  reweight_ZH.append('ZH_'+hmc+'to'+hrw+'')

#### WH EFT coupling signal hypotheses ###

hyps_mc = ["H0PM", "H0PH", "H0M", "H0L1", "H0PHf05", "H0Mf05", "H0L1f05"]

cvtype_WH = "AC"
hyps_reweight = ["H0PM", "H0PH", "H0M", "H0L1", "H0PHf05", "H0Mf05", "H0L1f05"]

print(" Number of WH hypotheses for "+cvtype_WH+" :", len(hyps_reweight))
print(hyps_reweight)

reweight_WH = []

for hmc in hyps_mc :
 nfiles = 400
 #if "WH_"+hmc+"" in eft_ewksys : nfiles = 100   
 samples['WH_'+hmc+''] = {
   'name':   nanoGetSampleFiles(mcDirectory, 'WH_'+hmc+'_ToWWTo2L2Nu'),
   'weight': mcCommonWeight+ '*WH_'+hmc+'_N',
   'FilesPerJob': nfiles,
 }
 for hrw in hyps_reweight :
  if hmc == hrw : continue
  samples['WH_'+hmc+'to'+hrw+''] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'WH_'+hmc+'_ToWWTo2L2Nu'),
    'weight': mcCommonWeight+ '*WH_'+hmc+'_N*WH_'+hmc+'to'+hrw+'_W',
    'FilesPerJob': 400,
  }
  reweight_WH.append('WH_'+hmc+'to'+hrw+'')

