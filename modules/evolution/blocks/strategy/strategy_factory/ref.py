"""
the elements of strategies:
    - population        class       (required)
    - selector          function    (required)
    - sampler           function    (optional)
    - comparator        function    (required)
    - template   string      (required)
"""

# from modules.evolution.blocks.strategy.elements.updaters.updater_factory import UpdaterCoEvoDEContrConcat, UpdaterCoEvoDEContrReplace
from modules.evolution.blocks.strategy.elements.updaters.updaters_current import updater_current_pairwise, updater_current_replace, updater_current_topk
from modules.evolution.blocks.strategy.elements.populations import (
    PopulationContrGA,
    PopulationEvoPrompt,
    PopulationCoEvo,
    PopulationExample,
    PopulationInitial
)
from modules.evolution.blocks.strategy.elements.samplers_contr import sampler_contr_random, sampler_contr_shifting
from modules.evolution.blocks.strategy.elements.selectors import (
    selector_co_evo,
    selector_contr_ga,
    selector_evo_de,
    selector_evo_ga,
    selector_opro
)
from modules.evolution.blocks.strategy.elements.templater.templater import Templater


class StrategyExample(PopulationExample, Templater):
    """ just for trace (not a Strategy at all)
    """
    # required
    select_ttl_parent = ...
    update_population = ...

    # optional
    sample_contr = ...
    def __init__(self, tag_task, full_name_model):
        PopulationExample.__init__(self, tag_task, full_name_model)
        Templater.__init__(self, "Example")


class StrategyEvoDE(PopulationEvoPrompt, Templater):
    select_ttl_parent = selector_evo_de
    update_population = updater_current_pairwise
    def __init__(self, tag_task, full_name_model):
        PopulationEvoPrompt.__init__(self, tag_task, full_name_model)
        Templater.__init__(self, "EvoDE")


class StrategyEvoGA(PopulationEvoPrompt, Templater):
    select_ttl_parent = selector_evo_ga
    update_population = updater_current_topk
    def __init__(self, tag_task, full_name_model):
        PopulationEvoPrompt.__init__(self, tag_task, full_name_model)
        Templater.__init__(self, "EvoGA")


class StrategyContrGA(PopulationContrGA, Templater):
    select_ttl_parent = selector_contr_ga
    update_population = updater_current_replace
    def __init__(self, tag_task, full_name_model):
        PopulationContrGA.__init__(self, tag_task, full_name_model)
        Templater.__init__(self, "ContrGA")


# class StrategyCoEvoDE_shift(PopulationCoEvo, Templater):
#     """ StrategyCoEvoDE_shift
#     """
#     select_ttl_parent = selector_co_evo
#     sample_contr = sampler_contr_shifting
#     update_population = updater_current_pairwise
#     def __init__(self, tag_task, full_name_model):
#         PopulationCoEvo.__init__(self, tag_task, full_name_model)
#         Templater.__init__(self, "CoEvoDE")

# class StrategyCoEvoDE_random(PopulationCoEvo, Templater):
#     select_ttl_parent = selector_co_evo
#     sample_contr = sampler_contr_random
#     update_population = updater_current_pairwise
#     def __init__(self, tag_task, full_name_model):
#         PopulationCoEvo.__init__(self, tag_task, full_name_model)
#         Templater.__init__(self, "CoEvoDE")

class StrategyOPRO(PopulationEvoPrompt, Templater):
    select_ttl_parent = selector_opro
    update_population = updater_current_topk
    def __init__(self, tag_task, full_name_model):
        PopulationEvoPrompt.__init__(self, tag_task, full_name_model)
        Templater.__init__(self, "OPRO")


class StrategyInitail(PopulationInitial):
    update_population = updater_current_replace
    def __init__(self, tag_task):
        PopulationInitial.__init__(self, tag_task)

SWITCH_Ref = {
    "EvoDE": StrategyEvoDE,
    "EvoGA": StrategyEvoGA,
    "OPRO": StrategyOPRO
}
