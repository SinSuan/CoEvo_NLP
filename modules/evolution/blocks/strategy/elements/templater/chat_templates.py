TEMPLATE = {
    "EvoDE": {
        "user": \
"""
Please follow the instruction step-by-step to generate a Better Prompt.

1. Identify the Different Parts between the Prompt 1 and Prompt 2:
Prompt 1: {p_1}
Prompt 2: {p_2}

2. Randomly mutate the Different Parts.

3. Combine the Mutated Different Parts with Prompt 3, selectively replace it with the Mutated Different Parts in step 2 and generate a New Prompt.
Prompt 3: {p_best}

4. Crossover the New Prompt in the step 3 with the following Basic Prompt and generate a Better Prompt bracketed with “ and ”:
Basic Prompt: {p_i}
""",
        "assistant": \
"""
1. Identify the Different Parts between the Prompt 1 and Prompt 2:
Prompt 1: {p_1}
Prompt 2: {p_2}

Different parts:
{part_diff}

2. Randomly mutate the Different Parts.

Mutated Different Parts:
{part_diff_mutated}

3. Combine the Mutated Different Parts with Prompt 3, selectively replace it with the Mutated Different Parts in step 2 and generate a New Prompt.
Prompt 3: {p_best}
New Prompt: {p_new}

4. Crossover the New Prompt in step 3 with the following Basic Prompt and generate a Better Prompt bracketed with “ and ”:
Basic Prompt: {p_i}
Better Prompt: “ {p_final} ”
"""
    },

    "EvoGA": {
        "user": \
"""
Please follow the instruction step-by-step to generate a Better Prompt.

1. Crossover the following prompts and generate a New Prompt:
Prompt 1: {p_1}
Prompt 2: {p_2}

2. Mutate the New Prompt generated in Step 1 and generate a Better Prompt bracketed with “ and ”.
""",
        "assistant": \
"""
1. Crossover the following prompts and generate a New Prompt:
Prompt 1: {p_1}
Prompt 2: {p_2}
New Prompt: {p_new}

2. Mutate the New Prompt generated in Step 1 and generate a Better Prompt bracketed with “ and ”.
New Prompt: {p_new}
Better Prompt: “ {p_final} ”
"""
    },

    "ContrGA": {
        "user": \
"""
Please follow the instruction step-by-step to generate a Worse Prompt.

1. Crossover the following prompts and generate a New Prompt:
Better Prompt: {p_better}
Normal Prompt: {p_normal}

2. Mutate the New Prompt generated in Step 1 and generate a Worse Prompt bracketed with “ and ”.
""",
        "assistant": \
"""
Please follow the instruction step-by-step to generate a Worse Prompt.

1. Crossover the following prompts and generate a New Prompt:
Better Prompt: {p_better}
Normal Prompt: {p_normal}
New Prompt: {p_new}

2. Mutate the New Prompt generated in Step 1 and generate a Worse Prompt bracketed with “ and ”.
New Prompt: {p_new}
Worse Prompt: “ {p_final} ”
"""
    },

    "CoEvoDE": {
        "user": \
"""
Please follow the instruction step-by-btep to generate a Better Prompt.

1. Identify the Common parts and the Different Parts between Worse Prompt and Normal Prompt:
Worse Prompt: {p_contr}
Normal Prompt: {p_best}

2. Randomly mutate the Common parts and the Different Parts.

3. Combine the Mutated Common Parts and the Mutated Different Parts with Normal Prompt, selectively replace it with the Mutated Common Parts and the Mutated Different Parts in step 2 and generate a New Prompt.
Normal Prompt: {p_best}

4. Crossover the New Prompt in the step 3 with the following Basic Prompt and generate a Better Prompt bracketed with “ and ”:
Basic Prompt: {p_i}
""",
        "assistant": \
"""
1. Identify the Common parts and the Different Parts between Worse Prompt and Normal Prompt:
Worse Prompt: {p_contr}
Normal Prompt: {p_best}

Common Parts:
{part_common}

Different Parts:
{part_diff}

2. Randomly mutate the Common parts and the Different Parts.

Mutated Common Parts:
{part_common_mutated}

Mutated Different Parts:
{part_diff_mutated}

3. Combine the Mutated Common Parts and the Mutated Different Parts with Normal Prompt, selectively replace it with the Mutated Common Parts and the Mutated Different Parts in step 2 and generate a New Prompt.
Normal Prompt: {p_best}
New Prompt: {p_new}

4. Crossover the New Prompt in the step 3 with the following Basic Prompt and generate a Better Prompt bracketed with “ and ”:
Basic Prompt: {p_i}
Better Prompt: “ {p_final} ”
"""
    },

    "CoEvoDE_noCommonPart": {
        "user": \
"""
Please follow the instruction step-by-btep to generate a Better Prompt.

1. Identify the Different Parts between Worse Prompt and Normal Prompt:
Worse Prompt: {p_contr}
Normal Prompt: {p_best}

2. Randomly mutate the Different Parts.

3. Combine the Mutated Different Parts with Normal Prompt, selectively replace it with the Mutated Different Parts in step 2 and generate a New Prompt.
Normal Prompt: {p_best}

4. Crossover the New Prompt in the step 3 with the following Basic Prompt and generate a Better Prompt bracketed with “ and ”:
Basic Prompt: {p_i}
""",
        "assistant": \
"""
1. Identify the Different Parts between Worse Prompt and Normal Prompt:
Worse Prompt: {p_contr}
Normal Prompt: {p_best}

Different Parts:
{part_diff}

2. Randomly mutate the Different Parts.

Mutated Different Parts:
{part_diff_mutated}

3. Combine the Mutated Different Parts with Normal Prompt, selectively replace it with the Mutated Different Parts in step 2 and generate a New Prompt.
Normal Prompt: {p_best}
New Prompt: {p_new}

4. Crossover the New Prompt in the step 3 with the following Basic Prompt and generate a Better Prompt bracketed with “ and ”:
Basic Prompt: {p_i}
Better Prompt: “ {p_final} ”
"""
    },

    "CoEvoDE_noMutateDiff": {
        "user": \
"""
Please follow the instruction step-by-btep to generate a Better Prompt.

1. Identify the Common parts and the Different Parts between Worse Prompt and Normal Prompt:
Worse Prompt: {p_contr}
Normal Prompt: {p_best}

2. Randomly mutate the Common parts.

3. Combine the Mutated Common Parts and the Different Parts with Normal Prompt, selectively replace it with the Mutated Common Parts and the Different Parts in step 2 and generate a New Prompt.
Normal Prompt: {p_best}

4. Crossover the New Prompt in the step 3 with the following Basic Prompt and generate a Better Prompt bracketed with “ and ”:
Basic Prompt: {p_i}
""",
        "assistant": \
"""
1. Identify the Common parts and the Different Parts between Worse Prompt and Normal Prompt:
Worse Prompt: {p_contr}
Normal Prompt: {p_best}

Common Parts:
{part_common}

Different Parts:
{part_diff}

2. Randomly mutate the Common parts and the Different Parts.

Mutated Common Parts:
{part_common_mutated}

3. Combine the Mutated Common Parts and the Different Parts with Normal Prompt, selectively replace it with the Mutated Common Parts and the Different Parts in step 2 and generate a New Prompt.
Normal Prompt: {p_best}
New Prompt: {p_new}

4. Crossover the New Prompt in the step 3 with the following Basic Prompt and generate a Better Prompt bracketed with “ and ”:
Basic Prompt: {p_i}
Better Prompt: “ {p_final} ”
"""
    },

    "OPRO":{
        "user": \
"""
.
"""   
    }
}
