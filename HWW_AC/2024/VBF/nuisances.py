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
mc_other = [ skey for skey in samples if (skey not in exclude_data and not skey.startswith('VBF_H')) ]
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

################################ EXPERIMENTAL UNCERTAINTIES  #################################

nuisances['JER'] = {
    'name': 'CMS_res_j_2024',
    'skipCMS' : 1,
    'kind': 'suffix',
    'type': 'shape',
    'mapUp': 'jerup',
    'mapDown': 'jerdo',
    #'separator': '__',
    'samples': dict((skey, ['1', '1']) for skey in mc),
    'folderUp': makeMCDirectory('jerup_suffix'),
    'folderDown': makeMCDirectory('jerdo_suffix'),
    'AsLnN': '0'
}

jes_systs    = ["Absolute", "Absolute_2024", "FlavorQCD", "BBEC1", "EC2", "HF", "BBEC1_2024", "EC2_2024", "RelativeBal", "RelativeSample_2024", "HF_2024"] # Reduced set of 11 uncertainties
#jes_systs = ['jesTotal']

for js in jes_systs:
    
    nuisances[js] = {
        'name'      : 'CMS_scale_j_' + js,
        'skipCMS' : 1,
        'kind'      : 'suffix',
        'type'      : 'shape',
        'mapUp'     : 'jesRegroed_' + js + 'up',
        'mapDown'   : 'jesRegroed_' + js + 'do',
        'samples'   : dict((skey, ['1', '1']) for skey in mc),
        'folderUp'  : makeMCDirectory('jesRegroed_' + js + 'up_suffix'),
        'folderDown': makeMCDirectory('jesRegroed_' + js + 'do_suffix'),
        'AsLnN'     : '0'
    }

nuisances['MET'] = {
    'name': 'CMS_scale_met_2024',
    'skipCMS' : 1,
    'kind': 'suffix',
    'type': 'shape',
    'mapUp': 'unclustEnup',
    'mapDown': 'unclustEndo',
    #'separator': '__',
    'samples': dict((skey, ['1', '1']) for skey in mc),
    'folderUp': makeMCDirectory('unclustEnup_suffix'),
    'folderDown': makeMCDirectory('unclustEndo_suffix'),
    'AsLnN': '0'
}

##### Lepton scale
nuisances['lepscale'] = {
    'name': 'CMS_lepscale_2024',
    'skipCMS' : 1,
    'kind': 'suffix',
    'type': 'shape',
    'mapUp': 'leptonScaleup',
    'mapDown': 'leptonScaledo',
    #'separator': '__',
    'samples': dict((skey, ['1', '1']) for skey in mc),
    'folderUp': makeMCDirectory('leptonScaleup_suffix'),
    'folderDown': makeMCDirectory('leptonScaledo_suffix'),
    'AsLnN': '0'
}
##### Lepton resolution
nuisances['lepres'] = {
    'name': 'CMS_lepres_2024',
    'skipCMS' : 1,
    'kind': 'suffix',
    'type': 'shape',
    'mapUp': 'leptonResolutionup',
    'mapDown': 'leptonResolutiondo',
    #'separator': '__',
    'samples': dict((skey, ['1', '1']) for skey in mc),
    'folderUp': makeMCDirectory('leptonResolutionup_suffix'),
    'folderDown': makeMCDirectory('leptonResolutiondo_suffix'),
    'AsLnN': '0'
}

## B-tagger
#Fixed BTV SF variations
for flavour in ['bc', 'light']:
    for corr in ['uncorrelated', 'correlated']:
        btag_syst = [f'btagSF{flavour}_up_{corr}/btagSF{flavour}', f'btagSF{flavour}_down_{corr}/btagSF{flavour}']
        if corr == 'correlated':
            name = f'CMS_btagSF{flavour}_{corr}'
        else:
            name = f'CMS_btagSF{flavour}_2024'
        nuisances[f'btagSF{flavour}{corr}'] = {
            'name': name,
            'skipCMS' : 1,
            'kind': 'weight',
            'type': 'shape',
            'samples': dict((skey, btag_syst) for skey in mc),
        }


##### Trigger Scale Factors                                                                                                                                                                                

