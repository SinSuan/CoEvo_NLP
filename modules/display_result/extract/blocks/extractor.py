import json

from modules.display_result.extract.blocks.list_task_variant import get_switch_ttl_name_variant
from modules.utils.get_config import get_folder_project
from modules.utils.tools import list_direct_files

def extract_by_round(folder_ttl_round, extractor:callable):
    print(f"{folder_ttl_round=}")
    _, ttl_folder_round = list_direct_files(folder_ttl_round)
    ttl_round = []
    for folder_round in ttl_folder_round:
        ttl_target_iteration = extractor(folder_round)
        if ttl_target_iteration is not None:
            ttl_round.append(ttl_target_iteration)
    return ttl_round

def extract_by_variant(folder_ttl_variant, extractor:callable):
    print(f"{folder_ttl_variant=}")
    switch_ttl_name_variant = get_switch_ttl_name_variant()
    ttl_precision_variant = {}

    for variant in switch_ttl_name_variant:
        folder_variant = folder_ttl_variant / variant
        ttl_precision_round = extract_by_round(folder_variant, extractor)
        ttl_precision_variant[variant] = ttl_precision_round

    return ttl_precision_variant

def get_result(path_result, extractor:callable):
    folder_project = get_folder_project()
    folder_experiment = f"{folder_project}/data/record/experiment_draw/bbh"

    # ttl_task = get_switch_ttl_name_task()
    # result_merged = {
    #     task: {"google/gemma-3-1b-it": {}}
    #     for task in ttl_task
    # }
    _, ttl_task = list_direct_files(folder_experiment)
    ttl_task = [ _task for _task in ttl_task if "zzz" not in str(_task) ]
    result_merged = {
        name_task: {"google/gemma-3-1b-it": {}}
        for name_task in [task.stem for task in ttl_task]
    }

    for task in ttl_task:
        name_task = task.stem
        print(f"{task=}")
        folder_task = task/"google/gemma-3-1b-it"
        result_merged[name_task]["google/gemma-3-1b-it"] = extract_by_variant(folder_task, extractor)

    # folder_result = f"{folder_experiment}/zzzz_result_merged"
    # path_result = f"{folder_result}/result_merged_2025_0710_1726_all.json"

    with open(path_result, 'w', encoding="utf-8") as f:
        json.dump(result_merged, f, indent=4, ensure_ascii=False)
