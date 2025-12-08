import argparse

import numpy as np
import ray
import torch

# from modules.evolution.blocks.call_model.llm import CallTGI
from modules.evolution.blocks.call_model.local.llm import LLM
from modules.evolution.blocks.call_model.vllm.llm import vLLM
from modules.evolution.blocks.judgement.judge import Judge
from modules.evolution.blocks.judgement.judge_vllm import Judge_vLLM
from modules.evolution.blocks.judgement.task_informations.bbh.information_bbh import InformationBBH

from modules.evolution.blocks.strategy.strategy_factory.coevode.CoEvoDE_full import SWITCH_CoEvoDE_full
from modules.evolution.blocks.strategy.strategy_factory.coevode.CoEvoDE_noCommonPart import SWITCH_CoEvoDE_noCommonPart
from modules.evolution.blocks.strategy.strategy_factory.coevode.CoEvoDE_noMutateDiff import SWITCH_CoEvoDE_noMutateDiff
from modules.evolution.blocks.strategy.strategy_factory.ref import SWITCH_Ref
from modules.evolution.evolvers import Evolver, EvolverContrGA, EvolverInitial
from modules.execution.blocks.framework import Framework
from modules.execution.blocks.terminator import Terminator
from modules.execution.blocks.utils import load_model

from modules.utils.get_config import get_config
CONFIG = get_config()
DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]

class PreparerExperiment:
    """
    required:
        --task
        --full_name_model
        --gpu
        --strategy
        --target_score
        --target_itration
        --num_experiment
    """
    def __init__(self):
        """ get input from user
        """
        parser = argparse.ArgumentParser(description="For experiment.")

        # for strategy of evolver, information of judge
        parser.add_argument('--task', type=str, required=True, help="{name_task} ex: 'boolean_expressions' (in bbh)")
        parser.add_argument('--full_name_model', type=str, required=True, help="full_name_model for evolver")
        parser.add_argument('--gpu', type=str, required=True, help="list of the indices of GPUs used")

        # for framework

        # parser.add_argument('--strategy', type=str, required=True, choices=["EvoGA", "EvoDE", "CoEvoDE", "EvoGA,EvoDE,CoEvoDE"], help="ref: module/evolution/blocks/strategy/strategy_factory")
        parser.add_argument('--target_score', type=int, required=True)
        parser.add_argument('--target_itration', type=int, required=True)
        # parser.add_argument('--tag_experiment', type=str, required=True, help="under data/record/experiment/")
        parser.add_argument('--num_experiment', type=int, required=True, help="for compute standard deviation")
        parser.add_argument('--strategy', type=str, required=True, help="ref: module/evolution/blocks/strategy/strategy_factory")
        args = parser.parse_args()

        self.class_information = InformationBBH
        
        self.ttl_type_strategy = args.strategy.split(",")

        self.ttl_task = args.task.split(",")
        self.full_name_model = args.full_name_model
        self.gpu = args.gpu
        self.llm = vLLM(self.full_name_model, self.gpu)
        # self.ttl_gpu = [int(i) for i in args.gpu.split(",")]
        # ray.init(ignore_reinit_error=True, num_gpus=len(self.ttl_gpu))

        self.target_score = args.target_score
        self.target_itration = args.target_itration
        # self.tag_experiment = f"experiment/{args.tag_experiment}"
        self.num_experiment = args.num_experiment

    def prepare(self, idx_experiment):
        """ prepare the experiment
        """
        # create evolver
        # llm_evolver = self.llm
        # llm_evolver = LLM(self.full_name_model, self.ttl_gpu[0])

        # information = self.class_information(self.tag_task)
        # ttl_future = [
        #     load_model(self.full_name_model, gpu)
        #     for gpu in self.ttl_gpu
        # ]
        # ttl_llm_judge = ray.get(ttl_future)
        # judge = Judge(information, ttl_llm_judge)
        # llm_judge = LLM(self.full_name_model, self.ttl_gpu)
        # llm_judge = self.llm
        # judge = Judge_vLLM(information, llm_judge)

        switch_strategy = {
            **SWITCH_Ref,
            **SWITCH_CoEvoDE_full,
            **SWITCH_CoEvoDE_noMutateDiff,
            **SWITCH_CoEvoDE_noCommonPart
        }

        ttl_framework = []
        for type_strategy in self.ttl_type_strategy:
            for task in self.ttl_task:
                tag_task = f"bbh/{task}"
                class_strategy = switch_strategy[type_strategy]
                strategy = class_strategy(tag_task, self.full_name_model)

                # create judge
                information = self.class_information(tag_task)
                llm_judge = self.llm
                judge = Judge_vLLM(information, llm_judge)

                # create evolver
                llm_evolver = self.llm
                evolver = Evolver(llm_evolver, judge, strategy, type_strategy)

                # create framework
                tag_experiment_idx = f"experiment_topk_3_correct/{tag_task}/{self.full_name_model}/{type_strategy}/{idx_experiment:>03}"
                print(f"{tag_experiment_idx=}")
                terminator = Terminator(self.target_score, self.target_itration)
                framework = Framework(tag_experiment_idx, evolver, terminator)

                ttl_framework.append(framework)
        return ttl_framework


