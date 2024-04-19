import os
import inspect
from mkShapesRDF.lib.search_files import SearchFiles

searchFiles = SearchFiles()
redirector = ""

################################################                                                                                                                                                           
################# SKIMS ########################                                                                                                                                                           
################################################                                                                                                                                                           

mcProduction = 'Summer20UL18_106x_nAODv9_Full2018v9'
dataReco     = 'Run2018_UL2018_nAODv9_Full2018v9'
mcSteps      = 'MCl1loose2018v9__MCCorr2018v9NoJERInHorn__l2tightOR2018v9{var}'
fakeSteps    = 'DATAl1loose2018v9__l2loose__fakeW'
dataSteps    = 'DATAl1loose2018v9__l2loose__l2tightOR2018v9'

samples = {}


##############################################
###### Tree base directory for the site ######
##############################################

treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'
limitFiles = -1

def makeMCDirectory(var=''):
    return os.path.join(treeBaseDir, mcProduction, mcSteps.format(var=''))


mcDirectory = makeMCDirectory()
fakeDirectory = os.path.join(treeBaseDir, dataReco, fakeSteps)
dataDirectory = os.path.join(treeBaseDir, dataReco, dataSteps)


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
    ['A','Run2018A-UL2018-v1'],
    ['B','Run2018B-UL2018-v1'],
    ['C','Run2018C-UL2018-v1'],
    ['D','Run2018D-UL2018-v1'],
]


DataSets = ['MuonEG','SingleMuon','EGamma','DoubleMuon']

DataTrig = {
    'MuonEG'         : 'Trigger_ElMu' ,
    'DoubleMuon'     : '!Trigger_ElMu && Trigger_dblMu' ,
    'SingleMuon'     : '!Trigger_ElMu && !Trigger_dblMu && Trigger_sngMu' ,
    'EGamma'         : '!Trigger_ElMu && !Trigger_dblMu && !Trigger_sngMu && (Trigger_sngEl || Trigger_dblEl)' ,
}



#########################################
############ MC COMMON ##################
#########################################

# SFweight does not include btag weights
mcCommonWeight = 'XSWeight*SFweight*METFilter_MC'
mcCommonWeightMatched = 'XSWeight*SFweight*PromptGenLepMatch2l*METFilter_MC'

###########################################
#############  BACKGROUNDS  ###############
###########################################


###### DY #######                                                                                                                                                                                          
useDYtt = True

files=[]
if useDYtt:
    files = nanoGetSampleFiles(mcDirectory, 'DYJetsToTT_MuEle_M-50') + \
            nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-10to50-LO')
else:
    files = nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-50_ext2') + \
            nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-10to50-LO')


samples['DY'] = {
    'name': files,
    'weight': mcCommonWeight + '*( !(Sum(PhotonGen_isPrompt==1 && PhotonGen_pt>15 && abs(PhotonGen_eta)<2.6) > 0))',
    'FilesPerJob': 1,
    #'EventsPerJob': 35000
}

addSampleWeight(samples,'DY','DYJetsToTT_MuEle_M-50','DY_NLO_pTllrw')
addSampleWeight(samples,'DY','DYJetsToLL_M-10to50-LO','DY_LO_pTllrw')


##### Top #######
files = nanoGetSampleFiles(mcDirectory, 'TTTo2L2Nu') + \
        nanoGetSampleFiles(mcDirectory, 'ST_s-channel') + \
        nanoGetSampleFiles(mcDirectory, 'ST_t-channel_top') + \
        nanoGetSampleFiles(mcDirectory, 'ST_t-channel_antitop') + \
        nanoGetSampleFiles(mcDirectory, 'ST_tW_antitop') + \
        nanoGetSampleFiles(mcDirectory, 'ST_tW_top')

samples['top'] = {
    'name': files,
    'weight': mcCommonWeightMatched,
    'FilesPerJob': 1,
    #'EventsPerJob': 35000
}

addSampleWeight(samples,'top','TTTo2L2Nu','Top_pTrw')


###### WW ########
samples['WW'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'WWTo2L2Nu'),
    'weight': mcCommonWeightMatched + '*nllW*ewknloW', 
    'FilesPerJob': 1,
    #'EventsPerJob': 35000
}


###### WWewk ########