trig_syst = ['TriggerSFWeight_2l_u/TriggerSFWeight_2l', 'TriggerSFWeight_2l_d/TriggerSFWeight_2l']

nuisances['trigg'] = {
    'name': 'CMS_eff_hwwtrigger_2024',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, trig_syst) for skey in mc)
}

##### Electron Efficiency and energy scale

nuisances['eff_e'] = {
    'name': 'CMS_eff_e_2024',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, ['SFweightEleUp', 'SFweightEleDown']) for skey in mc),
}

##### Muon Efficiency and energy scale

nuisances['eff_m'] = {
    'name': 'CMS_eff_m_2024',
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, ['SFweightMuUp', 'SFweightMuDown']) for skey in mc),
}


nuisances['PU'] = {
    'name': 'CMS_pileup_2024',
    'skipCMS'    : 1,
    'kind': 'weight',
    'type': 'shape',
    'samples': dict((skey, ['puWeightUp/puWeight', 'puWeightDown/puWeight']) for skey in mc),
    'AsLnN'   : '0'
}     

##### PS 

HPS = ['qqH_htt','ggH_hww','qqH_hww'] + eft_ewksys  # qqH_Htt crashing here 

nuisances['PS_ISR']  = {
    'name'    : 'ps_isr',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['PSWeight[2]', 'PSWeight[0]']) for skey in mc if skey not in HPS),
    'AsLnN'   : '0',
}
nuisances['PS_FSR']  = {
    'name'    : 'ps_fsr',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : dict((skey, ['PSWeight[3]', 'PSWeight[1]']) for skey in mc if skey not in HPS),
    'AsLnN'   : '0',
}

HISR =     {'ggH_hww' : ['PSWeight[2]*NormTHU_ggH_hww_ps_isr_Up', 'PSWeight[0]*NormTHU_ggH_hww_ps_isr_Down'],
            'qqH_hww' : ['PSWeight[2]*NormTHU_qqH_hww_ps_isr_Up', 'PSWeight[0]*NormTHU_qqH_hww_ps_isr_Down']}
HISR.update(dict((skey, ['1', '1']) for skey in eft_ewksys))

nuisances['PS_ISR_higgs']  = {
    'name'    : 'ps_isr',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : HISR,
    'AsLnN'   : '0',
}

HFSR =     {'ggH_hww' : ['PSWeight[3]*NormTHU_ggH_hww_ps_fsr_Up', 'PSWeight[1]*NormTHU_ggH_hww_ps_fsr_Down'],
            'qqH_hww' : ['PSWeight[3]*NormTHU_qqH_hww_ps_fsr_Up', 'PSWeight[1]*NormTHU_qqH_hww_ps_fsr_Down']}
HFSR.update(dict((skey, ['1', '1']) for skey in eft_ewksys))

nuisances['PS_FSR_higgs']  = {
    'name'    : 'ps_fsr',
    'kind'    : 'weight',
    'type'    : 'shape',
    'samples' : HFSR,
    'AsLnN'   : '0',
}

nuisances['UE_CP5']  = {
    'name'    : 'UEPS',
    'type'    : 'lnN',
    'samples' : dict((skey, '1.015') for skey in mc),
}


##### pdf uncertainties
pdf_variations = ["LHEPdfWeight[%d]" %i for i in range(1,103)] # Float_t LHE pdf variation weights (w_var / w_nominal) for LHA IDs  320901 - 321000
nuisances['pdf_WW']  = {
    'name'  : 'CMS_pdf_WW',
    'skipCMS' : 1,
    'kind'  : 'weight_rms',
    'type'  : 'shape',
    'AsLnN': '0',
    'samples'  : {
        'WW'   : pdf_variations,
    },
}

nuisances['pdf_top']  = {
    'name'  : 'CMS_pdf_top',
    'skipCMS' : 1,
    'kind'  : 'weight_rms',
    'type'  : 'shape',
    'AsLnN': '0',
    'samples'  : {
        'Top'   : pdf_variations,
    },
}

valuesggh = HiggsXS.GetHiggsProdXSNP('ggH','125.38','pdf','sm')
valuesggzh = HiggsXS.GetHiggsProdXSNP('ggH','125.38','pdf','sm') #DM ggZH not present?  

