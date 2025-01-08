import os, glob
mcProduction = 'Summer20UL18_106x_nAODv9_Full2018v9'
dataReco = 'Run2018_UL2018_nAODv9_Full2018v9'
mcSteps = 'MCl1loose2018v9__MCCorr2018v9NoJERInHorn__l2tightOR2018v9'
fakeSteps = 'DATAl1loose2018v9__l2loose__fakeW'
dataSteps = 'DATAl1loose2018v9__l2loose__l2tightOR2018v9'

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
    f = ROOT.TFile.Open(leastFiles[0])
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
mcCommonWeightNoMatch = 'XSWeight*METFilter_MC*SFweight'
mcCommonWeight = 'XSWeight*METFilter_MC*PromptGenLepMatch2l*SFweight'

###########################################
#############  BACKGROUNDS  ###############
###########################################


useEmbeddedDY = False
embed_tautauveto = ''

###### DY #######

files = nanoGetSampleFiles(mcDirectory, 'DYJetsToTT_MuEle_M-50') + \
        nanoGetSampleFiles(mcDirectory, 'DYJetsToLL_M-10to50-LO')

samples['dytt'] = {
    'name': files,
    'weight': mcCommonWeight + '*(Lepton_pdgId[0]*Lepton_pdgId[1] == -11*13)*( !(Sum(PhotonGen_isPrompt==1 && PhotonGen_pt>15 && abs(PhotonGen_eta)<2.6) > 0))',
    'FilesPerJob': 4,
}

##### Top #######

files = nanoGetSampleFiles(mcDirectory, 'TTTo2L2Nu') + \
         nanoGetSampleFiles(mcDirectory, 'ST_s-channel') + \
         nanoGetSampleFiles(mcDirectory, 'ST_t-channel_top') + \
         nanoGetSampleFiles(mcDirectory, 'ST_t-channel_antitop') + \
         nanoGetSampleFiles(mcDirectory, 'ST_tW_antitop') + \
         nanoGetSampleFiles(mcDirectory, 'ST_tW_top')

samples['top'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 1,
}

addSampleWeight(samples,'top','TTTo2L2Nu','Top_pTrw')

##### Other ######

###### WW ########

samples['WW'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'WWTo2L2Nu'),
    'weight': mcCommonWeight + '*nllW', # temporary - nllW module not run on PS and UE variation samples
    'FilesPerJob': 3
}

samples['WWewk'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'WpWmJJ_EWK_noTop'),
    'weight': mcCommonWeight+embed_tautauveto + '*(Sum(abs(GenPart_pdgId)==6 || GenPart_pdgId==25)==0)', # Filter tops and Higgs,
    'FilesPerJob': 3
}


files = nanoGetSampleFiles(mcDirectory, 'GluGluToWWToENEN') + \
        nanoGetSampleFiles(mcDirectory, 'GluGluToWWToENMN') + \
        nanoGetSampleFiles(mcDirectory, 'GluGluToWWToENTN') + \
        nanoGetSampleFiles(mcDirectory, 'GluGluToWWToMNEN') + \
        nanoGetSampleFiles(mcDirectory, 'GluGluToWWToMNMN') + \
        nanoGetSampleFiles(mcDirectory, 'GluGluToWWToMNTN') + \
        nanoGetSampleFiles(mcDirectory, 'GluGluToWWToTNEN') + \
        nanoGetSampleFiles(mcDirectory, 'GluGluToWWToTNMN') + \
        nanoGetSampleFiles(mcDirectory, 'GluGluToWWToTNTN')

samples['ggWW'] = {
    'name': files,
    'weight': mcCommonWeight+embed_tautauveto + '*1.53/1.4', # updating k-factor <-- do we still need the k-factor?
    'FilesPerJob': 4
}

######## Vg ########

files = nanoGetSampleFiles(mcDirectory, 'Wg_AMCNLOFXFX_01J_PDF') + \
        nanoGetSampleFiles(mcDirectory, 'Wg_AMCNLOFXFX_01J') + \
        nanoGetSampleFiles(mcDirectory, 'ZGToLLG')