samples['WWewk'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'WpWmJJ_EWK_noTop'),
    'weight': mcCommonWeight+ '*(Sum(abs(GenPart_pdgId)==6 || GenPart_pdgId==25)==0)', #filter tops and Higgs
    'FilesPerJob': 1,
    #'EventsPerJob': 50000
}

###### ggWW ########

samples['ggWW'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'GluGluToWWToENEN') + \
            nanoGetSampleFiles(mcDirectory, 'GluGluToWWToENMN') + \
            nanoGetSampleFiles(mcDirectory, 'GluGluToWWToENTN') + \
            nanoGetSampleFiles(mcDirectory, 'GluGluToWWToMNEN') + \
            nanoGetSampleFiles(mcDirectory, 'GluGluToWWToMNMN') + \
            nanoGetSampleFiles(mcDirectory, 'GluGluToWWToMNTN') + \
            nanoGetSampleFiles(mcDirectory, 'GluGluToWWToTNEN') + \
            nanoGetSampleFiles(mcDirectory, 'GluGluToWWToTNMN') + \
            nanoGetSampleFiles(mcDirectory, 'GluGluToWWToTNTN'),
    'weight': mcCommonWeight+'*1.53/1.4',
    'FilesPerJob': 1,
    #'EventsPerJob': 10000
}


######## Wg ########
files = nanoGetSampleFiles(mcDirectory, 'Wg_AMCNLOFXFX_01J')

samples['Wg'] = {
    'name': files,
    'weight': mcCommonWeight + '*(Gen_ZGstar_mass <= 0)',
    'suppressNegative' :['all'],
    'suppressNegativeNuisances' :['all'],
    'FilesPerJob': 2
}

######## Zg ########
files = nanoGetSampleFiles(mcDirectory, 'ZGToLLG')

samples['Zg'] = {
    'name': files,
    'weight': mcCommonWeight + '*(Gen_ZGstar_mass <= 0)',
    'suppressNegative' :['all'],
    'suppressNegativeNuisances' :['all'],
    'FilesPerJob': 2
}

######## WgS ######## 
files = nanoGetSampleFiles(mcDirectory, 'Wg_AMCNLOFXFX_01J') + \
        nanoGetSampleFiles(mcDirectory, 'WZTo3LNu_mllmin0p1')

samples['WgS'] = {
    'name': files,
    'weight': mcCommonWeightMatched + ' * (gstarLow * 0.94)',
    'suppressNegative' :['all'],
    'suppressNegativeNuisances' :['all'],
    'FilesPerJob': 2,
}
addSampleWeight(samples, 'WgS', 'Wg_AMCNLOFXFX_01J',  '(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 0.1)')
addSampleWeight(samples, 'WgS', 'WZTo3LNu_mllmin0p1', '(Gen_ZGstar_mass > 0.1)*(0.601644*58.59/4.666)')


######## ZgS ########
files = nanoGetSampleFiles(mcDirectory, 'ZGToLLG')

samples['ZgS'] = {
    'name': files,
    'weight': mcCommonWeightMatched,
    'suppressNegative' :['all'],
    'suppressNegativeNuisances' :['all'],
    'FilesPerJob': 2,
}
addSampleWeight(samples, 'ZgS', 'ZGToLLG', '(Gen_ZGstar_mass > 0)')


############ ZZ ############
samples['ZZ'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'ZZTo4L'),
    'weight': mcCommonWeightMatched,
    'FilesPerJob': 2
}


############ WZ ############
samples['WZ'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'WZTo3LNu_mllmin0p1'),
    'weight': mcCommonWeightMatched + ' * (gstarHigh)',
    'FilesPerJob': 2
}
addSampleWeight(samples, 'WZ', 'WZTo3LNu_mllmin0p1', '(0.601644*58.59/4.666)')


########## VVV #########
files = nanoGetSampleFiles(mcDirectory, 'ZZZ') + \
        nanoGetSampleFiles(mcDirectory, 'WZZ') + \
        nanoGetSampleFiles(mcDirectory, 'WWZ') + \
        nanoGetSampleFiles(mcDirectory, 'WWW')

samples['VVV'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 2
}

###########################################
#############   SIGNALS  ##################
###########################################

signals = []


