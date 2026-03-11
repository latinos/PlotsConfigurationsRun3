import sys,os

variable = ""

print("#######################")
print("Number of arguments: {}".format(len(sys.argv)))
print("Argument List: {}".format(str(sys.argv)))
if (len(sys.argv) > 1):
    variable = sys.argv[1]
    print(f"Variable: {variable}")
else:
    print("Please specify the variable you want to use. E.g.:")
    print("python script_combine_datacards_variable.py mll")
    sys.exit()
print("#######################")

# ---------
# Full 2018
# ---------

# 2018 datacards
WHSS_2018_high_pt = f"WH_SS_em_1j_minus_2018=../Full2018_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_em_1j_minus_pt2ge20/{variable}/datacard.txt         \
                      WH_SS_em_1j_plus_2018=../Full2018_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_em_1j_plus_pt2ge20/{variable}/datacard.txt           \
                      WH_SS_mm_1j_minus_2018=../Full2018_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_minus_pt2ge20/{variable}/datacard.txt \
                      WH_SS_mm_1j_plus_2018=../Full2018_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_plus_pt2ge20/{variable}/datacard.txt   \
                      WH_SS_ee_1j_minus_2018=../Full2018_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_ee_1j_minus_pt2ge20/{variable}/datacard.txt         \
                      WH_SS_ee_1j_plus_2018=../Full2018_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_ee_1j_plus_pt2ge20/{variable}/datacard.txt           \
                      WH_SS_em_2j_minus_2018=../Full2018_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_em_2j_minus_pt2ge20/{variable}/datacard.txt         \
                      WH_SS_em_2j_plus_2018=../Full2018_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_em_2j_plus_pt2ge20/{variable}/datacard.txt           \
                      WH_SS_mm_2j_minus_2018=../Full2018_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_minus_pt2ge20/{variable}/datacard.txt \
                      WH_SS_mm_2j_plus_2018=../Full2018_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_plus_pt2ge20/{variable}/datacard.txt   \
                      WH_SS_ee_2j_minus_2018=../Full2018_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_ee_2j_minus_pt2ge20/{variable}/datacard.txt         \
                      WH_SS_ee_2j_plus_2018=../Full2018_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_ee_2j_plus_pt2ge20/{variable}/datacard.txt           \
                      "

WHSS_2018_WZ_CR_SS_events = f"WH_SS_WZ_1j_2018=../Full2018_v9/WH3l/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_WZ_1j/events/datacard.txt \
                              WH_SS_WZ_2j_2018=../Full2018_v9/WH3l/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_WZ_2j/events/datacard.txt \
                              "

WHSS_2018_WZ_CR_SS_var = f"WH_SS_WZ_1j_2018=../Full2018_v9/WH3l/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_WZ_1j/{variable}/datacard.txt \
                           WH_SS_WZ_2j_2018=../Full2018_v9/WH3l/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_WZ_2j/{variable}/datacard.txt \
                           "

WH3l_2018 = f"WH_3l_sssf_plus_2018=../Full2018_v9/WH3l/datacards_original_signal_scale/wh3l_13TeV_sssf_plus_pt2ge20/{variable}/datacard.txt   \
              WH_3l_sssf_minus_2018=../Full2018_v9/WH3l/datacards_original_signal_scale/wh3l_13TeV_sssf_minus_pt2ge20/{variable}/datacard.txt \
              WH_3l_ossf_plus_2018=../Full2018_v9/WH3l/datacards_original_signal_scale/wh3l_13TeV_ossf_plus_pt2ge20/{variable}/datacard.txt   \
              WH_3l_ossf_minus_2018=../Full2018_v9/WH3l/datacards_original_signal_scale/wh3l_13TeV_ossf_minus_pt2ge20/{variable}/datacard.txt \
              "

WH3l_2018_WZ_CR_3l_events = f"WH_3l_WZ_CR_0j_2018=../Full2018_v9/WH3l/datacards_original_signal_scale/wh3l_wz_13TeV/events/datacard.txt "

WH3l_2018_WZ_CR_3l_var    = f"WH_3l_WZ_CR_0j_2018=../Full2018_v9/WH3l/datacards_original_signal_scale/wh3l_wz_13TeV/{variable}/datacard.txt "

# ---------
# Full 2017
# ---------

