import os
import inspect
import numpy as np
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
embedReco    = 'Embedding2018_UL2018_nAODv9_Full2018v9'
embedSteps   = 'DATAl1loose2018v9__l2loose__l2tightOR2018v9__Embedding'

samples = {}


##############################################
###### Tree base directory for the site ######
##############################################

treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'
limitFiles = -1

def makeMCDirectory(var=''):
    return os.path.join(treeBaseDir, mcProduction, mcSteps.format(var=''))


mcDirectory = makeMCDirectory()
melaDirectory = '/eos/user/s/sblancof/MC/Summer20UL18_106x_nAODv9_Full2018v9/MCl1loose2018v9__MCCorr2018v9NoJERInHorn__l2tightOR2018v9__melaWeights/'
fakeDirectory = os.path.join(treeBaseDir, dataReco, fakeSteps)
dataDirectory = os.path.join(treeBaseDir, dataReco, dataSteps)
embedDirectory = os.path.join(treeBaseDir, embedReco, embedSteps)

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
#############    SIGNALS    ###############
########################################### 

doSignals = True
doTotal = True

###########################################
#############  BACKGROUNDS  ###############
###########################################


###### DY #######
useEmbeddedDY = True
useDYtt = True
runDYveto = True

embed_tautauveto = '' #Setup
if useEmbeddedDY:
  embed_tautauveto = '*embed_tautauveto'
  
files=[]


