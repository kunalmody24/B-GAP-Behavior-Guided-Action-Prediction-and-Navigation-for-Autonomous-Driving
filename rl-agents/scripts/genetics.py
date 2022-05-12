# copy the given config 
# make n copies with rand differences
# run n instances for m episodes
import json
import sys
import copy
import numpy as np

def gen_configs(filename, num_in_gen):
    np.random.seed(42)
    new_configs = []
    with open(filename, 'r') as f:
        config_json = json.load(f)
        for config_num in range(num_in_gen):
            temp_config = copy.deepcopy(config_json)
            for key in temp_config['rewards'].keys():
                temp_config['rewards'][key] = temp_config['rewards'][key] + np.random.randn()
            new_configs.append(temp_config)
    return new_configs
        

if __name__ == "__main__":
    configs_to_run = gen_configs(sys.argv[1], 2)
    gen = 0
    for config in range(len(configs_to_run)):
        with open("./genetic_configs/temp" + str(config) + str(gen) + '.json', 'w') as file:
            json.dump(configs_to_run[config], file)