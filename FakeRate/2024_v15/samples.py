import os,sys,glob

################################################
################# SKIMS ########################
################################################

mcProduction   = 'Summer24_150x_nAODv15_Full2024v15'
mcSteps        = 'MCl1loose2024v15__fakeSel'
dataRecoMuon   = 'Run2024_ReRecoCDE_PromptFGHI_nAODv15_Full2024v15_Muon'
dataRecoEGamma = 'Run2024_ReRecoCDE_PromptFGHI_nAODv15_Full2024v15_EGamma'
dataSteps      = 'DATAl1loose2024v15__fakeSel'

##############################################
###### Tree base directory for the site ######
##############################################

treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'

limitFiles  = -1

def makeMCDirectory(var=''):
    return os.path.join(treeBaseDir, mcProduction, mcSteps.format(var=''))

mcDirectory   = makeMCDirectory()
dataDirectoryMuon = os.path.join(treeBaseDir, dataRecoMuon, dataSteps)
dataDirectoryEGamma = os.path.join(treeBaseDir, dataRecoEGamma, dataSteps)
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
    ['C','Run2024C-ReReco-v1'],
    ['D','Run2024D-ReReco-v1'],
    ['E','Run2024E-ReReco-v1'],
    ['F','Run2024F-Prompt-v1'],
    ['G','Run2024G-Prompt-v1'],
    ['H','Run2024H-Prompt-v1'],
    ['I','Run2024I-Prompt-v1'],
]


DataSets = ['Muon0','Muon1','EGamma0','EGamma1']

DataTrig = {
    'Muon0'   : '((Lepton_pt[0] <= 20 && HLT_Mu8_TrkIsoVVL > 0.5) || (Lepton_pt[0] > 20 && HLT_Mu17_TrkIsoVVL > 0.5)) && (HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30 < 0.5) && (HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 < 0.5)',
    'Muon1'   : '((Lepton_pt[0] <= 20 && HLT_Mu8_TrkIsoVVL > 0.5) || (Lepton_pt[0] > 20 && HLT_Mu17_TrkIsoVVL > 0.5)) && (HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30 < 0.5) && (HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 < 0.5)',
    'EGamma0' : '((Lepton_pt[0] <= 25 && HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5) || (Lepton_pt[0] > 25 && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5)) && (HLT_Mu8_TrkIsoVVL < 0.5) && (HLT_Mu17_TrkIsoVVL < 0.5)',
    'EGamma1' : '((Lepton_pt[0] <= 25 && HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5) || (Lepton_pt[0] > 25 && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5)) && (HLT_Mu8_TrkIsoVVL < 0.5) && (HLT_Mu17_TrkIsoVVL < 0.5)',
}


# Unprescaled triggers for prompt rate estimation
DataRunUnprescaled = [
    ['C','Run2024C-ReReco-v1'],
    ['D','Run2024D-ReReco-v1'],
    ['E','Run2024E-ReReco-v1'],
    ['F','Run2024F-Prompt-v1'],
    ['G','Run2024G-Prompt-v1'],
    ['H','Run2024H-Prompt-v1'],
    ['I','Run2024I-Prompt-v1'],
]

DataSetsUnprescaled = ['Muon0','Muon1','EGamma0','EGamma1']