nuisances['pdf_Higgs_ggH']  = {
    'name'  : 'CMS_pdf_Higgs_gg',
    'skipCMS' : 1,
    'type'  : 'lnN',
    'samples'  : {
        'ggH_hww' : valuesggh,
        'ggH_htt' : valuesggh,
        'ggZH_hww' : valuesggzh
    },
}

values = HiggsXS.GetHiggsProdXSNP('ttH','125.38','pdf','sm')

nuisances['pdf_Higgs_ttH']  = {
    'name'  : 'CMS_pdf_Higgs_ttH',
    'skipCMS' : 1,
    'type'  : 'lnN',
    'samples'  : {
        'ttH_hww' : valuesggh,
    },
}

valuesqqh = HiggsXS.GetHiggsProdXSNP('vbfH','125.38','pdf','sm')
valueswh = HiggsXS.GetHiggsProdXSNP('WH','125.38','pdf','sm')
valueszh = HiggsXS.GetHiggsProdXSNP('ZH','125.38','pdf','sm')

qqPDF = {'qqH_hww' : valuesqqh,
        'qqH_htt' : valuesqqh,
        'WH_hww' : valueswh,
        'ZH_hww' : valueszh}
qqPDF.update(dict((skey, valuesqqh) for skey in eft_ewksys))

nuisances['pdf_Higgs_qqbar']  = {
    'name'  : 'CMS_pdf_Higgs_qqbar',
    'skipCMS' : 1,
    'type'  : 'lnN',
    'samples'  : qqPDF,
}

nuisances['pdf_qqbar'] = {
    'name': 'pdf_qqbar',
    'type': 'lnN',
    'samples': {
        'VZ': '1.04',
        'Vg': '1.04',
        'VgS': '1.04', # PDF: 0.0064 / 0.1427 = 0.0448493
    },
}


## This should work for samples with either 8 or 9 LHE scale weights (Length$(LHEScaleWeight) == 8 or 9)
variations = ['Alt(LHEScaleWeight,0,1)',
              'Alt(LHEScaleWeight,1,1)',
              'Alt(LHEScaleWeight,3,1)',
              'Alt(LHEScaleWeight,nLHEScaleWeight-4,1)',
              'Alt(LHEScaleWeight,nLHEScaleWeight-2,1)',
              'Alt(LHEScaleWeight,nLHEScaleWeight-1,1)']

nuisances['QCDscale_top']  = {
    'name'  : 'QCDscale_ttbar',
    'kind'  : 'weight_envelope',
    'type'  : 'shape',
    'samples'  : {'top' : variations}
}

nuisances['QCDscale_DY'] = {
    'name': 'QCDscale_DY',
    'kind'  : 'weight_envelope',
    'type': 'shape',
    'samples': {'DY': variations}
}

nuisances['QCDscale_VV'] = {
    'name' : 'QCDscale_VV',
    'kind' : 'weight_envelope',
    'type' : 'shape',
    'samples' : {'WW'  : variations}
}

nuisances['QCDscale_ggWW'] = {
    'name': 'QCDscale_ggWW',
    'type': 'lnN',
    'samples': {'ggWW': '1.15'},
}

variations_ggH = ['Alt(LHEScaleWeight,0,1)*NormTHU_ggH_hww_QCDscale_ggH_SPECIAL_NUIS_envelope0',
              'Alt(LHEScaleWeight,1,1)*NormTHU_ggH_hww_QCDscale_ggH_SPECIAL_NUIS_envelope1',
              'Alt(LHEScaleWeight,3,1)*NormTHU_ggH_hww_QCDscale_ggH_SPECIAL_NUIS_envelope2',
              'Alt(LHEScaleWeight,nLHEScaleWeight-4,1)*NormTHU_ggH_hww_QCDscale_ggH_SPECIAL_NUIS_envelope3',
              'Alt(LHEScaleWeight,nLHEScaleWeight-2,1)*NormTHU_ggH_hww_QCDscale_ggH_SPECIAL_NUIS_envelope4',
              'Alt(LHEScaleWeight,nLHEScaleWeight-1,1)*NormTHU_ggH_hww_QCDscale_ggH_SPECIAL_NUIS_envelope5']

