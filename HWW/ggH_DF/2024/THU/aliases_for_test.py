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

with open('NormTHU.json', 'r') as f:
    NormTHU = json.load(f)

for sample in NormTHU.keys():
    for varName, norm in NormTHU[sample].items():
        
        # --- 1. Handle single float variations (Envelope Nuisances) ---
        if isinstance(norm, (int, float)):
            val = norm
            if abs(val) > 10 or abs(val) < 0.1:
                val = 1.
                NormTHU[sample][varName] = 1.
                print(f"[WARNING] {varName} nuisance envelope variation is faulty, set to 1.0")
            
            alias_name = f'NormTHU_{sample}_{varName}'
            aliases[alias_name] = {
                'expr': str(val),
                'samples': sample
            }
            
            # Print single-value alias
            print(f"{alias_name} = {val}")

        # --- 2. Handle 2-element list variations (Standard Up/Down) ---
        elif isinstance(norm, list) and len(norm) == 2:
            if abs(norm[0]) > 10 or abs(norm[0]) < 0.1:
                NormTHU[sample][varName][0] = 1.
                print(f"[WARNING] {varName} nuisance Up variation is faulty, set to 1.0")
            if abs(norm[1]) > 10 or abs(norm[1]) < 0.1:
                NormTHU[sample][varName][1] = 1.
                print(f"[WARNING] {varName} nuisance Down variation is faulty, set to 1.0")
                
            val_up = NormTHU[sample][varName][0]
            val_down = NormTHU[sample][varName][1]

            if 'pdf' not in varName:
                alias_up = f'NormTHU_{sample}_{varName}_Up'
                alias_down = f'NormTHU_{sample}_{varName}_Down'
                
                aliases[alias_up] = {
                    'expr': str(val_up),
                    'samples': sample
                }
                aliases[alias_down] = {
                    'expr': str(val_down),
                    'samples': sample
                }
                
                # Print Up/Down aliases
                print(f"{alias_up} = {val_up}")
                print(f"{alias_down} = {val_down}")
            else:
                alias_name = f'NormTHU_{sample}_{varName}'
                aliases[alias_name] = {
                    'expr': str(val_up),
                    'samples': sample
                }
                
                # Print single PDF alias
                print(f"{alias_name} = {val_up}")

# LepSF2l__ele_cutBased_MediumID_tthMVA_Run3__mu_cut_TightID_pfIsoTight_HWW_tthmva_67
eleWP = 'cutBased_MediumID_tthMVA_Run3'
muWP  = 'cut_TightID_pfIsoTight_HWW_tthmva_67'

aliases['LepWPCut'] = {
    'expr': 'LepCut2l__ele_'+eleWP+'__mu_'+muWP,
    'samples': mc + ['DATA'],
}
