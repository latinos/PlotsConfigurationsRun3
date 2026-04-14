import sys,os
argv = sys.argv
sys.argv = argv[:1]

import optparse

pwd = os.getcwd()

# Input variables
sys.argv = argv

usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)

parser.add_option('--final_state', dest='final_state', help='Final state to inspect',                             default='DEFAULT')
parser.add_option('--submit',      dest='submit',      help='Flag to submit job',                                 action='store_true')
parser.add_option('--poi',         dest='poi',         help='POI to inspect: WH inclusive or WH plus-minus',      default='WH')

# read default parsing options as well
(opt, args) = parser.parse_args()

print("Final state : {}".format(opt.final_state))
print("Submit      : {}".format(opt.submit))
print("POI         : {}".format(opt.poi))

# Exceptions
if opt.final_state == 'DEFAULT' :
    print("Please select the final state to inspect. E.g.:")
    print("python submit_gof.py --final_state FullRun2        --submit")
    print("python submit_gof.py --final_state FullRun2_WHSS   --submit")
    print("python submit_gof.py --final_state FullRun2_WH3l   --submit")
    print("python submit_gof.py --final_state Full2018        --submit")
    print("python submit_gof.py --final_state Full2018_WHSS   --submit")
    print("python submit_gof.py --final_state Full2018_WH3l   --submit")
    print("python submit_gof.py --final_state Full2017        --submit")
    print("python submit_gof.py --final_state Full2017_WHSS   --submit")
    print("python submit_gof.py --final_state Full2017_WH3l   --submit")
    print("python submit_gof.py --final_state 2016noHIPM      --submit")
    print("python submit_gof.py --final_state 2016noHIPM_WHSS --submit")
    print("python submit_gof.py --final_state 2016noHIPM_WH3l --submit")
    print("python submit_gof.py --final_state 2016HIPM        --submit")
    print("python submit_gof.py --final_state 2016HIPM_WHSS   --submit")
    print("python submit_gof.py --final_state 2016HIPM_WH3l   --submit")    
    raise ValueError("I need to know which fintate to inspect")

if opt.poi != 'WH' and opt.poi != 'WH_plus_minus':
    raise ValueError("I only know two POI sets: WH and WH_plus_minus")

final_state = opt.final_state
submit      = opt.submit
poi         = opt.poi

# Dictionary with workspace corresponding to each final state
dict_fs_ws = {
    "FullRun2"        : "WH_chargeAsymmetry_WH_FullRun2_v9_high_pt_binning_WH_strength.root",
    "FullRun2_WHSS"   : "WH_chargeAsymmetry_WH_FullRun2_v9_WHSS_high_pt_binning_WH_strength.root",
    "FullRun2_WH3l"   : "WH_chargeAsymmetry_WH_FullRun2_v9_WH3l_binning_WH_strength.root",
    "Full2018"        : "WH_chargeAsymmetry_WH_Full2018_v9_high_pt_binning_WH_strength.root",
    "Full2018_WHSS"   : "WH_chargeAsymmetry_WH_Full2018_v9_WHSS_high_pt_binning_WH_strength.root",
    "Full2018_WH3l"   : "WH_chargeAsymmetry_WH_Full2018_v9_WH3l_binning_WH_strength.root",
    "Full2017"        : "WH_chargeAsymmetry_WH_Full2017_v9_high_pt_binning_WH_strength.root",
    "Full2017_WHSS"   : "WH_chargeAsymmetry_WH_Full2017_v9_WHSS_high_pt_binning_WH_strength.root",
    "Full2017_WH3l"   : "WH_chargeAsymmetry_WH_Full2017_v9_WH3l_binning_WH_strength.root",
    "2016noHIPM"      : "WH_chargeAsymmetry_WH_2016noHIPM_v9_high_pt_binning_WH_strength.root",
    "2016noHIPM_WHSS" : "WH_chargeAsymmetry_WH_2016noHIPM_v9_WHSS_high_pt_binning_WH_strength.root",
    "2016noHIPM_WH3l" : "WH_chargeAsymmetry_WH_2016noHIPM_v9_WH3l_binning_WH_strength.root",
    "2016HIPM"        : "WH_chargeAsymmetry_WH_2016HIPM_v9_high_pt_binning_WH_strength.root",
    "2016HIPM_WHSS"   : "WH_chargeAsymmetry_WH_2016HIPM_v9_WHSS_high_pt_binning_WH_strength.root",
    "2016HIPM_WH3l"   : "WH_chargeAsymmetry_WH_2016HIPM_v9_WH3l_binning_WH_strength.root",    
}

datacard    = dict_fs_ws[final_state]
if poi == 'WH_plus_minus':
    datacard = datacard.replace('WH_strength.root','WH_plus_minus.root')


# Preparing cfg file and submit
print("Preparing cfg ...")

os.system(f"mkdir -p GoF")
os.system(f"mkdir -p GoF_{final_state}")

with open (f"GoF_{final_state}/submit.jdl", "w") as sub_file:
    sub_file.write(f"universe     = vanilla \n")
    sub_file.write(f"executable   = ../do_gof_test.sh \n")
    sub_file.write(f"arguments    = {final_state} {datacard} {poi} {pwd} \n")
    sub_file.write(f"output       = out.txt \n")
    sub_file.write(f"error        = err.txt \n")
    sub_file.write(f"log          = log.txt \n")
    sub_file.write(f"request_cpus = 1 \n")
    sub_file.write(f"+JobFlavour  = \"tomorrow\" \n")
    sub_file.write(f"queue 1 \n")
    sub_file.close()

print("... done!")
    
if submit:
    os.chdir(f'GoF_{final_state}/')
    os.system("condor_submit submit.jdl")
    os.chdir(f'{pwd}')
