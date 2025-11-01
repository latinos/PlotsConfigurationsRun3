import sys
 
# Enable reading YR for Higgs XS and uncertainties
sys.path.append('../../../macros/')
import HiggsXSection
HiggsXS = HiggsXSection.HiggsXSection()

nuisances = {}

mcProduction = 'Summer20UL16_106x_nAODv9_noHIPM_Full2016v9'
dataReco     = 'Run2016_UL2016_nAODv9_noHIPM_Full2016v9'
mcSteps      = 'MCl1loose2016v9__MCCorr2016v9NoJERInHorn__l2tightOR2016v9'
fakeSteps    = 'DATAl1loose2016v9__l2loose__fakeW'
dataSteps    = 'DATAl1loose2016v9__l2loose__l2tightOR2016v9'

treeBaseDir  = '/eos/cms/store/group/phys_higgs/cmshww/amassiro/HWWNano'
limitFiles   = -1

mc = [skey for skey in samples if skey not in ('Fake', 'DATA')]

redirector = ""

useXROOTD = False

def makeMCDirectory(var=''):
    if var== '':
        print(os.path.join(treeBaseDir, mcProduction, mcSteps))
        return os.path.join(treeBaseDir, mcProduction, mcSteps)
    else:
        print(os.path.join(treeBaseDir, mcProduction, mcSteps + '__' + var))
        return os.path.join(treeBaseDir, mcProduction, mcSteps + '__' + var)

mcDirectory = makeMCDirectory()
fakeDirectory = os.path.join(treeBaseDir, dataReco, fakeSteps)
dataDirectory = os.path.join(treeBaseDir, dataReco, dataSteps)

################################ EXPERIMENTAL UNCERTAINTIES  #################################

#### Luminosity

# https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun2#LumiComb
# Uncorrelated 2016               1.0
# Uncorrelated       2017              2.0
# Uncorrelated             2018             1.5
# Correlated   2016, 2017, 2018   0.6, 0.9, 2.0
# Correlated         2017, 2018        0.6, 0.2

nuisances['lumi_Uncorrelated'] = {
    'name'    : 'lumi_13TeV_2016',
    'type'    : 'lnN',
    'samples' : dict((skey, '1.010') for skey in mc if skey not in ['WZ'])
}

nuisances['lumi_Correlated_Run2'] = {
    'name'    : 'lumi_13TeV_correlated',
    'type'    : 'lnN',
    'samples' : dict((skey, '1.006') for skey in mc if skey not in ['WZ'])
}


#### FAKES
nuisances['fake_ele'] = {
    'name'    : 'CMS_WH_hww_fake_e_2016',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : {
        'Fake_ee' : ['fakeWEleUp', 'fakeWEleDown'],
        'Fake_em' : ['fakeWEleUp', 'fakeWEleDown'],
    }
}
nuisances['fake_ele_stat'] = {
    'name'    : 'CMS_WH_hww_fake_stat_e_2016',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : {
        'Fake_ee' : ['fakeWStatEleUp', 'fakeWStatEleDown'],
        'Fake_em' : ['fakeWStatEleUp', 'fakeWStatEleDown'],
    }
}
nuisances['fake_mu'] = {
    'name'    : 'CMS_WH_hww_fake_m_2016',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : {
        'Fake_mm' : ['fakeWMuUp', 'fakeWMuDown'],
        'Fake_em' : ['fakeWMuUp', 'fakeWMuDown'],
    }   
}       
nuisances['fake_mu_stat'] = {
    'name'    : 'CMS_WH_hww_fake_stat_m_2016',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : {
        'Fake_mm' : ['fakeWStatMuUp', 'fakeWStatMuDown'],
        'Fake_em' : ['fakeWStatMuUp', 'fakeWStatMuDown'],
    }
}

###### B-tagger

