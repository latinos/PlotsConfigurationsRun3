import os,glob

################################################
################# SKIMS ########################
################################################

# MC:   /eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer20UL16_106x_nAODv9_noHIPM_Full2016v9/MCl1loose2016v9__MCCorr2016v9NoJERInHorn__l2tightOR2016v9/
# DATA: /eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Run2016_UL2016_nAODv9_noHIPM_Full2016v9/DATAl1loose2016v9__l2loose__l2tightOR2016v9/
# FAKE: /eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Run2016_UL2016_nAODv9_noHIPM_Full2016v9/DATAl1loose2016v9__l2loose__fakeW/

mcProduction = 'Summer20UL16_106x_nAODv9_noHIPM_Full2016v9'
dataReco     = 'Run2016_UL2016_nAODv9_noHIPM_Full2016v9'
mcSteps      = 'MCl1loose2016v9__MCCorr2016v9NoJERInHorn__l2tightOR2016v9{var}'
fakeSteps    = 'DATAl1loose2016v9__l2loose__fakeW'
dataSteps    = 'DATAl1loose2016v9__l2loose__l2tightOR2016v9'

##############################################
###### Tree base directory for the site ######
##############################################

# Site definition
site = 'cern'
if any(machine in os.uname()[1] for machine in ['portal','bms']):
    site = 'kit'

treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'
if site == 'kit':
    treeBaseDir = '/ceph/ntrevisa/HWWNano'
limitFiles  = -1

def makeMCDirectory(var=''):
    return os.path.join(treeBaseDir, mcProduction, mcSteps.format(var=''))

mcDirectory   = makeMCDirectory()
fakeDirectory = os.path.join(treeBaseDir, dataReco, fakeSteps)
dataDirectory = os.path.join(treeBaseDir, dataReco, dataSteps)

samples = {}

from mkShapesRDF.lib.search_files import SearchFiles
s = SearchFiles()

useXROOTD = True
redirector = 'root://eoscms.cern.ch/'
if site == 'kit':
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
    ['F','Run2016F-UL2016-v1'],
    ['G','Run2016G_UL2016-v1'],
    ['H','Run2016H_UL2016-v1'],
]

DataSets = ['MuonEG','SingleMuon','SingleElectron','DoubleMuon', 'DoubleEG']

DataTrig = {
    'MuonEG'         : ' Trigger_ElMu' ,
    'SingleMuon'     : '!Trigger_ElMu && Trigger_sngMu' ,
    'SingleElectron' : '!Trigger_ElMu && !Trigger_sngMu && Trigger_sngEl',
    'DoubleMuon'     : '!Trigger_ElMu && !Trigger_sngMu && !Trigger_sngEl && Trigger_dblMu',
    'DoubleEG'       : '!Trigger_ElMu && !Trigger_sngMu && !Trigger_sngEl && !Trigger_dblMu && Trigger_dblEl'
}

#########################################
############ MC COMMON ##################
#########################################

# SFweight does not include btag weights
mcCommonWeightNoMatch = 'XSWeight*SFweight*METFilter_MC'
mcCommonWeight        = 'XSWeight*SFweight*METFilter_MC*PromptGenLepMatch2l'

###########################################
#############  BACKGROUNDS  ###############
###########################################

############ DY OS ############
# Select opposite-sign events 
# and reweight them according
# to the leptons charge-flip
# probabilities

files = nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-10to50_NLO') + \
        nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-50')

samples['DY'] = {
    'name': files,
    'weight': mcCommonWeight + '*(Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13)*( !(Sum(PhotonGen_isPrompt==1 && PhotonGen_pt>15 && abs(PhotonGen_eta)<2.6) > 0))',
    'FilesPerJob': 4,
}

############ Non-charge-flip backgrounds ############
# In case we want to estimate the charge-flip
# backgrounds in the signal region, we can use
# data. But we have to subtract all the processes
# not affected by charge-flip:
# all but DY, WW, and top

######## Vg ########
files = nanoGetSampleFiles(mcDirectory, 'Wg_AMCNLOFXFX_01J') + \
        nanoGetSampleFiles(mcDirectory, 'ZGToLLG')

samples['Vg'] = {
    'name': files,
    'weight': mcCommonWeightNoMatch + '*(Gen_ZGstar_mass <= 0)*ttHMVA_eff_flip_2l',
    'FilesPerJob': 4,
}

######## VgS ######## 
files = nanoGetSampleFiles(mcDirectory, 'Wg_AMCNLOFXFX_01J') + \
        nanoGetSampleFiles(mcDirectory, 'WZTo3LNu_mllmin0p1') + \
        nanoGetSampleFiles(mcDirectory, 'ZGToLLG')

