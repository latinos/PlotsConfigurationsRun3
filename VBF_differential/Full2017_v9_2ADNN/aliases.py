import os
import copy
import inspect


configurations = os.path.realpath(inspect.getfile(inspect.currentframe())) # this file


aliases = {}
aliases = OrderedDict()

mc     = [skey for skey in samples if skey not in ('Fake', 'DATA', 'Dyemb')]
mc_emb = [skey for skey in samples if skey not in ('Fake', 'DATA')]

mc_bsm = ['VBF_H0M','VBF_H0PH', 'VBF_H0L1','VBF_H0Mf05','VBF_H0PHf05', 'VBF_H0L1Zgf05', 'ggH_hww']

# LepCut2l__ele_mvaFall17V2Iso_WP90__mu_cut_Tight_HWWW_tthmva_80
eleWP = 'mvaFall17V2Iso_WP90'
muWP  = 'cut_Tight_HWWW_tthmva_80'


aliases['LepWPCut'] = {
    'expr': 'LepCut2l__ele_'+eleWP+'__mu_'+muWP,
    'samples': mc_emb + ['DATA']
}

aliases['LepWPSF'] = {
    'expr': 'LepSF2l__ele_'+eleWP+'__mu_'+muWP,
    'samples': mc_emb
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
            'samples': mc
            }

aliases['Top_pTrw'] = {
    'expr': '(topGenPt * antitopGenPt > 0.) * (TMath::Sqrt(TMath::Exp(0.0615 - 0.0005 * topGenPt) * TMath::Exp(0.0615 - 0.0005 * antitopGenPt))) + (topGenPt * antitopGenPt <= 0.)',
    'samples': ['top']
}

# ##### DY Z pT reweighting
# aliases['nCleanGenJet'] = {
#     'linesToAdd': ['.L %s/src/PlotsConfigurations/Configurations/Differential/ngenjet.cc+' % os.getenv('CMSSW_BASE')],
#     'class': 'CountGenJet',
#     'samples': mc
# }

# aliases['getGenZpt_OTF'] = {
#     'linesToAdd':['.L %s/src/PlotsConfigurations/Configurations/patches/getGenZpt.cc+' % os.getenv('CMSSW_BASE')],
#     'class': 'getGenZpt',
#     'samples': ['DY']
# }
# handle = open('%s/src/PlotsConfigurations/Configurations/patches/DYrew30.py' % os.getenv('CMSSW_BASE'),'r')
# exec(handle)
# handle.close()
# aliases['DY_NLO_pTllrw'] = {
#     'expr': '('+DYrew['2016']['NLO'].replace('x', 'getGenZpt_OTF')+')*(nCleanGenJet == 0)+1.0*(nCleanGenJet > 0)',
#     'samples': ['DY']
# }
# aliases['DY_LO_pTllrw'] = {
#     'expr': '('+DYrew['2016']['LO'].replace('x', 'getGenZpt_OTF')+')*(nCleanGenJet == 0)+1.0*(nCleanGenJet > 0)',
#     'samples': ['DY']
# }


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
    'expr': 'Sum(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5 && Take(Jet_btagDeepFlavB, CleanJet_jetIdx) > 0.0532) == 0'
}
aliases['bReq'] = { 
    'expr': 'Sum(CleanJet_pt > 30. && abs(CleanJet_eta) < 2.5 && Take(Jet_btagDeepFlavB, CleanJet_jetIdx) > 0.0532) >= 1'
}

# CR definition

aliases['topcr'] = {
    'expr': 'mtw2>30 && mll>50 && ((zeroJet && !bVeto) || bReq)'
}

aliases['dycr'] = {
    'expr': 'mth<60 && mll>40 && mll<80 && bVeto'
}



# SF b tagging
aliases['bVetoSF'] = {
    'expr': 'TMath::Exp(Sum(LogVec((CleanJet_pt>20 && abs(CleanJet_eta)<2.5)*Take(Jet_btagSF_deepjet_shape, CleanJet_jetIdx)+1*(CleanJet_pt<20 || abs(CleanJet_eta)>2.5))))',
    'samples': mc
}

aliases['bReqSF'] = {
    'expr': 'TMath::Exp(Sum(LogVec((CleanJet_pt>30 && abs(CleanJet_eta)<2.5)*Take(Jet_btagSF_deepjet_shape, CleanJet_jetIdx)+1*(CleanJet_pt<30 || abs(CleanJet_eta)>2.5))))',
    'samples': mc
}

aliases['btagSF'] = {
    'expr': '(bVeto || (topcr && zeroJet))*bVetoSF + (topcr && !zeroJet)*bReqSF',
    'samples': mc
}

