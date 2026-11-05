import os,glob

#
# See as reference:
#     https://github.com/UniMiBAnalyses/PlotsConfigurations/blob/VBF_W/Configurations/VBF_W/2018/UL/samples.py
#     https://github.com/UniMiBAnalyses/PlotsConfigurations/blob/VBF_W/Configurations/VBF_W/2018/UL/aliases.py
#

################################################
################# SKIMS ########################
################################################

# MC:   /eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Summer20UL18_106x_nAODv9_Full2018v9/MCl1loose2018v9__MCCorr2018v9NoJERInHorn__l2tightOR2018v9/
# DATA: /eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Run2018_UL2018_nAODv9_Full2018v9/DATAl1loose2018v9__l2loose__l2tightOR2018v9/
# FAKE: /eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Run2018_UL2018_nAODv9_Full2018v9/DATAl1loose2018v9__l2loose__fakeW/


#
# 2l version
#
# mcProduction = 'Summer20UL18_106x_nAODv9_Full2018v9'
# dataReco     = 'Run2018_UL2018_nAODv9_Full2018v9'
# mcSteps      = 'MCl1loose2018v9__MCCorr2018v9NoJERInHorn__l2tightOR2018v9{var}'
# fakeSteps    = 'DATAl1loose2018v9__l2loose__fakeW'
# dataSteps    = 'DATAl1loose2018v9__l2loose__l2tightOR2018v9'
#
# ##############################################
# ###### Tree base directory for the site ######
# ##############################################
#
# treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'
#



mcProduction = 'Summer20UL18_106x_nAODv9_Full2018v9'
dataReco     = 'Run2018_UL2018_nAODv9_Full2018v9'
mcSteps      = 'MCl1loose2018v9__MCCorr2018v9NoJERInHorn{var}'
fakeSteps    = 'DATAl1loose2018v9'
dataSteps    = 'DATAl1loose2018v9'

##############################################
###### Tree base directory for the site ######
##############################################

treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'
limitFiles  = -1  # why on earth would you want to limit the number of files? Debug reason??


def makeMCDirectory(var=''):
    return os.path.join(treeBaseDir, mcProduction, mcSteps.format(var=''))

mcDirectory   = makeMCDirectory()
fakeDirectory = os.path.join(treeBaseDir, dataReco, fakeSteps)
dataDirectory = os.path.join(treeBaseDir, dataReco, dataSteps)

print (" mcDirectory = " , mcDirectory)


samples = {}

from mkShapesRDF.lib.search_files import SearchFiles
s = SearchFiles()

useXROOTD = True
redirector = 'root://eoscms.cern.ch/'

def nanoGetSampleFiles(path, name):
    _files = s.searchFiles(path, name, redirector=redirector)
    if limitFiles != -1 and len(_files) > limitFiles:
        return [(name, _files[:limitFiles])]
    else:
        return [(name, _files)]

def nanoGetLocalSampleFiles(path, name):
    print ("nanoGetLocalSampleFiles!")
    _files = s.searchFiles(path, name, redirector='')
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

DataSets = ['SingleMuon','EGamma']

DataTrig = {
    'SingleMuon'     : 'Trigger_sngMu' ,
    'EGamma'         : '!Trigger_sngMu && Trigger_sngEl' ,
}

#########################################
############ MC COMMON ##################
#########################################

XSWeight = 'baseW*genWeight'


trigg_MC = '( (abs(Lepton_pdgId[0])==13) * (HLT_IsoMu24 > 0.5) || (abs(Lepton_pdgId[0])==11) * (HLT_Ele32_WPTight_Gsf > 0.5) )'

#
# TriggerSFWeight_1l --> check the values but ok for now
# see https://github.com/latinos/mkShapesRDF/blob/master/mkShapesRDF/processor/data/TrigMaker_cfg.py
#
SFweight1l = ['puWeight', 'Lepton_RecoSF[0]', 'LepWPWeight_1l', 'LepWPCut_1l', 'btagSF', 'Jet_PUIDSF', 'TriggerSFWeight_1l', trigg_MC]

