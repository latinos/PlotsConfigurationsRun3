#!/bin/bash
if [ $# -eq 0 ];
then
  echo "$0: Missing arguments. Please specify the final state:"
  echo ""
  echo "bash do_fit.sh FullRun2_high_pt"
  echo "bash do_fit.sh FullRun2_WHSS_high_pt"
  echo "bash do_fit.sh FullRun2_WH3l"
  echo ""
  echo "bash do_fit.sh 2017_2018_high_pt"
  echo "bash do_fit.sh 2017_2018_WHSS_high_pt"
  echo "bash do_fit.sh 2017_2018_WH3l"
  echo ""
  echo "bash do_fit.sh 2016noHIPM_2017_2018_high_pt"
  echo "bash do_fit.sh 2016noHIPM_2017_2018_WHSS_high_pt"
  echo "bash do_fit.sh 2016noHIPM_2017_2018_WH3l"
  echo ""
  echo "bash do_fit.sh 2016HIPM_2017_2018_high_pt"
  echo "bash do_fit.sh 2016HIPM_2017_2018_WHSS_high_pt"
  echo "bash do_fit.sh 2016HIPM_2017_2018_WH3l"
  echo ""
  echo "bash do_fit.sh Full2016_high_pt"
  echo "bash do_fit.sh Full2016_WHSS_high_pt"
  echo "bash do_fit.sh Full2016_WH3l"
  echo ""
  echo "bash do_fit.sh Full2018_high_pt"
  echo "bash do_fit.sh Full2018_high_pt_noCR"
  echo "bash do_fit.sh 2018_WHSS_high_pt"
  echo "bash do_fit.sh 2018_WHSS_high_pt_noCR"
  echo "bash do_fit.sh 2018_WH3l"
  echo "bash do_fit.sh 2018_WH3l_noCR"
  echo ""
  echo "bash do_fit.sh Full2017_high_pt"
  echo "bash do_fit.sh 2017_WHSS_high_pt"
  echo "bash do_fit.sh 2017_WH3l"
  echo ""
  echo "bash do_fit.sh 2016noHIPM_high_pt"
  echo "bash do_fit.sh 2016noHIPM_WHSS_high_pt"
  echo "bash do_fit.sh 2016noHIPM_WH3l"
  echo ""
  echo "bash do_fit.sh 2016HIPM_high_pt"
  echo "bash do_fit.sh 2016HIPM_WHSS_high_pt"
  echo "bash do_fit.sh 2016HIPM_WH3l"
  echo ""
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

##################
### Full Run 2 ###
##################

if [ $FINAL_STATE == FullRun2_high_pt ]; then
	python3 script_combine_datacards_binning.py

	echo "nuisance edit drop WH_htt_plus  WH_SS_mm_1j_minus_2018 CMS_scale_met_2018" >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_high_pt_binning.txt

	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_FullRun2_v9_high_pt_binning \
			--output_name   Combination/FitResults_FullRun2_high_pt_binning.txt \
			--freeze_nuisances r_higgs

elif [ $FINAL_STATE == FullRun2_WHSS_high_pt ]; then
	python3 script_combine_datacards_binning.py

	echo "nuisance edit drop WH_htt_plus  WH_SS_mm_1j_minus_2018 CMS_scale_met_2018" >> Combination/WH_chargeAsymmetry_WH_FullRun2_v9_WHSS_high_pt_binning.txt

	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_FullRun2_v9_WHSS_high_pt_binning \
			--output_name   Combination/FitResults_FullRun2_WHSS_high_pt_binning.txt \
			--freeze_nuisances r_higgs

elif [ $FINAL_STATE == FullRun2_WH3l ]; then
	python3 script_combine_datacards_binning.py

	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_FullRun2_v9_WH3l_binning \
			--output_name   Combination/FitResults_FullRun2_WH3l_binning.txt \
			--freeze_nuisances r_higgs
	
###################
### 2017 + 2018 ###
###################

elif [ $FINAL_STATE == 2017_2018_high_pt ]; then
	python3 script_combine_datacards_binning.py

	echo "nuisance edit drop WH_htt_plus  WH_SS_mm_1j_minus_2018 CMS_scale_met_2018" >> Combination/WH_chargeAsymmetry_WH_2017_2018_v9_high_pt_binning.txt

	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_2017_2018_v9_high_pt_binning \
			--output_name   Combination/FitResults_2017_2018_high_pt_binning.txt \
			--freeze_nuisances r_higgs

elif [ $FINAL_STATE == 2017_2018_WHSS_high_pt ]; then
	python3 script_combine_datacards_binning.py

	echo "nuisance edit drop WH_htt_plus  WH_SS_mm_1j_minus_2018 CMS_scale_met_2018" >> Combination/WH_chargeAsymmetry_WH_2017_2018_v9_WHSS_high_pt_binning.txt

	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_2017_2018_v9_WHSS_high_pt_binning \
			--output_name   Combination/FitResults_2017_2018_WHSS_high_pt_binning.txt \
			--freeze_nuisances r_higgs

elif [ $FINAL_STATE == 2017_2018_WH3l ]; then
	python3 script_combine_datacards_binning.py

	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_2017_2018_v9_WH3l_binning \
			--output_name   Combination/FitResults_2017_2018_WH3l_binning.txt \
			--freeze_nuisances r_higgs

################################
### 2016noHIPM + 2017 + 2018 ###
################################

elif [ $FINAL_STATE == 2016noHIPM_2017_2018_high_pt ]; then
	python3 script_combine_datacards_binning.py

	echo "nuisance edit drop WH_htt_plus  WH_SS_mm_1j_minus_2018 CMS_scale_met_2018" >> Combination/WH_chargeAsymmetry_WH_2016noHIPM_2017_2018_v9_high_pt_binning.txt

	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_2016noHIPM_2017_2018_v9_high_pt_binning \
			--output_name   Combination/FitResults_2016noHIPM_2017_2018_high_pt_binning.txt \
			--freeze_nuisances r_higgs

elif [ $FINAL_STATE == 2016noHIPM_2017_2018_WHSS_high_pt ]; then
	python3 script_combine_datacards_binning.py

	echo "nuisance edit drop WH_htt_plus  WH_SS_mm_1j_minus_2018 CMS_scale_met_2018" >> Combination/WH_chargeAsymmetry_WH_2016noHIPM_2017_2018_v9_WHSS_high_pt_binning.txt

	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_2016noHIPM_2017_2018_v9_WHSS_high_pt_binning \
			--output_name   Combination/FitResults_2016noHIPM_2017_2018_WHSS_high_pt_binning.txt \
			--freeze_nuisances r_higgs

elif [ $FINAL_STATE == 2016noHIPM_2017_2018_WH3l ]; then
	python3 script_combine_datacards_binning.py

	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_2016noHIPM_2017_2018_v9_WH3l_binning \
			--output_name   Combination/FitResults_2016noHIPM_2017_2018_WH3l_binning.txt \
			--freeze_nuisances r_higgs
	
################################
### 2016HIPM + 2017 + 2018 ###
################################

elif [ $FINAL_STATE == 2016HIPM_2017_2018_high_pt ]; then
	python3 script_combine_datacards_binning.py

	echo "nuisance edit drop WH_htt_plus  WH_SS_mm_1j_minus_2018 CMS_scale_met_2018" >> Combination/WH_chargeAsymmetry_WH_2016HIPM_2017_2018_v9_high_pt_binning.txt

	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_2016HIPM_2017_2018_v9_high_pt_binning \
			--output_name   Combination/FitResults_2016HIPM_2017_2018_high_pt_binning.txt \
			--freeze_nuisances r_higgs

elif [ $FINAL_STATE == 2016HIPM_2017_2018_WHSS_high_pt ]; then
	python3 script_combine_datacards_binning.py

	echo "nuisance edit drop WH_htt_plus  WH_SS_mm_1j_minus_2018 CMS_scale_met_2018" >> Combination/WH_chargeAsymmetry_WH_2016HIPM_2017_2018_v9_WHSS_high_pt_binning.txt

	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_2016HIPM_2017_2018_v9_WHSS_high_pt_binning \
			--output_name   Combination/FitResults_2016HIPM_2017_2018_WHSS_high_pt_binning.txt \
			--freeze_nuisances r_higgs

elif [ $FINAL_STATE == 2016HIPM_2017_2018_WH3l ]; then
	python3 script_combine_datacards_binning.py

	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_2016HIPM_2017_2018_v9_WH3l_binning \
			--output_name   Combination/FitResults_2016HIPM_2017_2018_WH3l_binning.txt \
			--freeze_nuisances r_higgs

#################			
### Full 2016 ###
#################
			
# Full 2016 high pT
elif [ $FINAL_STATE == Full2016_high_pt ]; then
	python3 script_combine_datacards_binning.py

	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_Full2016_v9_high_pt_binning \
			--output_name   Combination/FitResults_Full2016_high_pt_binning.txt \
			--freeze_nuisances r_higgs
	
# Full 2016 WHSS high pT
elif [ $FINAL_STATE == 2016_WHSS_high_pt ]; then
	python3 script_combine_datacards_binning.py

	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_Full2016_v9_WHSS_high_pt_binning \
			--output_name   Combination/FitResults_Full2016_WHSS_high_pt_binning.txt \
			--freeze_nuisances r_higgs

# Full 2016 WH3l
elif [ $FINAL_STATE == 2016_WH3l ]; then
	python3 script_combine_datacards_binning.py

	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_Full2016_v9_WH3l_binning \
			--output_name   Combination/FitResults_Full2016_WH3l_binning.txt \
			--freeze_nuisances r_higgs

	
#################
### Full 2018 ###
#################
	
# Full 2018 high pT
elif [ $FINAL_STATE == Full2018_high_pt ]; then
	python3 script_combine_datacards_binning.py

	echo "nuisance edit drop WH_htt_plus  WH_SS_mm_1j_minus_2018 CMS_scale_met_2018" >> Combination/WH_chargeAsymmetry_WH_Full2018_v9_high_pt_binning.txt

	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_Full2018_v9_high_pt_binning \
			--output_name   Combination/FitResults_Full2018_high_pt_binning.txt \
			--freeze_nuisances r_higgs

# Full 2018 high pT no WZ CR
elif [ $FINAL_STATE == Full2018_high_pt_noCR ]; then
	python3 script_combine_datacards_binning.py

	echo "nuisance edit drop WH_htt_plus  WH_SS_mm_1j_minus_2018 CMS_scale_met_2018" >> Combination/WH_chargeAsymmetry_WH_Full2018_v9_high_pt_noCR_binning.txt

	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_Full2018_v9_high_pt_binning_noCR \
			--output_name   Combination/FitResults_Full2018_high_pt_noCR_binning.txt \
			--freeze_nuisances r_higgs
	
# Full 2018 WHSS high pT
elif [ $FINAL_STATE == 2018_WHSS_high_pt ]; then
	python3 script_combine_datacards_binning.py
	
	echo "nuisance edit drop WH_htt_plus  WH_SS_mm_1j_minus_2018 CMS_scale_met_2018" >> Combination/WH_chargeAsymmetry_WH_Full2018_v9_WHSS_high_pt_binning.txt

	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_Full2018_v9_WHSS_high_pt_binning \
			--output_name   Combination/FitResults_Full2018_WHSS_high_pt_binning.txt \
			--freeze_nuisances r_higgs

# Full 2018 WHSS high pT no WZ CR
elif [ $FINAL_STATE == 2018_WHSS_high_pt_noCR ]; then
	python3 script_combine_datacards_binning.py
	
	echo "nuisance edit drop WH_htt_plus  WH_SS_mm_1j_minus_2018 CMS_scale_met_2018" >> Combination/WH_chargeAsymmetry_WH_Full2018_v9_WHSS_high_pt_noCR_binning.txt

	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_Full2018_v9_WHSS_high_pt_noCR_binning \
			--output_name   Combination/FitResults_Full2018_WHSS_high_pt_noCR_binning.txt \
			--freeze_nuisances r_higgs
	
# Full 2018 WH3l
elif [ $FINAL_STATE == 2018_WH3l ]; then
	python3 script_combine_datacards_binning.py
	
	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_Full2018_v9_WH3l_binning \
			--output_name   Combination/FitResults_Full2018_WH3l_binning.txt \
			--freeze_nuisances r_higgs

# Full 2018 WH3l no WZ CR
elif [ $FINAL_STATE == 2018_WH3l_noCR ]; then
	python3 script_combine_datacards_binning.py
	
	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_Full2018_v9_WH3l_noCR_binning \
			--output_name   Combination/FitResults_Full2018_WH3l_noCR_binning.txt \
			--freeze_nuisances r_higgs
	
			
#################			
### Full 2017 ###
#################
			
# Full 2017 high pT
elif [ $FINAL_STATE == Full2017_high_pt ]; then
	python3 script_combine_datacards_binning.py

	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_Full2017_v9_high_pt_binning \
			--output_name   Combination/FitResults_Full2017_high_pt_binning.txt \
			--freeze_nuisances r_higgs
	
# Full 2017 WHSS high pT
elif [ $FINAL_STATE == 2017_WHSS_high_pt ]; then
	python3 script_combine_datacards_binning.py

	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_Full2017_v9_WHSS_high_pt_binning \
			--output_name   Combination/FitResults_Full2017_WHSS_high_pt_binning.txt \
			--freeze_nuisances r_higgs

# Full 2017 WH3l
elif [ $FINAL_STATE == 2017_WH3l ]; then
	python3 script_combine_datacards_binning.py

	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_Full2017_v9_WH3l_binning \
			--output_name   Combination/FitResults_Full2017_WH3l_binning.txt \
			--freeze_nuisances r_higgs


##################			
### 2016noHIPM ###
##################
			
# 2016noHIPM high pT
elif [ $FINAL_STATE == 2016noHIPM_high_pt ]; then
	python3 script_combine_datacards_binning.py

	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_2016noHIPM_v9_high_pt_binning \
			--output_name   Combination/FitResults_2016noHIPM_high_pt_binning.txt \
			--freeze_nuisances r_higgs
	
# 2016noHIPM WHSS high pT
elif [ $FINAL_STATE == 2016noHIPM_WHSS_high_pt ]; then
	python3 script_combine_datacards_binning.py

	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_2016noHIPM_v9_WHSS_high_pt_binning \
			--output_name   Combination/FitResults_2016noHIPM_WHSS_high_pt_binning.txt \
			--freeze_nuisances r_higgs

# 2016noHIPM WH3l
elif [ $FINAL_STATE == 2016noHIPM_WH3l ]; then
	python3 script_combine_datacards_binning.py

	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_2016noHIPM_v9_WH3l_binning \
			--output_name   Combination/FitResults_2016noHIPM_WH3l_binning.txt \
			--freeze_nuisances r_higgs
	

################			
### 2016HIPM ###
################
			
# 2016HIPM high pT
elif [ $FINAL_STATE == 2016HIPM_high_pt ]; then
	python3 script_combine_datacards_binning.py

	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_2016HIPM_v9_high_pt_binning \
			--output_name   Combination/FitResults_2016HIPM_high_pt_binning.txt \
			--freeze_nuisances r_higgs
	
# 2016HIPM WHSS high pT
elif [ $FINAL_STATE == 2016HIPM_WHSS_high_pt ]; then
	python3 script_combine_datacards_binning.py

	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_2016HIPM_v9_WHSS_high_pt_binning \
			--output_name   Combination/FitResults_2016HIPM_WHSS_high_pt_binning.txt \
			--freeze_nuisances r_higgs

# 2016HIPM WH3l
elif [ $FINAL_STATE == 2016HIPM_WH3l ]; then
	python3 script_combine_datacards_binning.py

	python3 ../scripts/script_workspace_and_fit.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_2016HIPM_v9_WH3l_binning \
			--output_name   Combination/FitResults_2016HIPM_WH3l_binning.txt \
			--freeze_nuisances r_higgs

	
###########
	
else
	echo "I still don't know this final state. Here is the list of the available final states:"
	echo ""
	echo "bash do_fit.sh FullRun2_high_pt"
	echo "bash do_fit.sh FullRun2_WHSS_high_pt"
	echo "bash do_fit.sh FullRun2_WH3l"
	echo ""
	echo "bash do_fit.sh 2017_2018_high_pt"
	echo "bash do_fit.sh 2017_2018_WHSS_high_pt"
	echo "bash do_fit.sh 2017_2018_WH3l"
	echo ""
	echo "bash do_fit.sh Full2016_high_pt"
	echo "bash do_fit.sh Full2016_WHSS_high_pt"
	echo "bash do_fit.sh Full2016_WH3l"
	echo ""
	echo "bash do_fit.sh 2016noHIPM_2017_2018_high_pt"
	echo "bash do_fit.sh 2016noHIPM_2017_2018_WHSS_high_pt"
	echo "bash do_fit.sh 2016noHIPM_2017_2018_WH3l"
	echo ""
	echo "bash do_fit.sh 2016HIPM_2017_2018_high_pt"
	echo "bash do_fit.sh 2016HIPM_2017_2018_WHSS_high_pt"
	echo "bash do_fit.sh 2016HIPM_2017_2018_WH3l"
	echo ""
	echo "bash do_fit.sh Full2018_high_pt"
	echo "bash do_fit.sh Full2018_high_pt_noCR"
	echo "bash do_fit.sh 2018_WHSS_high_pt"
	echo "bash do_fit.sh 2018_WHSS_high_pt_noCR"
	echo "bash do_fit.sh 2018_WH3l"
	echo "bash do_fit.sh 2018_WH3l_noCR"
	echo ""
	echo "bash do_fit.sh Full2017_high_pt"
	echo "bash do_fit.sh 2017_WHSS_high_pt"
	echo "bash do_fit.sh 2017_WH3l"
	echo ""
	echo "bash do_fit.sh 2016noHIPM_high_pt"
	echo "bash do_fit.sh 2016noHIPM_WHSS_high_pt"
	echo "bash do_fit.sh 2016noHIPM_WH3l"
	echo ""
	echo "bash do_fit.sh 2016HIPM_high_pt"
	echo "bash do_fit.sh 2016HIPM_WHSS_high_pt"
	echo "bash do_fit.sh 2016HIPM_WH3l"
  echo ""
	exit 1
fi
