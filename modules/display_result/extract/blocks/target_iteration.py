import json
from tqdm import tqdm

from modules.utils.tools import list_direct_files

def extract_precision_iteration(folder_ttl_iteration):
    print(f"{folder_ttl_iteration=}")
    ttl_iteration, _ = list_direct_files(folder_ttl_iteration)
    if len(ttl_iteration) != 21:
        ttl_precision_iteration = None
    else:
        ttl_precision_iteration = []
        for iteration in tqdm(ttl_iteration):
            with open(iteration, 'r', encoding="utf-8") as f:
                record = json.load(f)
            precision = record["result"]["pair_best"]["precision"]["train"]
            ttl_precision_iteration.append(precision)
    return ttl_precision_iteration

def extract_os_prompt_iteration(folder_ttl_iteration):
    print(f"{folder_ttl_iteration=}")
    ttl_iteration, _ = list_direct_files(folder_ttl_iteration)
    if len(ttl_iteration) != 21:
        ttl_os_prompt_iteration = None
    else:
        ttl_os_prompt_iteration = []
        for iteration in ttl_iteration[-1:]:
        # for iteration in tqdm(ttl_iteration):
            with open(iteration, 'r', encoding="utf-8") as f:
                record = json.load(f)
            os_prompt = record["result"]["pair_best"]["prompt"]
            ttl_os_prompt_iteration.append(os_prompt)
    return ttl_os_prompt_iteration
