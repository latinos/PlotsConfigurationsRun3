import sys,os
import optparse
import ROOT
import array

# Parsing input parameter
usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)

parser.add_option('--input_file',        dest='input_file',        help='Input file to inspect',                   default="DEFAULT")
parser.add_option('--variable',          dest='variable',          help='Variable to consider',                    default="DEFAULT")
parser.add_option('--cut',               dest='cut',               help='Cut to consider',                         default="DEFAULT")
parser.add_option('--nbins',             dest='nbins',             help='Number of bins in final histogram',       default="10")
parser.add_option('--min_signal_events', dest='min_signal_events', help='Minimum number of signal events per bin', default="0.5")

(opt, args) = parser.parse_args()

print("Input file name           = {}".format(opt.input_file))
print("Variable                  = {}".format(opt.variable))
print("Cut                       = {}".format(opt.cut))
print("Target number of bins     = {}".format(opt.nbins))
print("Min signal events per bin = {}".format(opt.min_signal_events))

# Exceptions
if opt.input_file == 'DEFAULT' :
    raise ValueError("Please insert input file name")

if opt.variable == 'DEFAULT' :
    raise ValueError("Please insert variable")

if opt.cut == 'DEFAULT' :
    raise ValueError("Please insert cut")

if int(opt.nbins) <= 0 :
    raise ValueError("Please insert a positive number of bins")

if float(opt.min_signal_events) <= 0 :
    raise ValueError("Please insert a positive minimum number of events per bin")


# Assign input parameters to variables
input_file        = opt.input_file
variable          = opt.variable
cut               = opt.cut
nbins             = int(opt.nbins)
min_signal_events = float(opt.min_signal_events)


def find_bin_edges(signals, cut, variable, nbins, min_signal_events):
    '''Finds the bin edges for a given cut

    signals: a list with the name of the processes considered as signal. 
             We can maybe take it from structure.py
    cut: cut to inspect
    variable: variable to inspect
    nbins: target number of bins
    min_signal_events: minimum number of signal events per bin
    '''

    # Checking total signal integral
    h_original = ""
    for sig in signals:
        h_tmp_name = f"{cut}/{variable}/{sig}"
        h_tmp = infile.Get(h_tmp_name)
        h_tmp.SetDirectory(0)
        if h_original == "":
            h_original = h_tmp # .Clone()
        else:
            h_original.Add(h_tmp)
        integral_tmp = h_tmp.Integral()
        integral = h_original.Integral()
        print(f"Current integral = {integral_tmp}; Total integral now is {integral}")


    while nbins > 0:
        target_bin_content = integral/nbins
        if target_bin_content < min_signal_events:
            print(f"With the current number of bins ({nbins}), we will have {target_bin_content} signal events per bin, while the minimum acceptable value is {min_signal_events}. Try with one bin less.")
            nbins = nbins-1
        else:
            break
    print(f"I will re-bin the signal histogram such that it has {nbins} bins, each containing {target_bin_content} expected events")
    
    # Finding bin edges considering total signal histogram
    print(f"Total number of bins in input histogram = {h_original.GetNbinsX()}")
    
    current_bin_content = 0
    bins_edges = []
    bins_edges_numbers = []
    # Loop starting from the right-most bin
    for i in range(1,h_original.GetNbinsX()+1):
        current_bin_content = current_bin_content + h_original.GetBinContent(h_original.GetNbinsX() + 1 - i)
        if current_bin_content >= target_bin_content:
            bins_edges.append(h_original.GetBinCenter(h_original.GetNbinsX() + 1 - i))
            bins_edges_numbers.append(h_original.GetNbinsX() + 1 - i)
            print(f"I have reached an integral of {current_bin_content} in bin {h_original.GetNbinsX() + 1 - i}, corresponding to x-axis position {bins_edges[-1]}")
            current_bin_content = 0

    new_bin_edges = bins_edges[::-1]
    new_bin_edges_round = []
    new_bin_edges_round.append(-1)
    for edge in new_bin_edges:
        new_bin_edges_round.append(round(edge,3))
    new_bin_edges_round.append(1)
    
    return new_bin_edges_round


    
