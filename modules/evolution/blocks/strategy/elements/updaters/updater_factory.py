from modules.evolution.blocks.strategy.elements.updaters.updaters_contrastive import updater_contr_concat, updater_contr_remain, updater_contr_replace
from modules.evolution.blocks.strategy.elements.updaters.updaters_current import updater_current_pairwise, updater_current_topk


class UpdaterCoEvoDE:
    def update_population(self, population_temp):
        """ 必須先做 population_contr 的 updater，因為才做 population 更新過後會變
        """
        self.population = self.updater_current(population_temp)
        self.population_contr = self.updater_contr()

class UpdaterCoEvoDEContrConcatPairwise(UpdaterCoEvoDE):
    updater_current = updater_current_pairwise
    updater_contr = updater_contr_concat

class UpdaterCoEvoDEContrReplacePairwise(UpdaterCoEvoDE):
    updater_current = updater_current_pairwise
    updater_contr = updater_contr_replace

class UpdaterCoEvoDEContrRemainPairwise(UpdaterCoEvoDE):
    updater_current = updater_current_pairwise
    updater_contr = updater_contr_remain

class UpdaterCoEvoDEContrConcatTopk(UpdaterCoEvoDE):
    updater_current = updater_current_topk
    updater_contr = updater_contr_concat

class UpdaterCoEvoDEContrReplaceTopk(UpdaterCoEvoDE):
    updater_current = updater_current_topk
    updater_contr = updater_contr_replace

class UpdaterCoEvoDEContrRemainTopk(UpdaterCoEvoDE):
    updater_current = updater_current_topk
    updater_contr = updater_contr_remain
