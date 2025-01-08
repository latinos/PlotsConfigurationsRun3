import os
import copy
import inspect


print('\n\n\n')
print('Configs:\n\n\n')
configurations = os.path.realpath(inspect.getfile(inspect.currentframe())) # this file
configurations = os.path.dirname(configurations) 
configurations = os.path.dirname(configurations) + '/' # VBF_differential 
print(configurations)
print('\n\n\n')

aliases = {}
aliases = OrderedDict()

mc     = [skey for skey in samples if skey not in ('Fake', 'DATA', 'Dyemb') and 'H0' not in skey]
mc_emb = [skey for skey in samples if skey not in ('Fake', 'DATA') and 'H0' not in skey]
mc_all     = [skey for skey in samples if skey not in ('Fake', 'DATA', 'Dyemb')]
ggH_sig = ['ggH_hww_GenDeltaPhijj_0fid','ggH_hww_GenDeltaPhijj_1fid','ggH_hww_GenDeltaPhijj_2fid','ggH_hww_GenDeltaPhijj_3fid', 'ggH_hww_GenDeltaPhijj_0nonfid','ggH_hww_GenDeltaPhijj_1nonfid','ggH_hww_GenDeltaPhijj_2nonfid','ggH_hww_GenDeltaPhijj_3nonfid']
qqH_sig = ['qqH_hww_GenDeltaPhijj_0fid','qqH_hww_GenDeltaPhijj_1fid','qqH_hww_GenDeltaPhijj_2fid','qqH_hww_GenDeltaPhijj_3fid', 'qqH_hww_GenDeltaPhijj_0nonfid','qqH_hww_GenDeltaPhijj_1nonfid','qqH_hww_GenDeltaPhijj_2nonfid','qqH_hww_GenDeltaPhijj_3nonfid']


# LepCut2l__ele_mvaFall17V2Iso_WP90_tthmva_70__mu_cut_Tight80x_tthmva_80
eleWP = 'mvaFall17V2Iso_WP90' # _tthmva_70'
muWP  = 'cut_Tight80x_tthmva_80' # _tthmva_80'


aliases['LepWPCut'] = {
    'expr': 'LepCut2l__ele_'+eleWP+'__mu_'+muWP,
    'samples': mc_all + ['DATA']
}

aliases['LepWPSF'] = {
    'expr': 'LepSF2l__ele_'+eleWP+'__mu_'+muWP,
    'samples': mc_all
}


aliases['gstarLow'] = {
    'expr': 'Gen_ZGstar_mass > 0 && Gen_ZGstar_mass < 4',
    'samples': 'VgS'
}

aliases['gstarHigh'] = {
    'expr': 'Gen_ZGstar_mass < 0 || Gen_ZGstar_mass > 4',
    'samples': 'VgS'
}

# aliases['embedtotal'] = {
#     'expr': 'embed_total_mva16',  # wrt. eleWP
#     'samples': 'Dyemb'
# }


# # Fake leptons transfer factor
aliases['fakeW'] = {
    'expr': 'fakeW2l_ele_'+eleWP+'_mu_'+muWP,
    'samples': ['Fake']
}

# And variations - already divided by central values in formulas !
aliases['fakeWEleUp'] = {
    'expr': 'fakeW2l_ele_'+eleWP+'_mu_'+muWP+'_EleUp',
    'samples': ['Fake']
}
aliases['fakeWEleDown'] = {
    'expr': 'fakeW2l_ele_'+eleWP+'_mu_'+muWP+'_EleDown',
    'samples': ['Fake']
}
aliases['fakeWMuUp'] = {
    'expr': 'fakeW2l_ele_'+eleWP+'_mu_'+muWP+'_MuUp',
    'samples': ['Fake']
}
aliases['fakeWMuDown'] = {
    'expr': 'fakeW2l_ele_'+eleWP+'_mu_'+muWP+'_MuDown',
    'samples': ['Fake']
}
aliases['fakeWStatEleUp'] = {
    'expr': 'fakeW2l_ele_'+eleWP+'_mu_'+muWP+'_statEleUp',
    'samples': ['Fake']
}
aliases['fakeWStatEleDown'] = {
    'expr': 'fakeW2l_ele_'+eleWP+'_mu_'+muWP+'_statEleDown',
    'samples': ['Fake']
}
aliases['fakeWStatMuUp'] = {
    'expr': 'fakeW2l_ele_'+eleWP+'_mu_'+muWP+'_statMuUp',
    'samples': ['Fake']
}
aliases['fakeWStatMuDown'] = {
    'expr': 'fakeW2l_ele_'+eleWP+'_mu_'+muWP+'_statMuDown',
    'samples': ['Fake']
}

