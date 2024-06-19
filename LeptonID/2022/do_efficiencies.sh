CUTS=(
	"sr_ele_wp90iso_mu_cut_TightID_POG_ee_high_"
	"sr_ele_wp90iso_mu_cut_TightID_POG_ee_low_"
	"sr_ele_wp90iso_mu_cut_TightID_POG_em_high_"
	"sr_ele_wp90iso_mu_cut_TightID_POG_em_low_"
	"sr_ele_wp90iso_mu_cut_TightID_POG_mm_high_"
	"sr_ele_wp90iso_mu_cut_TightID_POG_mm_low_"
	"sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightID_POG_ee_high_"
	"sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightID_POG_ee_low_"
	"sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightID_POG_em_high_"
	"sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightID_POG_em_low_"
	"sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightID_POG_mm_high_"
	"sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightID_POG_mm_low_"
	"sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightMiniIso_HWW_ee_high_"
	"sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightMiniIso_HWW_ee_low_"
	"sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightMiniIso_HWW_em_high_"
	"sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightMiniIso_HWW_em_low_"
	"sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightMiniIso_HWW_mm_high_"
	"sr_ele_mvaWinter22V2Iso_WP90_mu_cut_TightMiniIso_HWW_mm_low_"
)

PRESELS=(
	"basic_selections_ee_high_"
	"basic_selections_ee_low_"
	"basic_selections_em_high_"
	"basic_selections_em_low_"
	"basic_selections_mm_high_"
	"basic_selections_mm_low_"
	"basic_selections_ee_high_"
	"basic_selections_ee_low_"
	"basic_selections_em_high_"
	"basic_selections_em_low_"
	"basic_selections_mm_high_"
	"basic_selections_mm_low_"
	"basic_selections_ee_high_"
	"basic_selections_ee_low_"
	"basic_selections_em_high_"
	"basic_selections_em_low_"
	"basic_selections_mm_high_"
	"basic_selections_mm_low_"
)

rm eff_plots/efficiencies.csv
echo "signals ; backgrounds ; cut ; sig_eff ; bkg_eff" > eff_plots/efficiencies.csv

for ((idx=0; idx<${#CUTS[@]}; ++idx)); do

echo ${CUTS[$idx]}
cd ../scripts/
python mkEff.py --inputFile ../2022/rootFile/mkShapes__LeptonID_2022.root \
	   --signals ggH_hww \
	   --backgrounds WJets \
	   --cut ${CUTS[$idx]} \
	   --presel ${PRESELS[$idx]} \
	   --year 2022 \
	   --variable pt1 \
	   --outputDir ../2022/eff_plots/

python mkEff.py --inputFile ../2022/rootFile/mkShapes__LeptonID_2022.root \
	   --signals WW \
	   --backgrounds WJets \
	   --cut ${CUTS[$idx]} \
	   --presel ${PRESELS[$idx]} \
	   --year 2022 \
	   --variable pt1 \
	   --outputDir ../2022/eff_plots/

python mkEff.py --inputFile ../2022/rootFile/mkShapes__LeptonID_2022.root \
	   --signals ggH_hww \
	   --backgrounds TTToSemiLeptonic \
	   --cut ${CUTS[$idx]} \
	   --presel ${PRESELS[$idx]} \
	   --year 2022 \
	   --variable pt1 \
	   --outputDir ../2022/eff_plots/

python mkEff.py --inputFile ../2022/rootFile/mkShapes__LeptonID_2022.root \
	   --signals WW \
	   --backgrounds TTToSemiLeptonic \
	   --cut ${CUTS[$idx]} \
	   --presel ${PRESELS[$idx]} \
	   --year 2022 \
	   --variable pt1 \
	   --outputDir ../2022/eff_plots/
cd -
