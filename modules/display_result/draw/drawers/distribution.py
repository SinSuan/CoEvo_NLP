from typing import List
from matplotlib import pyplot as plt
import numpy as np
from modules.display_result.draw.blocks.draw import draw_label, draw_single_result
from modules.display_result.draw.drawers.utils import list_evolvers_tasks
# from modules.draw_result.blocks.load_data import list_evolvers_tasks

def bound_by_min_max(ttl_round:List[List[float]]) -> List[float]:
    """
    Return
        lb < ub
    """
    ttl_round = np.array(ttl_round)
    _min = np.min(ttl_round, axis=0)
    _max = np.max(ttl_round, axis=0)

    lb = _min
    ub = _max
    return lb, ub

def drawer_distribution_population(folder_experiment:str, name_model:str):
    ttl_name_task, ttl_name_evolver = list_evolvers_tasks(folder_experiment, name_model)

    ncols = len(ttl_name_task)
    nrows = len(ttl_name_evolver) + 1 # +1 for the display the labels only

    fig, axes = plt.subplots(nrows, ncols, figsize=(ncols*5, nrows*3), constrained_layout=True)
    fig.suptitle(name_model, fontsize=16)
    for idx_task, name_task in enumerate(ttl_name_task):
        for idx_evolver, name_evolver in enumerate(ttl_name_evolver):
            ax = axes[idx_evolver, idx_task]
            ax.set_title(name_task)
            ax.set_xticks(range(0,21))
            draw_single_result(
                ax=ax,
                folder_experiment=folder_experiment,
                name_task=name_task,
                name_model=name_model,
                name_evolver=name_evolver,
                find_lb_ub=bound_by_min_max
            )
    # the last ax is used to display the labels only
    ax = axes[-1][-1]
    for name_evolver in ttl_name_evolver:
        draw_label(
            ax=ax,
            name_evolver=name_evolver
        )

    return fig