nuisances['QCDscale_ggH_shape'] = {
    'name' : 'QCDscale_ggH_shape',
    'kind' : 'weight_envelope',
    'type' : 'shape',
    'samples' : {'ggH_hww'  : variations_ggH}
}

values = HiggsXS.GetHiggsProdXSNP('ggH','125.38','scale','sm')

nuisances['QCDscale_ggH_norm'] = {
    'name': 'QCDscale_ggH_norm', 
    'samples': {
        'ggH_hww': values,
        'ggH_htt': values
    },
    'type': 'lnN'
}

variations_qqH = ['Alt(LHEScaleWeight,0,1)*NormTHU_qqH_hww_QCDscale_qqH_SPECIAL_NUIS_envelope0',
              'Alt(LHEScaleWeight,1,1)*NormTHU_qqH_hww_QCDscale_qqH_SPECIAL_NUIS_envelope1',
              'Alt(LHEScaleWeight,3,1)*NormTHU_qqH_hww_QCDscale_qqH_SPECIAL_NUIS_envelope2',
              'Alt(LHEScaleWeight,nLHEScaleWeight-4,1)*NormTHU_qqH_hww_QCDscale_qqH_SPECIAL_NUIS_envelope3',
              'Alt(LHEScaleWeight,nLHEScaleWeight-2,1)*NormTHU_qqH_hww_QCDscale_qqH_SPECIAL_NUIS_envelope4',
              'Alt(LHEScaleWeight,nLHEScaleWeight-1,1)*NormTHU_qqH_hww_QCDscale_qqH_SPECIAL_NUIS_envelope5']

qqQCD = {'qqH_hww' : variations_qqH }
qqQCD.update(dict((skey, ['1','1','1','1','1','1']) for skey in eft_ewksys))

nuisances['QCDscale_qqH_shape'] = {
    'name' : 'QCDscale_qqH_shape',
    'kind' : 'weight_envelope',
    'type' : 'shape',
    'samples' : qqQCD
}

values = HiggsXS.GetHiggsProdXSNP('vbfH','125.38','scale','sm')

qqQCDn = {'qqH_hww' : values }
qqQCDn.update(dict((skey, values) for skey in eft_ewksys))

nuisances['QCDscale_qqH_norm'] = {
    'name': 'QCDscale_qqH_norm', 
    'samples': qqQCDn,
    'type': 'lnN'
}

valueswh = HiggsXS.GetHiggsProdXSNP('WH','125.38','scale','sm')
valueszh = HiggsXS.GetHiggsProdXSNP('ZH','125.38','scale','sm')

nuisances['QCDscale_VH'] = {
    'name': 'QCDscale_VH', 
    'samples': {
        'WH_hww': valueswh,
        'ZH_hww': valueszh,
    },
    'type': 'lnN',
}

values = HiggsXS.GetHiggsProdXSNP('ggH','125.38','scale','sm') #DM ggZH does not contain this?   

nuisances['QCDscale_ggZH'] = {
    'name': 'QCDscale_ggZH', 
    'samples': {
        'ggZH_hww': values
    },
    'type': 'lnN',
}

values = HiggsXS.GetHiggsProdXSNP('ttH','125.38','scale','sm')

nuisances['QCDscale_ttH'] = {
    'name': 'QCDscale_ttH',
    'samples': {
        'ttH_hww': values
    },
    'type': 'lnN',
}

thus = [
    # ('THU_ggH_Mu', 'ggH_mu'), # QCD uncertainty split into 4 independent sources: ggH_Mu: normalization, ggH_res: resummation, ggH_Mig01: 0-1 jet category migration, ggH_Mig12 1-2 jet category migration
    ('THU_ggH_Res', 'ggH_res'),
    # ('THU_ggH_Mig01', 'ggH_mig01'),
    # ('THU_ggH_Mig12', 'ggH_mig12'),
    # ('THU_ggH_VBF2j', 'ggH_VBF2j'), # VBF topology
    # ('THU_ggH_VBF3j', 'ggH_VBF3j'), # VBF topology
    # ('THU_ggH_PT60', 'ggH_pT60'), # Migration uncertainty around the 60 GeV boundary
    # ('THU_ggH_PT120', 'ggH_pT120'), # Migration uncertainty around the 120 GeV boundary
    ('THU_ggH_qmtop', 'ggH_qmtop') # Difference between finite top mass dependence @NLO vs @LO evaluated using Powheg NNLOPS taken as uncertainty on the treatment of top mass in ggF loop
]

