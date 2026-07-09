import os
import copy
import inspect

ROOT.gSystem.Load("libGpad.so")
ROOT.gSystem.Load("libGraf.so")

ROOT.gSystem.Load("libPhysics")
ROOT.gSystem.Load("libROOTVecOps")

configurations = os.path.realpath(inspect.getfile(inspect.currentframe()))
macros = os.path.dirname(configurations) + '/macros/'
fakerates = os.path.dirname(os.path.dirname(os.path.dirname(configurations))) + '/utils/data/FakeRate'
btagmaps = os.path.dirname(os.path.dirname(os.path.dirname(configurations))) + '/utils/data/btag'
print(macros)
print(fakerates)
print(btagmaps)

aliases = OrderedDict()

mc     = [skey for skey in samples if skey not in ('Fake', 'DATA', 'Dyemb', 'DATA_EG', 'DATA_Mu', 'DATA_EMu', 'Fake_EG', 'Fake_Mu', 'Fake_EMu')]
mc_emb = [skey for skey in samples if skey not in ('Fake', 'DATA', 'DATA_Mu', 'DATA_EMu', 'Fake_EG', 'Fake_Mu', 'Fake_EMu')]


# LepCut2l__ele_cutBased_LooseID_tthMVA_Run3__mu_cut_TightID_pfIsoTight_HWW_tthmva_67
eleWP = 'cutBased_LooseID_tthMVA_Run3'
muWP  = 'cut_TightID_pfIsoTight_HWW_tthmva_67'

aliases['LepWPCut'] = {
    'expr': 'LepCut2l__ele_'+eleWP+'__mu_'+muWP,
    'samples': mc + ['DATA'],
}

aliases['LepWPSF'] = {
    'expr': 'LepSF2l__ele_'+eleWP+'__mu_'+muWP,
    'samples': mc
}

# gen-matching to prompt only (GenLepMatch2l matches to *any* gen lepton)
aliases['PromptGenLepMatch2l'] = {
    'expr': 'Alt(Lepton_promptgenmatched, 0, 0) * Alt(Lepton_promptgenmatched, 1, 0)',
    'samples': mc
}

# Jet bins
# using Alt(CleanJet_pt, n, 0) instead of Sum(CleanJet_pt >= 30) because jet pt ordering is not strictly followed in JES-varied samples

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

aliases['noJetInHorn'] = {
    'expr' : 'Sum(CleanJet_pt > 30 && CleanJet_pt < 50 && abs(CleanJet_eta) > 2.5 && abs(CleanJet_eta) < 3.0) == 0',
}

Tag = 'ele_'+eleWP+'_mu_'+muWP

# Fake leptons transfer factor
aliases['fakeW'] = {
    'linesToAdd'     : [f'#include "{macros}fake_rate_reader_class.cc"'],
    'linesToProcess' : [f"ROOT.gInterpreter.ProcessLine('fake_rate_reader fr_reader = fake_rate_reader(\"{eleWP}\", \"{muWP}\", \"nominal\", 2, \"std\", \"{fakerates}\", \"2024_v15_pt\");')"],
    'expr'           : f'fr_reader(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_{muWP}, Lepton_isTightElectron_{eleWP}, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
    'samples'        : ['Fake']
}

for stat in ['','Stat']:
    for lep in ['Ele','Mu']:
        for variation in ['Up','Down']:
            aliases['fakeW'+stat+lep+variation] = {
                'linesToAdd'     : [f'#include "{macros}fake_rate_reader_class.cc"'],
                'linesToProcess' : [f"ROOT.gInterpreter.ProcessLine('fake_rate_reader fr_reader{stat}{lep}{variation} = fake_rate_reader(\"{eleWP}\", \"{muWP}\", \"{stat}{lep}{variation}\", 2, \"std\", \"{fakerates}\", \"2024_v15_pt\");')"],
                'expr'           : f'fr_reader{stat}{lep}{variation}(Lepton_pdgId, Lepton_pt, Lepton_eta, Lepton_isTightMuon_{muWP}, Lepton_isTightElectron_{eleWP}, Lepton_muonIdx, CleanJet_pt, nCleanJet)',
                'samples'        : ['Fake']
            }

