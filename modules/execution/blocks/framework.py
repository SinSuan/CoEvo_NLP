"""
主要是為了 experiment 設計的，
只是因為也可以用在 initial_population、create_population_contr，所以命名比較通用。
"""

import json
from pathlib import Path

import ray
from modules.evolution.evolvers import Evolver
from modules.execution.blocks.terminator import Terminator
from modules.execution.blocks.utils import time_now
from modules.utils.get_config import get_folder_project


class Framework:
    def __init__(self, tag_experiment:str, evolver:Evolver, terminator: Terminator):
        """
        Var
            tag_experiment: str
                {name_experiment}/{date_time_strategy}
                or just {name_experiment}
            evolver: Evolver
            terminator: Termination

        Attribute
            folder_experiment
            evolver
            terminator
        """
        # 設定實驗資料夾
        folder_project = get_folder_project()
        folder_experiment = Path(f"{folder_project}/data/record/{tag_experiment}")
        folder_experiment.mkdir(parents=True, exist_ok=False)   # 避免覆蓋之前的實驗
        self.folder_experiment = folder_experiment

        self.evolver = evolver
        self.terminator = terminator
    
    def save_iteration(self):
        """ save result of experiment
        """
        # sub_judge = self.evolver.judge.ttl_sub_judge[0]
        # llm_judge = ray.get(sub_judge.get_llm.remote())
        # full_name_model_judge = llm_judge.full_name_model
        # 整理資料
        original_population = {
            "parent": self.evolver.strategy.population,
        }
        if hasattr(self.evolver.strategy, "population_contr"):
            original_population["contrastive"] = self.evolver.strategy.population_contr
        metadata_iteration = {
            "information": {
                "corpus": {
                    "evolver": self.evolver.strategy.tag_task,
                    "judge": self.evolver.judge.information_task.tag_task
                },
                "type_llm": {
                    "evolver": self.evolver.llm.full_name_model,
                    "judge": self.evolver.judge.llm.full_name_model
                    # "judge": self.evolver.judge.ttl_sub_judge[0].llm.full_name_model
                    # "judge": full_name_model_judge
                },
                "type_embedding": None,
                "original_population": original_population
            },
            "result": {
                "pair_best": self.evolver.strategy.population[0],
                "population": self.evolver.strategy.population
            }
        }

        # 製作儲存路徑
        idx_iteration = self.terminator.idx_iteration
        t = time_now()
        filename_iteration = f"{idx_iteration:>03d}_{t}"
        path_iteration = self.folder_experiment / f"{filename_iteration}.json"

        # 儲存
        with open(path_iteration, "w", encoding='utf-8') as f:
            json.dump(metadata_iteration, f, ensure_ascii=False, indent=4)

        return metadata_iteration, path_iteration

    def run(self):
        """ run experiment
        """
        # 先儲存初始狀態
        metadata_iteration, path_iteration = self.save_iteration()
        self.terminator.idx_iteration += 1
        
        pair_best = metadata_iteration["result"]["pair_best"]

        if type(pair_best) is dict:
            score_best = pair_best["train_score"]
        elif type(pair_best) is str:
            score_best = 0
        else:
            print(f"{pair_best=}")
            raise TypeError("pair_best is not dict or list")

        # 開始進化
        while self.terminator.is_terminated(score_best) is False:
            # 進行一次演化
            self.evolver.evolve_population()

            # 儲存結果
            metadata_iteration, path_iteration = self.save_iteration()
            self.terminator.idx_iteration += 1
            score_best = metadata_iteration["result"]["pair_best"]["train_score"]

            # print(f"{self.terminator.idx_iteration=}\t{len(self.evolver.strategy.population)=}")

        return path_iteration