for shift in ['lf', 'hf', 'hfstats1', 'hfstats2', 'lfstats1', 'lfstats2', 'cferr1', 'cferr2']:
    btag_syst = ['(btagSF%sup)/(btagSF)' % shift, '(btagSF%sdown)/(btagSF)' % shift]

    name = 'CMS_btag_%s' % shift
    if 'stats' in shift:
        name += '_2016'

    nuisances['btag_shape_%s' % shift] = {
        'name'    : name,
        'kind'    : 'weight',
        'type'    : 'shape',
        'samples' : dict((skey, btag_syst) for skey in mc),
    }

##### Trigger Scale Factors

trig_syst = ['TriggerSFWeight_2l_u/TriggerSFWeight_2l', 'TriggerSFWeight_2l_d/TriggerSFWeight_2l']

nuisances['trigg'] = {
    'name'    : 'CMS_eff_hwwtrigger_2016',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, trig_syst) for skey in mc)
}

##### Electron Efficiency and energy scale

nuisances['eff_e'] = {
    'name'    : 'CMS_eff_e_2016',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['SFweightEleUp', 'SFweightEleDown']) for skey in mc)
}

nuisances['eff_ttHMVA_e'] = {
    'name'    : 'CMS_eff_ttHMVA_e_2016',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['LepWPttHMVASFEleUp', 'LepWPttHMVASFEleDown']) for skey in mc)
}

nuisances['electronpt'] = {
    'name'       : 'CMS_scale_e_2016',
    'kind'       : 'suffix',
    'type'       : 'shape',
    'mapUp'      : 'ElepTup',
    'mapDown'    : 'ElepTdo',
    'samples'    : dict((skey, ['1', '1']) for skey in mc),
    'folderUp'   : makeMCDirectory('ElepTup_suffix'),
    'folderDown' : makeMCDirectory('ElepTdo_suffix'),
    'AsLnN'      : '0'
}

##### Muon Efficiency and energy scale

nuisances['eff_m'] = {
    'name'    : 'CMS_eff_m_2016',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['SFweightMuUp', 'SFweightMuDown']) for skey in mc)
}

nuisances['eff_ttHMVA_m'] = {
    'name'    : 'CMS_eff_ttHMVA_m_2016',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['LepWPttHMVASFMuUp', 'LepWPttHMVASFMuDown']) for skey in mc)
}

nuisances['muonpt'] = {
    'name'       : 'CMS_scale_m_2016',
    'kind'       : 'suffix',
    'type'       : 'shape',
    'mapUp'      : 'MupTup',
    'mapDown'    : 'MupTdo',
    'samples'    : dict((skey, ['1', '1']) for skey in mc),
    'folderUp'   : makeMCDirectory('MupTup_suffix'),
    'folderDown' : makeMCDirectory('MupTdo_suffix'),
    'AsLnN'      : '0'
}

##### Jet energy scale
jes_systs    = ['JESAbsolute','JESAbsolute_2016','JESBBEC1','JESBBEC1_2016','JESEC2','JESEC2_2016','JESFlavorQCD','JESHF','JESHF_2016','JESRelativeBal','JESRelativeSample_2016']

for js in jes_systs:

  nuisances[js] = {
      'name'      : 'CMS_scale_' + js.replace("JES","j_"),
      'kind'      : 'suffix',
      'type'      : 'shape',
      'mapUp'     : js + 'up',
      'mapDown'   : js + 'do',
      'samples'   : dict((skey, ['1', '1']) for skey in mc),
      'folderUp'  : makeMCDirectory('RDF__JESup_suffix'),
      'folderDown': makeMCDirectory('RDF__JESdo_suffix'),
      'reweight'  : ['btagSF'+js.replace('JES','jes')+'up/btagSF','btagSF'+js.replace('JES','jes')+'down/btagSF'],
      'AsLnN'     : '0'
  }

##### Jet energy resolution
nuisances['JER'] = {
    'name'      : 'CMS_res_j_2016',
    'kind'      : 'suffix',
    'type'      : 'shape',
    'mapUp'     : 'JERup',
    'mapDown'   : 'JERdo',
    'samples'   : dict((skey, ['1', '1']) for skey in mc),
    'folderUp'  : makeMCDirectory('JERup_suffix'),
    'folderDown': makeMCDirectory('JERdo_suffix'),
    'AsLnN'     : '0'
}

