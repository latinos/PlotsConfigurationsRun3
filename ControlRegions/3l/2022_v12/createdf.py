import uproot
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
flat_tree = uproot.open("/afs/cern.ch/user/s/squinto/private/work/PlotsConfigurationsRun3/HWW/ggH_DF/2022/rootFiles/HWW/rootFiles__ggH_DF_2022_tree/mkShapes__ggH_DF_2022_tree.root")["trees/hww_sr_inc/"]
process = flat_tree.keys()[1::2]
print(process)
flat_tree = uproot.open("/afs/cern.ch/user/s/squinto/private/work/PlotsConfigurationsRun3/HWW/ggH_DF/2022/rootFiles/HWW/rootFiles__ggH_DF_2022_tree/mkShapes__ggH_DF_2022_tree.root")["trees/hww_sr_inc/" + process[0]]
variables = flat_tree.keys()
print(variables)

dfs = []

root_path = "/afs/cern.ch/user/s/squinto/private/work/PlotsConfigurationsRun3/HWW/ggH_DF/2022/rootFiles/HWW/rootFiles__ggH_DF_2022_tree/mkShapes__ggH_DF_2022_tree.root"
tree_path = "trees/hww_sr_inc/"
signal_processes = {'ggH_hww/Events;1', 'qqH_hww/Events;1'}


flat_tree = uproot.open(root_path)

for i in process:
    print(f"Processing: {i}")
    if tree_path + i not in flat_tree:
        print(f"Tree {tree_path + i} not found.")
        continue

    # Load the tree
    tree = flat_tree[tree_path + i]

    # Filter the keys to only those in `variables`
    available_variables = [var for var in variables if var in tree.keys()]

    if not available_variables:
        print(f"No matching variables for process: {i}")
        continue

    # Load all variables at once
    data = tree.arrays(available_variables, library="np")

    # Convert to DataFrame
    df_temp = pd.DataFrame({key: data[key].reshape(-1) for key in available_variables})

    if not df_temp.empty:
        # Assign labels
        df_temp['isSig'] = int(i in signal_processes)

        dfs.append(df_temp)
    else:
        print(f"No data found for process: {i}")

# Concatenate all DataFrames if any
if dfs:
    df = pd.concat(dfs, ignore_index=True)

    # Ensure columns are in the desired order
    order = ['nvtx', 'mll', 'mth', 'ptll', 'drll', 'dphill', '__pt1', '__pt2', '__eta1', '__eta2', '__phi1', '__phi2', 'puppimet', '__njet', 'jetpt1', 'jetpt2', 'jeteta1', 'jeteta2', 'isSig']
    df = df[order]

    # Add isBkg and variation labels
    df['isBkg'] = 1 - df['isSig']
    print(df)
else:
    print("No data to concatenate.")

#siglen = len(df[df['isSig'] == 1])
#print(siglen * 2)
#bkgsel = df[df['isBkg'] == 1].sample(siglen)
#sigsel = df[df['isSig'] == 1]
#df = pd.concat([sigsel, bkgsel])
df

df.to_pickle("/eos/user/s/squinto/SWAN_projects/ML/dfRerunnocuts.pkl.gz")
