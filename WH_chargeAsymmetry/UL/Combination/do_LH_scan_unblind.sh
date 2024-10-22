cd $HOME/work/combine/CMSSW_14_1_0_pre4/src/
eval `scramv1 ru -sh`
cd -
ulimit -s unlimited

alias python=python3

# Considering all systematics:
python3 ../scripts/script_workspace_and_fit_unblind.py \
		--datacard_name=Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning_WH_strength \
		--output_name=Combination/FitResults_WH_FullRun2_v9_binning_WH_strength_unblind.txt \
        --freeze_nuisances=r_higgs \
		--sanity_check=r_WH_scan \
		--only_fit 1
		
# Freezing all systematic effects and leaving only the statistical uncertainty:
python3 ../scripts/script_workspace_and_fit_unblind.py \
		--datacard_name=Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning_WH_strength \
		--output_name=Combination/FitResults_WH_FullRun2_v9_binning_WH_strength_unblind_freeze_all.txt \
		--freeze_nuisances all \
		--sanity_check=r_WH_scan \
		--only_fit 1

# Produce likelihood scan plots:
plot1DScan.py Combination/FitResults_WH_FullRun2_v9_binning_rA.root --main-label "All syst" \
    --others 'Combination/FitResults_WH_FullRun2_v9_binning_freeze_all_rA_freeze.root:Stat only:600' \
    -o scan1D_binning --POI r_A  --y-max 3.5 
