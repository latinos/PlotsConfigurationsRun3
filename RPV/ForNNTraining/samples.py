import os, glob
mcProduction = 'Summer20UL18_106x_nAODv9_Full2018v9'
dataReco = 'Run2018_UL2018_nAODv9_Full2018v9'
mcSteps = 'MCl1loose2018v9__MCCorr2018v9NoJERInHorn__l2tightOR2018v9'
mcStepsSig = 'MCl1loose2018v9__MCCorr2018v9NoJERInHornFS__l2tightOR2018v9{var}'
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
mcSigDirectory = makeMCDirectory().replace('Horn','HornFS')
fakeDirectory = os.path.join(treeBaseDir, dataReco, fakeSteps)
dataDirectory = os.path.join(treeBaseDir, dataReco, dataSteps)

samples = {}

from mkShapesRDF.lib.SearchFiles import SearchFiles
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



mcCommonWeight = 'XSWeight*METFilter_MC*PromptGenLepMatch2l*SFweight'

files = nanoGetSampleFiles(mcSigDirectory, 'RPV_113_udToSbottomToChi0ToSlep_massScan')

samples['RPV'] = {
          'name': files,
          'weight': mcCommonWeight,
          'subsamples' : {},
          'FilesPerJob': 10,
}


sb_masses = [300,700]
chi_mass_step = 50
mpoints = []

for sb_mass in sb_masses:
  start_chi_mass = 200 if sb_mass==300 else 400
  for chi_mass in [200 + i*50 for i in range(int((sb_mass-start_chi_mass)/chi_mass_step))]:
    for slep_mass in [chi_mass - 10 - i*20 for i in range(4)]:

      samples['RPV']['subsamples']['sb'+str(sb_mass)+'_chi'+str(chi_mass)+'_sl'+str(slep_mass)] = '(GenModel_RPV_udTo_sb'+str(sb_mass)+'_chi'+str(chi_mass)+'_sl'+str(slep_mass)+'==1)'

for slep_mass in [380,400,420,440]:
    samples['RPV_sb700_chi450_sl'+str(slep_mass)] = {
              'name': files,
              'weight': mcCommonWeight+'*(GenModel_RPV_udTo_sb700_chi450_sl'+str(slep_mass)+'==1)',
              'FilesPerJob': 10,
          }



files = nanoGetSampleFiles(mcSigDirectory, 'RPV_113_udToSbottomToChi0ToSlep_massScan_more')

samples['RPV_more'] = {
          'name': files,
          'weight': mcCommonWeight,
          'subsamples' : {},
          'FilesPerJob': 10,
}

sb_masses = [500,1000]
chi_mass_step = 100
mpoints = []

for sb_mass in sb_masses:
  start_chi_mass = 0
  for chi_mass in [sb_mass - 10 - i*chi_mass_step for i in range(int((sb_mass-start_chi_mass)/chi_mass_step))]:
    for slep_mass in [chi_mass - 10 - i*100 for i in range(100) if (chi_mass -10 -i*100)>0]:
      samples['RPV_more']['subsamples']['sb'+str(sb_mass)+'_chi'+str(chi_mass)+'_sl'+str(slep_mass)] = '(GenModel_RPV_udTo_sb'+str(sb_mass)+'_chi'+str(chi_mass)+'_sl'+str(slep_mass)+'==1)'



files = nanoGetSampleFiles(mcDirectory, 'TTTo2L2Nu')

samples['top'] = {
    'name': files,
    'weight': mcCommonWeight,
    'FilesPerJob': 1,
}