samples['Vg'] = {
    'name': files,
    'weight': mcCommonWeightNoMatch+embed_tautauveto + '*(!(Gen_ZGstar_mass > 0))',
    'FilesPerJob': 4
}

CombineBaseW(samples, 'Vg', ['Wg_AMCNLOFXFX_01J_PDF', 'Wg_AMCNLOFXFX_01J'])

######## VgS ########

files = nanoGetSampleFiles(mcDirectory, 'Wg_AMCNLOFXFX_01J_PDF') + \
        nanoGetSampleFiles(mcDirectory, 'Wg_AMCNLOFXFX_01J') + \
        nanoGetSampleFiles(mcDirectory, 'ZGToLLG') + \
        nanoGetSampleFiles(mcDirectory, 'WZTo3LNu_mllmin4p0') 

samples['VgS'] = {
    'name': files,
    'weight': mcCommonWeight+embed_tautauveto + ' * (gstarLow * 0.94 + gstarHigh * 1.14)',
    'FilesPerJob': 4,
    'subsamples': {
      'L': 'gstarLow',
      'H': 'gstarHigh'
    }
}

CombineBaseW(samples, 'VgS', ['Wg_AMCNLOFXFX_01J_PDF', 'Wg_AMCNLOFXFX_01J'])

addSampleWeight(samples, 'VgS', 'Wg_AMCNLOFXFX_01J_PDF', '(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4.0)')
addSampleWeight(samples, 'VgS', 'Wg_AMCNLOFXFX_01J', '(Gen_ZGstar_mass > 0 && Gen_ZGstar_mass <= 4.0)')
addSampleWeight(samples, 'VgS', 'ZGToLLG', '(Gen_ZGstar_mass > 0)')
addSampleWeight(samples, 'VgS', 'WZTo3LNu_mllmin4p0', '(Gen_ZGstar_mass > 4.0)')

############ VZ ############

files = nanoGetSampleFiles(mcDirectory, 'ZZTo2L2Nu') + \
        nanoGetSampleFiles(mcDirectory, 'ZZTo2Q2L_mllmin4p0') + \
        nanoGetSampleFiles(mcDirectory, 'WZTo2Q2L_mllmin4p0') # 'WZTo2L2Q')

samples['VZ'] = {
    'name': files,
    'weight': mcCommonWeight+embed_tautauveto + '*1.11',
    'FilesPerJob': 4
}

########## VVV #########

files = nanoGetSampleFiles(mcDirectory, 'ZZZ') + \
        nanoGetSampleFiles(mcDirectory, 'WZZ') + \
        nanoGetSampleFiles(mcDirectory, 'WWZ') + \
        nanoGetSampleFiles(mcDirectory, 'WWW')
#+ nanoGetSampleFiles(mcDirectory, 'WWG'), #should this be included? or is it already taken into account in the WW sample?

samples['VVV'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 4
}


###########################################
#############   SIGNALS  ##################
###########################################

############## ggH -> WW ############


