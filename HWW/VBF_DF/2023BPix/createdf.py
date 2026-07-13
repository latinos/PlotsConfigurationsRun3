import uproot
import pandas as pd
import numpy as np

root_path = "/afs/cern.ch/user/s/squinto/private/work/PlotsConfigurationRun3/HWW/VBF_DF/2023BPix/rootFiles/HWW/VBF/2023BPix/rootFiles__VBF_DF_2023BPixv12_traindf/mkShapes__VBF_DF_2023BPixv12_traindf.root"
tree_path = "trees/hww_sr_inc/"

file = uproot.open(root_path)

processes = file[tree_path].keys()[1::2]
print(processes)

# --------------------------------------------------
# Find variables from the first valid tree
# --------------------------------------------------
variables = None
for proc in processes:
    tree = file[tree_path + proc]
    if len(tree.keys()) > 0:
        variables = tree.keys()
        break

if variables is None:
    raise RuntimeError("Could not find any tree with branches")

print("Variables:", variables)

# --------------------------------------------------
# Process → label mapping
# --------------------------------------------------
label_map = {
    "ggH": "is_ggH",
    "qqH": "is_qqH",
    "top": "is_top",
    "WW":  "is_WW",
}

label_columns = list(label_map.values())
dfs = []

# --------------------------------------------------
# Loop over processes
# --------------------------------------------------
processes = ['top/Events;1', 'WW/Events;1', 'ggH_hww/Events;1', 'qqH_hww/Events;1']
for proc in processes:
    print(f"Processing: {proc}")
    tree = file[tree_path + proc]

    available_variables = [v for v in variables if v in tree.keys()]
    if not available_variables:
        print(f"No matching variables for {proc}")
        continue

    data = tree.arrays(available_variables, library="np")
    df_temp = pd.DataFrame({k: data[k].reshape(-1) for k in available_variables})

    if df_temp.empty:
        continue

    # Initialize labels
    for col in label_columns:
        df_temp[col] = 0

    # Set correct label
    for key, label in label_map.items():
        if key in proc:
            df_temp[label] = 1

    dfs.append(df_temp)

# --------------------------------------------------
# Concatenate
# --------------------------------------------------
if not dfs:
    raise RuntimeError("No data to concatenate")

df = pd.concat(dfs, ignore_index=True)
print(df)

df.to_pickle("/eos/user/s/squinto/SWAN_projects/ML/df2023BPixVBF_syst.pkl.gz")