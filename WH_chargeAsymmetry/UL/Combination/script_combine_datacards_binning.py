import sys,os

print("#######################")
print("Number of arguments: {}".format(len(sys.argv)))
print("Argument List: {}".format(str(sys.argv)))
if (len(sys.argv) > 1):
    if (sys.argv[1] == "1"):
        print("Using correct signal normalization!!")
    else:
        print("Using signal normalization enhanced by a factor 10")
else:
    print("Using signal normalization enhanced by a factor 10")
print("#######################")

print("\n\n\n\n")

# "Global" variables
suffix_WHSS = '_original_signal_scale'
suffix_WH3l = '_original_signal_scale'

suffix_WHSS_original_scale = "_original_signal_scale" # datacards_original_signal_scale/
suffix_WH3l_original_scale = "_original_signal_scale" # datacards_original_signal_scale/


if (len(sys.argv) > 1):
    if (sys.argv[1] == "1"):
        suffix_WHSS = suffix_WHSS_original_scale
        suffix_WH3l = suffix_WH3l_original_scale
    elif (sys.argv[1] == "old"):
        suffix_WHSS = suffix_WHSS_loose_bVeto
        suffix_WH3l = suffix_WH3l_old_wz_scaling

var_WHSS = 'BDTG6_TT_100_bins'
var_SSSF = 'BDT_WH3l_SSSF_new_v9_more'
var_OSSF = 'BDT_WH3l_OSSF_new_v9_more'

# ---------
# Full 2018
# ---------

# 2018 datacards
WHSS_2018_high_pt = "WH_SS_em_1j_minus_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_1j_minus_pt2ge20/BDTG6_TT_0_6/datacard.txt               \
                     WH_SS_em_1j_plus_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_1j_plus_pt2ge20/BDTG6_TT_0_6/datacard.txt                 \
                     WH_SS_mm_1j_minus_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_minus_pt2ge20/BDTG6_TT_0_6/datacard.txt       \
                     WH_SS_mm_1j_plus_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_plus_pt2ge20/BDTG6_TT_0_6/datacard.txt         \
                     WH_SS_ee_1j_minus_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_1j_minus_pt2ge20/BDTG6_TT_0_5/datacard.txt               \
                     WH_SS_ee_1j_plus_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_1j_plus_pt2ge20/BDTG6_TT_0_5/datacard.txt                 \
                     WH_SS_em_2j_minus_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_2j_minus_pt2ge20/BDTG6_TT_0_5/datacard.txt               \
                     WH_SS_em_2j_plus_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_2j_plus_pt2ge20/BDTG6_TT_0_5/datacard.txt                 \
                     WH_SS_mm_2j_minus_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_minus_pt2ge20/BDTG6_TT_0_5/datacard.txt       \
                     WH_SS_mm_2j_plus_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_plus_pt2ge20/BDTG6_TT_0_5/datacard.txt         \
                     WH_SS_ee_2j_minus_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_2j_minus_pt2ge20/BDTG6_TT_0_0/datacard.txt               \
                     WH_SS_ee_2j_plus_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_2j_plus_pt2ge20/BDTG6_TT_0_0/datacard.txt                 \
                     WH_SS_WZ_1j_2018=../Full2018_v9/WH3l/datacards{2}/hww2l2v_13TeV_WH_SS_WZ_1j/events/datacard.txt                                         \
                     WH_SS_WZ_2j_2018=../Full2018_v9/WH3l/datacards{2}/hww2l2v_13TeV_WH_SS_WZ_2j/events/datacard.txt                                         \
                     ".format(var_WHSS,suffix_WHSS,suffix_WH3l)
                     # WH_SS_mm_2j_SS_CR_minus_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_SS_CR_minus_pt2ge20/events/datacard.txt \
                     # WH_SS_mm_2j_SS_CR_plus_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_SS_CR_plus_pt2ge20/events/datacard.txt   \
                     # WH_SS_em_2j_SS_CR_minus_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_2j_SS_CR_minus_pt2ge20/events/datacard.txt         \
                     # WH_SS_em_2j_SS_CR_plus_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_2j_SS_CR_plus_pt2ge20/events/datacard.txt           \
                     # WH_SS_ee_2j_SS_CR_minus_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_2j_SS_CR_minus_pt2ge20/events/datacard.txt         \
                     # WH_SS_ee_2j_SS_CR_plus_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_2j_SS_CR_plus_pt2ge20/events/datacard.txt           \
                     # WH_SS_mm_1j_SS_CR_minus_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_SS_CR_minus_pt2ge20/events/datacard.txt \
                     # WH_SS_mm_1j_SS_CR_plus_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_SS_CR_plus_pt2ge20/events/datacard.txt   \
                     # WH_SS_em_1j_SS_CR_minus_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_1j_SS_CR_minus_pt2ge20/events/datacard.txt         \
                     # WH_SS_em_1j_SS_CR_plus_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_1j_SS_CR_plus_pt2ge20/events/datacard.txt           \
                     # WH_SS_ee_1j_SS_CR_minus_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_1j_SS_CR_minus_pt2ge20/events/datacard.txt         \
                     # WH_SS_ee_1j_SS_CR_plus_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_1j_SS_CR_plus_pt2ge20/events/datacard.txt           \