# gen-matching to prompt only (GenLepMatch2l matches to *any* gen lepton)
aliases['PromptGenLepMatch2l'] = {
            'expr': 'Alt(Lepton_promptgenmatched, 0, 0) * Alt(Lepton_promptgenmatched, 1, 0)',
            'samples': mc_all
            }

aliases['Top_pTrw'] = {
    'expr': '(topGenPt * antitopGenPt > 0.) * (TMath::Sqrt(TMath::Exp(0.0615 - 0.0005 * topGenPt) * TMath::Exp(0.0615 - 0.0005 * antitopGenPt))) + (topGenPt * antitopGenPt <= 0.)',
    'samples': ['top']
}



# Jet bins
# using Alt$(CleanJet_pt[n], 0) instead of Sum$(CleanJet_pt >= 30) because jet pt ordering is not strictly followed in JES-varied samples

# No jet with pt > 30 GeV
aliases['zeroJet'] = {
    'expr': 'Alt(CleanJet_pt, 0, 0) < 30.'
}

aliases['oneJet'] = {
    'expr': 'Alt(CleanJet_pt, 0, 0) > 30.'
}

aliases['multiJet'] = {
    'expr': 'Alt(CleanJet_pt, 1, 0) > 30.'
}

####################################################################################
# b tagging WPs: https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation106XUL17
####################################################################################

# DeepB = DeepCSV
# DeepFlavB = DeepJet

aliases['bVeto'] = {
    'expr': 'Sum(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5 && Take(Jet_btagDeepFlavB, CleanJet_jetIdx) > 0.0480) == 0'
}
aliases['bReq'] = { 
    'expr': 'Sum(CleanJet_pt > 30. && abs(CleanJet_eta) < 2.5 && Take(Jet_btagDeepFlavB, CleanJet_jetIdx) > 0.0480) >= 1'
}

# CR definition

aliases['topcr'] = {
    'expr': 'mtw2>30 && mll>50 && ((zeroJet && !bVeto) || bReq)'
}

aliases['dycr'] = {
    'expr': 'mth<60 && mll>40 && mll<80 && bVeto'
}


# Fixed BTV SF

btv_path =  '/afs/cern.ch/work/b/bcamaian/mkShapesRDF_el9/mkShapesRDF/processor/data/jsonpog-integration/POG/BTV/2016postVFP_UL'

for flavour in ['bc', 'light']:
    for shift in ['central', 'up_uncorrelated', 'down_uncorrelated', 'up_correlated', 'down_correlated']:
        btagsf = 'btagSF' + flavour
        if shift != 'central':
            btagsf += '_' + shift
        aliases[btagsf] = {
            'linesToAdd': [f'#include "{configurations}/macros/evaluate_btagSF{flavour}_2016noHIPM.cc"'],
            'linesToProcess': [f"ROOT.gInterpreter.Declare('btagSF{flavour} btagSF{flavour}_{shift} = btagSF{flavour}(\"{btv_path}/bTagEff_2016noHIPM_ttbar_DeepFlavB_loose.root\");')"],
            'expr': f'btagSF{flavour}_{shift}(CleanJet_pt, CleanJet_eta, CleanJet_jetIdx, nCleanJet, Jet_hadronFlavour, Jet_btagDeepFlavB, "L", "{shift}")',
            'samples' : mc_all,
        }




aliases['Jet_PUIDSF'] = { 
          'expr' : 'TMath::Exp(Sum((Jet_jetId>=2)*LogVec(Jet_PUIDSF_loose)))',
          'samples': mc_all
          }