if useEmbeddedDY:
    samples['Dyemb'] = {
        'name': [],
        'weight': 'METFilter_DATA*LepWPCut*embedtotal',
        'weights': [],
        'isData': ['all'],
        'FilesPerJob': 2
    }

    for run_, sd in DataRun:
        files = nanoGetSampleFiles(embedDirectory, 'DYToTT_MuEle_Embedded_Run2018' + run_)
        samples['Dyemb']['name'].extend(files)
        addSampleWeight(samples, 'Dyemb', 'DYToTT_MuEle_Embedded_Run2018' + run_, '(Trigger_ElMu || Trigger_dblMu || Trigger_sngMu || Trigger_sngEl || Trigger_dblEl)')

    if runDYveto:
        # Vetoed MC: Needed for uncertainty
        files = nanoGetSampleFiles(mcDirectory, 'TTTo2L2Nu') + \
            nanoGetSampleFiles(mcDirectory, 'ST_s-channel') + \
            nanoGetSampleFiles(mcDirectory, 'ST_t-channel_top') + \
            nanoGetSampleFiles(mcDirectory, 'ST_t-channel_antitop') + \
            nanoGetSampleFiles(mcDirectory, 'ST_tW_antitop') + \
            nanoGetSampleFiles(mcDirectory, 'ST_tW_top') + \
            nanoGetSampleFiles(mcDirectory, 'WWJTo2L2Nu_minnlo') + \
            nanoGetSampleFiles(mcDirectory, 'WpWmJJ_EWK_noTop') + \
            nanoGetSampleFiles(mcDirectory, 'GluGluToWWToENEN') + \
            nanoGetSampleFiles(mcDirectory, 'GluGluToWWToENMN') + \
            nanoGetSampleFiles(mcDirectory, 'GluGluToWWToENTN') + \
            nanoGetSampleFiles(mcDirectory, 'GluGluToWWToMNEN') + \
            nanoGetSampleFiles(mcDirectory, 'GluGluToWWToMNMN') + \
            nanoGetSampleFiles(mcDirectory, 'GluGluToWWToMNTN') + \
            nanoGetSampleFiles(mcDirectory, 'GluGluToWWToTNEN') + \
            nanoGetSampleFiles(mcDirectory, 'GluGluToWWToTNMN') + \
            nanoGetSampleFiles(mcDirectory, 'GluGluToWWToTNTN') + \
            nanoGetSampleFiles(mcDirectory, 'ZZTo4L') + \
            nanoGetSampleFiles(mcDirectory, 'WZTo3LNu_mllmin0p1') + \
            nanoGetSampleFiles(mcDirectory, 'ZGToLLG')
        
        samples['Dyveto'] = {
            'name': files,
            'weight': '(1-embed_tautauveto)',
            'FilesPerJob': 1,
            'EventsPerJob': 50000
        }
        
        addSampleWeight(samples, 'Dyveto', 'TTTo2L2Nu', mcCommonWeightMatched + '* (topGenPt * antitopGenPt > 0.) * (TMath::Sqrt((0.103*TMath::Exp(-0.0118*topGenPt) - 0.000134*topGenPt + 0.973) * (0.103*TMath::Exp(-0.0118*antitopGenPt) - 0.000134*antitopGenPt + 0.973))) + (topGenPt * antitopGenPt <= 0.)')
        addSampleWeight(samples, 'Dyveto', 'ST_s-channel', mcCommonWeightMatched)
        addSampleWeight(samples, 'Dyveto', 'ST_t-channel_top', mcCommonWeightMatched)
        addSampleWeight(samples, 'Dyveto', 'ST_t-channel_antitop', mcCommonWeightMatched)
        addSampleWeight(samples, 'Dyveto', 'ST_tW_antitop', mcCommonWeightMatched)
        addSampleWeight(samples, 'Dyveto', 'ST_tW_top', mcCommonWeightMatched)
        addSampleWeight(samples, 'Dyveto', 'WWJTo2L2Nu_minnlo', mcCommonWeight)
        addSampleWeight(samples, 'Dyveto', 'WpWmJJ_EWK_noTop', mcCommonWeight + '*(Sum(abs(GenPart_pdgId)==6 || GenPart_pdgId==25)==0)')
        addSampleWeight(samples, 'Dyveto', 'GluGluToWWToENEN', mcCommonWeight + '*1.53/1.4')
        addSampleWeight(samples, 'Dyveto', 'GluGluToWWToENMN', mcCommonWeight + '*1.53/1.4')
        addSampleWeight(samples, 'Dyveto', 'GluGluToWWToENTN', mcCommonWeight + '*1.53/1.4')
        addSampleWeight(samples, 'Dyveto', 'GluGluToWWToMNEN', mcCommonWeight + '*1.53/1.4')
        addSampleWeight(samples, 'Dyveto', 'GluGluToWWToMNMN', mcCommonWeight + '*1.53/1.4')
        addSampleWeight(samples, 'Dyveto', 'GluGluToWWToMNTN', mcCommonWeight + '*1.53/1.4')
        addSampleWeight(samples, 'Dyveto', 'GluGluToWWToTNEN', mcCommonWeight + '*1.53/1.4')
        addSampleWeight(samples, 'Dyveto', 'GluGluToWWToTNMN', mcCommonWeight + '*1.53/1.4')
        addSampleWeight(samples, 'Dyveto', 'GluGluToWWToTNTN', mcCommonWeight + '*1.53/1.4')
        addSampleWeight(samples, 'Dyveto', 'ZZTo4L', mcCommonWeightMatched)
        addSampleWeight(samples, 'Dyveto', 'ZGToLLG', ' ( ' + mcCommonWeight + '*(!(Gen_ZGstar_mass > 0))' + ' ) + ( ' + mcCommonWeightMatched + ' * ((Gen_ZGstar_mass >0 && Gen_ZGstar_mass < 4) * 0.94 + (Gen_ZGstar_mass <0 || Gen_ZGstar_mass > 4) * 1.14) * (Gen_ZGstar_mass > 0)' + ' ) ') # Vg contribution + VgS contribution
        addSampleWeight(samples, 'Dyveto', 'WZTo3LNu_mllmin0p1', mcCommonWeightMatched + '*((Gen_ZGstar_mass >0 && Gen_ZGstar_mass < 4) * 0.94 + (Gen_ZGstar_mass <0 || Gen_ZGstar_mass > 4) * 1.14) * (Gen_ZGstar_mass > 0.1)')
        
if useDYtt:
    files = nanoGetSampleFiles(mcDirectory, 'DYJetsToTT_MuEle_M-50') + \
        nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-10to50-LO')
else:
    files = nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-50_ext2') + \
        nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-10to50-LO')   

samples['DY'] = {
    'name': files,
    'weight': mcCommonWeight + embed_tautauveto + '*( !(Sum(PhotonGen_isPrompt==1 && PhotonGen_pt>15 && abs(PhotonGen_eta)<2.6) > 0))',
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
    'weight': mcCommonWeightMatched + embed_tautauveto,
    'FilesPerJob': 1,
    'EventsPerJob': 35000
}

addSampleWeight(samples,'top','TTTo2L2Nu','Top_pTrw')


###### WW ########
#samples['WW'] = {
#    'name': nanoGetSampleFiles(mcDirectory, 'WWTo2L2Nu'),
#    'weight': mcCommonWeightMatched + '*nllW*ewknloW', 
#    'FilesPerJob': 1,
#    #'EventsPerJob': 35000
#}

samples['WW_minnlo'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'WWJTo2L2Nu_minnlo'),
    'weight': mcCommonWeight + embed_tautauveto,
    'FilesPerJob': 1,
    'EventsPerJob': 50000
}

###### WWewk ########

