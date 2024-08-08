

### 2018

pushd ./datacards_2018

echo $PWD

combineCards.py hww2l2v_13TeV_sr_RF_Signal_0j_pt2gt20/RF_0J_TT/datacard.txt hww2l2v_13TeV_sr_RF_Signal_0j_pt2lt20/RF_0J_TT/datacard.txt hww2l2v_13TeV_top_0j/events/datacard.txt hww2l2v_13TeV_dytt_0j/events/datacard.txt hww2l2v_13TeV_sr_RF_bkg_0j/events/datacard.txt hww2l2v_13TeV_ss_0j/events/datacard.txt > datacard_combined_0j.txt

combineCards.py hww2l2v_13TeV_sr_RF_Signal_1j_pt2gt20/RF_1J_TT/datacard.txt hww2l2v_13TeV_sr_RF_Signal_1j_pt2lt20/RF_1J_TT/datacard.txt hww2l2v_13TeV_top_1j/events/datacard.txt hww2l2v_13TeV_dytt_1j/events/datacard.txt hww2l2v_13TeV_sr_RF_bkg_1j/events/datacard.txt hww2l2v_13TeV_ss_1j/events/datacard.txt > datacard_combined_1j.txt

combineCards.py hww2l2v_13TeV_sr_RF_Signal_2j/RF_2J_LL/datacard.txt hww2l2v_13TeV_top_2j/events/datacard.txt hww2l2v_13TeV_dytt_2j/events/datacard.txt hww2l2v_13TeV_sr_RF_bkg_2j/events/datacard.txt hww2l2v_13TeV_ss_2j/events/datacard.txt > datacard_combined_2j.txt

combineCards.py hww2l2v_13TeV_sr_RF_Signal_2j_vbf/RF_VBF_LL/datacard.txt hww2l2v_13TeV_sr_RF_bkg_2j_vbf/events/datacard.txt > datacard_combined_2j_vbf.txt

combineCards.py datacard_combined_0j.txt datacard_combined_1j.txt datacard_combined_2j.txt datacard_combined_2j_vbf.txt > datacard_combined.txt

popd


### 2017


pushd ./datacards_2017

echo $PWD

combineCards.py hww2l2v_13TeV_sr_RF_Signal_0j_pt2gt20/RF_0J_TT/datacard.txt hww2l2v_13TeV_sr_RF_Signal_0j_pt2lt20/RF_0J_TT/datacard.txt hww2l2v_13TeV_top_0j/events/datacard.txt hww2l2v_13TeV_dytt_0j/events/datacard.txt hww2l2v_13TeV_sr_RF_bkg_0j/events/datacard.txt hww2l2v_13TeV_ss_0j/events/datacard.txt > datacard_combined_0j.txt

combineCards.py hww2l2v_13TeV_sr_RF_Signal_1j_pt2gt20/RF_1J_TT/datacard.txt hww2l2v_13TeV_sr_RF_Signal_1j_pt2lt20/RF_1J_TT/datacard.txt hww2l2v_13TeV_top_1j/events/datacard.txt hww2l2v_13TeV_dytt_1j/events/datacard.txt hww2l2v_13TeV_sr_RF_bkg_1j/events/datacard.txt hww2l2v_13TeV_ss_1j/events/datacard.txt > datacard_combined_1j.txt

combineCards.py hww2l2v_13TeV_sr_RF_Signal_2j/RF_2J_LL/datacard.txt hww2l2v_13TeV_top_2j/events/datacard.txt hww2l2v_13TeV_dytt_2j/events/datacard.txt hww2l2v_13TeV_sr_RF_bkg_2j/events/datacard.txt hww2l2v_13TeV_ss_2j/events/datacard.txt > datacard_combined_2j.txt

combineCards.py hww2l2v_13TeV_sr_RF_Signal_2j_vbf/RF_VBF_LL/datacard.txt hww2l2v_13TeV_sr_RF_bkg_2j_vbf/events/datacard.txt > datacard_combined_2j_vbf.txt

combineCards.py datacard_combined_0j.txt datacard_combined_1j.txt datacard_combined_2j.txt datacard_combined_2j_vbf.txt > datacard_combined.txt

popd

### 2016 HIPM

pushd ./datacards_2016_HIPM

echo $PWD

