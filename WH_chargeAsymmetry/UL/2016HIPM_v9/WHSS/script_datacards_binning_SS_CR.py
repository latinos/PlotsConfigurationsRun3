import sys,os

# Define variables and strategy to use
suffix    = ["_original_signal_scale"]

# Actually combine datacards
#for var in variables:
for suff in suffix:
    
    # Using ee, em, and mm final state, and including low-pT categories. Remove the Z veto for the mm final state.
    tmp_command = "combineCards.py WH_SS_em_2j_minus=datacards{0}/hww2l2v_13TeV_WH_SS_em_2j_minus_pt2ge20/BDTG6_TT_0_5/datacard.txt \
                                   WH_SS_em_2j_plus=datacards{0}/hww2l2v_13TeV_WH_SS_em_2j_plus_pt2ge20/BDTG6_TT_0_5/datacard.txt \
                     	           WH_SS_mm_2j_minus=datacards{0}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_minus_pt2ge20/BDTG6_TT_0_5/datacard.txt \
                     		   WH_SS_mm_2j_plus=datacards{0}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_plus_pt2ge20/BDTG6_TT_0_5/datacard.txt \
                     		   WH_SS_ee_2j_minus=datacards{0}/hww2l2v_13TeV_WH_SS_ee_2j_minus_pt2ge20/BDTG6_TT_0_0/datacard.txt \
                     		   WH_SS_ee_2j_plus=datacards{0}/hww2l2v_13TeV_WH_SS_ee_2j_plus_pt2ge20/BDTG6_TT_0_0/datacard.txt \
                                   WH_SS_em_1j_minus=datacards{0}/hww2l2v_13TeV_WH_SS_em_1j_minus_pt2ge20/BDTG6_TT_0_6/datacard.txt \
                                   WH_SS_em_1j_plus=datacards{0}/hww2l2v_13TeV_WH_SS_em_1j_plus_pt2ge20/BDTG6_TT_0_6/datacard.txt \
                                   WH_SS_mm_1j_minus=datacards{0}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_minus_pt2ge20/BDTG6_TT_0_6/datacard.txt \
                                   WH_SS_mm_1j_plus=datacards{0}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_plus_pt2ge20/BDTG6_TT_0_6/datacard.txt \
                                   WH_SS_ee_1j_minus=datacards{0}/hww2l2v_13TeV_WH_SS_ee_1j_minus_pt2ge20/BDTG6_TT_0_5/datacard.txt \
                                   WH_SS_ee_1j_plus=datacards{0}/hww2l2v_13TeV_WH_SS_ee_1j_plus_pt2ge20/BDTG6_TT_0_5/datacard.txt \
                                   WH_SS_em_2j_minus_low_pt=datacards{0}/hww2l2v_13TeV_WH_SS_em_2j_minus_pt2lt20/BDTG6_TT_0_0/datacard.txt \
                                   WH_SS_em_2j_plus_low_pt=datacards{0}/hww2l2v_13TeV_WH_SS_em_2j_plus_pt2lt20/BDTG6_TT_0_0/datacard.txt \
                                   WH_SS_mm_2j_minus_low_pt=datacards{0}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_minus_pt2lt20/BDTG6_TT_0_0/datacard.txt \
                                   WH_SS_mm_2j_plus_low_pt=datacards{0}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_plus_pt2lt20/BDTG6_TT_0_0/datacard.txt \
                                   WH_SS_ee_2j_minus_low_pt=datacards{0}/hww2l2v_13TeV_WH_SS_ee_2j_minus_pt2lt20/BDTG6_TT_0_0/datacard.txt \
                                   WH_SS_ee_2j_plus_low_pt=datacards{0}/hww2l2v_13TeV_WH_SS_ee_2j_plus_pt2lt20/BDTG6_TT_0_0/datacard.txt \
                                   WH_SS_em_1j_minus_low_pt=datacards{0}/hww2l2v_13TeV_WH_SS_em_1j_minus_pt2lt20/BDTG6_TT_0_5/datacard.txt \
                                   WH_SS_em_1j_plus_low_pt=datacards{0}/hww2l2v_13TeV_WH_SS_em_1j_plus_pt2lt20/BDTG6_TT_0_5/datacard.txt \
                                   WH_SS_mm_1j_minus_low_pt=datacards{0}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_minus_pt2lt20/BDTG6_TT_0_5/datacard.txt \
                                   WH_SS_mm_1j_plus_low_pt=datacards{0}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_plus_pt2lt20/BDTG6_TT_0_5/datacard.txt \
                                   WH_SS_ee_1j_minus_low_pt=datacards{0}/hww2l2v_13TeV_WH_SS_ee_1j_minus_pt2lt20/BDTG6_TT_0_0/datacard.txt \
                                   WH_SS_ee_1j_plus_low_pt=datacards{0}/hww2l2v_13TeV_WH_SS_ee_1j_plus_pt2lt20/BDTG6_TT_0_0/datacard.txt \
                                   WH_SS_WZ_1j=../WH3l/datacards{0}/hww2l2v_13TeV_WH_SS_WZ_1j/events/datacard.txt \
                                   WH_SS_WZ_2j=../WH3l/datacards{0}/hww2l2v_13TeV_WH_SS_WZ_2j/events/datacard.txt \
                                   WH_SS_mm_2j_SS_CR_minus=datacards{0}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_SS_CR_minus_pt2ge20/events/datacard.txt \
                                   WH_SS_mm_2j_SS_CR_plus=datacards{0}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_SS_CR_plus_pt2ge20/events/datacard.txt \
                                   WH_SS_em_2j_SS_CR_minus=datacards{0}/hww2l2v_13TeV_WH_SS_em_2j_SS_CR_minus_pt2ge20/events/datacard.txt \
                                   WH_SS_em_2j_SS_CR_plus=datacards{0}/hww2l2v_13TeV_WH_SS_em_2j_SS_CR_plus_pt2ge20/events/datacard.txt \
                                   WH_SS_ee_2j_SS_CR_minus=datacards{0}/hww2l2v_13TeV_WH_SS_ee_2j_SS_CR_minus_pt2ge20/events/datacard.txt \
                                   WH_SS_ee_2j_SS_CR_plus=datacards{0}/hww2l2v_13TeV_WH_SS_ee_2j_SS_CR_plus_pt2ge20/events/datacard.txt \
                                   WH_SS_mm_1j_SS_CR_minus=datacards{0}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_SS_CR_minus_pt2ge20/events/datacard.txt \
                                   WH_SS_mm_1j_SS_CR_plus=datacards{0}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_SS_CR_plus_pt2ge20/events/datacard.txt \
                                   WH_SS_em_1j_SS_CR_minus=datacards{0}/hww2l2v_13TeV_WH_SS_em_1j_SS_CR_minus_pt2ge20/events/datacard.txt \
                                   WH_SS_em_1j_SS_CR_plus=datacards{0}/hww2l2v_13TeV_WH_SS_em_1j_SS_CR_plus_pt2ge20/events/datacard.txt \
                                   WH_SS_ee_1j_SS_CR_minus=datacards{0}/hww2l2v_13TeV_WH_SS_ee_1j_SS_CR_minus_pt2ge20/events/datacard.txt \
                                   WH_SS_ee_1j_SS_CR_plus=datacards{0}/hww2l2v_13TeV_WH_SS_ee_1j_SS_CR_plus_pt2ge20/events/datacard.txt \
                     		   > Combination/WH_chargeAsymmetry_WH_SS_2016HIPM_v9_SS_CR.txt".format(suff)
    print(tmp_command)
    print()
    print()
    os.system(tmp_command)
    
