from typing import List

import numpy as np

from modules.display_result.extract.blocks.list_task_variant import get_switch_ttl_name_task, get_switch_ttl_name_variant

# from modules.display_result.extract.blocks.extractor import get_switch_ttl_name_task, get_switch_ttl_name_variant


def record_2_average_result(ttl_round:List[List[float]]) -> float:
    """
    Var:
        ttl_round: List[List[float]]
            [
                [round 1],
                ...
            ]

    Return:
        average_performance: float
    """
    ttl_round = np.array(ttl_round)
    # print(f"{ttl_round=}")
    average_round = np.mean(ttl_round, axis=0)
    average_result = average_round[-1]
    return average_result


def get_data_for_latex(result_merged:dict):
    """
    Var:
        result_merged: dict
            {
                "task_1": {
                    "model_1": {
                        "evolver_1": [
                            [round 1],
                            ...
                        ],
                        "evolver_2": ...
                    }
                    "model_2": ...
                },
                "task_2": ...
            }

    Return:
        data: dict
            {
                model_1: {
                    evolver_1: {
                        task_1: score_1-1-1,
                        task_2: score_1-1-2,
                        task_3: ...
                    },
                    evolver_2: ...
                },
                model_2: ...
            }
    """
    ttl_task = list(result_merged.keys())
    ttl_model = list(result_merged[ttl_task[0]].keys())
    ttl_evolver = list(result_merged[ttl_task[0]][ttl_model[0]].keys())

    data = {}
    for model in ttl_model:
        # print(f"{model=}")
        data_model = {}
        for evolver in ttl_evolver:
            # print(f"\t{evolver=}")
            data_evolver = {}
            for task in ttl_task:
                # print(f"\t\t{task=}")
                ttl_round = result_merged[task][model][evolver]
                average_result = record_2_average_result(ttl_round)
                data_evolver[task] = average_result
            data_model[evolver] = data_evolver
        data[model] = data_model

    return data

def create_abbr(name, concat_symbol):
    ttl_token = name.split(concat_symbol)
    abbr_name = ""
    for token in ttl_token:
        abbr_name += token[0]
    return abbr_name

SWITCH_TTL_TASK = get_switch_ttl_name_task()
SWITCH_TTL_VARIANT = get_switch_ttl_name_variant()
def construct_rows(data:dict) -> str:
    """
    Var:
        data: dict
            {
                model_1: {
                    evolver_1: {
                        task_1: score_1-1-1,
                        task_2: score_1-1-2,
                        task_3: ...
                    },
                    evolver_2: ...
                },
                model_2: ...
            }

    Return:
        latex_table: str
    """

    # display(SWITCH_TTL_VARIANT)

    ttl_row = {}

    # 欄位名稱
    for model, data_model in list(data.items())[:1]:
        for evolver, data_evolver in list(data_model.items())[:1]:
            row = ""
            for task, score in data_evolver.items():
                task_old = task
                # task = create_abbr(name=task, concat_symbol="_")
                task = SWITCH_TTL_TASK[task]
                # print(f"{task_old} ({task})")

                # 因為 markdown 格式會用到大括號，如果再用 f-string 會很亂
                row += r" & \multicolumn{1}{c}{\textbf{<<task>>}}"
                row = row.replace("<<task>>", task)
            row += "\\\\ \n"
        ttl_row["name_col"] = row

    # 數據
    # len_pre = len("CoEvoDE_")
    for model, data_model in data.items():
        ttl_evolver = {}
        for evolver, data_evolver in data_model.items():
            # evolver = evolver[len_pre:].replace("_", r"\_")
            evolver = SWITCH_TTL_VARIANT[evolver].replace("_", r"\_")
            row = ""
            for task, score in data_evolver.items():
                # score = int(score * 100)
                # row += f" & {score:>2d}"
                score = round(score * 100, 1)
                row += f" & {score:>3.1f}"
            row += "\\\\ \n"
            ttl_evolver[evolver] = row
        ttl_row[model] = ttl_evolver

    return ttl_row

def construct_latex_table(ttl_row:dict, model_name:str) -> str:
    template_latex_table = \
r"""
\begin{tabular}{<<column_alignment>>}
    \Xhline{3\arrayrulewidth}
    <<data>>
    \Xhline{3\arrayrulewidth}
\end{tabular}
"""

    divider = r"\hline" + "\n"

    # init
    data = f"\t{ttl_row['name_col']}"   # 以欄位名稱起頭
    num_col = len(data.split(" & "))
    column_alignment = "l" + "r" * (num_col-1)    # 數值全部靠右
    ttl_row.pop("name_col")  # 移除欄位名稱

    data_model = ttl_row[model_name]
    for evolver, scores in data_model.items():
        row = f"{evolver}\t{scores}"
        data += row + divider
    data = data[:-len(divider)]  # remove last divider

    latex_table = template_latex_table.replace("<<column_alignment>>", column_alignment)
    latex_table = latex_table.replace("<<data>>", data)

    return latex_table

def result_2_latex_table(result_merged:dict, model_name:str) -> str:
    data = get_data_for_latex(result_merged)
    ttl_row = construct_rows(data)
    latex_table = construct_latex_table(ttl_row, model_name)
    return latex_table