############ ggH H->WW ############
samples['ggH_hww'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'GluGluHToWWTo2L2Nu_M125') + nanoGetSampleFiles(mcDirectory, 'GGHjjToWWTo2L2Nu_minloHJJ_M125'),                                                                
    'weight': mcCommonWeight,
    'FilesPerJob': 1,
    #'EventsPerJob': 25000
}
addSampleWeight(samples, 'ggH_hww', 'GluGluHToWWTo2L2Nu_M125', '(HTXS_stage1_1_cat_pTjet30GeV<107)*Weight2MINLO*1092.7640/1073.2567') #only non GE2J categories with the weight to NNLOPS and renormalize integral 
addSampleWeight(samples, 'ggH_hww', 'GGHjjToWWTo2L2Nu_minloHJJ_M125', '(HTXS_stage1_1_cat_pTjet30GeV>106)*1092.7640/1073.2567')                                                                            

signals.append('ggH_hww')


############ VBF H->WW ############
samples['qqH_hww'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'VBFHToWWTo2L2Nu_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 1,
    #'EventsPerJob': 25000
}


########### ggH+ggWW Interference ########
samples['ggH_gWW_Int'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'GluGluHToWWTo2L2Nu_M125') + \
            nanoGetSampleFiles(mcDirectory, 'GGHjjToWWTo2L2Nu_minloHJJ_M125') + \
            nanoGetSampleFiles(mcDirectory, 'GluGluToWWToENEN') + \
            nanoGetSampleFiles(mcDirectory, 'GluGluToWWToENMN') + \
            nanoGetSampleFiles(mcDirectory, 'GluGluToWWToENTN') + \
            nanoGetSampleFiles(mcDirectory, 'GluGluToWWToMNEN') + \
            nanoGetSampleFiles(mcDirectory, 'GluGluToWWToMNMN') + \
            nanoGetSampleFiles(mcDirectory, 'GluGluToWWToMNTN') + \
            nanoGetSampleFiles(mcDirectory, 'GluGluToWWToTNEN') + \
            nanoGetSampleFiles(mcDirectory, 'GluGluToWWToTNMN') + \
            nanoGetSampleFiles(mcDirectory, 'GluGluToWWToTNTN'),
    'weight': mcCommonWeight + '*ggHWW_Interference',
    'FilesPerJob': 1,
}

addSampleWeight(samples, 'ggH_gWW_Int', 'GluGluHToWWTo2L2Nu_M125', '(HTXS_stage1_1_cat_pTjet30GeV<107)*Weight2MINLO*1092.7640/1073.2567')
addSampleWeight(samples, 'ggH_gWW_Int', 'GGHjjToWWTo2L2Nu_minloHJJ_M125', '(HTXS_stage1_1_cat_pTjet30GeV>106)*1092.7640/1073.2567')
addSampleWeight(samples, 'ggH_gWW_Int', 'GluGluToWWToENEN', '1.53/1.4')
addSampleWeight(samples, 'ggH_gWW_Int', 'GluGluToWWToENMN', '1.53/1.4')
addSampleWeight(samples, 'ggH_gWW_Int', 'GluGluToWWToENTN', '1.53/1.4')
addSampleWeight(samples, 'ggH_gWW_Int', 'GluGluToWWToMNEN', '1.53/1.4')
addSampleWeight(samples, 'ggH_gWW_Int', 'GluGluToWWToMNMN', '1.53/1.4')
addSampleWeight(samples, 'ggH_gWW_Int', 'GluGluToWWToMNTN', '1.53/1.4')
addSampleWeight(samples, 'ggH_gWW_Int', 'GluGluToWWToTNEN', '1.53/1.4')
addSampleWeight(samples, 'ggH_gWW_Int', 'GluGluToWWToTNMN', '1.53/1.4')
addSampleWeight(samples, 'ggH_gWW_Int', 'GluGluToWWToTNTN', '1.53/1.4')


############ VBF+qqWW Interference ###########
samples['qqH_qqWW_Int'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'VBFHToWWTo2L2Nu_M125') + nanoGetSampleFiles(mcDirectory, 'WWTo2L2Nu') + nanoGetSampleFiles(mcDirectory, 'WpWmJJ_EWK_noTop'),
    'weight': mcCommonWeight + '*qqHWW_Interference',
    'FilesPerJob': 1,
}