WHSS_2018_low_pt = "WH_SS_em_1j_minus_low_pt_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_1j_minus_pt2lt20/BDTG6_TT_0_5/datacard.txt         \
                    WH_SS_em_1j_plus_low_pt_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_1j_plus_pt2lt20/BDTG6_TT_0_5/datacard.txt           \
                    WH_SS_mm_1j_minus_low_pt_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_minus_pt2lt20/BDTG6_TT_0_5/datacard.txt \
                    WH_SS_mm_1j_plus_low_pt_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_plus_pt2lt20/BDTG6_TT_0_5/datacard.txt   \
                    WH_SS_ee_1j_minus_low_pt_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_1j_minus_pt2lt20/BDTG6_TT_0_0/datacard.txt         \
                    WH_SS_ee_1j_plus_low_pt_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_1j_plus_pt2lt20/BDTG6_TT_0_0/datacard.txt           \
                    WH_SS_em_2j_minus_low_pt_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_2j_minus_pt2lt20/BDTG6_TT_0_0/datacard.txt         \
                    WH_SS_em_2j_plus_low_pt_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_2j_plus_pt2lt20/BDTG6_TT_0_0/datacard.txt           \
                    WH_SS_mm_2j_minus_low_pt_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_minus_pt2lt20/BDTG6_TT_0_0/datacard.txt \
                    WH_SS_mm_2j_plus_low_pt_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_plus_pt2lt20/BDTG6_TT_0_0/datacard.txt   \
                    WH_SS_ee_2j_minus_low_pt_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_2j_minus_pt2lt20/BDTG6_TT_0_0/datacard.txt         \
                    WH_SS_ee_2j_plus_low_pt_2018=../Full2018_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_2j_plus_pt2lt20/BDTG6_TT_0_0/datacard.txt           \
                    ".format(var_WHSS,suffix_WHSS)

WH3l_2018 = "WH_3l_sssf_plus_2018=../Full2018_v9/WH3l/datacards{2}/wh3l_13TeV_sssf_plus_pt2ge20/BDT_WH3l_SSSF_new_v9_0_75/datacard.txt   \
             WH_3l_sssf_minus_2018=../Full2018_v9/WH3l/datacards{2}/wh3l_13TeV_sssf_minus_pt2ge20/BDT_WH3l_SSSF_new_v9_0_75/datacard.txt \
             WH_3l_ossf_plus_2018=../Full2018_v9/WH3l/datacards{2}/wh3l_13TeV_ossf_plus_pt2ge20/BDT_WH3l_OSSF_new_v9_0_75/datacard.txt   \
             WH_3l_ossf_minus_2018=../Full2018_v9/WH3l/datacards{2}/wh3l_13TeV_ossf_minus_pt2ge20/BDT_WH3l_OSSF_new_v9_0_75/datacard.txt \
             WH_3l_WZ_CR_0j_2018=../Full2018_v9/WH3l/datacards{2}/wh3l_wz_13TeV/events/datacard.txt                                      \
             ".format(var_SSSF,var_OSSF,suffix_WH3l)

# ---------
# Full 2017
# ---------

