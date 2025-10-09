### Combine datacards
python3 script_combine_datacards_binning.py

### Drop problematic nuisances

# WHSS 2018
echo "nuisance edit drop WH_htt_plus  WH_SS_mm_1j_minus_2018        CMS_scale_met_2018"              >> Combination/WH_chargeAsymmetry_WH_Full2018_v9_highpt_binning.txt

### Create workspace
python3 ../scripts/script_workspace_and_fit.py \
		--datacard_name Combination/WH_chargeAsymmetry_WH_Full2018_v9_highpt_binning \
		--output_name   Combination/FitResults_Full2018_v9_highpt_binning.txt \
		--freeze_nuisances r_higgs \
		--only_workspace 1