samples['ggH_hww'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'GGHjjToWWTo2L2Nu_minloHJJ_M125'),
    'weight': mcCommonWeight + '*1.103',
    'FilesPerJob': 5,
    'subsamples' : {
          'GenDeltaPhijj_0fid' : '(isFID == 1 && GenDeltaPhijj > -(TMath::Pi()) && GenDeltaPhijj <= -(TMath::Pi())/2)',
          'GenDeltaPhijj_1fid' : '(isFID == 1 && GenDeltaPhijj > -(TMath::Pi())/2 && GenDeltaPhijj <= 0)',
          'GenDeltaPhijj_2fid' : '(isFID == 1 && GenDeltaPhijj > 0 && GenDeltaPhijj <= (TMath::Pi())/2)',
          'GenDeltaPhijj_3fid' : '(isFID == 1 && GenDeltaPhijj > (TMath::Pi())/2 && GenDeltaPhijj <= (TMath::Pi()))',
          'GenDeltaPhijj_0nonfid' : '(isFID <= 0 && GenDeltaPhijj > -(TMath::Pi()) && GenDeltaPhijj <= -(TMath::Pi())/2)',
          'GenDeltaPhijj_1nonfid' : '(isFID <= 0 && GenDeltaPhijj > -(TMath::Pi())/2 && GenDeltaPhijj <= 0)',
          'GenDeltaPhijj_2nonfid' : '(isFID <= 0 && GenDeltaPhijj > 0 && GenDeltaPhijj <= (TMath::Pi())/2)',
          'GenDeltaPhijj_3nonfid' : '(isFID <= 0 && GenDeltaPhijj > (TMath::Pi())/2 && GenDeltaPhijj <= (TMath::Pi()))',
          'noGenDeltaPhijj' : '(isFID <= 0 && GenDeltaPhijj==-9999)'
     }
}

########### VBF H->WW ############

samples['qqH_hww'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'VBFHToWWTo2L2Nu_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 4,
    'subsamples' : {
         'GenDeltaPhijj_0fid' : '(isFID == 1 && GenDeltaPhijj > -(TMath::Pi()) && GenDeltaPhijj <= -(TMath::Pi())/2)',
         'GenDeltaPhijj_1fid' : '(isFID == 1 && GenDeltaPhijj > -(TMath::Pi())/2 && GenDeltaPhijj <= 0)',
         'GenDeltaPhijj_2fid' : '(isFID == 1 && GenDeltaPhijj > 0 && GenDeltaPhijj <= (TMath::Pi())/2)',
         'GenDeltaPhijj_3fid' : '(isFID == 1 && GenDeltaPhijj > (TMath::Pi())/2 && GenDeltaPhijj <= (TMath::Pi()))',
         'GenDeltaPhijj_0nonfid' : '(isFID <= 0 && GenDeltaPhijj > -(TMath::Pi()) && GenDeltaPhijj <= -(TMath::Pi())/2)',
         'GenDeltaPhijj_1nonfid' : '(isFID <= 0 && GenDeltaPhijj > -(TMath::Pi())/2 && GenDeltaPhijj <= 0)',
         'GenDeltaPhijj_2nonfid' : '(isFID <= 0 && GenDeltaPhijj > 0 && GenDeltaPhijj <= (TMath::Pi())/2)',
         'GenDeltaPhijj_3nonfid' : '(isFID <= 0 && GenDeltaPhijj > (TMath::Pi())/2 && GenDeltaPhijj <= (TMath::Pi()))',
         'noGenDeltaPhijj' : '(isFID <= 0 && GenDeltaPhijj==-9999)'
     }
}

# Original VBF samples 

samples['VBF_H0M'] = { 
   'name':   nanoGetSampleFiles(mcDirectory, 'VBF_H0M_ToWWTo2L2Nu'), 
   'weight': mcCommonWeight+ '*VBF_H0M_W',   
   'FilesPerJob': 4, 
   'subsamples' : {
         'GenDeltaPhijj_0fid' : '(isFID == 1 && GenDeltaPhijj > -(TMath::Pi()) && GenDeltaPhijj <= -(TMath::Pi())/2)',
         'GenDeltaPhijj_1fid' : '(isFID == 1 && GenDeltaPhijj > -(TMath::Pi())/2 && GenDeltaPhijj <= 0)',
         'GenDeltaPhijj_2fid' : '(isFID == 1 && GenDeltaPhijj > 0 && GenDeltaPhijj <= (TMath::Pi())/2)',
         'GenDeltaPhijj_3fid' : '(isFID == 1 && GenDeltaPhijj > (TMath::Pi())/2 && GenDeltaPhijj <= (TMath::Pi()))',
         'GenDeltaPhijj_0nonfid' : '(isFID <= 0 && GenDeltaPhijj > -(TMath::Pi()) && GenDeltaPhijj <= -(TMath::Pi())/2)',
         'GenDeltaPhijj_1nonfid' : '(isFID <= 0 && GenDeltaPhijj > -(TMath::Pi())/2 && GenDeltaPhijj <= 0)',
         'GenDeltaPhijj_2nonfid' : '(isFID <= 0 && GenDeltaPhijj > 0 && GenDeltaPhijj <= (TMath::Pi())/2)',
         'GenDeltaPhijj_3nonfid' : '(isFID <= 0 && GenDeltaPhijj > (TMath::Pi())/2 && GenDeltaPhijj <= (TMath::Pi()))',
         'noGenDeltaPhijj' : '(isFID <= 0 && GenDeltaPhijj==-9999)'
     }
   
} 