# 2017 datacards
WHSS_2017_high_pt = "WH_SS_em_1j_minus_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_1j_minus_pt2ge20/BDTG6_TT_0_6/datacard.txt               \
                     WH_SS_em_1j_plus_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_1j_plus_pt2ge20/BDTG6_TT_0_6/datacard.txt                 \
                     WH_SS_mm_1j_minus_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_minus_pt2ge20/BDTG6_TT_0_6/datacard.txt       \
                     WH_SS_mm_1j_plus_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_plus_pt2ge20/BDTG6_TT_0_6/datacard.txt         \
                     WH_SS_ee_1j_minus_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_1j_minus_pt2ge20/BDTG6_TT_0_5/datacard.txt               \
                     WH_SS_ee_1j_plus_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_1j_plus_pt2ge20/BDTG6_TT_0_5/datacard.txt                 \
                     WH_SS_em_2j_minus_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_2j_minus_pt2ge20/BDTG6_TT_0_5/datacard.txt               \
                     WH_SS_em_2j_plus_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_2j_plus_pt2ge20/BDTG6_TT_0_5/datacard.txt                 \
                     WH_SS_mm_2j_minus_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_minus_pt2ge20/BDTG6_TT_0_5/datacard.txt       \
                     WH_SS_mm_2j_plus_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_plus_pt2ge20/BDTG6_TT_0_5/datacard.txt         \
                     WH_SS_ee_2j_minus_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_2j_minus_pt2ge20/BDTG6_TT_0_0/datacard.txt               \
                     WH_SS_ee_2j_plus_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_2j_plus_pt2ge20/BDTG6_TT_0_0/datacard.txt                 \
                     WH_SS_WZ_1j_2017=../Full2017_v9/WH3l/datacards{2}/hww2l2v_13TeV_WH_SS_WZ_1j/events/datacard.txt                                         \
                     WH_SS_WZ_2j_2017=../Full2017_v9/WH3l/datacards{2}/hww2l2v_13TeV_WH_SS_WZ_2j/events/datacard.txt                                         \
                     ".format(var_WHSS,suffix_WHSS,suffix_WH3l)
                     # WH_SS_mm_2j_SS_CR_minus_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_SS_CR_minus_pt2ge20/events/datacard.txt \
                     # WH_SS_mm_2j_SS_CR_plus_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_SS_CR_plus_pt2ge20/events/datacard.txt   \
                     # WH_SS_em_2j_SS_CR_minus_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_2j_SS_CR_minus_pt2ge20/events/datacard.txt         \
                     # WH_SS_em_2j_SS_CR_plus_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_2j_SS_CR_plus_pt2ge20/events/datacard.txt           \
                     # WH_SS_ee_2j_SS_CR_minus_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_2j_SS_CR_minus_pt2ge20/events/datacard.txt         \
                     # WH_SS_ee_2j_SS_CR_plus_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_2j_SS_CR_plus_pt2ge20/events/datacard.txt           \
                     # WH_SS_mm_1j_SS_CR_minus_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_SS_CR_minus_pt2ge20/events/datacard.txt \
                     # WH_SS_mm_1j_SS_CR_plus_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_SS_CR_plus_pt2ge20/events/datacard.txt   \
                     # WH_SS_em_1j_SS_CR_minus_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_1j_SS_CR_minus_pt2ge20/events/datacard.txt         \
                     # WH_SS_em_1j_SS_CR_plus_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_1j_SS_CR_plus_pt2ge20/events/datacard.txt           \
                     # WH_SS_ee_1j_SS_CR_minus_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_1j_SS_CR_minus_pt2ge20/events/datacard.txt         \
                     # WH_SS_ee_1j_SS_CR_plus_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_1j_SS_CR_plus_pt2ge20/events/datacard.txt           \

WHSS_2017_low_pt = "WH_SS_em_1j_minus_low_pt_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_1j_minus_pt2lt20/BDTG6_TT_0_5/datacard.txt         \
                    WH_SS_em_1j_plus_low_pt_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_1j_plus_pt2lt20/BDTG6_TT_0_5/datacard.txt           \
                    WH_SS_mm_1j_minus_low_pt_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_minus_pt2lt20/BDTG6_TT_0_5/datacard.txt \
                    WH_SS_mm_1j_plus_low_pt_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_plus_pt2lt20/BDTG6_TT_0_5/datacard.txt   \
                    WH_SS_ee_1j_minus_low_pt_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_1j_minus_pt2lt20/BDTG6_TT_0_0/datacard.txt         \
                    WH_SS_ee_1j_plus_low_pt_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_1j_plus_pt2lt20/BDTG6_TT_0_0/datacard.txt           \
                    WH_SS_em_2j_minus_low_pt_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_2j_minus_pt2lt20/BDTG6_TT_0_0/datacard.txt         \
                    WH_SS_em_2j_plus_low_pt_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_2j_plus_pt2lt20/BDTG6_TT_0_0/datacard.txt           \
                    WH_SS_mm_2j_minus_low_pt_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_minus_pt2lt20/BDTG6_TT_0_0/datacard.txt \
                    WH_SS_mm_2j_plus_low_pt_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_plus_pt2lt20/BDTG6_TT_0_0/datacard.txt   \
                    WH_SS_ee_2j_minus_low_pt_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_2j_minus_pt2lt20/BDTG6_TT_0_0/datacard.txt         \
                    WH_SS_ee_2j_plus_low_pt_2017=../Full2017_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_2j_plus_pt2lt20/BDTG6_TT_0_0/datacard.txt           \
                    ".format(var_WHSS,suffix_WHSS)

WH3l_2017 = "WH_3l_sssf_plus_2017=../Full2017_v9/WH3l/datacards{2}/wh3l_13TeV_sssf_plus_pt2ge20/BDT_WH3l_SSSF_new_v9_0_75/datacard.txt   \
             WH_3l_sssf_minus_2017=../Full2017_v9/WH3l/datacards{2}/wh3l_13TeV_sssf_minus_pt2ge20/BDT_WH3l_SSSF_new_v9_0_75/datacard.txt \
             WH_3l_ossf_plus_2017=../Full2017_v9/WH3l/datacards{2}/wh3l_13TeV_ossf_plus_pt2ge20/BDT_WH3l_OSSF_new_v9_0_75/datacard.txt   \
             WH_3l_ossf_minus_2017=../Full2017_v9/WH3l/datacards{2}/wh3l_13TeV_ossf_minus_pt2ge20/BDT_WH3l_OSSF_new_v9_0_75/datacard.txt \
             WH_3l_WZ_CR_0j_2017=../Full2017_v9/WH3l/datacards{2}/wh3l_wz_13TeV/events/datacard.txt                                          \
             ".format(var_SSSF,var_OSSF,suffix_WH3l)

