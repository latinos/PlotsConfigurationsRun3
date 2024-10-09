cd ../scripts/

# Muons
python mkFakeRate.py --inputFile /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFile ../Full2018_v9/MuonFR_20.root --jet_pt 20 --flavor muon --variable pt1_eta1
python mkFakeRate.py --inputFile /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFile ../Full2018_v9/MuonFR_25.root --jet_pt 25 --flavor muon --variable pt1_eta1
python mkFakeRate.py --inputFile /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFile ../Full2018_v9/MuonFR_30.root --jet_pt 30 --flavor muon --variable pt1_eta1
python mkFakeRate.py --inputFile /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFile ../Full2018_v9/MuonFR_35.root --jet_pt 35 --flavor muon --variable pt1_eta1
python mkFakeRate.py --inputFile /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFile ../Full2018_v9/MuonFR_40.root --jet_pt 40 --flavor muon --variable pt1_eta1
python mkFakeRate.py --inputFile /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFile ../Full2018_v9/MuonFR_45.root --jet_pt 45 --flavor muon --variable pt1_eta1 --do_prompt_rate True --outputFilePR ../Full2018_v9/MuonPR.root

# Electrons
python mkFakeRate.py --inputFile /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFile ../Full2018_v9/EleFR_20.root --jet_pt 20 --flavor ele --variable pt1_eta1
python mkFakeRate.py --inputFile /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFile ../Full2018_v9/EleFR_25.root --jet_pt 25 --flavor ele --variable pt1_eta1
python mkFakeRate.py --inputFile /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFile ../Full2018_v9/EleFR_30.root --jet_pt 30 --flavor ele --variable pt1_eta1
python mkFakeRate.py --inputFile /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFile ../Full2018_v9/EleFR_35.root --jet_pt 35 --flavor ele --variable pt1_eta1
python mkFakeRate.py --inputFile /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFile ../Full2018_v9/EleFR_40.root --jet_pt 40 --flavor ele --variable pt1_eta1
python mkFakeRate.py --inputFile /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFile ../Full2018_v9/EleFR_45.root --jet_pt 45 --flavor ele --variable pt1_eta1 --do_prompt_rate True --outputFilePR ../Full2018_v9/ElectronPR.root

cd -
