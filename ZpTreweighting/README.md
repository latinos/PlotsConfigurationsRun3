# Z pT reweighting of DY

Derives a data-driven correction to the DY Z pT spectrum, in jet bins, and applies it back to DY.

Current config folders: `2022_v12`, `2023_v12`, `2024_v15`. Each one is self-contained: it has its own `automate.py`, `extract_Zptrw.py` and `dyZpTrw.json`.

## Pipeline

1. **Fill the shapes without reweighting.**
   - Selection (`cuts.py`): two tight leptons, 60 < mll < 120 GeV, `noJetInHorn`.
   - Regions: `Zee` / `Zmm`, each split into `0j`, `1j` (second jet pT < 30 GeV) and `2j`.
   - Variable: `ptll`.
   - The DY weight `DY_ZpTrw` is switched off during this step.
2. **Build the data/DY ratio.** In each jet bin, `extract_Zptrw.py` takes the `ptll` histograms from the merged ROOT file and computes:
   - (DATA − all non-DY backgrounds) / DY
   - The non-DY backgrounds typically include top, WW, ggWW, WZ, WZS, ZZ, Zg, ZgS, Wg, WgS, VVV and SMhiggs.
3. **Fit the ratio** (μμ channel, `-f -n 2`).
   - Fit range: 0–50 GeV.
   - Fit function: `p0*Erf((x-p1)/p2) + p3*x + p4*x^2 + p5`.
   - Above 50 GeV the weight is held at the fit value at 50 GeV.
   - The resulting formula is written to `dyZpTrw.json` under `DYrew[<year>][<sample-type>_<0j|1j|2j>]`. Entries for other years and sample types are kept.
   - The ee channel is only plotted, as a cross-check.
4. **Apply the weights.**
   - `aliases.py` reads `dyZpTrw.json` and builds `DY_ZpTrw`: the fitted formula in each jet bin, evaluated at the generator-level Z pT (`gen_Zpt`).
   - `samples.py` applies it to the DY datasets with `addSampleWeight(samples, 'DY', ..., 'DY_ZpTrw')`.
5. **Closure.** Rerun the shapes with the weights applied and check the `ptll` data/MC agreement. In this pass `extract_Zptrw.py` runs without `-f`, so it only makes plots and leaves `dyZpTrw.json` unchanged.

`samples.py` chooses the DY sample from the tag: `_LO_` in the tag means the LO DY sample, anything else means NLO.

## Running

On lxplus, with mkShapesRDF set up (`source start.sh`), go into a year folder and run:

```
cd 2024_v15
python3 automate.py --year 2024_v15 --sample-type NLO --second-analysis ./ | tee automation_terminal_output.txt
```

- `--year`: the key used in `dyZpTrw.json` and in the `DYrew[...]` lookups in `aliases.py`. Use the folder name.
- `--sample-type`: `LO` or `NLO`. Please NOTE that LO sample names need to be updated based on post-processing campaign samples. As of 12 October, 2026, all NLO samples are updated and correct.
- `--second-analysis ./`: also runs the closure pass (step 5) in the same folder. Without it, the script stops after writing `dyZpTrw.json`.

The full run takes about 40 minutes (about 20 per mkShapesRDF round), so run it inside `tmux` or `screen`.

### What `automate.py` does

**Round 1: derive the weights**
- Sets `tag` in `configuration.py` to `{year}_{sample-type}_ZpTreweighting_obtainWeights`.
- Comments out the `DY_ZpTrw` `addSampleWeight` line in `samples.py`.
- Runs `mkShapesRDF -c 1`, then `mkShapesRDF -o 0 -f . -b 1`.
- Waits for condor, then merges with `mkShapesRDF -o 2 -f .`.
- Runs `extract_Zptrw.py` for 0j, 1j and 2j, which updates `dyZpTrw.json`.
- Runs `mkPlot --onlyPlot cratio --showIntegralLegend 1 --fileFormats png`.
- Moves `condor/`, `configs/`, `extractPlots_*` and `plots_*` to `/eos/user/<u>/<user>/mkShapesRDF_rootfiles/<tag>/`.

**Round 2: closure** (only with `--second-analysis`)
- Sets the tag suffix to `afterReweighting`.
- Points the `DYrew[...]` keys in `aliases.py` at `--year` / `--sample-type`.
- Uncomments the `DY_ZpTrw` line in `samples.py`.
- Compiles, submits, waits and merges.
- Runs `extract_Zptrw.py` for plots only, then `mkPlot`.
- Moves the outputs to EOS, with the folder suffix `_afterReweighting`.

`automate.py` edits `configuration.py`, `samples.py` and `aliases.py` in place, so expect them to show up in `git diff` after a run.

Merged ROOT files are written to:

```
/eos/user/<u>/<user>/mkShapesRDF_rootfiles/<tag>/rootFile/mkShapes__<tag>.root
```

### Resuming a partial run

Round-1 skip flags:
- `--skip-submit`
- `--skip-wait`
- `--skip-merge`
- `--skip-extract`

Round-2 skip flags:
- `--skip-second-wait`
- `--skip-second-merge`

Round 2 has no skip flag for compile and submit. Rerunning with `--second-analysis` therefore always resubmits every closure job. If round 2 fails after its jobs are done, finish it by hand: merge, run `extract_Zptrw.py` without `-f`, then `mkPlot`.

If `mkShapesRDF -o 2` stops with `TFileMerger::AddFile: cannot open file ...__ALL__<sample>_<n>.root`, one job's output is missing or truncated.
- `mkShapesRDF -o 1` does not open the output files, so it can miss this.
- Fix: move the bad files aside, resubmit only those jobs, then merge again.

### Running `extract_Zptrw.py` by hand

```
python3 extract_Zptrw.py -f -n 2 -c mm -nj 0 --input <merged.root> --write-json dyZpTrw.json --year 2024_v15 --sample-type NLO
python3 extract_Zptrw.py -c ee -nj 0 --input <merged.root>
```

- `-f`: fit the ratio. `--write-json` only writes when `-f` is given.
- `-n`: normalization method, see `--help`.
- `-c`: channel, `mm` or `ee`.
- `-nj`: jet bin, `0`, `1` or `2`.
- `--fit-xrange` / `--plot-xrange`: default 50 / 80 GeV.

The background histograms subtracted from data are listed explicitly in the script. If you add or rename a background sample in `samples.py`, update that list too.

## 2D gen pTll vs pTll histograms

To produce the 2D histograms of gen_pTll vs pTll, run from the ZpTreweighting/ folder:
```
root
.x twoDhists.cc(2022, "DY", "DeepFlavB", "loose")
```
The arguments (2022, "DY", "DeepFlavB", "loose") are the default ones, so those could be omitted.