samples['VBF_H0Mf05'] = { 
   'name':   nanoGetSampleFiles(mcDirectory, 'VBF_H0Mf05_ToWWTo2L2Nu'), 
   'weight': mcCommonWeight+ '*VBF_H0Mf05_W',   
   'FilesPerJob': 4, 
   'subsamples' : {
         'GenDeltaPhijj_0fid' : '(isFID == 1 && GenDeltaPhijj > -(TMath::Pi()) && GenDeltaPhijj <= -(TMath::Pi())/2)',
         'GenDeltaPhijj_1fid' : '(isFID == 1 && GenDeltaPhijj > -(TMath::Pi())/2 && GenDeltaPhijj <= 0)',
         'GenDeltaPhijj_2fid' : '(isFID == 1 && GenDeltaPhijj > 0 && GenDeltaPhijj <= (TMath::Pi())/2)',
         'GenDeltaPhijj_3fid' : '(isFID == 1 && GenDeltaPhijj > (TMath::Pi())/2 && GenDeltaPhijj <= (TMath::Pi()))',
         'GenDeltaPhijj_0nonfid' : '(isFID <= 0 && GenDeltaPhijj > -(TMath::Pi()) && GenDeltaPhijj <= -(TMath::Pi())/2)',
         'GenDeltaPhijj_1nonfid' : '(isFID <= 0 && GenDeltaPhijj > -(TMath::Pi())/2 && GenDeltaPhijj <= 0)',
         'GenDeltaPhijj_2nonfid' : '(isFID <= 0 && GenDeltaPhijj > 0 && GenDeltaPhijj <= (TMath::Pi())/2)',
         'GenDeltaPhijj_3nonfid' : '(isFID <= 0 && GenDeltaPhijj > (TMath::Pi())/2 && GenDeltaPhijj <= (TMath::Pi()))',
         'noGenDeltaPhijj' : '(isFID <= 0 && GenDeltaPhijj==-9999)'
     }
} 


samples['VBF_H0PH'] = { 
   'name':   nanoGetSampleFiles(mcDirectory, 'VBF_H0PH_ToWWTo2L2Nu'), 
   'weight': mcCommonWeight+ '*VBF_H0PH_W',   
   'FilesPerJob': 4, 
   'subsamples' : {
         'GenDeltaPhijj_0fid' : '(isFID == 1 && GenDeltaPhijj > -(TMath::Pi()) && GenDeltaPhijj <= -(TMath::Pi())/2)',
         'GenDeltaPhijj_1fid' : '(isFID == 1 && GenDeltaPhijj > -(TMath::Pi())/2 && GenDeltaPhijj <= 0)',
         'GenDeltaPhijj_2fid' : '(isFID == 1 && GenDeltaPhijj > 0 && GenDeltaPhijj <= (TMath::Pi())/2)',
         'GenDeltaPhijj_3fid' : '(isFID == 1 && GenDeltaPhijj > (TMath::Pi())/2 && GenDeltaPhijj <= (TMath::Pi()))',
         'GenDeltaPhijj_0nonfid' : '(isFID <= 0 && GenDeltaPhijj > -(TMath::Pi()) && GenDeltaPhijj <= -(TMath::Pi())/2)',
         'GenDeltaPhijj_1nonfid' : '(isFID <= 0 && GenDeltaPhijj > -(TMath::Pi())/2 && GenDeltaPhijj <= 0)',
         'GenDeltaPhijj_2nonfid' : '(isFID <= 0 && GenDeltaPhijj > 0 && GenDeltaPhijj <= (TMath::Pi())/2)',
         'GenDeltaPhijj_3nonfid' : '(isFID <= 0 && GenDeltaPhijj > (TMath::Pi())/2 && GenDeltaPhijj <= (TMath::Pi()))',
         'noGenDeltaPhijj' : '(isFID <= 0 && GenDeltaPhijj==-9999)'
     }
} 


