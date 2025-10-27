#!/bin/bash
if [ $# -eq 0 ];
then
	echo "$0: Missing arguments. Please specify the final state:"
	echo ""
	echo "bash do_fit_unblind.sh FullRun2_high_pt"
	echo ""
	echo "bash do_fit_unblind.sh Full2018_high_pt"
	echo "bash do_fit_unblind.sh 2018_WHSS_high_pt"
	echo "bash do_fit_unblind.sh 2018_WH3l"
	echo ""
	echo "bash do_fit_unblind.sh Full2017_high_pt"
	echo "bash do_fit_unblind.sh 2017_WHSS_high_pt"
	echo "bash do_fit_unblind.sh 2017_WH3l"
	echo ""
	echo "bash do_fit_unblind.sh 2016noHIPM_high_pt"
	echo "bash do_fit_unblind.sh 2016noHIPM_WHSS_high_pt"
	echo "bash do_fit_unblind.sh 2016noHIPM_WH3l"
	echo ""
	echo "bash do_fit_unblind.sh 2016HIPM_high_pt"
	echo "bash do_fit_unblind.sh 2016HIPM_WHSS_high_pt"
	echo "bash do_fit_unblind.sh 2016HIPM_WH3l"
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

	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_FullRun2_v9_high_pt_binning \
			--output_name   Combination/FitResults_FullRun2_high_pt_binning_unblind.txt \
			--freeze_nuisances r_higgs


#################
### Full 2018 ###
#################
	
# Full 2018 high pT
elif [ $FINAL_STATE == Full2018_high_pt ]; then
	python3 script_combine_datacards_binning.py

	echo "nuisance edit drop WH_htt_plus  WH_SS_mm_1j_minus_2018 CMS_scale_met_2018" >> Combination/WH_chargeAsymmetry_WH_Full2018_v9_high_pt_binning.txt

	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_Full2018_v9_high_pt_binning \
			--output_name   Combination/FitResults_Full2018_high_pt_binning_unblind.txt \
			--freeze_nuisances r_higgs
	
# Full 2018 WHSS high pT
elif [ $FINAL_STATE == 2018_WHSS_high_pt ]; then
	python3 script_combine_datacards_binning.py
	
	echo "nuisance edit drop WH_htt_plus  WH_SS_mm_1j_minus_2018 CMS_scale_met_2018" >> Combination/WH_chargeAsymmetry_WH_Full2018_v9_WHSS_high_pt_binning.txt

	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_Full2018_v9_WHSS_high_pt_binning \
			--output_name   Combination/FitResults_Full2018_WHSS_high_pt_binning_unblind.txt \
			--freeze_nuisances r_higgs

# Full 2018 WH3l high pT
elif [ $FINAL_STATE == 2018_WH3l ]; then
	python3 script_combine_datacards_binning.py
	
	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_Full2018_v9_WH3l_binning \
			--output_name   Combination/FitResults_Full2018_WH3l_binning_unblind.txt \
			--freeze_nuisances r_higgs

			
#################			
### Full 2017 ###
#################
			
# Full 2017 high pT
elif [ $FINAL_STATE == Full2017_high_pt ]; then
	python3 script_combine_datacards_binning.py

	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_Full2017_v9_high_pt_binning \
			--output_name   Combination/FitResults_Full2017_high_pt_binning_unblind.txt \
			--freeze_nuisances r_higgs
	
# Full 2017 WHSS high pT
elif [ $FINAL_STATE == 2017_WHSS_high_pt ]; then
	python3 script_combine_datacards_binning.py

	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_Full2017_v9_WHSS_high_pt_binning \
			--output_name   Combination/FitResults_Full2017_WHSS_high_pt_binning_unblind.txt \
			--freeze_nuisances r_higgs

# Full 2017 WH3l
elif [ $FINAL_STATE == 2017_WH3l ]; then
	python3 script_combine_datacards_binning.py

	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_Full2017_v9_WH3l_binning \
			--output_name   Combination/FitResults_Full2017_WH3l_binning_unblind.txt \
			--freeze_nuisances r_higgs


##################			
### 2016noHIPM ###
##################
			
# 2016noHIPM high pT
elif [ $FINAL_STATE == 2016noHIPM_high_pt ]; then
	python3 script_combine_datacards_binning.py

	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_2016noHIPM_v9_high_pt_binning \
			--output_name   Combination/FitResults_2016noHIPM_high_pt_binning_unblind.txt \
			--freeze_nuisances r_higgs
	
# 2016noHIPM WHSS high pT
elif [ $FINAL_STATE == 2016noHIPM_WHSS_high_pt ]; then
	python3 script_combine_datacards_binning.py

	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_2016noHIPM_v9_WHSS_high_pt_binning \
			--output_name   Combination/FitResults_2016noHIPM_WHSS_high_pt_binning_unblind.txt \
			--freeze_nuisances r_higgs

# 2016noHIPM WH3l
elif [ $FINAL_STATE == 2016noHIPM_WH3l ]; then
	python3 script_combine_datacards_binning.py

	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_2016noHIPM_v9_WH3l_binning \
			--output_name   Combination/FitResults_2016noHIPM_WH3l_binning_unblind.txt \
			--freeze_nuisances r_higgs
	

################			
### 2016HIPM ###
################
			
# 2016HIPM high pT
elif [ $FINAL_STATE == 2016HIPM_high_pt ]; then
	python3 script_combine_datacards_binning.py

	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_2016HIPM_v9_high_pt_binning \
			--output_name   Combination/FitResults_2016HIPM_high_pt_binning_unblind.txt \
			--freeze_nuisances r_higgs
	
# 2016HIPM WHSS high pT
elif [ $FINAL_STATE == 2016HIPM_WHSS_high_pt ]; then
	python3 script_combine_datacards_binning.py

	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_2016HIPM_v9_WHSS_high_pt_binning \
			--output_name   Combination/FitResults_2016HIPM_WHSS_high_pt_binning_unblind.txt \
			--freeze_nuisances r_higgs

# 2016HIPM WH3l
elif [ $FINAL_STATE == 2016HIPM_WH3l ]; then
	python3 script_combine_datacards_binning.py

	python3 ../scripts/script_workspace_and_fit_unblind.py \
			--datacard_name Combination/WH_chargeAsymmetry_WH_2016HIPM_v9_WH3l_binning \
			--output_name   Combination/FitResults_2016HIPM_WH3l_binning_unblind.txt \
			--freeze_nuisances r_higgs

	
###########
	
else
	echo "I still don't know this final state. Here is the list of the available final states:"
	echo ""
	echo "bash do_fit_unblind.sh FullRun2_high_pt"
	echo ""
	echo "bash do_fit_unblind.sh Full2018_high_pt"
	echo "bash do_fit_unblind.sh 2018_WHSS_high_pt"
	echo "bash do_fit_unblind.sh 2018_WH3l"
	echo ""
	echo "bash do_fit_unblind.sh Full2017_high_pt"
	echo "bash do_fit_unblind.sh 2017_WHSS_high_pt"
	echo "bash do_fit_unblind.sh 2017_WH3l"
	echo ""
	echo "bash do_fit_unblind.sh 2016noHIPM_high_pt"
	echo "bash do_fit_unblind.sh 2016noHIPM_WHSS_high_pt"
	echo "bash do_fit_unblind.sh 2016noHIPM_WH3l"
	echo ""
	echo "bash do_fit_unblind.sh 2016HIPM_high_pt"
	echo "bash do_fit_unblind.sh 2016HIPM_WHSS_high_pt"
	echo "bash do_fit_unblind.sh 2016HIPM_WH3l"
	echo ""
	exit 1
fi