aliases['Jet_PUIDSF_up'] = {
  'expr' : 'TMath::Exp(Sum((Jet_jetId>=2)*LogVec(Jet_PUIDSF_loose_up)))',
  'samples': mc
}
aliases['Jet_PUIDSF_down'] = {
  'expr' : 'TMath::Exp(Sum((Jet_jetId>=2)*LogVec(Jet_PUIDSF_loose_down)))',
  'samples': mc
}




# data/MC scale factors
aliases['SFweight'] = {
    'expr': ' * '.join(['SFweight2l', 'LepWPCut', 'LepWPSF','Jet_PUIDSF', 'PrefireWeight', 'btagSFbc', 'btagSFlight']),
    'samples': mc_all
}

# variations
aliases['SFweightEleUp'] = {
    'expr': 'LepSF2l__ele_'+eleWP+'__Up',
    'samples': mc_emb
}
aliases['SFweightEleDown'] = {
    'expr': 'LepSF2l__ele_'+eleWP+'__Do',
    'samples': mc_emb
}
aliases['SFweightMuUp'] = {
    'expr': 'LepSF2l__mu_'+muWP+'__Up',
    'samples': mc_emb
}
aliases['SFweightMuDown'] = {
    'expr': 'LepSF2l__mu_'+muWP+'__Do',
    'samples': mc_emb
}

# Fix METFilter_DATA definition: Flag_ecalBadCalibFilter is removed since it is not needed in 2016
aliases['METFilter_DATA_fix'] = {
    'expr' : 'Flag_goodVertices*Flag_globalSuperTightHalo2016Filter*Flag_HBHENoiseFilter*Flag_HBHENoiseIsoFilter*Flag_EcalDeadCellTriggerPrimitiveFilter*Flag_BadPFMuonFilter*Flag_BadPFMuonDzFilter*Flag_eeBadScFilter',
    'samples': ['DATA','Fake']
}




# my macro


aliases['m_lj'] = {
  'linesToAdd': ['#include "%s/macros/m_lj.cc"' % configurations],
  'class': 'm_lj',
  'args': 'CleanJet_pt, CleanJet_eta, CleanJet_phi, CleanJet_jetIdx, Jet_mass, Lepton_pt, Lepton_eta, Lepton_phi',
  'afterNuis': True,
}


# D_VBF_GGH D_VBF_VH D_GGH_VH
aliases['memela'] = {
  'linesToProcess':['ROOT.gSystem.Load("/afs/cern.ch/work/b/bcamaian/mkShapesRDF/JHUGenMELA/MELA/data/slc7_amd64_gcc920/libmcfm_707.so","",ROOT.kTRUE)',
                    'ROOT.gSystem.Load("/afs/cern.ch/work/b/bcamaian/mkShapesRDF/JHUGenMELA/MELA/data/slc7_amd64_gcc920/libJHUGenMELAMELA.so","", ROOT.kTRUE)',
 			        'ROOT.gSystem.Load("/afs/cern.ch/work/b/bcamaian/mkShapesRDF_el9/VBF_differential/macros/ME_class_cc.so","", ROOT.kTRUE)',
			        'ROOT.gInterpreter.Declare("MEMELA a;")'],
   'expr' :   'a(nCleanJet, nLepton, PuppiMET_pt, PuppiMET_phi, Lepton_pt, Lepton_phi, Lepton_eta, CleanJet_pt, CleanJet_phi, CleanJet_eta, Lepton_pdgId)',
   'afterNuis': True,

}