#Top pT reweighting
aliases['Top_pTrw'] = {
    'expr': '(topGenPt * antitopGenPt > 0.) * (TMath::Sqrt((0.103*TMath::Exp(-0.0118*topGenPt) - 0.000134*topGenPt + 0.973) * (0.103*TMath::Exp(-0.0118*antitopGenPt) - 0.000134*antitopGenPt + 0.973))) + (topGenPt * antitopGenPt <= 0.)',
    'samples': ['top']
}


##########################################################################
# B-Tagging WP: https://btv-wiki.docs.cern.ch/ScaleFactors/Run3Summer23/
##########################################################################

# Algo / WP / WP cut
btagging_WPs = {
    "UParTAK4B" : {"loose" : "0.0246", "medium" : "0.1272", "tight" : "0.4648", "xtight" : "0.6298", "xxtight" : "0.9739"},
}

# Algo / SF name
btagging_SFs = {
    "UParTAK4B"      : "upart",
}

# Algorithm and WP selection
bAlgo = 'UParTAK4B'
WP    = 'loose'     # ['loose','medium','tight','xtight','xxtight']

WP_eval = 'L' # ['L', 'M', 'T', 'XT', 'XXT']
tagger = 'UParTAK4'

# Access information from dictionaries
bWP   = btagging_WPs[bAlgo][WP]

#################
### B-tagging ###
#################

# Fixed BTV wp

# btagging MC efficiencies and SFs are read through the btagSF{flavour} object:
# - the first argument is the MC btagging efficiency root file
# - the second argument is the year from which SFs are retrieved from the POG/BTV json-pog correctionlib directory; 
#   allowed options are = ['Run3-22CDSep23-Summer22-NanoAODv12', 'Run3-22EFGSep23-Summer22EE-NanoAODv12, 'Run3-23CSep23-Summer23-NanoAODv12', 'Run3-23DSep23-Summer23BPix-NanoAODv12', 'Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15']
# The btagSF{flavour}_{shift} constructor executes the actual computation
# In this you specify the WP for the computation and the tagger using the WP_eval and tagger strings.

# We assume that you heve the efficiency maps root files in your configuration, as well as the evaluation macros
# If this is not the case, swap configurations with the proper path

# path = "your/path"

eff_map_year = '2024' #['2022', '2022EE', '2023', '2023BPix', '2024]
year = 'Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15' # ['Run3-22CDSep23-Summer22-NanoAODv12', 'Run3-22EFGSep23-Summer22EE-NanoAODv12, 'Run3-23CSep23-Summer23-NanoAODv12', 'Run3-23DSep23-Summer23BPix-NanoAODv12', 'Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15']

shifts_per_flavour = {
    'bc'   : ['central', 'down', 'down_bfragmentation', 'down_correlated', 'down_fsrdef', 'down_hdamp', 'down_isrdef', 'down_jer', 'down_jes', 'down_muf', 'down_mur', 'down_pdfas', 'down_pileup', 'down_statistic', 'down_topmass', 'down_type3', 'down_uncorrelated', 'up', 'up_bfragmentation', 'up_correlated', 'up_fsrdef', 'up_hdamp', 'up_isrdef', 'up_jer', 'up_jes', 'up_muf', 'up_mur', 'up_pdfas', 'up_pileup', 'up_statistic', 'up_topmass', 'up_type3', 'up_uncorrelated'],    
    'light': ['central', 'down', 'down_correlated', 'down_uncorrelated', 'up', 'up_correlated', 'up_uncorrelated'],
}

for flavour in ['bc', 'light']:
    for shift in shifts_per_flavour[flavour]:
        btagsf = 'btagSF' + flavour
        if shift != 'central':
            btagsf += '_' + shift
        aliases[btagsf] = {
            'linesToAdd': [f'#include "{macros}evaluate_btagSF{flavour}.cc"'],
            'linesToProcess': [f"ROOT.gInterpreter.ProcessLine('btagSF{flavour} btagSF{flavour}_{shift} = btagSF{flavour}(\"{btagmaps}/{eff_map_year}/bTagEff_{eff_map_year}_ttbar_{bAlgo}_loose.root\", \"{year}\");')"],
            'expr': f'btagSF{flavour}_{shift}(CleanJet_pt, CleanJet_eta, CleanJet_jetIdx, nCleanJet, Jet_hadronFlavour, Jet_btag{bAlgo}, "{WP_eval}", "{shift}", "{tagger}","{eff_map_year}")',
            'samples' : mc,
        }

