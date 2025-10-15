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
  echo "Arg #1: Variable     : $1"
  echo "Arg #2: Input file   : $2"
  echo "Arg #3: Era file     : $3"
  echo "==========================="
  VAR=$1
  INPUT=$2
  ERA=$3
fi

CUTS=(
	"WH_SS_em_1j_plus_${ERA}" 
	"WH_SS_em_1j_minus_${ERA}"
	"WH_SS_mm_1j_plus_${ERA}"
	"WH_SS_mm_1j_minus_${ERA}"
	"WH_SS_ee_1j_plus_${ERA}"
	"WH_SS_ee_1j_minus_${ERA}"
	"WH_SS_em_2j_plus_${ERA}"
	"WH_SS_em_2j_minus_${ERA}"
	"WH_SS_mm_2j_plus_${ERA}"
	"WH_SS_mm_2j_minus_${ERA}"
	"WH_SS_ee_2j_plus_${ERA}"
	"WH_SS_ee_2j_minus_${ERA}"
	# "WH_SS_em_1j_plus_low_pt_${ERA}" 
	# "WH_SS_em_1j_minus_low_pt_${ERA}"
	# "WH_SS_mm_1j_plus_low_pt_${ERA}"
	# "WH_SS_mm_1j_minus_low_pt_${ERA}"
	# "WH_SS_ee_1j_plus_low_pt_${ERA}"
	# "WH_SS_ee_1j_minus_low_pt_${ERA}"
	# "WH_SS_em_2j_plus_low_pt_${ERA}"
	# "WH_SS_em_2j_minus_low_pt_${ERA}"
	# "WH_SS_mm_2j_plus_low_pt_${ERA}"
	# "WH_SS_mm_2j_minus_low_pt_${ERA}"
	# "WH_SS_ee_2j_plus_low_pt_${ERA}"
	# "WH_SS_ee_2j_minus_low_pt_${ERA}"
	"WH_3l_sssf_plus_${ERA}"
	"WH_3l_sssf_minus_${ERA}"
	"WH_3l_ossf_plus_${ERA}"
	"WH_3l_ossf_minus_${ERA}"
	"WH_3l_WZ_CR_0j_${ERA}"
	"WH_SS_WZ_1j_${ERA}"
	"WH_SS_WZ_2j_${ERA}"
)

CUTS_ORIGINAL=(
	"hww2l2v_13TeV_WH_SS_em_1j_plus_pt2ge20" 
	"hww2l2v_13TeV_WH_SS_em_1j_minus_pt2ge20" 
	"hww2l2v_13TeV_WH_SS_noZveto_mm_1j_plus_pt2ge20" 
	"hww2l2v_13TeV_WH_SS_noZveto_mm_1j_minus_pt2ge20" 
	"hww2l2v_13TeV_WH_SS_ee_1j_plus_pt2ge20" 
	"hww2l2v_13TeV_WH_SS_ee_1j_minus_pt2ge20" 
	"hww2l2v_13TeV_WH_SS_em_2j_plus_pt2ge20" 
	"hww2l2v_13TeV_WH_SS_em_2j_minus_pt2ge20" 
	"hww2l2v_13TeV_WH_SS_noZveto_mm_2j_plus_pt2ge20" 
	"hww2l2v_13TeV_WH_SS_noZveto_mm_2j_minus_pt2ge20" 
	"hww2l2v_13TeV_WH_SS_ee_2j_plus_pt2ge20" 
	"hww2l2v_13TeV_WH_SS_ee_2j_minus_pt2ge20" 
	# "hww2l2v_13TeV_WH_SS_em_1j_plus_pt2lt20" 
	# "hww2l2v_13TeV_WH_SS_em_1j_minus_pt2lt20" 
	# "hww2l2v_13TeV_WH_SS_noZveto_mm_1j_plus_pt2lt20" 
	# "hww2l2v_13TeV_WH_SS_noZveto_mm_1j_minus_pt2lt20" 
	# "hww2l2v_13TeV_WH_SS_ee_1j_plus_pt2lt20" 
	# "hww2l2v_13TeV_WH_SS_ee_1j_minus_pt2lt20" 
	# "hww2l2v_13TeV_WH_SS_em_2j_plus_pt2lt20" 
	# "hww2l2v_13TeV_WH_SS_em_2j_minus_pt2lt20" 
	# "hww2l2v_13TeV_WH_SS_noZveto_mm_2j_plus_pt2lt20" 
	# "hww2l2v_13TeV_WH_SS_noZveto_mm_2j_minus_pt2lt20" 
	# "hww2l2v_13TeV_WH_SS_ee_2j_plus_pt2lt20" 
	# "hww2l2v_13TeV_WH_SS_ee_2j_minus_pt2lt20" 
	"wh3l_13TeV_sssf_plus_pt2ge20"
	"wh3l_13TeV_sssf_minus_pt2ge20"
	"wh3l_13TeV_ossf_plus_pt2ge20"
	"wh3l_13TeV_ossf_minus_pt2ge20"
	"wh3l_wz_13TeV"
	"hww2l2v_13TeV_WH_SS_WZ_1j"
	"hww2l2v_13TeV_WH_SS_WZ_2j"
)

