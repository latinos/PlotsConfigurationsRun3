
cmsenv

case "$1" in
    Fai)
        coups=("muV" "muF" "Fa2" "Fa3" "Fg2" "Fg3" "Fk1" "Fz2" "Fz3")
        ;;
    ciHB)
        coups=("cZ" "cZZ" "cZZt" "cZB" "cZg" "cZgt" "cgg" "cggt")
        ;;
    ciWB)
        coups=("cHb" "cHD" "cHW" "cHWt" "cHWB" "cHWBt" "cHB" "cHBt")
        ;;
esac

loc="condor"

echo "Directory :" $loc

for coup in "${coups[@]}"; do
  echo "$coup"

  hadd higgsCombineHVV_"$coup".MultiDimFit.mH125.root $loc/higgsCombineHVV_"$coup".POINTS.*.MultiDimFit.mH125.1.root
  mv higgsCombineHVV_"$coup".MultiDimFit.mH125.root hists/

  hadd higgsCombineHVV_"$coup"Fr.MultiDimFit.mH125.root $loc/higgsCombineHVV_"$coup"Fr.POINTS.*.MultiDimFit.mH125.1.root
  mv higgsCombineHVV_"$coup"Fr.MultiDimFit.mH125.root hists/
  
done



