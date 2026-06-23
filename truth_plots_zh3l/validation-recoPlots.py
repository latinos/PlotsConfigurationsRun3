import ROOT
import math
import glob
import os
import argparse
import numpy as np
from mkShapesRDF.lib.search_files import SearchFiles
searchFiles = SearchFiles()

def invariant_mass(p4s):
    total = ROOT.TLorentzVector()
    for p4 in p4s:
        total += p4
    return total.M()

def get_lepton_p4(pt, eta, phi, mass):
    p4 = ROOT.TLorentzVector()
    p4.SetPtEtaPhiM(pt, eta, phi, mass)
    return p4

def get_jet_p4(pt, eta, phi, mass):
    p4 = ROOT.TLorentzVector()
    p4.SetPtEtaPhiM(pt, eta, phi, mass)
    return p4

def deltaPhi(phi1, phi2):
    dphi = phi1 - phi2
    while dphi > math.pi: dphi -= 2*math.pi
    while dphi < -math.pi: dphi += 2*math.pi
    return abs(dphi)

def w_transverse_mass(pt_lep, phi_lep, met, met_phi):
    dphi = deltaPhi(phi_lep, met_phi)
    return math.sqrt(2 * pt_lep * met * (1 - math.cos(dphi)))

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
Whad_recoMethodology = 'normal' # 'normal' or 'refined'
FROM_HARD_PROCESS = 8
IS_FIRST_COPY = 12
w_mass = 80.4  # W boson mass in GeV
z_mass = 91.1876  # Z boson mass in GeV

mcDirectory   = makeMCDirectory()
samples = ["GluGluZH_Zto2L_Hto2WtoLNu2Q", "ZH_Zto2L_Hto2WtoLNu2Q", "WZ"]
cutflow_vs_sample = {}    

