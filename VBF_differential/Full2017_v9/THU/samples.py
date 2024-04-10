import os, glob
mcProduction = 'Summer20UL17_106x_nAODv9_Full2017v9'
mcSteps = 'MCl1loose2017v9__MCCorr2017v9NoJERInHorn'

##############################################
###### Tree base directory for the site ######
##############################################
treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'
limitFiles = -1

def makeMCDirectory(var=''):
        return os.path.join(treeBaseDir, mcProduction, mcSteps.format(var=''))

mcDirectory = makeMCDirectory()

samples = {}

from mkShapesRDF.lib.search_files import SearchFiles
s = SearchFiles()

useXROOTD = True
redirector = 'root://eoscms.cern.ch/'


def nanoGetSampleFiles(path, name):
    _files = s.searchFiles(path,  name, redirector=redirector)
    #_files = glob.glob(path + f"/nanoLatino_{name}__part*.root")
    if limitFiles != -1 and len(_files) > limitFiles:
        return [(name, _files[:limitFiles])]
    else:
        return  [(name, _files)]

def CombineBaseW(samples, proc, samplelist):
    _filtFiles = list(filter(lambda k: k[0] in samplelist, samples[proc]['name']))
    _files = list(map(lambda k: k[1], _filtFiles))
    _l = list(map(lambda k: len(k), _files))
    leastFiles = _files[_l.index(min(_l))]
    dfSmall = ROOT.RDataFrame("Runs", leastFiles)
    s = dfSmall.Sum('genEventSumw').GetValue()
    f = ROOT.TFile(leastFiles[0])
    t = f.Get("Events")
    t.GetEntry(1)
    xs = t.baseW * s

    __files = []
    for f in _files:
        __files += f
    df = ROOT.RDataFrame("Runs", __files)
    s = df.Sum('genEventSumw').GetValue()
    newbaseW = str(xs / s)
    weight = newbaseW + '/baseW'

    for iSample in samplelist:
        addSampleWeight(samples, proc, iSample, weight) 

def addSampleWeight(samples, sampleName, sampleNameType, weight):
    obj = list(filter(lambda k: k[0] == sampleNameType, samples[sampleName]['name']))[0]
    samples[sampleName]['name'] = list(filter(lambda k: k[0] != sampleNameType, samples[sampleName]['name']))
    if len(obj) > 2:
        samples[sampleName]['name'].append((obj[0], obj[1], obj[2] + '*(' + weight + ')'))
    else:
        samples[sampleName]['name'].append((obj[0], obj[1], '(' + weight + ')' ))


#########################################
############ MC COMMON ##################
#########################################

# SFweight does not include btag weights
mcCommonWeight = 'XSWeight'

############## ggH -> WW ############
samples['ggH_hww'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'GGHjjToWWTo2L2Nu_minloHJJ_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 2,
    'subsamples' : {
          'GenDeltaPhijj_0fid' : '(isFID == 1 && GenDeltaPhijj > -(TMath::Pi()) && GenDeltaPhijj <= -(TMath::Pi())/2)',
          'GenDeltaPhijj_1fid' : '(isFID == 1 && GenDeltaPhijj > -(TMath::Pi())/2 && GenDeltaPhijj <= 0)',
          'GenDeltaPhijj_2fid' : '(isFID == 1 && GenDeltaPhijj > 0 && GenDeltaPhijj <= (TMath::Pi())/2)',
          'GenDeltaPhijj_3fid' : '(isFID == 1 && GenDeltaPhijj > (TMath::Pi())/2 && GenDeltaPhijj <= (TMath::Pi()))',
          'GenDeltaPhijj_0nonfid' : '(isFID == 0 && GenDeltaPhijj > -(TMath::Pi()) && GenDeltaPhijj <= -(TMath::Pi())/2)',
          'GenDeltaPhijj_1nonfid' : '(isFID == 0 && GenDeltaPhijj > -(TMath::Pi())/2 && GenDeltaPhijj <= 0)',
          'GenDeltaPhijj_2nonfid' : '(isFID == 0 && GenDeltaPhijj > 0 && GenDeltaPhijj <= (TMath::Pi())/2)',
          'GenDeltaPhijj_3nonfid' : '(isFID == 0 && GenDeltaPhijj > (TMath::Pi())/2 && GenDeltaPhijj <= (TMath::Pi()))'
     }
}

############ VBF H->WW ############

samples['qqH_hww'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'VBFHToWWTo2L2Nu_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 2,
    'subsamples' : {
         'GenDeltaPhijj_0fid' : '(isFID == 1 && GenDeltaPhijj > -(TMath::Pi()) && GenDeltaPhijj <= -(TMath::Pi())/2)',
         'GenDeltaPhijj_1fid' : '(isFID == 1 && GenDeltaPhijj > -(TMath::Pi())/2 && GenDeltaPhijj <= 0)',
         'GenDeltaPhijj_2fid' : '(isFID == 1 && GenDeltaPhijj > 0 && GenDeltaPhijj <= (TMath::Pi())/2)',
         'GenDeltaPhijj_3fid' : '(isFID == 1 && GenDeltaPhijj > (TMath::Pi())/2 && GenDeltaPhijj <= (TMath::Pi()))',
         'GenDeltaPhijj_0nonfid' : '(isFID == 0 && GenDeltaPhijj > -(TMath::Pi()) && GenDeltaPhijj <= -(TMath::Pi())/2)',
         'GenDeltaPhijj_1nonfid' : '(isFID == 0 && GenDeltaPhijj > -(TMath::Pi())/2 && GenDeltaPhijj <= 0)',
         'GenDeltaPhijj_2nonfid' : '(isFID == 0 && GenDeltaPhijj > 0 && GenDeltaPhijj <= (TMath::Pi())/2)',
         'GenDeltaPhijj_3nonfid' : '(isFID == 0 && GenDeltaPhijj > (TMath::Pi())/2 && GenDeltaPhijj <= (TMath::Pi()))'
     }
}