# D_VBF_DY
aliases['MoMEMta_D'] = {
  'linesToProcess':['ROOT.gSystem.Load("/afs/cern.ch/work/b/bcamaian/mkShapesRDF/momemta/lib/libmomemta.so.1.0.1","",ROOT.kTRUE)',
                    'ROOT.gSystem.Load("/afs/cern.ch/work/b/bcamaian/mkShapesRDF/momemta/lib/libmomemta.so.1","", ROOT.kTRUE)',
                    'ROOT.gSystem.Load("/afs/cern.ch/work/b/bcamaian/mkShapesRDF_el9/VBF_differential/macros/MoMEMta_D_cc.so","", ROOT.kTRUE)'],
#   'linesToAdd': ['#include "%s/macros/MoMEMta_D.cc"' % configurations],
  'class': 'MoMEMta_discriminant',
  'args': 'nCleanJet, nLepton, PuppiMET_pt, PuppiMET_phi, Lepton_pt[0], Lepton_pt[1], Lepton_phi[0], Lepton_phi[1], Lepton_eta[0], Lepton_eta[1], CleanJet_pt[0], CleanJet_pt[1], CleanJet_phi[0], CleanJet_phi[1], CleanJet_eta[0], CleanJet_eta[1], Lepton_pdgId[0], Lepton_pdgId[1] ',
  'afterNuis': True,
}

#adnns[0] = isVBF  adnns[1]=isGGH
aliases['adnns'] = {
  'linesToAdd': ['#include "%s/macros/evaluate_adnns.cc"' % configurations ],
  'class': 'adversarial_dnn',
  'args': ' nLepton, nCleanJet, Lepton_pdgId[0], Lepton_pdgId[1], CleanJet_eta[0], CleanJet_eta[1], CleanJet_phi[0], CleanJet_phi[1], CleanJet_pt[0], CleanJet_pt[1], Lepton_eta[0], Lepton_eta[1], Lepton_phi[0], Lepton_phi[1], Lepton_pt[0], Lepton_pt[1], Jet_qgl[CleanJet_jetIdx[0]], Jet_qgl[CleanJet_jetIdx[1]],  mjj, mll, ptll, detajj, dphill, PuppiMET_pt, PuppiMET_phi, dphillmet, drll, ht, mTi, mth, m_lj[0], m_lj[1], m_lj[2], m_lj[3], memela[0], memela[1], memela[2], MoMEMta_D[0], 2016, event',
  'afterNuis': True,
}



bin_adnnisVBF = ['0.0', '0.04', '0.08', '0.12', '0.16', '0.2', '0.24', '0.28', '0.32', '0.36', '0.4', '0.44', '0.48', '0.52', '0.56', '0.6', '0.64', '0.68', '0.72', '0.76', '0.8', '0.84', '0.88', '0.92', '0.96', '1.0']
bin_adnnisGGH = ['0.0', '0.50', '0.80', '0.9', '1.0']
adnn2D = ''
for i in range(len(bin_adnnisGGH)-1):
  for j in range(len(bin_adnnisVBF)-1):
    if i+j != len(bin_adnnisVBF)+len(bin_adnnisGGH)-4: 
      adnn2D+='('+bin_adnnisGGH[i]+'<adnns[1])*(adnns[1]<'+bin_adnnisGGH[i+1]+')*(('+str((len(bin_adnnisVBF)-1)*i)+')+('+str(j+1)+'))*('+bin_adnnisVBF[j]+'<adnns[0])*(adnns[0]<'+bin_adnnisVBF[j+1]+')+'
    else: 
      adnn2D+='('+bin_adnnisGGH[i]+'<adnns[1])*(adnns[1]<'+bin_adnnisGGH[i+1]+')*(('+str((len(bin_adnnisVBF)-1)*i)+')+('+str(j+1)+'))*('+bin_adnnisVBF[j]+'<adnns[0])*(adnns[0]<'+bin_adnnisVBF[j+1]+')'
 

aliases['adnns_2D'] = {
    'expr' : adnn2D,
    'afterNuis': True,

    }

    #dnn[0] = isVBF, dnn[1] = isGGH  
aliases['dnns'] = {
  'linesToAdd': ['#include "%s/macros/evaluate_dnn.cc"' % configurations  ],
  'class': 'evaluate_dnn',
  'args': ' nLepton, nCleanJet, Lepton_pdgId[0], Lepton_pdgId[1], CleanJet_eta[0], CleanJet_eta[1], CleanJet_phi[0], CleanJet_phi[1], CleanJet_pt[0], CleanJet_pt[1], Lepton_eta[0], Lepton_eta[1], Lepton_phi[0], Lepton_phi[1], Lepton_pt[0], Lepton_pt[1], Jet_qgl[CleanJet_jetIdx[0]], Jet_qgl[CleanJet_jetIdx[1]],  mjj, mll, ptll, detajj, dphill, PuppiMET_pt, PuppiMET_phi, dphillmet, drll, ht, mTi, mth,  m_lj[0], m_lj[1], m_lj[2], m_lj[3]',
 'afterNuis': True,
}