class PreparerExperiment2:
    """
    required:
        --task
        --full_name_model
        --gpu
        --strategy
        --target_score
        --target_itration
        --num_experiment
    """
    def __init__(self):
        """ get input from user
        """
        parser = argparse.ArgumentParser(description="For experiment.")

        # for strategy of evolver, information of judge
        parser.add_argument('--task', type=str, required=True, help="{name_task} ex: 'boolean_expressions' (in bbh)")
        parser.add_argument('--full_name_model', type=str, required=True, help="full_name_model for evolver")
        parser.add_argument('--gpu', type=str, required=True, help="list of the indices of GPUs used")

        # for framework

        # parser.add_argument('--strategy', type=str, required=True, choices=["EvoGA", "EvoDE", "CoEvoDE", "EvoGA,EvoDE,CoEvoDE"], help="ref: module/evolution/blocks/strategy/strategy_factory")
        parser.add_argument('--strategy', type=str, required=True, help="ref: module/evolution/blocks/strategy/strategy_factory")
        parser.add_argument('--target_score', type=int, required=True)
        parser.add_argument('--target_itration', type=int, required=True)
        # parser.add_argument('--tag_experiment', type=str, required=True, help="under data/record/experiment/")
        parser.add_argument('--num_experiment', type=int, required=True, help="for compute standard deviation")
        args = parser.parse_args()

        # type_task = args.tag_task.split("/")[0]
        # switch_information = {
        #     "bbh": InformationBBH
        # }
        # self.class_information = switch_information[type_task]
        self.class_information = InformationBBH

        self.ttl_type_strategy = args.strategy.split(",")

        self.ttl_task = args.task.split(",")
        self.full_name_model = args.full_name_model
        self.gpu = args.gpu
        self.llm = vLLM(self.full_name_model, self.gpu)
        # self.ttl_gpu = [int(i) for i in args.gpu.split(",")]
        # ray.init(ignore_reinit_error=True, num_gpus=len(self.ttl_gpu))

        self.target_score = args.target_score
        self.target_itration = args.target_itration
        # self.tag_experiment = f"experiment/{args.tag_experiment}"
        self.num_experiment = args.num_experiment

    def prepare(self, idx_experiment):
        """ prepare the experiment
        """
        # create evolver
        # llm_evolver = self.llm
        # llm_evolver = LLM(self.full_name_model, self.ttl_gpu[0])

        # information = self.class_information(self.tag_task)
        # ttl_future = [
        #     load_model(self.full_name_model, gpu)
        #     for gpu in self.ttl_gpu
        # ]
        # ttl_llm_judge = ray.get(ttl_future)
        # judge = Judge(information, ttl_llm_judge)
        # llm_judge = LLM(self.full_name_model, self.ttl_gpu)
        # llm_judge = self.llm
        # judge = Judge_vLLM(information, llm_judge)

        switch_strategy = {
            **SWITCH_Ref,
            **SWITCH_CoEvoDE_full,
            **SWITCH_CoEvoDE_noMutateDiff,
            **SWITCH_CoEvoDE_noCommonPart
        }

        ttl_framework = []
        for type_strategy in self.ttl_type_strategy:
            for task in self.ttl_task:
                tag_task = f"bbh/{task}"
                class_strategy = switch_strategy[type_strategy]
                strategy = class_strategy(tag_task, self.full_name_model)

                # create judge
                information = self.class_information(tag_task)
                llm_judge = self.llm
                judge = Judge_vLLM(information, llm_judge)
                
                # create evolver
                llm_evolver = self.llm
                evolver = Evolver(llm_evolver, judge, strategy, type_strategy)

                # create framework
                tag_experiment_idx = f"experiment_topk_2_correct/{tag_task}/{self.full_name_model}/{type_strategy}/{idx_experiment:>03}"
                print(f"{tag_experiment_idx=}")
                terminator = Terminator(self.target_score, self.target_itration)
                framework = Framework(tag_experiment_idx, evolver, terminator)

                ttl_framework.append(framework)
        return ttl_framework


