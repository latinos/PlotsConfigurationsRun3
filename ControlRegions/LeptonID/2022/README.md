# WW_Run3
PlotConfiguration for WW Run 3 analysis

## Install

```
git clone https://github.com/BlancoFS/mkShapesRDF.git -b Run3

export MY_WORKDIR=$PWD

cd mkShapesRDF

./install.sh

source start.sh
```

## Once installed, every time you log in

```
cd mkShapesRDF

source start.sh
```

## Warnings

There have been two issues in the Postprocessing step. They are explained here:

- Lepton working point default value set as **True** instead of False. To deal with this, the `LepCut` aliases must be redefined in aliases.py using `&` instead of `||`.

- Jet collection not correctly created (Several problems with the jet_veto_maps and the PU ID, not existing anymore with Puppi). The jet collection is correctly recreated on-the-fly in runner.py. To solve the issue:

```
cp runner.py $MY_WORKDIR/mkShapesRDF/mkShapesRDF/shapeAnalysis/
```

## Run the code

Always compile after making any change in the configuration.

```
cd examples

git clone https://github.com/BlancoFS/WW_Run3.git

cd WW_Run3

mkShapesRDF -c 1

mkShapesRDF -o 0 -f . -b 1

hadd -fk -j 8 rootFiles/mkShapes__WW_2022.root rootFiles/mkShapes__WW_2022__ALL__*

mkPlot
```

The plots should be created in the `plots` folder.