samples['VgS'] = {
    'name': files,
    'weight': mcCommonWeight + '*ttHMVA_eff_flip_2l',
    'FilesPerJob': 4,
}
addSampleWeight(samples, 'VgS', 'Wg_AMCNLOFXFX_01J',  '((Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 0.1))*(gstarLow*0.94)')
addSampleWeight(samples, 'VgS', 'WZTo3LNu_mllmin0p1', '((Gen_ZGstar_mass > 0.1)*(0.601644*58.59/4.666))*(gstarLow*0.94)')
addSampleWeight(samples, 'VgS', 'ZGToLLG',            '(Gen_ZGstar_mass > 0)')

# ######## Wg ########
# files = nanoGetSampleFiles(mcDirectory, 'Wg_AMCNLOFXFX_01J')

# samples['Wg'] = {
#     'name': files,
#     'weight': mcCommonWeightNoMatch + '*(Gen_ZGstar_mass <= 0)*ttHMVA_eff_flip_2l',
#     'FilesPerJob': 2,
# }


# ######## Zg ########
# files = nanoGetSampleFiles(mcDirectory, 'ZGToLLG')

# samples['Zg'] = {
#     'name': files,
#     'weight': mcCommonWeightNoMatch + '*(Gen_ZGstar_mass <= 0)*ttHMVA_eff_flip_2l',
#     'FilesPerJob': 2
# }


# ######## WgS ######## 
# files = nanoGetSampleFiles(mcDirectory, 'Wg_AMCNLOFXFX_01J') + \
#         nanoGetSampleFiles(mcDirectory, 'WZTo3LNu_mllmin0p1')

# samples['WgS'] = {
#     'name': files,
#     'weight': mcCommonWeight + ' * (gstarLow * 0.94)*ttHMVA_eff_flip_2l',
#     'FilesPerJob': 2,
# }
# addSampleWeight(samples, 'WgS', 'Wg_AMCNLOFXFX_01J',  '(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 0.1)')
# addSampleWeight(samples, 'WgS', 'WZTo3LNu_mllmin0p1', '(Gen_ZGstar_mass > 0.1)*(0.601644*58.59/4.666)')


# ######## ZgS ########
# files = nanoGetSampleFiles(mcDirectory, 'ZGToLLG')

# samples['ZgS'] = {
#     'name': files,
#     'weight': mcCommonWeight + '*(Gen_ZGstar_mass > 0)*ttHMVA_eff_flip_2l',
#     'FilesPerJob': 2,
# }


############ WZ ############
files = nanoGetSampleFiles(mcDirectory, 'WZTo3LNu_mllmin0p1') + \
        nanoGetSampleFiles(mcDirectory, 'WZTo2Q2L_mllmin4p0')

samples['WZ'] = {
    'name': files,
    'weight': mcCommonWeight + ' * (gstarHigh)*ttHMVA_eff_flip_2l',
    'FilesPerJob': 4
}
addSampleWeight(samples, 'WZ', 'WZTo3LNu_mllmin0p1', '(0.601644*58.59/4.666)')


############ ZZ ############
files = nanoGetSampleFiles(mcDirectory, 'ZZTo2L2Nu') + \
        nanoGetSampleFiles(mcDirectory, 'ZZTo2Q2L_mllmin4p0') + \
        nanoGetSampleFiles(mcDirectory, 'ZZTo4L')

samples['ZZ'] = {
    'name': files,
    'weight': mcCommonWeight + '*ttHMVA_eff_flip_2l',
    'FilesPerJob': 4
}


########## VVV #########
files = nanoGetSampleFiles(mcDirectory, 'ZZZ') + \
        nanoGetSampleFiles(mcDirectory, 'WZZ') + \
        nanoGetSampleFiles(mcDirectory, 'WWZ') + \
        nanoGetSampleFiles(mcDirectory, 'WWW')

samples['VVV'] = {
    'name': files,
    'weight': mcCommonWeight + '*ttHMVA_eff_flip_2l',
    'FilesPerJob': 4
}

###########################################
#############   SIGNALS  ##################
###########################################

signals = []

############ ggH H->WW ############
samples['ggH_hww'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'GluGluHToWWTo2L2Nu_M125'),
    'weight': mcCommonWeight + '*ttHMVA_eff_flip_2l',
    'FilesPerJob': 2
}
signals.append('ggH_hww')

############ VBF H->WW ############
samples['qqH_hww'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'VBFHToWWTo2L2Nu_M125'),
    'weight': mcCommonWeight + '*ttHMVA_eff_flip_2l',
    'FilesPerJob': 4
}
signals.append('qqH_hww')

