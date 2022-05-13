import json
import sys
import copy
import threading
import logging
import os
from docopt import docopt
import experiments
import numpy as np
from rl_agents.trainer import logger

BENCHMARK_FILE = 'benchmark_summary'
LOGGING_CONFIG = 'configs/logging.json'
VERBOSE_CONFIG = 'configs/verbose.json'
logger = logging.getLogger(__name__)

scores_lock = threading.Lock()
control_score = 0
scores = []

def gen_configs(filename, num_in_gen):
    new_configs = []
    with open(filename, 'r') as f:
        config_json = json.load(f)
        for config_num in range(num_in_gen):
            temp_config = copy.deepcopy(config_json)
            for key in temp_config['rewards'].keys():
                temp_config['rewards'][key] = temp_config['rewards'][key] + (200 * np.random.randn())
            new_configs.append(temp_config)
    return new_configs

def run_episodes(env_config_path, episode_count, thread_num):
    result = experiments.main_genetics(env_config_path, episode_count, thread_num)

    
    scores_lock.acquire(blocking=True)
    scores.append((result, env_config_path))
    scores_lock.release()


if __name__ == "__main__":
    og_config_name = sys.argv[1]
    thread_count = int(sys.argv[2])
    num_eps = int(sys.argv[3])
    generations = int(sys.argv[4])

    np.random.seed(42)

    best_config = og_config_name

    for gen in range(generations):
        configs_to_run = gen_configs(best_config, thread_count)
        open_threads = []

        for thread in range(thread_count):
            filename = "./genetic_configs/temp" + str(thread) + str(gen) + '.json'

            file = open(filename, 'w')
            json.dump(configs_to_run[thread], file)
            file.close()

            t = threading.Thread(target=run_episodes, args=(filename, num_eps, thread))
            open_threads.append(t)
            

        for t in open_threads: # stupid awful and dumb, blame pytorch 
            t.start()
            t.join()
        
        scores.sort(key=lambda x: x[0], reverse=True)
        best_config = scores[0][1]

        for score in scores: 
            print(score)

        scores = []
    

