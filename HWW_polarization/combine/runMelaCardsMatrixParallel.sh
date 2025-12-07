#!/bin/bash

echo ""
echo "Prepare input cards!"
echo ""

if [ $1 == "0p0" ]
then
    fl=$1
else
    fl=m$1
fi

echo ""
echo "---- Input parameters ----"
echo "fL = " $1
echo "fP = " $2
echo "fL for datacards = " $fl
echo "--------------------------"

cd /afs/cern.ch/work/s/sblancof/private/Run2Analysis/combine/CMSSW_14_1_0_pre4/src/

cmsenv

ulimit -Ss unlimited

for i in {2016_HIPM,2016_noHIPM,2017,2018}
do
    pushd /eos/user/s/sblancof/MC/combine/HWW_helicity/MatrixCLL/datacards_MELA_${i}/

    echo $PWD

    # datacard_fL_0p4_fPerp_m0p6.txt

    combineCards.py hww2l2v_13TeV_sr_0j_pt2gt20/RF_0J_2D/datacard_fL_${fl}_fPerp_${2}.txt hww2l2v_13TeV_sr_0j_pt2lt20/RF_0J_2D/datacard_fL_${fl}_fPerp_${2}.txt hww2l2v_13TeV_top_0j/events/datacard_fL_${fl}_fPerp_${2}.txt hww2l2v_13TeV_dytt_0j/events/datacard_fL_${fl}_fPerp_${2}.txt hww2l2v_13TeV_ss_0j/events/datacard_fL_${fl}_fPerp_${2}.txt > datacard_fL_${fl}_fPerp_${2}_combined_0j.txt

    combineCards.py hww2l2v_13TeV_sr_1j_pt2gt20/RF_1J_2D/datacard_fL_${fl}_fPerp_${2}.txt hww2l2v_13TeV_sr_1j_pt2lt20/RF_1J_2D/datacard_fL_${fl}_fPerp_${2}.txt hww2l2v_13TeV_top_1j/events/datacard_fL_${fl}_fPerp_${2}.txt hww2l2v_13TeV_dytt_1j/events/datacard_fL_${fl}_fPerp_${2}.txt hww2l2v_13TeV_ss_1j/events/datacard_fL_${fl}_fPerp_${2}.txt > datacard_fL_${fl}_fPerp_${2}_combined_1j.txt

    combineCards.py hww2l2v_13TeV_sr_2j/RF_2J_2D/datacard_fL_${fl}_fPerp_${2}.txt hww2l2v_13TeV_sr_2j_vbf/RF_VBF_2D/datacard_fL_${fl}_fPerp_${2}.txt hww2l2v_13TeV_top_2j/events/datacard_fL_${fl}_fPerp_${2}.txt hww2l2v_13TeV_dytt_2j/events/datacard_fL_${fl}_fPerp_${2}.txt hww2l2v_13TeV_ss_2j/events/datacard_fL_${fl}_fPerp_${2}.txt > datacard_fL_${fl}_fPerp_${2}_combined_2j.txt

    combineCards.py datacard_fL_${fl}_fPerp_${2}_combined_0j.txt datacard_fL_${fl}_fPerp_${2}_combined_1j.txt datacard_fL_${fl}_fPerp_${2}_combined_2j.txt > datacard_fL_${1}_fPerp_${2}_combined.txt

    popd
done

combineCards.py /eos/user/s/sblancof/MC/combine/HWW_helicity/MatrixCLL/datacards_MELA_2018/datacard_fL_${1}_fPerp_${2}_combined.txt /eos/user/s/sblancof/MC/combine/HWW_helicity/MatrixCLL/datacards_MELA_2017/datacard_fL_${1}_fPerp_${2}_combined.txt /eos/user/s/sblancof/MC/combine/HWW_helicity/MatrixCLL/datacards_MELA_2016_noHIPM/datacard_fL_${1}_fPerp_${2}_combined.txt /eos/user/s/sblancof/MC/combine/HWW_helicity/MatrixCLL/datacards_MELA_2016_HIPM/datacard_fL_${1}_fPerp_${2}_combined.txt > /eos/user/s/sblancof/MC/combine/HWW_helicity/MatrixCLL/datacard_fL_${1}_fPerp_${2}_combined.txt

text2workspace.py /eos/user/s/sblancof/MC/combine/HWW_helicity/MatrixCLL/datacard_fL_${1}_fPerp_${2}_combined.txt -m 125 -P HiggsAnalysis.CombinedLimit.QEHWW:QEHWW --PO fL_${1} --PO fPerp_${2} --PO doMatrix -o /eos/user/s/sblancof/MC/combine/HWW_helicity/MatrixCLL/datacard_fL_${1}_fPerp_${2}_combined_matrix.root

mkdir limits_fL_${1}_fPerp_${2}_matrixParallel

cd limits_fL_${1}_fPerp_${2}_matrixParallel

combineTool.py -M MultiDimFit --algo grid --points 50 --setParameters r=0,cll=1 --redefineSignalPOIs cll --setParameterRanges cll=-1.0,1.0 --alignEdges 1 -t -1 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy=0 --verbose 1 -d /eos/user/s/sblancof/MC/combine/HWW_helicity/MatrixCLL/datacard_fL_${1}_fPerp_${2}_combined_matrix.root -m 125 --saveToys --job-mode=condor --split-points 1
