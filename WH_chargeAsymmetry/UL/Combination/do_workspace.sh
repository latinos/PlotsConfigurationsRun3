### Combine datacards
python3 script_combine_datacards_binning.py

### Drop problematic nuisances

# WHSS 2018
echo "nuisance edit drop WH_htt_plus  WH_SS_mm_1j_minus_2018        CMS_scale_met_2018"              >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt
echo "nuisance edit drop WH_hww_minus WH_SS_em_1j_plus_low_pt_2018  CMS_scale_j_RelativeBal"         >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt
echo "nuisance edit drop WH_hww_minus WH_SS_em_1j_plus_low_pt_2018  CMS_scale_j_RelativeSample_2018" >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt
echo "nuisance edit drop WH_hww_minus WH_SS_em_1j_plus_low_pt_2018  CMS_scale_met_2018"              >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt
echo "nuisance edit drop WH_hww_plus  WH_SS_ee_1j_minus_low_pt_2018 CMS_scale_met_2018"              >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt
echo "nuisance edit drop ggH_htt      WH_SS_ee_1j_minus_low_pt_2018 CMS_scale_j_Absolute"            >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt
echo "nuisance edit drop ggH_htt      WH_SS_ee_1j_minus_low_pt_2018 CMS_scale_j_FlavorQCD"           >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt
echo "nuisance edit drop ggH_htt      WH_SS_ee_1j_minus_low_pt_2018 CMS_scale_j_HF"                  >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt
echo "nuisance edit drop ggH_htt      WH_SS_ee_1j_minus_low_pt_2018 CMS_scale_j_RelativeBal"         >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt
echo "nuisance edit drop ggH_htt      WH_SS_ee_1j_minus_low_pt_2018 CMS_scale_j_RelativeSample_2018" >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt
echo "nuisance edit drop ggH_hww      WH_SS_ee_1j_plus_low_pt_2018  CMS_scale_met_2018"              >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt
echo "nuisance edit drop ggH_hww      WH_SS_ee_1j_plus_low_pt_2018  CMS_scale_met_2018"              >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt

# WHSS 2017
echo "nuisance edit drop VgS     WH_SS_em_2j_minus_low_pt_2017 CMS_btag_cferr1"                 >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt
echo "nuisance edit drop VgS     WH_SS_em_2j_minus_low_pt_2017 CMS_scale_j_Absolute_2017"       >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt
echo "nuisance edit drop VgS     WH_SS_em_2j_minus_low_pt_2017 CMS_scale_j_BBEC1"               >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt
echo "nuisance edit drop VgS     WH_SS_em_2j_minus_low_pt_2017 CMS_scale_j_EC2_2017"            >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt
echo "nuisance edit drop VgS     WH_SS_em_2j_minus_low_pt_2017 CMS_scale_j_RelativeSample_2017" >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt
echo "nuisance edit drop VgS     WH_SS_em_2j_minus_low_pt_2017 CMS_scale_met_2017"              >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt
echo "nuisance edit drop VgS     WH_SS_em_2j_minus_low_pt_2017 PS_WH_hww_FSR"                   >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt
echo "nuisance edit drop VgS     WH_SS_em_2j_minus_low_pt_2017 PS_WH_hww_ISR"                   >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt
echo "nuisance edit drop VgS     WH_SS_em_2j_minus_low_pt_2017 QCDscale_VV"                     >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt
echo "nuisance edit drop VVV     WH_SS_mm_2j_minus_low_pt_2017 PS_WH_hww_FSR"                   >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt
echo "nuisance edit drop Fake_ee WH_SS_ee_2j_plus_low_pt_2017  CMS_WH_hww_fake_stat_e_2j_2017"  >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt

# WHSS 2016noHIPM
echo "nuisance edit drop WH_htt_plus WH_SS_em_1j_minus_low_pt_2016noHIPM CMS_scale_met_2016" >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt

# WHSS 2016HIPM
echo "nuisance edit drop Fake_em WH_SS_em_1j_minus_low_pt_2016HIPM CMS_WH_hww_fake_stat_e_1j_2016HIPM" >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt
echo "nuisance edit drop Fake_em WH_SS_em_1j_plus_low_pt_2016HIPM  CMS_WH_hww_fake_stat_e_1j_2016HIPM" >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt
echo "nuisance edit drop Fake_ee WH_SS_ee_1j_minus_low_pt_2016HIPM CMS_WH_hww_fake_stat_e_1j_2016HIPM" >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt
echo "nuisance edit drop Fake_ee WH_SS_ee_1j_plus_low_pt_2016HIPM  CMS_WH_hww_fake_stat_e_1j_2016HIPM" >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt

echo "nuisance edit drop Fake_em WH_SS_em_2j_minus_low_pt_2016HIPM CMS_WH_hww_fake_stat_e_2j_2016HIPM" >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt
echo "nuisance edit drop Fake_em WH_SS_em_2j_plus_low_pt_2016HIPM  CMS_WH_hww_fake_stat_e_2j_2016HIPM" >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt
echo "nuisance edit drop Fake_ee WH_SS_ee_2j_minus_low_pt_2016HIPM CMS_WH_hww_fake_stat_e_2j_2016HIPM" >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt
echo "nuisance edit drop Fake_ee WH_SS_ee_2j_plus_low_pt_2016HIPM  CMS_WH_hww_fake_stat_e_2j_2016HIPM" >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning.txt

### Create workspace
python3 ../scripts/script_workspace_and_fit.py \
		--datacard_name Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning \
		--output_name   Combination/FitResults_binning.txt \
		--freeze_nuisances r_higgs \
		--only_workspace 1
