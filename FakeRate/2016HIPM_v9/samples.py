import os,sys,glob

################################################
################# SKIMS ########################
################################################

# MC:   /eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer20UL16_106x_nAODv9_HIPM_Full2016v9/MCl1loose2016v9__MCCorr2016v9NoJERInHorn/
# DATA: /eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Run2016_UL2016_nAODv9_HIPM_Full2016v9/DATAl1loose2016v9/

mcProduction = 'Summer20UL16_106x_nAODv9_HIPM_Full2016v9'
dataReco     = 'Run2016_UL2016_nAODv9_HIPM_Full2016v9'

mcSteps      = 'MCl1loose2016v9__MCCorr2016v9NoJERInHorn'
dataSteps    = 'DATAl1loose2016v9'

##############################################
###### Tree base directory for the site ######
##############################################

treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'
if 'portal' in os.uname()[1]:
    treeBaseDir = '/ceph/ntrevisa/HWWNano'

limitFiles  = -1

def makeMCDirectory(var=''):
    return os.path.join(treeBaseDir, mcProduction, mcSteps.format(var=''))

mcDirectory   = makeMCDirectory()
dataDirectory = os.path.join(treeBaseDir, dataReco, dataSteps)

samples = {}

from mkShapesRDF.lib.search_files import SearchFiles
s = SearchFiles()

useXROOTD = True
redirector = 'root://eoscms.cern.ch/'
if 'portal' in os.uname()[1]:
    redirector = ''

def nanoGetSampleFiles(path, name):
    _files = s.searchFiles(path, name, redirector=redirector)
    if limitFiles != -1 and len(_files) > limitFiles:
        return [(name, _files[:limitFiles])]
    else:
        return [(name, _files)]

def CombineBaseW(samples, proc, samplelist):
    _filtFiles = list(filter(lambda k: k[0] in samplelist, samples[proc]['name']))
    _files = list(map(lambda k: k[1], _filtFiles))
    _l = list(map(lambda k: len(k), _files))
    leastFiles = _files[_l.index(min(_l))]
    dfSmall = ROOT.RDataFrame('Runs', leastFiles)
    s = dfSmall.Sum('genEventSumw').GetValue()
    f = ROOT.TFile.Open(leastFiles[0])
    t = f.Get('Events')
    t.GetEntry(1)
    xs = t.baseW * s

    __files = []
    for f in _files:
        __files += f
    df = ROOT.RDataFrame('Runs', __files)
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


################################################
############ DATA DECLARATION ##################
################################################

DataRun = [
    ['B','Run2016B-ver1_HIPM_UL2016-v2'],
    ['B','Run2016B-ver2_HIPM_UL2016-v2'],
    ['C','Run2016C-HIPM_UL2016-v2'],
    ['D','Run2016D-HIPM_UL2016-v2'],
    ['E','Run2016E-HIPM_UL2016-v2'],
    ['F','Run2016F-HIPM_UL2016-v2'],
]

# Pre-scaled triggers for fake rate estimation
DataSets = ['DoubleMuon','DoubleEG']

DataTrig = {
     'DoubleMuon' : '(Lepton_pt[0] <= 20 && HLT_Mu8_TrkIsoVVL > 0.5) || (Lepton_pt[0] > 20 && HLT_Mu17_TrkIsoVVL > 0.5)',
     'DoubleEG'   : '(HLT_Mu8_TrkIsoVVL < 0.5) && (HLT_Mu17_TrkIsoVVL < 0.5) && ((Lepton_pt[0] <= 25 && HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5) || (Lepton_pt[0] > 25 && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5))',
}

# Unprescaled triggers for prompt rate estimation
DataRunUnprescaled = [
    ['B','Run2016B-ver1_HIPM_UL2016-v2'],
    ['B','Run2016B-ver2_HIPM_UL2016-v2'],
    ['C','Run2016C-HIPM_UL2016-v2'],
    ['D','Run2016D-HIPM_UL2016-v2'],
    ['E','Run2016E-HIPM_UL2016-v2'],
    ['F','Run2016F-HIPM_UL2016-v2'],
]

DataSetsUnprescaled = ['SingleMuon','SingleElectron']

DataTrigUnprescaled = {
    'SingleMuon'     : 'HLT_IsoMu24 > 0.5 || HLT_IsoTkMu24 > 0.5',
    'SingleElectron' : '(HLT_IsoMu24 < 0.5 && HLT_IsoTkMu24 < 0.5) && HLT_Ele27_WPTight_Gsf > 0.5',
}