# B tagging selections and scale factors
aliases['bVeto'] = {
    'expr': f'Sum(CleanJet_pt > 20. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{bAlgo}, CleanJet_jetIdx) > {bWP}) == 0'
}

aliases['bReq'] = { 
    'expr': f'Sum(CleanJet_pt > 30. && abs(CleanJet_eta) < 2.5 && Take(Jet_btag{bAlgo}, CleanJet_jetIdx) > {bWP}) >= 1'
}

# CR definition
#TODO: mtw2 > 30 ?
aliases['topcr'] = {
    'expr': 'mll > 50 && ((zeroJet && !bVeto) || bReq)'
}
aliases['dycr'] = {
    'expr': 'mth < 60 && abs(mll-65) < 15 && bVeto'
}
aliases['wwcr'] = {
    'expr': 'mth > 60 && mtw2 > 30 && mll > 100 && bVeto'
}

# SR definition
aliases['sr'] = {
    'expr': 'bVeto'
}



########################
### End of b tagging ###
########################

# data/MC scale factors

# Use this for the usual SF
aliases['SFweight'] = {
    'expr': ' * '.join(['SFweight2l', 'LepWPCut', 'LepWPSF', 'btagSFbc', 'btagSFlight']),
    'samples': mc
}


aliases['SFweightEleUp'] = {
    'expr': 'LepSF2l__ele_'+eleWP+'__Up',
    'samples': mc
}
aliases['SFweightEleDown'] = {
    'expr': 'LepSF2l__ele_'+eleWP+'__Down',
    'samples': mc
}
aliases['SFweightMuUp'] = {
    'expr': 'LepSF2l__mu_'+muWP+'__Up',
    'samples': mc
}
aliases['SFweightMuDown'] = {
    'expr': 'LepSF2l__mu_'+muWP+'__Down',
    'samples': mc
}

############## signal specific

#auxiliary
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

aliases['dr_lj'] = {
  'linesToAdd': [f'#include "{macros}DR_lj.cc"'],
  'class': 'dr_lj',
  'args': 'CleanJet_eta, CleanJet_phi, Lepton_eta, Lepton_phi',
  #'samples': mc
}

aliases['m_lj'] = {
  'linesToAdd': [f'#include "{macros}m_lj.cc"'],
  'class': 'm_lj',
  'args': 'CleanJet_pt, CleanJet_eta, CleanJet_phi, CleanJet_jetIdx, Jet_mass, Lepton_pt, Lepton_eta, Lepton_phi',
  #'samples': mc
}

aliases['proxyW'] = {
  'linesToAdd': [f'#include "{macros}proxyW.cc"'],
  'class': 'proxyW',
  'args': 'Lepton_pt, Lepton_eta, Lepton_phi, PuppiMET_pt, PuppiMET_phi',
  #'samples': mc
}

aliases['mT2'] = {
  #'linesToAdd': [f'#include "{macros}mT2.cc"'],
  'linesToAdd' : [f'gSystem->Load("{macros}mT2_cc.so")'],
  'class': 'mT2',
  'args': 'Lepton_pt, Lepton_eta, Lepton_phi, PuppiMET_pt, PuppiMET_phi',
  #'samples': mc
}

