
from copy import deepcopy
import json
from pathlib import Path

from modules.execution.blocks.utils import time_now
from modules.utils.get_config import get_config
CONFIG = get_config()
DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]

def refine_pair(pair):
    """ prompt 可能紀錄很多資訊只留下 prompt、*_score、precision，方便讀檔的時候知道從哪個 iteration 開始變化
    Var
        pair: dict
            dict formation:
            {
                "prompt": str,
                "train_score": int,
                "dev_score": int,
            }
    
    Return: dict
        {
            "prompt": str,          (required)
            "train_score": int,     (required)
            "dev_score": int,       (required)
            "preicision": {         (optional)
                "train": float,
                "dev": float
            }
        }
    """
    pair = deepcopy(pair)

    if pair is str:
        refined_pair = pair
    else:
        refined_pair = {
            "prompt": pair['prompt'],
            "train_score": pair['train_score'],
            # "dev_score": pair['dev_score'],
            }

        if "precision" in pair:
            refined_pair["precision"] = pair["precision"]

    return refined_pair

def refine_population(population):
    """ refine the population
    Var
        population: list[dict]
            list of pair, each pair is a dict
            dict formation:
            {
                "prompt": str,
                "train_score": int,
                "dev_score": int,
            }
    """
    population = deepcopy(population)
    population_refine = [
        refine_pair(pair)
        for pair in population
    ]
    return population_refine

def get_unique_path(path):
    path = Path(path)
    path_new = path
    idx = 0
    while path_new.exists():
        idx += 1
        path_new = path.with_name(f"{path.stem}_{idx:>03}{path.suffix}")
    return path_new

def save_pair(pair_new, folder_experiment_temp):
    """ save the pair_new
    """
    t = time_now()
    path_pair = folder_experiment_temp / f"{t}.json"
    path_pair = get_unique_path(path_pair)
    with open(path_pair, "w", encoding='utf-8') as f:
        json.dump(pair_new, f, ensure_ascii=False, indent=4)
    
    return path_pair