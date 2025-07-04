cd ../scripts/

if [[ "$(uname -a)" == *portal* ]] || [[ "$(uname -a)" == *bms* ]]; then
    echo "We are at KIT!"
    input_dir=/ceph/${USER}
else
    echo "We are on lxplus!"
    input_dir=/eos/user/${USER}/${USER:0:1}
fi

# Muons
python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFolder ../Full2018_v9/fakerate/cut_Tight_HWWW_tthmva_82 --outputFileName MuonFR_45.root --jet_pt 45 --flavor muon --variable pt2_eta2 --do_prompt_rate True --outputFileNamePR MuonPR.root

python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFolder ../Full2018_v9/fakerate/cut_Tight_HWWW_tthmva_82 --outputFileName MuonFR_jet10.root --jet_pt 10 --flavor muon --variable pt1_eta1
python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFolder ../Full2018_v9/fakerate/cut_Tight_HWWW_tthmva_82 --outputFileName MuonFR_jet15.root --jet_pt 15 --flavor muon --variable pt1_eta1
python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFolder ../Full2018_v9/fakerate/cut_Tight_HWWW_tthmva_82 --outputFileName MuonFR_jet20.root --jet_pt 20 --flavor muon --variable pt1_eta1
python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFolder ../Full2018_v9/fakerate/cut_Tight_HWWW_tthmva_82 --outputFileName MuonFR_jet25.root --jet_pt 25 --flavor muon --variable pt1_eta1
python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFolder ../Full2018_v9/fakerate/cut_Tight_HWWW_tthmva_82 --outputFileName MuonFR_jet30.root --jet_pt 30 --flavor muon --variable pt1_eta1
python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFolder ../Full2018_v9/fakerate/cut_Tight_HWWW_tthmva_82 --outputFileName MuonFR_jet35.root --jet_pt 35 --flavor muon --variable pt1_eta1
python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFolder ../Full2018_v9/fakerate/cut_Tight_HWWW_tthmva_82 --outputFileName MuonFR_jet40.root --jet_pt 40 --flavor muon --variable pt1_eta1
python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFolder ../Full2018_v9/fakerate/cut_Tight_HWWW_tthmva_82 --outputFileName MuonFR_jet45.root --jet_pt 45 --flavor muon --variable pt1_eta1

# Electrons
python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFolder ../Full2018_v9/fakerate/mvaFall17V2Iso_WP90_tthmva_UL_90 --outputFileName EleFR_45.root --jet_pt 45 --flavor ele --variable pt2_eta2 --do_prompt_rate True --outputFileNamePR ElePR.root

python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFolder ../Full2018_v9/fakerate/mvaFall17V2Iso_WP90_tthmva_UL_90 --outputFileName EleFR_jet10.root --jet_pt 10 --flavor ele --variable pt1_eta1
python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFolder ../Full2018_v9/fakerate/mvaFall17V2Iso_WP90_tthmva_UL_90 --outputFileName EleFR_jet15.root --jet_pt 15 --flavor ele --variable pt1_eta1
python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFolder ../Full2018_v9/fakerate/mvaFall17V2Iso_WP90_tthmva_UL_90 --outputFileName EleFR_jet25.root --jet_pt 25 --flavor ele --variable pt1_eta1
python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFolder ../Full2018_v9/fakerate/mvaFall17V2Iso_WP90_tthmva_UL_90 --outputFileName EleFR_jet30.root --jet_pt 30 --flavor ele --variable pt1_eta1
python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFolder ../Full2018_v9/fakerate/mvaFall17V2Iso_WP90_tthmva_UL_90 --outputFileName EleFR_jet35.root --jet_pt 35 --flavor ele --variable pt1_eta1
python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFolder ../Full2018_v9/fakerate/mvaFall17V2Iso_WP90_tthmva_UL_90 --outputFileName EleFR_jet40.root --jet_pt 40 --flavor ele --variable pt1_eta1
python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFolder ../Full2018_v9/fakerate/mvaFall17V2Iso_WP90_tthmva_UL_90 --outputFileName EleFR_jet45.root --jet_pt 45 --flavor ele --variable pt1_eta1

cd -