for name, vname in thus:

    updown = [f'{vname}', f'(2. - {vname})']

    nuisances[name] = {
        'name': name,
        'skipCMS': 1,
        'kind': 'weight',
        'type': 'shape',
        'samples': dict((skey, updown) for skey in ['ggH_hww']),
    }


#  uncertainty sources
#  10 QCD-nuisances:  1 x yields uncertainty on the inclusive xsec, 9 x migration uncertainties (1 x 3rd jet veto, 6 x Mjj cuts, 1 x PTH cut, 1 x 01->2 jetBin)

thusQQH = [
#   ("THU_qqH_YIELD","qqH_YIELD"),
#   ("THU_qqH_PTH200","qqH_PTH200"),
#   ("THU_qqH_Mjj60","qqH_Mjj60"),
#   ("THU_qqH_Mjj120","qqH_Mjj120"),
#   ("THU_qqH_Mjj350","qqH_Mjj350"),
#   ("THU_qqH_Mjj700","qqH_Mjj700"),
#   ("THU_qqH_Mjj1000","qqH_Mjj1000"),
#   ("THU_qqH_Mjj1500","qqH_Mjj1500"),
#   ("THU_qqH_PTH25","qqH_PTH25"),
#   ("THU_qqH_JET01","qqH_JET01"),
  ("THU_qqH_EWK","qqH_EWK"), # Electroweak corrections
]

for name, vname in thusQQH:

    updown = [f'{vname}', f'(2. - {vname})']
    
    qqHDict = { 'qqH_hww': updown }
    qqHDict.update(dict((skey, ['1', '1']) for skey in eft_ewksys))

    nuisances[name] = {
        'name': name,
        'skipCMS': 1,
        'kind': 'weight',
        'type': 'shape',
        'samples': qqHDict,
        }

##### FAKES

nuisances['fake_syst'] = {
    'name': 'CMS_fake_syst',
    'skipCMS': 1,
    'type': 'lnN',
    'samples': {
        'Fake': '1.3'
    },
}

nuisances['fake_ele'] = {
    'name': 'CMS_fake_e_2024',
    'skipCMS': 1,
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake': ['fakeWEleUp', 'fakeWEleDown'],
    }
}

nuisances['fake_ele_stat'] = {
    'name': 'CMS_fake_stat_e_2024',
    'skipCMS': 1,
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake': ['fakeWStatEleUp', 'fakeWStatEleDown']
    }
}

nuisances['fake_mu'] = {
    'name': 'CMS_fake_m_2024',
    'skipCMS': 1,
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake': ['fakeWMuUp', 'fakeWMuDown'],
    }
}

nuisances['fake_mu_stat'] = {
    'name': 'CMS_fake_stat_m_2024',
    'skipCMS': 1,
    'kind': 'weight',
    'type': 'shape',
    'samples': {
        'Fake': ['fakeWStatMuUp', 'fakeWStatMuDown'],
    }
}

nuisances['lumi_2024'] = {
    'name'    : 'lumi_2024',
    'type'    : 'lnN',
    'samples' : dict((skey, '1.016') for skey in mc)
}

##rate parameters

nuisances['DYnorm']  = {
    'name'  : 'CMS_hww_DYnorm2j_2024',
    'skipCMS': 1,
    'type'  : 'rateParam',
    'samples'  : {'DY' : '1.00' },
}

nuisances['WWnorm']  = {
    'name'  : 'CMS_hww_WWnorm2j_2024',
    'skipCMS': 1,
    'type'  : 'rateParam',
    'samples'  : {'WW' : '1.00' },
}

nuisances['ggWWnorm']  = {
    'name'  : 'CMS_hww_ggWWnorm2j_2024',
    'skipCMS': 1,
    'type'  : 'rateParam',
    'samples'  : {'ggWW' : '1.00' },
}

nuisances['topnorm']  = {
    'name'  : 'CMS_hww_topnorm2j_2024',
    'skipCMS': 1,
    'type'  : 'rateParam',
    'samples'  : {'top' : '1.00' },
}

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
