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

parser = argparse.ArgumentParser(description="Process NanoAOD ROOT files.")
parser.add_argument("--i", type=str, default='/eos/user/d/dshekar/MCsamplesForBDTzh3l', help="Path to the directory containing NanoAOD ROOT files.")
args = parser.parse_args()

input_dir = args.i
print(f"Input directory set to: {input_dir}")
redirector = ""
mcProduction = 'Summer22EE_130x_nAODv12_Full2022v12'
mcSteps      = 'MCl2loose2022EEv12__MCCorr2022EEv12JetScaling__l2tight'
treeBaseDir = input_dir #f'/eos/user/d/dshekar/MCsamplesForBDTzh3l'
limitFiles = 1


def makeMCDirectory(var=""):
    _treeBaseDir = treeBaseDir + ""
    if redirector != "":
        _treeBaseDir = redirector + treeBaseDir
    if var == "":
        return "/".join([_treeBaseDir, mcProduction, mcSteps])
    else:
        return "/".join([_treeBaseDir, mcProduction, mcSteps + "__" + var])


mcDirectory   = makeMCDirectory()
samples = ["GluGluZH_Zto2L_Hto2WtoLNu2Q", "ZH_Zto2L_Hto2WtoLNu2Q"]

for sample in samples:
    save_dir = mcDirectory + "/" + str(sample)+'_results/'
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    if not os.path.isdir(input_dir):
        raise FileNotFoundError(f"The directory '{input_dir}' does not exist.")

    # Create output file and histograms
    out = ROOT.TFile(str(save_dir)+"/reco_plots_WhadDiJetSelection.root", "RECREATE")
    hist_nLeptons = ROOT.TH1F("hist_nLeptons", "Reconstructed number of leptons; n_{L}; Events", 20, 0, 20)
    hist_nJets = ROOT.TH1F("hist_nJets", "Reconstructed number of jets; n_{j}; Events", 20, 0, 20)
    hist_mZcandidate = ROOT.TH1F("hist_mZcandidate", "Reconstructed Z mass; m_{LL} [GeV]; Events", 60, 60, 120)
    hist_mWhadronicCandidate = ROOT.TH1F("hist_mWhadronicCandidate", "Reconstructed hadronic W mass; m_{jj} [GeV]; Events", 50, 0, 500)
    hist_mWleptonicCandidate = ROOT.TH1F("hist_mWleptonicCandidate", "Reconstructed leptonic W transverse mass; m^{LNu}_{T} [GeV]; Events", 50, 0, 200)
    h_mH_T = ROOT.TH1F("h_mH_T", "Reconstructed Higgs transverse mass; m^{H}_{T} [GeV]; Events", 60, 0, 600)
    hist_deltaPhi_ZH = ROOT.TH1F("hist_deltaPhi_ZH", "Delta Phi between Z and Higgs;delPhi [rad];Events", 50, -math.pi, math.pi)
    hist_nZcandidates = ROOT.TH1F("hist_nZcandidates", "Number of Z-candidates per event; n_{L}; Events", 20, 0, 20) # Curious to know how many Z candidates we get per event on average with this selection (DS, 19May24)
    hist_nWZcandidates = ROOT.TH1F("hist_nWZcandidates", "Number of WZ-candidates per event; n_{L}; Events", 20, 0, 20) # Curious to know how many WZ candidates we get per event on average with this selection (DS, 19May24)

    n_Z_candidates = 0
    n_W_lep_candidates = 0
    n_W_had_candidates = 0
    n_H_candidates = 0

    w_mass = 80.4  # W boson mass in GeV
    z_mass = 91.1876



    root_files = nanoGetSampleFiles(mcDirectory, sample)[0][1]
    print(f"Found ROOT files ({root_files}) in {input_dir} for sample {sample}.")
    # root_files = glob.glob(os.path.join(input_dir, "*.root"))
    for root_file_iter, root_file_name in enumerate(root_files):
        if root_file_iter % 10 == 0:
            print(f"Processing file {root_file_iter + 1}/{len(root_files)}: {root_file_name}")
        f = ROOT.TFile.Open(root_file_name)
        tree = f.Get("Events")
        for event in tree:
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
            hist_nLeptons.Fill(len(n_leptons))
            if len(leptons) < 3: continue
            if leptons[0]['pt'] < 25 or leptons[1]['pt'] < 20 or leptons[2]['pt'] < 15: continue
            if len(leptons) > 3 and leptons[3]['pt'] > 10: continue

            # Min(mll) > 12 for all lepton pairs
            pass_mll = True
            for i in range(len(leptons)):
                for j in range(i+1, len(leptons)):
                    l1 = get_lepton_p4(leptons[i]['pt'], leptons[i]['eta'], leptons[i]['phi'], leptons[i]['mass'])
                    l2 = get_lepton_p4(leptons[j]['pt'], leptons[j]['eta'], leptons[j]['phi'], leptons[j]['mass'])
                    if (l1 + l2).M() < 12:
                        pass_mll = False
            if not pass_mll: continue
            if abs(sum([lep['charge'] for lep in leptons])) != 1: continue

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
            
            zcand = min(zcands, key=lambda x: abs(x[2] - z_mass))
            hist_nZcandidates.Fill(len(zcands))
            z_leptons = [leptons[zcand[0]], leptons[zcand[1]]]
            hist_mZcandidate.Fill(zcand[2])
            Z_candidate = get_lepton_p4(z_leptons[0]['pt'], z_leptons[0]['eta'], z_leptons[0]['phi'], z_leptons[0]['mass']) + get_lepton_p4(z_leptons[1]['pt'], z_leptons[1]['eta'], z_leptons[1]['phi'], z_leptons[1]['mass'])
            n_Z_candidates += 1

            # # --- b-jet veto ---
            # has_bjet = False
            # for i in range(event.nJet):
            #     if event.Jet_pt[i] > 20 and event.Jet_btagDeepB[i] > 0.4184:
            #         has_bjet = True
            # if has_bjet: continue

            # --- Zγ veto: |m3l - mZ| > 20 GeV ---
            third_lepton = [lep for k, lep in enumerate(leptons) if k not in [zcand[0], zcand[1]]][0]
            l3_p4 = get_lepton_p4(third_lepton['pt'], third_lepton['eta'], third_lepton['phi'], third_lepton['mass'])
            z1_p4 = get_lepton_p4(z_leptons[0]['pt'], z_leptons[0]['eta'], z_leptons[0]['phi'], z_leptons[0]['mass'])
            z2_p4 = get_lepton_p4(z_leptons[1]['pt'], z_leptons[1]['eta'], z_leptons[1]['phi'], z_leptons[1]['mass'])
            m3l = (z1_p4 + z2_p4 + l3_p4).M()
            if abs(m3l - z_mass) < 20: continue

            # --- Jet selection ---
            jets = []
            for i in range(event.nJet):
                if event.Jet_pt[i] > 30 and abs(event.Jet_eta[i]) < 4.7:
                    jets.append({'pt': event.Jet_pt[i], 'eta': event.Jet_eta[i], 'phi': event.Jet_phi[i], 'mass': event.Jet_mass[i]})
            hist_nJets.Fill(len(jets))
            jets = sorted(jets, key=lambda x: -x['pt']) # Sort jets by descending pT

            # --- Signal region selection and W reconstruction (revised) ---
            # Initialize variables
            signal_region = False
            selected_w_pair = None

            if len(jets) >= 2:
                # Generate all possible dijet pairs and compute |m_jj - 80.4|
                dijet_pairs = []
                for i in range(len(jets)):
                    for j in range(i+1, len(jets)):
                        jet1_p4 = get_jet_p4(jets[i]['pt'], jets[i]['eta'], jets[i]['phi'], jets[i]['mass'])
                        jet2_p4 = get_jet_p4(jets[j]['pt'], jets[j]['eta'], jets[j]['phi'], jets[j]['mass'])
                        m_jj = (jet1_p4 + jet2_p4).M()
                        dijet_pairs.append({
                            'i': i, 'j': j, 
                            'dm': abs(m_jj - 80.4), 
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
                    hist_nWZcandidates.Fill(1)
                    continue  # Skip event if no valid pairs

            elif len(jets) == 1:
                # Original 1-jet logic (unchanged)
                l_met_px = third_lepton['pt']*math.cos(third_lepton['phi']) + event.MET_pt*math.cos(event.MET_phi)
                l_met_py = third_lepton['pt']*math.sin(third_lepton['phi']) + event.MET_pt*math.sin(event.MET_phi)
                l_met_phi = math.atan2(l_met_py, l_met_px)
                dphi = deltaPhi(l_met_phi, jets[0]['phi'])
                
                if dphi < math.pi/2:
                    signal_region = True
                    selected_w_pair = (0,)  # Mark single jet as W candidate

            if not signal_region:
                hist_nWZcandidates.Fill(1)
                continue

            # --- W (leptonic) reconstruction ---
            lep_p4 = get_lepton_p4(third_lepton['pt'], third_lepton['eta'], third_lepton['phi'], third_lepton['mass'])
            nu_p4 = ROOT.TLorentzVector()
            nu_p4.SetPtEtaPhiM(event.MET_pt, 0, event.MET_phi, 0)
            w_lep_mass = (lep_p4 + nu_p4).M()
            w_lep_mt = w_transverse_mass(third_lepton['pt'], third_lepton['phi'], event.MET_pt, event.MET_phi)
            hist_mWleptonicCandidate.Fill(w_lep_mt)
            n_W_lep_candidates += 1


            # --- Reconstruct W and Higgs using selected jets ---
            had_w_p4 = None

            if len(jets) == 1:
                # 1-jet case
                had_w_p4 = get_jet_p4(jets[0]['pt'], jets[0]['eta'], jets[0]['phi'], jets[0]['mass'])
                hist_mWhadronicCandidate.Fill(had_w_p4.M())
                n_W_had_candidates += 1

            elif len(jets) >= 2 and selected_w_pair is not None:
                # Reconstruct from selected dijet pair
                i, j = selected_w_pair
                jet1_p4 = get_jet_p4(jets[i]['pt'], jets[i]['eta'], jets[i]['phi'], jets[i]['mass'])
                jet2_p4 = get_jet_p4(jets[j]['pt'], jets[j]['eta'], jets[j]['phi'], jets[j]['mass'])
                had_w_p4 = jet1_p4 + jet2_p4
                hist_mWhadronicCandidate.Fill(had_w_p4.M())
                n_W_had_candidates += 1
            
            # --- Higgs reconstruction ---
            if had_w_p4 is not None:
                # Visible system: lepton + hadronic W
                vis_p4 = lep_p4 + had_w_p4
                m_vis = vis_p4.M()
                pt_vis = vis_p4.Pt()
                px_vis = vis_p4.Px()
                py_vis = vis_p4.Py()
                px_miss = event.MET_pt * math.cos(event.MET_phi)
                py_miss = event.MET_pt * math.sin(event.MET_phi)
                et_vis = math.sqrt(m_vis**2 + pt_vis**2)
                et_miss = event.MET_pt
                mt2 = (et_vis + et_miss)**2 - ((px_vis + px_miss)**2 + (py_vis + py_miss)**2)
                mt_higgs = math.sqrt(mt2) if mt2 > 0 else 0.
                h_mH_T.Fill(mt_higgs)
                n_H_candidates += 1
                px_higgs = px_vis + px_miss
                py_higgs = py_vis + py_miss
                phi_H_candidate = math.atan2(py_higgs, px_higgs)

            if Z_candidate is None or phi_H_candidate is None:
                continue
            phi_Z = Z_candidate.Phi()
            hist_deltaPhi_ZH.Fill(deltaPhi(phi_Z, phi_H_candidate))
        f.Close()

    out.Write()
    out.Close()

    print(f"Number of Z candidates: {n_Z_candidates}")
    print(f"Number of leptonic W candidates: {n_W_lep_candidates}")
    print(f"Number of hadronic W candidates: {n_W_had_candidates}")
    print(f"Number of H candidates: {n_H_candidates}")
    print(f"Histograms saved to {str(save_dir)}/reco_plots_WhadDiJetSelection.root")
