# **B Tagging Studies**  

This configuration is designed for **B tagging studies** in the **top control region** using **2022 data**. Below are the instructions to run the analysis.  

---

## **Features**  

In addition to the standard `.py` files found in most configurations, this setup includes macros for:  

- **Computing B tagging efficiency maps**, which are required for applying **fixed Working Point (WP) scale factors (SFs)**.  
- **Calculating the phase space extrapolation ratio (`r`)**, used for the application of **shape correction SFs**.  

For detailed documentation, refer to:  
- [Fixed Working Point Scale Factor Recommendations](https://btv-wiki.docs.cern.ch/PerformanceCalibration/fixedWPSFRecommendations/)  
- [Shape Correction Scale Factor Recommendations](https://btv-wiki.docs.cern.ch/PerformanceCalibration/shapeCorrectionSFRecommendations/)  

Since the fixed WP and reshaping methods require different configurations, `aliases.py` and `nuisances.py` have **separate versions**:  
- `*_fixedWP.py`  
- `*_reshaping.py`  

The appropriate files should be specified in `configuration.py` based on the chosen method.  

---

## **Loading the `mkShapesRDF` Environment**  

To load the `mkShapesRDF` environment, navigate to its installation directory and run:  

```sh
. ./start.sh
```

---

## **Running the `btag_ratio.cc` Macro**  

The `btag_ratio.cc` macro computes the **`r` ratio**, used for the **normalization of shape correction scale factors**.  

### **Usage:**  
1. Open **ROOT**:  

    ```sh
    root
    ```

2. Execute the macro:  

    ```cpp
    .x btag_ratio.cc("process", "algo_name", "wp")
    ```

- **Arguments:**  
  - `process`: Name of the process (e.g., `"ttbar"`)  
  - `algo_name`: B tagging algorithm (e.g., `"deepjet"`)  
  - `wp`: Working point (e.g., `"loose"`)  

- **Example:** Computing the ratio for the `ttbar` process using the `deepjet` algorithm at the `loose` WP:  

    ```cpp
    .x btag_ratio.cc("ttbar", "deepjet", "loose")
    ```

- **Output:**  
  - A `.txt` file saved in the **`btag_ratios`** folder.  
  - The **inclusive `r` ratio** is labeled as `Ratio totalXS`.  

---

## **Running the `bTagEff.cc` Macro**  

The `bTagEff.cc` macro generates **efficiency maps**, needed for **fixed WP scale factor applications**.  

### **Usage:**  
1. Open **ROOT**:  

    ```sh
    root
    ```

2. Execute the macro:  

    ```cpp
    .x bTagEff.cc(year, "process", "algo_name", "wp")
    ```

- **Arguments:**  
  - `year`: Data-taking year (e.g., `2022`)  
  - `process`: Name of the process (e.g., `"ttbar"`)  
  - `algo_name`: B tagging algorithm (e.g., `"DeepFlavB"`)  
  - `wp`: Working point (e.g., `"loose"`)  

- **Example:** Computing efficiency maps for `ttbar` in **2022 pre-EE era**, using the `DeepFlavB` algorithm at the `loose` WP:  

    ```cpp
    .x bTagEff(2022, "ttbar", "DeepFlavB", "loose")
    ```

- **Output:**  
  - A `.root` file stored in the **configuration folder**.  
  - Efficiency maps saved as **`.png` files** inside the `efficiencies` folder.  
  - The `.root` file will be used by **`evaluate_btagSFbc.cc`** and **`evaluate_btagSFlight.cc`** for **SF evaluations** (described in `aliases_reshaping.py`).  

---

## **Additional Information**  

For a better understanding of macro arguments, check the macro files directly, as naming conventions may vary.