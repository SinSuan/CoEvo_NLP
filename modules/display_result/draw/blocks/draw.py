from typing import Callable
import numpy as np

from modules.utils.get_config import get_config
CONFIG = get_config()
DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]

from modules.display_result.draw.blocks.kwargs_plot import (
    # SWITCH_COLOR,
    # SWITCH_MARKER,
    set_color,
    set_marker,
    set_line_style,
    set_alpha
)
from modules.display_result.draw.blocks.load_data import load_precision


def draw(ax:np.ndarray, x, y, lb, ub, **kwargs_plot):
    """
    Var:
        lb: lower bound
        ub: upper bound
    """
    if DEBUGGER=="True": print("enter draw")

    # kwargs_plot.pop('label', None)
    ax.plot(x, y, **kwargs_plot)
    kwargs_plot.pop('linestyle', None)
    kwargs_plot["s"]=10
    ax.scatter(x, y, **kwargs_plot)
    # ax.fill_between(x, lb, ub, alpha=0.2, color=kwargs_plot["color"])
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Precision")
    # ax.legend(fontsize=4)

    if DEBUGGER=="True": print("leave draw")

def draw_single_result(
        ax:np.ndarray,
        folder_experiment:str,
        name_task:str,
        name_model:str,
        name_evolver:str,
        find_lb_ub:Callable
    ):
    if DEBUGGER=="True": print("enter draw_single_result")

    ttl_round = load_precision(
        folder_experiment=folder_experiment,
        name_task=name_task,
        name_model=name_model,
        name_evolver=name_evolver
    )
    if ttl_round is not None:
        # print(f"\t{ttl_round=}\n")
        kwargs_plot = {
            # 'color': SWITCH_COLOR[name_evolver],
            # 'marker': SWITCH_MARKER[name_evolver],
            'color': set_color(name_evolver),
            'marker': set_marker(name_evolver),
            # 'label': name_evolver,
            'linestyle': set_line_style(name_evolver),
            'alpha': set_alpha(name_evolver)
        }
        lb, ub = find_lb_ub(ttl_round)
        y = np.mean(ttl_round, axis=0)
        x = np.arange(len(y))
        draw(ax, x, y, lb, ub, **kwargs_plot)

    if DEBUGGER=="True": print("leave draw_single_result")

def draw_label(ax:np.ndarray, name_evolver:str):
    if DEBUGGER=="True": print("enter draw_label")

    kwargs_plot = {
        # 'color': SWITCH_COLOR[name_evolver],
        # 'marker': SWITCH_MARKER[name_evolver],
        'color': set_color(name_evolver),
        'marker': set_marker(name_evolver),
        # 'label': name_evolver,
        # 'linestyle': set_line_style(name_evolver),
        'alpha': set_alpha(name_evolver)
    }
    ax.plot([], [], **kwargs_plot, label=name_evolver)
    ax.legend()

    if DEBUGGER=="True": print("leave draw_label")