samples['VBF_H0PHf05'] = { 
   'name':   nanoGetSampleFiles(mcDirectory, 'VBF_H0PHf05_ToWWTo2L2Nu'), 
   'weight': mcCommonWeight+ '*VBF_H0PHf05_W',   
   'FilesPerJob': 4, 
   'subsamples' : {
         'GenDeltaPhijj_0fid' : '(isFID == 1 && GenDeltaPhijj > -(TMath::Pi()) && GenDeltaPhijj <= -(TMath::Pi())/2)',
         'GenDeltaPhijj_1fid' : '(isFID == 1 && GenDeltaPhijj > -(TMath::Pi())/2 && GenDeltaPhijj <= 0)',
         'GenDeltaPhijj_2fid' : '(isFID == 1 && GenDeltaPhijj > 0 && GenDeltaPhijj <= (TMath::Pi())/2)',
         'GenDeltaPhijj_3fid' : '(isFID == 1 && GenDeltaPhijj > (TMath::Pi())/2 && GenDeltaPhijj <= (TMath::Pi()))',
         'GenDeltaPhijj_0nonfid' : '(isFID <= 0 && GenDeltaPhijj > -(TMath::Pi()) && GenDeltaPhijj <= -(TMath::Pi())/2)',
         'GenDeltaPhijj_1nonfid' : '(isFID <= 0 && GenDeltaPhijj > -(TMath::Pi())/2 && GenDeltaPhijj <= 0)',
         'GenDeltaPhijj_2nonfid' : '(isFID <= 0 && GenDeltaPhijj > 0 && GenDeltaPhijj <= (TMath::Pi())/2)',
         'GenDeltaPhijj_3nonfid' : '(isFID <= 0 && GenDeltaPhijj > (TMath::Pi())/2 && GenDeltaPhijj <= (TMath::Pi()))',
         'noGenDeltaPhijj' : '(isFID <= 0 && GenDeltaPhijj==-9999)'
     }
} 


samples['VBF_H0L1'] = { 
   'name':   nanoGetSampleFiles(mcDirectory, 'VBF_H0L1_ToWWTo2L2Nu'), 
   'weight': mcCommonWeight+ '*VBF_H0L1_W',   
   'FilesPerJob': 4, 
   'subsamples' : {
         'GenDeltaPhijj_0fid' : '(isFID == 1 && GenDeltaPhijj > -(TMath::Pi()) && GenDeltaPhijj <= -(TMath::Pi())/2)',
         'GenDeltaPhijj_1fid' : '(isFID == 1 && GenDeltaPhijj > -(TMath::Pi())/2 && GenDeltaPhijj <= 0)',
         'GenDeltaPhijj_2fid' : '(isFID == 1 && GenDeltaPhijj > 0 && GenDeltaPhijj <= (TMath::Pi())/2)',
         'GenDeltaPhijj_3fid' : '(isFID == 1 && GenDeltaPhijj > (TMath::Pi())/2 && GenDeltaPhijj <= (TMath::Pi()))',
         'GenDeltaPhijj_0nonfid' : '(isFID <= 0 && GenDeltaPhijj > -(TMath::Pi()) && GenDeltaPhijj <= -(TMath::Pi())/2)',
         'GenDeltaPhijj_1nonfid' : '(isFID <= 0 && GenDeltaPhijj > -(TMath::Pi())/2 && GenDeltaPhijj <= 0)',
         'GenDeltaPhijj_2nonfid' : '(isFID <= 0 && GenDeltaPhijj > 0 && GenDeltaPhijj <= (TMath::Pi())/2)',
         'GenDeltaPhijj_3nonfid' : '(isFID <= 0 && GenDeltaPhijj > (TMath::Pi())/2 && GenDeltaPhijj <= (TMath::Pi()))',
         'noGenDeltaPhijj' : '(isFID <= 0 && GenDeltaPhijj==-9999)'
     }
} 

