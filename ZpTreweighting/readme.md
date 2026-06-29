## Deriving and applying ZpT reweights for all jet bin categories for a certain year:
Go within a certain config folder (divided by years) and run automate.py with required parameters values. Example:
`python3 automate.py  --second-analysis ./ --year 2023 --sample-type NLO | tee automation_terminal_output.txt`

It is advised to run the above codeline on a lingering screen (tmux or screen) owing to ~40 minutes of runtime (20 for each mkShapesRDF run), but not strictly necessary.

In order to produce the 2D histograms looking at gen_pTll vs pTll, an example runline(s) from the ZpTreweighting/ folder are as follows:
'''
root
.x twoDhists.cc(2022, "DY", "DeepFlavB", "loose")
'''
The arguments (2022, "DY", "DeepFlavB", "loose") are the default ones, so those could be omitted.