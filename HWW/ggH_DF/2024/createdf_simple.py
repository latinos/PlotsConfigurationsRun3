import uproot
import pandas as pd
import numpy as np

root_path = "/afs/cern.ch/user/s/squinto/private/work/PlotsConfigurationRun3/HWW/ggH_DF/2024/rootFiles/HWW/ggF/2024/rootFiles__ggF_DF_2024_0526_df_simple/mkShapes__ggF_DF_2024_0526_df_simple.root"
tree_path = "trees/hww_sr_inc/"
output_path = "/eos/user/s/squinto/SWAN_projects/ML/df2024ggf_simple.pkl.gz"

# Manteniamo la tua impostazione: qqH è un fondo (is_Bkg)
label_map = {
    "ggH": "is_Sig",
    "qqH": "is_Bkg",  
    "top": "is_Bkg",
    "WW":  "is_Bkg",
    "ggWW": "is_Bkg",
    #"DY": "is_Bkg",
}
label_columns = list(set(label_map.values()))

#processes = ['top/Events;1', 'WW/Events;15', 'WW/Events;16', 'ggH_hww/Events;1', 'qqH_hww/Events;1', 'ggWW/Events;2', 'ggWW/Events;3', 'DY/Events;1']
processes = ['top/Events;1', 'WW/Events;15', 'WW/Events;16', 'ggH_hww/Events;1', 'qqH_hww/Events;1', 'ggWW/Events;2', 'ggWW/Events;3']

file = uproot.open(root_path)

# --- 1. Mappatura precisa dei singoli processi ---
tree_to_macro = {}
for proc in processes:
    if "ggH_hww" in proc:
        tree_to_macro[proc] = "ggH"
    elif "qqH_hww" in proc:
        tree_to_macro[proc] = "qqH"
    elif "top" in proc:
        tree_to_macro[proc] = "top"
    elif "ggWW" in proc:
        tree_to_macro[proc] = "ggWW"
    elif "WW" in proc:
        tree_to_macro[proc] = "WW"
    #elif "DY" in proc:
    #    tree_to_macro[proc] = "DY"

# --- 2. Calcolo dei conteggi reali per Macro-Processo ---
counts = {}
macro_counts = {k: 0 for k in label_map.keys()}

for proc in processes:
    tree = file[tree_path + proc]
    n_entries = tree.num_entries
    counts[proc] = n_entries
    
    macro = tree_to_macro[proc]
    macro_counts[macro] += n_entries

print(f"Conteggi per singolo TTree: {counts}\n")
print("--- Conteggi totali aggregati per fisica ---")
for k, v in macro_counts.items():
    print(f"  {k}: {v} eventi")

bkg_keys = [k for k, v in label_map.items() if v == "is_Bkg" and macro_counts[k] > 0]
sig_keys = [k for k, v in label_map.items() if v == "is_Sig" and macro_counts[k] > 0]

# Calcoliamo i limiti massimi teorici per capire dove sta il collo di bottiglia
min_bkg_macro = min([macro_counts[k] for k in bkg_keys])
max_bkg_theor = min_bkg_macro * len(bkg_keys)
max_sig_avail = sum([macro_counts[k] for k in sig_keys])

# IL VERO COLLO DI BOTTIGLIA: Il target totale è il minimo tra il fondo massimo equo e il segnale totale disponibile
total_target_per_class = min(max_bkg_theor, max_sig_avail)

# Ripartiamo il target finale equamente tra i singoli macro-processi
events_per_bkg = int(total_target_per_class / len(bkg_keys))
events_per_sig = int(total_target_per_class / len(sig_keys))

print("\n--- Nuova Strategia di Bilanciamento (Logica Universale del Collo di Bottiglia) ---")
print(f"--> Massimo fondo teorico (mantenendo equità): {max_bkg_theor} eventi")
print(f"--> Massimo segnale disponibile nel file:     {max_sig_avail} eventi")
print(f"--> COLLO DI BOTTIGLIA RILEVATO. Target finale per classe (Sig/Bkg): {total_target_per_class} eventi")
print(f"--> Ogni macro-processo di FONDO sarà tagliato a: {events_per_bkg} eventi")
print(f"--> Ogni macro-processo di SEGNALE sarà tagliato a: {events_per_sig} eventi")

# --- 3. Processamento e Campionamento ---
dfs = []

for proc in processes:
    print(f"Processing: {proc}")
    tree = file[tree_path + proc]
    df_proc = tree.arrays(library="pd")
    df_proc.columns = [c.decode('utf-8') if isinstance(c, bytes) else c for c in df_proc.columns]
    
    current_macro = tree_to_macro[proc]
    macro_total = macro_counts[current_macro]
    tree_total = counts[proc]
    
    # Determina il target a seconda che sia segnale o fondo
    if label_map[current_macro] == "is_Bkg":
        macro_target = events_per_bkg
    else:
        macro_target = events_per_sig

    # Calcola la quota proporzionale per questo specifico TTree del fondo
    if macro_total > 0:
        n_target = int((tree_total / macro_total) * macro_target)
    else:
        n_target = 0
        
    # Applica il campionamento (solo se dobbiamo ridurre gli eventi, cioè per i fondi)
    if n_target > 0 and n_target <= len(df_proc):
        df_proc = df_proc.sample(n=n_target, random_state=42).reset_index(drop=True)
    elif n_target > len(df_proc):
        print(f"  Warning: richiesti {n_target} eventi per {proc} ma disponibili solo {len(df_proc)}.")
    
    # Inizializzazione colonne target (tutte a 0)
    for col in label_columns:
        df_proc[col] = 0
        
    # Imposta la label corretta a 1
    target_label = label_map[current_macro]
    df_proc[target_label] = 1
    
    dfs.append(df_proc)

if not dfs:
    raise RuntimeError("No data to concatenate")

# Merge di tutti i campioni
df_final = pd.concat(dfs, ignore_index=True)

# Shuffle finale del dataset
df_final = df_final.sample(frac=1, random_state=42).reset_index(drop=True)

print("\n--- Statistiche Finali ---")
print(f"Shape totale: {df_final.shape}")
print(f"Numero di colonne totali: {len(df_final.columns)}")

for col in label_columns:
    print(f"  {col}: {df_final[df_final[col] == 1].shape[0]} eventi")

# Salvataggio su EOS
df_final.to_pickle(output_path, compression='gzip')
print(f"\nFile bilanciato perfettamente salvato in: {output_path}")