def get_switch_ttl_name_task():
    switch_ttl_task = {
        "boolean_expressions": "be",
        "causal_judgement": "cj",
        "date_understanding": "du",
        "disambiguation_qa": "dqa",
        "formal_fallacies": "ff",
        "hyperbaton": "hb",
        "logical_deduction_five_objects": "ld5",
        "logical_deduction_seven_objects": "ld7",
        "logical_deduction_three_objects": "ld3",
        "navigate": "nav",
        "ruin_names": "rn",
        "salient_translation_error_detection": "sted",
        "snarks": "s",
        "sports_understanding": "su",
        "temporal_sequences": "ts",
        "tracking_shuffled_objects_five_objects": "ts5",
        "tracking_shuffled_objects_seven_objects": "ts7",
        "tracking_shuffled_objects_three_objects": "ts3",
        "web_of_lies": "wol"
    }
    return switch_ttl_task

def get_switch_ttl_name_variant():
    switch_ttl_type_prompt = {
        "full": "ful",
        "noCommonPart": "ncp",
        "noMutateDiff": "nmd",
    }
    switch_ttl_type_update_curr = {
        "pairwise": "pw",
        "topk": "tk"
    }
    switch_ttl_type_sampler = {
        "random": "r",
        "shift": "s"
    }
    switch_ttl_type_update_contr = {
        "remain": "rem",
        "replace": "rep",
        "concat": "cat",
    }
    switch_ttl_variant = {}
    for type_prompt, type_prompt_abbr in switch_ttl_type_prompt.items():
        for type_update_curr, type_update_curr_abbr in switch_ttl_type_update_curr.items():
            for type_sampler, type_sampler_abbr in switch_ttl_type_sampler.items():
                for type_update_contr, type_update_contr_abbr in switch_ttl_type_update_contr.items():
                    variant = f"CoEvoDE_{type_prompt}_{type_sampler}_{type_update_contr}_{type_update_curr}"
                    variant_abbr = f"{type_prompt_abbr}_{type_update_curr_abbr}_{type_sampler_abbr}_{type_update_contr_abbr}"
                    switch_ttl_variant[variant] = variant_abbr

    switch_ttl_variant.update({
        "EvoDE": "EvoED",
        "EvoGA": "EvoGA"
    })
    return switch_ttl_variant
