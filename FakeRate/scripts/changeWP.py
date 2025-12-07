import os

# Cartella contenente i file da modificare
folder_path = "/afs/cern.ch/user/s/squinto/private/work/PlotsConfigurationRun3/FakeRate/2022EE_v12"

# Dizionario delle stringhe da sostituire: chiave = vecchia stringa, valore = nuova stringa
replacements = {
    "cutBased_LooseID_tthMVA_Run3": "wp90iso",
    "cut_TightID_pfIsoTight_HWW_tthmva_67": "cut_Tight_HWW"
}

# Itera su tutti i file nella cartella
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    
    # Modifica solo file di testo (puoi cambiare l'estensione se vuoi)
    if os.path.isfile(file_path) and (filename.endswith(".py") or filename.endswith(".sh")):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Sostituisci le stringhe
        for old_str, new_str in replacements.items():
            content = content.replace(old_str, new_str)
        
        # Riscrivi il file con le modifiche
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

print("Sostituzioni completate!")
