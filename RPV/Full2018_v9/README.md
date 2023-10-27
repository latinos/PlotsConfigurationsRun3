# 1 - Produce the histrograms

Follow the instructions to install mkShapesRDF and to run the analysis:
https://mkshapesrdf.readthedocs.io/en/latest/getting_started.html#getting-started

# 2 - Produce the datacards including the analytic Crystal-Ball pdf for modelling the signal:

```bash
python scripts/mkDatacardsParam.py --pycfg configuration.py --inputFile=rootFile/XYZ.root --isParametric 
```

# 3 - Run the fit procedure:

```bash
./scripts/doFits.sh
```
