
cmsenv
ulimit -s unlimited

Card_Dir=~/work/private/Comb/CMSSW_14_1_0_pre4/src/run3/cards

CombSet="-s 1 -t -1 --cminDefaultMinimizerTolerance=0.1 --cminDefaultMinimizerStrategy=1 --cminDefaultMinimizerType Minuit2 --cminDefaultMinimizerAlgo Migrad --cminFallbackAlgo Minuit2,Migrad,0:0.6 --cminPreFit=1 --cminApproxPreFitStrategy=2 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --X-rtd MINIMIZER_analytic --alignEdges 1 --saveNLL --X-rtd REMOVE_CONSTANT_ZERO_POINT=1 --X-rtd FAST_VERTICAL_MORPH" # --dry-run"

case "$1" in     
    Fai)
        coups=("muV" "muF" "Fa2" "Fa3" "Fg2" "Fg3" "Fk1" "Fz2" "Fz3")
	srange=("0,3" "0,3" "-0.6,0.6" "-0.2,0.2" "-0.99,0.99" "-0.99,0.99" "-0.2,0.6" "-0.99,0.99" "-0.99,0.99") 
        initval="muV=1,muF=1,Fa2=0,Fa3=0,Fg2=0,Fg3=0,Fk1=0,Fz2=0,Fz3=0"
        inputcard="${Card_Dir}/HVVFai.root"
	conjob="--job-mode=condor --split-points 10"
	#conjob="--pointsRandProf 100 --job-mode=condor --split-points 1"  # Allow multiple initial guesses (slow!) 
        ;;
    ciHB)
        coups=("cZ" "cZZ" "cZZt" "cZB" "cZg" "cZgt" "cgg" "cggt")
	srange=("-1,1" "-2,2" "-2,2" "-0.5,0.5" "-3,3" "-3,3" "-10,10" "-10,10") 
        initval="cZ=0,cZZ=0,cZZt=0,cZB=0,cZg=0,cZgt=0,cgg=0,cggt=0"
        inputcard="${Card_Dir}/HVVciHB.root"
	conjob="--job-mode=condor --split-points 10"
        ;;
    ciWB)
        coups=("cHb" "cHD" "cHW" "cHWt" "cHWB" "cHWBt" "cHB" "cHBt")
	srange=("-10,10" "-5,5" "-3,3" "-3,3" "-10,10" "-10,10" "-5,5" "-5,5") 
        initval="cHb=0,cHD=0,cHW=0,cHWt=0,cHWB=0,cHWBt=0,cHB=0,cHBt=0"
        inputcard="${Card_Dir}/HVVciWB.root"
	conjob="--job-mode=condor --split-points 10"
        ;;
esac

echo "Card : " $inputcard
echo "Initial Setting : " $initval 

for i in "${!coups[@]}"; do
    
    coup="${coups[$i]}"
    ran="${srange[$i]}"
    echo "Scan: ${coup} in range: ${ran}"

    other_coups=()
    for x in "${coups[@]}"; do
        if [[ "$x" != "$coup" && "$x" != "muV" && "$x" != "muF" ]]; then
            other_coups+=("$x")
        fi
    done
    other_coups_fr=$(IFS=, ; echo "${other_coups[*]}")

    combineTool.py -n HVV_"$coup" -d $inputcard -m 125 --algo=grid --points 51 --setParameters $initval --redefineSignalPOIs="$coup" --setParameterRanges "$coup"="$ran" -M MultiDimFit $CombSet $conjob --sub-opts=$'output = /dev/null\nerror = /dev/null\nlog = condor/$(Cluster).log\n+JobFlavour = "tomorrow"' --task-name HVV_"$coup" 

    echo "Freeze : ${other_coups_fr}"
    
    combineTool.py -n HVV_"$coup"Fr -d $inputcard -m 125 --algo=grid --points 51 --setParameters $initval --redefineSignalPOIs="$coup" --setParameterRanges "$coup"="$ran" --freezeParameters "$other_coups_fr" -M MultiDimFit $CombSet --job-mode=condor --split-points 100 --sub-opt '+JobFlavour = "tomorrow"' --task-name HVV_"$coup"Fr

    done
 
# Useful additions : --freezeParameters allConstrainedNuisances
