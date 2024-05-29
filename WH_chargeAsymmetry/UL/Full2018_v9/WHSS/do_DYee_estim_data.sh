#!/bin/bash

cd ../../scripts/

python mkDYee_chargeFlip_OS_SS_data.py \
    --os_ss_cutsFile /afs/cern.ch/user/n/ntrevisa/work/latinos/Run3/PlotsConfigurationsRun3/WH_chargeAsymmetry/UL/Full2018_v9/WHSS/dict_os_ss_cuts.py \
    --inputFileSS    /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/WHSS_2018_v9_chargeAsymmetry_Mu82_EleUL90/rootFile/mkShapes__WHSS_2018_v9_chargeAsymmetry_Mu82_EleUL90.root \
    --inputFileOS    /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/WHSS_OSCR_2018_v9_chargeAsymmetry_Mu82_EleUL90/rootFile/mkShapes__WHSS_OSCR_2018_v9_chargeAsymmetry_Mu82_EleUL90.root \
    --outputDir      /eos/user/n/ntrevisa/mkShapesRDF_rootfiles/WHSS_2018_v9_chargeAsymmetry_Mu82_EleUL90/rootFile/ \
    --outputFile     plots_WHSS_2018_v9_chargeAsymmetry_Mu82_EleUL90_DYflip_data.root \
    --year           2018 \
    --non_cf_bkg     Vg,VgS,WZ,ZZ,VVV,ggH_hww,qqH_hww,ZH_hww,ggZH_hww,WH_hww_plus,WH_hww_minus,ttH_hww,ggH_htt,qqH_htt,ZH_htt,WH_htt_plus,WH_htt_minus,Fake_ee,Fake_em_Fake_mm

cd -
