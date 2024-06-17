# CUTS=(
# 	sr_ele_wp90iso_mu_cut_TightID_POG_ee_high_pt \
# 	sr_ele_wp90iso_mu_cut_TightID_POG_ee_low_pt \
# 	sr_ele_wp90iso_mu_cut_TightID_POG_em_high_pt \
# 	sr_ele_wp90iso_mu_cut_TightID_POG_em_low_pt \
# 	sr_ele_wp90iso_mu_cut_TightID_POG_mm_high_pt \
# 	sr_ele_wp90iso_mu_cut_TightID_POG_mm_low_pt \
# 	sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightID_POG_ee_high_pt \
# 	sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightID_POG_ee_low_pt \
# 	sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightID_POG_em_high_pt \
# 	sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightID_POG_em_low_pt \
# 	sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightID_POG_mm_high_pt \
# 	sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightID_POG_mm_low_pt \
# 	sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightMiniIso_HWW_ee_high_pt \
# 	sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightMiniIso_HWW_ee_low_pt \
# 	sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightMiniIso_HWW_em_high_pt \
# 	sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightMiniIso_HWW_em_low_pt \
# 	sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightMiniIso_HWW_mm_high_pt \
# 	sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightMiniIso_HWW_mm_low_pt \
# )

CUT=sr_ele_wp90iso_mu_cut_TightID_POG_ee_high_pt,sr_ele_wp90iso_mu_cut_TightID_POG_ee_low_pt,sr_ele_wp90iso_mu_cut_TightID_POG_em_high_pt,sr_ele_wp90iso_mu_cut_TightID_POG_em_low_pt,sr_ele_wp90iso_mu_cut_TightID_POG_mm_high_pt,sr_ele_wp90iso_mu_cut_TightID_POG_mm_low_pt,sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightID_POG_ee_high_pt,sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightID_POG_ee_low_pt,sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightID_POG_em_high_pt,sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightID_POG_em_low_pt,sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightID_POG_mm_high_pt,sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightID_POG_mm_low_pt,sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightMiniIso_HWW_ee_high_pt,sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightMiniIso_HWW_ee_low_pt,sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightMiniIso_HWW_em_high_pt,sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightMiniIso_HWW_em_low_pt,sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightMiniIso_HWW_mm_high_pt,sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightMiniIso_HWW_mm_low_pt

rm eff_plots/efficiencies.csv
echo "signals ; backgrounds ; cut ; sig_eff ; bkg_eff" > eff_plots/efficiencies.csv

echo $CUT
cd ../scripts/
python mkEff.py --inputFile ../2022/rootFile/mkShapes__LeptonID_2022.root \
	   --signals ggH_hww \
	   --backgrounds WJets \
	   --cut $CUT \
	   --year 2022 \
	   --variable pt1 \
	   --outputDir ../2022/eff_plots/

python mkEff.py --inputFile ../2022/rootFile/mkShapes__LeptonID_2022.root \
	   --signals WW \
	   --backgrounds WJets \
	   --cut $CUT \
	   --year 2022 \
	   --variable pt1 \
	   --outputDir ../2022/eff_plots/

python mkEff.py --inputFile ../2022/rootFile/mkShapes__LeptonID_2022.root \
	   --signals ggH_hww \
	   --backgrounds TTToSemiLeptonic \
	   --cut $CUT \
	   --year 2022 \
	   --variable pt1 \
	   --outputDir ../2022/eff_plots/

python mkEff.py --inputFile ../2022/rootFile/mkShapes__LeptonID_2022.root \
	   --signals WW \
	   --backgrounds TTToSemiLeptonic \
	   --cut $CUT \
	   --year 2022 \
	   --variable pt1 \
	   --outputDir ../2022/eff_plots/
cd -
