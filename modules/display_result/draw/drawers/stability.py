import re
from typing import List
import numpy as np
import matplotlib.pyplot as plt
from modules.display_result.draw.blocks.draw import draw_single_result, draw_label
from modules.display_result.draw.drawers.utils import list_evolvers_tasks
# from modules.draw_result.blocks.load_data import list_evolvers_tasks

from modules.utils.get_config import get_config
CONFIG = get_config()
DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]

def bound_with_mean_std(ttl_round:List[List[float]]) -> List[float]:
    ttl_round = np.array(ttl_round)
    mean = np.mean(ttl_round, axis=0)
    std = np.std(ttl_round, axis=0)

    lb = mean - std
    ub = mean + std
    return lb, ub

def drawer_stability_experiment(folder_experiment:str, name_model:str, invariants:list):
    if DEBUGGER=="True": print("enter drawer_stability_experiment")
    print(f"{folder_experiment=}\n{name_model=}")

    ttl_name_task, ttl_name_evolver = list_evolvers_tasks(folder_experiment, name_model)
    print(f"{ttl_name_evolver=}")

    # 使用正則表達式過濾
    a, b = invariants
    pattern = re.compile(fr'.*{a}.*{b}.*')
    ttl_name_evolver = [name_evolver for name_evolver in ttl_name_evolver if pattern.match(name_evolver)]
    print(f"{ttl_name_evolver=}")
    # num_ax = len(ttl_name_task)
    num_ax = len(ttl_name_task) + 1 # +1 for the display the labels only

    ncols = round(np.sqrt(num_ax))
    # nrows = num_ax//ncols + 1
    nrows = np.ceil(float(num_ax)/ncols)
    nrows = int(nrows)
    # print(f"{num_ax=}\n{ncols=}\n{nrows=}\n")

    fig, axes = plt.subplots(nrows, ncols, figsize=(ncols*4, nrows*2), constrained_layout=True)
    print(f"{axes.shape=}")
    axes = axes.flatten()   # for-loop 內 idx 的處理可以比較 general
    # fig.set_size_inches(20, 10)
    fig.suptitle(name_model, fontsize=16)

    # draw results
    for idx, name_task in enumerate(ttl_name_task):
        # print(f"{type(axes[idx])=}")
        # ax = axes[idx // 4, idx % 4]
        ax = axes[idx]
        ax.set_title(name_task)
        ax.set_xticks(range(0,21))
        for name_evolver in ttl_name_evolver:
            # print(f"{name_task=}")
            # print(f"{name_evolver=}")
            draw_single_result(
                ax=ax,
                folder_experiment=folder_experiment,
                name_task=name_task,
                name_model=name_model,
                name_evolver=name_evolver,
                find_lb_ub=bound_with_mean_std
            )

    # the last ax is used to display the labels only
    # print(f"{type(axes[-1])=}")
    ax = axes[-1]
    for name_evolver in ttl_name_evolver:
        draw_label(
            ax=ax,
            name_evolver=name_evolver
        )
    plt.close(fig)
    if DEBUGGER=="True": print("leave drawer_stability_experiment")
    return fig