bin_dnnisVBF = ['0.0', '0.04', '0.08', '0.12', '0.16', '0.2', '0.24', '0.28', '0.32', '0.36', '0.4', '0.44', '0.48', '0.52', '0.56', '0.6', '0.64', '0.68', '0.72', '0.76', '0.8', '0.84', '0.88', '0.92', '0.96', '1.0']
bin_dnnisGGH = ['0.0', '0.50', '0.80', '0.9', '1.0']
dnn2D = ''

for i in range(len(bin_dnnisGGH)-1):
  for j in range(len(bin_dnnisVBF)-1):
    if i+j != len(bin_dnnisVBF)+len(bin_dnnisGGH)-4: 
      dnn2D+='('+bin_dnnisGGH[i]+'<dnns[1])*(dnns[1]<'+bin_dnnisGGH[i+1]+')*(('+str((len(bin_dnnisVBF)-1)*i)+')+('+str(j+1)+'))*('+bin_dnnisVBF[j]+'<dnns[0])*(dnns[0]<'+bin_dnnisVBF[j+1]+')+'
    else: 
      dnn2D+='('+bin_dnnisGGH[i]+'<dnns[1])*(dnns[1]<'+bin_dnnisGGH[i+1]+')*(('+str((len(bin_dnnisVBF)-1)*i)+')+('+str(j+1)+'))*('+bin_dnnisVBF[j]+'<dnns[0])*(dnns[0]<'+bin_dnnisVBF[j+1]+')'
 

aliases['dnns_2D'] = {
    'expr' : dnn2D,
    'afterNuis': True,

    }




aliases['DeltaPhijj'] = {
  'linesToAdd': ['#include "%s/macros/GetJetDeltaPhi.cc"' % configurations],
  'class': 'JetDeltaPhi',
  'args': 'nCleanJet, CleanJet_eta, CleanJet_phi',
  'afterNuis': True,
}

aliases['isFID'] = {
  'linesToAdd': ['#include "%s/macros/isFid.cc"' % configurations],
  'class': 'isFiducial',
  'args': 'nGenDressedLepton, GenDressedLepton_pdgId, GenDressedLepton_pt, GenDressedLepton_eta, GenDressedLepton_phi, GenDressedLepton_mass, GenDressedLepton_hasTauAnc, nGenJet, GenJet_pt, GenJet_eta, GenJet_phi, GenJet_mass, GenMET_pt, GenMET_phi',
  'samples': mc_all
}

aliases['GenDeltaPhijj'] = {
  'linesToAdd': ['#include "%s/macros/GetGenJetDeltaPhi.cc"' % configurations],
  'class': 'GenJetDeltaPhi',
  'args': 'nGenDressedLepton, GenDressedLepton_pdgId, GenDressedLepton_pt, GenDressedLepton_eta, GenDressedLepton_phi, GenDressedLepton_mass, GenDressedLepton_hasTauAnc, nGenJet, GenJet_pt, GenJet_eta, GenJet_phi, GenJet_mass',
  'samples': mc_all
}


# diffcuts_ggh = samples['ggH_hww']['subsamples'] if 'ggH_hww' in samples  else {}
diffcuts_ggh = {key: value for key, value in samples['ggH_hww']['subsamples'].items() if 'noGenDeltaPhijj' not in key} if 'ggH_hww' in samples else {}
# diffcuts_qqh = samples['qqH_hww']['subsamples'] if 'qqH_hww' in samples else {}
diffcuts_qqh = {key: value for key, value in samples['qqH_hww']['subsamples'].items() if 'noGenDeltaPhijj' not in key} if 'qqH_hww' in samples else {}

