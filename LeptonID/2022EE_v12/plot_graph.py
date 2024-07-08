import ROOT
import sys,os

ele_ids  = ["wp90iso","mvaWinter22V2Iso_WP90"]
muon_ids = ["cut_TightID_POG","cut_Tight_HWW","cut_TightMiniIso_HWW","mvaMuID_WP_medium","mvaMuID_WP_tight"] 

signals     = ["WW","ggH_hww"]
backgrounds = ["TTToSemiLeptonic","WJets"]

final_states = ["ee","em","mm"]
pt_ranges    = ["high_pt","low_pt"]

input_file_name = "eff_plots/efficiencies.root"

colors = [ROOT.kGreen+1,ROOT.kRed+1,ROOT.kBlue,ROOT.kOrange,ROOT.kMagenta,ROOT.kAzure+10]

sys.argv.append('-b')
ROOT.gROOT.SetBatch()

def plot_canvas(input_file_name,
                sig,
                bkg,
                ele_ids,
                muon_ids,
                final_state,
                pt_range,
                output_name,
                focus):
    """plots a canvas with the requested cuts and processes"""

    input_file = ROOT.TFile(input_file_name)

    first_graph = 0

    # Create canvas
    c1 = ROOT.TCanvas("c1","c1",800,800)
    c1.cd()

    # Trick to allow legend to get all the graphs --> put them into a list
    graphs = []
            
    for ele_id in ele_ids:
        for muon_id in muon_ids:
            
            graph_name = f"{sig}_{bkg}_sr_ele_{ele_id}__mu_{muon_id}_{final_state}_{pt_range}"
            print(f"Graph name: {graph_name}")

            if first_graph == 0:
                print("Preparing first graph")
                graph = input_file.Get(graph_name)
                if isinstance(graph, ROOT.TGraph): 
                    graphs.append(input_file.Get(graph_name))
                    graphs[-1].SetMarkerStyle(20)
                    graphs[-1].SetMarkerColor(colors[first_graph])
                    graphs[-1].GetXaxis().SetRangeUser(0,1)
                    graphs[-1].GetYaxis().SetRangeUser(0,1)
                    if focus == 'muon': graphs[-1].SetName(muon_id)
                    if focus == 'ele':  graphs[-1].SetName(ele_id)
                    if focus == 'both': graphs[-1].SetName(ele_id + "_" + muon_id)
                    graphs[-1].Draw("AP")
                    graphs[-1].GetXaxis().SetRangeUser(0,1)
                    graphs[-1].GetYaxis().SetRangeUser(0,1)
                    print("First graph plotted!")
                    print(f"Values = ({graphs[-1].GetPointX(0)},{graphs[-1].GetPointY(0)})")
                    first_graph += 1
            else:
                print(f"Preparing graph number {first_graph+1}")
                graph = input_file.Get(graph_name)
                if isinstance(graph, ROOT.TGraph): 
                    graphs.append(input_file.Get(graph_name))
                    graphs[-1].SetMarkerStyle(20)
                    graphs[-1].SetMarkerColor(colors[first_graph])
                    if focus == 'muon': graphs[-1].SetName(muon_id)
                    if focus == 'ele':  graphs[-1].SetName(ele_id)
                    if focus == 'both': graphs[-1].SetName(ele_id + "_" + muon_id)
                    graphs[-1].Draw("P,same")
                    print(f"Graph {first_graph+1} plotted!")
                    print(f"Values = ({graphs[-1].GetPointX(0)},{graphs[-1].GetPointY(0)})")
                    first_graph += 1

    # Legend                
    leg = ROOT.TLegend(0.12,0.12,0.82,0.42)
    leg.SetLineColor(0)
    if focus == 'muon':   leg.SetHeader("Muon ID:")
    elif focus == 'ele':  leg.SetHeader("Electron ID:")
    elif focus == 'both': leg.SetHeader("Electron and Muon ID:")
    else:
        raise ValueError("Please spcify what I should put my focus on")
    for g in graphs:
        leg.AddEntry(g,g.GetName(),"p")
    
    print(f"Graphs = {graphs}")
    leg.Draw("same")
    print(f"Total legend rows = {leg.GetNRows()}")
    c1.Print(f"eff_plots/{output_name}.png")
    input_file.Close()
    