# ------------
# 2016 no HIPM
# ------------

# 2016noHIPM datacards
WHSS_2016noHIPM_high_pt = "WH_SS_em_1j_minus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_1j_minus_pt2ge20/BDTG6_TT_0_6/datacard.txt               \
                           WH_SS_em_1j_plus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_1j_plus_pt2ge20/BDTG6_TT_0_6/datacard.txt                 \
                           WH_SS_mm_1j_minus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_minus_pt2ge20/BDTG6_TT_0_6/datacard.txt       \
                           WH_SS_mm_1j_plus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_plus_pt2ge20/BDTG6_TT_0_6/datacard.txt         \
                           WH_SS_ee_1j_minus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_1j_minus_pt2ge20/BDTG6_TT_0_5/datacard.txt               \
                           WH_SS_ee_1j_plus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_1j_plus_pt2ge20/BDTG6_TT_0_5/datacard.txt                 \
                           WH_SS_em_2j_minus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_2j_minus_pt2ge20/BDTG6_TT_0_5/datacard.txt               \
                           WH_SS_em_2j_plus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_2j_plus_pt2ge20/BDTG6_TT_0_5/datacard.txt                 \
                           WH_SS_mm_2j_minus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_minus_pt2ge20/BDTG6_TT_0_5/datacard.txt       \
                           WH_SS_mm_2j_plus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_plus_pt2ge20/BDTG6_TT_0_5/datacard.txt         \
                           WH_SS_ee_2j_minus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_2j_minus_pt2ge20/BDTG6_TT_0_0/datacard.txt               \
                           WH_SS_ee_2j_plus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_2j_plus_pt2ge20/BDTG6_TT_0_0/datacard.txt                 \
                           WH_SS_WZ_1j_2016noHIPM=../2016noHIPM_v9/WH3l/datacards{2}/hww2l2v_13TeV_WH_SS_WZ_1j/events/datacard.txt                                         \
                           WH_SS_WZ_2j_2016noHIPM=../2016noHIPM_v9/WH3l/datacards{2}/hww2l2v_13TeV_WH_SS_WZ_2j/events/datacard.txt                                         \
                           ".format(var_WHSS,suffix_WHSS,suffix_WH3l)
                           # WH_SS_mm_2j_SS_CR_minus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_SS_CR_minus_pt2ge20/events/datacard.txt \
                           # WH_SS_mm_2j_SS_CR_plus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_SS_CR_plus_pt2ge20/events/datacard.txt   \
                           # WH_SS_em_2j_SS_CR_minus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_2j_SS_CR_minus_pt2ge20/events/datacard.txt         \
                           # WH_SS_em_2j_SS_CR_plus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_2j_SS_CR_plus_pt2ge20/events/datacard.txt           \
                           # WH_SS_ee_2j_SS_CR_minus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_2j_SS_CR_minus_pt2ge20/events/datacard.txt         \
                           # WH_SS_ee_2j_SS_CR_plus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_2j_SS_CR_plus_pt2ge20/events/datacard.txt           \
                           # WH_SS_mm_1j_SS_CR_minus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_SS_CR_minus_pt2ge20/events/datacard.txt \
                           # WH_SS_mm_1j_SS_CR_plus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_SS_CR_plus_pt2ge20/events/datacard.txt   \
                           # WH_SS_em_1j_SS_CR_minus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_1j_SS_CR_minus_pt2ge20/events/datacard.txt         \
                           # WH_SS_em_1j_SS_CR_plus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_1j_SS_CR_plus_pt2ge20/events/datacard.txt           \
                           # WH_SS_ee_1j_SS_CR_minus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_1j_SS_CR_minus_pt2ge20/events/datacard.txt         \
                           # WH_SS_ee_1j_SS_CR_plus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_1j_SS_CR_plus_pt2ge20/events/datacard.txt           \