#########################################
############ MC COMMON ##################
#########################################

# SFweight does not include btag weights
# mcCommonWeight = 'XSWeight/1000.'
# XSWeight = baseW * Generator_weight
mcCommonWeight = 'baseW*puWeight*Generator_weight/1000.'

###########################################
#############  BACKGROUNDS  ###############
###########################################

lumi_ele_low_pt   = '11.028*(HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5)*(Lepton_pt[0]<=25)';
lumi_ele_high_pt  = '52.768*(HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5)*(Lepton_pt[0]>25)';
lumi_muon_low_pt  =  '6.584*(HLT_Mu8_TrkIsoVVL > 0.5)*(Lepton_pt[0]<=20)';
lumi_muon_high_pt = '192.064*(HLT_Mu17_TrkIsoVVL > 0.5)*(Lepton_pt[0]>20)';
lumi_full_2018    = '19521'

# DY
files = nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-50')

samples['DY_ele_low_pt'] = {
    'name': files,
    'weight': mcCommonWeight + '*' + lumi_ele_low_pt,
    'FilesPerJob': 4,
}

samples['DY_ele_high_pt'] = {
    'name': files,
    'weight': mcCommonWeight + '*' + lumi_ele_high_pt,
    'FilesPerJob': 4,
}

samples['DY_muon_low_pt'] = {
    'name': files,
    'weight': mcCommonWeight + '*' + lumi_muon_low_pt,
    'FilesPerJob': 4,
}

samples['DY_muon_high_pt'] = {
    'name': files,
    'weight': mcCommonWeight + '*' + lumi_muon_high_pt,
    'FilesPerJob': 4,
}

samples['DY_unprescaled'] = {
    'name': files,
    'weight': mcCommonWeight + '*' + lumi_full_2018,
    'FilesPerJob': 4,
}

##### WJets #######
files = nanoGetSampleFiles(mcDirectory, 'WJetsToLNu-LO')

samples['WJets_ele_low_pt'] = {
    'name': files,
    'weight': mcCommonWeight + '*' + lumi_ele_low_pt + '*(XSWeight < 1)',
    'FilesPerJob': 4,
}

samples['WJets_ele_high_pt'] = {
    'name': files,
    'weight': mcCommonWeight + '*' + lumi_ele_high_pt + '*(XSWeight < 1)',
    'FilesPerJob': 4,
}

samples['WJets_muon_low_pt'] = {
    'name': files,
    'weight': mcCommonWeight + '*' + lumi_muon_low_pt + '*(XSWeight < 1)',
    'FilesPerJob': 4,
}

samples['WJets_muon_high_pt'] = {
    'name': files,
    'weight': mcCommonWeight + '*' + lumi_muon_high_pt + '*(XSWeight < 1)',
    'FilesPerJob': 4,
}

###########################################
################## DATA ###################
###########################################

# Prescaled
samples['DATA'] = {
  'name': [],
  'weight': 'METFilter_DATA',
  'weights': [],
  'isData': ['all'],
  'FilesPerJob': 10
}

for _, sd in DataRun:
  for pd in DataSets:
    tag_data = pd + '_' + sd

    if 'DoubleEG' in pd and 'Run2016B-ver2' in sd:
        print("sd      = {}".format(sd))
        print("pd      = {}".format(pd))
        print("Old tag = {}".format(tag_data))
        tag_data = tag_data.replace('v2','v3')
        print("New tag = {}".format(tag_data))

    files = nanoGetSampleFiles(dataDirectory, tag_data)

    samples['DATA']['name'].extend(files)
    addSampleWeight(samples, 'DATA', tag_data, DataTrig[pd])


# Unprescaled
samples['DATA_unprescaled'] = {
  'name': [],
  'weight': 'METFilter_DATA',
  'weights': [],
  'isData': ['all'],
  'FilesPerJob': 10
}

for _, sd in DataRunUnprescaled:
  for pd in DataSetsUnprescaled:
    tag_data = pd + '_' + sd

    if 'DoubleEG' in pd and 'Run2016B-ver2' in sd:
        print("sd      = {}".format(sd))
        print("pd      = {}".format(pd))
        print("Old tag = {}".format(tag_data))
        tag_data = tag_data.replace('v2','v3')
        print("New tag = {}".format(tag_data))

    files = nanoGetSampleFiles(dataDirectory, tag_data)

    samples['DATA_unprescaled']['name'].extend(files)
    addSampleWeight(samples, 'DATA_unprescaled', tag_data, DataTrigUnprescaled[pd])    
