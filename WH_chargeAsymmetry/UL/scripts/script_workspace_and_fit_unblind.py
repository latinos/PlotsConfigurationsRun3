import sys,os
import optparse


# Parsing input parameter
usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)

parser.add_option('--datacard_name',    dest='datacard_name',    help='datacard to use for the fit',                          default="DEFAULT")
parser.add_option('--output_name',      dest='output_name',      help='txt file where fit results are saved',                 default="DEFAULT")
parser.add_option('--sanity_check',     dest='sanity_check',     help='comma-separated list of additional fit sanity checks', default=False)
parser.add_option('--freeze_nuisances', dest='freeze_nuisances', help='freeze systematic uncertainties',                      default=False)
parser.add_option('--only_workspace',   dest='only_workspace',   help='flag to create only workspace',                        default=False)
parser.add_option('--only_fit',         dest='only_fit',         help='flag to only perform fit',                             default=False)
parser.add_option('--channel_mask',     dest='channel_mask',     help='channels to mask',                                     default=False)

(opt, args) = parser.parse_args()

print("Datacard name    = {}".format(opt.datacard_name))
print("Output name      = {}".format(opt.output_name))
print("Sanity checks    = {}".format(opt.sanity_check))
print("Freeze nuisances = {}".format(opt.freeze_nuisances))
print("Only workspace   = {}".format(opt.only_workspace))
print("Only fit         = {}".format(opt.only_fit))
print("Channels to mask = {}".format(opt.channel_mask))

# Exceptions
if opt.datacard_name == 'DEFAULT' :
    raise ValueError("Please insert datacard file name")
    
if opt.output_name == 'DEFAULT' :
    raise ValueError("Please insert output file name")


# Assign input parameters to variables
datacard_name = opt.datacard_name
output_name   = opt.output_name

sanity_check = [] # False
# if opt.sanity_check == "True" or opt.sanity_check == "1":
#     opt.sanity_check = True
# else:
#     sanity_check = opt.sanity_check

if opt.sanity_check != False:
    sanity_check = opt.sanity_check.split(',')

nuisances = ""
if opt.freeze_nuisances == "True" or opt.freeze_nuisances == "1" or opt.freeze_nuisances == "all":
    nuisances = "--freezeParameters allConstrainedNuisances"
if opt.freeze_nuisances == "r_higgs":
    nuisances = "--freezeParameters r_higgs"

only_workspace = False
if opt.only_workspace == "True" or opt.only_workspace == "1":
    only_workspace = True

only_fit = False
if opt.only_fit == "True" or opt.only_fit == "1":
    only_fit = True

channel_mask = ""
if opt.channel_mask != False:
    mask = opt.channel_mask.split(",")
    masked_channels = ['mask_' + m for m in mask]
    masked_channels_one = [m + '=1' for m in masked_channels]
    channel_mask = ','.join(masked_channels_one)
    
####################    
### Create workspace
####################

# Using POIs: r_S, r_A
workspace_command = f"text2workspace.py \
                     {datacard_name}.txt \
                     -o {datacard_name}.root \
                     -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
                     -m 125 \
                     --PO verbose \
                     --PO 'map=.*/ggH_hww:r_higgs[1,0.99,1.01]' \
                     --PO 'map=.*/qqH_hww:r_higgs[1,0.99,1.01]' \
                     --PO 'map=.*/ZH_hww:r_higgs[1,0.99,1.01]' \
                     --PO 'map=.*/ggZH_hww:r_higgs[1,0.99,1.01]' \
                     --PO 'map=.*/ttH_hww:r_higgs[1,0.99,1.01]' \
                     --PO 'map=.*/ggH_htt:r_higgs[1,0.99,1.01]' \
                     --PO 'map=.*/qqH_htt:r_higgs[1,0.99,1.01]' \
                     --PO 'map=.*/ZH_htt:r_higgs[1,0.99,1.01]' \
                     --PO 'map=.*/WH_h.*_plus:r_WH_plus=expr;;r_WH_plus(\"@0*(1+@1)/(2*0.8380)\",r_S[1.3693,-10,10],r_A[0.224,-10,10])' \
                     --PO 'map=.*/WH_h.*_minus:r_WH_minus=expr;;r_WH_minus(\"@0*(1-@1)/(2*0.5313)\",r_S,r_A)'"
#                     --PO 'map=.*/WH_h.*_minus:r_WH_minus=expr;;r_WH_minus(\"(@0-@1*0.8380)/0.5313\",r_S,r_WH_plus)' \

