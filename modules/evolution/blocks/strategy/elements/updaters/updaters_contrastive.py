""" for CoEvo
"""

from copy import deepcopy
from modules.evolution.blocks.utils import sort_by_key

# def select_fail_population(population_temp, population):
#     """
#     Var
#         ** len(population_temp) == len(population) **
#     """
#     size_population = len(population)

#     population_fail = []
#     for i in range(size_population):
#         try:
#             if population_temp[i]["train_score"] >= population[i]["train_score"]:
#                 population_fail.append(population[i])
#             else:
#                 population_fail.append(population_temp[i])
#         except Exception as e:
#             print(f"{i=}")
#             print(f"{population_temp=}")
#             print(f"{population=}")
#             print(f"{population_fail=}")
#             raise e

#     return population_fail

def updater_contr_concat(self):
    """ dynamic update population_contr; concat lower ones to population_contr
    """
    population_all = self.population_contr + self.population_worse
    self.population_contr = sort_by_key(population_all)

    return deepcopy(self.population_contr)


def updater_contr_replace(self):
    """ dynamic update population_contr; replace population_contr with lower ones
    """
    self.population_contr = sort_by_key(self.population_worse)

    return deepcopy(self.population_contr)


def updater_contr_remain(self):
    """ fixed population_contr
    """
    return deepcopy(self.population_contr)
