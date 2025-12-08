EXAMPLE = {
    "EvoDE": {
        "user" : {
            "p_1": "We'll tackle this reasoning challenge step by step, taking our time to carefully consider each part along the way.",
            "p_2": "Let’s work this out in a step by step way to be sure we have the right answer.",
            "p_best": "Before we dive into the answer,",
            "p_i": "We'll thoughtfully progress through this task step by step."
        },
        "assistant" : {
            "part_diff": \
"""\"We'll -> Let’s"
"tackle -> work"
"this reasoning challenge" -> "this"
"carefully consider each part along the way" -> "to be sure we have the right answer\"""",

            "part_diff_mutated": \
"""\"We'll -> I will"
"tackle -> solve"
"this reasoning challenge" -> "the problem"
"carefully consider each part along the way" -> "to ensure we solve it correctly\"""",

            "p_new": "Before I ensure the answer carefully,",
            "p_final": "Before I carefully confirm the answer, let's thoughtfully work through this task step by step."
        }
    },

    "EvoGA": {
        "user": {
            "p_1": "We'll tackle this reasoning challenge step by step, taking our time to carefully consider each part along the way.",
            "p_2": "Before we dive into the answer,",
        },
        "assistant": {
            "p_new": "Before I ensure the answer carefully, we'll thoughtfully progress through this task step by step.",
            "p_final": "Before I carefully confirm the answer, let's thoughtfully work through this task step by step."
        }
    },

    "ContrGA": {
        "user": {
            "p_better": "We'll tackle this reasoning challenge step by step, taking our time to carefully consider each part along the way.",
            "p_normal": "Before we dive into the answer,",
        },
        "assistant": {
            "p_new": "Before we get started, we'll take our time and think things through.",
            "p_final": "Before we begin, let's take a moment to carefully consider everything."
        }
    },

    "CoEvoDE": {
        "user": {
            "p_contr": "We'll tackle this reasoning challenge step by step, taking our time to carefully consider each part along the way.",
            "p_best": "Let’s work this out in a step by step way to be sure we have the right answer.",
            "p_i": "We'll thoughtfully progress through this task step by step."
        },

        "assistant" : {
            "part_common": \
"""\"we"
"this"
"step by step"
"way\"""",

            "part_diff": \
"""\"We'll -> Let’s"
"tackle -> work"
"this reasoning challenge" -> "this"
"carefully consider each part along the way" -> "to be sure we have the right answer\"""",

            "part_common_mutated": \
"""\"we" -> "our team"
"this" -> "that"
"step by step" -> "gradual"
"way" -> "avenue\"""",

            "part_diff_mutated": \
"""\"We'll -> I will"
"tackle -> solve"
"this reasoning challenge" -> "the problem"
"carefully consider each part along the way" -> "to ensure we solve it correctly\"""",

            "p_new": "Let’s solve this in a gradual way to ensure we have the correct answer.",
            "p_final": "We are going to solve the problem gradually to ensure the answer correct."
        }
    },
    
    "CoEvoDE_noCommonPart": {
        "user": {
            "p_contr": "We'll tackle this reasoning challenge step by step, taking our time to carefully consider each part along the way.",
            "p_best": "Let’s work this out in a step by step way to be sure we have the right answer.",
            "p_i": "We'll thoughtfully progress through this task step by step."
        },

        "assistant" : {
            "part_diff": \
"""\"We'll -> Let’s"
"tackle -> work"
"this reasoning challenge" -> "this"
"carefully consider each part along the way" -> "to be sure we have the right answer\"""",

            "part_diff_mutated": \
"""\"We'll -> I will"
"tackle -> solve"
"this reasoning challenge" -> "the problem"
"carefully consider each part along the way" -> "to ensure we solve it correctly\"""",

            "p_new": "Let’s solve this in a gradual way to ensure we have the correct answer.",
            "p_final": "We are going to solve the problem gradually to ensure the answer correct."
        }
    },
    
    "CoEvoDE_noMutateDiff": {
        "user": {
            "p_contr": "We'll tackle this reasoning challenge step by step, taking our time to carefully consider each part along the way.",
            "p_best": "Let’s work this out in a step by step way to be sure we have the right answer.",
            "p_i": "We'll thoughtfully progress through this task step by step."
        },

        "assistant" : {
            "part_common": \
"""\"we"
"this"
"step by step"
"way\"""",

            "part_diff": \
"""\"We'll -> Let’s"
"tackle -> work"
"this reasoning challenge" -> "this"
"carefully consider each part along the way" -> "to be sure we have the right answer\"""",

            "part_common_mutated": \
"""\"we" -> "our team"
"this" -> "that"
"step by step" -> "gradual"
"way" -> "avenue\"""",

            "p_new": "Let’s solve this in a gradual way to ensure we have the correct answer.",
            "p_final": "We are going to solve the problem gradually to ensure the answer correct."
        }
    },

}