samples['WWewk'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'WpWmJJ_EWK_noTop'),
    'weight': mcCommonWeight + embed_tautauveto + '*(Sum(abs(GenPart_pdgId)==6 || GenPart_pdgId==25)==0)', #filter tops and Higgs
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
    #'weight': mcCommonWeight + embed_tautauveto +'*1.53/1.4',
    'weight': mcCommonWeight + embed_tautauveto +'* KFactor_ggWW / 1.4',
    'FilesPerJob': 1,
    'EventsPerJob': 10000
}


######## Vg ########
files = nanoGetSampleFiles(mcDirectory, 'ZGToLLG') + \
    nanoGetSampleFiles(mcDirectory, 'Wg_AMCNLOFXFX_01J')

samples['Vg'] = {
    'name': files,
    'weight': mcCommonWeight + embed_tautauveto + '*(Gen_ZGstar_mass <= 0)',
    'suppressNegative' :['all'],
    'suppressNegativeNuisances' :['all'],
    'FilesPerJob': 1,
    'EventsPerJob': 35000
}

######## VgS ######## 
files = nanoGetSampleFiles(mcDirectory, 'ZGToLLG') + \
    nanoGetSampleFiles(mcDirectory, 'Wg_AMCNLOFXFX_01J') + \
    nanoGetSampleFiles(mcDirectory, 'WZTo3LNu_mllmin0p1')

samples['VgS'] = {
    'name': files,
    'weight': mcCommonWeightMatched + embed_tautauveto,
    'suppressNegative' :['all'],
    'suppressNegativeNuisances' :['all'],
    'FilesPerJob': 1,
    'EventsPerJob': 35000
}
addSampleWeight(samples, 'VgS', 'ZGToLLG', '(Gen_ZGstar_mass > 0)')
addSampleWeight(samples, 'VgS', 'Wg_AMCNLOFXFX_01J',  '(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 0.1) * (gstarLow * 0.94)')
addSampleWeight(samples, 'VgS', 'WZTo3LNu_mllmin0p1', '(Gen_ZGstar_mass > 0.1)*(0.601644*58.59/4.666) * (gstarLow * 0.94)')

############ ZZ ############
samples['ZZ'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'ZZTo4L'),
    'weight': mcCommonWeightMatched + embed_tautauveto,
    'FilesPerJob': 1,
    'EventsPerJob': 50000
}


############ WZ ############
samples['WZ'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'WZTo3LNu_mllmin0p1'),
    'weight': mcCommonWeightMatched + embed_tautauveto + ' * (gstarHigh)',
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
    'EventsPerJob': 25000
}
addSampleWeight(samples, 'ggH_hww', 'GluGluHToWWTo2L2Nu_M125', '(HTXS_stage1_1_cat_pTjet30GeV<107)*Weight2MINLO*1092.7640/1073.2567') #only non GE2J categories with the weight to NNLOPS and renormalize integral 
addSampleWeight(samples, 'ggH_hww', 'GGHjjToWWTo2L2Nu_minloHJJ_M125', '(HTXS_stage1_1_cat_pTjet30GeV>106)*1092.7640/1073.2567')                                                                            

signals.append('ggH_hww')


############ VBF H->WW ############
samples['qqH_hww'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'VBFHToWWTo2L2Nu_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 1,
    'EventsPerJob': 25000
}