samples['VBF_H0L1f05'] = { 
   'name':   nanoGetSampleFiles(mcDirectory, 'VBF_H0L1f05_ToWWTo2L2Nu'), 
   'weight': mcCommonWeight+ '*VBF_H0L1f05_W',  
  'FilesPerJob': 4, 
  'subsamples' : {
         'GenDeltaPhijj_0fid' : '(isFID == 1 && GenDeltaPhijj > -(TMath::Pi()) && GenDeltaPhijj <= -(TMath::Pi())/2)',
         'GenDeltaPhijj_1fid' : '(isFID == 1 && GenDeltaPhijj > -(TMath::Pi())/2 && GenDeltaPhijj <= 0)',
         'GenDeltaPhijj_2fid' : '(isFID == 1 && GenDeltaPhijj > 0 && GenDeltaPhijj <= (TMath::Pi())/2)',
         'GenDeltaPhijj_3fid' : '(isFID == 1 && GenDeltaPhijj > (TMath::Pi())/2 && GenDeltaPhijj <= (TMath::Pi()))',
         'GenDeltaPhijj_0nonfid' : '(isFID <= 0 && GenDeltaPhijj > -(TMath::Pi()) && GenDeltaPhijj <= -(TMath::Pi())/2)',
         'GenDeltaPhijj_1nonfid' : '(isFID <= 0 && GenDeltaPhijj > -(TMath::Pi())/2 && GenDeltaPhijj <= 0)',
         'GenDeltaPhijj_2nonfid' : '(isFID <= 0 && GenDeltaPhijj > 0 && GenDeltaPhijj <= (TMath::Pi())/2)',
         'GenDeltaPhijj_3nonfid' : '(isFID <= 0 && GenDeltaPhijj > (TMath::Pi())/2 && GenDeltaPhijj <= (TMath::Pi()))',
         'noGenDeltaPhijj' : '(isFID <= 0 && GenDeltaPhijj==-9999)'
     }
} 

samples['VBF_H0L1Zgf05'] = { 
   'name':   nanoGetSampleFiles(mcDirectory, 'VBF_H0L1Zgf05_ToWWTo2L2Nu'), 
   'weight': mcCommonWeight+ '*VBF_H0LZgf05_W',  
  'FilesPerJob': 4, 
  'subsamples' : {
         'GenDeltaPhijj_0fid' : '(isFID == 1 && GenDeltaPhijj > -(TMath::Pi()) && GenDeltaPhijj <= -(TMath::Pi())/2)',
         'GenDeltaPhijj_1fid' : '(isFID == 1 && GenDeltaPhijj > -(TMath::Pi())/2 && GenDeltaPhijj <= 0)',
         'GenDeltaPhijj_2fid' : '(isFID == 1 && GenDeltaPhijj > 0 && GenDeltaPhijj <= (TMath::Pi())/2)',
         'GenDeltaPhijj_3fid' : '(isFID == 1 && GenDeltaPhijj > (TMath::Pi())/2 && GenDeltaPhijj <= (TMath::Pi()))',
         'GenDeltaPhijj_0nonfid' : '(isFID <= 0 && GenDeltaPhijj > -(TMath::Pi()) && GenDeltaPhijj <= -(TMath::Pi())/2)',
         'GenDeltaPhijj_1nonfid' : '(isFID <= 0 && GenDeltaPhijj > -(TMath::Pi())/2 && GenDeltaPhijj <= 0)',
         'GenDeltaPhijj_2nonfid' : '(isFID <= 0 && GenDeltaPhijj > 0 && GenDeltaPhijj <= (TMath::Pi())/2)',
         'GenDeltaPhijj_3nonfid' : '(isFID <= 0 && GenDeltaPhijj > (TMath::Pi())/2 && GenDeltaPhijj <= (TMath::Pi()))',
         'noGenDeltaPhijj' : '(isFID <= 0 && GenDeltaPhijj==-9999)' 
     }
} 

