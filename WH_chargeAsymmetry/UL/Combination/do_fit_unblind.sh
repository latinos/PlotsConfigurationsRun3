#!/bin/bash
if [ $# -eq 0 ];
then
  echo "$0: Missing arguments"
  exit 1
else
  echo "We got some argument(s)"
  echo "==========================="
  echo "Number of arguments. : $#"
  echo "List of arguments... : $@"
  echo "Arg #1: Final State  : $1"
  echo "==========================="
  FINAL_STATE=$1
fi

### Prepare list of channels
WHSS_2018_HIGH_PT=WH_SS_em_1j_minus_2018,WH_SS_em_1j_plus_2018,WH_SS_mm_1j_minus_2018,WH_SS_mm_1j_plus_2018,WH_SS_ee_1j_minus_2018,WH_SS_ee_1j_plus_2018,WH_SS_em_2j_minus_2018,WH_SS_em_2j_plus_2018,WH_SS_mm_2j_minus_2018,WH_SS_mm_2j_plus_2018,WH_SS_ee_2j_minus_2018,WH_SS_ee_2j_plus_2018,WH_SS_WZ_1j_2018,WH_SS_WZ_2j_2018

WHSS_2018_LOW_PT=WH_SS_em_1j_minus_low_pt_2018,WH_SS_em_1j_plus_low_pt_2018,WH_SS_mm_1j_minus_low_pt_2018,WH_SS_mm_1j_plus_low_pt_2018,WH_SS_ee_1j_minus_low_pt_2018,WH_SS_ee_1j_plus_low_pt_2018,WH_SS_em_2j_minus_low_pt_2018,WH_SS_em_2j_plus_low_pt_2018,WH_SS_mm_2j_minus_low_pt_2018,WH_SS_mm_2j_plus_low_pt_2018,WH_SS_ee_2j_minus_low_pt_2018,WH_SS_ee_2j_plus_low_pt_2018

WH3l_2018=WH_3l_sssf_plus_2018,WH_3l_sssf_minus_2018,WH_3l_ossf_plus_2018,WH_3l_ossf_minus_2018,WH_3l_WZ_CR_0j_2018


WHSS_2017_HIGH_PT=WH_SS_em_1j_minus_2017,WH_SS_em_1j_plus_2017,WH_SS_mm_1j_minus_2017,WH_SS_mm_1j_plus_2017,WH_SS_ee_1j_minus_2017,WH_SS_ee_1j_plus_2017,WH_SS_em_2j_minus_2017,WH_SS_em_2j_plus_2017,WH_SS_mm_2j_minus_2017,WH_SS_mm_2j_plus_2017,WH_SS_ee_2j_minus_2017,WH_SS_ee_2j_plus_2017,WH_SS_WZ_1j_2017,WH_SS_WZ_2j_2017

WHSS_2017_LOW_PT=WH_SS_em_1j_minus_low_pt_2017,WH_SS_em_1j_plus_low_pt_2017,WH_SS_mm_1j_minus_low_pt_2017,WH_SS_mm_1j_plus_low_pt_2017,WH_SS_ee_1j_minus_low_pt_2017,WH_SS_ee_1j_plus_low_pt_2017,WH_SS_em_2j_minus_low_pt_2017,WH_SS_em_2j_plus_low_pt_2017,WH_SS

WH3l_2017=WH_3l_sssf_plus_2017,WH_3l_sssf_minus_2017,WH_3l_ossf_plus_2017,WH_3l_ossf_minus_2017,WH_3l_WZ_CR_0j_2017


WHSS_2016noHIPM_HIGH_PT=WH_SS_em_1j_minus_2016noHIPM,WH_SS_em_1j_plus_2016noHIPM,WH_SS_mm_1j_minus_2016noHIPM,WH_SS_mm_1j_plus_2016noHIPM,WH_SS_ee_1j_minus_2016noHIPM,WH_SS_ee_1j_plus_2016noHIPM,WH_SS_em_2j_minus_2016noHIPM,WH_SS_em_2j_plus_2016noHIPM,WH_SS_mm_2j_minus_2016noHIPM,WH_SS_mm_2j_plus_2016noHIPM,WH_SS_ee_2j_minus_2016noHIPM,WH_SS_ee_2j_plus_2016noHIPM,WH_SS_WZ_1j_2016noHIPM,WH_SS_WZ_2j_2016noHIPM

WHSS_2016noHIPM_LOW_PT=WH_SS_em_1j_minus_low_pt_2016noHIPM,WH_SS_em_1j_plus_low_pt_2016noHIPM,WH_SS_mm_1j_minus_low_pt_2016noHIPM,WH_SS_mm_1j_plus_low_pt_2016noHIPM,WH_SS_ee_1j_minus_low_pt_2016noHIPM,WH_SS_ee_1j_plus_low_pt_2016noHIPM,WH_SS_em_2j_minus_low_pt_2016noHIPM,WH_SS_em_2j_plus_low_pt_2016noHIPM,WH_SS_mm_2j_minus_low_pt_2016noHIPM,WH_SS_mm_2j_plus_low_pt_2016noHIPM,WH_SS_ee_2j_minus_low_pt_2016noHIPM,WH_SS_ee_2j_plus_low_pt_2016noHIPM

WH3l_2016noHIPM=WH_3l_sssf_plus_2016noHIPM,WH_3l_sssf_minus_2016noHIPM,WH_3l_ossf_plus_2016noHIPM,WH_3l_ossf_minus_2016noHIPM,WH_3l_WZ_CR_0j_2016noHIPM


WHSS_2016HIPM_HIGH_PT=WH_SS_em_1j_minus_2016HIPM,WH_SS_em_1j_plus_2016HIPM,WH_SS_mm_1j_minus_2016HIPM,WH_SS_mm_1j_plus_2016HIPM,WH_SS_ee_1j_minus_2016HIPM,WH_SS_ee_1j_plus_2016HIPM,WH_SS_em_2j_minus_2016HIPM,WH_SS_em_2j_plus_2016HIPM,WH_SS_mm_2j_minus_2016HIPM,WH_SS_mm_2j_plus_2016HIPM,WH_SS_ee_2j_minus_2016HIPM,WH_SS_ee_2j_plus_2016HIPM,WH_SS_WZ_1j_2016HIPM,WH_SS_WZ_2j_2016HIPM

WHSS_2016HIPM_LOW_PT=WH_SS_em_1j_minus_low_pt_2016HIPM,WH_SS_em_1j_plus_low_pt_2016HIPM,WH_SS_mm_1j_minus_low_pt_2016HIPM,WH_SS_mm_1j_plus_low_pt_2016HIPM,WH_SS_ee_1j_minus_low_pt_2016HIPM,WH_SS_ee_1j_plus_low_pt_2016HIPM,WH_SS_em_2j_minus_low_pt_2016HIPM,WH_SS_em_2j_plus_low_pt_2016HIPM,WH_SS_mm_2j_minus_low_pt_2016HIPM,WH_SS_mm_2j_plus_low_pt_2016HIPM,WH_SS_ee_2j_minus_low_pt_2016HIPM,WH_SS_ee_2j_plus_low_pt_2016HIPM

WH3l_2016HIPM=WH_3l_sssf_plus_2016HIPM,WH_3l_sssf_minus_2016HIPM,WH_3l_ossf_plus_2016HIPM,WH_3l_ossf_minus_2016HIPM,WH_3l_WZ_CR_0j_2016HIPM


### Create workspace and perform fit

# Full Run 2
if [ $FINAL_STATE == FullRun2 ]; then
	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning \
			--output_name   Combination/FitResults_binning_unblind.txt \
			--freeze_nuisances r_higgs \
			--only_fit 1

###########
	
# Full 2018
elif [ $FINAL_STATE == Full2018 ]; then
	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning \
			--output_name   Combination/FitResults_binning_unblind_Full2018.txt \
			--freeze_nuisances r_higgs \
			--only_fit 1 \
			--channel_mask ${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}

# Full 2018 no low pT
elif [ $FINAL_STATE == Full2018_no_low_pt ]; then
	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning \
			--output_name   Combination/FitResults_binning_unblind_Full2018_no_low_pt.txt \
			--freeze_nuisances r_higgs \
			--only_fit 1 \
			--channel_mask ${WHSS_2018_LOW_PT},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
	
# Full 2018 WHSS
elif [ $FINAL_STATE == Full2018_WHSS ]; then
	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning \
			--output_name   Combination/FitResults_binning_unblind_Full2018_WHSS.txt \
			--freeze_nuisances r_higgs \
			--only_fit 1 \
			--channel_mask ${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}

# Full 2018 WHSS no low pT
elif [ $FINAL_STATE == Full2018_WHSS_no_low_pt ]; then
	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning \
			--output_name   Combination/FitResults_binning_unblind_Full2018_WHSS_no_low_pt.txt \
			--freeze_nuisances r_higgs \
			--only_fit 1 \
			--channel_mask ${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
	
# Full 2018 WH3l
elif [ $FINAL_STATE == Full2018_WH3l ]; then
	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning \
			--output_name   Combination/FitResults_binning_unblind_Full2018_WH3l.txt \
			--freeze_nuisances r_higgs \
			--only_fit 1 \
			--channel_mask ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}

###########

# Full 2017
elif [ $FINAL_STATE == Full2017 ]; then
	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning \
			--output_name   Combination/FitResults_binning_unblind_Full2017.txt \
			--freeze_nuisances r_higgs \
			--only_fit 1 \
			--channel_mask ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}