import json
normfactors = json.load(open("HiggsTHUNormFactors.json"))

ggh_thus = ['QCDscale_ren_ggH_hww', 'QCDscale_fac_ggH_hww', 'THU_ggH_Mu','THU_ggH_Res','THU_ggH_Mig01','THU_ggH_Mig12',
        'THU_ggH_VBF2j','THU_ggH_VBF3j','THU_ggH_PT60','THU_ggH_PT120','THU_ggH_qmtop',
        'PS_ISR', 'PS_FSR']

for name in ggh_thus:
    aliases['norm_ggh_'+name+'_up'] = {
        'expr' : '+'.join(['({})*({})'.format(diffcuts_ggh[binname],normfactors[name]["ggH_hww_"+binname][0]) for binname in diffcuts_ggh]),
        'samples' : ['ggH_hww'],
    }
    aliases['norm_ggh_'+name+'_down'] = {
        'expr' : '+'.join(['({})*({})'.format(diffcuts_ggh[binname],normfactors[name]["ggH_hww_"+binname][1]) for binname in diffcuts_ggh]),
        'samples' : ['ggH_hww'],
    }


qqh_thus = ["QCDscale_ren_qqH_hww", "QCDscale_fac_qqH_hww","THU_qqH_YIELD","THU_qqH_PTH200","THU_qqH_Mjj60","THU_qqH_Mjj120",
        "THU_qqH_Mjj350","THU_qqH_Mjj700","THU_qqH_Mjj1000","THU_qqH_Mjj1500",
        "THU_qqH_PTH25","THU_qqH_JET01","THU_qqH_EWK","PS_ISR","PS_FSR"]

for name in qqh_thus:
    aliases['norm_qqh_'+name+'_up'] = {
        'expr' : '+'.join(['({})*({})'.format(diffcuts_qqh[binname],normfactors[name]["qqH_hww_"+binname][0]) for binname in diffcuts_qqh]),
        'samples' : ['qqH_hww'],
    }
    aliases['norm_qqh_'+name+'_down'] = {
        'expr' : '+'.join(['({})*({})'.format(diffcuts_qqh[binname],normfactors[name]["qqH_hww_"+binname][1]) for binname in diffcuts_qqh]),
        'samples' : ['qqH_hww'],
    }


# Couplings used in JHUGen

aliases['G2_HWW']  = {'expr': '1.133582'}
aliases['G4_HWW']  = {'expr': '1.76132'}
aliases['L1_HWW']  = {'expr': '-13752.22'}

aliases['G2_VBF']  = {'expr': '0.27196538'}
aliases['G4_VBF']  = {'expr': '0.29797901870'}
aliases['L1_VBF']  = {'expr': '-2158.21307286'}

aliases['G4_GGHjj']= {'expr': '1.0062'}

# Cross-sections : Decay 

aliases['JHUXSHWWa1']   = {'expr': '312.04019'}
aliases['JHUXSHWWa2']   = {'expr': '242.6283'}
aliases['JHUXSHWWa3']   = {'expr': '100.79135'} 
aliases['JHUXSHWWL1']   = {'expr': '1.6475531e-06'}
aliases['JHUXSHWWa1a2'] = {'expr': '1149.9181'}
aliases['JHUXSHWWa1a3'] = {'expr': '624.7195'}
aliases['JHUXSHWWa1L1'] = {'expr': '5.3585509'}


# Cross-sections : Production

aliases['JHUXSVBFa1']   = {'expr': '968.88143'}
aliases['JHUXSVBFa2']   = {'expr': '13097.831'}
aliases['JHUXSVBFa3']   = {'expr': '10910.237'}
aliases['JHUXSVBFL1']   = {'expr': '0.00020829261'}
aliases['JHUXSVBFLZg']  = {'expr': '5.2902139e-05'}
aliases['JHUXSVBFa1a2'] = {'expr': '2207.6738'}
aliases['JHUXSVBFa1a3'] = {'expr': '1936.4327'}
aliases['JHUXSVBFa1L1'] = {'expr': '2861.7003'}
aliases['JHUXSVBFa1LZg'] = {'expr': '1574.5833'}

