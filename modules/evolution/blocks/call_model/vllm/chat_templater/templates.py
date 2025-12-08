CHAT_TEMPLATE = {
    "Mistral-7B-Instruct-v0.2": {
        "prefix": "<s>",
        "user": "[INST] {text_user}",
        "assistant": " [/INST] {text_assistant}",
        "suffix_assistant": " </s>",
    },
    "gemma-3-1b-it": {
        "prefix": "<bos>",
        "user": "<start_of_turn>user\n{text_user}<end_of_turn>\n",
        "assistant": "<start_of_turn>model\n{text_assistant}",
        "suffix_assistant": "<end_of_turn>\n",
    }
}