for shift in ['jes','lf','hf','lfstats1','lfstats2','hfstats1','hfstats2','cferr1','cferr2']:

    for targ in ['bVeto', 'bReq']:
        alias = aliases['%sSF%sup' % (targ, shift)] = copy.deepcopy(aliases['%sSF' % targ])
        alias['expr'] = alias['expr'].replace('btagSF_deepjet_shape', 'btagSF_deepjet_shape_up_%s' % shift)

        alias = aliases['%sSF%sdown' % (targ, shift)] = copy.deepcopy(aliases['%sSF' % targ])
        alias['expr'] = alias['expr'].replace('btagSF_deepjet_shape', 'btagSF_deepjet_shape_down_%s' % shift)

    aliases['btagSF%sup' % shift] = {
        'expr': aliases['btagSF']['expr'].replace('SF', 'SF' + shift + 'up'),
        'samples': mc
    }

    aliases['btagSF%sdown' % shift] = {
        'expr': aliases['btagSF']['expr'].replace('SF', 'SF' + shift + 'down'),
        'samples': mc
    }



aliases['Jet_PUIDSF'] = { 
          'expr' : 'TMath::Exp(Sum((Jet_jetId>=2)*LogVec(Jet_PUIDSF_loose)))',
          'samples': mc
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
    'expr': ' * '.join(['SFweight2l', 'LepWPCut', 'LepWPSF','Jet_PUIDSF', 'PrefireWeight','btagSF']),
    #'expr': ' * '.join(['SFweight2l', 'LepWPCut', 'LepWPSF']),
    'samples': mc
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



# my macro
print('\n\n\n')
print('Configs:\n\n\n')
# configurations = os.path.abspath('.') + '/'
configurations = os.path.realpath(inspect.getfile(inspect.currentframe())) # this file
configurations = os.path.dirname(configurations) # Full2017_v9
configurations = os.path.dirname(configurations) + '/' # VBF_differential 
print(configurations)
print('\n\n\n')

aliases['m_lj'] = {
  'linesToAdd': ['#include "%s/extended/m_lj.cc+"' % configurations],
  'class': 'm_lj',
  'args': 'CleanJet_pt, CleanJet_eta, CleanJet_phi, CleanJet_jetIdx, Jet_mass, Lepton_pt, Lepton_eta, Lepton_phi',
  #'samples': mc
}


# D_VBF_QCD D_VBF_VH D_QCD_VH
aliases['memela'] = {
  'linesToProcess':['ROOT.gSystem.Load("/afs/cern.ch/work/b/bcamaian/mkShapesRDF/JHUGenMELA/MELA/data/slc7_amd64_gcc920/libmcfm_707.so","",ROOT.kTRUE)',
                    'ROOT.gSystem.Load("/afs/cern.ch/work/b/bcamaian/mkShapesRDF/JHUGenMELA/MELA/data/slc7_amd64_gcc920/libJHUGenMELAMELA.so","", ROOT.kTRUE)',
 			        'ROOT.gSystem.Load("/afs/cern.ch/work/b/bcamaian/mkShapesRDF/VBF_differential/extended/ME_class_cc.so","", ROOT.kTRUE)',
			        'ROOT.gInterpreter.Declare("MEMELA a;")'],
   'expr' :   'a(nCleanJet, nLepton, PuppiMET_pt, PuppiMET_phi, Lepton_pt, Lepton_phi, Lepton_eta, CleanJet_pt, CleanJet_phi, CleanJet_eta, Lepton_pdgId)',

}

# D_VBF_DY
aliases['MoMEMta_D'] = {
  'linesToProcess':['ROOT.gSystem.Load("/afs/cern.ch/work/b/bcamaian/mkShapesRDF/momemta/lib/libmomemta.so.1.0.1","",ROOT.kTRUE)',
                    'ROOT.gSystem.Load("/afs/cern.ch/work/b/bcamaian/mkShapesRDF/momemta/lib/libmomemta.so.1","", ROOT.kTRUE)'],
  'linesToAdd': ['#include "%s/extended/MoMEMta_D.cc+"' % configurations],
  'class': 'MoMEMta_discriminant',
  'args': 'nCleanJet, nLepton, PuppiMET_pt, PuppiMET_phi, Lepton_pt[0], Lepton_pt[1], Lepton_phi[0], Lepton_phi[1], Lepton_eta[0], Lepton_eta[1], CleanJet_pt[0], CleanJet_pt[1], CleanJet_phi[0], CleanJet_phi[1], CleanJet_eta[0], CleanJet_eta[1], Lepton_pdgId[0], Lepton_pdgId[1] ',
}

#adnns[0] = isVBF  adnns[1]=isGGH
aliases['adnns'] = {
  'linesToAdd': ['#include "/afs/cern.ch/work/b/bcamaian/mkShapesRDF/VBF_differential/Full2017_v9_2ADNN/evaluate_adnns_2017.cc+"' ],
  'class': 'adversarial_dnn',
  'args': ' nLepton, nCleanJet, Lepton_pdgId[0], Lepton_pdgId[1], CleanJet_eta[0], CleanJet_eta[1], CleanJet_phi[0], CleanJet_phi[1], CleanJet_pt[0], CleanJet_pt[1], Lepton_eta[0], Lepton_eta[1], Lepton_phi[0], Lepton_phi[1], Lepton_pt[0], Lepton_pt[1], Jet_qgl[CleanJet_jetIdx[0]], Jet_qgl[CleanJet_jetIdx[1]],  mjj, mll, ptll, detajj, dphill, PuppiMET_pt, PuppiMET_phi, dphillmet, drll, ht, mTi, mth, m_lj[0], m_lj[1], m_lj[2], m_lj[3], memela[0], memela[1], memela[2], MoMEMta_D[0]',
  #'samples': mc
}


bin_adnnisVBF = ['0.0', '0.50', '0.65', '0.80', '0.85', '0.9', '0.93', '0.95', '0.96', '0.98', '0.99', '1.0']
bin_adnnisGGH = ['0.0', '0.50', '0.65', '0.80', '0.85', '0.9', '0.93', '0.95', '0.96', '0.98', '0.99', '1.0']
adnn2D = ''
for i in range(len(bin_adnnisVBF)-1):
  for j in range(len(bin_adnnisGGH)-1):
    if i+j != len(bin_adnnisVBF)+len(bin_adnnisGGH)-4: 
      adnn2D+='('+bin_adnnisVBF[i]+'<adnns[0])*(adnns[0]<'+bin_adnnisVBF[i+1]+')*(('+str((len(bin_adnnisVBF)-1)*i)+')+('+str(j+1)+'))*('+bin_adnnisGGH[j]+'<adnns[1])*(adnns[1]<'+bin_adnnisGGH[j+1]+')+'
    else: 
      adnn2D+='('+bin_adnnisVBF[i]+'<adnns[0])*(adnns[0]<'+bin_adnnisVBF[i+1]+')*(('+str((len(bin_adnnisVBF)-1)*i)+')+('+str(j+1)+'))*('+bin_adnnisGGH[j]+'<adnns[1])*(adnns[1]<'+bin_adnnisGGH[j+1]+')'
 
aliases['adnns_2D'] = {
    'expr' : adnn2D,
    }


aliases['DeltaPhijj'] = {
  'linesToAdd': ['#include "%s/extended/GetJetDeltaPhi.cc+"' % configurations],
  'class': 'JetDeltaPhi',
  'args': 'nCleanJet, CleanJet_eta, CleanJet_phi',
#   'samples': mc
}

aliases['isFID'] = {
  'linesToAdd': ['#include "%s/extended/isFid.cc+"' % configurations],
  'class': 'isFiducial',
  'args': 'nGenDressedLepton, GenDressedLepton_pdgId, GenDressedLepton_pt, GenDressedLepton_eta, GenDressedLepton_phi, GenDressedLepton_mass, GenDressedLepton_hasTauAnc, nGenJet, GenJet_pt, GenJet_eta, GenJet_phi, GenJet_mass, GenMET_pt, GenMET_phi',
  'samples': mc
}

aliases['GenDeltaPhijj'] = {
  'linesToAdd': ['#include "%s/extended/GetGenJetDeltaPhi.cc+"' % configurations],
  'class': 'GenJetDeltaPhi',
  'args': 'nGenDressedLepton, GenDressedLepton_pdgId, GenDressedLepton_pt, GenDressedLepton_eta, GenDressedLepton_phi, GenDressedLepton_mass, GenDressedLepton_hasTauAnc, nGenJet, GenJet_pt, GenJet_eta, GenJet_phi, GenJet_mass',
  'samples': mc
}




# Couplings used in JHUGen

aliases['G2_HWW']  = {'expr': '1.133582'}
aliases['G4_HWW']  = {'expr': '1.76132'}
aliases['L1_HWW']  = {'expr': '-13752.22'}

aliases['G2_VBF']  = {'expr': '0.27196538'}
aliases['G4_VBF']  = {'expr': '0.29797901870'}
aliases['L1_VBF']  = {'expr': '-2158.21307286'}

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
aliases['JHUXSVBFa1a2'] = {'expr': '2207.6738'}
aliases['JHUXSVBFa1a3'] = {'expr': '1936.4327'}
aliases['JHUXSVBFa1L1'] = {'expr': '2861.7003'}

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
aliases['VBF_H0Mf05_W']  = { 'expr': 'H0Mf05VBF_W*(JHUXSVBFa1a3/JHUXSVBFa1)'}
aliases['VBF_H0PHf05_W'] = { 'expr': 'H0PHf05VBF_W*(JHUXSVBFa1a2/JHUXSVBFa1)'}
aliases['VBF_H0L1f05_W'] = { 'expr': 'H0L1f05VBF_W*(JHUXSVBFa1L1/JHUXSVBFa1)'}
