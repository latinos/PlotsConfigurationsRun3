mcProduction = 'Summer24_150x_nAODv15_Full2024v15'
mcSteps      = 'MCl2loose2024v15__MCCorr2024v15__JERFrom23BPix__l2tight'
dataRecoMuon     = 'Run2024_ReRecoCDE_PromptFGHI_nAODv15_Full2024v15_Muon'
dataRecoEGamma     = 'Run2024_ReRecoCDE_PromptFGHI_nAODv15_Full2024v15_EGamma'
dataRecoMuonEG     = 'Run2024_ReRecoCDE_PromptFGHI_nAODv15_Full2024v15_MuonEG'
dataSteps    = 'DATAl2loose2024v15__l2loose'

treeBaseDir = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'
limitFiles = -1

#mc = [skey for skey in samples if skey not in ('Fake', 'DATA')]
exclude_data = {'Fake', 'DATA'}
mc_other = [ skey for skey in samples if (skey not in exclude_data and not skey.startswith('WH_H') and not skey.startswith('ZH_H'))]
mc = mc_other + eft_ewksys
print("MC for nuisances :", mc)

redirector = ""

useXROOTD = False

def makeMCDirectory(var=''):
    _treeBaseDir = treeBaseDir + ''
    if useXROOTD:
        _treeBaseDir = redirector + treeBaseDir
    if var== '':
        return '/'.join([_treeBaseDir, mcProduction, mcSteps])
    else:
        return '/'.join([_treeBaseDir, mcProduction, mcSteps + '__' + var])

mcDirectory = makeMCDirectory()
#fakeDirectory = os.path.join(treeBaseDir, dataReco, fakeSteps)
#dataDirectory = os.path.join(treeBaseDir, dataReco, dataSteps)
print(treeBaseDir)

nuisances = {}

configurations = os.path.realpath(inspect.getfile(inspect.currentframe()))
hxs_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(configurations)))) + '/utils/data/lhc-hxswg-YR5/'
sys.path.append(hxs_path)
cwd = os.getcwd()
os.chdir(hxs_path)
from HiggsXSection import HiggsXSection
HiggsXS = HiggsXSection()
os.chdir(cwd)

################################ 

autoStats = True
if autoStats:
    ## Use the following if you want to apply the automatic combine MC stat nuisances.
    nuisances['stat'] = {
        'type': 'auto',
        'maxPoiss': '10',
        'includeSignal': '0',
        #  nuisance ['maxPoiss'] =  Number of threshold events for Poisson modelling
        #  nuisance ['includeSignal'] =  Include MC stat nuisances on signal processes (1=True, 0=False)
        'samples': {}
    }