######
#1D  #
######
aliases['dnn_SigVsBkg'] = {
  #'linesToAdd': [f'gSystem->Load("{macros}dnn_SigVsBkg_cc.so")'],
  'linesToProcess': [f"ROOT.gInterpreter.ProcessLine('.L {macros}dnn_SigVsBkg.cc+')"],
  'expr': 'dnn_SigVsBkg(CleanJet_eta[0], CleanJet_eta[1], CleanJet_phi[0], CleanJet_phi[1], CleanJet_pt[0], CleanJet_pt[1], \
            Lepton_eta[0], Lepton_eta[1], Lepton_phi[0], Lepton_phi[1], Lepton_pt[0], Lepton_pt[1], \
            Rpt, Zepp_l1, Zepp_l2, Zepp_ll, detajj, detall, dphijj, dphilep1jet1, dphilep1jet2, dphilep1jj, \
            dphilep2jet1, dphilep2jet2, dphilep2jj, dphill, dphilljet, dphilljetjet, dphillmet, dphilmet1, dphilmet2, \
            dr_lj[0], dr_lj[1], dr_lj[2], dr_lj[3], drll, ht, m2ljj30, mT2, mTi, m_lj[0], m_lj[1], m_lj[2], m_lj[3], \
            mcoll, mcollWW, mjj, mll, mtw1, mtw2, PuppiMET_phi, proxyW[0], proxyW[1], PuppiMET_pt, ptll, recoil, yll)',
  #'samples': mc          
}  

aliases['dnn_LLVsOther'] = {
  #'linesToAdd': [f'#include "{macros}dnn_LLVsOther.cc"'],
  'linesToProcess': [f"ROOT.gInterpreter.ProcessLine('.L {macros}dnn_LLVsOther.cc+')"],
  'expr': 'dnn_LLVsOther(CleanJet_eta[0], CleanJet_eta[1], CleanJet_phi[0], CleanJet_phi[1], CleanJet_pt[0], CleanJet_pt[1], \
            Lepton_eta[0], Lepton_eta[1], Lepton_phi[0], Lepton_phi[1], Lepton_pt[0], Lepton_pt[1], \
            Rpt, Zepp_l1, Zepp_l2, Zepp_ll, detajj, detall, dphijj, dphilep1jet1, dphilep1jet2, dphilep1jj, \
            dphilep2jet1, dphilep2jet2, dphilep2jj, dphill, dphilljet, dphilljetjet, dphillmet, dphilmet1, dphilmet2, \
            dr_lj[0], dr_lj[1], dr_lj[2], dr_lj[3], drll, ht, m2ljj30, mT2, mTi, m_lj[0], m_lj[1], m_lj[2], m_lj[3], \
            mcoll, mcollWW, mjj, mll, mtw1, mtw2, PuppiMET_phi, proxyW[0], proxyW[1], PuppiMET_pt, ptll, recoil, yll)',
  #'samples': mc
}

aliases['dnn_TTVsOther'] = {
  #'linesToAdd': [f'#include "{macros}dnn_TTVsOther.cc"'],
  'linesToProcess': [f"ROOT.gInterpreter.ProcessLine('.L {macros}dnn_TTVsOther.cc+')"],
  'expr': 'dnn_TTVsOther(CleanJet_eta[0], CleanJet_eta[1], CleanJet_phi[0], CleanJet_phi[1], CleanJet_pt[0], CleanJet_pt[1], \
            Lepton_eta[0], Lepton_eta[1], Lepton_phi[0], Lepton_phi[1], Lepton_pt[0], Lepton_pt[1], \
            Rpt, Zepp_l1, Zepp_l2, Zepp_ll, detajj, detall, dphijj, dphilep1jet1, dphilep1jet2, dphilep1jj, \
            dphilep2jet1, dphilep2jet2, dphilep2jj, dphill, dphilljet, dphilljetjet, dphillmet, dphilmet1, dphilmet2, \
            dr_lj[0], dr_lj[1], dr_lj[2], dr_lj[3], drll, ht, m2ljj30, mT2, mTi, m_lj[0], m_lj[1], m_lj[2], m_lj[3], \
            mcoll, mcollWW, mjj, mll, mtw1, mtw2, PuppiMET_phi, proxyW[0], proxyW[1], PuppiMET_pt, ptll, recoil, yll)',
  #'samples': mc
}

aliases['LLD'] = {
    'expr' : 'dnn_LLVsOther[0]/(1-dnn_TTVsOther[0])',
    }

aliases['TTD'] = {
    'expr' : 'dnn_TTVsOther[0]/(1-dnn_LLVsOther[0])',
    }

#######
#2D   #
#######
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
