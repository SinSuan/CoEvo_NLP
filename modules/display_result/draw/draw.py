from modules.display_result.draw.drawers.distribution import drawer_distribution_population
from modules.display_result.draw.drawers.stability import drawer_stability_experiment
from modules.utils.tools import time_now


SWITCH_NAME_FIG = {
    drawer_stability_experiment: "stability",
    drawer_distribution_population: "distribution"
}

def draw_result(folder_experiment:str, name_model:str, drawer: callable):

    prompt_variant = ["noCommonPart", "noMutateDiff", "full"]
    contrastive_sample = ["random", "shift"]
    population_update = ["remain", "replace", "concat"]
    ttl_comoponent = [prompt_variant, contrastive_sample, population_update]
    ttl_invariants = []
    for i in range(3):
        component_1 = ttl_comoponent[i]
        for j in range(i+1, 3):
            component_2 = ttl_comoponent[j]
            for a in component_1:
                for b in component_2:
                    invariants = [a, b]
                    ttl_invariants.append(invariants)

    print(f"{ttl_invariants=}\n")
    for invariants in ttl_invariants:
        print(f"\n{invariants=}")

        a,b = invariants
        if a == "full" and b != "remain":
            pass
        else:
            fig = drawer(folder_experiment, name_model, invariants)

            t = time_now()
            name_fig = f"{name_model.split('/')[-1]}_{t}_{SWITCH_NAME_FIG[drawer]}__{a}_{b}"
            # path_fig = f"{folder_experiment}/zzz_results_col4_full/{name_fig}.png"
            path_fig = f"{folder_experiment}/zzz_test/{name_fig}.png"

            fig.savefig(path_fig, dpi=300)