'''
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
    'EventsPerJob': 15000
}

addSampleWeight(samples, 'ggH_gWW_Int', 'GluGluHToWWTo2L2Nu_M125', '(HTXS_stage1_1_cat_pTjet30GeV<107)*Weight2MINLO*1092.7640/1073.2567')
addSampleWeight(samples, 'ggH_gWW_Int', 'GGHjjToWWTo2L2Nu_minloHJJ_M125', '(HTXS_stage1_1_cat_pTjet30GeV>106)*1092.7640/1073.2567')
addSampleWeight(samples, 'ggH_gWW_Int', 'GluGluToWWToENEN', 'KFactor_ggWW / 1.4')
addSampleWeight(samples, 'ggH_gWW_Int', 'GluGluToWWToENMN', 'KFactor_ggWW / 1.4')
addSampleWeight(samples, 'ggH_gWW_Int', 'GluGluToWWToENTN', 'KFactor_ggWW / 1.4')
addSampleWeight(samples, 'ggH_gWW_Int', 'GluGluToWWToMNEN', 'KFactor_ggWW / 1.4')
addSampleWeight(samples, 'ggH_gWW_Int', 'GluGluToWWToMNMN', 'KFactor_ggWW / 1.4')
addSampleWeight(samples, 'ggH_gWW_Int', 'GluGluToWWToMNTN', 'KFactor_ggWW / 1.4')
addSampleWeight(samples, 'ggH_gWW_Int', 'GluGluToWWToTNEN', 'KFactor_ggWW / 1.4')
addSampleWeight(samples, 'ggH_gWW_Int', 'GluGluToWWToTNMN', 'KFactor_ggWW / 1.4')
addSampleWeight(samples, 'ggH_gWW_Int', 'GluGluToWWToTNTN', 'KFactor_ggWW / 1.4')


############ VBF+qqWW Interference ###########
samples['qqH_qqWW_Int'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'VBFHToWWTo2L2Nu_M125') + nanoGetSampleFiles(mcDirectory, 'WWTo2L2Nu') + nanoGetSampleFiles(mcDirectory, 'WpWmJJ_EWK_noTop'),
    'weight': mcCommonWeight + '*qqHWW_Interference',
    'FilesPerJob': 1,
    'EventsPerJob': 25000
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

samples['ggWW_si'] = {
    'name': [],
    'weight': mcCommonWeight,
    'FilesPerJob': 1,
}

samples['WWewk_si'] = {
    'name': [],
    'weight': mcCommonWeight,
    'FilesPerJob': 1,
}


#### --------------------------------

files = nanoGetSampleFiles(mcDirectory, 'HZJ_HToWW_M125') + \
          nanoGetSampleFiles(mcDirectory, 'GluGluZH_HToWWTo2L2Nu_M125') + \
          nanoGetSampleFiles(mcDirectory, 'HWplusJ_HToWWTo2L2Nu_WToLNu_M125') + \
          nanoGetSampleFiles(mcDirectory, 'HWminusJ_HToWWTo2L2Nu_WToLNu_M125') + \
          nanoGetSampleFiles(mcDirectory, 'ttHToNonbb_M125')

samples['hww'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 1,
    'EventsPerJob': 50000,
}


############ H->TauTau ############

files = nanoGetSampleFiles(mcDirectory, 'GluGluHToTauTau_M125_Powheg') + \
    nanoGetSampleFiles(mcDirectory, 'VBFHToTauTau_M125') + \
    nanoGetSampleFiles(mcDirectory, 'ZHToTauTau_M125') + \
    nanoGetSampleFiles(mcDirectory, 'WplusHToTauTau_M125') + \
    nanoGetSampleFiles(mcDirectory, 'WminusHToTauTau_M125')

samples['htt'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 1
}


##################                                                                                                                                                                                         
#     ggH LL     #                                                                                                                                                                                         
##################                                                                                                                                                                                         

samples['ggH_HWLWL'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'GluGluHToWWTo2L2Nu_M125') + nanoGetSampleFiles(mcDirectory, 'GGHjjToWWTo2L2Nu_minloHJJ_M125'), 
    'weight': mcCommonWeight + ' * p_GEN_fL_1p0_fPerp_0p0',
    'FilesPerJob': 1,
    'EventsPerJob': 25000,
    'friendFiles': melaDirectory,
}

addSampleWeight(samples, 'ggH_HWLWL', 'GluGluHToWWTo2L2Nu_M125', '(HTXS_stage1_1_cat_pTjet30GeV<107)*Weight2MINLO*1092.7640/1073.2567') #only non GE2J categories with the weight to NNLOPS and renormalize integral                                                         
addSampleWeight(samples, 'ggH_HWLWL', 'GGHjjToWWTo2L2Nu_minloHJJ_M125', '(HTXS_stage1_1_cat_pTjet30GeV>106)*1092.7640/1073.2567')                                                                                                                                             

signals.append('ggH_HWLWL')

##################                                                                                                                                                                                         
#     ggH TT     #                                                                                                                                                                                         
##################                                                                                                                                                                                         

samples['ggH_HWTWT'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'GluGluHToWWTo2L2Nu_M125') + nanoGetSampleFiles(mcDirectory, 'GGHjjToWWTo2L2Nu_minloHJJ_M125'), 
    'weight': mcCommonWeight + ' * p_GEN_fL_0p0_fPerp_0p0',
    'FilesPerJob': 1,
    'EventsPerJob': 25000,
    'friendFiles': melaDirectory,
}

addSampleWeight(samples, 'ggH_HWTWT', 'GluGluHToWWTo2L2Nu_M125', '(HTXS_stage1_1_cat_pTjet30GeV<107)*Weight2MINLO*1092.7640/1073.2567')
addSampleWeight(samples, 'ggH_HWTWT', 'GGHjjToWWTo2L2Nu_minloHJJ_M125', '(HTXS_stage1_1_cat_pTjet30GeV>106)*1092.7640/1073.2567')
signals.append('ggH_HWTWT')

################## 
#    ggH Perp    # 
##################

samples['ggH_perp'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'GluGluHToWWTo2L2Nu_M125') + nanoGetSampleFiles(mcDirectory, 'GGHjjToWWTo2L2Nu_minloHJJ_M125'),
    'weight': mcCommonWeight + ' * p_GEN_fL_0p0_fPerp_1p0',
    'FilesPerJob': 1,
    'EventsPerJob': 25000,
    'friendFiles': melaDirectory,
}

addSampleWeight(samples, 'ggH_perp', 'GluGluHToWWTo2L2Nu_M125', '(HTXS_stage1_1_cat_pTjet30GeV<107)*Weight2MINLO*1092.7640/1073.2567')
addSampleWeight(samples, 'ggH_perp', 'GGHjjToWWTo2L2Nu_minloHJJ_M125', '(HTXS_stage1_1_cat_pTjet30GeV>106)*1092.7640/1073.2567')
signals.append('ggH_perp')

##################
#     qqH LL     #
##################

samples['qqH_HWLWL'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'VBFHToWWTo2L2Nu_M125'),
    'weight': mcCommonWeight + ' * p_GEN_fL_1p0_fPerp_0p0',
    'FilesPerJob': 1,
    'EventsPerJob': 25000,
    'friendFiles': melaDirectory,
}

signals.append('qqH_HWLWL')

##################
#     qqH TT     #
##################

samples['qqH_HWTWT'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'VBFHToWWTo2L2Nu_M125'),
    'weight': mcCommonWeight + ' * p_GEN_fL_0p0_fPerp_0p0',
    'FilesPerJob': 1,
    'EventsPerJob': 25000,
    'friendFiles': melaDirectory,
}

signals.append('qqH_HWTWT')

################## 
#    qqH perp    #
##################

samples['qqH_perp'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'VBFHToWWTo2L2Nu_M125'),
    'weight': mcCommonWeight + ' * p_GEN_fL_0p0_fPerp_1p0',
    'FilesPerJob': 1,
    'EventsPerJob': 25000,
    'friendFiles': melaDirectory,
}

signals.append('qqH_perp')

###########################################
################## FAKE ###################
###########################################

samples['Fake'] = {
  'name': [],
  'weight': 'METFilter_DATA*fakeW',
  'weights': [],
  'isData': ['all'],
  'FilesPerJob': 1
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
    addSampleWeight(samples, 'DATA', tag, DataTrig[pd])


    
######### All polarization signals ########### 

if doSignals:

    if not doTotal:
        samples = {}

    for i in np.linspace(-1, 1, 21):
        jlim = round(1.0 - abs(i), 2)
        jn = 2 * 10*abs(jlim) + 2
        for j in np.linspace(-1*jlim, jlim, int(jn)-1):
            i = round(i, 1)
            j = round(j, 1)
            
            if i<0.0:
                itxt = str(i).replace("-", "m")
            else:
                itxt = str(i)
            itxt = itxt.replace(".", "p")

            if j<0.0:
                jtxt = str(j).replace("-", "m")
            else:
                jtxt = str(j)
            jtxt = jtxt.replace(".", "p")            
            
            weighttxt = f"p_GEN_fL_{itxt}_fPerp_{jtxt}"
            txt = f"_fL_{itxt}_fPerp_{jtxt}"
            
            samples['ggH'+txt] = {
                'name': nanoGetSampleFiles(mcDirectory, 'GluGluHToWWTo2L2Nu_M125') + nanoGetSampleFiles(mcDirectory, 'GGHjjToWWTo2L2Nu_minloHJJ_M125'),
                'weight': mcCommonWeight + f' * {weighttxt}',
                'FilesPerJob': 1,
                'friendFiles': melaDirectory,
            }
            addSampleWeight(samples, 'ggH'+txt, 'GluGluHToWWTo2L2Nu_M125', '(HTXS_stage1_1_cat_pTjet30GeV<107)*Weight2MINLO*1092.7640/1073.2567')
            addSampleWeight(samples, 'ggH'+txt, 'GGHjjToWWTo2L2Nu_minloHJJ_M125', '(HTXS_stage1_1_cat_pTjet30GeV>106)*1092.7640/1073.2567')

            samples['qqH'+txt] = {    
                'name': nanoGetSampleFiles(mcDirectory, 'VBFHToWWTo2L2Nu_M125'),
                'weight': mcCommonWeight + f' * {weighttxt}',
                'FilesPerJob': 1,  
                'friendFiles': melaDirectory,    
            } 
            
