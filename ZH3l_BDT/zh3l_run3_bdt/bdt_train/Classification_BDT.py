#!/usr/bin/env python
import ROOT
from ROOT import TMVA, TFile, TTree, TCut, TChain, RDataFrame
from subprocess import call
import os
from os.path import isfile
import json
import sys
import re
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_curve, roc_auc_score, accuracy_score, confusion_matrix
import matplotlib.pyplot as plt

# import config_BDT as config
import preselections

def make_model(input_dim):
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(input_dim,)),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(1, activation="sigmoid")
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="binary_crossentropy",
        metrics=[
            tf.keras.metrics.AUC(name="auc"),
            tf.keras.metrics.BinaryAccuracy(name="accuracy")
        ]
    )
    return model


def plot_and_save(y_true, y_score, outdir):
    fpr, tpr, _ = roc_curve(y_true, y_score)
    auc = roc_auc_score(y_true, y_score)

    plt.figure(figsize=(7, 6))
    plt.plot(fpr, tpr, lw=2, label=f"ROC AUC = {auc:.4f}")
    plt.plot([0, 1], [0, 1], "--", color="gray")
    plt.xlabel("Background efficiency")
    plt.ylabel("Signal efficiency")
    plt.title("DNN ROC curve")
    plt.legend(loc="lower right")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "roc_curve.png"), dpi=200)
    plt.close()

    plt.figure(figsize=(7, 6))
    plt.hist(y_score[y_true == 1], bins=50, histtype="step", density=True, label="Signal", linewidth=2)
    plt.hist(y_score[y_true == 0], bins=50, histtype="step", density=True, label="Background", linewidth=2)
    plt.xlabel("DNN score")
    plt.ylabel("Normalized entries")
    plt.title("DNN score distribution")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "score_distribution.png"), dpi=200)
    plt.close()

    return fpr, tpr, auc

def alt_to_rdf(expr):
    # Replace Alt$( X[n], d ) with (X.size() > n ? X[n] : d)
    return re.sub(
        r'Alt\$\(\s*([A-Za-z0-9_]+)\s*\[\s*(\d+)\s*\]\s*,\s*([^\)]+)\)',
        r'(\1.size() > \2 ? \1[\2] : \3)',
        expr
    )

def build_dataframe(files, branches, cut_expr, label):
    dfs = []
    for f in files:
        df = RDataFrame("Events", f) # Reference - https://root.cern/doc/master/classROOT_1_1RDataFrame.html
        # if cut_expr and str(cut_expr).strip():
        #     cut_expr_rdf = alt_to_rdf(cut_expr)
        #     df = df.Filter(cut_expr_rdf) # Filter rows based on user-defined conditions
        #     # a C++ expression is passed to the Filter() operation as a string, even if we call the method from Python. 
        # cols = list(branches)
        # Define scalar columns for array branches
        df = df.Define("CleanJet_pt_0", "CleanJet_pt.size() > 0 ? CleanJet_pt[0] : 0")
        df = df.Define("Lepton_pt_0", "Lepton_pt.size() > 0 ? Lepton_pt[0] : 0")
        df = df.Define("Lepton_pt_1", "Lepton_pt.size() > 1 ? Lepton_pt[1] : 0")
        df = df.Define("Lepton_pt_2", "Lepton_pt.size() > 2 ? Lepton_pt[2] : 0")
        if cut_expr and str(cut_expr).strip():
            cut_expr_rdf = alt_to_rdf(cut_expr)
            df = df.Filter(cut_expr_rdf)
        # Use the defined scalar columns
        cols = [
            "CleanJet_pt_0",
            "ZH3l_dphilmetjj",
            "PuppiMET_pt",
            "Lepton_pt_0",
            "Lepton_pt_1",
            "Lepton_pt_2"
        ]
        rdf = df.AsNumpy(cols) # AsNumpy returns the columns of RDataFrame as a dict of numpy arrays
        arr = np.column_stack([rdf[c] for c in cols])
        y = np.full((arr.shape[0], 1), label, dtype=np.int32) # the full function returns a new array of a given shape and data type, entirely filled with a specified value.
        dfs.append((arr, y))
    if not dfs:
        return np.empty((0, len(branches))), np.empty((0, 1), dtype=np.int32)
    X = np.concatenate([d[0] for d in dfs], axis=0)
    y = np.concatenate([d[1] for d in dfs], axis=0)
    return X, y