#
# Jet_PUIDSF defined in aliases.py
# btagSF     defined in aliases.py
#

SFweight = ' * '.join(SFweight1l)


#
# METFilter_MC not filled??
#

mcCommonWeightNoMatch = XSWeight+'*' + SFweight
mcCommonWeight        = XSWeight+'*' + SFweight + '*Lepton_genmatched[0]'
# mcCommonWeightNoMatch = 'XSWeight*SFweight*METFilter_MC'
# mcCommonWeight        = 'XSWeight*SFweight*METFilter_MC*Lepton_genmatched[0]'


###### H>gluglu #######

# the string "ZHgg" here is very important, since the root files that will be selected must have the format "nanoLatino_ZHgg__part*.root"
#files = nanoGetSampleFiles("/eos/user/a/amassiro/HIG/", "ZHgg")
# files = nanoGetLocalSampleFiles("/eos/user/a/amassiro/HIG/ZHggPostProc/Summer20UL18_106x_nAODv9_Full2018v9/MCFull2018v9/", "ZHgg")
# print (" list of files Hgg = ", files)
#
# samples["Hgluglu"] = {
#     "name": files,
#     #"weight": mcCommonWeight,  --> missing post processing
#     #"weight": 1,
#     "weight": "baseW*genWeight*0.8839*0.08187*0.033658*3",
#     "FilesPerJob": 1,
# }


#
# qqZH: 8.839E-01 pb - 1.227E-01 pb = 7.612E-01
#
# AM: should I subtract the two values from the excel file?
#

files = nanoGetLocalSampleFiles("/eos/user/a/amassiro/HIG/ZHggPostProc/Summer20UL18_106x_nAODv9_Full2018v9/MCFull2018v9/", "ZHllHgg")

samples["qqZHgluglu"] = {
    "name": files,
    #"weight": mcCommonWeight,  --> missing post processing
    #"weight": 1,
    "weight": "baseW*genWeight*0.7612*0.08187*0.033658*3",
    "FilesPerJob": 200,
}


#
# ggZH: 1.227E-01  pb
#

files = nanoGetLocalSampleFiles("/eos/user/a/amassiro/HIG/ZHggPostProc/Summer20UL18_106x_nAODv9_Full2018v9/MCFull2018v9/", "ggZHllHgg")

samples["ggZHgluglu"] = {
    "name": files,
    #"weight": mcCommonWeight,  --> missing post processing
    #"weight": 1,
    "weight": "baseW*genWeight*0.1227*0.08187*0.033658*3",
    "FilesPerJob": 200,
}


#
# W+ : 8.400E-01  pb
# W- : 5.328E-01  pb
#
files = nanoGetLocalSampleFiles("/eos/user/a/amassiro/HIG/ZHggPostProc/Summer20UL18_106x_nAODv9_Full2018v9/MCFull2018v9/", "WminuslvHgg") + \
        nanoGetLocalSampleFiles("/eos/user/a/amassiro/HIG/ZHggPostProc/Summer20UL18_106x_nAODv9_Full2018v9/MCFull2018v9/", "WpluslvHgg")

samples["WHgluglu"] = {
    "name": files,
    #"weight": mcCommonWeight,  --> missing post processing
    #"weight": 1,
    "weight": "baseW*genWeight*1.0*0.08187*0.1086*3",
    "FilesPerJob": 200,
}

addSampleWeight( samples, 'WHgluglu', 'WminuslvHgg',  '0.5328') # xsec pb (above I put 1.0)
addSampleWeight( samples, 'WHgluglu', 'WpluslvHgg',   '0.8400') # xsec pb (above I put 1.0)