CONFIGURATIONS=(
	"configuration_1j"
	"configuration_1j"
	"configuration_1j_mm"
	"configuration_1j_mm"
	"configuration_1j"
	"configuration_1j"
	"configuration_2j"
	"configuration_2j"
	"configuration_2j_mm"
	"configuration_2j_mm"
	"configuration_2j"
	"configuration_2j"
	# "configuration_1j"
	# "configuration_1j"
	# "configuration_1j_mm"
	# "configuration_1j_mm"
	# "configuration_1j"
	# "configuration_1j"
	# "configuration_2j"
	# "configuration_2j"
	# "configuration_2j_mm"
	# "configuration_2j_mm"
	# "configuration_2j"
	# "configuration_2j"
	"configuration_SSSF"
	"configuration_SSSF"
	"configuration_OSSF"
	"configuration_OSSF"
	"configuration_WZ0j"
	"configuration_WZ1j"
	"configuration_WZ2j"
)

if [ $VAR == binning ];
then
	VARIABLES=(
		"BDTG6_TT_0_6"
		"BDTG6_TT_0_6"
		"BDTG6_TT_0_6"
		"BDTG6_TT_0_6"
		"BDTG6_TT_0_5"
		"BDTG6_TT_0_5"
		"BDTG6_TT_0_5"
		"BDTG6_TT_0_5"
		"BDTG6_TT_0_0"
		"BDTG6_TT_0_0"
		"BDTG6_TT_0_0"
		"BDTG6_TT_0_0"
		# "BDTG6_TT_0_5"
		# "BDTG6_TT_0_5"
		# "BDTG6_TT_0_5"
		# "BDTG6_TT_0_5"
		# "BDTG6_TT_0_0"
		# "BDTG6_TT_0_0"
		# "BDTG6_TT_0_0"
		# "BDTG6_TT_0_0"
		# "BDTG6_TT_0_0"
		# "BDTG6_TT_0_0"
		# "BDTG6_TT_0_0"
		# "BDTG6_TT_0_0"
		"BDT_WH3l_SSSF_new_v9_0_75"
		"BDT_WH3l_SSSF_new_v9_0_75"
		"BDT_WH3l_OSSF_new_v9_0_75"
		"BDT_WH3l_OSSF_new_v9_0_75"
		"events"
		"events"
		"events"
	)
fi

if [ $ERA == 2018 ]; then
   ERA_DIR=Full2018_v9
fi

if [ $ERA == 2017 ]; then
   ERA_DIR=Full2017_v9
fi

if [ $ERA == 2016noHIPM ]; then
   ERA_DIR=2016noHIPM_v9
fi

if [ $ERA == 2016HIPM ]; then
   ERA_DIR=2016HIPM_v9
fi


# Pre-fit plots for discriminant variable
rm output.root

for ((idx=0; idx<${#CUTS[@]}; ++idx)); do

FINAL_STATE=WHSS
if [[ ${CUTS[$idx]} =~ "3l" ]]; then
	FINAL_STATE=WH3l
fi
if [[ ${CUTS[$idx]} =~ "WZ" ]]; then
	FINAL_STATE=WH3l
fi


	python ../scripts/mkPostFitPlot.py \
           --inputFileCombine ${INPUT} \
           --outputFile output.root \
           --variable ${VARIABLES[$idx]} \
           --cut ${CUTS[$idx]} \
		   --cutNameInOriginal ${CUTS_ORIGINAL[$idx]} \
           --inputFile ../${ERA_DIR}/${FINAL_STATE}/datacards_original_signal_scale/${CUTS_ORIGINAL[$idx]}/${VARIABLES[$idx]}/shapes/histos_${CUTS_ORIGINAL[$idx]}.root \
		   --isInputFileFromDatacard 1 \
           --kind s \
           --getSignalFromPrefit 0 \
           --structureFile ../${ERA_DIR}/${FINAL_STATE}/${CONFIGURATIONS[$idx]}
	
	cd configurations/${ERA}/${FINAL_STATE}

	mkShapesRDF -c 1
	
	mkPlot \
		--fileFormats png \
		--onlyPlot cratio \
		--showIntegralLegend 1 \
		--onlyCut ${CUTS_ORIGINAL[$idx]} \
        --onlyVariable ${VARIABLES[$idx]} \
		--postFit s \
		--skipMissingNuisance
	    # --skipMissingSample

	cd -
	
done
