import os
import copy
import inspect
import ROOT
import json

ROOT.gSystem.Load("libGpad.so")
ROOT.gSystem.Load("libGraf.so")
ROOT.gSystem.Load("libc.so")

configurations = os.path.realpath(inspect.getfile(inspect.currentframe()))


aliases = {}
aliases = OrderedDict()

mc     = [skey for skey in samples if skey not in ('Fake', 'DATA')]
mc_emb = [skey for skey in samples if skey not in ('Fake', 'DATA')]

# LepSF2l__ele_cutBased_MediumID_tthMVA_Run3__mu_cut_TightID_pfIsoTight_HWW_tthmva_67
eleWP = 'cutBased_MediumID_tthMVA_Run3'
muWP  = 'cut_TightID_pfIsoTight_HWW_tthmva_67'

aliases['LepWPCut'] = {
    'expr': 'LepCut2l__ele_'+eleWP+'__mu_'+muWP,
    'samples': mc + ['DATA'],
}
