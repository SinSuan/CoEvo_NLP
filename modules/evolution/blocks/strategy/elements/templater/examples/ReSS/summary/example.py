EXAMPLE = {
    "EvoDE": {
        "user" : {
            "p_1": "Rewrite the input text into simpler text.",
            "p_2": "Rewrite my complex sentence in simpler terms, but keep the meaning.",
            "p_best": "Rewrite the given input text into simpler English sentences while preserving the same meaning, so it can be understood by non-native English speakers.",
            "p_i": "Make the sentence easier for people who do not speak English fluently to comprehend."
        },
        "assistant" : {
            "part_diff": \
"""- "input text" vs "my complex sentence"
- "simpler text" vs "simpler terms, but keep the meaning\"""",

            "part_diff_mutated": \
"""- "input text" -> "provided text"
- "my complex sentence" -> "the difficult sentence"
- "simpler text" -> "easier language"
- "simpler terms, but keep the meaning" -> "simpler words while maintaining the meaning\"""",

            "p_new": "Transform the provided text into easier language while maintaining the meaning, making it accessible for non-native English speakers.",
            "p_final": "Convert the difficult sentence into simpler words while preserving the meaning, so it's easier for non-native English speakers to understand."
        }
    },

    "EvoGA": {
        "user": {
            "p_1": "Rewrite the input text into simpler text.",
            "p_2": "Rewrite my complex sentence in simpler terms, but keep the meaning."
        },
        "assistant": {
            "p_new": "Simplify the complex text while maintaining its meaning.",
            "p_final": "Make the complex text easier while maintaining its meaning."
        }
    },

    "ContrGA": {
        "user": {
            "p_better": "Rewrite the input text into simpler text.",
            "p_normal": "Rewrite my complex sentence in simpler terms, but keep the meaning."
        },
        "assistant": {
            "p_new": "Simplify the complex text while maintaining its meaning.",
            "p_final": "Make the complex text easier while maintaining its meaning."
        }
    },

    "CoEvo": {
        "user": {
            "p_contr": "Rewrite the input text into simpler text.",
            "p_best": "Rewrite my complex sentence in simpler terms, but keep the meaning.",
            "p_i": "Make the sentence easier for people who do not speak English fluently to comprehend."
        },

        "assistant" : {
            "part_common": \
"""- "rewrite"
- "simpler\"""",

            "part_diff": \
"""- "input text" vs "my complex sentence"
- "simpler text" vs "simpler terms, but keep the meaning\"""",

            "part_common_mutated": \
"""- "rewrite" -> "transform"
- "simpler" -> "easier\"""",

            "part_diff_mutated": \
"""- "input text" -> "provided text"
- "my complex sentence" -> "the difficult sentence"
- "simpler text" -> "easier language"
- "simpler terms, but keep the meaning" -> "simpler words while maintaining the meaning\"""",

            "p_new": "Make the sentence easier for people who do not speak English fluently to comprehend.",
            "p_final": "Transform the difficult sentence in easier words while maintaining the meaning to make it easier for people who do not speak English fluently to comprehend."
        }
    }
}