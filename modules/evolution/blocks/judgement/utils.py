import ray

# from modules.evolution.blocks.judgement.judge import SubJudge

from modules.utils.get_config import get_config
CONFIG = get_config()
DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]

@ray.remote
def ray_sub_judge(sub_judge, os_prompt:str, num_shot:int):
    if DEBUGGER=="True": print(f"enter ray_sub_judge")
    if DEBUGGER=="True": print(f"leave ray_sub_judge")
    return sub_judge.judge(os_prompt, sub_judge.information_task.dataset["train_split"], num_shot)