##### MET unclustered energy

nuisances['met'] = {
    'name'      : 'CMS_scale_met_2016',
    'kind'      : 'suffix',
    'type'      : 'shape',
    'mapUp'     : 'METup',
    'mapDown'   : 'METdo',
    'samples'   : dict((skey, ['1', '1']) for skey in mc),
    'folderUp'  : makeMCDirectory('METup_suffix'),
    'folderDown': makeMCDirectory('METdo_suffix'),
    'AsLnN'     : '0'
}


##### Pileup

# puWeight_UL2016
nuisances['PU'] = {
    'name'    : 'CMS_pileup_2016',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : {
        'DY'      : ['1.000489*(puWeightUp/puWeight)', '0.998828*(puWeightDown/puWeight)'],
        'WW'      : ['1.007152*(puWeightUp/puWeight)', '0.993194*(puWeightDown/puWeight)'],
        'ggWW'    : ['1.006460*(puWeightUp/puWeight)', '0.993661*(puWeightDown/puWeight)'],
        'Vg'      : ['1.004694*(puWeightUp/puWeight)', '0.998294*(puWeightDown/puWeight)'],
        'WZ'      : ['1.003158*(puWeightUp/puWeight)', '0.997747*(puWeightDown/puWeight)'],
        'ZZ'      : ['1.000801*(puWeightUp/puWeight)', '0.999199*(puWeightDown/puWeight)'],
        'VVV'     : ['0.996144*(puWeightUp/puWeight)', '1.005616*(puWeightDown/puWeight)'],
        'top'     : ['1.004374*(puWeightUp/puWeight)', '0.995684*(puWeightDown/puWeight)'],
        'Higgs'   : ['1.006460*(puWeightUp/puWeight)', '0.993559*(puWeightDown/puWeight)'],
    },
    'AsLnN'   : '0',
}

### PU ID SF uncertainty

puid_syst = ['Jet_PUIDSF_up/Jet_PUIDSF', 'Jet_PUIDSF_down/Jet_PUIDSF']

nuisances['jetPUID'] = {
    'name'    : 'CMS_eff_j_PUJET_id_2016',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, puid_syst) for skey in mc)
}

### PS and UE

nuisances['PS_ISR']  = {
    'name'    : 'PS_WH_hww_ISR',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['PSWeight[2]', 'PSWeight[0]']) for skey in mc),
    'AsLnN'   : '0',
}

nuisances['PS_FSR']  = {
    'name'    : 'PS_WH_hww_FSR',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['PSWeight[3]', 'PSWeight[1]']) for skey in mc),
    'AsLnN'   : '0',
}

nuisances['UE_CP5']  = {
    'name'    : 'CMS_WH_hww_UE',
    'skipCMS' : 1,
    'type'    : 'lnN',
    'samples' : dict((skey, '1.015') for skey in mc),
}

# Charge flip efficiency
nuisances['chargeFlipEff'] = {
    'name'    : 'CMS_whss_chargeFlipEff_2016',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['1-ttHMVA_eff_err_flip_2l', '1+ttHMVA_eff_err_flip_2l']) for skey in ['DY','DATA']),
    'cuts'    : [cut for cut in cuts if ('_ee_' in cut or '_em_' in cut)]
}

nuisances['WgStar'] = {
    'name'    : 'CMS_hww_WgStarScale',
    'type'    : 'lnN',
    'samples' : {
        'WgS' : '1.25'
    }
}

# Use the following if you want to apply the automatic combine MC stat nuisances.
nuisances['stat']  = {
    'type'          : 'auto',
    'maxPoiss'      : '10',
    'includeSignal' : '0',
    'samples'       : {}
}
# nuisance ['maxPoiss']      = Number of threshold events for Poisson modelling
# nuisance ['includeSignal'] = Include MC stat nuisances on signal processes (1=True, 0=False)

for n in nuisances.values():
    n['skipCMS'] = 1