# Using only one POI for the total WH signal strength
workspace_command_WH = f"text2workspace.py \
                        {datacard_name}.txt \
                        -o {datacard_name}_WH_strength.root \
                        -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
                        -m 125 \
                        --PO verbose \
                        --PO 'map=.*/ggH_hww:r_higgs[1,0.99,1.01]' \
                        --PO 'map=.*/qqH_hww:r_higgs[1,0.99,1.01]' \
                        --PO 'map=.*/ZH_hww:r_higgs[1,0.99,1.01]' \
                        --PO 'map=.*/ggZH_hww:r_higgs[1,0.99,1.01]' \
                        --PO 'map=.*/ttH_hww:r_higgs[1,0.99,1.01]' \
                        --PO 'map=.*/ggH_htt:r_higgs[1,0.99,1.01]' \
                        --PO 'map=.*/qqH_htt:r_higgs[1,0.99,1.01]' \
                        --PO 'map=.*/ZH_htt:r_higgs[1,0.99,1.01]' \
                        --PO 'map=.*/WH_h.*_plus:r_WH[1,-10.0,10.0]' \
                        --PO 'map=.*/WH_h.*_minus:r_WH[1,-10.0,10.0]'"

# Using POIs: r_WH_plus, r_WH_minus
workspace_command_WH_plus_minus = f"text2workspace.py \
                                   {datacard_name}.txt \
                                   -o {datacard_name}_WH_plus_minus.root \
                                   -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel \
                                   -m 125 \
                                   --PO verbose \
                                   --PO 'map=.*/ggH_hww:r_higgs[1,0.99,1.01]' \
                                   --PO 'map=.*/qqH_hww:r_higgs[1,0.99,1.01]' \
                                   --PO 'map=.*/ZH_hww:r_higgs[1,0.99,1.01]' \
                                   --PO 'map=.*/ggZH_hww:r_higgs[1,0.99,1.01]' \
                                   --PO 'map=.*/ttH_hww:r_higgs[1,0.99,1.01]' \
                                   --PO 'map=.*/ggH_htt:r_higgs[1,0.99,1.01]' \
                                   --PO 'map=.*/qqH_htt:r_higgs[1,0.99,1.01]' \
                                   --PO 'map=.*/ZH_htt:r_higgs[1,0.99,1.01]' \
                                   --PO 'map=.*/WH_h.*_plus:r_WH_plus[1,-10.0,10.0]' \
                                   --PO 'map=.*/WH_h.*_minus:r_WH_minus[1,-10.0,10.0]'"


################
### Actually fit
################

# Fit to get the asymmetry value
combine_command = f"combine \
                   -M MultiDimFit \
                   --algo=singles \
                   -d {datacard_name}.root \
                   --cminDefaultMinimizerStrategy 0 \
                   --stepSize 0.01 --cminPreScan \
                   --setParameters r_S=1.3693,r_A=0.224 \
                   --setParameterRanges r_S=-10,10:r_A=-10,10 \
                   --redefineSignalPOIs r_S,r_A \
                   --cminFallbackAlgo Minuit2,0:0.2 \
                   {nuisances} \
                   > {output_name}"

#                   --X-rtd MINIMIZER_analytic \
#                   -v 9 \
#                   --cminPreFit 2

# Fit to get the total WH signal strength
combine_command_WH = f"combine \
                      -M MultiDimFit \
                      --algo=singles \
                      -d {datacard_name}_WH_strength.root \
                      --cminDefaultMinimizerStrategy 0 \
                      --stepSize 0.01 --cminPreScan \
                      --setParameters r_WH=1 \
                      --setParameterRanges r_WH=-10,10 \
                      --redefineSignalPOIs r_WH \
                      --cminFallbackAlgo Minuit2,0:0.2 \
                      {nuisances} \
                      > {output_name.replace('.txt','_WH_strength.txt')}"

                      # --robustFit 1 \

# Fit to get the total two WH signal strengths, for separate
combine_command_WH_plus_minus = f"combine \
                                 -M MultiDimFit \
                                 --algo=singles \
                                 -d {datacard_name}_WH_plus_minus.root \
                                 --cminDefaultMinimizerStrategy 0 \
                                 --stepSize 0.01 --cminPreScan \
                                 --setParameters r_WH_plus=1,r_WH_minus=1 \
                                 --setParameterRanges r_WH_plus=-10,10:r_WH_minus=-10,10 \
                                 --redefineSignalPOIs r_WH_plus,r_WH_minus \
                                 --cminFallbackAlgo Minuit2,0:0.2 \
                                 {nuisances} \
                                 > {output_name.replace('.txt','_WH_plus_minus.txt')}"

# combineTool.py -M MultiDimFit --algo grid -t -1 --setParameters r=1 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy=0 -d ../../globalMu_htt.root -n globalMu_scan --task-name globalMu_scan --autoRange 2 --points 40 --split-points 1 --job-mode=condor --redefineSignalPOIs r --floatOtherPOIs 1
# grid

