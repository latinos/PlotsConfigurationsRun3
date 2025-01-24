cd ../scripts/

# Muons
python mkFakeRate.py --inputFile /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFile ../Full2018_v9/MuonFR_45.root --jet_pt 45 --flavor muon --variable pt2_eta2 --do_prompt_rate True --outputFilePR ../Full2018_v9/MuonPR.root

python mkFakeRate.py --inputFile /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFile ../Full2018_v9/MuonFR_jet10.root --jet_pt 10 --flavor muon --variable pt1_eta1
python mkFakeRate.py --inputFile /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFile ../Full2018_v9/MuonFR_jet15.root --jet_pt 15 --flavor muon --variable pt1_eta1
python mkFakeRate.py --inputFile /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFile ../Full2018_v9/MuonFR_jet20.root --jet_pt 20 --flavor muon --variable pt1_eta1
python mkFakeRate.py --inputFile /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFile ../Full2018_v9/MuonFR_jet25.root --jet_pt 25 --flavor muon --variable pt1_eta1
python mkFakeRate.py --inputFile /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFile ../Full2018_v9/MuonFR_jet30.root --jet_pt 30 --flavor muon --variable pt1_eta1
python mkFakeRate.py --inputFile /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFile ../Full2018_v9/MuonFR_jet35.root --jet_pt 35 --flavor muon --variable pt1_eta1
python mkFakeRate.py --inputFile /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFile ../Full2018_v9/MuonFR_jet40.root --jet_pt 40 --flavor muon --variable pt1_eta1
python mkFakeRate.py --inputFile /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFile ../Full2018_v9/MuonFR_jet45.root --jet_pt 45 --flavor muon --variable pt1_eta1

# Electrons
python mkFakeRate.py --inputFile /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFile ../Full2018_v9/EleFR_45.root --jet_pt 45 --flavor ele --variable pt2_eta2 --do_prompt_rate True --outputFilePR ../Full2018_v9/ElePR.root

python mkFakeRate.py --inputFile /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFile ../Full2018_v9/EleFR_jet10.root --jet_pt 10 --flavor ele --variable pt1_eta1
python mkFakeRate.py --inputFile /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFile ../Full2018_v9/EleFR_jet15.root --jet_pt 15 --flavor ele --variable pt1_eta1
python mkFakeRate.py --inputFile /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFile ../Full2018_v9/EleFR_jet25.root --jet_pt 25 --flavor ele --variable pt1_eta1
python mkFakeRate.py --inputFile /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFile ../Full2018_v9/EleFR_jet30.root --jet_pt 30 --flavor ele --variable pt1_eta1
python mkFakeRate.py --inputFile /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFile ../Full2018_v9/EleFR_jet35.root --jet_pt 35 --flavor ele --variable pt1_eta1
python mkFakeRate.py --inputFile /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFile ../Full2018_v9/EleFR_jet40.root --jet_pt 40 --flavor ele --variable pt1_eta1
python mkFakeRate.py --inputFile /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/Fake_Full2018_v9/rootFile/mkShapes__Fake_Full2018_v9.root --outputFile ../Full2018_v9/EleFR_jet45.root --jet_pt 45 --flavor ele --variable pt1_eta1

cd -