samples['GGHjj_H0M'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'GGHjj_H0M_ToWWTo2L2Nu'),
    'weight': mcCommonWeight + '*GGHjj_H0M_W',
    'FilesPerJob': 8,
    'subsamples' : {
         'GenDeltaPhijj_0fid' : '(isFID == 1 && GenDeltaPhijj > -(TMath::Pi()) && GenDeltaPhijj <= -(TMath::Pi())/2)',
         'GenDeltaPhijj_1fid' : '(isFID == 1 && GenDeltaPhijj > -(TMath::Pi())/2 && GenDeltaPhijj <= 0)',
         'GenDeltaPhijj_2fid' : '(isFID == 1 && GenDeltaPhijj > 0 && GenDeltaPhijj <= (TMath::Pi())/2)',
         'GenDeltaPhijj_3fid' : '(isFID == 1 && GenDeltaPhijj > (TMath::Pi())/2 && GenDeltaPhijj <= (TMath::Pi()))',
         'GenDeltaPhijj_0nonfid' : '(isFID <= 0 && GenDeltaPhijj > -(TMath::Pi()) && GenDeltaPhijj <= -(TMath::Pi())/2)',
         'GenDeltaPhijj_1nonfid' : '(isFID <= 0 && GenDeltaPhijj > -(TMath::Pi())/2 && GenDeltaPhijj <= 0)',
         'GenDeltaPhijj_2nonfid' : '(isFID <= 0 && GenDeltaPhijj > 0 && GenDeltaPhijj <= (TMath::Pi())/2)',
         'GenDeltaPhijj_3nonfid' : '(isFID <= 0 && GenDeltaPhijj > (TMath::Pi())/2 && GenDeltaPhijj <= (TMath::Pi()))',
         'noGenDeltaPhijj' : '(isFID <= 0 && GenDeltaPhijj==-9999)'
     }
}


samples['GGHjj_H0Mf05'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'GGHjj_H0Mf05_ToWWTo2L2Nu'),
    'weight': mcCommonWeight + '*GGHjj_H0Mf05_W',
    'FilesPerJob': 8,
    'subsamples' : {
         'GenDeltaPhijj_0fid' : '(isFID == 1 && GenDeltaPhijj > -(TMath::Pi()) && GenDeltaPhijj <= -(TMath::Pi())/2)',
         'GenDeltaPhijj_1fid' : '(isFID == 1 && GenDeltaPhijj > -(TMath::Pi())/2 && GenDeltaPhijj <= 0)',
         'GenDeltaPhijj_2fid' : '(isFID == 1 && GenDeltaPhijj > 0 && GenDeltaPhijj <= (TMath::Pi())/2)',
         'GenDeltaPhijj_3fid' : '(isFID == 1 && GenDeltaPhijj > (TMath::Pi())/2 && GenDeltaPhijj <= (TMath::Pi()))',
         'GenDeltaPhijj_0nonfid' : '(isFID <= 0 && GenDeltaPhijj > -(TMath::Pi()) && GenDeltaPhijj <= -(TMath::Pi())/2)',
         'GenDeltaPhijj_1nonfid' : '(isFID <= 0 && GenDeltaPhijj > -(TMath::Pi())/2 && GenDeltaPhijj <= 0)',
         'GenDeltaPhijj_2nonfid' : '(isFID <= 0 && GenDeltaPhijj > 0 && GenDeltaPhijj <= (TMath::Pi())/2)',
         'GenDeltaPhijj_3nonfid' : '(isFID <= 0 && GenDeltaPhijj > (TMath::Pi())/2 && GenDeltaPhijj <= (TMath::Pi()))',
         'noGenDeltaPhijj' : '(isFID <= 0 && GenDeltaPhijj==-9999)'
     }
}


