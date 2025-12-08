import json
from typing import List

from modules.utils.get_config import get_folder_project
from modules.utils.tools import list_direct_files

from modules.utils.get_config import get_config
CONFIG = get_config()
# DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]
DEBUGGER = "False"

# def list_evolvers_tasks(folder_experiment:str) -> List[str]:
#     if DEBUGGER=="True": print("enter list_evolvers_tasks")

#     # get ttl_name_task
#     _, ttl_folder_task = list_direct_files(folder_experiment)
#     task_0 = ttl_folder_task[0] # for getting ttl_name_evolver
#     ttl_name_task = [folder_task.stem for folder_task in ttl_folder_task]

#     # get ttl_name_evolver
#     _, ttl_folder_model = list_direct_files(task_0)
#     _, ttl_folder_evolver = list_direct_files(ttl_folder_model[0])
#     ttl_name_evolver = [folder_evolver.stem for folder_evolver in ttl_folder_evolver]

#     if DEBUGGER=="True": print("leave list_evolvers_tasks")
#     return ttl_name_task, ttl_name_evolver

def extract_precision(ttl_path_iteration:List[str]) -> List[float]:
    if DEBUGGER=="True": print("enter extract_precision")

    _round = []
    for path_iteration in ttl_path_iteration:
        with open(path_iteration, 'r', encoding='utf-8') as f:
            iteration = json.load(f)
        precision_best = iteration["result"]["pair_best"]["precision"]["train"]
        _round.append(precision_best)

    if DEBUGGER=="True": print("leave extract_precision")
    return _round

def load_precision_from_experiment(folder_experiment:str, name_task:str, name_model:str, name_evolver:str) -> List[List[float]]:
    if DEBUGGER=="True": print("enter load_precision")

    folder_desired = f"{folder_experiment}/{name_task}/{name_model}/{name_evolver}"
    _, ttl_path_round = list_direct_files(folder_desired)

    ttl_round = []
    for path_round in ttl_path_round:
        ttl_path_iteration, _ = list_direct_files(path_round)
        print(f"{len(ttl_path_iteration)=}\t{ttl_path_iteration=}")
        if len(ttl_path_iteration) == 21:
            _round = extract_precision(ttl_path_iteration)
            ttl_round.append(_round)

    if DEBUGGER=="True": print("leave load_precision")
    return ttl_round


FOLDER_PROJECT = get_folder_project()
PATH_RESULT_MERGED = f"{FOLDER_PROJECT}/data/record/experiment_draw/bbh/result_merged.json"
with open(PATH_RESULT_MERGED, 'r', encoding='utf-8') as f:
    RESULT_MERGED = json.load(f)
def load_precision(folder_experiment:str, name_task:str, name_model:str, name_evolver:str) -> List[List[float]]:
    # print(f"{folder_experiment=}\n{name_task=}\n{name_model=}\n{name_evolver=}\n")
    ttl_round = RESULT_MERGED[name_task][name_model][name_evolver]
    return ttl_round
