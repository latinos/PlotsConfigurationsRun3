import os
import copy
import inspect

configurations = os.path.realpath(inspect.getfile(inspect.currentframe())) # this file
configurations = os.path.dirname(configurations)

aliases = {}
aliases = OrderedDict()

with open('THU/NormTHU.json', 'r') as f:
    NormTHU = json.load(f)
for sample in NormTHU.keys():
    for varName, norm in NormTHU[sample].items():
        if abs(norm[0]) > 10 or abs(norm[0]) < 0.1:
            NormTHU[sample][varName][0] = 1.
            print(varName + ' nuisance Up variation is faulty')
        if abs(norm[1]) > 10 or abs(norm[1]) < 0.1:
            NormTHU[sample][varName][1] = 1.
            print(varName + ' nuisance Down variation is faulty')
        if 'pdf' not in varName:
            aliases['NormTHU_' + sample + '_' + varName + '_Up'] = {
                'expr': str(NormTHU[sample][varName][0]),
                'samples' : sample
            }
            aliases['NormTHU_' + sample + '_' + varName + '_Do'] = {
                'expr': str(NormTHU[sample][varName][1]),
                'samples' : sample
            }
        else:
            aliases['NormTHU_' + sample + '_' + varName] = {
                'expr': str(NormTHU[sample][varName][0]),
                'samples' : sample
            }


mc     = [skey for skey in samples if skey not in ('Fake', 'DATA', 'Dyemb')]
mc_emb = [skey for skey in samples if skey not in ('Fake', 'DATA')]

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
#     'linesToAdd': ['#include "%s/src/PlotsConfigurations/Configurations/Differential/ngenjet.cc+"' % os.getenv('CMSSW_BASE')],
#     'class': 'CountGenJet',
#     'samples': mc
# }

# aliases['getGenZpt_OTF'] = {
#     'linesToAdd':['#include "%s/src/PlotsConfigurations/Configurations/patches/getGenZpt.cc+"' % os.getenv('CMSSW_BASE')],
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

aliases['bVeto'] = {
    'expr': 'Sum(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5 && Take(Jet_btagDeepFlavB, CleanJet_jetIdx) > 0.0490) == 0'
}
aliases['bReq'] = { 
    'expr': 'Sum(CleanJet_pt > 30. && abs(CleanJet_eta) < 2.5 && Take(Jet_btagDeepFlavB, CleanJet_jetIdx) > 0.0490) >= 1'
}

# CR definition

aliases['topcr'] = {
    'expr': 'mll>50 && ((zeroJet && !bVeto) || bReq)'
}

aliases['dycr'] = {
    'expr': 'bVeto'
}

# SR definition

aliases['sr'] = {
    'expr': 'bVeto'
}

aliases['lowZ'] = {
    'expr':  '0.5*abs((Lepton_eta[0] + Lepton_eta[1]) - (CleanJet_eta[0] + CleanJet_eta[1])) < 1'        
}

aliases['highZ'] = {
    'expr':  '0.5*abs((Lepton_eta[0] + Lepton_eta[1]) - (CleanJet_eta[0] + CleanJet_eta[1])) >= 1'
}

# my macro
print('\n\n\n')
print('Configs:\n\n\n')
print(configurations)
print('\n\n\n')

aliases['dr_lj'] = {
  'linesToAdd': ['#include "%s/DR_lj.cc"' % configurations],
  'class': 'dr_lj',
  'args': 'CleanJet_eta, CleanJet_phi, Lepton_eta, Lepton_phi',
  #'samples': mc
}

aliases['m_lj'] = {
  'linesToAdd': ['#include "%s/m_lj.cc"' % configurations],
  'class': 'm_lj',
  'args': 'CleanJet_pt, CleanJet_eta, CleanJet_phi, CleanJet_jetIdx, Jet_mass, Lepton_pt, Lepton_eta, Lepton_phi',
  #'samples': mc
}