# Likelihood scan on POIs - focusing on r_A
rA_scan_command = f"combine \
                   -M MultiDimFit \
                   --algo grid \
                   --setParameters r_A=0.224,r_S=1.3693 \
                   -d {datacard_name}.root \
                   -n _r_A_scan \
                   --points 20 \
                   --redefineSignalPOIs r_A,r_S \
                   -P r_A \
                   --floatOtherPOIs 1 \
                   --trackParameters r_S \
                   {nuisances}"

                   # --X-rtd MINIMIZER_analytic \
                   # --cminDefaultMinimizerStrategy=0 \
                   # --task-name globalMu_scan \
                   # --autoRange 2 \
                   # --split-points 1 \
                   # --job-mode=condor \

# Likelihood scan on POIs - focusing on r_WH
rWH_strength_scan_command = f"combine \
                              -M MultiDimFit \
                              --algo grid \
                              --setParameters r_WH=1 \
                              -d {datacard_name}_WH_strength.root \
                              -n _r_WH_scan \
                              --points 20 \
                              --redefineSignalPOIs r_WH \
                              -P r_WH \
                              {nuisances}"

                              # --robustFit 1 \

# Likelihood scan on POIs
likelihood_scan_command = f"combine \
                           -M MultiDimFit \
                           --algo=grid \
                           --points=50 \
                           -d {datacard_name}.root \
                           --setParameters r_S=1.3693,r_A=0.224 \
                           --setParameterRanges r_S=-0.01,5:r_A=-1,1 \
                           --redefineSignalPOIs r_A,r_S \
                           --floatOtherPOIs 1 \
                           {nuisances}"
                           # ,r_higgs 

# Fast likelihood scan of all parameters
prepare_toy_command = f"combine \
                       -M GenerateOnly \
                       -d {datacard_name}.root \
                       --saveToys \
                       --setParameters r_S=1.3693,r_A=0.224"

fast_scan_command = f"combineTool.py \
                     -M FastScan \
                     --robustHesse=1 \
                     -w {datacard_name}.root:w \
                     -d higgsCombineTest.GenerateOnly.mH120.123456.root:toys/toy_asimov"

# Fit diagnostic  
fit_diagnostics_command = f"combine \
                           -M FitDiagnostics {datacard_name}.root \
                           --setParameters r_S=1.3693,r_A=0.224 \
                           --saveShapes \
                           --saveWithUncertainties"

fit_diagnostics_WH_command = f"combine \
                             -M FitDiagnostics {datacard_name}_WH_strength.root \
                             --setParameters r_WH=1 \
                             --saveShapes \
                             --saveWithUncertainties"

# --saveOverallShapes \
# --numToysForShapes 200 \


######################
# Now use the commands
######################

# Asymmetry extraction
if only_fit == False:
    print("Preparing workspace for asymmetry...")
    print(workspace_command)
    os.system(workspace_command)
    print("\n")
    print("\n")

if only_workspace == False:
    print("Fitting the asymmetry value...")
    print(combine_command)
    os.system(combine_command)
    print("\n")
    print("\n")

    print("Moving output to Combine folder...")
    root_output_name = output_name.replace(".txt",".root")
    if (opt.freeze_nuisances) == "1" or (opt.freeze_nuisances) == "True" or (opt.freeze_nuisances) == "all" :
        root_output_name = output_name.replace(".txt","_freeze.root")
    move_command = "mv higgsCombineTest.MultiDimFit.mH120.root {}".format(root_output_name)
    # os.system(move_command)
    print(move_command)
    print("\n")
    print("\n")


# Total signal strength extraction
if only_fit == False:
    print("Preparing workspace for WH signal strength...")
    print(workspace_command_WH)
    os.system(workspace_command_WH)
    print("\n")
    print("\n")

if only_workspace == False:
    print("Fitting the signal strength value...")
    print(combine_command_WH)
    os.system(combine_command_WH)
    print("\n")
    print("\n")

    print("Moving output to Combine folder...")
    root_output_name_WH = output_name.replace(".txt","_WH_strength.root")
    if (opt.freeze_nuisances) == "1" or (opt.freeze_nuisances) == "True"  or (opt.freeze_nuisances) == "all":
        root_output_name_WH = output_name.replace(".txt","_WH_strength_freeze.root")
    move_command = "mv higgsCombineTest.MultiDimFit.mH120.root {}".format(root_output_name_WH)
    # os.system(move_command)
    print(move_command)
    print("\n")
    print("\n")

# Individual WH_plus/WH_minus signal strengths extraction
if only_fit == False:
    print("Preparing workspace for WH_plus/WH_minus signal strengths...")
    print(workspace_command_WH_plus_minus)
    os.system(workspace_command_WH_plus_minus)
    print("\n")
    print("\n")