# 2017 datacards
WHSS_2017_high_pt = f"WH_SS_em_1j_minus_2017=../Full2017_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_em_1j_minus_pt2ge20/{variable}/datacard.txt         \
                      WH_SS_em_1j_plus_2017=../Full2017_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_em_1j_plus_pt2ge20/{variable}/datacard.txt           \
                      WH_SS_mm_1j_minus_2017=../Full2017_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_minus_pt2ge20/{variable}/datacard.txt \
                      WH_SS_mm_1j_plus_2017=../Full2017_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_plus_pt2ge20/{variable}/datacard.txt   \
                      WH_SS_ee_1j_minus_2017=../Full2017_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_ee_1j_minus_pt2ge20/{variable}/datacard.txt         \
                      WH_SS_ee_1j_plus_2017=../Full2017_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_ee_1j_plus_pt2ge20/{variable}/datacard.txt           \
                      WH_SS_em_2j_minus_2017=../Full2017_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_em_2j_minus_pt2ge20/{variable}/datacard.txt         \
                      WH_SS_em_2j_plus_2017=../Full2017_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_em_2j_plus_pt2ge20/{variable}/datacard.txt           \
                      WH_SS_mm_2j_minus_2017=../Full2017_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_minus_pt2ge20/{variable}/datacard.txt \
                      WH_SS_mm_2j_plus_2017=../Full2017_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_plus_pt2ge20/{variable}/datacard.txt   \
                      WH_SS_ee_2j_minus_2017=../Full2017_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_ee_2j_minus_pt2ge20/{variable}/datacard.txt         \
                      WH_SS_ee_2j_plus_2017=../Full2017_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_ee_2j_plus_pt2ge20/{variable}/datacard.txt           \
                      "

WHSS_2017_WZ_CR_SS_events = f"WH_SS_WZ_1j_2017=../Full2017_v9/WH3l/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_WZ_1j/events/datacard.txt \
                              WH_SS_WZ_2j_2017=../Full2017_v9/WH3l/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_WZ_2j/events/datacard.txt \
                              "

WHSS_2017_WZ_CR_SS_var = f"WH_SS_WZ_1j_2017=../Full2017_v9/WH3l/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_WZ_1j/{variable}/datacard.txt \
                           WH_SS_WZ_2j_2017=../Full2017_v9/WH3l/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_WZ_2j/{variable}/datacard.txt \
                           "

WH3l_2017 = f"WH_3l_sssf_plus_2017=../Full2017_v9/WH3l/datacards_original_signal_scale/wh3l_13TeV_sssf_plus_pt2ge20/{variable}/datacard.txt   \
              WH_3l_sssf_minus_2017=../Full2017_v9/WH3l/datacards_original_signal_scale/wh3l_13TeV_sssf_minus_pt2ge20/{variable}/datacard.txt \
              WH_3l_ossf_plus_2017=../Full2017_v9/WH3l/datacards_original_signal_scale/wh3l_13TeV_ossf_plus_pt2ge20/{variable}/datacard.txt   \
              WH_3l_ossf_minus_2017=../Full2017_v9/WH3l/datacards_original_signal_scale/wh3l_13TeV_ossf_minus_pt2ge20/{variable}/datacard.txt \
              "

WH3l_2017_WZ_CR_3l_events = f"WH_3l_WZ_CR_0j_2017=../Full2017_v9/WH3l/datacards_original_signal_scale/wh3l_wz_13TeV/events/datacard.txt "

WH3l_2017_WZ_CR_3l_var    = f"WH_3l_WZ_CR_0j_2017=../Full2017_v9/WH3l/datacards_original_signal_scale/wh3l_wz_13TeV/{variable}/datacard.txt "


# ------------
# 2016 no HIPM
# ------------

# 2016noHIPM datacards
WHSS_2016noHIPM_high_pt = f"WH_SS_em_1j_minus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_em_1j_minus_pt2ge20/{variable}/datacard.txt         \
                            WH_SS_em_1j_plus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_em_1j_plus_pt2ge20/{variable}/datacard.txt           \
                            WH_SS_mm_1j_minus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_minus_pt2ge20/{variable}/datacard.txt \
                            WH_SS_mm_1j_plus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_plus_pt2ge20/{variable}/datacard.txt   \
                            WH_SS_ee_1j_minus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_ee_1j_minus_pt2ge20/{variable}/datacard.txt         \
                            WH_SS_ee_1j_plus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_ee_1j_plus_pt2ge20/{variable}/datacard.txt           \
                            WH_SS_em_2j_minus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_em_2j_minus_pt2ge20/{variable}/datacard.txt         \
                            WH_SS_em_2j_plus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_em_2j_plus_pt2ge20/{variable}/datacard.txt           \
                            WH_SS_mm_2j_minus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_minus_pt2ge20/{variable}/datacard.txt \
                            WH_SS_mm_2j_plus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_plus_pt2ge20/{variable}/datacard.txt   \
                            WH_SS_ee_2j_minus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_ee_2j_minus_pt2ge20/{variable}/datacard.txt         \
                            WH_SS_ee_2j_plus_2016noHIPM=../2016noHIPM_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_ee_2j_plus_pt2ge20/{variable}/datacard.txt           \
                            "

WHSS_2016noHIPM_WZ_CR_SS_events = f"WH_SS_WZ_1j_2016noHIPM=../2016noHIPM_v9/WH3l/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_WZ_1j/events/datacard.txt \
                                    WH_SS_WZ_2j_2016noHIPM=../2016noHIPM_v9/WH3l/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_WZ_2j/events/datacard.txt \
                                    "