combineCards.py hww2l2v_13TeV_sr_RF_Signal_0j_pt2gt20/RF_0J_TT/datacard.txt hww2l2v_13TeV_sr_RF_Signal_0j_pt2lt20/RF_0J_TT/datacard.txt hww2l2v_13TeV_top_0j/events/datacard.txt hww2l2v_13TeV_dytt_0j/events/datacard.txt hww2l2v_13TeV_sr_RF_bkg_0j/events/datacard.txt hww2l2v_13TeV_ss_0j/events/datacard.txt > datacard_combined_0j.txt

combineCards.py hww2l2v_13TeV_sr_RF_Signal_1j_pt2gt20/RF_1J_TT/datacard.txt hww2l2v_13TeV_sr_RF_Signal_1j_pt2lt20/RF_1J_TT/datacard.txt hww2l2v_13TeV_top_1j/events/datacard.txt hww2l2v_13TeV_dytt_1j/events/datacard.txt hww2l2v_13TeV_sr_RF_bkg_1j/events/datacard.txt hww2l2v_13TeV_ss_1j/events/datacard.txt > datacard_combined_1j.txt

combineCards.py hww2l2v_13TeV_sr_RF_Signal_2j/RF_2J_LL/datacard.txt hww2l2v_13TeV_top_2j/events/datacard.txt hww2l2v_13TeV_dytt_2j/events/datacard.txt hww2l2v_13TeV_sr_RF_bkg_2j/events/datacard.txt hww2l2v_13TeV_ss_2j/events/datacard.txt > datacard_combined_2j.txt

combineCards.py hww2l2v_13TeV_sr_RF_Signal_2j_vbf/RF_VBF_LL/datacard.txt hww2l2v_13TeV_sr_RF_bkg_2j_vbf/events/datacard.txt > datacard_combined_2j_vbf.txt

combineCards.py datacard_combined_0j.txt datacard_combined_1j.txt datacard_combined_2j.txt datacard_combined_2j_vbf.txt > datacard_combined.txt

popd

### 2016 noHIPM

pushd ./datacards_2016_noHIPM

echo $PWD

combineCards.py hww2l2v_13TeV_sr_RF_Signal_0j_pt2gt20/RF_0J_TT/datacard.txt hww2l2v_13TeV_sr_RF_Signal_0j_pt2lt20/RF_0J_TT/datacard.txt hww2l2v_13TeV_top_0j/events/datacard.txt hww2l2v_13TeV_dytt_0j/events/datacard.txt hww2l2v_13TeV_sr_RF_bkg_0j/events/datacard.txt hww2l2v_13TeV_ss_0j/events/datacard.txt > datacard_combined_0j.txt

combineCards.py hww2l2v_13TeV_sr_RF_Signal_1j_pt2gt20/RF_1J_TT/datacard.txt hww2l2v_13TeV_sr_RF_Signal_1j_pt2lt20/RF_1J_TT/datacard.txt hww2l2v_13TeV_top_1j/events/datacard.txt hww2l2v_13TeV_dytt_1j/events/datacard.txt hww2l2v_13TeV_sr_RF_bkg_1j/events/datacard.txt hww2l2v_13TeV_ss_1j/events/datacard.txt > datacard_combined_1j.txt

combineCards.py hww2l2v_13TeV_sr_RF_Signal_2j/RF_2J_LL/datacard.txt hww2l2v_13TeV_top_2j/events/datacard.txt hww2l2v_13TeV_dytt_2j/events/datacard.txt hww2l2v_13TeV_sr_RF_bkg_2j/events/datacard.txt hww2l2v_13TeV_ss_2j/events/datacard.txt > datacard_combined_2j.txt

combineCards.py hww2l2v_13TeV_sr_RF_Signal_2j_vbf/RF_VBF_LL/datacard.txt hww2l2v_13TeV_sr_RF_bkg_2j_vbf/events/datacard.txt > datacard_combined_2j_vbf.txt

combineCards.py datacard_combined_0j.txt datacard_combined_1j.txt datacard_combined_2j.txt datacard_combined_2j_vbf.txt > datacard_combined.txt

popd


#### Combine

combineCards.py datacards_2018/datacard_combined.txt datacards_2017/datacard_combined.txt datacards_2016_HIPM/datacard_combined.txt datacards_2016_noHIPM/datacard_combined.txt > datacard_combined.txt

text2workspace.py datacard_combined.txt -m 125 -P HiggsAnalysis.CombinedLimit.HiggsHelicity:higgshelicity --PO doOnlyPolarization -o datacard_combined.root