############ ZH H->WW ############
samples['ZH_hww'] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'HZJ_HToWW_M125'),
    'weight': mcCommonWeight + '*ttHMVA_eff_flip_2l',
    'FilesPerJob': 4
}
signals.append('ZH_hww')

samples['ggZH_hww'] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'ggZH_HToWW_M125'),
    'weight': mcCommonWeight + '*ttHMVA_eff_flip_2l',
    'FilesPerJob': 4
}
signals.append('ggZH_hww')

############ WH H->WW ############
samples['WH_hww_plus'] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'HWplusJ_HToWW_M125'),
    'weight': mcCommonWeight + '*ttHMVA_eff_flip_2l',
    'FilesPerJob': 4
}
signals.append('WH_hww_plus')

samples['WH_hww_minus'] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'HWminusJ_HToWW_M125'),
    'weight': mcCommonWeight + '*ttHMVA_eff_flip_2l',
    'FilesPerJob': 4
}

signals.append('WH_hww_minus')

############ ttH ############
samples['ttH_hww'] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'ttHToNonbb_M125'),
    'weight': mcCommonWeight + '*ttHMVA_eff_flip_2l',
    'FilesPerJob': 2
}
signals.append('ttH_hww')

############ H->TauTau ############
samples['ggH_htt'] = {
    # 'name': nanoGetSampleFiles(mcDirectory, 'GluGluHToTauTau_M125_Powheg'),
    'name': nanoGetSampleFiles(mcDirectory, 'GluGluHToTauTau_M125'),
    'weight': mcCommonWeight + '*ttHMVA_eff_flip_2l',
    'FilesPerJob': 20
}
signals.append('ggH_htt')

samples['qqH_htt'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'VBFHToTauTau_M125'),
    'weight': mcCommonWeight + '*ttHMVA_eff_flip_2l',
    'FilesPerJob': 10
}
signals.append('qqH_htt')

samples['ZH_htt'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'ZHToTauTau_M125'),
    'weight': mcCommonWeight + '*ttHMVA_eff_flip_2l',
    'FilesPerJob': 4
}
signals.append('ZH_htt')

############ WH H->TauTau ############
samples['WH_htt_plus'] = {
    'name':  nanoGetSampleFiles(mcDirectory, 'WplusHToTauTau_M125'),
    'weight': mcCommonWeight + '*ttHMVA_eff_flip_2l',
    'FilesPerJob': 4
}
signals.append('WH_htt_plus')

samples['WH_htt_minus'] = {
    'name':  nanoGetSampleFiles(mcDirectory, 'WminusHToTauTau_M125'),
    'weight': mcCommonWeight + '*ttHMVA_eff_flip_2l',
    'FilesPerJob': 4
}
signals.append('WH_htt_minus')


###########################################
################## FAKE ###################
###########################################

samples['Fake'] = {
    'name': [],
    'weight': 'METFilter_DATA*fakeW*ttHMVA_eff_flip_2l',
    'weights': [],
    'isData': ['all'],
    'FilesPerJob': 50
}

for _, sd in DataRun:
  for pd in DataSets:
    tag_data = pd + '_' + sd

    if 'DoubleMuon' in pd and 'Run2016G' in sd: 
        print("sd      = {}".format(sd))
        print("pd      = {}".format(pd))
        print("Old tag = {}".format(tag_data))
        tag_data = tag_data.replace('v1','v2')
        print("New tag = {}".format(tag_data))

    files = nanoGetSampleFiles(fakeDirectory, tag_data)

    samples['Fake']['name'].extend(files)
    addSampleWeight(samples, 'Fake', tag_data, DataTrig[pd])

samples['Fake']['subsamples'] = {
    'em': 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*13',
    'mm': 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 13*13',
    'ee': 'abs(Lepton_pdgId[0]*Lepton_pdgId[1]) == 11*11'
}


###########################################
################## DATA ###################
###########################################

samples['DATA'] = {
  'name': [],
  'weight': 'LepWPCut*METFilter_DATA*ttHMVA_eff_flip_2l',
  'weights': [],
  'isData': ['all'],
  'FilesPerJob': 50
}

for _, sd in DataRun:
  for pd in DataSets:
    tag_data = pd + '_' + sd

    if 'DoubleMuon' in pd and 'Run2016G' in sd: 
        print("sd      = {}".format(sd))
        print("pd      = {}".format(pd))
        print("Old tag = {}".format(tag_data))
        tag_data = tag_data.replace('v1','v2')
        print("New tag = {}".format(tag_data))

    files = nanoGetSampleFiles(dataDirectory, tag_data)

    samples['DATA']['name'].extend(files)
    addSampleWeight(samples, 'DATA', tag_data, DataTrig[pd])