############ ZH H->WW ############

samples['ZH_hww'] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'HZJ_HToWW_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 3,
}


samples['ggZH_hww'] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'GluGluZH_HToWWTo2L2Nu_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 3,
}


############ WH H->WW ############

samples['WH_hww'] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'HWplusJ_HToWW_M125') + nanoGetSampleFiles(mcDirectory, 'HWminusJ_HToWW_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 3,
}


############ ttH ############

samples['ttH_hww'] = {
    'name':   nanoGetSampleFiles(mcDirectory, 'ttHToNonbb_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 3,
}


############ H->TauTau ############

samples['ggH_htt'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'GluGluHToTauTau_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 3,
}


samples['qqH_htt'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'VBFHToTauTau_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 3,
}


samples['ZH_htt'] = {
    'name': nanoGetSampleFiles(mcDirectory, 'ZHToTauTau_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 1,
}


samples['WH_htt'] = {
    'name':  nanoGetSampleFiles(mcDirectory, 'WplusHToTauTau_M125') + nanoGetSampleFiles(mcDirectory, 'WminusHToTauTau_M125'),
    'weight': mcCommonWeight,
    'FilesPerJob': 1,
}



###########################################
################## FAKE ###################
###########################################

samples['Fake'] = {
  'name': [],
  'weight': 'METFilter_DATA*fakeW',
  'weights': [],
  'isData': ['all'],
  'FilesPerJob': 50
}

for _, sd in DataRun:
  for pd in DataSets:
    datatag = pd + '_' + sd

    if (   ('DoubleMuon' in pd and 'Run2018B' in sd)
        or ('DoubleMuon' in pd and 'Run2018D' in sd)
        or ('SingleMuon' in pd and 'Run2018A' in sd)
        or ('SingleMuon' in pd and 'Run2018B' in sd)
        or ('SingleMuon' in pd and 'Run2018C' in sd)):
        print("sd      = {}".format(sd))
        print("pd      = {}".format(pd))
        print("Old datatag = {}".format(datatag))
        datatag = datatag.replace('v1','v2')
        print("New datatag = {}".format(datatag))

    files = nanoGetSampleFiles(fakeDirectory, datatag)

    samples['Fake']['name'].extend(files)
    addSampleWeight(samples, 'Fake', datatag, DataTrig[pd])
    #samples['Fake']['weights'].extend([DataTrig[pd]] * len(files))

samples['Fake']['subsamples'] = {
  'e': 'abs(Lepton_pdgId[1]) == 11',
  'm': 'abs(Lepton_pdgId[1]) == 13'
}



###########################################
################## DATA ###################
###########################################

samples['DATA'] = {
  'name': [],
  'weight': 'LepWPCut*METFilter_DATA',
  'weights': [],
  'isData': ['all'],
  'FilesPerJob': 50
}

for _, sd in DataRun:
  for pd in DataSets:
    datatag = pd + '_' + sd

    if (   ('DoubleMuon' in pd and 'Run2018B' in sd)
        or ('DoubleMuon' in pd and 'Run2018D' in sd)
        or ('SingleMuon' in pd and 'Run2018A' in sd)
        or ('SingleMuon' in pd and 'Run2018B' in sd)
        or ('SingleMuon' in pd and 'Run2018C' in sd)):
        print("sd      = {}".format(sd))
        print("pd      = {}".format(pd))
        print("Old datatag = {}".format(datatag))
        datatag = datatag.replace('v1','v2')
        print("New datatag = {}".format(datatag))

    files = nanoGetSampleFiles(dataDirectory, datatag)

    samples['DATA']['name'].extend(files)
    addSampleWeight(samples, 'DATA', datatag, DataTrig[pd])
    #samples['DATA']['weights'].extend([DataTrig[pd]] * len(files))