aliases['proxyW'] = {
  'linesToAdd': ['#include "%s/proxyW.cc"' % configurations],
  'class': 'proxyW',
  'args': 'Lepton_pt, Lepton_eta, Lepton_phi, PuppiMET_pt, PuppiMET_phi',
  #'samples': mc
}

# SF
# Fixed BTV wp

# btagging MC efficiencies and SFs are read through the btagSF{flavour} object:
# - the first argument is the MC btagging efficiency root file
# - the second argument is the year from which SFs are retrieved from the POG/BTV json-pog correctionlib directory; 
#   allowed options are = ["2016postVFP_UL, 2016preVFP_UL", "2017_UL", "2018_UL"]
# The btagSF{flavour}_{shift} constructor executes the actual computation

# btv_path variable must be updated with the proper year
# replace it with the proper path if you move b-tagging efficiency root files somewhere else

year = '2018_UL' # allowed options are = ["2016postVFP_UL, 2016preVFP_UL", "2017_UL", "2018_UL"]
btv_path = os.environ["STARTPATH"].replace('start.sh', '') + 'mkShapesRDF/processor/data/jsonpog-integration/POG/BTV/' + year

for flavour in ['bc', 'light']:
    for shift in ['central', 'up_uncorrelated', 'down_uncorrelated', 'up_correlated', 'down_correlated']:
        btagsf = 'btagSF' + flavour
        if shift != 'central':
            btagsf += '_' + shift
        aliases[btagsf] = {
            'linesToAdd': [f'#include "{configurations}/evaluate_btagSF{flavour}.cc"'],
            'linesToProcess': [f"ROOT.gInterpreter.Declare('btagSF{flavour} btagSF{flavour}_{shift} = btagSF{flavour}(\"{btv_path}/bTagEff_2018_ttbar_DeepFlavB_loose.root\", \"{year}\");')"], 
            'expr': f'btagSF{flavour}_{shift}(CleanJet_pt, CleanJet_eta, CleanJet_jetIdx, nCleanJet, Jet_hadronFlavour, Jet_btagDeepFlavB, "L", "{shift}")',
            'samples' : mc,
        }

# Shape correction
'''
aliases['bVetoSF'] = {
    #'expr': 'TMath::Exp(Sum(LogVec((CleanJet_pt>20 && abs(CleanJet_eta)<2.5)*Take(Jet_btagSF_deepcsv_shape, CleanJet_jetIdx)+1*(CleanJet_pt<20 || abs(CleanJet_eta)>2.5))))',
    'expr': 'TMath::Exp(Sum(LogVec((CleanJet_pt>20 && abs(CleanJet_eta)<2.5)*Take(Jet_btagSF_deepjet_shape, CleanJet_jetIdx)+1*(CleanJet_pt<20 || abs(CleanJet_eta)>2.5))))',
    'samples': mc
}

aliases['bReqSF'] = {
    #'expr': 'TMath::Exp(Sum(LogVec((CleanJet_pt>30 && abs(CleanJet_eta)<2.5)*Take(Jet_btagSF_deepcsv_shape, CleanJet_jetIdx)+1*(CleanJet_pt<30 || abs(CleanJet_eta)>2.5))))',
    'expr': 'TMath::Exp(Sum(LogVec((CleanJet_pt>30 && abs(CleanJet_eta)<2.5)*Take(Jet_btagSF_deepjet_shape, CleanJet_jetIdx)+1*(CleanJet_pt<30 || abs(CleanJet_eta)>2.5))))',
    'samples': mc
}

aliases['btagSF'] = {
    #'expr': '(bVeto || (topcr && zeroJet))*bVetoSF + (topcr && !zeroJet)*bReqSF',
    'expr': 'bVeto*bVetoSF + topcr*bReqSF',
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
'''
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

aliases['Zepp_l1'] = {
    'expr': 'Lepton_eta[0] - (CleanJet_eta[0] + CleanJet_eta[1])/2'
}

