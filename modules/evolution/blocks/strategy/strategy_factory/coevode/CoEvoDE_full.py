from modules.evolution.blocks.strategy.elements.populations import PopulationCoEvo
from modules.evolution.blocks.strategy.elements.samplers_contr import sampler_contr_random, sampler_contr_shifting
from modules.evolution.blocks.strategy.elements.selectors import selector_co_evo
from modules.evolution.blocks.strategy.elements.templater.templater import Templater
from modules.evolution.blocks.strategy.elements.updaters.updater_factory import (
    UpdaterCoEvoDEContrConcatPairwise,
    UpdaterCoEvoDEContrRemainPairwise,
    UpdaterCoEvoDEContrReplacePairwise,
    UpdaterCoEvoDEContrConcatTopk,
    UpdaterCoEvoDEContrRemainTopk,
    UpdaterCoEvoDEContrReplaceTopk
)

class StrategyCoEvoDE_full(PopulationCoEvo, Templater):
    select_ttl_parent = selector_co_evo
    def __init__(self, tag_task, full_name_model):
        PopulationCoEvo.__init__(self, tag_task, full_name_model)
        Templater.__init__(self, "CoEvoDE")

class StrategyCoEvoDE_full_shift_remain_pairwise(
    StrategyCoEvoDE_full,
    UpdaterCoEvoDEContrRemainPairwise
):
    sample_contr = sampler_contr_shifting

class StrategyCoEvoDE_full_random_remain_pairwise(
    StrategyCoEvoDE_full,
    UpdaterCoEvoDEContrRemainPairwise
):
    sample_contr = sampler_contr_random

class StrategyCoEvoDE_full_shift_concat_pairwise(
    StrategyCoEvoDE_full,
    UpdaterCoEvoDEContrConcatPairwise
):
    sample_contr = sampler_contr_shifting

class StrategyCoEvoDE_full_random_concat_pairwise(
    StrategyCoEvoDE_full,
    UpdaterCoEvoDEContrConcatPairwise
):
    sample_contr = sampler_contr_random

class StrategyCoEvoDE_full_shift_replace_pairwise(
    StrategyCoEvoDE_full,
    UpdaterCoEvoDEContrReplacePairwise
):
    sample_contr = sampler_contr_shifting

class StrategyCoEvoDE_full_random_replace_pairwise(
    StrategyCoEvoDE_full,
    UpdaterCoEvoDEContrReplacePairwise
):
    sample_contr = sampler_contr_random

class StrategyCoEvoDE_full_shift_remain_topk(
    StrategyCoEvoDE_full,
    UpdaterCoEvoDEContrRemainTopk
):
    sample_contr = sampler_contr_shifting

class StrategyCoEvoDE_full_random_remain_topk(
    StrategyCoEvoDE_full,
    UpdaterCoEvoDEContrRemainTopk
):
    sample_contr = sampler_contr_random

class StrategyCoEvoDE_full_shift_concat_topk(
    StrategyCoEvoDE_full,
    UpdaterCoEvoDEContrConcatTopk
):
    sample_contr = sampler_contr_shifting

class StrategyCoEvoDE_full_random_concat_topk(
    StrategyCoEvoDE_full,
    UpdaterCoEvoDEContrConcatTopk
):
    sample_contr = sampler_contr_random

class StrategyCoEvoDE_full_shift_replace_topk(
    StrategyCoEvoDE_full,
    UpdaterCoEvoDEContrReplaceTopk
):
    sample_contr = sampler_contr_shifting

class StrategyCoEvoDE_full_random_replace_topk(
    StrategyCoEvoDE_full,
    UpdaterCoEvoDEContrReplaceTopk
):
    sample_contr = sampler_contr_random

SWITCH_CoEvoDE_full = {
    "CoEvoDE_full_shift_remain_pairwise": StrategyCoEvoDE_full_shift_remain_pairwise,
    "CoEvoDE_full_random_remain_pairwise": StrategyCoEvoDE_full_random_remain_pairwise,
    "CoEvoDE_full_shift_concat_pairwise": StrategyCoEvoDE_full_shift_concat_pairwise,
    "CoEvoDE_full_random_concat_pairwise": StrategyCoEvoDE_full_random_concat_pairwise,
    "CoEvoDE_full_shift_replace_pairwise": StrategyCoEvoDE_full_shift_replace_pairwise,
    "CoEvoDE_full_random_replace_pairwise": StrategyCoEvoDE_full_random_replace_pairwise,
    "CoEvoDE_full_shift_remain_topk": StrategyCoEvoDE_full_shift_remain_topk,
    "CoEvoDE_full_random_remain_topk": StrategyCoEvoDE_full_random_remain_topk,
    "CoEvoDE_full_shift_concat_topk": StrategyCoEvoDE_full_shift_concat_topk,
    "CoEvoDE_full_random_concat_topk": StrategyCoEvoDE_full_random_concat_topk,
    "CoEvoDE_full_shift_replace_topk": StrategyCoEvoDE_full_shift_replace_topk,
    "CoEvoDE_full_random_replace_topk": StrategyCoEvoDE_full_random_replace_topk,
}
