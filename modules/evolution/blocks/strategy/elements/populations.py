"""
method required
    population_all(): None -> list[dict]
        return the union/concatenation of all populations for avoiding duplication
"""

from copy import deepcopy
import json

from modules.evolution.blocks.utils import sort_by_key
from modules.evolution.utils import refine_population
from modules.utils.get_config import get_folder_project

class PopulationExample:
    def __init__(self, tag_task:str, full_name_model:str):
        """
        Var
            task: str
                {type_task}/{name_task}
            
            full_name_model: str
        """
        # required
        self.tag_task = ...
        self.full_name_model = ...
        self.population = ...
        
        # optional
        self.population_contr = ...
    
    def get_population_all(self):
        population_all = deepcopy(self.population+self.population_contr)
        return population_all

class PopulationEvoPrompt:
    def __init__(self, tag_task:str, full_name_model:str):
        """
        Var
            task: str
                {type_task}/{name_task}
            
            full_name_model: str
        """
        self.tag_task = tag_task
        self.full_name_model = full_name_model

        folder_project = get_folder_project()
        path_population = f"{folder_project}/data/population/init/{tag_task}/{full_name_model}/population.json"
        with open(path_population, "r", encoding='utf-8') as f:
            population_record = json.load(f)
        population = population_record["result"]["population"]
        population_refine = refine_population(population)
        self.population = sort_by_key(population_refine)

    def get_population_all(self):
        population_all = deepcopy(self.population)
        return population_all

class PopulationContrGA:
    def __init__(self, tag_task:str, full_name_model:str):
        """
        Var
            task: str
                {type_task}/{name_task}
            
            full_name_model: str
        """
        self.tag_task = tag_task
        self.full_name_model = full_name_model

        folder_project = get_folder_project()
        path_population = f"{folder_project}/data/population/init/{tag_task}/{full_name_model}/population.json"
        with open(path_population, "r", encoding='utf-8') as f:
            population_record = json.load(f)
        population = population_record["result"]["population"]
        population_refine = refine_population(population)
        self.population = sort_by_key(population_refine)

    def get_population_all(self):
        population_all = deepcopy(self.population)
        return population_all

class PopulationCoEvo:
    def __init__(self, tag_task:str, full_name_model:str):
        """
        Var
            task: str
                {type_task}/{name_task}
            
            full_name_model: str
        """
        self.tag_task = tag_task
        self.full_name_model = full_name_model

        folder_project = get_folder_project()

        path_population = f"{folder_project}/data/population/init/{tag_task}/{full_name_model}/population.json"
        with open(path_population, "r", encoding='utf-8') as f:
            population_record = json.load(f)
        population = population_record["result"]["population"]
        population_refine = refine_population(population)
        self.population = sort_by_key(population_refine)

        path_population_contr = f"{folder_project}/data/population/contr/{tag_task}/{full_name_model}/population.json"
        with open(path_population_contr, "r", encoding='utf-8') as f:
            population_contr_record = json.load(f)
        population_contr = population_contr_record["result"]["population"]
        population_contr_refine = refine_population(population_contr)
        self.population_contr = sort_by_key(population_contr_refine)

    def get_population_all(self):
        population_all = deepcopy(self.population+self.population_contr)
        return population_all

class PopulationInitial:
    def __init__(self, tag_task:str):
        """
        Var
            task: str
                {type_task}/{name_task}
            
        Attribute
            population: list[str]
        """
        self.tag_task = tag_task
        self.full_name_model = "None"

        folder_project = get_folder_project()

        # path_population = f"{folder_project}/data/population/raw/{tag_task}/generate/prompts_auto.json"
        path_population = f"{folder_project}/data/population/raw/bbh/general_prompts.json"
        with open(path_population, "r", encoding='utf-8') as f:
            self.population = json.load(f)

    def get_population_all(self):
        population_all = deepcopy(self.population)
        return population_all