addSampleWeight(samples, 'qqH_qqWW_Int', 'WpWmJJ_EWK_noTop', '(Sum(abs(GenPart_pdgId)==6 || GenPart_pdgId==25)==0)')
addSampleWeight(samples, 'qqH_qqWW_Int', 'WWTo2L2Nu', 'nllW*ewknloW')


'''
###### Dummy Total histograms for mkDatacards

samples['ggToWW'] = {
    'name': [],
    'weight': mcCommonWeight,
    'FilesPerJob': 1,
}

samples['qqToWW'] = {
    'name': [],
    'weight': mcCommonWeight,
    'FilesPerJob': 1,
}
'''
#### --------------------------------


############ ZH H->WW ############
samples['ZH_hww'] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'HZJ_HToWW_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 1
}

samples['ggZH_hww'] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'GluGluZH_HToWWTo2L2Nu_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 1
}

############ WH H->WW ############
samples['WH_hww_plus'] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'HWplusJ_HToWWTo2L2Nu_WToLNu_M125'), 
    'weight': mcCommonWeight,
    'FilesPerJob': 1,
    #'EventsPerJob': 50000
}

samples['WH_hww_minus'] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'HWminusJ_HToWWTo2L2Nu_WToLNu_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 1,
    #'EventsPerJob': 50000
}


############ ttH ############
samples['ttH_hww'] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'ttHToNonbb_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 1
}

############ H->TauTau ############
samples['ggH_htt'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'GluGluHToTauTau_M125_Powheg'), 
    'weight': mcCommonWeight,
    'FilesPerJob': 1
}

samples['qqH_htt'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'VBFHToTauTau_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 1
}

samples['ZH_htt'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'ZHToTauTau_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 1
}

############ WH H->TauTau ############
samples['WH_htt_plus'] = {
    'name':  nanoGetSampleFiles(mcDirectory, 'WplusHToTauTau_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 1
}

samples['WH_htt_minus'] = {
    'name':  nanoGetSampleFiles(mcDirectory, 'WminusHToTauTau_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 1
}


##################                                                                                                                                                                                         
#     ggH LL     #                                                                                                                                                                                         
##################                                                                                                                                                                                         

samples['ggH_HWLWL'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'GluGluHToWWTo2L2Nu_M125') + nanoGetSampleFiles(mcDirectory, 'GGHjjToWWTo2L2Nu_minloHJJ_M125'), 
    'weight': mcCommonWeight + '*Higgs_WW_LL*(Higgs_WW_LL>-5)',
    'FilesPerJob': 1,
    #'EventsPerJob': 25000
}

addSampleWeight(samples, 'ggH_HWLWL', 'GluGluHToWWTo2L2Nu_M125', '(HTXS_stage1_1_cat_pTjet30GeV<107)*Weight2MINLO*1092.7640/1073.2567') #only non GE2J categories with the weight to NNLOPS and renormalize integral                                                         
addSampleWeight(samples, 'ggH_HWLWL', 'GGHjjToWWTo2L2Nu_minloHJJ_M125', '(HTXS_stage1_1_cat_pTjet30GeV>106)*1092.7640/1073.2567')                                                                                                                                             

signals.append('ggH_HWLWL')


##################                                                                                                                                                                                         
#     ggH TT     #                                                                                                                                                                                         
##################                                                                                                                                                                                         

samples['ggH_HWTWT'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'GluGluHToWWTo2L2Nu_M125') + nanoGetSampleFiles(mcDirectory, 'GGHjjToWWTo2L2Nu_minloHJJ_M125'), 
    'weight': mcCommonWeight + '*Higgs_WW_TT*(Higgs_WW_TT>-5)',
    'FilesPerJob': 1,
    #'EventsPerJob': 25000
}

addSampleWeight(samples, 'ggH_HWTWT', 'GluGluHToWWTo2L2Nu_M125', '(HTXS_stage1_1_cat_pTjet30GeV<107)*Weight2MINLO*1092.7640/1073.2567')
addSampleWeight(samples, 'ggH_HWTWT', 'GGHjjToWWTo2L2Nu_minloHJJ_M125', '(HTXS_stage1_1_cat_pTjet30GeV>106)*1092.7640/1073.2567')
signals.append('ggH_HWTWT')


##################
#     qqH LL     #
##################

