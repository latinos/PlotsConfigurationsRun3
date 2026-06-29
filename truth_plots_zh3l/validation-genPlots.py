import ROOT
import math
import glob
import os
import argparse
from mkShapesRDF.lib.search_files import SearchFiles
searchFiles = SearchFiles()

def invariant_mass(p4s):
    total = ROOT.TLorentzVector()
    for p4 in p4s:
        total += p4
    return total.M()

def angle_bw_vectors(v1, v2):
    return v1.Angle(v2.Vect())

def nanoGetSampleFiles(path, name):
    _files = searchFiles.searchFiles(path, name, redirector=redirector)
    if limitFiles != -1 and len(_files) > limitFiles:
        return [(name, _files[:limitFiles])]
    else:
        return [(name, _files)]

def makeMCDirectory(var=""):
    _treeBaseDir = treeBaseDir + ""
    if redirector != "":
        _treeBaseDir = redirector + treeBaseDir
    if var == "":
        return "/".join([_treeBaseDir, mcProduction, mcSteps])
    else:
        return "/".join([_treeBaseDir, mcProduction, mcSteps + "__" + var])

parser = argparse.ArgumentParser(description="Process NanoAOD ROOT files.")
parser.add_argument("--i", type=str, default='/eos/user/d/dshekar/MCsamplesForBDTzh3l', help="Path to the directory containing NanoAOD ROOT files.")
args = parser.parse_args()

input_dir = args.i
print(f"Input directory set to: {input_dir}")
redirector = ""
mcProduction = 'Summer22EE_130x_nAODv12_Full2022v12'
mcSteps      = 'MCl2loose2022EEv12__MCCorr2022EEv12JetScaling__l2tight'
treeBaseDir = input_dir #f'/eos/user/d/dshekar/MCsamplesForBDTzh3l'
limitFiles = -1

FROM_HARD_PROCESS = 8
IS_FIRST_COPY = 12

mcDirectory   = makeMCDirectory()
samples = ["GluGluZH_Zto2L_Hto2WtoLNu2Q", "ZH_Zto2L_Hto2WtoLNu2Q"]