WHSS_2016noHIPM_low_pt = "WH_SS_em_1j_minus_low_pt_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_1j_minus_pt2lt20/BDTG6_TT_0_5/datacard.txt         \
                          WH_SS_em_1j_plus_low_pt_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_1j_plus_pt2lt20/BDTG6_TT_0_5/datacard.txt           \
                          WH_SS_mm_1j_minus_low_pt_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_minus_pt2lt20/BDTG6_TT_0_5/datacard.txt \
                          WH_SS_mm_1j_plus_low_pt_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_plus_pt2lt20/BDTG6_TT_0_5/datacard.txt   \
                          WH_SS_ee_1j_minus_low_pt_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_1j_minus_pt2lt20/BDTG6_TT_0_0/datacard.txt         \
                          WH_SS_ee_1j_plus_low_pt_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_1j_plus_pt2lt20/BDTG6_TT_0_0/datacard.txt           \
                          WH_SS_em_2j_minus_low_pt_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_2j_minus_pt2lt20/BDTG6_TT_0_0/datacard.txt         \
                          WH_SS_em_2j_plus_low_pt_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_2j_plus_pt2lt20/BDTG6_TT_0_0/datacard.txt           \
                          WH_SS_mm_2j_minus_low_pt_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_minus_pt2lt20/BDTG6_TT_0_0/datacard.txt \
                          WH_SS_mm_2j_plus_low_pt_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_plus_pt2lt20/BDTG6_TT_0_0/datacard.txt   \
                          WH_SS_ee_2j_minus_low_pt_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_2j_minus_pt2lt20/BDTG6_TT_0_0/datacard.txt         \
                          WH_SS_ee_2j_plus_low_pt_2016noHIPM=../2016noHIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_2j_plus_pt2lt20/BDTG6_TT_0_0/datacard.txt           \
                          ".format(var_WHSS,suffix_WHSS)

WH3l_2016noHIPM = "WH_3l_sssf_plus_2016noHIPM=../2016noHIPM_v9/WH3l/datacards{2}/wh3l_13TeV_sssf_plus_pt2ge20/BDT_WH3l_SSSF_new_v9_0_75/datacard.txt   \
                   WH_3l_sssf_minus_2016noHIPM=../2016noHIPM_v9/WH3l/datacards{2}/wh3l_13TeV_sssf_minus_pt2ge20/BDT_WH3l_SSSF_new_v9_0_75/datacard.txt \
                   WH_3l_ossf_plus_2016noHIPM=../2016noHIPM_v9/WH3l/datacards{2}/wh3l_13TeV_ossf_plus_pt2ge20/BDT_WH3l_OSSF_new_v9_0_75/datacard.txt   \
                   WH_3l_ossf_minus_2016noHIPM=../2016noHIPM_v9/WH3l/datacards{2}/wh3l_13TeV_ossf_minus_pt2ge20/BDT_WH3l_OSSF_new_v9_0_75/datacard.txt \
                   WH_3l_WZ_CR_0j_2016noHIPM=../2016noHIPM_v9/WH3l/datacards{2}/wh3l_wz_13TeV/events/datacard.txt                                      \
                   ".format(var_SSSF,var_OSSF,suffix_WH3l)

# ---------
# 2016 HIPM
# ---------

# 2016HIPM datacards
WHSS_2016HIPM_high_pt = "WH_SS_em_1j_minus_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_1j_minus_pt2ge20/BDTG6_TT_0_6/datacard.txt               \
                         WH_SS_em_1j_plus_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_1j_plus_pt2ge20/BDTG6_TT_0_6/datacard.txt                 \
                         WH_SS_mm_1j_minus_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_minus_pt2ge20/BDTG6_TT_0_6/datacard.txt       \
                         WH_SS_mm_1j_plus_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_plus_pt2ge20/BDTG6_TT_0_6/datacard.txt         \
                         WH_SS_ee_1j_minus_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_1j_minus_pt2ge20/BDTG6_TT_0_5/datacard.txt               \
                         WH_SS_ee_1j_plus_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_1j_plus_pt2ge20/BDTG6_TT_0_5/datacard.txt                 \
                         WH_SS_em_2j_minus_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_2j_minus_pt2ge20/BDTG6_TT_0_5/datacard.txt               \
                         WH_SS_em_2j_plus_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_2j_plus_pt2ge20/BDTG6_TT_0_5/datacard.txt                 \
                         WH_SS_mm_2j_minus_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_minus_pt2ge20/BDTG6_TT_0_5/datacard.txt       \
                         WH_SS_mm_2j_plus_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_plus_pt2ge20/BDTG6_TT_0_5/datacard.txt         \
                         WH_SS_ee_2j_minus_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_2j_minus_pt2ge20/BDTG6_TT_0_0/datacard.txt               \
                         WH_SS_ee_2j_plus_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_2j_plus_pt2ge20/BDTG6_TT_0_0/datacard.txt                 \
                         WH_SS_WZ_1j_2016HIPM=../2016HIPM_v9/WH3l/datacards{2}/hww2l2v_13TeV_WH_SS_WZ_1j/events/datacard.txt                                         \
                         WH_SS_WZ_2j_2016HIPM=../2016HIPM_v9/WH3l/datacards{2}/hww2l2v_13TeV_WH_SS_WZ_2j/events/datacard.txt                                         \
                         ".format(var_WHSS,suffix_WHSS,suffix_WH3l)
                         # WH_SS_mm_2j_SS_CR_minus_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_SS_CR_minus_pt2ge20/events/datacard.txt \
                         # WH_SS_mm_2j_SS_CR_plus_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_SS_CR_plus_pt2ge20/events/datacard.txt   \
                         # WH_SS_em_2j_SS_CR_minus_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_2j_SS_CR_minus_pt2ge20/events/datacard.txt         \
                         # WH_SS_em_2j_SS_CR_plus_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_2j_SS_CR_plus_pt2ge20/events/datacard.txt           \
                         # WH_SS_ee_2j_SS_CR_minus_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_2j_SS_CR_minus_pt2ge20/events/datacard.txt         \
                         # WH_SS_ee_2j_SS_CR_plus_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_2j_SS_CR_plus_pt2ge20/events/datacard.txt           \
                         # WH_SS_mm_1j_SS_CR_minus_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_SS_CR_minus_pt2ge20/events/datacard.txt \
                         # WH_SS_mm_1j_SS_CR_plus_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_SS_CR_plus_pt2ge20/events/datacard.txt   \
                         # WH_SS_em_1j_SS_CR_minus_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_1j_SS_CR_minus_pt2ge20/events/datacard.txt         \
                         # WH_SS_em_1j_SS_CR_plus_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_1j_SS_CR_plus_pt2ge20/events/datacard.txt           \
                         # WH_SS_ee_1j_SS_CR_minus_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_1j_SS_CR_minus_pt2ge20/events/datacard.txt         \
                         # WH_SS_ee_1j_SS_CR_plus_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_1j_SS_CR_plus_pt2ge20/events/datacard.txt           \

