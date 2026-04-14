import sys,os
import importlib.util

variable = ""

print("#######################")
print("Number of arguments: {}".format(len(sys.argv)))
print("Argument List: {}".format(str(sys.argv)))
if (len(sys.argv) > 1):
    variable = sys.argv[1]
    print(f"Variable: {variable}")
else:
    print("Please specify the variable you want to use. E.g.:")
    print("python script_gof_variables_wrapper.py mll")
    sys.exit()
print("#######################")

pwd = os.getcwd()

# Function to load variables
def load_module_from_path(module_name, file_path):
    spec   = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# WHSS variables
variables_whss = load_module_from_path("variables_whss", f"{pwd}/../Full2018_v9/WHSS/variables.py")
vars_whss_dict = variables_whss.variables
vars_whss_list = list(vars_whss_dict.keys())
print(vars_whss_list)

# WH3l variables
variables_wh3l = load_module_from_path("variables_wh3l", f"{pwd}/../Full2018_v9/WH3l/variables.py")
vars_wh3l_dict = variables_wh3l.variables
vars_wh3l_list = list(vars_wh3l_dict.keys())
print(vars_wh3l_list)

# All variables
vars_all_list = list(set(vars_wh3l_list) | set(vars_whss_list))
print(vars_all_list)

if variable not in vars_all_list:
    print("This variable is not available. Check this list of available variables:")
    for var in vars_all_list:
        print(f"python script_gof_variables_wrapper.py {var}")
    sys.exit()

# Combining datacards
os.system(f"python3 script_combine_datacards_variable.py {variable}")

if ((variable in vars_whss_list) and (variable in vars_wh3l_list)):
    # WHSS + WH3l
    os.system(f"bash do_gof_test.sh Full2016        WH_chargeAsymmetry_WH_Full2016_v9_high_pt        {pwd} {variable}")
    os.system(f"bash do_gof_test.sh 2016noHIPM      WH_chargeAsymmetry_WH_2016noHIPM_v9_high_pt      {pwd} {variable}")
    os.system(f"bash do_gof_test.sh 2016HIPM        WH_chargeAsymmetry_WH_2016HIPM_v9_high_pt        {pwd} {variable}")

if variable in vars_whss_list:
    # Only WHSS
    os.system(f"bash do_gof_test.sh Full2016_WHSS   WH_chargeAsymmetry_WH_Full2016_v9_WHSS_high_pt   {pwd} {variable}")
    os.system(f"bash do_gof_test.sh 2016noHIPM_WHSS WH_chargeAsymmetry_WH_2016noHIPM_v9_WHSS_high_pt {pwd} {variable}")
    os.system(f"bash do_gof_test.sh 2016HIPM_WHSS   WH_chargeAsymmetry_WH_2016HIPM_v9_WHSS_high_pt   {pwd} {variable}")

if variable in vars_wh3l_list:    
    # Only WH3l
    os.system(f"bash do_gof_test.sh Full2016_WH3l   WH_chargeAsymmetry_WH_Full2016_v9_WH3l           {pwd} {variable}")
    os.system(f"bash do_gof_test.sh 2016HIPM_WH3l   WH_chargeAsymmetry_WH_2016HIPM_v9_WH3l           {pwd} {variable}")
    os.system(f"bash do_gof_test.sh 2016noHIPM_WH3l WH_chargeAsymmetry_WH_2016noHIPM_v9_WH3l         {pwd} {variable}")