samples['qqH_HWLWL'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'VBFHToWWTo2L2Nu_M125'),
    'weight': mcCommonWeight + '*(Higgs_WW_LL*(Higgs_WW_LL>-5))',
    'FilesPerJob': 1,
    #'EventsPerJob': 25000
}

signals.append('qqH_HWLWL')

##################
#     qqH TT     #
##################

samples['qqH_HWTWT'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'VBFHToWWTo2L2Nu_M125'),
    'weight': mcCommonWeight + '*(Higgs_WW_TT*(Higgs_WW_TT>-5))',
    'FilesPerJob': 1,
    #'EventsPerJob': 25000
}

signals.append('qqH_HWTWT')



'''
######################                                                                                                                                                                                     
#      ggH Int       #                                                                                                                                                                                     
######################                                                                                                                                                                                     

samples['ggH_HWW_Int'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'GluGluHToWWTo2L2Nu_M125') + nanoGetSampleFiles(mcDirectory, 'GGHjjToWWTo2L2Nu_minloHJJ_M125'), 
    'weight': mcCommonWeight + '*(Higgs_WW_Int)',
    'FilesPerJob': 1,
    'EventsPerJob': 25000
}

addSampleWeight(samples, 'ggH_HWW_Int', 'GluGluHToWWTo2L2Nu_M125', '(HTXS_stage1_1_cat_pTjet30GeV<107)*Weight2MINLO*1092.7640/1073.2567') #only non GE2J categories with the weight to NNLOPS and renormalize integral                                                       
addSampleWeight(samples, 'ggH_HWW_Int', 'GGHjjToWWTo2L2Nu_minloHJJ_M125', '(HTXS_stage1_1_cat_pTjet30GeV>106)*1092.7640/1073.2567')                                                                        

signals.append('ggH_HWW_Int')
'''


###########################################
################## FAKE ###################
###########################################

samples['Fake'] = {
  'name': [],
  'weight': 'METFilter_DATA*fakeW',
  'weights': [],
  'isData': ['all'],
  'FilesPerJob': 10
}

for _, sd in DataRun:
  for pd in DataSets:
    tag = pd + '_' + sd

    if (   ('DoubleMuon' in pd and 'Run2018B' in sd)
        or ('DoubleMuon' in pd and 'Run2018D' in sd)
        or ('DoubleMuon' in pd and 'Run2018D' in sd)
        or ('SingleMuon' in pd and 'Run2018A' in sd)
        or ('SingleMuon' in pd and 'Run2018B' in sd)
        or ('SingleMuon' in pd and 'Run2018C' in sd)):
        print("sd      = {}".format(sd))
        print("pd      = {}".format(pd))
        print("Old tag = {}".format(tag))
        tag = tag.replace('v1','v2')
        print("New tag = {}".format(tag))

    files = nanoGetSampleFiles(fakeDirectory, tag)

    samples['Fake']['name'].extend(files)
    #samples['Fake']['weights'].extend([DataTrig[pd]] * len(files))
    addSampleWeight(samples, 'Fake', tag, DataTrig[pd])

###########################################
################## DATA ###################
###########################################

samples['DATA'] = {
  'name': [],
  'weight': 'LepWPCut*METFilter_DATA',
  'weights': [],
  'isData': ['all'],
  'FilesPerJob': 10
}

for _, sd in DataRun:
  for pd in DataSets:
    tag = pd + '_' + sd

    if (   ('DoubleMuon' in pd and 'Run2018B' in sd)
        or ('DoubleMuon' in pd and 'Run2018D' in sd)
        or ('DoubleMuon' in pd and 'Run2018D' in sd)
        or ('SingleMuon' in pd and 'Run2018A' in sd)
        or ('SingleMuon' in pd and 'Run2018B' in sd)
        or ('SingleMuon' in pd and 'Run2018C' in sd)):
        print("sd      = {}".format(sd))
        print("pd      = {}".format(pd))
        print("Old tag = {}".format(tag))
        tag = tag.replace('v1','v2')
        print("New tag = {}".format(tag))

    files = nanoGetSampleFiles(dataDirectory, tag)

    samples['DATA']['name'].extend(files)
    #samples['DATA']['weights'].extend([DataTrig[pd]] * len(files))
    addSampleWeight(samples, 'DATA', tag, DataTrig[pd])