class PreparerExperiment3:
    """
    required:
        --task
        --full_name_model
        --gpu
        --strategy
        --target_score
        --target_itration
        --num_experiment
    """
    def __init__(self):
        """ get input from user
        """
        parser = argparse.ArgumentParser(description="For experiment.")

        # for strategy of evolver, information of judge
        parser.add_argument('--task', type=str, required=True, help="{name_task} ex: 'boolean_expressions' (in bbh)")
        parser.add_argument('--full_name_model', type=str, required=True, help="full_name_model for evolver")
        parser.add_argument('--gpu', type=str, required=True, help="list of the indices of GPUs used")

        # for framework

        # parser.add_argument('--strategy', type=str, required=True, choices=["EvoGA", "EvoDE", "CoEvoDE", "EvoGA,EvoDE,CoEvoDE"], help="ref: module/evolution/blocks/strategy/strategy_factory")
        parser.add_argument('--strategy', type=str, required=True, help="ref: module/evolution/blocks/strategy/strategy_factory")
        parser.add_argument('--target_score', type=int, required=True)
        parser.add_argument('--target_itration', type=int, required=True)
        # parser.add_argument('--tag_experiment', type=str, required=True, help="under data/record/experiment/")
        parser.add_argument('--num_experiment', type=int, required=True, help="for compute standard deviation")
        args = parser.parse_args()

        # type_task = args.tag_task.split("/")[0]
        # switch_information = {
        #     "bbh": InformationBBH
        # }
        # self.class_information = switch_information[type_task]
        self.class_information = InformationBBH

        self.ttl_type_strategy = args.strategy.split(",")

        self.ttl_task = args.task.split(",")
        self.full_name_model = args.full_name_model
        self.gpu = args.gpu
        self.llm = vLLM(self.full_name_model, self.gpu)
        # self.ttl_gpu = [int(i) for i in args.gpu.split(",")]
        # ray.init(ignore_reinit_error=True, num_gpus=len(self.ttl_gpu))

        self.target_score = args.target_score
        self.target_itration = args.target_itration
        # self.tag_experiment = f"experiment/{args.tag_experiment}"
        self.num_experiment = args.num_experiment

    def prepare(self, idx_experiment):
        """ prepare the experiment
        """
        # create evolver
        # llm_evolver = self.llm
        # llm_evolver = LLM(self.full_name_model, self.ttl_gpu[0])

        # information = self.class_information(self.tag_task)
        # ttl_future = [
        #     load_model(self.full_name_model, gpu)
        #     for gpu in self.ttl_gpu
        # ]
        # ttl_llm_judge = ray.get(ttl_future)
        # judge = Judge(information, ttl_llm_judge)
        # llm_judge = LLM(self.full_name_model, self.ttl_gpu)
        # llm_judge = self.llm
        # judge = Judge_vLLM(information, llm_judge)

        switch_strategy = {
            **SWITCH_Ref,
            **SWITCH_CoEvoDE_full,
            **SWITCH_CoEvoDE_noMutateDiff,
            **SWITCH_CoEvoDE_noCommonPart
        }

        ttl_framework = []
        for type_strategy in self.ttl_type_strategy:
            for task in self.ttl_task:
                tag_task = f"bbh/{task}"
                class_strategy = switch_strategy[type_strategy]
                strategy = class_strategy(tag_task, self.full_name_model)

                # create judge
                information = self.class_information(tag_task)
                llm_judge = self.llm
                judge = Judge_vLLM(information, llm_judge)
                
                # create evolver
                llm_evolver = self.llm
                evolver = Evolver(llm_evolver, judge, strategy, type_strategy)

                # create framework
                tag_experiment_idx = f"experiment3/{tag_task}/{self.full_name_model}/{type_strategy}/{idx_experiment:>03}"
                print(f"{tag_experiment_idx=}")
                terminator = Terminator(self.target_score, self.target_itration)
                framework = Framework(tag_experiment_idx, evolver, terminator)

                ttl_framework.append(framework)
        return ttl_framework