WHSS_2016noHIPM_WZ_CR_SS_var = f"WH_SS_WZ_1j_2016noHIPM=../2016noHIPM_v9/WH3l/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_WZ_1j/{variable}/datacard.txt \
                                 WH_SS_WZ_2j_2016noHIPM=../2016noHIPM_v9/WH3l/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_WZ_2j/{variable}/datacard.txt \
                                 "

WH3l_2016noHIPM = f"WH_3l_sssf_plus_2016noHIPM=../2016noHIPM_v9/WH3l/datacards_original_signal_scale/wh3l_13TeV_sssf_plus_pt2ge20/{variable}/datacard.txt   \
                    WH_3l_sssf_minus_2016noHIPM=../2016noHIPM_v9/WH3l/datacards_original_signal_scale/wh3l_13TeV_sssf_minus_pt2ge20/{variable}/datacard.txt \
                    WH_3l_ossf_plus_2016noHIPM=../2016noHIPM_v9/WH3l/datacards_original_signal_scale/wh3l_13TeV_ossf_plus_pt2ge20/{variable}/datacard.txt   \
                    WH_3l_ossf_minus_2016noHIPM=../2016noHIPM_v9/WH3l/datacards_original_signal_scale/wh3l_13TeV_ossf_minus_pt2ge20/{variable}/datacard.txt \
                    "

WH3l_2016noHIPM_WZ_CR_3l_events = f"WH_3l_WZ_CR_0j_2016noHIPM=../2016noHIPM_v9/WH3l/datacards_original_signal_scale/wh3l_wz_13TeV/events/datacard.txt "

WH3l_2016noHIPM_WZ_CR_3l_var    = f"WH_3l_WZ_CR_0j_2016noHIPM=../2016noHIPM_v9/WH3l/datacards_original_signal_scale/wh3l_wz_13TeV/{variable}/datacard.txt "


# ---------
# 2016 HIPM
# ---------

# 2016HIPM datacards
WHSS_2016HIPM_high_pt = f"WH_SS_em_1j_minus_2016HIPM=../2016HIPM_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_em_1j_minus_pt2ge20/{variable}/datacard.txt               \
                          WH_SS_em_1j_plus_2016HIPM=../2016HIPM_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_em_1j_plus_pt2ge20/{variable}/datacard.txt                 \
                          WH_SS_mm_1j_minus_2016HIPM=../2016HIPM_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_minus_pt2ge20/{variable}/datacard.txt       \
                          WH_SS_mm_1j_plus_2016HIPM=../2016HIPM_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_plus_pt2ge20/{variable}/datacard.txt         \
                          WH_SS_ee_1j_minus_2016HIPM=../2016HIPM_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_ee_1j_minus_pt2ge20/{variable}/datacard.txt               \
                          WH_SS_ee_1j_plus_2016HIPM=../2016HIPM_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_ee_1j_plus_pt2ge20/{variable}/datacard.txt                 \
                          WH_SS_em_2j_minus_2016HIPM=../2016HIPM_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_em_2j_minus_pt2ge20/{variable}/datacard.txt               \
                          WH_SS_em_2j_plus_2016HIPM=../2016HIPM_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_em_2j_plus_pt2ge20/{variable}/datacard.txt                 \
                          WH_SS_mm_2j_minus_2016HIPM=../2016HIPM_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_minus_pt2ge20/{variable}/datacard.txt       \
                          WH_SS_mm_2j_plus_2016HIPM=../2016HIPM_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_plus_pt2ge20/{variable}/datacard.txt         \
                          WH_SS_ee_2j_minus_2016HIPM=../2016HIPM_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_ee_2j_minus_pt2ge20/{variable}/datacard.txt               \
                          WH_SS_ee_2j_plus_2016HIPM=../2016HIPM_v9/WHSS/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_ee_2j_plus_pt2ge20/{variable}/datacard.txt                 \
                          "

WHSS_2016HIPM_WZ_CR_SS_events = f"WH_SS_WZ_1j_2016HIPM=../2016HIPM_v9/WH3l/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_WZ_1j/events/datacard.txt \
                                  WH_SS_WZ_2j_2016HIPM=../2016HIPM_v9/WH3l/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_WZ_2j/events/datacard.txt \
                                  "

WHSS_2016HIPM_WZ_CR_SS_var = f"WH_SS_WZ_1j_2016HIPM=../2016HIPM_v9/WH3l/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_WZ_1j/{variable}/datacard.txt \
                               WH_SS_WZ_2j_2016HIPM=../2016HIPM_v9/WH3l/datacards_original_signal_scale/hww2l2v_13TeV_WH_SS_WZ_2j/{variable}/datacard.txt \
                               "

