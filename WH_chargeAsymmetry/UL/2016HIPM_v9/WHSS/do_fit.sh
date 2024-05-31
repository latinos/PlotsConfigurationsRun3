# Combine datacards
mkdir -p Combination/
python script_datacards_binning_SS_CR.py

# Create workspace and perform fit
python ../../scripts/script_workspace_and_fit.py \
	   --datacard_name Combination/WH_chargeAsymmetry_WH_SS_2016HIPM_v9_SS_CR \
	   --output_name   Combination/FitResults_binning.txt \
	   --freeze_nuisances r_higgs
