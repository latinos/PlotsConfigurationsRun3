import os
import glob
import subprocess


datacard_base = "../datacards"    
gof_dir = "GoF"
num_seeds = 101                   
container_image = "/cvmfs/unpacked.cern.ch/registry.hub.docker.com/cverstege/alma9-gridjob:latest"

os.makedirs(gof_dir, exist_ok=True)
os.chdir(gof_dir)

base_pattern = os.path.join(datacard_base, "*")
datacard_dirs = [d for d in glob.glob(base_pattern) if os.path.isdir(d)]

merge_script_name = "run_merge_and_plot.sh"
merge_script = open(merge_script_name, "w")
merge_script.write("#!/bin/bash\n\n")

for datacard_dir in datacard_dirs:
    final_state = os.path.basename(datacard_dir)
    var_dirs = [d for d in os.listdir(datacard_dir) if os.path.isdir(os.path.join(datacard_dir, d))]
    for var in var_dirs:
        datacard_txt = os.path.join(datacard_dir, var, "datacard.txt")
        datacard_root = os.path.join(datacard_dir, var, "datacard.root")
        if not os.path.exists(datacard_txt):
            continue

        out_name = f"_{final_state}_{var}"

        subprocess.run([
            "combineTool.py", "-M", "T2W", "-m", "125",
            "-o", "datacard.root",
            "-i", datacard_txt,
            "--channel-masks",
            "-P", "HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel",
            "--PO", "map=.*/WH_h.*_plus:r_WH[1,-10.0,10.0]",
            "--PO", "map=.*/WH_h.*_minus:r_WH[1,-10.0,10.0]",
        ])

        print(f"GoF for real Data of {final_state}/{var} ...")
        subprocess.run([
            "combineTool.py", "-M", "GoodnessOfFit", datacard_root,
            "--algo=saturated",
            "--setParameters", "r_WH=1",
            "--setParameterRanges", "r_WH=-5,5",
            "--redefineSignalPOIs", "r_WH",
            "-n", out_name,
        ])

        # toys
        toy_script_name = f"run_toys_{out_name}.sh"
        with open(toy_script_name, "w") as toy_script:
            toy_script.write("#!/bin/bash\n")
            toy_script.write("ulimit -s unlimited\n")
            for seed in range(num_seeds):  
                toy_script.write(
                    f"combine -M GoodnessOfFit {datacard_root} --algo=saturated -t 1 -s {seed} "
                    f"--setParameters r_WH=1 --setParameterRanges r_WH=-5,5 --redefineSignalPOIs r_WH -n {out_name}\n"
                )
        os.chmod(toy_script_name, 0o755)

        condor_file = f"condor_toys_{out_name}.sub"
        with open(condor_file, "w") as cf:
            cf.write(f"""\
universe         = container
container_image  = {container_image}
executable       = {os.path.abspath(toy_script_name)}
output           = {toy_script_name}.out
error            = {toy_script_name}.err
log              = {toy_script_name}.log
request_cpus     = 1
request_memory   = 2GB
queue
""")
        print(f"submit condor job for {out_name} ...")
        subprocess.run(["condor_submit", condor_file])


        merge_script.write(f"echo 'Merging/Plotting für {out_name}...'\n")
        merge_script.write(f"hadd -f higgsCombine{out_name}.GoodnessOfFit.mH120.toys.root higgsCombine{out_name}.GoodnessOfFit.mH120.*.root\n")
        merge_script.write(f"combineTool.py -M CollectGoodnessOfFit --input higgsCombine{out_name}.GoodnessOfFit.mH120.root higgsCombine{out_name}.GoodnessOfFit.mH120.toys.root -m 125 -o GoF{out_name}.json\n")
        merge_script.write(f"plotGof.py GoF{out_name}.json --statistic saturated --mass 120.0 -o GoF{out_name} --title-right={out_name} --range 0 200\n\n")


merge_script.close()
os.chmod(merge_script_name, 0o755)

print(f"\nstart merge and plot:\n    ./{merge_script_name}\n")
