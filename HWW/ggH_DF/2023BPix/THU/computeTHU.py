import ROOT
from optparse import OptionParser
import json
import re

parser = OptionParser()
parser.add_option("-f", "--inputFile", dest="ifile", default="input.root", type='string', help="ROOT input file")
parser.add_option("-c", "--category",  dest="category", default="cat", type='string', help="ROOT input category")
parser.add_option("-v", "--variable",  dest="variable", default="var", type='string', help="ROOT input variable")
(options, args) = parser.parse_args()

ifile    = options.ifile
category = options.category
variable = options.variable

samples = ['ggH_hww', 'qqH_hww']

rfile   = ROOT.TFile.Open(ifile)
rdir    = rfile.Get(f"{category}/{variable}")
keys    = rdir.GetListOfKeys()

nominal = {}
variations = {}
norm    = {}

for sample in samples:
    histo = rfile.Get(f"{category}/{variable}/histo_{sample}")
    nominal[sample] = histo.Integral()
    variations[sample] = {}
    norm[sample] = {}

for key in keys:
    key_name = key.GetName()
    
    # Check sample association
    matched_sample = None
    for sample in samples:
        if key_name.startswith(f"histo_{sample}_"):
            matched_sample = sample
            break
            
    if not matched_sample:
        continue

    histo = rfile.Get(f"{category}/{variable}/{key_name}")
    integral = histo.Integral()
    print(f"{key_name}, integral = {integral}")

    # 1. Handle SPECIAL_NUIS envelope variations individually
    envelope_match = re.search(r'histo_' + matched_sample + r'_(.*_SPECIAL_NUIS_envelope\d+)$', key_name)
    if envelope_match:
        var = envelope_match.group(1)  # Keeps full name e.g. "QCDscale_ggH_SPECIAL_NUIS_envelope0"
        variations[matched_sample][var] = integral
        norm[matched_sample][var] = nominal[matched_sample] / integral if integral != 0 else 0.
        continue

    # 2. Handle standard Up/Down variations
    if 'Up' in key_name or 'Down' in key_name:
        var = key_name.replace(f"histo_{matched_sample}_", "").replace("Up", "").replace("Down", "")
        
        if var not in variations[matched_sample]:
            variations[matched_sample][var] = [0., 0.]
            norm[matched_sample][var] = [0., 0.]

        if 'Up' in key_name:
            variations[matched_sample][var][0] = integral
            norm[matched_sample][var][0] = nominal[matched_sample] / integral if integral != 0 else 0.
        elif 'Down' in key_name:
            variations[matched_sample][var][1] = integral
            norm[matched_sample][var][1] = nominal[matched_sample] / integral if integral != 0 else 0.

# Save output JSON
with open('NormTHU.json', 'w', encoding='utf-8') as f:
    json.dump(norm, f, ensure_ascii=False, indent=4)