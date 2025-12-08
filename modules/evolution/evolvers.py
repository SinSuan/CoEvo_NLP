"""
正常情況下使用 Evolver，
只有要製作 population_contr 時才用 EvolverContrGA
"""

import json
from pathlib import Path
from typing import Union
from modules.evolution.blocks.call_model.vllm.llm import vLLM
from modules.evolution.blocks.judgement.judge_vllm import Judge_vLLM
from modules.evolution.blocks.create_unique_prompt import create_unique_prompt
# from modules.evolution.blocks.call_model.llm import CallTGI, NoneTGI
from modules.evolution.blocks.call_model.local.llm import LLM, NoneLLM
from modules.evolution.blocks.judgement.judge import Judge
from modules.evolution.blocks.strategy.strategy_factory.ref import StrategyExample
from modules.evolution.utils import refine_population, save_pair
from modules.execution.blocks.utils import time_now
from modules.utils.get_config import get_folder_project


class Evolver:
    def __init__(
        self,
        llm: Union[LLM, vLLM],
        judge: Union[Judge, Judge_vLLM],
        strategy: StrategyExample,
        type_strategy: str
    ):
        self.llm = llm
        self.judge = judge
        self.strategy = strategy

        polder_project = get_folder_project()
        t = time_now()
        type_task, name_task = self.strategy.tag_task.split("/")
        folder_experiment_temp = Path(f"{polder_project}/data/record/temporary/{type_task}/{t}_{name_task}_{type_strategy}")
        # folder_experiment_temp = Path(f"{polder_project}/data/record/temporary/{self.strategy.tag_task}_{t}")
        folder_experiment_temp.mkdir(parents=True, exist_ok=False)   # 避免覆蓋之前的實驗
        self.folder_experiment_temp = folder_experiment_temp

    def prepare_evolve(self, *ttl_idx):
        """ create the prompt for creating the os prompt
        Var:
            ttl_idx: list[int]
                int(s) for the index of the prompt
                為了保持一致性又要配合 EvolverContrGA，所以用 * 傳進來
        """
        ttl_parent_pair = self.strategy.select_ttl_parent(*ttl_idx)
        ttl_parent_prompt_only = {
            key: pair["prompt"]
            for key, pair in ttl_parent_pair.items()
        }
        # prompt_4_create_os_prompt = self.strategy.template.format(**ttl_parent_prompt_only)
        prompt_4_create_os_prompt = self.strategy.create_message(**ttl_parent_prompt_only)

        return ttl_parent_pair, prompt_4_create_os_prompt

    def evolve_pair(self, ttl_idx, population_temp):
        """ 用來進行進化
        Var
            ttl_idx: list[int]
                為了保持一致性又要配合 EvolverContrGA，所以用 * 傳給 prepare_evolve()
    
            ttl_parent: list[dict]
                dict formation:
                {
                    "prompt": str,
                    "train_score": float,
                    "dev_score": float
                }
        """

        # 製作進化的指令
        ttl_parent_pair, prompt_4_create_os_prompt = self.prepare_evolve(*ttl_idx)

        # 進化
        ttl_pair_exist = population_temp + self.strategy.get_population_all()
        # print(f"{len(population_temp)=}\n{len(self.strategy.population)=}\n{len(self.strategy.population_contr)=}")
        os_prompt_new, reply = create_unique_prompt(ttl_pair_exist, prompt_4_create_os_prompt, self.llm)

        # create info
        # ttl_parent_pair_refined = {
        #     key: pair
        #     for key, pair in ttl_parent_pair.items()
        # }
        info = {
            # "parent": ttl_parent_pair_refined,
            "parent": ttl_parent_pair,
            "generation":{
                "instruction": prompt_4_create_os_prompt,
                "reply": reply
            }
        }
        if os_prompt_new is None:
            print("in Evolver.evolve_pair")
            print(f"【進化失敗】\n{info=}")
            raise Exception("can't generate unique prompt")
        else:
            # 加上進化資訊
            pair_new = self.judge.get_result(os_prompt_new, num_shot=3)
            pair_new["info"] = info

        # 存檔
        save_pair(pair_new, self.folder_experiment_temp)

        return pair_new

    def evolve_population(self):
        """ main function of this class
        """
        self.strategy.population = refine_population(self.strategy.population)

        size_population = len(self.strategy.population)
        population_temp = []
        for i in range(size_population):
            pair_new = self.evolve_pair([i], population_temp)
            if pair_new is not None:
                population_temp.append(pair_new)

        population_new = self.strategy.update_population(population_temp)
        return population_new


class EvolverContrGA(Evolver):
    """ 專門給 create population_contr 的 evolver，僅覆寫 evolve_population
    """
    def __init__(
        self,
        llm: Union[LLM, vLLM],
        judge: Union[Judge, Judge_vLLM],
        strategy: StrategyExample
    ):
        self.llm = llm
        self.judge = judge
        self.strategy = strategy

        polder_project = get_folder_project()
        t = time_now()
        type_task, name_task = self.strategy.tag_task.split("/")
        folder_experiment_temp = Path(f"{polder_project}/data/record/temporary/{type_task}/{t}_{name_task}_contr")
        # folder_experiment_temp = Path(f"{polder_project}/data/record/temporary/{self.strategy.tag_task}_{t}")
        folder_experiment_temp.mkdir(parents=True, exist_ok=False)   # 避免覆蓋之前的實驗
        self.folder_experiment_temp = folder_experiment_temp

    def evolve_population(self):
        """ main function of this class
        """
        # 其實不用 refine population，因為只會做一個 iteration，而 population 的 __init__ 做過了
        self.strategy.population = refine_population(self.strategy.population)

        size_population = len(self.strategy.population)
        population_temp = []
        for i in range(size_population-1):
            for j in range(i+1, size_population):
                pair_new = self.evolve_pair([i,j], population_temp)
                population_temp.append(pair_new)

        population_new = self.strategy.update_population(population_temp)
        return population_new


class EvolverOPRO(Evolver):
    def evolve_population(self):
        """ main function of this class
        """
        self.strategy.population = refine_population(self.strategy.population)

        population_temp = []
        for _ in range(8):
            pair_new = self.evolve_pair([None], population_temp)
            if pair_new is not None:
                population_temp.append(pair_new)

        population_new = self.strategy.update_population(population_temp)
        return population_new


class EvolverInitial:
    """ no evolving
    為了配合 modules/execution/blocks/initialization.py 中 Framework 的寫法
    """
    def __init__(
        self,
        judge: Judge,
        strategy: StrategyExample
    ):
        self.llm = NoneLLM  # 因為這行，所以不能直接繼承 Evolver.__init__
        self.judge = judge
        self.strategy = strategy

        polder_project = get_folder_project()
        t = time_now()
        type_task, name_task = self.strategy.tag_task.split("/")
        folder_experiment_temp = Path(f"{polder_project}/data/record/temporary/{type_task}/{t}_{name_task}_init")
        folder_experiment_temp.mkdir(parents=True, exist_ok=False)   # 避免覆蓋之前的實驗
        self.folder_experiment_temp = folder_experiment_temp

    def evolve_population(self):
        """ main function of this class
        """
        # 不用 refine，因為一開始都是最簡單的 string

        population_temp = []
        for os_prompt in self.strategy.population:
            pair_new = self.judge.get_result(os_prompt, num_shot=3)
            save_pair(pair_new, self.folder_experiment_temp)

            population_temp.append(pair_new)

        population_new = self.strategy.update_population(population_temp)
        return population_new
