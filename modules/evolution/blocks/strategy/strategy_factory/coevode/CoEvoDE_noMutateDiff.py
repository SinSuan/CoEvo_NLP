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

class StrategyCoEvoDE_noMutateDiff(PopulationCoEvo, Templater):
    select_ttl_parent = selector_co_evo
    def __init__(self, tag_task, full_name_model):
        PopulationCoEvo.__init__(self, tag_task, full_name_model)
        Templater.__init__(self, "CoEvoDE_noMutateDiff")

class StrategyCoEvoDE_noMutateDiff_shift_remain_pairwise(
    StrategyCoEvoDE_noMutateDiff,
    UpdaterCoEvoDEContrRemainPairwise
):
    sample_contr = sampler_contr_shifting

class StrategyCoEvoDE_noMutateDiff_random_remain_pairwise(
    StrategyCoEvoDE_noMutateDiff,
    UpdaterCoEvoDEContrRemainPairwise
):
    sample_contr = sampler_contr_random

class StrategyCoEvoDE_noMutateDiff_shift_concat_pairwise(
    StrategyCoEvoDE_noMutateDiff,
    UpdaterCoEvoDEContrConcatPairwise
):
    sample_contr = sampler_contr_shifting

class StrategyCoEvoDE_noMutateDiff_random_concat_pairwise(
    StrategyCoEvoDE_noMutateDiff,
    UpdaterCoEvoDEContrConcatPairwise
):
    sample_contr = sampler_contr_random

class StrategyCoEvoDE_noMutateDiff_shift_replace_pairwise(
    StrategyCoEvoDE_noMutateDiff,
    UpdaterCoEvoDEContrReplacePairwise
):
    sample_contr = sampler_contr_shifting

class StrategyCoEvoDE_noMutateDiff_random_replace_pairwise(
    StrategyCoEvoDE_noMutateDiff,
    UpdaterCoEvoDEContrReplacePairwise
):
    sample_contr = sampler_contr_random

class StrategyCoEvoDE_noMutateDiff_shift_remain_topk(
    StrategyCoEvoDE_noMutateDiff,
    UpdaterCoEvoDEContrRemainTopk
):
    sample_contr = sampler_contr_shifting

class StrategyCoEvoDE_noMutateDiff_random_remain_topk(
    StrategyCoEvoDE_noMutateDiff,
    UpdaterCoEvoDEContrRemainTopk
):
    sample_contr = sampler_contr_random

class StrategyCoEvoDE_noMutateDiff_shift_concat_topk(
    StrategyCoEvoDE_noMutateDiff,
    UpdaterCoEvoDEContrConcatTopk
):
    sample_contr = sampler_contr_shifting

class StrategyCoEvoDE_noMutateDiff_random_concat_topk(
    StrategyCoEvoDE_noMutateDiff,
    UpdaterCoEvoDEContrConcatTopk
):
    sample_contr = sampler_contr_random

class StrategyCoEvoDE_noMutateDiff_shift_replace_topk(
    StrategyCoEvoDE_noMutateDiff,
    UpdaterCoEvoDEContrReplaceTopk
):
    sample_contr = sampler_contr_shifting

class StrategyCoEvoDE_noMutateDiff_random_replace_topk(
    StrategyCoEvoDE_noMutateDiff,
    UpdaterCoEvoDEContrReplaceTopk
):
    sample_contr = sampler_contr_random

SWITCH_CoEvoDE_noMutateDiff = {
    "CoEvoDE_noMutateDiff_shift_remain_pairwise": StrategyCoEvoDE_noMutateDiff_shift_remain_pairwise,
    "CoEvoDE_noMutateDiff_random_remain_pairwise": StrategyCoEvoDE_noMutateDiff_random_remain_pairwise,
    "CoEvoDE_noMutateDiff_shift_concat_pairwise": StrategyCoEvoDE_noMutateDiff_shift_concat_pairwise,
    "CoEvoDE_noMutateDiff_random_concat_pairwise": StrategyCoEvoDE_noMutateDiff_random_concat_pairwise,
    "CoEvoDE_noMutateDiff_shift_replace_pairwise": StrategyCoEvoDE_noMutateDiff_shift_replace_pairwise,
    "CoEvoDE_noMutateDiff_random_replace_pairwise": StrategyCoEvoDE_noMutateDiff_random_replace_pairwise,
    "CoEvoDE_noMutateDiff_shift_remain_topk": StrategyCoEvoDE_noMutateDiff_shift_remain_topk,
    "CoEvoDE_noMutateDiff_random_remain_topk": StrategyCoEvoDE_noMutateDiff_random_remain_topk,
    "CoEvoDE_noMutateDiff_shift_concat_topk": StrategyCoEvoDE_noMutateDiff_shift_concat_topk,
    "CoEvoDE_noMutateDiff_random_concat_topk": StrategyCoEvoDE_noMutateDiff_random_concat_topk,
    "CoEvoDE_noMutateDiff_shift_replace_topk": StrategyCoEvoDE_noMutateDiff_shift_replace_topk,
    "CoEvoDE_noMutateDiff_random_replace_topk": StrategyCoEvoDE_noMutateDiff_random_replace_topk,
}
