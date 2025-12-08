"""
select the contrastive parent prompt(s) from self.population_contr
(for SelectorCoEvo in modules/evolution/blocks/config/elements/selectors.py)

Var required; place holder (*args) at least
"""

from copy import deepcopy
import numpy as np


def sampler_contr_random(self, pair_i=None):
    """
    Var:
        pair_i: place holder (no need)
    """
    population_contr = deepcopy(self.population_contr)
    pair_contr = np.random.choice(population_contr)
    return pair_contr

def sampler_contr_shifting(self, pair_i):
    """
    Var:
        pair_i: dict
            the prompt to be compared
            {
                "prompt": str,
                "train_score": int
            }
    """
    population_contr = deepcopy(self.population_contr)
    score_i = pair_i["train_score"]
    score_upper = score_i - 5
    population_contr_desired = [pair_i] # 確保非空
    for i, pair in enumerate(population_contr):
        if pair["train_score"] <= score_upper:
            population_contr_desired = population_contr[i:]
            break

    # # 確保非空
    # if len(population_contr_desired) == 0:
    #     population_contr_desired = [pair_i]

    pair_contr = np.random.choice(population_contr_desired)
    return pair_contr