for sample in samples:
    save_dir = mcDirectory + "/" + str(sample)+'_results/'
    cutflow_full_sample = np.zeros(7) # Total number of events, after preselections, low-mass resonance, z mass selection, Zg veto, jet preselection, signal region.
    with ROOT.TFile(str(save_dir)+"/reco_plots_"+str(Whad_recoMethodology)+"WHadReco.root", "RECREATE") as out:
        if not os.path.isdir(save_dir):
            os.makedirs(save_dir)
        if not os.path.isdir(input_dir):
            raise FileNotFoundError(f"The directory '{input_dir}' does not exist.")
        
        # Baseline kinematic histograms for leptons and jets
        h_nLeps = ROOT.TH1F("h_nLeps", "Reco # leptons, pT> 10 (no other sel); n_{L}; Events", 20, 0, 20)
        h_E_lep1 = ROOT.TH1F("h_E_lep1", "Reco Lep1 E;E [GeV];Events", 100, 0, 200)
        h_E_lep2 = ROOT.TH1F("h_E_lep2", "Reco Lep2 E;E [GeV];Events", 100, 0, 200)
        h_E_lep3 = ROOT.TH1F("h_E_lep3", "Reco Lep3 E;E [GeV];Events", 100, 0, 200)
        h_pT_lep1 = ROOT.TH1F("h_pT_lep1", "Reco Lep1 pT;pT [GeV];Events", 100, 0, 200)
        h_pT_lep2 = ROOT.TH1F("h_pT_lep2", "Reco Lep2 pT;pT [GeV];Events", 100, 0, 200)
        h_pT_lep3 = ROOT.TH1F("h_pT_lep3", "Reco Lep3 pT;pT [GeV];Events", 100, 0, 200)
        h_pz_lep1 = ROOT.TH1F("h_pZ_lep1", "Reco Lep1 pZ;pZ [GeV];Events", 100, 0, 200)
        h_pz_lep2 = ROOT.TH1F("h_pZ_lep2", "Reco Lep2 pZ;pZ [GeV];Events", 100, 0, 200)
        h_pz_lep3 = ROOT.TH1F("h_pZ_lep3", "Reco Lep3 pZ;pZ [GeV];Events", 100, 0, 200)
        h_nJets = ROOT.TH1F("h_nJets", "Reco # jets, pT>30, eta<4.7 (no other sel); n_{j}; Events", 20, 0, 20)
        h_E_jet1 = ROOT.TH1F("h_E_Jet1", "Reco Jet1 E;E [GeV];Events", 100, 0, 200)
        h_E_jet2 = ROOT.TH1F("h_E_Jet2", "Reco Jet2 E;E [GeV];Events", 100, 0, 200)
        h_pT_jet1 = ROOT.TH1F("h_pT_Jet1", "Reco Jet1 pT;pT [GeV];Events", 100, 0, 200)
        h_pT_jet2 = ROOT.TH1F("h_pT_Jet2", "Reco Jet2 pT;pT [GeV];Events", 100, 0, 200)
        h_pz_jet1 = ROOT.TH1F("h_pZ_Jet1", "Reco Jet1 pZ;pZ [GeV];Events", 100, 0, 200)
        h_pz_jet2 = ROOT.TH1F("h_pZ_Jet2", "Reco Jet2 pZ;pZ [GeV];Events", 100, 0, 200)
        h_eTmiss = ROOT.TH1F("h_eTmiss", "Reco MET;E_{T}^{miss} [GeV];Events", 100, 0, 200)
        # h_nLepWdecay = ROOT.TH1F("h_nLepWdecay", "Reconstructed number of leptons from Reco W;nLeptons_{W};Events", 10, 0, 1)
        
        # Histograms for W and Z mass, and angles between W-W and Z-H
        # h_Hmass = ROOT.TH1F("h_Hmass", "H mass;Mass [GeV];Events", 100, 0, 200)
        h_Hmass_T = ROOT.TH1F("h_Hmass_T", "Reconstructed Higgs transverse mass; m^{H}_{T} [GeV]; Events", 60, 0, 600)
        h_Zmass = ROOT.TH1F("h_Zmass", "Reconstructed Z mass; m_{LL} [GeV]; Events", 60, 60, 120)
        h_Whadmass = ROOT.TH1F("h_Whadmass", "Reconstructed hadronic W mass; m_{jj} [GeV]; Events", 50, 0, 500)
        h_Wlepmass_T = ROOT.TH1F("h_Wlepmass", "Reconstructed leptonic W transverse mass; m^{LNu}_{T} [GeV]; Events", 50, 0, 200)
        h_angle_WW = ROOT.TH1F("h_angle_WW", "Angle between Ws;Angle [rad];Events", 64, 0, math.pi)
        h_dPhi_WW = ROOT.TH1F("h_dPhi_WW", "Phi angle between Ws;Angle [rad];Events", 64, 0, math.pi)
        h_angle_ZH = ROOT.TH1F("h_angle_ZH", "Angle between Z and H;Angle [rad];Events", 64, 0, math.pi)
        h_dPhi_ZH = ROOT.TH1F("h_dPhi_ZH", "Phi angle between Z and H;Angle [rad];Events", 64, 0, math.pi)

        n_Z_candidates = 0
        n_W_lep_candidates = 0
        n_W_had_candidates = 0
        n_H_candidates = 0

        root_files = nanoGetSampleFiles(mcDirectory, sample)[0][1]
        print(f"Found ROOT files ({root_files}) in {input_dir} for sample {sample}.")
        # root_files = glob.glob(os.path.join(input_dir, "*.root"))
        for root_file_iter, root_file_name in enumerate(root_files):
            cutflow_full_file = np.zeros(7)
            if root_file_iter % 10 == 0:
                print(f"Processing file {root_file_iter + 1}/{len(root_files)}: {root_file_name}")
            f = ROOT.TFile.Open(root_file_name)
            tree = f.Get("Events")
            for event in tree:
                cutflow_full_file[0] += 1 # Total events
                Z_candidate = None
                phi_H_candidate = None
                # --- Lepton selection (as in your table) ---
                leptons = []
                for i in range(event.nElectron):
                    # if event.Electron_pt[i] > 25 and abs(event.Electron_eta[i]) < 2.5:
                    leptons.append({'pt': event.Electron_pt[i], 'eta': event.Electron_eta[i], 'phi': event.Electron_phi[i], 'mass': 0.000511, 'charge': event.Electron_charge[i], 'pdgId': 11})
                for i in range(event.nMuon):
                    # if event.Muon_pt[i] > 15 and abs(event.Muon_eta[i]) < 2.4:
                    leptons.append({'pt': event.Muon_pt[i], 'eta': event.Muon_eta[i], 'phi': event.Muon_phi[i], 'mass': 0.105, 'charge': event.Muon_charge[i], 'pdgId': 13})
                leptons = sorted(leptons, key=lambda x: -x['pt'])
                n_leptons = sorted([lep for lep in leptons if lep['pt'] > 10], key=lambda x: -x['pt'])
                h_nLeps.Fill(len(n_leptons))
                if len(leptons) < 3: continue
                if leptons[0]['pt'] < 25 or leptons[1]['pt'] < 20 or leptons[2]['pt'] < 15: continue
                if len(leptons) > 3 and leptons[3]['pt'] > 10: continue
                if abs(sum([lep['charge'] for lep in leptons[0:3]])) != 1: continue # If there's a 4th lepton with pT<10 then we need to check the charge sum of the leading 3 leptons
                cutflow_full_file[1] += 1 # After lepton pre-selections
                # Min(mll) > 12 for all lepton pairs
                pass_mll = True
                for i in range(len(leptons)):
                    for j in range(i+1, len(leptons)):
                        l1 = get_lepton_p4(leptons[i]['pt'], leptons[i]['eta'], leptons[i]['phi'], leptons[i]['mass'])
                        l2 = get_lepton_p4(leptons[j]['pt'], leptons[j]['eta'], leptons[j]['phi'], leptons[j]['mass'])
                        if (l1 + l2).M() < 12:
                            pass_mll = False
                if not pass_mll: continue
                cutflow_full_file[2] += 1 # After low-mass resonance veto

                # --- Z candidate: OSSF pair with |mll - mZ| < 25 ---
                zcands = []
                for i in range(len(leptons)):
                    for j in range(i+1, len(leptons)):
                        if leptons[i]['pdgId'] != leptons[j]['pdgId']: continue
                        if leptons[i]['charge'] * leptons[j]['charge'] > 0: continue
                        l1 = get_lepton_p4(leptons[i]['pt'], leptons[i]['eta'], leptons[i]['phi'], leptons[i]['mass'])
                        l2 = get_lepton_p4(leptons[j]['pt'], leptons[j]['eta'], leptons[j]['phi'], leptons[j]['mass'])
                        mll = (l1 + l2).M()
                        if abs(mll - z_mass) < 25:
                            zcands.append((i, j, mll))
                if len(zcands) == 0: continue
                cutflow_full_file[3] += 1 # After Z mass window selection
                zcand = min(zcands, key=lambda x: abs(x[2] - z_mass))
                z_leptons = [leptons[zcand[0]], leptons[zcand[1]]]
                h_pT_lep1.Fill(z_leptons[0]['pt'])
                h_pT_lep2.Fill(z_leptons[1]['pt'])
                h_pz_lep1.Fill(get_lepton_p4(z_leptons[0]['pt'], z_leptons[0]['eta'], z_leptons[0]['phi'], z_leptons[0]['mass']).Pz())
                h_pz_lep2.Fill(get_lepton_p4(z_leptons[1]['pt'], z_leptons[1]['eta'], z_leptons[1]['phi'], z_leptons[1]['mass']).Pz())
                h_E_lep1.Fill(get_lepton_p4(z_leptons[0]['pt'], z_leptons[0]['eta'], z_leptons[0]['phi'], z_leptons[0]['mass']).E())
                h_E_lep2.Fill(get_lepton_p4(z_leptons[1]['pt'], z_leptons[1]['eta'], z_leptons[1]['phi'], z_leptons[1]['mass']).E())
                h_Zmass.Fill(zcand[2])
                Z_candidate = get_lepton_p4(z_leptons[0]['pt'], z_leptons[0]['eta'], z_leptons[0]['phi'], z_leptons[0]['mass']) + get_lepton_p4(z_leptons[1]['pt'], z_leptons[1]['eta'], z_leptons[1]['phi'], z_leptons[1]['mass'])
                n_Z_candidates += 1

                # # --- b-jet veto ---
                # has_bjet = False
                # for i in range(event.nJet):
                #     if event.Jet_pt[i] > 20 and event.Jet_btagDeepB[i] > 0.4184:
                #         has_bjet = True
                # if has_bjet: continue

                # --- Zγ veto: |m3l - mZ| > 20 GeV ---
                third_lepton = [lep for k, lep in enumerate(leptons) if k not in [zcand[0], zcand[1]]][0] # Highest pT lepton that is not part of the Z candidate
                h_pT_lep3.Fill(third_lepton['pt'])
                h_pz_lep3.Fill(get_lepton_p4(third_lepton['pt'], third_lepton['eta'], third_lepton['phi'], third_lepton['mass']).Pz())
                h_E_lep3.Fill(get_lepton_p4(third_lepton['pt'], third_lepton['eta'], third_lepton['phi'], third_lepton['mass']).E())
                
                l3_p4 = get_lepton_p4(third_lepton['pt'], third_lepton['eta'], third_lepton['phi'], third_lepton['mass'])
                z1_p4 = get_lepton_p4(z_leptons[0]['pt'], z_leptons[0]['eta'], z_leptons[0]['phi'], z_leptons[0]['mass'])
                z2_p4 = get_lepton_p4(z_leptons[1]['pt'], z_leptons[1]['eta'], z_leptons[1]['phi'], z_leptons[1]['mass'])
                m3l = (z1_p4 + z2_p4 + l3_p4).M()
                if abs(m3l - z_mass) < 20: continue
                cutflow_full_file[4] += 1 # After Zγ veto

                # --- Jet selection ---
                jets = []
                for i in range(event.nJet):
                    if event.Jet_pt[i] > 30 and abs(event.Jet_eta[i]) < 4.7:
                        jets.append({'pt': event.Jet_pt[i], 'eta': event.Jet_eta[i], 'phi': event.Jet_phi[i], 'mass': event.Jet_mass[i]})
                h_nJets.Fill(len(jets))
                jets = sorted(jets, key=lambda x: -x['pt']) # Sort jets by descending pT

                # --- Signal region selection ---
                signal_region = False
                selected_w_pair = None
                if len(jets) == 1:
                    cutflow_full_file[5] += 1 # After jet preselection for 1-jet category
                    # Δφ(l + MET, j) < π/2
                    l_met_px = third_lepton['pt']*math.cos(third_lepton['phi']) + event.MET_pt*math.cos(event.MET_phi)
                    l_met_py = third_lepton['pt']*math.sin(third_lepton['phi']) + event.MET_pt*math.sin(event.MET_phi)
                    l_met_phi = math.atan2(l_met_py, l_met_px)
                    dphi = deltaPhi(l_met_phi, jets[0]['phi'])
                    if dphi < math.pi/2:
                        signal_region = True
                        selected_w_pair = (0,)  # Mark single jet as W candidate
                elif len(jets) >= 2:
                    cutflow_full_file[5] += 1 # After jet preselection for 2-jet category
                    if Whad_recoMethodology == 'refined':
                        # Generate all possible dijet pairs and compute |m_jj - 80.4|
                        dijet_pairs = []
                        for i in range(len(jets)):
                            for j in range(i+1, len(jets)):
                                jet1_p4 = get_jet_p4(jets[i]['pt'], jets[i]['eta'], jets[i]['phi'], jets[i]['mass'])
                                jet2_p4 = get_jet_p4(jets[j]['pt'], jets[j]['eta'], jets[j]['phi'], jets[j]['mass'])
                                m_jj = (jet1_p4 + jet2_p4).M()
                                dijet_pairs.append({
                                    'i': i, 'j': j, 
                                    'dm': abs(m_jj - w_mass), 
                                    'phi_jj': math.atan2(
                                        jets[i]['pt']*math.sin(jets[i]['phi']) + jets[j]['pt']*math.sin(jets[j]['phi']),
                                        jets[i]['pt']*math.cos(jets[i]['phi']) + jets[j]['pt']*math.cos(jets[j]['phi']))
                                    })
                        
                        # Sort dijet pairs by proximity to W mass (smallest dm first)
                        dijet_pairs = sorted(dijet_pairs, key=lambda x: x['dm'])
                        
                        # Check pairs in order of ascending dm
                        for pair in dijet_pairs:
                            # Calculate Δφ(l+MET, dijet system)
                            l_met_px = third_lepton['pt']*math.cos(third_lepton['phi']) + event.MET_pt*math.cos(event.MET_phi)
                            l_met_py = third_lepton['pt']*math.sin(third_lepton['phi']) + event.MET_pt*math.sin(event.MET_phi)
                            l_met_phi = math.atan2(l_met_py, l_met_px)
                            dphi = deltaPhi(l_met_phi, pair['phi_jj'])
                            
                            if dphi < math.pi/2:
                                signal_region = True
                                selected_w_pair = (pair['i'], pair['j'])
                                break  # Use first valid pair
                        
                        if not signal_region:
                            # hist_nWZcandidates.Fill(1)
                            continue  # Skip event if no valid pairs
                    if Whad_recoMethodology == 'normal':
                        # Selecting 2 leading pT jets as the hadronic W decay products 
                        # Δφ(l + MET, jj) < π/2
                        px_jj = jets[0]['pt']*math.cos(jets[0]['phi']) + jets[1]['pt']*math.cos(jets[1]['phi'])
                        py_jj = jets[0]['pt']*math.sin(jets[0]['phi']) + jets[1]['pt']*math.sin(jets[1]['phi'])
                        phi_jj = math.atan2(py_jj, px_jj)
                        l_met_px = third_lepton['pt']*math.cos(third_lepton['phi']) + event.MET_pt*math.cos(event.MET_phi)
                        l_met_py = third_lepton['pt']*math.sin(third_lepton['phi']) + event.MET_pt*math.sin(event.MET_phi)
                        l_met_phi = math.atan2(l_met_py, l_met_px)
                        dphi = deltaPhi(l_met_phi, phi_jj)
                        if dphi < math.pi/2:
                            signal_region = True
                            selected_w_pair = (0, 1)  # Mark leading two jets as W candidates


                if not signal_region:
                    continue 
                cutflow_full_file[6] += 1 # After signal region selection
                # --- W (leptonic) reconstruction ---
                lep_p4 = get_lepton_p4(third_lepton['pt'], third_lepton['eta'], third_lepton['phi'], third_lepton['mass'])
                nu_p4 = ROOT.TLorentzVector()
                nu_p4.SetPtEtaPhiM(event.MET_pt, 0, event.MET_phi, 0)
                w_lep_mass = (lep_p4 + nu_p4).M()
                w_lep_mt = w_transverse_mass(third_lepton['pt'], third_lepton['phi'], event.MET_pt, event.MET_phi)
                h_Wlepmass_T.Fill(w_lep_mt)
                n_W_lep_candidates += 1

                # --- W (hadronic) reconstruction ---
                had_w_p4 = None

                if len(jets) == 1:
                    # 1-jet signal region: the jet is the hadronic W, if Δφ(l + MET, j) > π/2 then the prior IF statement would not have passed
                    had_w_p4 = get_jet_p4(jets[0]['pt'], jets[0]['eta'], jets[0]['phi'], jets[0]['mass'])
                    h_Whadmass.Fill(had_w_p4.M())
                    h_pT_jet1.Fill(jets[0]['pt'])
                    h_pz_jet1.Fill(get_jet_p4(jets[0]['pt'], jets[0]['eta'], jets[0]['phi'], jets[0]['mass']).Pz())
                    h_E_jet1.Fill(get_jet_p4(jets[0]['pt'], jets[0]['eta'], jets[0]['phi'], jets[0]['mass']).E())
                    n_W_had_candidates += 1

                elif len(jets) >= 2 and selected_w_pair is not None:
                    # 2-jet signal region:
                    i, j = selected_w_pair
                    had_w_p4 = get_jet_p4(jets[i]['pt'], jets[i]['eta'], jets[i]['phi'], jets[i]['mass']) + get_jet_p4(jets[j]['pt'], jets[j]['eta'], jets[j]['phi'], jets[j]['mass'])
                    h_Whadmass.Fill(had_w_p4.M())
                    h_pT_jet1.Fill(jets[i]['pt'])
                    h_pT_jet2.Fill(jets[j]['pt'])
                    h_pz_jet1.Fill(get_jet_p4(jets[i]['pt'], jets[i]['eta'], jets[i]['phi'], jets[i]['mass']).Pz())
                    h_pz_jet2.Fill(get_jet_p4(jets[j]['pt'], jets[j]['eta'], jets[j]['phi'], jets[j]['mass']).Pz())
                    h_E_jet1.Fill(get_jet_p4(jets[i]['pt'], jets[i]['eta'], jets[i]['phi'], jets[i]['mass']).E())
                    h_E_jet2.Fill(get_jet_p4(jets[j]['pt'], jets[j]['eta'], jets[j]['phi'], jets[j]['mass']).E())
                    n_W_had_candidates += 1

                if had_w_p4 is not None:
                    phi_W_lep = lep_p4.Phi()
                    phi_W_had = had_w_p4.Phi()
                    h_dPhi_WW.Fill(deltaPhi(phi_W_lep, phi_W_had))
                    # Visible system: lepton + hadronic W
                    vis_p4 = lep_p4 + had_w_p4
                    m_vis = vis_p4.M()
                    pt_vis = vis_p4.Pt()
                    px_vis = vis_p4.Px()
                    py_vis = vis_p4.Py()
                    px_miss = event.MET_pt * math.cos(event.MET_phi)
                    py_miss = event.MET_pt * math.sin(event.MET_phi)
                    et_vis = math.sqrt(m_vis**2 + pt_vis**2)
                    et_miss = event.MET_sumEt #event.MET_pt
                    mt2 = (et_vis + et_miss)**2 - ((px_vis + px_miss)**2 + (py_vis + py_miss)**2)
                    mt_higgs = math.sqrt(mt2) if mt2 > 0 else 0.
                    h_Hmass_T.Fill(mt_higgs)
                    n_H_candidates += 1
                    px_higgs = px_vis + px_miss
                    py_higgs = py_vis + py_miss
                    phi_H_candidate = math.atan2(py_higgs, px_higgs)

                if Z_candidate is None or phi_H_candidate is None:
                    continue
                phi_Z = Z_candidate.Phi()
                h_dPhi_ZH.Fill(deltaPhi(phi_Z, phi_H_candidate))
            f.Close()
            cutflow_full_sample += cutflow_full_file
        # # Create output file and histograms
        # out = ROOT.TFile(str(save_dir)+"/reco_plots.root", "RECREATE")
        # out.Close()
        out.Write()
    cutflow_vs_sample[sample] = cutflow_full_sample
    print(f"Number of Z candidates: {n_Z_candidates}")
    print(f"Number of leptonic W candidates: {n_W_lep_candidates}")
    print(f"Number of hadronic W candidates: {n_W_had_candidates}")
    print(f"Number of H candidates: {n_H_candidates}")
    print("Histograms saved to reco_plots.root")