def reassign_bin_content(original_histo, bin_edges):
    '''Takes a histogram in input as rebins it

    
    original histo: histogram to rebin
    bin_edges: bin edges of the rebinned histogram
    '''

    # Define output histogram
    histo_name  = original_histo.GetName()
    histo_title = original_histo.GetTitle()
    edges       = array.array('d', bin_edges)
    # print(f"Edges inside function: {edges}")
    output_histogram = ROOT.TH1F(histo_name, histo_title, len(edges)-1, edges)
    output_histogram.SetDirectory(0)

    # Filling bins of output histogram
    bin_content = 0
    current_bin = 0
    # Loop over all bins of original histogram
    for i in range(1,original_histo.GetNbinsX()+1):
        bin_content = bin_content + original_histo.GetBinContent(i)
        # print(f"Current bin center: {original_histo.GetBinCenter(i)}. Current bin content = {bin_content}. Next edge at: {bin_edges[current_bin+1]}")
        # Once the bin edge is reached, fill the corresponding bin in the updated histogram, and move to the next bin.
        if (original_histo.GetBinCenter(i) > bin_edges[current_bin+1]):
            output_histogram.SetBinContent(current_bin, bin_content)
            # print(f"I have filled bin {current_bin} with the value {output_histogram.GetBinContent(current_bin)} ({bin_content})")
            current_bin = current_bin + 1
            bin_content = 0
            
    return output_histogram
    

infile = ROOT.TFile(input_file,"update")

signals = ["histo_WH_hww_plus","histo_WH_hww_minus","histo_WH_htt_plus","histo_WH_htt_minus"]

# # Checking total signal integral
# h_original = ""
# for sig in signals:
#     h_tmp_name = f"{cut}/{variable}/{sig}"
#     h_tmp = infile.Get(h_tmp_name)
#     h_tmp.SetDirectory(0)
#     if h_original == "":
#         h_original = h_tmp # .Clone()
#     else:
#         h_original.Add(h_tmp)
#     integral_tmp = h_tmp.Integral()
#     integral = h_original.Integral()
#     print(f"Current integral = {integral_tmp}; Total integral now is {integral}")

# target_bin_content = integral/nbins
# print(f"I will re-bin the signal histogram such that it has {nbins} bins, each containing {target_bin_content} expected events")
    
# # Finding bin edges considering total signal histogram
# print(f"Total number of bins in input histogram = {h_original.GetNbinsX()}")

# current_bin_content = 0
# bins_edges = []
# bins_edges_numbers = []
# # Loop starting from the right-most bin
# for i in range(1,h_original.GetNbinsX()+1):
#     current_bin_content = current_bin_content + h_original.GetBinContent(h_original.GetNbinsX() + 1 - i)
#     if current_bin_content >= target_bin_content:
#         bins_edges.append(h_original.GetBinCenter(h_original.GetNbinsX() + 1 - i))
#         bins_edges_numbers.append(h_original.GetNbinsX() + 1 - i)
#         print(f"I have reached an integral of {current_bin_content} in bin {h_original.GetNbinsX() + 1 - i}, corresponding to x-axis position {bins_edges[-1]}")
#         current_bin_content = 0

# new_bin_edges = bins_edges[::-1]
# new_bin_edges_round = []
# new_bin_edges_round.append(-1)
# for edge in new_bin_edges:
#     new_bin_edges_round.append(round(edge,3))
# new_bin_edges_round.append(1)
    
# print(f"Bin edges: {new_bin_edges_round}")


# First layer: cuts
for cut in infile.GetListOfKeys():
    if cut.IsFolder() == False: continue 
    cut_dir = cut.GetName()
    # output_file.mkdir(cut_dir) 
    print("Current cut: {}".format(cut_dir))
    if 'SS_CR' in cut_dir:
        print('Skipping')
        continue
    
    edges_for_current_cut = find_bin_edges(signals,cut_dir,variable,nbins,min_signal_events)
    
    # We set the variable name as input: no need to loop over all of them
    # infile.cd(f"{cut_dir}/{variable}")
    old_directory_name = f"{cut_dir}/{variable}/"
    new_directory_name = f"{cut_dir}/{variable}_flatten/"
    
    infile.mkdir(new_directory_name)

    infile.cd(old_directory_name)

    for histo in ROOT.gDirectory.GetListOfKeys() :
        infile.cd(old_directory_name)
        # print(histo.GetName())

        original_histo = infile.Get(f"{cut_dir}/{variable}/{histo.GetName()}")
        original_histo.SetDirectory(0)
        # new_histo = reassign_bin_content(original_histo, new_bin_edges_round)
        new_histo = reassign_bin_content(original_histo, edges_for_current_cut)
        
        infile.cd(new_directory_name)
        # new_histo.Draw()
        new_histo.Write()
        
        # del new_histo
        # del original_histo