# WH_SS_ee_2j_SS_CR_minus_low_pt=datacards{0}/hww2l2v_13TeV_WH_SS_ee_2j_SS_CR_minus_pt2lt20/events/datacard.txt \
# WH_SS_ee_2j_SS_CR_plus_low_pt=datacards{0}/hww2l2v_13TeV_WH_SS_ee_2j_SS_CR_plus_pt2lt20/events/datacard.txt \
# WH_SS_mm_2j_SS_CR_minus_low_pt=datacards{0}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_SS_CR_minus_pt2lt20/events/datacard.txt \
# WH_SS_mm_2j_SS_CR_plus_low_pt=datacards{0}/hww2l2v_13TeV_WH_SS_noZveto_mm_2j_SS_CR_plus_pt2lt20/events/datacard.txt \
# WH_SS_em_2j_SS_CR_minus_low_pt=datacards{0}/hww2l2v_13TeV_WH_SS_em_2j_SS_CR_minus_pt2lt20/events/datacard.txt \
# WH_SS_em_2j_SS_CR_plus_low_pt=datacards{0}/hww2l2v_13TeV_WH_SS_em_2j_SS_CR_plus_pt2lt20/events/datacard.txt \
                
# WH_SS_ee_1j_SS_CR_minus_low_pt=datacards{0}/hww2l2v_13TeV_WH_SS_ee_1j_SS_CR_minus_pt2lt20/events/datacard.txt \
# WH_SS_ee_1j_SS_CR_plus_low_pt=datacards{0}/hww2l2v_13TeV_WH_SS_ee_1j_SS_CR_plus_pt2lt20/events/datacard.txt \
# WH_SS_mm_1j_SS_CR_minus_low_pt=datacards{0}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_SS_CR_minus_pt2lt20/events/datacard.txt \
# WH_SS_mm_1j_SS_CR_plus_low_pt=datacards{0}/hww2l2v_13TeV_WH_SS_noZveto_mm_1j_SS_CR_plus_pt2lt20/events/datacard.txt \
# WH_SS_em_1j_SS_CR_minus_low_pt=datacards{0}/hww2l2v_13TeV_WH_SS_em_1j_SS_CR_minus_pt2lt20/events/datacard.txt \
# WH_SS_em_1j_SS_CR_plus_low_pt=datacards{0}/hww2l2v_13TeV_WH_SS_em_1j_SS_CR_plus_pt2lt20/events/datacard.txt \                