class PreparerExperiment4:
    """
    required:
        --task
        --full_name_model
        --gpu
        --strategy
        --target_score
        --target_itration
        --num_experiment
    """
    def __init__(self):
        """ get input from user
        """
        parser = argparse.ArgumentParser(description="For experiment.")

        # for strategy of evolver, information of judge
        parser.add_argument('--task', type=str, required=True, help="{name_task} ex: 'boolean_expressions' (in bbh)")
        parser.add_argument('--full_name_model', type=str, required=True, help="full_name_model for evolver")
        parser.add_argument('--gpu', type=str, required=True, help="list of the indices of GPUs used")

        # for framework

        # parser.add_argument('--strategy', type=str, required=True, choices=["EvoGA", "EvoDE", "CoEvoDE", "EvoGA,EvoDE,CoEvoDE"], help="ref: module/evolution/blocks/strategy/strategy_factory")
        parser.add_argument('--strategy', type=str, required=True, help="ref: module/evolution/blocks/strategy/strategy_factory")
        parser.add_argument('--target_score', type=int, required=True)
        parser.add_argument('--target_itration', type=int, required=True)
        # parser.add_argument('--tag_experiment', type=str, required=True, help="under data/record/experiment/")
        parser.add_argument('--num_experiment', type=int, required=True, help="for compute standard deviation")
        args = parser.parse_args()

        # type_task = args.tag_task.split("/")[0]
        # switch_information = {
        #     "bbh": InformationBBH
        # }
        # self.class_information = switch_information[type_task]
        self.class_information = InformationBBH

        self.ttl_type_strategy = args.strategy.split(",")

        self.ttl_task = args.task.split(",")
        self.full_name_model = args.full_name_model
        self.gpu = args.gpu
        self.llm = vLLM(self.full_name_model, self.gpu)
        # self.ttl_gpu = [int(i) for i in args.gpu.split(",")]
        # ray.init(ignore_reinit_error=True, num_gpus=len(self.ttl_gpu))

        self.target_score = args.target_score
        self.target_itration = args.target_itration
        # self.tag_experiment = f"experiment/{args.tag_experiment}"
        self.num_experiment = args.num_experiment

    def prepare(self, idx_experiment):
        """ prepare the experiment
        """
        # create evolver
        # llm_evolver = self.llm
        # llm_evolver = LLM(self.full_name_model, self.ttl_gpu[0])

        # information = self.class_information(self.tag_task)
        # ttl_future = [
        #     load_model(self.full_name_model, gpu)
        #     for gpu in self.ttl_gpu
        # ]
        # ttl_llm_judge = ray.get(ttl_future)
        # judge = Judge(information, ttl_llm_judge)
        # llm_judge = LLM(self.full_name_model, self.ttl_gpu)
        # llm_judge = self.llm
        # judge = Judge_vLLM(information, llm_judge)

        switch_strategy = {
            **SWITCH_Ref,
            **SWITCH_CoEvoDE_full,
            **SWITCH_CoEvoDE_noMutateDiff,
            **SWITCH_CoEvoDE_noCommonPart
        }

        ttl_framework = []
        for type_strategy in self.ttl_type_strategy:
            for task in self.ttl_task:
                tag_task = f"bbh/{task}"
                class_strategy = switch_strategy[type_strategy]
                strategy = class_strategy(tag_task, self.full_name_model)

                # create judge
                information = self.class_information(tag_task)
                llm_judge = self.llm
                judge = Judge_vLLM(information, llm_judge)
                
                # create evolver
                llm_evolver = self.llm
                evolver = Evolver(llm_evolver, judge, strategy, type_strategy)

                # create framework
                tag_experiment_idx = f"experiment4/{tag_task}/{self.full_name_model}/{type_strategy}/{idx_experiment:>03}"
                print(f"{tag_experiment_idx=}")
                terminator = Terminator(self.target_score, self.target_itration)
                framework = Framework(tag_experiment_idx, evolver, terminator)

                ttl_framework.append(framework)
        return ttl_framework


