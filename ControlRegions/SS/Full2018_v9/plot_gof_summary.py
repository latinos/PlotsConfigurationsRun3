import os
import json
import matplotlib.pyplot as plt
from collections import defaultdict
import warnings
from variables import variables  


plt.rcParams.update({
    "font.size": 12,
    "axes.labelsize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
})


warnings.filterwarnings("ignore", message="The value of the smallest subnormal")


def load_pvalue(json_path):
    with open(json_path) as f:
        data = json.load(f)
        if "120.0" in data and "p" in data["120.0"]:
            return data["120.0"]["p"]
    return None


def extract_finalstate_and_variable(filename, valid_vars):
    base = filename.replace("GoF_", "").replace(".json", "")
    for var in sorted(valid_vars, key=len, reverse=True):
        if base.endswith(f"_{var}"):
            final_state = base[:-(len(var) + 1)]
            return final_state, var
    return None, None


def plot_gof(final_state, var_to_pval, output_dir):
    if not var_to_pval:
        print(f"No p-values for {final_state}")
        return

    ordered_items = [(var, var_to_pval[var]) for var in variables if var in var_to_pval]
    variable_names, p_values = zip(*ordered_items)
    height = min(0.3 * len(variable_names), 30)

    plt.figure(figsize=(8, height))
    plt.axvspan(0, 0.05, color='red', alpha=0.3, label="p < 0.05")
    plt.scatter(p_values, range(len(variable_names)), marker='+', s=100, color='blue')
    plt.yticks(range(len(variable_names)), variable_names)
    plt.xlabel("Saturated GoF p-value")
    plt.title(f"GoF Summary: {final_state}")
    plt.xlim(0, 1)
    plt.grid(True, axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()

    os.makedirs(output_dir, exist_ok=True)
    out_base = os.path.join(output_dir, f"{final_state}_GoF_summary")
    plt.savefig(f"{out_base}.png", dpi=300)
    plt.savefig(f"{out_base}.pdf")
    plt.close()
    print(f"Saved plot: {out_base}.png / .pdf")



def plot_all_by_final_state(gof_dir, output_dir="GoF/summary_plots_by_finalstate"):
    json_files = [f for f in os.listdir(gof_dir) if f.startswith("GoF_") and f.endswith(".json")]
    if not json_files:
        print(f"No GoF_*.json files found in {gof_dir}")
        return

    valid_vars = variables.keys()
    data = defaultdict(dict)

    for filename in json_files:
        json_path = os.path.join(gof_dir, filename)
        pval = load_pvalue(json_path)
        if pval is not None:
            final_state, variable = extract_finalstate_and_variable(filename, valid_vars)
            if final_state and variable:
                data[final_state][variable] = pval
            else:
                print(f"Could not match variable in: {filename}")

    for final_state, var_to_pval in data.items():
        plot_gof(final_state, var_to_pval, output_dir)

if __name__ == "__main__":
    plot_all_by_final_state("GoF/plots")



