# Combine datacards
python script_datacards_binning_SS_CR.py

# Drop problematic nuisances
echo "nuisance edit drop WH_htt_plus  WH_SS_mm_1j_minus        CMS_scale_met_2018"              >> Combination/WH_chargeAsymmetry_WH_SS_Full2018_v9_SS_CR.txt
echo "nuisance edit drop WH_hww_minus WH_SS_em_1j_plus_low_pt  CMS_scale_j_RelativeBal"         >> Combination/WH_chargeAsymmetry_WH_SS_Full2018_v9_SS_CR.txt
echo "nuisance edit drop WH_hww_minus WH_SS_em_1j_plus_low_pt  CMS_scale_j_RelativeSample_2018" >> Combination/WH_chargeAsymmetry_WH_SS_Full2018_v9_SS_CR.txt
echo "nuisance edit drop WH_hww_minus WH_SS_em_1j_plus_low_pt  CMS_scale_met_2018"              >> Combination/WH_chargeAsymmetry_WH_SS_Full2018_v9_SS_CR.txt
echo "nuisance edit drop WH_hww_plus  WH_SS_ee_1j_minus_low_pt CMS_scale_met_2018"              >> Combination/WH_chargeAsymmetry_WH_SS_Full2018_v9_SS_CR.txt
echo "nuisance edit drop ggH_htt      WH_SS_ee_1j_minus_low_pt CMS_scale_j_Absolute"            >> Combination/WH_chargeAsymmetry_WH_SS_Full2018_v9_SS_CR.txt
echo "nuisance edit drop ggH_htt      WH_SS_ee_1j_minus_low_pt CMS_scale_j_FlavorQCD"           >> Combination/WH_chargeAsymmetry_WH_SS_Full2018_v9_SS_CR.txt
echo "nuisance edit drop ggH_htt      WH_SS_ee_1j_minus_low_pt CMS_scale_j_HF"                  >> Combination/WH_chargeAsymmetry_WH_SS_Full2018_v9_SS_CR.txt
echo "nuisance edit drop ggH_htt      WH_SS_ee_1j_minus_low_pt CMS_scale_j_RelativeBal"         >> Combination/WH_chargeAsymmetry_WH_SS_Full2018_v9_SS_CR.txt
echo "nuisance edit drop ggH_htt      WH_SS_ee_1j_minus_low_pt CMS_scale_j_RelativeSample_2018" >> Combination/WH_chargeAsymmetry_WH_SS_Full2018_v9_SS_CR.txt
echo "nuisance edit drop ggH_hww      WH_SS_ee_1j_plus_low_pt  CMS_scale_met_2018"              >> Combination/WH_chargeAsymmetry_WH_SS_Full2018_v9_SS_CR.txt
echo "nuisance edit drop ggH_hww      WH_SS_ee_1j_plus_low_pt  CMS_scale_met_2018"              >> Combination/WH_chargeAsymmetry_WH_SS_Full2018_v9_SS_CR.txt


# Create workspace and perform fit
python ../../scripts/script_workspace_and_fit.py \
	   --datacard_name Combination/WH_chargeAsymmetry_WH_SS_Full2018_v9_SS_CR \
	   --output_name   Combination/FitResults_binning.txt \
	   --freeze_nuisances r_higgs
