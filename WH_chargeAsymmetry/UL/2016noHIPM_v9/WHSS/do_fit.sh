# Combine datacards
mkdir -p Combination/
python script_datacards_binning_SS_CR.py

# Drop problematic nuisances
echo "nuisance edit drop WH_htt_plus WH_SS_em_1j_minus_low_pt CMS_scale_met_2016"     >> Combination/WH_chargeAsymmetry_WH_SS_2016noHIPM_v9_SS_CR.txt

# Create workspace and perform fit
python ../../scripts/script_workspace_and_fit.py \
	   --datacard_name Combination/WH_chargeAsymmetry_WH_SS_2016noHIPM_v9_SS_CR \
	   --output_name   Combination/FitResults_binning.txt \
	   --freeze_nuisances r_higgs
