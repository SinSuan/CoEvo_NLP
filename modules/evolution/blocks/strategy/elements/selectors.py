"""
select parent prompts from self.population (and self.population_contr)
"""

from copy import deepcopy

import numpy as np

from modules.evolution.blocks.strategy.elements.utils import get_weight
from modules.evolution.utils import refine_pair, refine_population


def selector_evo_de(self, i):
    population = refine_population(self.population)
    pair_best = population[0]
    pair_i = population[i]

    remaining_pairs = [pair for pair in population if pair['prompt'] != pair_i['prompt']]
    pair_1, pair_2 = np.random.choice(remaining_pairs, size=2, replace=False)

    ttl_parent = {
        "p_1": pair_1,
        "p_2": pair_2,
        "p_best": pair_best,
        "p_i": pair_i
    }

    return ttl_parent


def selector_evo_ga(self, i=None):
    """
    Var:
        i: int
            不能省略，作為 Evolver 中的佔位符
    """
    population = refine_population(self.population)
    
    ttl_score = [pair['train_score'] for pair in population]
    ttl_weight = get_weight(ttl_score)
    pair_1, pair_2 = np.random.choice(population , size=2, replace=False, p=ttl_weight)

    ttl_parent = {
        "p_1": pair_1,
        "p_2": pair_2
    }
    
    return ttl_parent


def selector_contr_ga(self, i, j):
    """
    Var:
        i < j: int
    """
    population = refine_population(self.population)
    p_better = population[i]
    p_normal = population[j]
    
    ttl_parent = {
        "p_better": p_better,
        "p_normal": p_normal
    }
    
    return ttl_parent


def selector_co_evo(self, i):
    population = refine_population(self.population)
    pair_best = population[0]
    pair_i = population[i]

    # 不是每種方法都需要 pair_i，但就是放這裡
    pair_contr = self.sample_contr(pair_i)

    ttl_parent = {
        "p_contr": pair_contr,
        "p_best": pair_best,
        "p_i": pair_i
    }

    return ttl_parent

def selector_opro(self, i=None):
    """
    Var:
        i: int
            不能省略，作為 Evolver 中的佔位符
    """
    population = refine_population(self.population)
    ttl_example = population[:20]

    ttl_parent = {
        f"p_{i}": pair
        for i, pair in enumerate(ttl_example)
    }

    return ttl_parent
