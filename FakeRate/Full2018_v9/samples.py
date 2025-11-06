import os,sys,glob

################################################
################# SKIMS ########################
################################################

# MC:   /eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer20UL18_106x_nAODv9_Full2018v9/MCl1loose2018v9__MCCorr2018v9NoJERInHorn/
# DATA: /eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Run2018_UL2018_nAODv9_Full2018v9/DATAl1loose2018v9/
# FAKE: /eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Run2018_UL2018_nAODv9_Full2018v9/DATAl1loose2018v9/

mcProduction = 'Summer20UL18_106x_nAODv9_Full2018v9'
dataReco     = 'Run2018_UL2018_nAODv9_Full2018v9'

mcSteps      = 'MCl1loose2018v9__MCCorr2018v9NoJERInHorn'
dataSteps    = 'DATAl1loose2018v9'

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
# fakeDirectory = os.path.join(treeBaseDir, dataReco, fakeSteps)

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
    ['A','Run2018A-UL2018-v1'],
    ['B','Run2018B-UL2018-v1'],
    ['C','Run2018C-UL2018-v1'],
    ['D','Run2018D-UL2018-v1'],
]

# Pre-scaled triggers for fake rate estimation
DataSets = ['DoubleMuon','EGamma']

DataTrig = {
     'DoubleMuon' : '(Lepton_pt[0] <= 20 && HLT_Mu8_TrkIsoVVL > 0.5) || (Lepton_pt[0] > 20 && HLT_Mu17_TrkIsoVVL > 0.5)',
     'EGamma'     : '(HLT_Mu8_TrkIsoVVL < 0.5) && (HLT_Mu17_TrkIsoVVL < 0.5) && ((Lepton_pt[0] <= 25 && HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5) || (Lepton_pt[0] > 25 && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5))',
}

# Unprescaled triggers for prompt rate estimation
DataRunUnprescaled = [
    ['A','Run2018A-UL2018-v1'],
    ['B','Run2018B-UL2018-v1'],
    ['C','Run2018C-UL2018-v1'],
    ['D','Run2018D-UL2018-v1'],
]

DataSetsUnprescaled = ['SingleMuon','EGamma']

DataTrigUnprescaled = {
     'SingleMuon' : 'HLT_IsoMu24 > 0.5',
     'EGamma'     : 'HLT_IsoMu24 < 0.5 && HLT_Ele32_WPTight_Gsf > 0.5',
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

lumi_ele_low_pt   =  '6.412*(HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5)*(Lepton_pt[0]<=25)';
lumi_ele_high_pt  = '38.906*(HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5)*(Lepton_pt[0]>25)';
lumi_muon_low_pt  =  '8.561*(HLT_Mu8_TrkIsoVVL > 0.5)*(Lepton_pt[0]<=20)';
lumi_muon_high_pt = '45.781*(HLT_Mu17_TrkIsoVVL > 0.5)*(Lepton_pt[0]>20)';
lumi_full_2018    = '59832'

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

# # Top SemiLeptonic
# files = nanoGetSampleFiles(mcDirectory, 'TTToSemiLeptonic')

# samples['TTToSemiLeptonic_ele_low_pt'] = {
#     'name': files,
#     'weight': mcCommonWeight + '*' + lumi_ele_low_pt,
#     'FilesPerJob': 4,
# }

# samples['TTToSemiLeptonic_ele_high_pt'] = {
#     'name': files,
#     'weight': mcCommonWeight + '*' + lumi_ele_high_pt,
#     'FilesPerJob': 4,
# }

# samples['TTToSemiLeptonic_muon_low_pt'] = {
#     'name': files,
#     'weight': mcCommonWeight + '*' + lumi_muon_low_pt,
#     'FilesPerJob': 4,
# }

# samples['TTToSemiLeptonic_muon_high_pt'] = {
#     'name': files,
#     'weight': mcCommonWeight + '*' + lumi_muon_high_pt,
#     'FilesPerJob': 4,
# }


# # Top Fully Leptonic
# files = nanoGetSampleFiles(mcDirectory, 'TTTo2L2Nu')

# samples['TTTo2L2Nu_ele_low_pt'] = {
#     'name': files,
#     'weight': mcCommonWeight + '*' + lumi_ele_low_pt,
#     'FilesPerJob': 4,
# }

# samples['TTTo2L2Nu_ele_high_pt'] = {
#     'name': files,
#     'weight': mcCommonWeight + '*' + lumi_ele_high_pt,
#     'FilesPerJob': 4,
# }

# samples['TTTo2L2Nu_muon_low_pt'] = {
#     'name': files,
#     'weight': mcCommonWeight + '*' + lumi_muon_low_pt,
#     'FilesPerJob': 4,
# }

# samples['TTTo2L2Nu_muon_high_pt'] = {
#     'name': files,
#     'weight': mcCommonWeight + '*' + lumi_muon_high_pt,
#     'FilesPerJob': 4,
# }

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

    if (   ('DoubleMuon' in pd and 'Run2018B' in sd)
        or ('DoubleMuon' in pd and 'Run2018D' in sd)):
        print("sd      = {}".format(sd))
        print("pd      = {}".format(pd))
        print("Old tag = {}".format(tag_data))
        tag_data = tag_data.replace('v1','v2')
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

    if (   ('SingleMuon' in pd and 'Run2018A' in sd)
        or ('SingleMuon' in pd and 'Run2018B' in sd)
        or ('SingleMuon' in pd and 'Run2018C' in sd)):
        print("sd      = {}".format(sd))
        print("pd      = {}".format(pd))
        print("Old tag = {}".format(tag_data))
        tag_data = tag_data.replace('v1','v2')
        print("New tag = {}".format(tag_data))

    files = nanoGetSampleFiles(dataDirectory, tag_data)

    samples['DATA_unprescaled']['name'].extend(files)
    addSampleWeight(samples, 'DATA_unprescaled', tag_data, DataTrigUnprescaled[pd])    