class PreparerCreatePopulationContr:
    """
    required:
        --task
        --full_name_model
        --gpu
    """
    def __init__(self):
        """ get input from user
        """
        parser = argparse.ArgumentParser(description="For experiment.")

        # for strategy of evolver, information of judge
        parser.add_argument('--task', type=str, required=True, help="{name_task} ex: 'boolean_expressions' (in bbh)")
        parser.add_argument('--full_name_model', type=str, required=True, help="full_name_model for evolver")
        parser.add_argument('--gpu', type=str, required=True, help="list of the indices of GPUs used")

        args = parser.parse_args()

        # switch_information = {
        #     "bbh": InformationBBH
        # }
        # self.class_information = switch_information[type_task]
        self.class_information = InformationBBH
        self.class_strategy = StrategyContrGA

        self.ttl_task = args.task.split(",")
        self.full_name_model = args.full_name_model
        self.gpu = args.gpu
        self.llm = vLLM(self.full_name_model, self.gpu)
        # self.ttl_gpu = [int(i) for i in args.gpu.split(",")]
        # ray.init(ignore_reinit_error=True, num_gpus=len(self.ttl_gpu))

        # self.tag_experiment = f"construct/population_contr/{args.tag_task}/{args.full_name_model}"
        self.num_experiment = 1

    def prepare(self, idx_experiment=None):
        """ prepare the experiment
        Var:
            idx_experiment: (placeholder)
        """
        # llm = LLM(self.full_name_model, self.gpu)
        # create evolver
        # llm_evolver = llm
        # llm_evolver = LLM(self.full_name_model, self.gpu)
        # llm_evolver = LLM(self.full_name_model, self.ttl_gpu[0])

        # information = self.class_information(self.tag_task)
        # ttl_future = [
        #     load_model(self.full_name_model, gpu)
        #     for gpu in self.ttl_gpu
        # ]
        # ttl_llm_judge = ray.get(ttl_future)
        # judge = Judge(information, ttl_llm_judge)
        # llm_judge = llm
        # llm_judge = LLM(self.full_name_model, self.gpu)
        # llm_judge = LLM(self.full_name_model, self.ttl_gpu)
        # judge = Judge(information, llm_judge)

        # strategy = self.class_strategy(self.tag_task, self.full_name_model)

        # evolver = EvolverContrGA(llm_evolver, judge, strategy)

        # create terminator
        # terminator = Terminator(np.inf, 1)

        # create framework
        # framework = Framework(self.tag_experiment, evolver, terminator)


        ttl_framework = []
        for task in self.ttl_task:
            tag_task = f"bbh/{task}"

            # create judge
            information = self.class_information(tag_task)
            llm_judge = self.llm
            judge = Judge_vLLM(information, llm_judge)

            # create evolver
            strategy = StrategyContrGA(tag_task, self.full_name_model)
            llm_evolver = self.llm
            evolver = EvolverContrGA(llm_evolver, judge, strategy)

            # create framework
            tag_experiment = f"construct/population_contr/{tag_task}/{self.full_name_model}"
            terminator = Terminator(np.inf, 1)
            framework = Framework(tag_experiment, evolver, terminator)

            ttl_framework.append(framework)
            
        return ttl_framework