WH3l_2016HIPM = f"WH_3l_sssf_plus_2016HIPM=../2016HIPM_v9/WH3l/datacards_original_signal_scale/wh3l_13TeV_sssf_plus_pt2ge20/{variable}/datacard.txt   \
                  WH_3l_sssf_minus_2016HIPM=../2016HIPM_v9/WH3l/datacards_original_signal_scale/wh3l_13TeV_sssf_minus_pt2ge20/{variable}/datacard.txt \
                  WH_3l_ossf_plus_2016HIPM=../2016HIPM_v9/WH3l/datacards_original_signal_scale/wh3l_13TeV_ossf_plus_pt2ge20/{variable}/datacard.txt   \
                  WH_3l_ossf_minus_2016HIPM=../2016HIPM_v9/WH3l/datacards_original_signal_scale/wh3l_13TeV_ossf_minus_pt2ge20/{variable}/datacard.txt \
                  "

WH3l_2016HIPM_WZ_CR_3l_events = f"WH_3l_WZ_CR_0j_2016HIPM=../2016HIPM_v9/WH3l/datacards_original_signal_scale/wh3l_wz_13TeV/events/datacard.txt "

WH3l_2016HIPM_WZ_CR_3l_var    = f"WH_3l_WZ_CR_0j_2016HIPM=../2016HIPM_v9/WH3l/datacards_original_signal_scale/wh3l_wz_13TeV/{variable}/datacard.txt "


# Here we define the actual combine commands we want to use
os.system("mkdir -p Combination")

tmp_command = "combineCards.py "

##################
### Full Run 2 ###
##################

# Full Run 2 WHSS and WH3l high pT plus control regions
combine_command_FullRun2_high_pt = tmp_command + WHSS_2018_high_pt       + WH3l_2018       + WHSS_2018_WZ_CR_SS_events       + WH3l_2018_WZ_CR_3l_events       \
                                               + WHSS_2017_high_pt       + WH3l_2017       + WHSS_2017_WZ_CR_SS_events       + WH3l_2017_WZ_CR_3l_events       \
                                               + WHSS_2016noHIPM_high_pt + WH3l_2016noHIPM + WHSS_2016noHIPM_WZ_CR_SS_events + WH3l_2016noHIPM_WZ_CR_3l_events \
                                               + WHSS_2016HIPM_high_pt   + WH3l_2016HIPM   + WHSS_2016HIPM_WZ_CR_SS_events   + WH3l_2016HIPM_WZ_CR_3l_events   \
                                               + f" > Combination/WH_chargeAsymmetry_WH_FullRun2_v9_high_pt_{variable}.txt"
print(combine_command_FullRun2_high_pt)
os.system(combine_command_FullRun2_high_pt)
print("")
print("")
print("")
# Fixing nuisances yielding negative integral
with open (f"Combination/WH_chargeAsymmetry_WH_FullRun2_v9_high_pt_{variable}.txt","a") as my_datacard:
    my_datacard.write("nuisance edit drop WH_htt_plus  WH_SS_mm_1j_minus_2018 CMS_scale_met_2018")

    
# Full Run 2 WHSS high pT plus control regions
combine_command_FullRun2_WHSS_high_pt = tmp_command + WHSS_2018_high_pt       + WHSS_2018_WZ_CR_SS_events       \
                                                    + WHSS_2017_high_pt       + WHSS_2017_WZ_CR_SS_events       \
                                                    + WHSS_2016noHIPM_high_pt + WHSS_2016noHIPM_WZ_CR_SS_events \
                                                    + WHSS_2016HIPM_high_pt   + WHSS_2016HIPM_WZ_CR_SS_events   \
                                                    + f" > Combination/WH_chargeAsymmetry_WH_FullRun2_v9_WHSS_high_pt_{variable}.txt"
print(combine_command_FullRun2_WHSS_high_pt)
os.system(combine_command_FullRun2_WHSS_high_pt)
print("")
print("")
print("")
# Fixing nuisances yielding negative integral
with open (f"Combination/WH_chargeAsymmetry_WH_FullRun2_v9_WHSS_high_pt_{variable}.txt","a") as my_datacard:
    my_datacard.write("nuisance edit drop WH_htt_plus  WH_SS_mm_1j_minus_2018 CMS_scale_met_2018")

# Full Run 2 WH3l high pT
combine_command_FullRun2_WH3l = tmp_command + WH3l_2018       + WH3l_2018_WZ_CR_3l_events       \
                                            + WH3l_2017       + WH3l_2017_WZ_CR_3l_events       \
                                            + WH3l_2016noHIPM + WH3l_2016noHIPM_WZ_CR_3l_events \
                                            + WH3l_2016HIPM   + WH3l_2016HIPM_WZ_CR_3l_events   \
                                            + f" > Combination/WH_chargeAsymmetry_WH_FullRun2_v9_WH3l_{variable}.txt"
print(combine_command_FullRun2_WH3l)
os.system(combine_command_FullRun2_WH3l)
print("")
print("")
print("")

#############################
### Full 2017 + Full 2018 ###
#############################

# Full 2017 + Full 2018 WHSS and WH3l high pT plus control regions
combine_command_2017_2018_high_pt = tmp_command + WHSS_2018_high_pt       + WH3l_2018       + WHSS_2018_WZ_CR_SS_events       + WH3l_2018_WZ_CR_3l_events       \
                                                + WHSS_2017_high_pt       + WH3l_2017       + WHSS_2017_WZ_CR_SS_events       + WH3l_2017_WZ_CR_3l_events       \
                                                + f" > Combination/WH_chargeAsymmetry_WH_2017_2018_v9_high_pt_{variable}.txt"