aliases['Zepp_l2'] = {
    'expr': 'Lepton_eta[1] - (CleanJet_eta[0] + CleanJet_eta[1])/2'
}

aliases['Zepp_ll'] = {
    'expr': '0.5*abs((Lepton_eta[0] + Lepton_eta[1]) - (CleanJet_eta[0] + CleanJet_eta[1]))'
}

aliases['Rpt'] = {
    'expr': 'Lepton_pt[0]*Lepton_pt[1]/(CleanJet_pt[0]*CleanJet_pt[1])'
}

# aliases['SFweight2lAlt'] = {
#     'expr'   : 'puWeight*TriggerSFWeight_2l*Lepton_RecoSF[0]*Lepton_RecoSF[1]*EMTFbug_veto',
#     'samples': mc
# }

# aliases['trigger_bits'] = {
#     'expr'    : 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL || HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL || HLT_IsoTkMu24 || HLT_IsoMu24 || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Ele27_WPTight_Gsf || HLT_Ele25_eta2p1_WPTight_Gsf',
#     'samples' : mc
# }

# data/MC scale factors
aliases['SFweight'] = {
    'expr': ' * '.join(['SFweight2l', 'LepWPCut', 'LepWPSF', 'Jet_PUIDSF', 'btagSFbc', 'btagSFlight']),
    #'expr': ' * '.join(['SFweight2l', 'LepWPCut', 'LepWPSF', 'Jet_PUIDSF', 'btagSF']),
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

# Two leading jets matched to gen-level jets with pT > 25 GeV 
aliases['hardJets'] = {
    'expr':  'Jet_genJetIdx[CleanJet_jetIdx[0]] >= 0 && Jet_genJetIdx[CleanJet_jetIdx[1]] >= 0 && GenJet_pt[Jet_genJetIdx[CleanJet_jetIdx[0]]] > 25 && GenJet_pt[Jet_genJetIdx[CleanJet_jetIdx[1]]] > 25', 
    'samples': ['DY']
}

aliases['PUJets'] = {
    'expr':  '!(Jet_genJetIdx[CleanJet_jetIdx[0]] >= 0 && Jet_genJetIdx[CleanJet_jetIdx[1]] >= 0 && GenJet_pt[Jet_genJetIdx[CleanJet_jetIdx[0]]] > 25 && GenJet_pt[Jet_genJetIdx[CleanJet_jetIdx[1]]] > 25)',
    'samples': ['DY']
}

# Number of hard (= gen-matched) jets
aliases['nHardJets'] = {
    # 'expr':  '!(Jet_genJetIdx[CleanJet_jetIdx[0]] >= 0 && Jet_genJetIdx[CleanJet_jetIdx[1]] >= 0 && GenJet_pt[Jet_genJetIdx[CleanJet_jetIdx[0]]] > 25 && GenJet_pt[Jet_genJetIdx[CleanJet_jetIdx[1]]] > 25)',
    'expr':  'Sum(Jet_genJetIdx[CleanJet_jetIdx] >= 0 && GenJet_pt[Jet_genJetIdx[CleanJet_jetIdx]] > 25)',
    'samples': ['DY']
}

aliases['lhe_mjj'] = {
    'expr': 'TMath::Sqrt(2. * LHEPart_pt[4] * LHEPart_pt[5] * (TMath::CosH(LHEPart_eta[4] - LHEPart_eta[5]) - TMath::Cos(LHEPart_phi[4] - LHEPart_phi[5])))',
    'samples': ['Zjj']
}

aliases['dnn_SigVsBkg'] = {
  'linesToAdd': ['#include "%s/dnn_SigVsBkg.cc"' % configurations],
  'class': 'dnn_SigVsBkg',
  'args': ' CleanJet_eta[0], CleanJet_eta[1], CleanJet_phi[0], CleanJet_phi[1], CleanJet_pt[0], CleanJet_pt[1], \
            Lepton_eta[0], Lepton_eta[1], Lepton_phi[0], Lepton_phi[1], Lepton_pt[0], Lepton_pt[1], \
            Rpt, Zepp_l1, Zepp_l2, Zepp_ll, detajj, detall, dphijj, dphilep1jet1, dphilep1jet2, dphilep1jj, \
            dphilep2jet1, dphilep2jet2, dphilep2jj, dphill, dphilljet, dphilljetjet, dphillmet, dphilmet1, dphilmet2, \
            dr_lj[0], dr_lj[1], dr_lj[2], dr_lj[3], drll, ht, m2ljj30, mT2, mTi, m_lj[0], m_lj[1], m_lj[2], m_lj[3], \
            mcoll, mcollWW, mjj, mll, mtw1, mtw2, PuppiMET_phi, proxyW[0], proxyW[1], PuppiMET_pt, ptll, recoil, yll',
  #'samples': mc
}

aliases['dnn_LLVsOther'] = {
  'linesToAdd': ['#include "%s/dnn_LLVsOther.cc"' % configurations],
  'class': 'dnn_LLVsOther',
  'args': ' CleanJet_eta[0], CleanJet_eta[1], CleanJet_phi[0], CleanJet_phi[1], CleanJet_pt[0], CleanJet_pt[1], \
            Lepton_eta[0], Lepton_eta[1], Lepton_phi[0], Lepton_phi[1], Lepton_pt[0], Lepton_pt[1], \
            Rpt, Zepp_l1, Zepp_l2, Zepp_ll, detajj, detall, dphijj, dphilep1jet1, dphilep1jet2, dphilep1jj, \
            dphilep2jet1, dphilep2jet2, dphilep2jj, dphill, dphilljet, dphilljetjet, dphillmet, dphilmet1, dphilmet2, \
            dr_lj[0], dr_lj[1], dr_lj[2], dr_lj[3], drll, ht, m2ljj30, mT2, mTi, m_lj[0], m_lj[1], m_lj[2], m_lj[3], \
            mcoll, mcollWW, mjj, mll, mtw1, mtw2, PuppiMET_phi, proxyW[0], proxyW[1], PuppiMET_pt, ptll, recoil, yll',
  #'samples': mc
}

aliases['dnn_TTVsOther'] = {
  'linesToAdd': ['#include "%s/dnn_TTVsOther.cc"' % configurations],
  'class': 'dnn_TTVsOther',
  'args': ' CleanJet_eta[0], CleanJet_eta[1], CleanJet_phi[0], CleanJet_phi[1], CleanJet_pt[0], CleanJet_pt[1], \
            Lepton_eta[0], Lepton_eta[1], Lepton_phi[0], Lepton_phi[1], Lepton_pt[0], Lepton_pt[1], \
            Rpt, Zepp_l1, Zepp_l2, Zepp_ll, detajj, detall, dphijj, dphilep1jet1, dphilep1jet2, dphilep1jj, \
            dphilep2jet1, dphilep2jet2, dphilep2jj, dphill, dphilljet, dphilljetjet, dphillmet, dphilmet1, dphilmet2, \
            dr_lj[0], dr_lj[1], dr_lj[2], dr_lj[3], drll, ht, m2ljj30, mT2, mTi, m_lj[0], m_lj[1], m_lj[2], m_lj[3], \
            mcoll, mcollWW, mjj, mll, mtw1, mtw2, PuppiMET_phi, proxyW[0], proxyW[1], PuppiMET_pt, ptll, recoil, yll',
  #'samples': mc
}

bin_dnnTT = ['0.', '0.1', '0.2','0.4', '0.6', '0.8', '0.9', '1.']
bin_dnnLL = ['0.', '0.1', '0.2', '0.4', '0.6', '0.8', '0.9', '1.']
dnn2D = ''
for i in range(len(bin_dnnTT)-1):
  for j in range(len(bin_dnnLL)-1):
    if i+j != len(bin_dnnTT)+len(bin_dnnLL)-4: 
      dnn2D+='('+bin_dnnTT[i]+'<dnn_TTVsOther[0])*(dnn_TTVsOther[0]<'+bin_dnnTT[i+1]+')*(('+str((len(bin_dnnTT)-1)*i)+')+('+str(j+1)+'))*('+bin_dnnLL[j]+'<dnn_LLVsOther[0])*(dnn_LLVsOther[0]<'+bin_dnnLL[j+1]+')+'
    else: 
      dnn2D+='('+bin_dnnTT[i]+'<dnn_TTVsOther[0])*(dnn_TTVsOther[0]<'+bin_dnnTT[i+1]+')*(('+str((len(bin_dnnTT)-1)*i)+')+('+str(j+1)+'))*('+bin_dnnLL[j]+'<dnn_LLVsOther[0])*(dnn_LLVsOther[0]<'+bin_dnnLL[j+1]+')'
 
aliases['dnn2D_49'] = {
    'expr' : dnn2D,
    }

bin_dnnTT = ['0.', '0.15', '0.3', '0.5', '0.7', '0.85', '1.']
bin_dnnLL = ['0.', '0.15', '0.3', '0.5', '0.7', '0.85', '1.']
dnn2D = ''
for i in range(len(bin_dnnTT)-1):
  for j in range(len(bin_dnnLL)-1):
    if i+j != len(bin_dnnTT)+len(bin_dnnLL)-4: 
      dnn2D+='('+bin_dnnTT[i]+'<dnn_TTVsOther[0])*(dnn_TTVsOther[0]<'+bin_dnnTT[i+1]+')*(('+str((len(bin_dnnTT)-1)*i)+')+('+str(j+1)+'))*('+bin_dnnLL[j]+'<dnn_LLVsOther[0])*(dnn_LLVsOther[0]<'+bin_dnnLL[j+1]+')+'
    else: 
      dnn2D+='('+bin_dnnTT[i]+'<dnn_TTVsOther[0])*(dnn_TTVsOther[0]<'+bin_dnnTT[i+1]+')*(('+str((len(bin_dnnTT)-1)*i)+')+('+str(j+1)+'))*('+bin_dnnLL[j]+'<dnn_LLVsOther[0])*(dnn_LLVsOther[0]<'+bin_dnnLL[j+1]+')'
 
aliases['dnn2D_36'] = {
    'expr' : dnn2D,
    }

bin_dnnTT = ['0.', '0.15', '0.3', '0.7', '0.85', '1.']
bin_dnnLL = ['0.', '0.15', '0.3', '0.7', '0.85', '1.']
dnn2D = ''
for i in range(len(bin_dnnTT)-1):
  for j in range(len(bin_dnnLL)-1):
    if i+j != len(bin_dnnTT)+len(bin_dnnLL)-4: 
      dnn2D+='('+bin_dnnTT[i]+'<dnn_TTVsOther[0])*(dnn_TTVsOther[0]<'+bin_dnnTT[i+1]+')*(('+str((len(bin_dnnTT)-1)*i)+')+('+str(j+1)+'))*('+bin_dnnLL[j]+'<dnn_LLVsOther[0])*(dnn_LLVsOther[0]<'+bin_dnnLL[j+1]+')+'
    else: 
      dnn2D+='('+bin_dnnTT[i]+'<dnn_TTVsOther[0])*(dnn_TTVsOther[0]<'+bin_dnnTT[i+1]+')*(('+str((len(bin_dnnTT)-1)*i)+')+('+str(j+1)+'))*('+bin_dnnLL[j]+'<dnn_LLVsOther[0])*(dnn_LLVsOther[0]<'+bin_dnnLL[j+1]+')'
 
aliases['dnn2D_25'] = {
    'expr' : dnn2D,
    }

bin_dnnTT = ['0.', '0.2', '0.5', '0.8', '1.']
bin_dnnLL = ['0.', '0.2', '0.5', '0.8', '1.']
dnn2D = ''
for i in range(len(bin_dnnTT)-1):
  for j in range(len(bin_dnnLL)-1):
    if i+j != len(bin_dnnTT)+len(bin_dnnLL)-4: 
      dnn2D+='('+bin_dnnTT[i]+'<dnn_TTVsOther[0])*(dnn_TTVsOther[0]<'+bin_dnnTT[i+1]+')*(('+str((len(bin_dnnTT)-1)*i)+')+('+str(j+1)+'))*('+bin_dnnLL[j]+'<dnn_LLVsOther[0])*(dnn_LLVsOther[0]<'+bin_dnnLL[j+1]+')+'
    else: 
      dnn2D+='('+bin_dnnTT[i]+'<dnn_TTVsOther[0])*(dnn_TTVsOther[0]<'+bin_dnnTT[i+1]+')*(('+str((len(bin_dnnTT)-1)*i)+')+('+str(j+1)+'))*('+bin_dnnLL[j]+'<dnn_LLVsOther[0])*(dnn_LLVsOther[0]<'+bin_dnnLL[j+1]+')'
 
aliases['dnn2D_16'] = {
    'expr' : dnn2D,
    }

bin_dnnTT = ['0.', '0.25', '0.5', '0.75', '1.']
bin_dnnLL = ['0.', '0.25', '0.5', '0.75', '1.']
dnn2D = ''
for i in range(len(bin_dnnTT)-1):
  for j in range(len(bin_dnnLL)-1):
    if i+j != len(bin_dnnTT)+len(bin_dnnLL)-4: 
      dnn2D+='('+bin_dnnTT[i]+'<dnn_TTVsOther[0])*(dnn_TTVsOther[0]<'+bin_dnnTT[i+1]+')*(('+str((len(bin_dnnTT)-1)*i)+')+('+str(j+1)+'))*('+bin_dnnLL[j]+'<dnn_LLVsOther[0])*(dnn_LLVsOther[0]<'+bin_dnnLL[j+1]+')+'
    else: 
      dnn2D+='('+bin_dnnTT[i]+'<dnn_TTVsOther[0])*(dnn_TTVsOther[0]<'+bin_dnnTT[i+1]+')*(('+str((len(bin_dnnTT)-1)*i)+')+('+str(j+1)+'))*('+bin_dnnLL[j]+'<dnn_LLVsOther[0])*(dnn_LLVsOther[0]<'+bin_dnnLL[j+1]+')'
 
aliases['dnn2D_16v2'] = {
    'expr' : dnn2D,
    }

bin_dnnTT = ['0.', '0.5', '1.']
bin_dnnLL = ['0.', '0.5', '1.']
dnn2D = ''
for i in range(len(bin_dnnTT)-1):
  for j in range(len(bin_dnnLL)-1):
    if i+j != len(bin_dnnTT)+len(bin_dnnLL)-4: 
      dnn2D+='('+bin_dnnTT[i]+'<dnn_TTVsOther[0])*(dnn_TTVsOther[0]<'+bin_dnnTT[i+1]+')*(('+str((len(bin_dnnTT)-1)*i)+')+('+str(j+1)+'))*('+bin_dnnLL[j]+'<dnn_LLVsOther[0])*(dnn_LLVsOther[0]<'+bin_dnnLL[j+1]+')+'
    else: 
      dnn2D+='('+bin_dnnTT[i]+'<dnn_TTVsOther[0])*(dnn_TTVsOther[0]<'+bin_dnnTT[i+1]+')*(('+str((len(bin_dnnTT)-1)*i)+')+('+str(j+1)+'))*('+bin_dnnLL[j]+'<dnn_LLVsOther[0])*(dnn_LLVsOther[0]<'+bin_dnnLL[j+1]+')'
 
aliases['dnn2D_4'] = {
    'expr' : dnn2D,
    }

aliases['LLD'] = {
    'expr' : 'dnn_LLVsOther[0]/(1-dnn_TTVsOther[0])',
    }

aliases['TTD'] = {
    'expr' : 'dnn_TTVsOther[0]/(1-dnn_LLVsOther[0])',
    }
