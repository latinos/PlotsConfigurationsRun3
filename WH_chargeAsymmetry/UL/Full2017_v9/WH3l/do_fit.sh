# Combine datacards
mkdir -p Combination/
python script_datacards_binning.py

python ../../scripts/script_workspace_and_fit.py \
	   --datacard_name Combination/WH_chargeAsymmetry_WH_3l_Full2017_v9 \
	   --output_name   Combination/FitResults_binning.txt \
	   --freeze_nuisances r_higgs
