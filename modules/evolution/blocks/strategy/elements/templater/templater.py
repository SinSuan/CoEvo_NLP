"""
依據不同 task 選擇不同的 exmpla
依據不同論文選擇不同的 template
"""

from modules.evolution.blocks.strategy.elements.templater.chat_templates import TEMPLATE
from modules.evolution.blocks.strategy.elements.templater.examples.bbh.general_example import EXAMPLE

class Templater:
    def __init__(self, type_strategy):
        """
        Var
            type_strategy: str
                ex: "EvoDE", "EvoGA", "ContrGA", "CoEvo", ...

        Attributes
            type_strategy: str

            template: dict[str, str]
                {
                    "user": f-string,
                    "assistant": f-string
                }

            example: dict[str, dict[str, str]]
                {
                    "user": dict[str, str],
                    "assistant": dict[str, str]
                }
                    dict formation:
                    {key in template: str}: {value in template: str}
        """
        self.type_strategy = type_strategy

        self.template = TEMPLATE[type_strategy]
        self.example = EXAMPLE[type_strategy]

    def create_message(self, **ttl_parent_prompt_only):
        """
        Var
            ttl_parent_prompt_only: dict[str, str]
                dict formation:
                {
                    key: str,
                    value: str
                }
        """
        template_user = self.template["user"]
        template_assistant = self.template["assistant"]

        # create shot
        example_user = self.example["user"]
        example_assistant = example_user | self.example["assistant"]
        shot_user = template_user.format(**example_user)
        shot_assistant = template_assistant.format(**example_assistant)
        shot = {
            "user": shot_user,
            "assistant": shot_assistant
        }

        # create query
        query_user = template_user.format(**ttl_parent_prompt_only)
        query_assistant = "1."
        query = {
            "user": query_user,
            "assistant": query_assistant
        }

        # create message
        message = [shot, query]
        return message
