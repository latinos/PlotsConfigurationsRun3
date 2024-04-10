import ROOT
from optparse import OptionParser
import json

parser = OptionParser()
parser.add_option("-f", "--inputFile", dest="ifile", default="input.root", type='string', help="ROOT input file")
parser.add_option("-c", "--category",  dest="category", default="cat", type='string', help="ROOT input file")
parser.add_option("-v", "--variable",  dest="variable", default="var", type='string', help="ROOT input file")
(options, args) = parser.parse_args()

ifile   = options.ifile
category = options.category
variable = options.variable

samples = ['WWewk_CMWW_LL', 'WWewk_CMWW_LT', 'WWewk_CMWW_TL', 'WWewk_CMWW_TT',
           'WWewk_LL', 'WWewk_LT', 'WWewk_TL', 'WWewk_TT']

rfile   = ROOT.TFile.Open(ifile)
rdir    = rfile.Get(category + '/' + variable)
keys    = rdir.GetListOfKeys()
nominal = {}
variations = {}
norm    = {}
for sample in samples:
    histo = rfile.Get(category + '/' + variable + '/histo_' + sample)
    nominal[sample] = histo.Integral()
    variations[sample] = {}
    norm[sample] = {}

for key in keys:
    if 'Up' not in key.GetName() and 'Down' not in key.GetName():
        continue
    histo = rfile.Get(category + '/' + variable + '/' + key.GetName())
    var = ''
    print(key.GetName() + ', integral = ' + str(histo.Integral()))
    for sample in samples:
        if sample in key.GetName():
            var = key.GetName().replace('histo_' + sample + '_', '').replace('Up', '').replace('Down','')
        if var not in variations[sample].keys() and sample in key.GetName():
            variations[sample][var] = [0., 0.]
            norm[sample][var] = [0., 0.]
        if sample in key.GetName():
            if 'Up' in key.GetName():
                variations[sample][var][0]  = histo.Integral()
                norm[sample][var][0]        = nominal[sample] / variations[sample][var][0]
            elif 'Down' in key.GetName():
                variations[sample][var][1]  = histo.Integral()
                norm[sample][var][1]        = nominal[sample] / variations[sample][var][1]
            else:
                print('nuisance not recognized: ' + key.GetName())

with open('NormTHU.json', 'w', encoding='utf-8') as f:
    json.dump(norm, f, ensure_ascii=False, indent=4)