WHSS_2016HIPM_low_pt = "WH_SS_em_1j_minus_low_pt_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_1j_minus_pt2lt20/BDTG6_TT_0_5/datacard.txt         \
                        WH_SS_em_1j_plus_low_pt_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_1j_plus_pt2lt20/BDTG6_TT_0_5/datacard.txt           \
                        WH_SS_mm_1j_minus_low_pt_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_minus_pt2lt20/BDTG6_TT_0_5/datacard.txt \
                        WH_SS_mm_1j_plus_low_pt_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_plus_pt2lt20/BDTG6_TT_0_5/datacard.txt   \
                        WH_SS_ee_1j_minus_low_pt_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_1j_minus_pt2lt20/BDTG6_TT_0_0/datacard.txt         \
                        WH_SS_ee_1j_plus_low_pt_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_1j_plus_pt2lt20/BDTG6_TT_0_0/datacard.txt           \
                        WH_SS_em_2j_minus_low_pt_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_2j_minus_pt2lt20/BDTG6_TT_0_0/datacard.txt         \
                        WH_SS_em_2j_plus_low_pt_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_em_2j_plus_pt2lt20/BDTG6_TT_0_0/datacard.txt           \
                        WH_SS_mm_2j_minus_low_pt_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_minus_pt2lt20/BDTG6_TT_0_0/datacard.txt \
                        WH_SS_mm_2j_plus_low_pt_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_plus_pt2lt20/BDTG6_TT_0_0/datacard.txt   \
                        WH_SS_ee_2j_minus_low_pt_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_2j_minus_pt2lt20/BDTG6_TT_0_0/datacard.txt         \
                        WH_SS_ee_2j_plus_low_pt_2016HIPM=../2016HIPM_v9/WHSS/datacards{1}/hww2l2v_13TeV_WH_SS_ee_2j_plus_pt2lt20/BDTG6_TT_0_0/datacard.txt           \
                        ".format(var_WHSS,suffix_WHSS)

WH3l_2016HIPM = "WH_3l_sssf_plus_2016HIPM=../2016HIPM_v9/WH3l/datacards{2}/wh3l_13TeV_sssf_plus_pt2ge20/BDT_WH3l_SSSF_new_v9_0_75/datacard.txt   \
                 WH_3l_sssf_minus_2016HIPM=../2016HIPM_v9/WH3l/datacards{2}/wh3l_13TeV_sssf_minus_pt2ge20/BDT_WH3l_SSSF_new_v9_0_75/datacard.txt \
                 WH_3l_ossf_plus_2016HIPM=../2016HIPM_v9/WH3l/datacards{2}/wh3l_13TeV_ossf_plus_pt2ge20/BDT_WH3l_OSSF_new_v9_0_75/datacard.txt   \
                 WH_3l_ossf_minus_2016HIPM=../2016HIPM_v9/WH3l/datacards{2}/wh3l_13TeV_ossf_minus_pt2ge20/BDT_WH3l_OSSF_new_v9_0_75/datacard.txt \
                 WH_3l_WZ_CR_0j_2016HIPM=../2016HIPM_v9/WH3l/datacards{2}/wh3l_wz_13TeV/events/datacard.txt                                          \
                   ".format(var_SSSF,var_OSSF,suffix_WH3l)

# Here we define the actual combine commands we want to use
os.system("mkdir -p Combination")

tmp_command = "combineCards.py "

