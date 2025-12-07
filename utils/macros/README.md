# README

## Using the b-tagging scale factor macros

This directory provides two ROOT macros:

* **`evaluate_btagSFbc.cc`**
* **`evaluate_btagSFlight.cc`**

Before using them inside **`aliases.py`**, you must compile them using ROOT.

### 1. Compile the macros with ROOT

Open a ROOT session and run:

```
.L evaluate_btagSFbc.cc+g
.L evaluate_btagSFlight.cc+g
```

The `+g` option tells ROOT to compile the macros and generate dictionaries so they can be called externally.

### 2. Load them in `aliases.py`

After compilation, the functions defined in these macros can be imported and used directly inside **`aliases.py`**.
