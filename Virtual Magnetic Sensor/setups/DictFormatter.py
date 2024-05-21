import ast
import subprocess
import numpy as np

#INI FILE TO PY FILE

file_path="setups/EvoStandard.py"

def convert_lists_to_arrays(input_dict):
    for key, value in input_dict.items():
        if isinstance(value, list):
            np_array = np.array(value)
            input_dict[key] = np.object_(np_array)
    return input_dict

with open(file_path, 'r') as file:
    file_content = file.read()
    data_dict = ast.literal_eval(file_content)

data_key_list=list(data_dict.keys())
test=str()

for i in range(len(data_key_list)):
    convert_lists_to_arrays(data_dict[data_key_list[i]])
    test+=str(data_key_list[i])+"="+str(data_dict[data_key_list[i]])+"\n"

# Open the file & clear its contents
with open(file_path, "w") as file:
    file.write("import numpy as np"+"\n")
    file.write(test)
    subprocess.run(["autopep8", "--in-place", file_path])  