output_name_suffix = "_binning"
if (len(sys.argv) > 1):
    if (sys.argv[1] == "1"):
        output_name_suffix = "_binning_original_signal_scale"

combine_command_FullRun2 = tmp_command + WHSS_2018_high_pt       + WHSS_2018_low_pt       + WH3l_2018 \
                                       + WHSS_2017_high_pt       + WHSS_2017_low_pt       + WH3l_2017 \
                                       + WHSS_2016noHIPM_high_pt + WHSS_2016noHIPM_low_pt + WH3l_2016noHIPM \
                                       + WHSS_2016HIPM_high_pt   + WHSS_2016HIPM_low_pt   + WH3l_2016HIPM \
                                       + " > Combination/WH_chargeAsymmetry_WH_FullRun2_v9{0}.txt".format(output_name_suffix)
print(combine_command_FullRun2)
os.system(combine_command_FullRun2)
print("")
print("")
print("")


# # WHSS and WH3l Full 2018
# combine_command_Full2018 = tmp_command + WHSS_2018_high_pt + WHSS_2018_low_pt + WH3l_2018 + " > Combination/WH_chargeAsymmetry_WH_Full2018_v9{0}.txt".format(output_name_suffix)
# print(combine_command_Full2018)
# os.system(combine_command_Full2018)
# print("")
# print("")
# print("")

# # WHSS Full 2018
# combine_command_WHSS_Full2018 = tmp_command + WHSS_2018_high_pt + WHSS_2018_low_pt + " > Combination/WH_chargeAsymmetry_WH_WHSS_Full2018_v9{0}.txt".format(output_name_suffix)
# print(combine_command_WHSS_Full2018)
# os.system(combine_command_WHSS_Full2018)
# print("")
# print("")
# print("")

# # WHSS Full 2018 high_pt
# combine_command_WHSS_high_pt_Full2018 = tmp_command + WHSS_2018_high_pt + " > Combination/WH_chargeAsymmetry_WH_WHSS_high_pt_Full2018_v9{0}.txt".format(output_name_suffix)
# print(combine_command_WHSS_high_pt_Full2018)
# os.system(combine_command_WHSS_high_pt_Full2018)
# print("")
# print("")
# print("")

# # WHSS Full 2018 low_pt
# combine_command_WHSS_high_pt_Full2018 = tmp_command + WHSS_2018_low_pt + " > Combination/WH_chargeAsymmetry_WH_WHSS_low_pt_Full2018_v9{0}.txt".format(output_name_suffix)
# print(combine_command_WHSS_high_pt_Full2018)
# os.system(combine_command_WHSS_high_pt_Full2018)
# print("")
# print("")
# print("")

# # WH3l Full 2018
# combine_command_WH3l_Full2018 = tmp_command + WH3l_2018 + " > Combination/WH_chargeAsymmetry_WH_WH3l_Full2018_v9{0}.txt".format(output_name_suffix)
# print(combine_command_WH3l_Full2018)
# os.system(combine_command_WH3l_Full2018)
# print("")
# print("")
# print("")


# # WHSS and WH3l Full 2017
# combine_command_Full2017 = tmp_command + WHSS_2017_high_pt + WHSS_2017_low_pt + WH3l_2017 + " > Combination/WH_chargeAsymmetry_WH_Full2017_v9{0}.txt".format(output_name_suffix)
# print(combine_command_Full2017)
# os.system(combine_command_Full2017)
# print("")
# print("")
# print("")

# # WHSS Full 2017
# combine_command_WHSS_Full2017 = tmp_command + WHSS_2017_high_pt + WHSS_2017_low_pt + " > Combination/WH_chargeAsymmetry_WH_WHSS_Full2017_v9{0}.txt".format(output_name_suffix)
# print(combine_command_WHSS_Full2017)
# os.system(combine_command_WHSS_Full2017)
# print("")
# print("")
# print("")

# # WHSS Full 2017 high_pt
# combine_command_WHSS_high_pt_Full2017 = tmp_command + WHSS_2017_high_pt + " > Combination/WH_chargeAsymmetry_WH_WHSS_high_pt_Full2017_v9{0}.txt".format(output_name_suffix)
# print(combine_command_WHSS_high_pt_Full2017)
# os.system(combine_command_WHSS_high_pt_Full2017)
# print("")
# print("")
# print("")

# # WHSS Full 2017 low_pt
# combine_command_WHSS_high_pt_Full2017 = tmp_command + WHSS_2017_low_pt + " > Combination/WH_chargeAsymmetry_WH_WHSS_low_pt_Full2017_v9{0}.txt".format(output_name_suffix)
# print(combine_command_WHSS_high_pt_Full2017)
# os.system(combine_command_WHSS_high_pt_Full2017)
# print("")
# print("")
# print("")

