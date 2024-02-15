#!/bin/bash

toysignal="RPV_sb700_chi400_sl370"
variables="sb_mass chi_mass slep_mass"

COMBINE_OPTIONS="--cminDefaultMinimizerStrategy 0 --cminApproxPreFitTolerance=100  --cminFallbackAlgo Minuit2,Migrad,0:0.1 --cminDefaultMinimizerTolerance 0.1 --X-rtd MINIMIZER_MaxCalls=9999999  --X-rtd MINIMIZER_analytic --X-rtd FAST_VERTICAL_MORPH  --X-rtd MINIMIZER_freezeDisassociatedParams  --X-rtd OPTIMIZE_BOUNDS=0"

cd ${HOME}/Combine14x/CMSSW_14_0_0_pre1/src/
cmsenv
cd -

for variable in $variables; do
  echo $variable

  if [ $variable == "chi_mass" ]; then
    range="180 10 600"
  elif [ $variable == "sb_mass" ]; then
    range="250 10 800"
  elif [ $variable == "slep_mass" ]; then
    range="100 10 450"
  else
    continue
  fi
  
  datacard_path=PATH/${variable}
  cd $datacard_path
  
  # some edits in the datacard
  if ! grep -Fq "shapes  data_obs" datacard.txt;
  then
    sed -i '9 i shapes  data_obs           * shapes/histos_hww2l2v_13TeV_top_1j.root     w:top' datacard.txt
  fi
  sed -i 's/.*observation.*/observation -1/g' datacard.txt
  ## The following removes MC stat nuisance parameters for all the processes. Actually we want to remove them only for 'sig' but did not find a way yet.
  sed -i '/.*autoMCStats.*/d' datacard.txt

  # workspace used for toy generation
  text2workspace.py datacard.txt -o datacard_${toysignal}.root -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose --PO 'map=.*/.*sb.*:0' --PO 'map=.*/sig:0' --PO 'map=.*/.*'${toysignal}'.*:r[1,-10,10]'
 
  # workspace used for fits
  text2workspace.py datacard.txt -o datacard_forfit.root -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose --PO 'map=.*/.*sb.*:0' --PO 'map=.*/sig:r[1,0,20000]'
  
  # Generate toy signal 
  combine -M GenerateOnly datacard_${toysignal}.root -t 1 --expectSignal=1 --saveToys -n ${toysignal}
  
  # Perform a mass scan and compute the p-value for each mass hypothesis (mass == mean of the CrystalBall p.d.f.)
  for mass in `seq $range`; do
    echo "################### $mass"	
    combine -M Significance --pvalue datacard_forfit.root --toysFile higgsCombine${toysignal}.GenerateOnly.mH120.123456.root -t 1 --setParameters MH=${mass},alpha=1 --freezeParameter MH --setParameterRanges sigma=1,100:n=0.1,40:alpha=0,5:r=0,20000 --redefineSignalPOI r $COMBINE_OPTIONS &> pvalue_${toysignal}_m${mass}.out
  done
done