#
# during post-processing, baseW, xsec = 1
#
# xs_db["ZHgg"] = ["xsec=1.000", "kfact=1.000", "ref=X"]
# Units in pb
# From https://twiki.cern.ch/twiki/pub/LHCPhysics/HiggsXSBR/Higgs_XSBR_YR4_update.xlsx
# 8.839E-01 pb
# and the branching ratio: 
# https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageBR
# 8.187E-02
# BR Z>ll:  3.3658% x 3
# From https://pdg.lbl.gov/2018/listings/rpp2018-list-z-boson.pdf
#
# BR W>lv: 10.86% x 3
# https://pdg.lbl.gov/2018/listings/rpp2018-list-w-boson.pdf
#
# ZH_HToGluGlu_ZToLL_13TeV_powheg_pythia8
#
# 59000×0.8839×0.08187×0.033658×3
#

###########################################
#############  BACKGROUNDS  ###############
###########################################


# # ####### Wjets #########

files = nanoGetSampleFiles(mcDirectory, 'WJetsToLNu-LO')            + \
        nanoGetSampleFiles(mcDirectory, 'WJetsToLNu_HT70To100')     + \
        nanoGetSampleFiles(mcDirectory, 'WJetsToLNu_HT100To200')    + \
        nanoGetSampleFiles(mcDirectory, 'WJetsToLNu_HT200To400')    + \
        nanoGetSampleFiles(mcDirectory, 'WJetsToLNu_HT400To600')    + \
        nanoGetSampleFiles(mcDirectory, 'WJetsToLNu_HT600To800')    + \
        nanoGetSampleFiles(mcDirectory, 'WJetsToLNu_HT800To1200')   + \
        nanoGetSampleFiles(mcDirectory, 'WJetsToLNu_HT1200To2500')  + \
        nanoGetSampleFiles(mcDirectory, 'WJetsToLNu_HT2500ToInf')


samples['Wjets'] = {
    'name': files,
    'weight': mcCommonWeight + '*1',
    'FilesPerJob' : 4,
    }

# # Fix Wjets binned + LO
addSampleWeight(samples,'Wjets', 'WJetsToLNu-LO', '(LHE_HT < 70)')
# ############
# # HT stiching corrections 2018
addSampleWeight( samples, 'Wjets', 'WJetsToLNu_HT70To100',    '1.21 * 0.95148')  #adding also k-factor
addSampleWeight( samples, 'Wjets', 'WJetsToLNu_HT100To200',   '0.9471')
addSampleWeight( samples, 'Wjets', 'WJetsToLNu_HT200To400',   '0.9515')
addSampleWeight( samples, 'Wjets', 'WJetsToLNu_HT400To600',   '0.9581')
addSampleWeight( samples, 'Wjets', 'WJetsToLNu_HT600To800',   '1.0582')
addSampleWeight( samples, 'Wjets', 'WJetsToLNu_HT800To1200',  '1.1285')
addSampleWeight( samples, 'Wjets', 'WJetsToLNu_HT1200To2500', '1.3268')
addSampleWeight( samples, 'Wjets', 'WJetsToLNu_HT2500ToInf',  '2.7948')



############ DY ############

files = nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-10to50_NLO') + \
        nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-50')

#print (" list of files DY = ", files)

samples['DY'] = {
    'name': files,
    'weight': mcCommonWeight + '*1',
    'FilesPerJob': 4,
}


##### Top #######

files = nanoGetSampleFiles(mcDirectory, 'TTTo2L2Nu') + \
        nanoGetSampleFiles(mcDirectory, 'ST_s-channel') + \
        nanoGetSampleFiles(mcDirectory, 'ST_t-channel_top') + \
        nanoGetSampleFiles(mcDirectory, 'ST_t-channel_antitop') + \
        nanoGetSampleFiles(mcDirectory, 'ST_tW_antitop') + \
        nanoGetSampleFiles(mcDirectory, 'ST_tW_top')  + \
        nanoGetSampleFiles(mcDirectory, 'TTToSemiLeptonic')

samples['top'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 8,
}

addSampleWeight(samples,'top','TTTo2L2Nu','Top_pTrw')
addSampleWeight(samples,'top','TTToSemiLeptonic','Top_pTrw')

############# VV ##################