# # WH3l Full 2017
# combine_command_WH3l_Full2017 = tmp_command + WH3l_2017 + " > Combination/WH_chargeAsymmetry_WH_WH3l_Full2017_v9{0}.txt".format(output_name_suffix)
# print(combine_command_WH3l_Full2017)
# os.system(combine_command_WH3l_Full2017)
# print("")
# print("")
# print("")


# # WHSS and WH3l 2016noHIPM
# combine_command_2016noHIPM = tmp_command + WHSS_2016noHIPM_high_pt + WHSS_2016noHIPM_low_pt + WH3l_2016noHIPM + " > Combination/WH_chargeAsymmetry_WH_2016noHIPM_v9{0}.txt".format(output_name_suffix)
# print(combine_command_2016noHIPM)
# os.system(combine_command_2016noHIPM)
# print("")
# print("")
# print("")

# # WHSS 2016noHIPM
# combine_command_WHSS_2016noHIPM = tmp_command + WHSS_2016noHIPM_high_pt + WHSS_2016noHIPM_low_pt + " > Combination/WH_chargeAsymmetry_WH_WHSS_2016noHIPM_v9{0}.txt".format(output_name_suffix)
# print(combine_command_WHSS_2016noHIPM)
# os.system(combine_command_WHSS_2016noHIPM)
# print("")
# print("")
# print("")

# # WHSS 2016noHIPM high_pt
# combine_command_WHSS_high_pt_2016noHIPM = tmp_command + WHSS_2016noHIPM_high_pt + " > Combination/WH_chargeAsymmetry_WH_WHSS_high_pt_2016noHIPM_v9{0}.txt".format(output_name_suffix)
# print(combine_command_WHSS_high_pt_2016noHIPM)
# os.system(combine_command_WHSS_high_pt_2016noHIPM)
# print("")
# print("")
# print("")

# # WHSS 2016noHIPM low_pt
# combine_command_WHSS_high_pt_2016noHIPM = tmp_command + WHSS_2016noHIPM_low_pt + " > Combination/WH_chargeAsymmetry_WH_WHSS_low_pt_2016noHIPM_v9{0}.txt".format(output_name_suffix)
# print(combine_command_WHSS_high_pt_2016noHIPM)
# os.system(combine_command_WHSS_high_pt_2016noHIPM)
# print("")
# print("")
# print("")

# # WH3l 2016noHIPM
# combine_command_WH3l_2016noHIPM = tmp_command + WH3l_2016noHIPM + " > Combination/WH_chargeAsymmetry_WH_WH3l_2016noHIPM_v9{0}.txt".format(output_name_suffix)
# print(combine_command_WH3l_2016noHIPM)
# os.system(combine_command_WH3l_2016noHIPM)
# print("")
# print("")
# print("")


# # WHSS and WH3l 2016HIPM
# combine_command_2016HIPM = tmp_command + WHSS_2016HIPM_high_pt + WHSS_2016HIPM_low_pt + WH3l_2016HIPM + " > Combination/WH_chargeAsymmetry_WH_2016HIPM_v9{0}.txt".format(output_name_suffix)
# print(combine_command_2016HIPM)
# os.system(combine_command_2016HIPM)
# print("")
# print("")
# print("")

# # WHSS 2016HIPM
# combine_command_WHSS_2016HIPM = tmp_command + WHSS_2016HIPM_high_pt + WHSS_2016HIPM_low_pt + " > Combination/WH_chargeAsymmetry_WH_WHSS_2016HIPM_v9{0}.txt".format(output_name_suffix)
# print(combine_command_WHSS_2016HIPM)
# os.system(combine_command_WHSS_2016HIPM)
# print("")
# print("")
# print("")

# # WHSS 2016HIPM high_pt
# combine_command_WHSS_high_pt_2016HIPM = tmp_command + WHSS_2016HIPM_high_pt + " > Combination/WH_chargeAsymmetry_WH_WHSS_high_pt_2016HIPM_v9{0}.txt".format(output_name_suffix)
# print(combine_command_WHSS_high_pt_2016HIPM)
# os.system(combine_command_WHSS_high_pt_2016HIPM)
# print("")
# print("")
# print("")

# # WHSS 2016HIPM low_pt
# combine_command_WHSS_high_pt_2016HIPM = tmp_command + WHSS_2016HIPM_low_pt + " > Combination/WH_chargeAsymmetry_WH_WHSS_low_pt_2016HIPM_v9{0}.txt".format(output_name_suffix)
# print(combine_command_WHSS_high_pt_2016HIPM)
# os.system(combine_command_WHSS_high_pt_2016HIPM)
# print("")
# print("")
# print("")

# # WH3l 2016HIPM
# combine_command_WH3l_2016HIPM = tmp_command + WH3l_2016HIPM + " > Combination/WH_chargeAsymmetry_WH_WH3l_2016HIPM_v9{0}.txt".format(output_name_suffix)
# print(combine_command_WH3l_2016HIPM)
# os.system(combine_command_WH3l_2016HIPM)
# print("")
# print("")
# print("")
