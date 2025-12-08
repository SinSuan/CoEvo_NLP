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

class StrategyCoEvoDE_noCommonPart(PopulationCoEvo, Templater):
    select_ttl_parent = selector_co_evo
    def __init__(self, tag_task, full_name_model):
        PopulationCoEvo.__init__(self, tag_task, full_name_model)
        Templater.__init__(self, "CoEvoDE_noCommonPart")

class StrategyCoEvoDE_noCommonPart_shift_remain_pairwise(
    StrategyCoEvoDE_noCommonPart,
    UpdaterCoEvoDEContrRemainPairwise
):
    sample_contr = sampler_contr_shifting

class StrategyCoEvoDE_noCommonPart_random_remain_pairwise(
    StrategyCoEvoDE_noCommonPart,
    UpdaterCoEvoDEContrRemainPairwise
):
    sample_contr = sampler_contr_random

class StrategyCoEvoDE_noCommonPart_shift_concat_pairwise(
    StrategyCoEvoDE_noCommonPart,
    UpdaterCoEvoDEContrConcatPairwise
):
    sample_contr = sampler_contr_shifting

class StrategyCoEvoDE_noCommonPart_random_concat_pairwise(
    StrategyCoEvoDE_noCommonPart,
    UpdaterCoEvoDEContrConcatPairwise
):
    sample_contr = sampler_contr_random

class StrategyCoEvoDE_noCommonPart_shift_replace_pairwise(
    StrategyCoEvoDE_noCommonPart,
    UpdaterCoEvoDEContrReplacePairwise
):
    sample_contr = sampler_contr_shifting

class StrategyCoEvoDE_noCommonPart_random_replace_pairwise(
    StrategyCoEvoDE_noCommonPart,
    UpdaterCoEvoDEContrReplacePairwise
):
    sample_contr = sampler_contr_random

class StrategyCoEvoDE_noCommonPart_shift_remain_topk(
    StrategyCoEvoDE_noCommonPart,
    UpdaterCoEvoDEContrRemainTopk
):
    sample_contr = sampler_contr_shifting

class StrategyCoEvoDE_noCommonPart_random_remain_topk(
    StrategyCoEvoDE_noCommonPart,
    UpdaterCoEvoDEContrRemainTopk
):
    sample_contr = sampler_contr_random

class StrategyCoEvoDE_noCommonPart_shift_concat_topk(
    StrategyCoEvoDE_noCommonPart,
    UpdaterCoEvoDEContrConcatTopk
):
    sample_contr = sampler_contr_shifting

class StrategyCoEvoDE_noCommonPart_random_concat_topk(
    StrategyCoEvoDE_noCommonPart,
    UpdaterCoEvoDEContrConcatTopk
):
    sample_contr = sampler_contr_random

class StrategyCoEvoDE_noCommonPart_shift_replace_topk(
    StrategyCoEvoDE_noCommonPart,
    UpdaterCoEvoDEContrReplaceTopk
):
    sample_contr = sampler_contr_shifting

class StrategyCoEvoDE_noCommonPart_random_replace_topk(
    StrategyCoEvoDE_noCommonPart,
    UpdaterCoEvoDEContrReplaceTopk
):
    sample_contr = sampler_contr_random

SWITCH_CoEvoDE_noCommonPart = {
    "CoEvoDE_noCommonPart_shift_remain_pairwise": StrategyCoEvoDE_noCommonPart_shift_remain_pairwise,
    "CoEvoDE_noCommonPart_random_remain_pairwise": StrategyCoEvoDE_noCommonPart_random_remain_pairwise,
    "CoEvoDE_noCommonPart_shift_concat_pairwise": StrategyCoEvoDE_noCommonPart_shift_concat_pairwise,
    "CoEvoDE_noCommonPart_random_concat_pairwise": StrategyCoEvoDE_noCommonPart_random_concat_pairwise,
    "CoEvoDE_noCommonPart_shift_replace_pairwise": StrategyCoEvoDE_noCommonPart_shift_replace_pairwise,
    "CoEvoDE_noCommonPart_random_replace_pairwise": StrategyCoEvoDE_noCommonPart_random_replace_pairwise,
    "CoEvoDE_noCommonPart_shift_remain_topk": StrategyCoEvoDE_noCommonPart_shift_remain_topk,
    "CoEvoDE_noCommonPart_random_remain_topk": StrategyCoEvoDE_noCommonPart_random_remain_topk,
    "CoEvoDE_noCommonPart_shift_concat_topk": StrategyCoEvoDE_noCommonPart_shift_concat_topk,
    "CoEvoDE_noCommonPart_random_concat_topk": StrategyCoEvoDE_noCommonPart_random_concat_topk,
    "CoEvoDE_noCommonPart_shift_replace_topk": StrategyCoEvoDE_noCommonPart_shift_replace_topk,
    "CoEvoDE_noCommonPart_random_replace_topk": StrategyCoEvoDE_noCommonPart_random_replace_topk,
}