# Calling the function to produce plots 
plot_canvas(input_file_name,"WW","WJets",ele_ids,muon_ids,"ee","high_pt","ee_WW_vs_Wjets","ele")
plot_canvas(input_file_name,"WW","WJets",ele_ids,muon_ids,"em","high_pt","em_WW_vs_Wjets","both")
plot_canvas(input_file_name,"WW","WJets",ele_ids,muon_ids,"mm","high_pt","mm_WW_vs_Wjets","muon")

plot_canvas(input_file_name,"ggH_hww","WJets",ele_ids,muon_ids,"ee","high_pt","ee_ggH_vs_Wjets","ele")
plot_canvas(input_file_name,"ggH_hww","WJets",ele_ids,muon_ids,"em","high_pt","em_ggH_vs_Wjets","both")
plot_canvas(input_file_name,"ggH_hww","WJets",ele_ids,muon_ids,"mm","high_pt","mm_ggH_vs_Wjets","muon")

plot_canvas(input_file_name,"WW","TTToSemiLeptonic",ele_ids,muon_ids,"ee","high_pt","ee_WW_vs_Top","ele")
plot_canvas(input_file_name,"WW","TTToSemiLeptonic",ele_ids,muon_ids,"em","high_pt","em_WW_vs_Top","both")
plot_canvas(input_file_name,"WW","TTToSemiLeptonic",ele_ids,muon_ids,"mm","high_pt","mm_WW_vs_Top","muon")

plot_canvas(input_file_name,"ggH_hww","TTToSemiLeptonic",ele_ids,muon_ids,"ee","high_pt","ee_ggH_vs_Top","ele")
plot_canvas(input_file_name,"ggH_hww","TTToSemiLeptonic",ele_ids,muon_ids,"em","high_pt","em_ggH_vs_Top","both")
plot_canvas(input_file_name,"ggH_hww","TTToSemiLeptonic",ele_ids,muon_ids,"mm","high_pt","mm_ggH_vs_Top","muon")


plot_canvas(input_file_name,"WW","WJets",ele_ids,muon_ids,"ee","low_pt","ee_WW_vs_Wjets_low_pT","ele")
plot_canvas(input_file_name,"WW","WJets",ele_ids,muon_ids,"em","low_pt","em_WW_vs_Wjets_low_pT","both")
plot_canvas(input_file_name,"WW","WJets",ele_ids,muon_ids,"mm","low_pt","mm_WW_vs_Wjets_low_pT","muon")

plot_canvas(input_file_name,"ggH_hww","WJets",ele_ids,muon_ids,"ee","low_pt","ee_ggH_vs_Wjets_low_pT","ele")
plot_canvas(input_file_name,"ggH_hww","WJets",ele_ids,muon_ids,"em","low_pt","em_ggH_vs_Wjets_low_pT","both")
plot_canvas(input_file_name,"ggH_hww","WJets",ele_ids,muon_ids,"mm","low_pt","mm_ggH_vs_Wjets_low_pT","muon")

plot_canvas(input_file_name,"WW","TTToSemiLeptonic",ele_ids,muon_ids,"ee","low_pt","ee_WW_vs_Top_low_pT","ele")
plot_canvas(input_file_name,"WW","TTToSemiLeptonic",ele_ids,muon_ids,"em","low_pt","em_WW_vs_Top_low_pT","both")
plot_canvas(input_file_name,"WW","TTToSemiLeptonic",ele_ids,muon_ids,"mm","low_pt","mm_WW_vs_Top_low_pT","muon")

plot_canvas(input_file_name,"ggH_hww","TTToSemiLeptonic",ele_ids,muon_ids,"ee","low_pt","ee_ggH_vs_Top_low_pT","ele")
plot_canvas(input_file_name,"ggH_hww","TTToSemiLeptonic",ele_ids,muon_ids,"em","low_pt","em_ggH_vs_Top_low_pT","both")
plot_canvas(input_file_name,"ggH_hww","TTToSemiLeptonic",ele_ids,muon_ids,"mm","low_pt","mm_ggH_vs_Top_low_pT","muon")
