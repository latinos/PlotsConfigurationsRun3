import uproot
import pandas as pd
import numpy as np

root_path = "/afs/cern.ch/user/s/squinto/private/work/PlotsConfigurationRun3/HWW/VBF_DF/2024/rootFiles/HWW/VBF/2024/rootFiles__VBF_DF_2024v15_DBNN_DF/mkShapes__VBF_DF_2024v15_DBNN_DF.root"
tree_path = "trees/hww_sr_inc/"
output_path = "/eos/user/s/squinto/SWAN_projects/ML/df2024VBF_dbnn_all_events.pkl.gz"

label_map = {
    "ggH": "is_ggH",
    "qqH": "is_qqH",
    "top": "is_top",
    "WW":  "is_WW",
}
label_columns = list(label_map.values())

suffixes = {
    "relsample_up": "_relsample_up",
    "relsample_down": "_relsample_down",
    "jer_up": "_jer_up",
    "jer_down": "_jer_down",
    "absolute_up": "_absolute_up",
    "absolute_down": "_absolute_down",
    "flavor_up": "_flavor_up",
    "flavor_down": "_flavor_down",
    "lepres_up": "_lepres_up",
    "lepres_down": "_lepres_down"
}

processes = ['top/Events;1', 'WW/Events;1', 'ggH_hww/Events;1', 'qqH_hww/Events;1']

file = uproot.open(root_path)


counts = {}
for proc in processes:
    tree = file[tree_path + proc]
    counts[proc] = tree.num_entries

min_events = max(counts.values())
print(f"Conteggi per sample: {counts}")
print(f"--> Bilanciamento su: {min_events} eventi per sample\n")


dfs = []

for proc in processes:
    print(f"Processing: {proc}")
    tree = file[tree_path + proc]
    all_branches = tree.keys()

    base_variables = [v for v in all_branches if not any(v.endswith(s) for s in suffixes.values())]
    
    branches_to_read = [v for v in all_branches if any(v.startswith(b) for b in base_variables)]
    data = tree.arrays(branches_to_read, library="np")

    df_temp_all = pd.DataFrame({k: data[k].reshape(-1) for k in branches_to_read})

    df_balanced = df_temp_all

    for version in ['nom', 'relsample_up', 'relsample_down', 'jer_up', 'jer_down', 'absolute_up', 'absolute_down', 'flavor_up', 'flavor_down', 'lepres_up', 'lepres_down']:
        block_dict = {}
        
        for var in base_variables:
            if version == 'nom':
                block_dict[var] = df_balanced[var]
            else:
                var_variant = var + suffixes[version]
                if var_variant in df_balanced.columns:
                    block_dict[var] = df_balanced[var_variant]
                else:
                    block_dict[var] = df_balanced[var]
        
        df_version = pd.DataFrame(block_dict)

        # Flag variazione
        df_version['is_nom'] = 1 if version == 'nom' else 0
        df_version['is_relsample_up'] = 1 if version == 'relsample_up' else 0
        df_version['is_relsample_down'] = 1 if version == 'relsample_down' else 0
        df_version['is_jer_up'] = 1 if version == 'jer_up' else 0
        df_version['is_jer_down'] = 1 if version == 'jer_down' else 0
        df_version['is_absolute_up'] = 1 if version == 'absolute_up' else 0
        df_version['is_absolute_down'] = 1 if version == 'absolute_down' else 0
        df_version['is_flavor_up'] = 1 if version == 'flavor_up' else 0
        df_version['is_flavor_down'] = 1 if version == 'flavor_down' else 0
        df_version['is_lepres_up'] = 1 if version == 'lepres_up' else 0
        df_version['is_lepres_down'] = 1 if version == 'lepres_down' else 0


        # Flag processo
        for col in label_columns:
            df_version[col] = 0
        for key, label in label_map.items():
            if key in proc:
                df_version[label] = 1

        dfs.append(df_version)

if not dfs:
    raise RuntimeError("No data to concatenate")

df_final = pd.concat(dfs, ignore_index=True)

print("\n--- Statistiche Finali ---")
print(f"Shape totale: {df_final.shape}")
print("Colonne finali:" + str(df_final.columns.tolist()))
print("Distribuzione per processo (considerando Nom+Up+Down):")
for col in label_columns:
    print(f"  {col}: {df_final[df_final[col] == 1].shape[0]}")

df_final.to_pickle(output_path)
print(f"\nFile salvato con successo in: {output_path}")