print(combine_command_2017_2018_high_pt)
os.system(combine_command_2017_2018_high_pt)
print("")
print("")
print("")
# Fixing nuisances yielding negative integral
with open (f"Combination/WH_chargeAsymmetry_WH_2017_2018_v9_high_pt_{variable}.txt","a") as my_datacard:
    my_datacard.write("nuisance edit drop WH_htt_plus  WH_SS_mm_1j_minus_2018 CMS_scale_met_2018")

# Full 2017 + Full 2018 WHSS high pT plus control regions
combine_command_2017_2018_WHSS_high_pt = tmp_command + WHSS_2018_high_pt       + WHSS_2018_WZ_CR_SS_events       \
                                                     + WHSS_2017_high_pt       + WHSS_2017_WZ_CR_SS_events       \
                                                     + f" > Combination/WH_chargeAsymmetry_WH_2017_2018_v9_WHSS_high_pt_{variable}.txt"
print(combine_command_2017_2018_WHSS_high_pt)
os.system(combine_command_2017_2018_WHSS_high_pt)
print("")
print("")
print("")
# Fixing nuisances yielding negative integral
with open (f"Combination/WH_chargeAsymmetry_WH_2017_2018_v9_WHSS_high_pt_{variable}.txt","a") as my_datacard:
    my_datacard.write("nuisance edit drop WH_htt_plus  WH_SS_mm_1j_minus_2018 CMS_scale_met_2018")

# Full 2017 + Full 2018 WH3l high pT
combine_command_2017_2018_WH3l = tmp_command + WH3l_2018       + WH3l_2018_WZ_CR_3l_events       \
                                             + WH3l_2017       + WH3l_2017_WZ_CR_3l_events       \
                                             + f" > Combination/WH_chargeAsymmetry_WH_2017_2018_v9_WH3l_{variable}.txt"
print(combine_command_2017_2018_WH3l)
os.system(combine_command_2017_2018_WH3l)
print("")
print("")
print("")


##########################################
### 2016noHIPM + Full 2017 + Full 2018 ###
##########################################

# 2016noHIPM + Full 2017 + Full 2018 WHSS and WH3l high pT plus control regions
combine_command_2016noHIPM_2017_2018_high_pt = tmp_command + WHSS_2018_high_pt       + WH3l_2018       + WHSS_2018_WZ_CR_SS_events       + WH3l_2018_WZ_CR_3l_events       \
                                                           + WHSS_2017_high_pt       + WH3l_2017       + WHSS_2017_WZ_CR_SS_events       + WH3l_2017_WZ_CR_3l_events       \
                                                           + WHSS_2016noHIPM_high_pt + WH3l_2016noHIPM + WHSS_2016noHIPM_WZ_CR_SS_events + WH3l_2016noHIPM_WZ_CR_3l_events \
                                                           + f" > Combination/WH_chargeAsymmetry_WH_2016noHIPM_2017_2018_v9_high_pt_{variable}.txt"
print(combine_command_2016noHIPM_2017_2018_high_pt)
os.system(combine_command_2016noHIPM_2017_2018_high_pt)
print("")
print("")
print("")
# Fixing nuisances yielding negative integral
with open (f"Combination/WH_chargeAsymmetry_WH_2016noHIPM_2017_2018_v9_high_pt_{variable}.txt","a") as my_datacard:
    my_datacard.write("nuisance edit drop WH_htt_plus  WH_SS_mm_1j_minus_2018 CMS_scale_met_2018")

# 2016noHIPM + Full 2017 + Full 2018 WHSS high pT plus control regions
combine_command_2016noHIPM_2017_2018_WHSS_high_pt = tmp_command + WHSS_2018_high_pt       + WHSS_2018_WZ_CR_SS_events       \
                                                                + WHSS_2017_high_pt       + WHSS_2017_WZ_CR_SS_events       \
                                                                + WHSS_2016noHIPM_high_pt + WHSS_2016noHIPM_WZ_CR_SS_events \
                                                                + f" > Combination/WH_chargeAsymmetry_WH_2016noHIPM_2017_2018_v9_WHSS_high_pt_{variable}.txt"
print(combine_command_2016noHIPM_2017_2018_WHSS_high_pt)
os.system(combine_command_2016noHIPM_2017_2018_WHSS_high_pt)
print("")
print("")
print("")
# Fixing nuisances yielding negative integral
with open (f"Combination/WH_chargeAsymmetry_WH_2016noHIPM_2017_2018_v9_WHSS_high_pt_{variable}.txt","a") as my_datacard:
    my_datacard.write("nuisance edit drop WH_htt_plus  WH_SS_mm_1j_minus_2018 CMS_scale_met_2018")

