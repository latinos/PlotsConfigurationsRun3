if [[ "$(uname -a)" == *portal* ]] || [[ "$(uname -a)" == *bms* ]]; then
    echo "We are at KIT!"
    input_dir=/ceph/${USER}
else
    echo "We are on lxplus!"
    input_dir=/eos/user/${USER:0:1}/${USER}
fi


cd ../scripts/


MUON_ID=cut_TightID_pfIsoTight_HWW_tthmva_67
ELE_ID=cutBased_LooseID_tthMVA_Run3


### Cone pT

# Muons
python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/2024v15_${ELE_ID}__mu_${MUON_ID}/rootFile/mkShapes__2024v15_${ELE_ID}__mu_${MUON_ID}.root --outputFolder ../2024_v15/FakeRate_cone_pt/2024_v15_conept/${MUON_ID} --outputFileName MuonFR_jet30.root --jet_pt 30 --flavor muon --variable conept2_eta2 --do_prompt_rate True --outputFileNamePR MuonPR.root

python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/2024v15_${ELE_ID}__mu_${MUON_ID}/rootFile/mkShapes__2024v15_${ELE_ID}__mu_${MUON_ID}.root --outputFolder ../2024_v15/FakeRate_cone_pt/2024_v15_conept/${MUON_ID} --outputFileName MuonFR_jet20.root --jet_pt 20 --flavor muon --variable conept1_eta1
python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/2024v15_${ELE_ID}__mu_${MUON_ID}/rootFile/mkShapes__2024v15_${ELE_ID}__mu_${MUON_ID}.root --outputFolder ../2024_v15/FakeRate_cone_pt/2024_v15_conept/${MUON_ID} --outputFileName MuonFR_jet30.root --jet_pt 30 --flavor muon --variable conept1_eta1
python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/2024v15_${ELE_ID}__mu_${MUON_ID}/rootFile/mkShapes__2024v15_${ELE_ID}__mu_${MUON_ID}.root --outputFolder ../2024_v15/FakeRate_cone_pt/2024_v15_conept/${MUON_ID} --outputFileName MuonFR_jet40.root --jet_pt 40 --flavor muon --variable conept1_eta1


# Electrons
python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/2024v15_${ELE_ID}__mu_${MUON_ID}/rootFile/mkShapes__2024v15_${ELE_ID}__mu_${MUON_ID}.root --outputFolder ../2024_v15/FakeRate_cone_pt/2024_v15_conept/${ELE_ID} --outputFileName EleFR_jet30.root --jet_pt 30 --flavor ele --variable conept2_eta2 --do_prompt_rate True --outputFileNamePR ElePR.root

python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/2024v15_${ELE_ID}__mu_${MUON_ID}/rootFile/mkShapes__2024v15_${ELE_ID}__mu_${MUON_ID}.root --outputFolder ../2024_v15/FakeRate_cone_pt/2024_v15_conept/${ELE_ID} --outputFileName EleFR_jet20.root --jet_pt 20 --flavor ele --variable conept1_eta1
python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/2024v15_${ELE_ID}__mu_${MUON_ID}/rootFile/mkShapes__2024v15_${ELE_ID}__mu_${MUON_ID}.root --outputFolder ../2024_v15/FakeRate_cone_pt/2024_v15_conept/${ELE_ID} --outputFileName EleFR_jet30.root --jet_pt 30 --flavor ele --variable conept1_eta1
python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/2024v15_${ELE_ID}__mu_${MUON_ID}/rootFile/mkShapes__2024v15_${ELE_ID}__mu_${MUON_ID}.root --outputFolder ../2024_v15/FakeRate_cone_pt/2024_v15_conept/${ELE_ID} --outputFileName EleFR_jet40.root --jet_pt 40 --flavor ele --variable conept1_eta1


### Lepton pT

# Muons
python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/2024v15_${ELE_ID}__mu_${MUON_ID}/rootFile/mkShapes__2024v15_${ELE_ID}__mu_${MUON_ID}.root --outputFolder ../2024_v15/FakeRate_pt/2024_v15_pt/${MUON_ID} --outputFileName MuonFR_jet30.root --jet_pt 30 --flavor muon --variable pt2_eta2 --do_prompt_rate True --outputFileNamePR MuonPR.root

python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/2024v15_${ELE_ID}__mu_${MUON_ID}/rootFile/mkShapes__2024v15_${ELE_ID}__mu_${MUON_ID}.root --outputFolder ../2024_v15/FakeRate_pt/2024_v15_pt/${MUON_ID} --outputFileName MuonFR_jet20.root --jet_pt 20 --flavor muon --variable pt1_eta1
python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/2024v15_${ELE_ID}__mu_${MUON_ID}/rootFile/mkShapes__2024v15_${ELE_ID}__mu_${MUON_ID}.root --outputFolder ../2024_v15/FakeRate_pt/2024_v15_pt/${MUON_ID} --outputFileName MuonFR_jet30.root --jet_pt 30 --flavor muon --variable pt1_eta1
python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/2024v15_${ELE_ID}__mu_${MUON_ID}/rootFile/mkShapes__2024v15_${ELE_ID}__mu_${MUON_ID}.root --outputFolder ../2024_v15/FakeRate_pt/2024_v15_pt/${MUON_ID} --outputFileName MuonFR_jet40.root --jet_pt 40 --flavor muon --variable pt1_eta1


# Electrons
python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/2024v15_${ELE_ID}__mu_${MUON_ID}/rootFile/mkShapes__2024v15_${ELE_ID}__mu_${MUON_ID}.root --outputFolder ../2024_v15/FakeRate_pt/2024_v15_pt/${ELE_ID} --outputFileName EleFR_jet30.root --jet_pt 30 --flavor ele --variable pt2_eta2 --do_prompt_rate True --outputFileNamePR ElePR.root

python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/2024v15_${ELE_ID}__mu_${MUON_ID}/rootFile/mkShapes__2024v15_${ELE_ID}__mu_${MUON_ID}.root --outputFolder ../2024_v15/FakeRate_pt/2024_v15_pt/${ELE_ID} --outputFileName EleFR_jet20.root --jet_pt 20 --flavor ele --variable pt1_eta1
python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/2024v15_${ELE_ID}__mu_${MUON_ID}/rootFile/mkShapes__2024v15_${ELE_ID}__mu_${MUON_ID}.root --outputFolder ../2024_v15/FakeRate_pt/2024_v15_pt/${ELE_ID} --outputFileName EleFR_jet30.root --jet_pt 30 --flavor ele --variable pt1_eta1
python mkFakeRate.py --inputFile ${input_dir}/mkShapesRDF_rootfiles/2024v15_${ELE_ID}__mu_${MUON_ID}/rootFile/mkShapes__2024v15_${ELE_ID}__mu_${MUON_ID}.root --outputFolder ../2024_v15/FakeRate_pt/2024_v15_pt/${ELE_ID} --outputFileName EleFR_jet40.root --jet_pt 40 --flavor ele --variable pt1_eta1

cd -
