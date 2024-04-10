import os
import copy
import inspect


configurations = os.path.realpath(inspect.getfile(inspect.currentframe())) # this file
configurations = os.path.realpath(inspect.getfile(inspect.currentframe())) # this file
configurations = os.path.dirname(configurations) 
configurations = os.path.dirname(configurations)
configurations = os.path.dirname(configurations) + '/' # VBF_differential 


aliases = {}
aliases = OrderedDict()

mc     = [skey for skey in samples if skey not in ('Fake', 'DATA', 'Dyemb')]
mc_emb = [skey for skey in samples if skey not in ('Fake', 'DATA')]


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

