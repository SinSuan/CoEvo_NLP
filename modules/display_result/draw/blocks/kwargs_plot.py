
from modules.utils.get_config import get_config
CONFIG = get_config()
DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]

SWITCH_COLOR = {
    'CoEvoDE': "orange",
    'CoEvoDE_rand': "limegreen",
    'EvoDE': "indianred",
    'EvoGA': "blue"
}

SWITCH_MARKER = {
    'CoEvoDE': "o",
    'CoEvoDE_rand': "^",
    'EvoDE': "*",
    'EvoGA': "X"
}

def set_color(name_evolver):
    if DEBUGGER=="True": print("enter set_color")

    if "concat" in name_evolver:
        color = "blue"
    elif "remain" in name_evolver:
        color = "orange"
    elif "replace" in name_evolver:
        color = "green"
    else:
        message = f"Unknown evolver: {name_evolver}"
        raise ValueError(message)

    if DEBUGGER=="True": print("leave set_color")
    return color

def set_marker(name_evolver):
    if "random" in name_evolver:
        marker = "."
    elif "shift" in name_evolver:
        marker = "^"
    else:
        message = f"Unknown evolver: {name_evolver}"
        raise ValueError(message)

    return marker

def set_line_style(name_evolver):
    if "noCommonPart" in name_evolver:
        linestyle = "-"
    elif "noMutateDiff" in name_evolver:
        linestyle = "-"
    elif "full" in name_evolver:
        linestyle = "--"
    else:
        message = f"Unknown evolver: {name_evolver}"
        raise ValueError(message)
    return linestyle

def set_alpha(name_evolver):
    if "noCommonPart" in name_evolver:
        alpha = 1
    elif "noMutateDiff" in name_evolver:
        alpha = 0.2
    elif "full" in name_evolver:
        alpha = 1
    else:
        message = f"Unknown evolver: {name_evolver}"
        raise ValueError(message)
    return alpha