# 2016noHIPM + Full 2017 + Full 2018 WH3l high pT
combine_command_2016noHIPM_2017_2018_WH3l = tmp_command + WH3l_2018       + WH3l_2018_WZ_CR_3l_events       \
                                                        + WH3l_2017       + WH3l_2017_WZ_CR_3l_events       \
                                                        + WH3l_2016noHIPM + WH3l_2016noHIPM_WZ_CR_3l_events \
                                                        + f" > Combination/WH_chargeAsymmetry_WH_2016noHIPM_2017_2018_v9_WH3l_{variable}.txt"
print(combine_command_2016noHIPM_2017_2018_WH3l)
os.system(combine_command_2016noHIPM_2017_2018_WH3l)
print("")
print("")
print("")


##########################################
### 2016HIPM + Full 2017 + Full 2018 ###
##########################################

# 2016HIPM + Full 2017 + Full 2018 WHSS and WH3l high pT plus control regions
combine_command_2016HIPM_2017_2018_high_pt = tmp_command + WHSS_2018_high_pt       + WH3l_2018       + WHSS_2018_WZ_CR_SS_events       + WH3l_2018_WZ_CR_3l_events     \
                                                         + WHSS_2017_high_pt       + WH3l_2017       + WHSS_2017_WZ_CR_SS_events       + WH3l_2017_WZ_CR_3l_events     \
                                                         + WHSS_2016HIPM_high_pt   + WH3l_2016HIPM   + WHSS_2016HIPM_WZ_CR_SS_events   + WH3l_2016HIPM_WZ_CR_3l_events \
                                                         + f" > Combination/WH_chargeAsymmetry_WH_2016HIPM_2017_2018_v9_high_pt_{variable}.txt"
print(combine_command_2016HIPM_2017_2018_high_pt)
os.system(combine_command_2016HIPM_2017_2018_high_pt)
print("")
print("")
print("")
# Fixing nuisances yielding negative integral
with open (f"Combination/WH_chargeAsymmetry_WH_2016HIPM_2017_2018_v9_high_pt_{variable}.txt","a") as my_datacard:
    my_datacard.write("nuisance edit drop WH_htt_plus  WH_SS_mm_1j_minus_2018 CMS_scale_met_2018")

# 2016HIPM + Full 2017 + Full 2018 WHSS high pT plus control regions
combine_command_2016HIPM_2017_2018_WHSS_high_pt = tmp_command + WHSS_2018_high_pt       + WHSS_2018_WZ_CR_SS_events     \
                                                              + WHSS_2017_high_pt       + WHSS_2017_WZ_CR_SS_events     \
                                                              + WHSS_2016HIPM_high_pt   + WHSS_2016HIPM_WZ_CR_SS_events \
                                                              + f" > Combination/WH_chargeAsymmetry_WH_2016HIPM_2017_2018_v9_WHSS_high_pt_{variable}.txt"
print(combine_command_2016HIPM_2017_2018_WHSS_high_pt)
os.system(combine_command_2016HIPM_2017_2018_WHSS_high_pt)
print("")
print("")
print("")
# Fixing nuisances yielding negative integral
with open (f"Combination/WH_chargeAsymmetry_WH_2016HIPM_2017_2018_v9_WHSS_high_pt_{variable}.txt","a") as my_datacard:
    my_datacard.write("nuisance edit drop WH_htt_plus  WH_SS_mm_1j_minus_2018 CMS_scale_met_2018")

# 2016HIPM + Full 2017 + Full 2018 WH3l high pT
combine_command_2016HIPM_2017_2018_WH3l = tmp_command + WH3l_2018       + WH3l_2018_WZ_CR_3l_events     \
                                                      + WH3l_2017       + WH3l_2017_WZ_CR_3l_events     \
                                                      + WH3l_2016HIPM   + WH3l_2016HIPM_WZ_CR_3l_events \
                                                      + f" > Combination/WH_chargeAsymmetry_WH_2016HIPM_2017_2018_v9_WH3l_{variable}.txt"
print(combine_command_2016HIPM_2017_2018_WH3l)
os.system(combine_command_2016HIPM_2017_2018_WH3l)
print("")
print("")
print("")


#################
### Full 2016 ###
#################

# Full 2016 WHSS and WH3l high pT plus control regions
combine_command_Full2016_high_pt = tmp_command + WHSS_2016noHIPM_high_pt + WH3l_2016noHIPM + WHSS_2016noHIPM_WZ_CR_SS_events + WH3l_2016noHIPM_WZ_CR_3l_events \
                                               + WHSS_2016HIPM_high_pt   + WH3l_2016HIPM   + WHSS_2016HIPM_WZ_CR_SS_events   + WH3l_2016HIPM_WZ_CR_3l_events   \
                                               + f" > Combination/WH_chargeAsymmetry_WH_Full2016_v9_high_pt_{variable}.txt"
print(combine_command_Full2016_high_pt)
os.system(combine_command_Full2016_high_pt)
print("")
print("")
print("")

