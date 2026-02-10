import os.path
import json
import matplotlib.pyplot as plt
import importlib.util


input_dir = "GoF"
cat = "2016HIPM_WHSS"

categories = {
    '2016HIPM_WHSS'   : "WHSS",
    '2016HIPM_WH3l'   : "WH3l",
    '2016noHIPM_WHSS' : "WHSS",
    '2016noHIPM_WH3l' : "WH3l",
}


def get_variables(final_state = "WHSS"):
    # Get variables
    spec = importlib.util.spec_from_file_location(
        "variables",
        f"../Full2018_v9/{final_state}/variables.py"
    )
    config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(config)

    d = config.variables
    variables = d.keys()

    return variables

def get_p_value(cat, var, p_value_dict):
    json_name = f"{input_dir}/GoF_{cat}_{var}.json"

    print(json_name)
    
    if os.path.isfile(json_name):
        with open(json_name, "r") as j:
            json_dict = json.load(j)
            p_value_dict[var] = json_dict['120.0']['p']


# Main

for cat in categories.keys():
    print(f"Current category: {cat}")

    # Inizialize p-value dictionary
    p_value_dict = {}

    # Get variables
    variables = get_variables(categories[cat])

    # Loop over variables
    for var in variables:
        get_p_value(cat, var, p_value_dict)

    # Check if the values makes sense
    print(p_value_dict)

    # Preparing variables for plotting
    variable_names, p_values = zip(*p_value_dict.items())
    variable_names = list(variable_names)
    p_values = list(p_values)

    height = min(0.3 * len(variable_names), 30)

    # Actual plotting
    plt.figure(figsize=(8, height))
    plt.axvspan(0, 0.05, color='red', alpha=0.3, label="p < 0.05")
    plt.scatter(p_values, range(len(variable_names)), marker='+', s=100, color='blue')
    plt.yticks(range(len(variable_names)), variable_names)
    plt.xlabel("Saturated GoF p-value")
    plt.title(f"GoF Summary: {cat}")
    plt.xlim(0, 1)
    plt.grid(True, axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()

    # Saving
    output_dir = 'GoF_summary_plot'
    os.makedirs(output_dir, exist_ok=True)
    os.system(f'cp ~/index.php {output_dir}')
    out_base = os.path.join(output_dir, f"{cat}_GoF_summary")
    plt.savefig(f"{out_base}.png", dpi=300)
    plt.savefig(f"{out_base}.pdf")
    plt.close()
    print(f"Saved plot: {out_base}.png / .pdf")


        

# # Cosmetic parameters
# plt.rcParams.update({
#     "font.size"       : 12,
#     "axes.labelsize"  : 14,
#     "xtick.labelsize" : 12,
#     "ytick.labelsize" : 12,
# })


# warnings.filterwarnings("ignore", message="The value of the smallest subnormal")

# def unroll_categories(cuts):
#     '''
#     Unrolls the cuts and categories from cuts.py
#     '''
#     categories = []
#     for cut in cuts:
#         for cat in cuts[cut]['categories'].keys():
#             categories.append(f'{cut}_{cat}')
#     print(categories)
#     return categories

# def load_pvalue(json_path, mass_value = "120.0"):
#     '''
#     Get p-value from GoF json file
#     '''
#     with open(json_path) as f:
#         data = json.load(f)
#         if mass_value in data and "p" in data[mass_value]:
#             return data[mass_value]["p"]
#     return None


# def extract_finalstate_and_variable(filename, valid_vars):
#     base = filename.replace("GoF_", "").replace(".json", "")
#     for var in sorted(valid_vars, key=len, reverse=True):
#         if base.endswith(f"_{var}"):
#             final_state = base[:-(len(var) + 1)]
#             return final_state, var
#     return None, None


# def plot_gof(final_state, var_to_pval, output_dir):
#     if not var_to_pval:
#         print(f"No p-values for {final_state}")
#         return

    
#     ordered_items = [(var, var_to_pval[var]) for var in variables if var in var_to_pval]
#     variable_names, p_values = zip(*ordered_items)
#     height = min(0.3 * len(variable_names), 30)

#     plt.figure(figsize=(8, height))
#     plt.axvspan(0, 0.05, color='red', alpha=0.3, label="p < 0.05")
#     plt.scatter(p_values, range(len(variable_names)), marker='+', s=100, color='blue')
#     plt.yticks(range(len(variable_names)), variable_names)
#     plt.xlabel("Saturated GoF p-value")
#     plt.title(f"GoF Summary: {final_state}")
#     plt.xlim(0, 1)
#     plt.grid(True, axis='x', linestyle='--', alpha=0.6)
#     plt.tight_layout()

#     os.makedirs(output_dir, exist_ok=True)
#     out_base = os.path.join(output_dir, f"{final_state}_GoF_summary")
#     plt.savefig(f"{out_base}.png", dpi=300)
#     plt.savefig(f"{out_base}.pdf")
#     plt.close()
#     print(f"Saved plot: {out_base}.png / .pdf")



# def plot_all_by_final_state(gof_dir, cat="Full2016", output_dir="GoF_plots/summary_plots_by_finalstate"):

#     # Collect all GoF json files
#     json_files = [f for f in os.listdir(gof_dir) if f.startswith("GoF_") and f.endswith(".json") and (cat in f)]
#     if not json_files:
#         print(f"No GoF_*.json files found in {gof_dir}")
#         return

#     # Collect variables
#     # valid_vars = variables.keys()
    
#     data = defaultdict(dict)

#     # Loop over json files
#     for filename in json_files:
#         json_path = os.path.join(gof_dir, filename)
#         pval      = load_pvalue(json_path)
#         if pval is not None:
#             final_state, variable = extract_finalstate_and_variable(filename, valid_vars)
#             if final_state and variable:
#                 data[final_state][variable] = pval
#             else:
#                 print(f"Could not match variable in: {filename}")

#     for final_state, var_to_pval in data.items():
#         plot_gof(final_state, var_to_pval, output_dir)

# # Main
# if __name__ == "__main__":

#     os.system("mkdir -p GoF_plots/")
#     os.system("cp /afs/cern.ch/user/n/ntrevisa/public/utils/index.php GoF_plots/")

#     # Collect json files
#     gof_dir = "GoF/"
#     cat = "Full2016"
#     var = "mll"
#     json_files = [f for f in os.listdir(gof_dir) if f.startswith("GoF_") and f.endswith(".json") and (cat in f)]
#     if not json_files:
#         print(f"No GoF_*.json files found in {gof_dir}")
#         # return
#     print(json_files)

#     final_name = f"GoF_{cat}_{var}.json"

#     for json_file in json_files:
#         if var in json_file:
#             print(json_file)

#     plot_gof(final_state, var_to_pval, output_dir)

#     # # categories = unroll_categories(cuts)
    
#     # for cat in categories:

#     #     print(f"Working on category: {cat}")
        
#     #     plot_all_by_final_state("GoF", cat)



