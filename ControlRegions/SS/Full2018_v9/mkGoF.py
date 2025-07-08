import os
import subprocess
from variables import variables


output_dir = 'GoF'
n_toys = 100
combine_dir = '/work/halnasri/bachelor/CMSSW_14_1_0_pre4/src/'
base_dir = '/work/halnasri/bachelor/PlotsConfigurationsRun3/ControlRegions/SS/Full2018_v9'
current_dir = os.getcwd()


variables = variables.keys()
cuts = [d for d in os.listdir('datacards') if os.path.isdir(os.path.join('datacards', d))]

cut_control = ['wh3l_13TeV_SS_CR_plus_pt2ge20']
variable_control = ['pt1', 'mll']


scripts_dir = os.path.join(output_dir, "scripts")
outputs_dir = os.path.join(output_dir, "outputs")
plots_dir = os.path.join(output_dir, "plots")

os.makedirs(scripts_dir, exist_ok=True)
os.makedirs(outputs_dir, exist_ok=True)
os.makedirs(plots_dir, exist_ok=True)


wrapper_path = os.path.join(scripts_dir, "run_one_job.sh")
with open(wrapper_path, "w") as wrapper:
    wrapper.write("""#!/bin/bash
bash "$1"
""")
os.chmod(wrapper_path, 0o755)


sub_path = os.path.join(scripts_dir, "job_gof_all.sub")
with open(sub_path, "w") as sub:
    sub.write(f"""universe       = container
container_image= /cvmfs/unpacked.cern.ch/registry.hub.docker.com/cverstege/alma9-gridjob:latest
executable     = {wrapper_path}
arguments      = $(script_path)
error          = $(script_path).err
output         = $(script_path).out
log            = {scripts_dir}/gof_combined.log
run_as_owner   = true
RequestMemory  = 2000
RequestDisk    = 100000
+RequestWalltime = 3600
requirements   = TARGET.ProvidesETPResources
accounting_group = cms.higgs

""")

    
    script_paths = []

    for cut in cuts:
        for variable in variables:
            
            tag = f"{cut}_{variable}"
            card_dir = os.path.join(current_dir, "datacards", cut, variable)
            card_txt = os.path.join(card_dir, "datacard.txt")
            card_root = os.path.join(card_dir, "datacard.root")

            if not os.path.exists(card_txt):
                print(f"Skipping {tag}: datacard.txt missing")
                continue

            script_name = f"job_{tag}.sh"
            script_path = os.path.join(scripts_dir, script_name)
            script_paths.append(script_path)

            with open(script_path, "w") as sh:
                sh.write(f"""#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd {combine_dir}
eval `scramv1 runtime -sh`
cd -

cd {base_dir}/{outputs_dir}

combineTool.py -M T2W -m 125 -o {card_root} -i {card_txt} \\
  --channel-masks \\
  -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \\
  --PO 'map=.*/WH_h.*_plus:r_WH[1,-10.0,10.0]' \\
  --PO 'map=.*/WH_h.*_minus:r_WH[1,-10.0,10.0]'

combineTool.py -M GoodnessOfFit {card_root} --algo=saturated \\
  --setParameters r_WH=1 --setParameterRanges r_WH=-5,5 \\
  --redefineSignalPOIs r_WH -n _{tag}

combineTool.py -M GoodnessOfFit {card_root} --algo=saturated -t 1 -s 0:{n_toys}:1 \\
  --setParameters r_WH=1 --setParameterRanges r_WH=-5,5 \\
  --redefineSignalPOIs r_WH -n _{tag}

hadd -f higgsCombine_{tag}.GoodnessOfFit.mH120.toys.root higgsCombine_{tag}.GoodnessOfFit.mH120.*.root

combineTool.py -M CollectGoodnessOfFit --input \\
  higgsCombine_{tag}.GoodnessOfFit.mH120.root \\
  higgsCombine_{tag}.GoodnessOfFit.mH120.toys.root \\
  -m 125 -o GoF_{tag}.json

mv GoF_{tag}.json {base_dir}/{plots_dir}/

cd {base_dir}/{plots_dir}
plotGof.py GoF_{tag}.json --statistic saturated --mass 120.0 \\
  -o GoF_{tag} --title-right={tag} --range 0 200
""")
            os.chmod(script_path, 0o755)

    
    sub.write("queue script_path in (\n")
    for path in script_paths:
        abs_path = os.path.abspath(path)
        sub.write(f"  {abs_path}\n")
    sub.write(")\n")


subprocess.run(["condor_submit", sub_path])