# Full 2016 WHSS high pT plus control regions
combine_command_Full2016_WHSS_high_pt = tmp_command + WHSS_2016noHIPM_high_pt + WHSS_2016noHIPM_WZ_CR_SS_events \
                                                    + WHSS_2016HIPM_high_pt   + WHSS_2016HIPM_WZ_CR_SS_events   \
                                                    + f" > Combination/WH_chargeAsymmetry_WH_Full2016_v9_WHSS_high_pt_{variable}.txt"
print(combine_command_Full2016_WHSS_high_pt)
os.system(combine_command_Full2016_WHSS_high_pt)
print("")
print("")
print("")

# Full 2016 WH3l high pT
combine_command_Full2016_WH3l = tmp_command + WH3l_2016noHIPM + WH3l_2016noHIPM_WZ_CR_3l_events \
                                            + WH3l_2016HIPM   + WH3l_2016HIPM_WZ_CR_3l_events   \
                                            + f" > Combination/WH_chargeAsymmetry_WH_Full2016_v9_WH3l_{variable}.txt"
print(combine_command_Full2016_WH3l)
os.system(combine_command_Full2016_WH3l)
print("")
print("")
print("")

#################
### Full 2018 ###
#################

# Full 2018 WHSS and WH3l high pt
combine_command_Full2018_high_pt = tmp_command + WHSS_2018_high_pt + WH3l_2018 + WHSS_2018_WZ_CR_SS_events + WH3l_2018_WZ_CR_3l_events \
                                               + f" > Combination/WH_chargeAsymmetry_WH_Full2018_v9_high_pt_{variable}.txt"
print(combine_command_Full2018_high_pt)
os.system(combine_command_Full2018_high_pt)
print("")
print("")
print("")
# Fixing nuisances yielding negative integral
with open (f"Combination/WH_chargeAsymmetry_WH_Full2018_v9_high_pt_{variable}.txt","a") as my_datacard:
    my_datacard.write("nuisance edit drop WH_htt_plus  WH_SS_mm_1j_minus_2018 CMS_scale_met_2018")

# Full 2018 WHSS and WH3l high pt no WZ CR
combine_command_Full2018_high_pt_noCR = tmp_command + WHSS_2018_high_pt + WH3l_2018 \
                                                   + f" > Combination/WH_chargeAsymmetry_WH_Full2018_v9_high_pt_noCR_{variable}.txt"
print(combine_command_Full2018_high_pt_noCR)
os.system(combine_command_Full2018_high_pt_noCR)
print("")
print("")
print("")
# Fixing nuisances yielding negative integral
with open (f"Combination/WH_chargeAsymmetry_WH_Full2018_v9_WHSS_high_pt_noCR_{variable}.txt","a") as my_datacard:
    my_datacard.write("nuisance edit drop WH_htt_plus  WH_SS_mm_1j_minus_2018 CMS_scale_met_2018")

# Full 2018 WHSS high_pt
combine_command_Full2018_WHSS_high_pt = tmp_command + WHSS_2018_high_pt + WHSS_2018_WZ_CR_SS_events \
                                                    + f" > Combination/WH_chargeAsymmetry_WH_Full2018_v9_WHSS_high_pt_{variable}.txt"
print(combine_command_Full2018_WHSS_high_pt)
os.system(combine_command_Full2018_WHSS_high_pt)
print("")
print("")
print("")
# Fixing nuisances yielding negative integral
with open (f"Combination/WH_chargeAsymmetry_WH_Full2018_v9_WHSS_high_pt_{variable}.txt","a") as my_datacard:
    my_datacard.write("nuisance edit drop WH_htt_plus  WH_SS_mm_1j_minus_2018 CMS_scale_met_2018")

# Full 2018 WHSS high_pt no WZ CR
combine_command_Full2018_WHSS_high_pt_noCR = tmp_command + WHSS_2018_high_pt \
                                                        + f" > Combination/WH_chargeAsymmetry_WH_Full2018_v9_WHSS_high_pt_noCR_{variable}.txt"
print(combine_command_Full2018_WHSS_high_pt_noCR)
os.system(combine_command_Full2018_WHSS_high_pt_noCR)
print("")
print("")
print("")
# Fixing nuisances yielding negative integral
with open (f"Combination/WH_chargeAsymmetry_WH_Full2018_v9_WHSS_high_pt_noCR_{variable}.txt","a") as my_datacard:
    my_datacard.write("nuisance edit drop WH_htt_plus  WH_SS_mm_1j_minus_2018 CMS_scale_met_2018")

# Full 2018 WH3l
combine_command_Full2018_WH3l = tmp_command + WH3l_2018 + WH3l_2018_WZ_CR_3l_events \
                                            + f" > Combination/WH_chargeAsymmetry_WH_Full2018_v9_WH3l_{variable}.txt"
print(combine_command_Full2018_WH3l)
os.system(combine_command_Full2018_WH3l)
print("")
print("")
print("")