for sample in samples:
    save_dir = mcDirectory + "/" + str(sample)+'_results/'
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    if not os.path.isdir(input_dir):
        raise FileNotFoundError(f"The directory '{input_dir}' does not exist.")
    
    # Baseline kinematic histograms for leptons and jets
    h_E_lep1 = ROOT.TH1F("h_E_lep1", "Gen Lep1 E;E [GeV];Events", 100, 0, 200)
    h_E_lep2 = ROOT.TH1F("h_E_lep2", "Gen Lep2 E;E [GeV];Events", 100, 0, 200)
    h_E_lep3 = ROOT.TH1F("h_E_lep3", "Gen Lep3 E;E [GeV];Events", 100, 0, 200)
    h_pT_lep1 = ROOT.TH1F("h_pT_lep1", "Gen Lep1 pT;pT [GeV];Events", 100, 0, 200)
    h_pT_lep2 = ROOT.TH1F("h_pT_lep2", "Gen Lep2 pT;pT [GeV];Events", 100, 0, 200)
    h_pT_lep3 = ROOT.TH1F("h_pT_lep3", "Gen Lep3 pT;pT [GeV];Events", 100, 0, 200)
    h_pz_lep1 = ROOT.TH1F("h_pZ_lep1", "Gen Lep1 pZ;pZ [GeV];Events", 100, 0, 200)
    h_pz_lep2 = ROOT.TH1F("h_pZ_lep2", "Gen Lep2 pZ;pZ [GeV];Events", 100, 0, 200)
    h_pz_lep3 = ROOT.TH1F("h_pZ_lep3", "Gen Lep3 pZ;pZ [GeV];Events", 100, 0, 200)
    h_E_jet1 = ROOT.TH1F("h_E_Jet1", "Gen Jet1 E;E [GeV];Events", 100, 0, 200)
    h_E_jet2 = ROOT.TH1F("h_E_Jet2", "Gen Jet2 E;E [GeV];Events", 100, 0, 200)
    h_E_jet3 = ROOT.TH1F("h_E_Jet3", "Gen Jet3 E;E [GeV];Events", 100, 0, 200)
    h_pT_jet1 = ROOT.TH1F("h_pT_Jet1", "Gen Jet1 pT;pT [GeV];Events", 100, 0, 200)
    h_pT_jet2 = ROOT.TH1F("h_pT_Jet2", "Gen Jet2 pT;pT [GeV];Events", 100, 0, 200)
    h_pT_jet3 = ROOT.TH1F("h_pT_Jet3", "Gen Jet3 pT;pT [GeV];Events", 100, 0, 200)
    h_pz_jet1 = ROOT.TH1F("h_pZ_Jet1", "Gen Jet1 pZ;pZ [GeV];Events", 100, 0, 200)
    h_pz_jet2 = ROOT.TH1F("h_pZ_Jet2", "Gen Jet2 pZ;pZ [GeV];Events", 100, 0, 200)
    h_pz_jet3 = ROOT.TH1F("h_pZ_Jet3", "Gen Jet3 pZ;pZ [GeV];Events", 100, 0, 200)
    h_eTmiss = ROOT.TH1F("h_eTmiss", "Gen MET;E_{T}^{miss} [GeV];Events", 100, 0, 200)
    h_nLepWdecay = ROOT.TH1F("h_nLepWdecay", "nLep from Gen W decay;nLeptons;Events", 10, 0, 1)
    # Histograms for W and Z mass, and angles between W-W and Z-H
    h_Hmass = ROOT.TH1F("h_Hmass", "H mass;Mass [GeV];Events", 100, 0, 200)
    h_zmass = ROOT.TH1F("h_zmass", "Gen Z mass;Mass [GeV];Events", 100, 0, 200)
    h_angle_WW = ROOT.TH1F("h_angle_WW", "Angle between Ws;Angle [rad];Events", 64, 0, math.pi)
    h_dPhi_WW = ROOT.TH1F("h_dPhi_WW", "Phi angle between Ws;Angle [rad];Events", 64, 0, math.pi)
    h_angle_ZH = ROOT.TH1F("h_angle_ZH", "Angle between Z and H;Angle [rad];Events", 64, 0, math.pi)
    h_dPhi_ZH = ROOT.TH1F("h_dPhi_ZH", "Phi angle between Z and H;Angle [rad];Events", 64, 0, math.pi)

    n_H = 0
    n_W = 0
    n_WfromH = 0
    n_W_leptonic = 0
    n_W_hadronic = 0
    n_Z = 0
    n_Z_leptonic = 0
    n_Z_hadronic = 0

    root_files = nanoGetSampleFiles(mcDirectory, sample)[0][1]
    print(f"Found ROOT files ({root_files}) in {input_dir} for sample {sample}.")
    # root_files = glob.glob(os.path.join(input_dir, "*.root"))
    for root_file_iter, root_file_name in enumerate(root_files):
        if root_file_iter % 10 == 0:
            print(f"Processing file {root_file_iter + 1}/{len(root_files)}: {root_file_name}")
        file = ROOT.TFile.Open(root_file_name)
        tree = file.Get("Events")

        for event in tree:
            nGenPart = event.nGenPart
            pdgId = list(event.GenPart_pdgId)
            statusFlags = list(event.GenPart_statusFlags)
            pt = list(event.GenPart_pt)
            eta = list(event.GenPart_eta)
            phi = list(event.GenPart_phi)
            mass = list(event.GenPart_mass)
            motherIdx = list(event.GenPart_genPartIdxMother)

            w_candidates = []
            z_candidates = []
            h_candidates = []
            all_particles = []

            for i in range(nGenPart):
                flag = statusFlags[i]
                abs_pdg = abs(pdgId[i])
                p4 = ROOT.TLorentzVector()
                p4.SetPtEtaPhiM(pt[i], eta[i], phi[i], mass[i])
                all_particles.append((i, pdgId[i], motherIdx[i], p4))

                if not (flag & (1 << FROM_HARD_PROCESS)):
                    continue
                if not (flag & (1 << IS_FIRST_COPY)):
                    continue

                if abs_pdg == 25:
                    h_candidates.append((i, p4))
                    n_H += 1
                elif abs_pdg == 24:
                    w_candidates.append((i, p4, motherIdx[i], pdgId[i]))
                    n_W += 1
                elif abs_pdg == 23:
                    z_candidates.append((i, p4, motherIdx[i]))
                    n_Z += 1

            # ----------- Higgs -> WW -----------
            for i, w1, m1, pdg1 in w_candidates:
                for j, w2, m2, pdg2 in w_candidates:
                    if i >= j: continue
                    if m1 == m2 and m1 >= 0 and abs(pdgId[m1]) == 25:
                        # Fill mass and angle
                        h_Hmass.Fill(invariant_mass([w1, w2]))
                        n_WfromH += 1
                        h_angle_WW.Fill(angle_bw_vectors(w1, w2))
                        h_dPhi_WW.Fill(abs(w1.Phi() - w2.Phi()))

                        # For each W, check decay mode
                        for w_idx, w_p4, w_mother, w_pdg in [(i, w1, m1, pdg1), (j, w2, m2, pdg2)]:
                            # Find daughters of this W
                            daughters = [p for p in all_particles if p[2] == w_idx]
                            # Leptonic: has e, mu, tau daughter
                            if any(abs(d[1]) in [11,13,15] for d in daughters):
                                h_nLepWdecay.Fill(len([d for d in daughters if abs(d[1]) in [11,13,15]]))
                                n_W_leptonic += 1
                                h_pT_lep3.Fill(daughters[0][3].Pt())  # Assuming the first lepton
                                h_pz_lep3.Fill(daughters[0][3].Pz())
                                h_E_lep3.Fill(daughters[0][3].E())
                                # if len(daughters) > 1:
                                    # print("WARNING: More than one daughter found in (H->) W decay.")

                            # Hadronic: has quark daughter
                            elif any(abs(d[1]) in range(1,7) for d in daughters):
                                n_W_hadronic += 1
                                h_pT_jet1.Fill(daughters[0][3].Pt())  # Assuming the first jet
                                h_pz_jet1.Fill(daughters[0][3].Pz())
                                h_E_jet1.Fill(daughters[0][3].E())
                                h_pT_jet2.Fill(daughters[1][3].Pt())  # Assuming the second jet
                                h_pz_jet2.Fill(daughters[1][3].Pz())
                                h_E_jet2.Fill(daughters[1][3].E())
                                if len(daughters) > 2:
                                    print("WARNING: More than two daughters found in (H->) W decay.")
                                    h_pT_jet3.Fill(daughters[2][3].Pt())
                                    h_pz_jet3.Fill(daughters[2][3].Pz())
                                    h_E_jet3.Fill(daughters[2][3].E())
                        break  # Only one unique pair per event

            # ----------- Z -> ll or hadrons -----------
            # print(z_candidates)
            for i, z, m1 in z_candidates:
                # Find all daughters of this Z
                daughters = [p for p in all_particles if p[2] == i and abs(p[1]) != 23]
                # all_particles.append((i, pdgId[i], motherIdx[i], p4))
                # print(daughters)
                # Leptonic: at least one lepton daughter
                if any(abs(d[1]) in [11,13,15] for d in daughters):
                    n_Z_leptonic += 1
                    h_pT_lep1.Fill(daughters[0][3].Pt())  # Assuming the first lepton
                    h_pz_lep1.Fill(daughters[0][3].Pz())
                    h_E_lep1.Fill(daughters[0][3].E())
                    h_pT_lep2.Fill(daughters[1][3].Pt())  # Assuming the second lepton
                    h_pz_lep2.Fill(daughters[1][3].Pz())
                    h_E_lep2.Fill(daughters[1][3].E())
                    if len(daughters) > 2:
                        print("WARNING: More than two daughters found in Z decay.")
                # Hadronic: at least one quark daughter
                elif any(abs(d[1]) in range(1,7) for d in daughters):
                    n_Z_hadronic += 1

                # Try to find the Higgs in the same event for Z-H angle
                if h_candidates:
                    h_p4 = h_candidates[0][1]
                    h_angle_ZH.Fill(angle_bw_vectors(z, h_p4))
                    h_dPhi_ZH.Fill(abs(z.Phi() - h_p4.Phi()))

                # For mass plot, look for lepton pairs from this Z
                z_leptons = [d[3] for d in daughters if abs(d[1]) in [11,13,15]]
                if len(z_leptons) == 2:
                    h_zmass.Fill(invariant_mass(z_leptons))
        file.Close()
    # Create output file and histograms
    out = ROOT.TFile(str(save_dir)+"/gen_plots.root", "RECREATE")
    h_E_lep1.Write()
    h_E_lep2.Write()
    h_E_lep3.Write()
    h_pT_lep1.Write()
    h_pT_lep2.Write()
    h_pT_lep3.Write()
    h_pz_lep1.Write()
    h_pz_lep2.Write()
    h_pz_lep3.Write()
    h_E_jet1.Write()
    h_E_jet2.Write()
    h_E_jet3.Write()
    h_pT_jet1.Write()
    h_pT_jet2.Write()
    h_pT_jet3.Write()
    h_pz_jet1.Write()
    h_pz_jet2.Write()
    h_pz_jet3.Write()
    h_eTmiss.Write()
    h_nLepWdecay.Write()
    h_Hmass.Write()
    h_zmass.Write()
    h_angle_WW.Write()
    h_dPhi_WW.Write()
    h_angle_ZH.Write()
    h_dPhi_ZH.Write()
    out.Close()
    h_E_lep1.Reset()
    h_E_lep2.Reset()
    h_E_lep3.Reset()
    h_pT_lep1.Reset()
    h_pT_lep2.Reset()
    h_pT_lep3.Reset()
    h_pz_lep1.Reset()
    h_pz_lep2.Reset()
    h_pz_lep3.Reset()
    h_E_jet1.Reset()
    h_E_jet2.Reset()
    h_E_jet3.Reset()
    h_pT_jet1.Reset()
    h_pT_jet2.Reset()
    h_pT_jet3.Reset()
    h_pz_jet1.Reset()
    h_pz_jet2.Reset()
    h_pz_jet3.Reset()
    h_eTmiss.Reset()
    h_nLepWdecay.Reset()
    h_Hmass.Reset()
    h_zmass.Reset()
    h_angle_WW.Reset()
    h_dPhi_WW.Reset()
    h_angle_ZH.Reset()
    h_dPhi_ZH.Reset()
    print(f"Finished processing sample {sample}.")
    print(f'Total Higgs candidates: {n_H}, total W candidates: {n_W}')
    print(f'Total W candidates from H: {n_WfromH}\n Num of leptonic W decays: {n_W_leptonic}\n Num of hadronic W decays: {n_W_hadronic}')
    print(f'Total Z candidates: {n_Z}\n Num of leptonic Z decays: {n_Z_leptonic}\n Num of hadronic Z decays: {n_Z_hadronic}')
    print("Validation plots saved to validation_plots.root")
    print(f"Histograms saved to {str(save_dir)}/gen_plots.root")