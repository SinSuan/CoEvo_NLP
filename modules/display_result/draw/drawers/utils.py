from typing import List
from modules.utils.tools import list_direct_files

from modules.utils.get_config import get_config
CONFIG = get_config()
DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]

def list_evolvers_tasks(folder_experiment:str, name_model:str) -> List[str]:
    if DEBUGGER=="True": print("enter list_evolvers_tasks")

    # get ttl_name_task
    _, ttl_folder_task = list_direct_files(folder_experiment)
    # print(f"{ttl_folder_task=}")
    # task_0 = ttl_folder_task[0] # for getting ttl_name_evolver
    ttl_name_task = [folder_task.stem for folder_task in ttl_folder_task]
    ttl_name_task = [name_task for name_task in ttl_name_task if "zzz" not in name_task]

    # get ttl_name_evolver
    # _, ttl_folder_model = list_direct_files(task_0)
    _, ttl_folder_evolver = list_direct_files(f"{ttl_folder_task[0]}/{name_model}")
    ttl_name_evolver = [folder_evolver.stem for folder_evolver in ttl_folder_evolver]

    # ttl_name_evolver = [
    #     name_evolver for name_evolver in ttl_name_evolver
    #     if len(name_evolver.split("_"))==5
    # ]
    # ttl_name_evolver = [
    #     # 'CoEvoDE_noCommonPart_random_concat',
    #     'CoEvoDE_noCommonPart_random_remain',
    #     # 'CoEvoDE_noCommonPart_random_replace',
    #     # 'CoEvoDE_noCommonPart_shift_concat',
    #     # 'CoEvoDE_noCommonPart_shift_remain',
    #     # 'CoEvoDE_noCommonPart_shift_replace',
    #     # 'CoEvoDE_noMutateDiff_random_concat',
    #     'CoEvoDE_noMutateDiff_random_remain',
    #     # 'CoEvoDE_noMutateDiff_random_replace',
    #     # 'CoEvoDE_noMutateDiff_shift_concat',
    #     # 'CoEvoDE_noMutateDiff_shift_remain',
    #     # 'CoEvoDE_noMutateDiff_shift_replace'
    # ]

    # ttl_name_task = ["hyperbaton"]
    # ttl_name_evolver = ["CoEvoDE_noCommonPart_random_replace"]

    if DEBUGGER=="True": print("leave list_evolvers_tasks")
    return ttl_name_task, ttl_name_evolver