DataTrigUnprescaled = {
    'Muon0'  : 'HLT_IsoMu24 > 0.5',                                # && HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8 < 0.5',
    'Muon1'  : 'HLT_IsoMu24 > 0.5',                                # && HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8 < 0.5',
    'EGamma0': 'HLT_IsoMu24 < 0.5 && HLT_Ele30_WPTight_Gsf > 0.5', # && HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8 < 0.5 && HLT_Ele30_WPTight_Gsf > 0.5',
    'EGamma1': 'HLT_IsoMu24 < 0.5 && HLT_Ele30_WPTight_Gsf > 0.5', # && HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8 < 0.5 && HLT_Ele30_WPTight_Gsf > 0.5',
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

lumi_ele_low_pt   = '70.525805414  * (HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5)*(Lepton_pt[0] <= 25)'
lumi_ele_high_pt  = '70.525805414  * (HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30 > 0.5)*(Lepton_pt[0] >  25)'
lumi_muon_low_pt  = '12.423819821  * (HLT_Mu8_TrkIsoVVL  > 0.5)*(Lepton_pt[0] <= 20)'
lumi_muon_high_pt = '336.398813605 * (HLT_Mu17_TrkIsoVVL > 0.5)*(Lepton_pt[0] >  20)'
lumi_full_2024    = '109329'

# DY
files = nanoGetSampleFiles(mcDirectory, 'DYto2E-2Jets_MLL-50') + \
        nanoGetSampleFiles(mcDirectory, 'DYto2Mu-2Jets_MLL-50') + \
        nanoGetSampleFiles(mcDirectory, 'DYto2Tau-2Jets_MLL-50')

samples['DY_ele_low_pt'] = {
    'name': files,
    'weight': mcCommonWeight + '*' + lumi_ele_low_pt,
    'FilesPerJob': 200,
}

samples['DY_ele_high_pt'] = {
    'name': files,
    'weight': mcCommonWeight + '*' + lumi_ele_high_pt,
    'FilesPerJob': 200,
}

samples['DY_muon_low_pt'] = {
    'name': files,
    'weight': mcCommonWeight + '*' + lumi_muon_low_pt,
    'FilesPerJob': 200,
}

samples['DY_muon_high_pt'] = {
    'name': files,
    'weight': mcCommonWeight + '*' + lumi_muon_high_pt,
    'FilesPerJob': 200,
}

samples['DY_unprescaled'] = {
    'name': files,
    'weight': mcCommonWeight + '*' + lumi_full_2024,
    'FilesPerJob': 200,
}


##### WJets #######
files = nanoGetSampleFiles(mcDirectory, 'WToENu-2Jet') + \
        nanoGetSampleFiles(mcDirectory, 'WToMuNu-2Jet') + \
        nanoGetSampleFiles(mcDirectory, 'WToTauNu-2Jet')

samples['WJets_ele_low_pt'] = {
    'name': files,
    'weight': mcCommonWeight + '*' + lumi_ele_low_pt,
    'FilesPerJob': 200,
}

samples['WJets_ele_high_pt'] = {
    'name': files,
    'weight': mcCommonWeight + '*' + lumi_ele_high_pt,
    'FilesPerJob': 200,
}

samples['WJets_muon_low_pt'] = {
    'name': files,
    'weight': mcCommonWeight + '*' + lumi_muon_low_pt,
    'FilesPerJob': 200,
}

samples['WJets_muon_high_pt'] = {
    'name': files,
    'weight': mcCommonWeight + '*' + lumi_muon_high_pt,
    'FilesPerJob': 200,
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
    'FilesPerJob': 250 
} 

for _, sd in DataRun:
  for pd in DataSets:
    datatag = pd + '_' + sd

    if 'Muon' in datatag:
        files = nanoGetSampleFiles(dataDirectoryMuon, datatag)
    if 'EGamma' in datatag:
        files = nanoGetSampleFiles(dataDirectoryEGamma, datatag)
    
    print(datatag)

    samples['DATA']['name'].extend(files)
    addSampleWeight(samples, 'DATA', datatag, DataTrig[pd])


# Unprescaled
samples['DATA_unprescaled'] = {
  'name': [],
  'weight': 'METFilter_DATA',
  'weights': [],
  'isData': ['all'],
  'FilesPerJob': 200
}

for _, sd in DataRunUnprescaled:
  for pd in DataSetsUnprescaled:
    datatag = pd + '_' + sd

    if 'Muon' in datatag:
        files = nanoGetSampleFiles(dataDirectoryMuon, datatag)
    if 'EGamma' in datatag:
        files = nanoGetSampleFiles(dataDirectoryEGamma, datatag)
    
    print(datatag)

    samples['DATA_unprescaled']['name'].extend(files)
    addSampleWeight(samples, 'DATA_unprescaled', datatag, DataTrigUnprescaled[pd])