files =   nanoGetSampleFiles( mcDirectory, 'WmToLNu_WmTo2J_QCD')    + \
          nanoGetSampleFiles( mcDirectory, 'WmToLNu_ZTo2J_QCD')     + \
          nanoGetSampleFiles( mcDirectory, 'WmTo2J_ZTo2L_QCD')      + \
          nanoGetSampleFiles( mcDirectory, 'WpTo2J_WmToLNu_QCD')    + \
          nanoGetSampleFiles( mcDirectory, 'WpTo2J_ZTo2L_QCD')      + \
          nanoGetSampleFiles( mcDirectory, 'WpToLNu_WpTo2J_QCD')    + \
          nanoGetSampleFiles( mcDirectory, 'WpToLNu_WmTo2J_QCD')    + \
          nanoGetSampleFiles( mcDirectory, 'WpToLNu_ZTo2J_QCD')     + \
          nanoGetSampleFiles( mcDirectory, 'ZTo2L_ZTo2J_QCD')

samples['VV']  = {
    'name' :  files,
    'weight': mcCommonWeight + '*1',
    'FilesPerJob' : 4,
    }


######## Vg ########
files = nanoGetSampleFiles(mcDirectory, 'Wg_AMCNLOFXFX_01J') + \
        nanoGetSampleFiles(mcDirectory, 'ZGToLLG')

samples['Vg'] = {
    'name': files,
    'weight': mcCommonWeightNoMatch + '*(Gen_ZGstar_mass <= 0)*1',
    'FilesPerJob': 4,
}

######## VgS ######## 
files = nanoGetSampleFiles(mcDirectory, 'Wg_AMCNLOFXFX_01J') + \
        nanoGetSampleFiles(mcDirectory, 'WZTo3LNu_mllmin0p1') + \
        nanoGetSampleFiles(mcDirectory, 'ZGToLLG')

samples['VgS'] = {
    'name': files,
    'weight': mcCommonWeight + '*1',
    'FilesPerJob': 4,
}
addSampleWeight(samples, 'VgS', 'Wg_AMCNLOFXFX_01J',  '((Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 0.1))*(gstarLow*0.94)')
addSampleWeight(samples, 'VgS', 'WZTo3LNu_mllmin0p1', '((Gen_ZGstar_mass > 0.1)*(0.601644*58.59/4.666))*(gstarLow*0.94)')
addSampleWeight(samples, 'VgS', 'ZGToLLG',            '(Gen_ZGstar_mass > 0)')


############ WZ ############
# files = nanoGetSampleFiles(mcDirectory, 'WZTo3LNu_mllmin0p1') + \
#         nanoGetSampleFiles(mcDirectory, 'WZTo2Q2L_mllmin4p0')
#
# samples['WZ'] = {
#     'name': files,
#     'weight': mcCommonWeight + ' * (gstarHigh)*1',
#     'FilesPerJob': 4
# }
# addSampleWeight(samples, 'WZ', 'WZTo3LNu_mllmin0p1', '(0.601644*58.59/4.666)')


############ ZZ ############
# files = nanoGetSampleFiles(mcDirectory, 'ZZTo2L2Nu') + \
#         nanoGetSampleFiles(mcDirectory, 'ZZTo2Q2L_mllmin4p0') + \
#         nanoGetSampleFiles(mcDirectory, 'ZZTo4L')
#
# samples['ZZ'] = {
#     'name': files,
#     'weight': mcCommonWeight + '*1',
#     'FilesPerJob': 4
# }


########## VVV #########
files = nanoGetSampleFiles(mcDirectory, 'ZZZ') + \
        nanoGetSampleFiles(mcDirectory, 'WZZ') + \
        nanoGetSampleFiles(mcDirectory, 'WWZ') + \
        nanoGetSampleFiles(mcDirectory, 'WWW')

samples['VVV'] = {
    'name': files,
    'weight': mcCommonWeight + '*1',
    'FilesPerJob': 4
}

###########################################
#############   SIGNALS  ##################
###########################################

signals = []