# Setup Tensorflow algorithm
def runJob_TF(output_and_dataset_name=""):
    outdir = f"dataset{output_and_dataset_name}"
    os.makedirs(outdir, exist_ok=True)

    # Load data
    Xs, ys = [], []
    branches = list(config_mvaVariables_TF)
    cuts = str(config_cut)
    for sample_name, sample in samples.items():
        isData = structure[sample_name]["isData"]
        # Don't train on data
        if (isinstance(isData, int) and isData == 1) or (not isinstance(isData, int) and "all" in isData):
            continue
        # Create file list
        files = []
        for entry in sample["name"]:
            if isinstance(entry, (list, tuple)) and len(entry) >= 2: # translated from TMVA config file line 'for name, *location_weights in sample['name']:'
                locations = entry[1]
                for loc in locations:
                    files.append(loc)
        
        if len(files) == 0:
            continue
        label = 1 if structure[sample_name]["isSignal"] == 1 else 0
        X, y = build_dataframe(files, branches, cuts, label)
        if X.shape[0] > 0:
            Xs.append(X)
            ys.append(y)

    if not Xs:
        raise RuntimeError("No training data found. Check samples and file paths.")

    X = np.concatenate(Xs, axis=0).astype(np.float32)
    y = np.concatenate(ys, axis=0).astype(np.int32).reshape(-1)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler() # ensures that each feature has zero mean and unit variance
    X_train = scaler.fit_transform(X_train)
    # StandardScaler strictly uses the mean and variance calculated from the training data to transform both the training and testing datasets. It doesn't calculate new statistics for testing data, even if the testing data has different upper and lower limits -> comes with risk of data leakage, out-of-boud values, etc.
    X_test = scaler.transform(X_test)

    np.save(os.path.join(outdir, "feature_names.npy"), np.array(branches, dtype=object))
    np.save(os.path.join(outdir, "X_train.npy"), X_train)
    np.save(os.path.join(outdir, "X_test.npy"), X_test)
    np.save(os.path.join(outdir, "y_train.npy"), y_train)
    np.save(os.path.join(outdir, "y_test.npy"), y_test)

    model = make_model(X_train.shape[1])

    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_auc",
            patience=20,
            mode="max",
            restore_best_weights=True
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.5,
            patience=10,
            min_lr=1e-6
        ),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=os.path.join(outdir, "best_model.keras"),
            monitor="val_auc",
            mode="max",
            save_best_only=True
        )
    ]

    history = model.fit(
        X_train, y_train,
        validation_split=0.2,
        epochs=500,
        batch_size=1024,
        callbacks=callbacks,
        verbose=2
    )

    model.save(os.path.join(outdir, "final_model.keras"))

    y_score = model.predict(X_test, batch_size=4096).reshape(-1)
    y_pred = (y_score >= 0.5).astype(np.int32)

    acc = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_score)
    cm = confusion_matrix(y_test, y_pred)

    np.save(os.path.join(outdir, "y_score.npy"), y_score)

    metrics = {
        "accuracy": float(acc),
        "auc": float(auc),
        "confusion_matrix": cm.tolist(),
        "n_train": int(len(y_train)),
        "n_test": int(len(y_test)),
        "n_features": int(X_train.shape[1])
    }

    with open(os.path.join(outdir, "metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)

    hist = history.history
    np.savez(
        os.path.join(outdir, "training_history.npz"),
        loss=np.array(hist.get("loss", [])),
        val_loss=np.array(hist.get("val_loss", [])),
        auc=np.array(hist.get("auc", [])),
        val_auc=np.array(hist.get("val_auc", [])),
        accuracy=np.array(hist.get("accuracy", [])),
        val_accuracy=np.array(hist.get("val_accuracy", []))
    )

    fpr, tpr, roc_auc = plot_and_save(y_test, y_score, outdir)

    summary_path = os.path.join(outdir, "summary.txt")
    with open(summary_path, "w") as f:
        f.write(f"Accuracy: {acc:.6f}\n")
        f.write(f"AUC: {auc:.6f}\n")
        f.write(f"Train events: {len(y_train)}\n")
        f.write(f"Test events: {len(y_test)}\n")
        f.write(f"Features: {X_train.shape[1]}\n")
        f.write("Confusion matrix:\n")
        f.write(np.array2string(cm))

    print(f"Saved outputs to: {outdir}")
    print(f"Accuracy = {acc:.6f}")
    print(f"AUC = {auc:.6f}")

# Setup TMVA
def runJob_TMVA(output_and_dataset_name = ""):
    TMVA.Tools.Instance()
    # TMVA.PyMethodBase.PyInitialize()

    output = TFile.Open('TMVA{}.root'.format(output_and_dataset_name), 'RECREATE')
    factory = TMVA.Factory('TMVAClassification', output,'!V:!Silent:Color:DrawProgressBar:AnalysisType=Classification')
    # factory = TMVA.Factory('TMVAClassification', output,'!V:!Silent:Color:DrawProgressBar:Transformations=D,G:AnalysisType=Classification')

    dataloader = TMVA.DataLoader("dataset{}".format(output_and_dataset_name))

    for br in config_mvaVariables:
        dataloader.AddVariable(br)

    for sampleName, sample in samples.items():
        isData = structure[sampleName]['isData']
        if (isinstance(isData, int) and isData == 1) or (not isinstance(isData, int) and 'all' in isData):
            continue

        sample['tree'] = TChain("Events")
        print("Sample name: ", sampleName)
        for name, *location_weights in sample['name']:
            print("Sub-sample: ", name)
            locations = location_weights[0]
            # weights = location_weights[1] if len(location_weights) > 1 else None
            for loc in locations:
                print("file: ", loc)
                sample['tree'].Add(loc)

        if structure[sampleName]['isSignal']==1:
            dataloader.AddSignalTree(sample['tree'], 1.0)
        else:
            dataloader.AddBackgroundTree(sample['tree'], 1.0)
        # output_dim += 1
    # Reference: https://root.cern.ch/download/doc/tmva/TMVAUsersGuide.pdf
    # Train test dataset will contain less/equal events compared to signal and background trees. How these events are chosen is given by the next line. Event weights are given by Monte Carlo generators, and may turn out to be overall very small or large. To avoid artifacts due to this, TMVA can internally renormalise the signal and background training using NormMode.
    dataloader.PrepareTrainingAndTestTree(TCut(config_cut),'SplitMode=Random:NormMode=NumEvents:!V')
    # dataloader.PrepareTrainingAndTestTree(TCut(config.cut),'nTrain_Signal=100000:nTrain_Background=100000:SplitMode=Random:NormMode=NumEvents:!V')#SSSF
    # Table 25 in TMVA UG explains all parameters, but to summarize:
    # - NTrees: number of trees in forest, 
    # - nCuts: Number of grid points in variable range used in finding optimal cut in node splitting
    # - MaxDepth: maximum depth of a tree allowed
    # - MinNodeSize: Minimum percentage of training events required in a leaf node
    # - BoostType: Boosting algorithm, here Gradient boosting
    # - Shrinkage: learning rate
    # - UseBaggedBoost: use bagging (Bootstrap AGGregatING) ...
    factory.BookMethod(dataloader, TMVA.Types.kBDT, "gBDT_D2",   "!H:!V:NTrees=500:MinNodeSize=1.5%:BoostType=Grad:Shrinkage=0.05:UseBaggedBoost:GradBaggingFraction=0.5:nCuts=500:MaxDepth=2" )
    factory.BookMethod(dataloader, TMVA.Types.kBDT, "gBDT_D2_S01",   "!H:!V:NTrees=500:MinNodeSize=1.5%:BoostType=Grad:Shrinkage=0.01:UseBaggedBoost:GradBaggingFraction=0.5:nCuts=500:MaxDepth=2" )
    factory.BookMethod(dataloader, TMVA.Types.kBDT, "gBDT_D2_C300", "!H:!V:NTrees=500:MinNodeSize=1.5%:BoostType=Grad:Shrinkage=0.05:UseBaggedBoost:GradBaggingFraction=0.5:nCuts=300:MaxDepth=2" )
    factory.BookMethod(dataloader, TMVA.Types.kBDT, "gBDT_D3",   "!H:!V:NTrees=500:MinNodeSize=1.5%:BoostType=Grad:Shrinkage=0.05:UseBaggedBoost:GradBaggingFraction=0.5:nCuts=500:MaxDepth=3" )
    factory.BookMethod(dataloader, TMVA.Types.kBDT, "gBDT_D4",   "!H:!V:NTrees=500:MinNodeSize=1.5%:BoostType=Grad:Shrinkage=0.05:UseBaggedBoost:GradBaggingFraction=0.5:nCuts=500:MaxDepth=4" )
    factory.BookMethod(dataloader, TMVA.Types.kBDT, "gBDT_D5",   "!H:!V:NTrees=500:MinNodeSize=1.5%:BoostType=Grad:Shrinkage=0.05:UseBaggedBoost:GradBaggingFraction=0.5:nCuts=500:MaxDepth=5" )
    factory.BookMethod(dataloader, TMVA.Types.kBDT, "gBDT_D6",   "!H:!V:NTrees=500:MinNodeSize=1.5%:BoostType=Grad:Shrinkage=0.05:UseBaggedBoost:GradBaggingFraction=0.5:nCuts=500:MaxDepth=6" )
    # factory.BookMethod(dataloader, TMVA.Types.kBDT, "gBDT_D2_F07"    ,   "!H:!V:NTrees=500:MinNodeSize=1.5%:BoostType=Grad:Shrinkage=0.05:UseBaggedBoost:GradBaggingFraction=0.7:nCuts=500:MaxDepth=2" )
    # factory.BookMethod(dataloader, TMVA.Types.kBDT, "gBDT_D2_S01_F07",   "!H:!V:NTrees=500:MinNodeSize=1.5%:BoostType=Grad:Shrinkage=0.01:UseBaggedBoost:GradBaggingFraction=0.7:nCuts=500:MaxDepth=2" )
    # Run training, test and evaluation
    factory.TrainAllMethods()
    factory.TestAllMethods()
    factory.EvaluateAllMethods()

    output.Close()

if __name__ == "__main__":

    print("Input arguments: {}".format(sys.argv))
    framework = "TF" # or "TMVA"

    isDEV=False
    # Load configuration
    with open("configuration_BDT.py") as handle:
        exec(handle.read())  # Read the file content as a string
    samples={}
    structure={}
    cuts={}
    for f in [samplesFile, structureFile, cutsFile]:
        with open(f) as handle:
            exec(handle.read())

    # Reduce sample files for fast dev
    if isDEV:
        for sampleName, sample in samples.items():
            if sampleName not in ['DY', 'top', 'ttV', 'WW', 'Zg', 'ZgS', 'WZ', 'ZZ', 'VVV', 'ZH_hww','ggZH_hww','WH_hww','ttH_hww', 'ZH_htt', 'WH_htt', 'Fake_e', 'Fake_m']:
            # if sampleName not in ['Wg','Zg','WgS','ZgS','ZZ','WZ','top','DY','WH_hww_plus','WH_hww_minus','WH_htt_plus','WH_htt_minus']:
                samples.pop(sampleName)
                continue

    # Define data to be loaded
    with open("./preselections.py") as handle:
        exec(handle.read())

    config_cut="(({0}) && ({1}))".format(cuts['NONE'],preselections['ALL'])

    config_mvaVariables = [
    'Alt$( CleanJet_pt[0], 0)',
    'ZH3l_dphilmetjj',
    'PuppiMET_pt',
    'Alt$( Lepton_pt[0], 0)',
    'Alt$( Lepton_pt[1], 0)',
    'Alt$( Lepton_pt[2], 0)'
    ]

    config_mvaVariables_TF = [
        "CleanJet_pt_0",
        "ZH3l_dphilmetjj",
        "PuppiMET_pt",
        "Lepton_pt_0",
        "Lepton_pt_1",
        "Lepton_pt_2"
    ]

    if len(sys.argv) > 1:
        print("Suffix is: {}".format(sys.argv[1]))
        output_and_dataset = sys.argv[1]
        if framework == "TF":
            runJob_TF(output_and_dataset)
        elif framework == "TMVA":
            runJob(output_and_dataset)
        os.system("mv dataset dataset{}".format(output_and_dataset))
    else:
        print("No suffix, running with standard output name")
        if framework == "TF":
            runJob_TF()
        elif framework == "TMVA":
            runJob()
