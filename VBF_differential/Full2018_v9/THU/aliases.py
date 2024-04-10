import os
import copy
import inspect


configurations = os.path.realpath(inspect.getfile(inspect.currentframe())) # this file


aliases = {}
aliases = OrderedDict()

mc     = [skey for skey in samples if skey not in ('Fake', 'DATA', 'Dyemb')]
mc_emb = [skey for skey in samples if skey not in ('Fake', 'DATA')]

print('\n\n\n')
print('Configs:\n\n\n')
# configurations = os.path.abspath('.') + '/'
configurations = os.path.realpath(inspect.getfile(inspect.currentframe())) # this file
configurations = os.path.dirname(configurations) # Full2018_v9_2output
configurations = os.path.dirname(configurations)
configurations = os.path.dirname(configurations) + '/' # VBF_differential 

print(configurations)
print('\n\n\n')


aliases['isFID'] = {
  'linesToAdd': ['#include "%s/extended/isFid.cc"' % configurations],
  'class': 'isFiducial',
  'args': 'nGenDressedLepton, GenDressedLepton_pdgId, GenDressedLepton_pt, GenDressedLepton_eta, GenDressedLepton_phi, GenDressedLepton_mass, GenDressedLepton_hasTauAnc, nGenJet, GenJet_pt, GenJet_eta, GenJet_phi, GenJet_mass, GenMET_pt, GenMET_phi',
  'samples': mc
}

aliases['GenDeltaPhijj'] = {
  'linesToAdd': ['#include "%s/extended/GetGenJetDeltaPhi.cc"' % configurations],
  'class': 'GenJetDeltaPhi',
  'args': 'nGenDressedLepton, GenDressedLepton_pdgId, GenDressedLepton_pt, GenDressedLepton_eta, GenDressedLepton_phi, GenDressedLepton_mass, GenDressedLepton_hasTauAnc, nGenJet, GenJet_pt, GenJet_eta, GenJet_phi, GenJet_mass',
  'samples': mc
}

diffcuts_ggh = samples['ggH_hww']['subsamples'] if 'ggH_hww' in samples else {}
diffcuts_qqh = samples['qqH_hww']['subsamples'] if 'qqH_hww' in samples else {}

import json
normfactors = json.load(open("HiggsTHUNormFactors.json"))

ggh_thus = ['THU_ggH_Mu','THU_ggH_Res','THU_ggH_Mig01','THU_ggH_Mig12',
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


qqh_thus = ["THU_qqH_YIELD","THU_qqH_PTH200","THU_qqH_Mjj60","THU_qqH_Mjj120",
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