############ ggH H->WW ############
samples['ggH_hww'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'GluGluHToWWTo2L2Nu_M125'),
    'weight': mcCommonWeight + '*1',
    'FilesPerJob': 2
}
signals.append('ggH_hww')

############ VBF H->WW ############
samples['qqH_hww'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'VBFHToWWTo2L2Nu_M125'),
    'weight': mcCommonWeight + '*1',
    'FilesPerJob': 4
}
signals.append('qqH_hww')

############ ZH H->WW ############
samples['ZH_hww'] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'HZJ_HToWW_M125'),
    'weight': mcCommonWeight + '*1',
    'FilesPerJob': 4
}
signals.append('ZH_hww')

samples['ggZH_hww'] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'GluGluZH_HToWWTo2L2Nu_M125'),
    'weight': mcCommonWeight + '*1',
    'FilesPerJob': 4
}
signals.append('ggZH_hww')

############ WH H->WW ############
samples['WH_hww_plus'] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'HWplusJ_HToWW_M125'),
    'weight': mcCommonWeight + '*1',
    'FilesPerJob': 4
}
signals.append('WH_hww_plus')

samples['WH_hww_minus'] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'HWminusJ_HToWW_M125'),
    'weight': mcCommonWeight + '*1',
    'FilesPerJob': 4
}

signals.append('WH_hww_minus')

############ ttH ############
samples['ttH_hww'] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'ttHToNonbb_M125'),
    'weight': mcCommonWeight + '*1',
    'FilesPerJob': 2
}
signals.append('ttH_hww')

############ H->TauTau ############
samples['ggH_htt'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'GluGluHToTauTau_M125_Powheg'),
    'weight': mcCommonWeight + '*1',
    'FilesPerJob': 20
}
signals.append('ggH_htt')

samples['qqH_htt'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'VBFHToTauTau_M125'),
    'weight': mcCommonWeight + '*1',
    'FilesPerJob': 10
}
signals.append('qqH_htt')

samples['ZH_htt'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'ZHToTauTau_M125'),
    'weight': mcCommonWeight + '*1',
    'FilesPerJob': 4
}
signals.append('ZH_htt')

############ WH H->TauTau ############
samples['WH_htt_plus'] = {
    'name':  nanoGetSampleFiles(mcDirectory, 'WplusHToTauTau_M125'),
    'weight': mcCommonWeight + '*1',
    'FilesPerJob': 4
}
signals.append('WH_htt_plus')

samples['WH_htt_minus'] = {
    'name':  nanoGetSampleFiles(mcDirectory, 'WminusHToTauTau_M125'),
    'weight': mcCommonWeight + '*1',
    'FilesPerJob': 4
}
signals.append('WH_htt_minus')


###########################################
################## FAKE ###################
###########################################

# # # ## Fakes
# samples['Fake'] = {
#   'name': [],
#   'weight': METFilter_DATA +'*'+ fakeW +'* fakes_correction',
#   'weights': [],
#   'isData': ['all'],
#   'FilesPerJob' : 30,
# }
#
# for Run in DataRun :
#   for DataSet in DataSets :
#     version = 'v1'
#     if "SingleMuon" in DataSet and any(k in Run[0] for k in ["A", "B", "C"]):
#       version = 'v2'
#     # # BE Careful --> we use directory_data because the Lepton tight cut was not applied in post-processing
#     files = nanoGetSampleFiles(dataDirectoryHWW, DataSet+'_'+Run[1]+'-'+version)
#     for iFile in files:
#       samples['Fake']['name'].append(iFile)
#       samples['Fake']['weights'].append(DataTrig[DataSet])



###########################################
################## DATA ###################
###########################################

samples['DATA'] = {
  'name': [],
  'weight': 'LepWPCut_1l*METFilter_DATA*1',
  'weights': [],
  'isData': ['all'],
  'FilesPerJob': 50
}

for _, sd in DataRun:
  for pd in DataSets:
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

    samples['DATA']['name'].extend(files)
    addSampleWeight(samples, 'DATA', tag_data, DataTrig[pd])
