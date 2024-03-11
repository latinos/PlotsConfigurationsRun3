import ROOT
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f", "--inputFile", dest="ifile", default="input.root", type='string', help="ROOT input file")
(options, args) = parser.parse_args()

ifile   = options.ifile

rfile   = ROOT.TFile.Open(ifile)
rdir    = rfile.Get('top_2j_em/events')
keys    = rdir.GetListOfKeys()
for key in keys:
    print(key.GetName(), rfile.Get('top_2j_em/events/' + key.GetName()).Integral())