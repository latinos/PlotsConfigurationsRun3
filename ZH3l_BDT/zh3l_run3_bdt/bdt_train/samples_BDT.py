import os
import subprocess

# global getSampleFiles
# from LatinoAnalysis.Tools.commonTools import getSampleFiles, addSampleWeight, getBaseWnAOD
# It looks like getBaseWnAOD and addSampleWeight from Latinos does the same job as CombineBaseW function from makeShapesRDF. Similarly getSampleFiles function from Latinos is the same as nanoGetSampleFiles from makeShapesRDF.

from mkShapesRDF.lib.search_files import SearchFiles
searchFiles = SearchFiles()
redirector = ""
limitFiles = 1
samples = {}

def nanoGetSampleFiles(path, name):
    _files = searchFiles.searchFiles(path, name, redirector=redirector)
    if limitFiles != -1 and len(_files) > limitFiles:
        print("Found {} files for sample {}".format(len(_files), name))
        return [(name, _files[:limitFiles])]
    else:
        print("Found {} files for sample {}".format(len(_files), name))
        return [(name, _files)]

def getSampleFilesNano(inputDir,Sample,absPath=False):
    # return getSampleFiles(inputDir,Sample,absPath,'nanoLatino_')
    return nanoGetSampleFiles(inputDir, Sample)

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
    return newbaseW # "/baseW is used after getBaseWnAOD/CombineBaseW calls in this code"
    # weight = newbaseW + "/baseW"

    # for iSample in samplelist:
    #     addSampleWeight(samples, proc, iSample, weight)


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


##############################################
###### Tree Directory according to site ######
##############################################

SITE=os.uname()[1]
xrootdPath=''
# xrootdPath='root://eoscms.cern.ch/'
treeBaseDir = '/eos/user/d/dshekar/MCsamplesForBDTzh3l/'
# treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/'

directory = treeBaseDir+'Summer22_130x_nAODv12_Full2022v12/MCl2loose2022v12__MCCorr2022v12JetScaling__l2tight'

################################################
############ NUMBER OF LEPTONS #################
################################################

#Nlep='2'
Nlep='3'
#Nlep='4'

################################################
############### Lepton WP ######################
################################################

eleWP='mvaFall17V1Iso_WP90'
#eleWP='mvaFall17V1Iso_WP90_SS'
#eleWP='mvaFall17V2Iso_WP90'
#eleWP='mvaFall17V2Iso_WP90_SS'
muWP ='cut_Tight_HWWW'
eleWP_new = 'cutBased_MediumID_tthMVA_Run3'
muWP_new  = 'cut_TightID_pfIsoTight_HWW_tthmva_67'


LepWPCut        = 'LepCut'+Nlep+'l__ele_'+eleWP_new+'__mu_'+muWP_new
#LepWPCut        = 'LepCut'+Nlep+'l__ele_'+eleWP+'__mu_'+muWP
#LepWPweight     = 'ttHMVA_SF_3l[0]' #SF for new WPs, defined in aliases
LepWPweight     = 'LepSF'+Nlep+'l__ele_'+eleWP_new+'__mu_'+muWP_new

################################################
############ BASIC MC WEIGHTS ##################
################################################

XSWeight      = 'XSWeight'
SFweight      = 'SFweight'+Nlep+'l*'+LepWPweight+'*'+LepWPCut#+'*Jet_PUIDSF'
PromptGenLepMatch   = 'PromptGenLepMatch'+Nlep+'l'

################################################
############## FAKE WEIGHTS ####################
################################################

#eleWP_new = 'mvaFall17V1Iso_WP90_tthmva_70'
#muWP_new  = 'cut_Tight_HWWW_tthmva_80'

if Nlep == '2' :
  fakeW = 'fakeW2l_ele_'+eleWP_new+'_mu_'+muWP_new
  #fakeW = 'fakeW2l_ele_'+eleWP+'_mu_'+muWP
else:
  fakeW = 'fakeW_ele_'+eleWP_new+'_mu_'+muWP_new+'_'+Nlep+'l'
  #fakeW = 'fakeW_ele_'+eleWP+'_mu_'+muWP+'_'+Nlep+'l'

################################################
############### B-Tag  WP ######################
################################################

SFweight += '*btagSF' #define in aliases.py

################################################
############   MET  FILTERS  ###################
################################################

METFilter_MC   = 'METFilter_MC'
METFilter_DATA = 'METFilter_DATA'

################################################
############ DATA DECLARATION ##################
################################################

DataRun = [
    ['C','Run2022C-ReReco-v1'],
    ['D','Run2022D-ReReco-v1'],
]

DataSets = ['MuonEG','Muon','EGamma']

DataTrig = {
    'MuonEG'         : 'Trigger_ElMu' ,
    'Muon'           : '!Trigger_ElMu && (Trigger_sngMu || Trigger_dblMu)',
    'EGamma'         : '!Trigger_ElMu && !Trigger_sngMu && !Trigger_dblMu && (Trigger_sngEl || Trigger_dblEl)'
}

###########################################
#############  BACKGROUNDS  ###############
###########################################

############ DY ############

ptllDYW_NLO = '1'
ptllDYW_LO = '1'

#####  WZ

samples['WZ']  = {    'name':   getSampleFilesNano(directory,'WZTo3LNu')
                              + getSampleFilesNano(directory,'WZTo2L2Q')
                              + getSampleFilesNano(directory,'WZ'),
                       'weight' : XSWeight+'*'+SFweight+'*'+PromptGenLepMatch+'*'+METFilter_MC+'*(gstarHigh)' ,
                       'FilesPerJob' : 5 ,
                  }

samples['ZZ'] = {  'name'  :   getSampleFilesNano(directory,'ZZ'),
                    'weight' : XSWeight+'*'+SFweight+'*'+PromptGenLepMatch+'*'+METFilter_MC,
                    'FilesPerJob' : 3,
                 }

##########################################
################ SIGNALS #################
##########################################

############ ZH H->WW ############

# samples['ZH_hww']  = {  'name'   :   getSampleFilesNano(directory,'HZJ_HToWW_M125'),
#                         'weight' : XSWeight+'*'+SFweight+'*'+PromptGenLepMatch+'*'+METFilter_MC ,
#                      }

samples['ggZH_hww']  = {  'name'   :   getSampleFilesNano(directory,'GluGluZH_Zto2L_Hto2WtoLNu2Q'),
                        'weight' : XSWeight+'*'+SFweight+'*'+PromptGenLepMatch+'*'+METFilter_MC ,
                     }

# directory = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano/Run2018_102X_nAODv7_Full2018v7/DATAl1loose2018v7__l2loose__fakeW/'

############
### DATA ###
############

samples['DATA'] = { 
    'name': [],  
    'weight': 'LepWPCut*METFilter_DATA',     
    'weights': [], 
    'isData': ['all'], 
    'FilesPerJob': 15 
} 


mcProduction = 'Summer22_130x_nAODv12_Full2022v12'
dataReco = 'Run2022_ReReco_nAODv12_Full2022v12'
dataSteps = 'DATAl2loose2022v12__l2loose'
treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'
dataDirectory = os.path.join(treeBaseDir, dataReco, dataSteps)


for _, sd in DataRun:
  for pd in DataSets:
    datatag = pd + '_' + sd

    files = nanoGetSampleFiles(dataDirectory, datatag)
    
    print(datatag)

    samples['DATA']['name'].extend(files)
    addSampleWeight(samples, 'DATA', datatag, DataTrig[pd])