# Full 2017 no low pT
elif [ $FINAL_STATE == Full2017_no_low_pt ]; then
	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning \
			--output_name   Combination/FitResults_binning_unblind_Full2017_no_low_pt.txt \
			--freeze_nuisances r_higgs \
			--only_fit 1 \
			--channel_mask ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_LOW_PT},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
	
# Full 2017 WHSS
elif [ $FINAL_STATE == Full2017_WHSS ]; then
	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning \
			--output_name   Combination/FitResults_binning_unblind_Full2017_WHSS.txt \
			--freeze_nuisances r_higgs \
			--only_fit 1 \
			--channel_mask ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}

# Full 2017 WHSS no low pT
elif [ $FINAL_STATE == Full2017_WHSS_no_low_pt ]; then
	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning \
			--output_name   Combination/FitResults_binning_unblind_Full2017_WHSS_no_low_pt.txt \
			--freeze_nuisances r_higgs \
			--only_fit 1 \
			--channel_mask ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
	
# Full 2017 WH3l
elif [ $FINAL_STATE == Full2017_WH3l ]; then
	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning \
			--output_name   Combination/FitResults_binning_unblind_Full2017_WH3l.txt \
			--freeze_nuisances r_higgs \
			--only_fit 1 \
			--channel_mask ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}