aliases['JHUXSGGHjja2']   = {'expr': '14583.61'}
aliases['JHUXSGGHjja3']   = {'expr': '14397.13'}
aliases['JHUXSGGHjja2a3'] = {'expr': '29169.2'}


# Normalisation Weights

aliases['H0PM_W']    = { 'expr': '1'}
aliases['H0M_W']     = { 'expr': '(JHUXSHWWa3/JHUXSHWWa1)'}
aliases['H0PH_W']    = { 'expr': '(JHUXSHWWa2/JHUXSHWWa1)'}
aliases['H0L1_W']    = { 'expr': '(JHUXSHWWL1/JHUXSHWWa1)'}
aliases['H0Mf05_W']  = { 'expr': '(JHUXSHWWa1a3/JHUXSHWWa1)'}
aliases['H0PHf05_W'] = { 'expr': '(JHUXSHWWa1a2/JHUXSHWWa1)'}
aliases['H0L1f05_W'] = { 'expr': '(JHUXSHWWa1L1/JHUXSHWWa1)'}

aliases['JHUXSHWWa1a2_I'] = {'expr':'(JHUXSHWWa1a2 - JHUXSHWWa1 - pow(G2_HWW,2)*JHUXSHWWa2)/G2_HWW'}
aliases['JHUXSHWWa1a3_I'] = {'expr':'(JHUXSHWWa1a3 - JHUXSHWWa1 - pow(G4_HWW,2)*JHUXSHWWa3)/G4_HWW'}
aliases['JHUXSHWWa1L1_I'] = {'expr':'(JHUXSHWWa1L1 - JHUXSHWWa1 - pow(L1_HWW,2)*JHUXSHWWL1)/L1_HWW'}

aliases['H0Mf05VBF_W']  = { 'expr': '(JHUXSHWWa1 + JHUXSHWWa1a3_I*G4_VBF + JHUXSHWWa3*pow(G4_VBF,2))/JHUXSHWWa1'}
aliases['H0PHf05VBF_W'] = { 'expr': '(JHUXSHWWa1 + JHUXSHWWa1a2_I*G2_VBF + JHUXSHWWa2*pow(G2_VBF,2))/JHUXSHWWa1'}
aliases['H0L1f05VBF_W'] = { 'expr': '(JHUXSHWWa1 + JHUXSHWWa1L1_I*L1_VBF + JHUXSHWWL1*pow(L1_VBF,2))/JHUXSHWWa1'}

aliases['VBF_H0PM_W']    = { 'expr': '1'}
aliases['VBF_H0M_W']     = { 'expr': 'H0M_W*(JHUXSVBFa3/JHUXSVBFa1)'}
aliases['VBF_H0PH_W']    = { 'expr': 'H0PH_W*(JHUXSVBFa2/JHUXSVBFa1)'}
aliases['VBF_H0L1_W']    = { 'expr': 'H0L1_W*(JHUXSVBFL1/JHUXSVBFa1)'}
aliases['VBF_H0LZg_W']   = { 'expr': '1*(JHUXSVBFLZg/JHUXSVBFa1)'}
aliases['VBF_H0Mf05_W']  = { 'expr': 'H0Mf05VBF_W*(JHUXSVBFa1a3/JHUXSVBFa1)'}
aliases['VBF_H0PHf05_W'] = { 'expr': 'H0PHf05VBF_W*(JHUXSVBFa1a2/JHUXSVBFa1)'}
aliases['VBF_H0L1f05_W'] = { 'expr': 'H0L1f05VBF_W*(JHUXSVBFa1L1/JHUXSVBFa1)'}
aliases['VBF_H0LZgf05_W']= { 'expr': '1*(JHUXSVBFa1LZg/JHUXSVBFa1)'}

aliases['GGHjj_H0M_W']     = { 'expr': '0.29*(JHUXSGGHjja3/JHUXSGGHjja2)'}
aliases['GGHjj_H0Mf05_W']  = { 'expr': '0.29*(JHUXSGGHjja2a3/JHUXSGGHjja2)'}
