# Combine datacards
mkdir -p Combination/
python script_datacards_binning_SS_CR.py

# Drop problematic nuisances
echo "nuisance edit drop VgS     WH_SS_em_2j_minus_low_pt CMS_btag_cferr1"                 >> Combination/WH_chargeAsymmetry_WH_SS_Full2017_v9_SS_CR.txt
echo "nuisance edit drop VgS     WH_SS_em_2j_minus_low_pt CMS_scale_j_Absolute_2017"       >> Combination/WH_chargeAsymmetry_WH_SS_Full2017_v9_SS_CR.txt
echo "nuisance edit drop VgS     WH_SS_em_2j_minus_low_pt CMS_scale_j_BBEC1"               >> Combination/WH_chargeAsymmetry_WH_SS_Full2017_v9_SS_CR.txt
echo "nuisance edit drop VgS     WH_SS_em_2j_minus_low_pt CMS_scale_j_EC2_2017"            >> Combination/WH_chargeAsymmetry_WH_SS_Full2017_v9_SS_CR.txt
echo "nuisance edit drop VgS     WH_SS_em_2j_minus_low_pt CMS_scale_j_RelativeSample_2017" >> Combination/WH_chargeAsymmetry_WH_SS_Full2017_v9_SS_CR.txt
echo "nuisance edit drop VgS     WH_SS_em_2j_minus_low_pt CMS_scale_met_2017"              >> Combination/WH_chargeAsymmetry_WH_SS_Full2017_v9_SS_CR.txt
echo "nuisance edit drop VgS     WH_SS_em_2j_minus_low_pt PS_WH_hww_FSR"                   >> Combination/WH_chargeAsymmetry_WH_SS_Full2017_v9_SS_CR.txt
echo "nuisance edit drop VgS     WH_SS_em_2j_minus_low_pt PS_WH_hww_ISR"                   >> Combination/WH_chargeAsymmetry_WH_SS_Full2017_v9_SS_CR.txt
echo "nuisance edit drop VVV     WH_SS_mm_2j_minus_low_pt PS_WH_hww_FSR"                   >> Combination/WH_chargeAsymmetry_WH_SS_Full2017_v9_SS_CR.txt
echo "nuisance edit drop Fake_ee WH_SS_ee_2j_plus_low_pt  CMS_WH_hww_fake_stat_e_2017"     >> Combination/WH_chargeAsymmetry_WH_SS_Full2017_v9_SS_CR.txt
echo "nuisance edit drop Vg      WH_SS_ee_2j_SS_CR_minus  CMS_scale_j_RelativeBal"         >> Combination/WH_chargeAsymmetry_WH_SS_Full2017_v9_SS_CR.txt
echo "nuisance edit drop Vg      WH_SS_ee_2j_SS_CR_minus  CMS_scale_j_RelativeSample_2017" >> Combination/WH_chargeAsymmetry_WH_SS_Full2017_v9_SS_CR.txt
echo "nuisance edit drop Vg      WH_SS_ee_2j_SS_CR_minus  CMS_scale_met_2017"              >> Combination/WH_chargeAsymmetry_WH_SS_Full2017_v9_SS_CR.txt
echo "nuisance edit drop Vg      WH_SS_ee_2j_SS_CR_minus  PS_WH_hww_FSR"                   >> Combination/WH_chargeAsymmetry_WH_SS_Full2017_v9_SS_CR.txt

# Create workspace and perform fit
python ../../scripts/script_workspace_and_fit.py \
	   --datacard_name Combination/WH_chargeAsymmetry_WH_SS_Full2017_v9_SS_CR \
	   --output_name   Combination/FitResults_binning.txt \
	   --freeze_nuisances r_higgs
