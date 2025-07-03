import sys,os

output_dir = 'GoF'

cut      = 'hww2l2v_13TeV_WH_SS_mm_1j_SS_CR_plus_pt2ge20'
variable = 'mll'
n_toys   = '100'

combine_directory = '/work/ntrevisa/combine/CMSSW_14_1_0_pre4/src/'

os.system(f'mkdir -p {output_dir}')

current_dir = os.getcwd()

# Preparing executable
script_name = f'{output_dir}/script_gof.sh'

script_text_indent = f'''
#!/bin/bash

# Setup environment
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd {combine_directory}
eval `scramv1 runtime -sh`
cd -

# Prepare workspace
combineTool.py -M T2W -m 125 \
    -o datacard.root \
    -i {current_dir}/datacards/{cut}/{variable}/datacard.txt \
    --channel-masks \
    -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
    --PO 'map=.*/WH_h.*_plus:r_WH[1,-10.0,10.0]' \
    --PO 'map=.*/WH_h.*_minus:r_WH[1,-10.0,10.0]'

# Fit on data
combineTool.py -M GoodnessOfFit {current_dir}/datacards/{cut}/{variable}/datacard.root \
    --algo=saturated \
    --setParameters r_WH=1 \
    --setParameterRanges r_WH=-5,5 \
    --redefineSignalPOIs r_WH \
    -n _{cut}_{variable}

# Produce toys and fit on pseudodata
combineTool.py -M GoodnessOfFit {current_dir}/datacards/{cut}/{variable}/datacard.root \
    --algo=saturated \
    -t 1 \
    -s 0:{n_toys}:1 \
    --setParameters r_WH=1 \
    --setParameterRanges r_WH=-5,5 \
    --redefineSignalPOIs r_WH \
    -n _{cut}_{variable}

# Hadd the fit to toys
hadd -f higgsCombine_{cut}_{variable}.GoodnessOfFit.mH120.toys.root higgsCombine_{cut}_{variable}.GoodnessOfFit.mH120.*.root

# Collect fit results and produce json file
combineTool.py -M CollectGoodnessOfFit --input higgsCombine_{cut}_{variable}.GoodnessOfFit.mH120.root higgsCombine_{cut}_{variable}.GoodnessOfFit.mH120.toys.root -m 125 -o GoF_{cut}_{variable}.json
	
# Plot
plotGof.py GoF_{cut}_{variable}.json --statistic saturated --mass 120.0 -o GoF_{cut}_{variable} --title-right=_{cut}_{variable} --range 0 200
'''

# Printing executable
with open(script_name, 'w') as outfile:
    outfile.write(script_text_indent)


    
# Preparing submission file
submission_name = f'{output_dir}/submit_gof.sub'

submission_text_indent = f'''
universe         = container                                          
container_image  = /cvmfs/unpacked.cern.ch/registry.hub.docker.com/cverstege/alma9-gridjob:latest

executable       = /bin/bash
arguments        = {current_dir}/GoF/script_gof.sh

error            = {cut}_{variable}.err
log              = {cut}_{variable}.log
output           = {cut}_{variable}.out

run_as_owner     = true
RequestMemory    = 1800
RequestDisk      = 100000
+RequestWalltime = 7200

requirements     = TARGET.ProvidesETPResources

accounting_group = cms.higgs

queue 1
'''

# Are these arguments needed?
# JobBatchName     = {os.path.basename(os.path.normpath(sim_dir))} 

# Printing submission file
with open(submission_name, 'w') as outfile:
    outfile.write(submission_text_indent)


# Submit job
os.chdir(f'{output_dir}')
os.system('condor_submit submit_gof.sub')