###########

# 2016 no HIPM
elif [ $FINAL_STATE == 2016noHIPM ]; then
	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning \
			--output_name   Combination/FitResults_binning_unblind_2016noHIPM.txt \
			--freeze_nuisances r_higgs \
			--only_fit 1 \
			--channel_mask ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}

# 2016 no HIPM no low pT
elif [ $FINAL_STATE == 2016noHIPM_no_low_pt ]; then
	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning \
			--output_name   Combination/FitResults_binning_unblind_2016noHIPM_no_low_pt.txt \
			--freeze_nuisances r_higgs \
			--only_fit 1 \
			--channel_mask ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_LOW_PT},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
	
# 2016 no HIPM WHSS
elif [ $FINAL_STATE == 2016noHIPM_WHSS ]; then
	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning \
			--output_name   Combination/FitResults_binning_unblind_2016noHIPM_WHSS.txt \
			--freeze_nuisances r_higgs \
			--only_fit 1 \
			--channel_mask ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}

# 2016 no HIPM WHSS no low pT
elif [ $FINAL_STATE == 2016noHIPM_WHSS_no_low_pt ]; then
	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning \
			--output_name   Combination/FitResults_binning_unblind_2016noHIPM_WHSS_no_low_pt.txt \
			--freeze_nuisances r_higgs \
			--only_fit 1 \
			--channel_mask ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
	
# 2016 no HIPM WH3l
elif [ $FINAL_STATE == 2016noHIPM_WH3l ]; then
	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning \
			--output_name   Combination/FitResults_binning_unblind_2016noHIPM_WH3l.txt \
			--freeze_nuisances r_higgs \
			--only_fit 1 \
			--channel_mask ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}

###########

# 2016 HIPM
elif [ $FINAL_STATE == 2016HIPM ]; then
	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning \
			--output_name   Combination/FitResults_binning_unblind_2016HIPM.txt \
			--freeze_nuisances r_higgs \
			--only_fit 1 \
			--channel_mask ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM}
	
# 2016 HIPM no low pT
elif [ $FINAL_STATE == 2016HIPM_no_low_pt ]; then
	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning \
			--output_name   Combination/FitResults_binning_unblind_2016HIPM_no_low_pt.txt \
			--freeze_nuisances r_higgs \
			--only_fit 1 \
			--channel_mask ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_LOW_PT}
	
# 2016 HIPM WHSS
elif [ $FINAL_STATE == 2016HIPM_WHSS ]; then
	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning \
			--output_name   Combination/FitResults_binning_unblind_2016HIPM_WHSS.txt \
			--freeze_nuisances r_higgs \
			--only_fit 1 \
			--channel_mask ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WH3l_2016HIPM}

# 2016 HIPM WHSS no low pT
elif [ $FINAL_STATE == 2016HIPM_WHSS_no_low_pt ]; then
	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning \
			--output_name   Combination/FitResults_binning_unblind_2016HIPM_WHSS_no_low_pt.txt \
			--freeze_nuisances r_higgs \
			--only_fit 1 \
			--channel_mask ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_LOW_PT},${WH3l_2016HIPM}
	
# 2016 HIPM WH3l
elif [ $FINAL_STATE == 2016HIPM_WH3l ]; then
	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_FullRun2_v9_binning \
			--output_name   Combination/FitResults_binning_unblind_2016HIPM_WH3l.txt \
			--freeze_nuisances r_higgs \
			--only_fit 1 \
			--channel_mask ${WHSS_2018_HIGH_PT},${WHSS_2018_LOW_PT},${WH3l_2018},${WHSS_2017_HIGH_PT},${WHSS_2017_LOW_PT},${WH3l_2017},${WHSS_2016noHIPM_HIGH_PT},${WHSS_2016noHIPM_LOW_PT},${WH3l_2016noHIPM},${WHSS_2016HIPM_HIGH_PT},${WHSS_2016HIPM_LOW_PT}
	
###########
	
else
	echo "I still don't know this final state"
	exit 1
fi