if only_workspace == False:
    print("Fitting the individual WH_plus/WH_minus signal strengths values...")
    print(combine_command_WH_plus_minus)
    os.system(combine_command_WH_plus_minus)
    print("\n")
    print("\n")

    print("Moving output to Combine folder...")
    root_output_name_WH_plus_minus = output_name.replace(".txt","_WH_plus_minus.root")
    if (opt.freeze_nuisances) == "1" or (opt.freeze_nuisances) == "True" or (opt.freeze_nuisances) == "all":
        root_output_name_WH_plus_minus = output_name.replace(".txt","_WH_plus_minus_freeze.root")
    move_command = "mv higgsCombineTest.MultiDimFit.mH120.root {}".format(root_output_name_WH_plus_minus)
    os.system(move_command)
    print(move_command)
    print("\n")
    print("\n")


# Additional sanity checks
if only_workspace == False:
    print("Sanity checks: {}".format(sanity_check))
    if sanity_check != []:

        # To read output file:
        # limit->Draw("deltaNLL:r_A","r_S < 1.5 && r_S > 0 && r_higgs > 0 && r_higgs < 2.5","colz")
        if "ML" in sanity_check:
            print("Performing likelihood scan on POIs...")
            print(likelihood_scan_command)
            os.system(likelihood_scan_command)
            ML_output_name = output_name.replace(".txt","_ML.root")
            if (opt.freeze_nuisances) == "1" or (opt.freeze_nuisances) == "True" or (opt.freeze_nuisances) == "all":
                ML_output_name = output_name.replace(".txt","_ML_freeze.root")
            move_command = "mv higgsCombineTest.MultiDimFit.mH120.root {}".format(ML_output_name)
            print(move_command)
            os.system(move_command)
            print("\n")
            print("\n")


        if "rA_scan" in sanity_check:
            print("Performing likelihood scan on POIs, focusing on r_A...")
            print(rA_scan_command)
            os.system(rA_scan_command)
            rA_output_name = output_name.replace(".txt","_rA.root")
            if (opt.freeze_nuisances) == "1" or (opt.freeze_nuisances) == "True" or (opt.freeze_nuisances) == "all":
                rA_output_name = output_name.replace(".txt","_rA_freeze.root")
            move_command = "mv higgsCombine_r_A_scan.MultiDimFit.mH120.root {}".format(rA_output_name)
            print(move_command)
            os.system(move_command)
            print("\n")
            print("\n")

        if "rWH_scan" in sanity_check:
            print("Performing likelihood scan on POIs, focusing on r_WH...")
            print(rWH_strength_scan_command)
            os.system(rWH_strength_scan_command)
            rWH_output_name = output_name.replace(".txt","_rWH.root")
            if (opt.freeze_nuisances) == "1" or (opt.freeze_nuisances) == "True" or (opt.freeze_nuisances) == "all":
                rWH_output_name = output_name.replace(".txt","_rWH_freeze.root")
            move_command = "mv higgsCombine_r_WH_scan.MultiDimFit.mH120.root {}".format(rWH_output_name)
            print(move_command)
            os.system(move_command)
            print("\n")
            print("\n")
            

        if "FS" in sanity_check:
            print("Preparing toys for fast likelihood scan on all parameters...")
            print(prepare_toy_command)
            os.system(prepare_toy_command)
            print("\n")
            print("\n")
        
            print("Now doing fast scan...")
            print(fast_scan_command)
            os.system(fast_scan_command)
            print("\n")
            print("\n")

        if "FD" in sanity_check:
            print("Doing FitDiagnistics...")
            print(fit_diagnostics_command)
            os.system(fit_diagnostics_command)
            print("\n")
            print("\n")
            FD_output_name = output_name.replace(".txt","_fitDiagnostics.root")
            if (opt.freeze_nuisances) == "1" or (opt.freeze_nuisances) == "True" or (opt.freeze_nuisances) == "all":
                rA_output_name = output_name.replace(".txt","_fitDiagnostics_freeze.root")
            move_command = "mv fitDiagnosticsTest.root {}".format(FD_output_name)
            print(move_command)
            os.system(move_command)
            print("\n")
            print("\n")

        if "FD_WH_strength" in sanity_check:
            print("Doing FitDiagnistics...")
            print(fit_diagnostics_WH_command)
            os.system(fit_diagnostics_WH_command)
            print("\n")
            print("\n")
            FD_output_name = output_name.replace(".txt","_fitDiagnostics_WH_strength.root")
            if (opt.freeze_nuisances) == "1" or (opt.freeze_nuisances) == "True" or (opt.freeze_nuisances) == "all":
                rA_output_name = output_name.replace(".txt","_fitDiagnostics_WH_strength_freeze.root")
            move_command = "mv fitDiagnosticsTest.root {}".format(FD_output_name)
            print(move_command)
            os.system(move_command)
            print("\n")
            print("\n")
            