# Full 2018 WH3l no WZ CR
combine_command_Full2018_WH3l_noCR = tmp_command + WH3l_2018 \
                                            + f" > Combination/WH_chargeAsymmetry_WH_Full2018_v9_WH3l_noCR_{variable}.txt"
print(combine_command_Full2018_WH3l_noCR)
os.system(combine_command_Full2018_WH3l_noCR)
print("")
print("")
print("")


#################
### Full 2017 ###
#################

# Full 2017 WHSS and WH3l high pt
combine_command_Full2017_high_pt = tmp_command + WHSS_2017_high_pt + WH3l_2017 + WHSS_2017_WZ_CR_SS_events + WH3l_2017_WZ_CR_3l_events \
                                               + f" > Combination/WH_chargeAsymmetry_WH_Full2017_v9_high_pt_{variable}.txt"
print(combine_command_Full2017_high_pt)
os.system(combine_command_Full2017_high_pt)
print("")
print("")
print("")

# Full 2017 WHSS high_pt
combine_command_Full2017_WHSS_high_pt = tmp_command + WHSS_2017_high_pt + WHSS_2017_WZ_CR_SS_events \
                                                    + f" > Combination/WH_chargeAsymmetry_WH_Full2017_v9_WHSS_high_pt_{variable}.txt"
print(combine_command_Full2017_WHSS_high_pt)
os.system(combine_command_Full2017_WHSS_high_pt)
print("")
print("")
print("")

# Full 2017 WH3l
combine_command_Full2017_WH3l = tmp_command + WH3l_2017 + WH3l_2017_WZ_CR_3l_events \
                                            + f" > Combination/WH_chargeAsymmetry_WH_Full2017_v9_WH3l_{variable}.txt"
print(combine_command_Full2017_WH3l)
os.system(combine_command_Full2017_WH3l)
print("")
print("")
print("")


##################
### 2016noHIPM ###
##################

# 2016noHIPM WHSS and WH3l high pt
combine_command_2016noHIPM_high_pt = tmp_command + WHSS_2016noHIPM_high_pt + WH3l_2016noHIPM + WHSS_2016noHIPM_WZ_CR_SS_events + WH3l_2016noHIPM_WZ_CR_3l_events \
                                                 + f" > Combination/WH_chargeAsymmetry_WH_2016noHIPM_v9_high_pt_{variable}.txt"
print(combine_command_2016noHIPM_high_pt)
os.system(combine_command_2016noHIPM_high_pt)
print("")
print("")
print("")

# 2016noHIPM WHSS high_pt
combine_command_2016noHIPM_WHSS_high_pt = tmp_command + WHSS_2016noHIPM_high_pt + WHSS_2016noHIPM_WZ_CR_SS_events \
                                                      + f" > Combination/WH_chargeAsymmetry_WH_2016noHIPM_v9_WHSS_high_pt_{variable}.txt"
print(combine_command_2016noHIPM_WHSS_high_pt)
os.system(combine_command_2016noHIPM_WHSS_high_pt)
print("")
print("")
print("")

# 2016noHIPM WH3l
combine_command_2016noHIPM_WH3l = tmp_command + WH3l_2016noHIPM + WH3l_2016noHIPM_WZ_CR_3l_events \
                                              + f" > Combination/WH_chargeAsymmetry_WH_2016noHIPM_v9_WH3l_{variable}.txt"
print(combine_command_2016noHIPM_WH3l)
os.system(combine_command_2016noHIPM_WH3l)
print("")
print("")
print("")


################
### 2016HIPM ###
################

# 2016HIPM WHSS and WH3l high pt
combine_command_2016HIPM_high_pt = tmp_command + WHSS_2016HIPM_high_pt + WH3l_2016HIPM + WHSS_2016HIPM_WZ_CR_SS_events + WH3l_2016HIPM_WZ_CR_3l_events \
                                               + f" > Combination/WH_chargeAsymmetry_WH_2016HIPM_v9_high_pt_{variable}.txt"
print(combine_command_2016HIPM_high_pt)
os.system(combine_command_2016HIPM_high_pt)
print("")
print("")
print("")

# 2016HIPM WHSS high_pt
combine_command_2016HIPM_WHSS_high_pt = tmp_command + WHSS_2016HIPM_high_pt + WHSS_2016HIPM_WZ_CR_SS_events \
                                                    + f" > Combination/WH_chargeAsymmetry_WH_2016HIPM_v9_WHSS_high_pt_{variable}.txt"
print(combine_command_2016HIPM_WHSS_high_pt)
os.system(combine_command_2016HIPM_WHSS_high_pt)
print("")
print("")
print("")

# 2016HIPM WH3l
combine_command_2016HIPM_WH3l = tmp_command + WH3l_2016HIPM + WH3l_2016HIPM_WZ_CR_3l_events \
                                            + f" > Combination/WH_chargeAsymmetry_WH_2016HIPM_v9_WH3l_{variable}.txt"
print(combine_command_2016HIPM_WH3l)
os.system(combine_command_2016HIPM_WH3l)
print("")
print("")
print("")
