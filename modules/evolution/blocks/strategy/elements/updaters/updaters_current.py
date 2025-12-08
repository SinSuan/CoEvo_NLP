"""
reserve the desired prompts from the union of self.population and population_temp
record the worse ones to self.population_worse
"""

from copy import deepcopy
from modules.evolution.blocks.utils import sort_by_key


def updater_current_pairwise(self, population_temp):
    """ for EvoDE
    """
    size_population = len(self.population)
    self.population_worse = []

    for i in range(size_population):
        if population_temp[i]["train_score"] >= self.population[i]["train_score"]:
            self.population_worse.append(self.population[i])
            self.population[i] = population_temp[i]
        else:
            self.population_worse.append(population_temp[i])
            self.population[i]["fail"] = population_temp[i]

    self.population = sort_by_key(self.population)
    return deepcopy(self.population)


def updater_current_topk(self, population_temp):
    """ for EvoGA
    """
    size_population = len(self.population)
    self.population_worse = []

    population_all = self.population + population_temp
    population_sorted = sort_by_key(population_all)

    self.population = population_sorted[:size_population]
    self.population_worse = population_sorted[size_population:]
    return deepcopy(self.population)


def updater_current_replace(self, population_temp):
    """ for ContrGA
    """
    self.population = population_temp
    return deepcopy(self.population)