class PreparerInitialPopulation:
    """
    required:
        --task
        --full_name_model
        --gpu
    """
    def __init__(self):
        """ get input from user
        """
        if DEBUGGER=="True": print("enter PreparerInitialPopulation.__init__")

        # print(f"PreparerInitialPopulation.{torch.cuda.is_available()=}")
        # if torch.cuda.is_available() is False:
        #     raise Exception("No GPU available.")
        parser = argparse.ArgumentParser(description="For experiment.")

        # for strategy of evolver, information of judge
        parser.add_argument('--task', type=str, required=True, help="{name_task} ex: 'boolean_expressions' (in bbh)")
        parser.add_argument('--full_name_model', type=str, required=True, help="full_name_model")
        parser.add_argument('--gpu', type=str, required=True, help="list of the indices of GPUs used")

        args = parser.parse_args()

        # type_task = args.tag_task.split("/")[0]
        # switch_information = {
        #     "bbh": InformationBBH
        # }
        # self.class_information = switch_information[type_task]
        self.class_information = InformationBBH
        # self.class_strategy = StrategyInitail

        self.ttl_task = args.task.split(",")
        self.full_name_model = args.full_name_model
        self.gpu = args.gpu
        self.llm = vLLM(self.full_name_model, self.gpu)
        # self.ttl_gpu = [int(i) for i in args.gpu.split(",")]
        # print(f"PreparerInitialPopulation.{self.ttl_gpu=}")
        # ray.init(ignore_reinit_error=True, num_gpus=len(self.ttl_gpu))

        # self.tag_experiment = f"construct/population_init/{args.tag_task}/{args.full_name_model}"
        self.num_experiment = 1
        
        if DEBUGGER=="True": print("leave PreparerInitial.__init__")

    def prepare(self, idx_experiment=None):
        """ prepare the experiment
        Var:
            idx_experiment: (placeholder)
        """
        if DEBUGGER=="True": print("enter PreparerInitial.prepare")

        # create evolver
        # information = self.class_information(self.tag_task)
        # ttl_future = [
        #     load_model.remote(self.full_name_model, gpu)
        #     for gpu in self.ttl_gpu
        # ]
        # ttl_llm_judge = ray.get(ttl_future)
        # ttl_llm_judge = ray.get(ttl_future)
        # ttl_llm_judge = [
        #     LLM(self.full_name_model, gpu)
        #     for gpu in self.ttl_gpu
        # ]
        # judge = Judge(information, ttl_llm_judge)
        # judge = Judge_vLLM(information, self.llm)

        # strategy = self.class_strategy(self.tag_task)

        # evolver = EvolverInitial(judge, strategy)

        # # create terminator
        # terminator = Terminator(np.inf, 1)

        # # create framework
        # framework = Framework(self.tag_experiment, evolver, terminator)

        ttl_framework = []
        for task in self.ttl_task:
            tag_task = f"bbh/{task}"

            # create judge
            information = self.class_information(tag_task)
            llm_judge = self.llm
            judge = Judge_vLLM(information, llm_judge)
            
            # create evolver
            strategy = StrategyInitail(tag_task)
            evolver = EvolverInitial(judge, strategy)
            
            # create framework
            tag_experiment = f"construct/population_init/{tag_task}/{self.full_name_model}"
            terminator = Terminator(np.inf, 1)
            framework = Framework(tag_experiment, evolver, terminator)

            ttl_framework.append(framework)
        if DEBUGGER=="True": print("leave PreparerInitial.prepare")
        return ttl_framework
