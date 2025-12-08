import os
from pathlib import Path
from vllm import LLM, SamplingParams
from modules.evolution.blocks.call_model.vllm.chat_templater.templates import CHAT_TEMPLATE
from modules.utils.get_config import get_folder_project

from modules.utils.get_config import get_config
CONFIG = get_config()
DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]

class vLLM:
    def __init__(self, full_name_model:str, gpu:int) -> None:
        """
        Var:
            full_name_model: str
                Full name of the model to be loaded
            gpu: int
                the index of GPU to be used
        """
        if DEBUGGER=="True": print("enter LLM.__init__")

        self.full_name_model = full_name_model
        folder_project = Path(get_folder_project())
        if full_name_model == "google/gemma-3-1b-it":
            path_model = str(folder_project / "model/google/models--google--gemma-3-1b-it/snapshots/dcc83ea841ab6100d6b47a070329e1ba4cf78752")
        else:
            path_model = str(folder_project / "model" / full_name_model)

        # load model
        os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu)
        self.model = LLM(model=path_model)
        
        # set chat template
        for key, value in CHAT_TEMPLATE.items():
            if key in full_name_model:
                self.chat_template = value
                break

        self.check_available_gpu()

        if DEBUGGER=="True": print("leave LLM.__init__")

    def check_available_gpu(self):
        if DEBUGGER=="True": print("enter LLM.check_available_gpu")

        # ttl_message_pair = [
        #     {
        #         "user": "say '***the LLM is available!***'",
        #         "assistant": ""
        #     }
        # ]
        # reply = self.generate_bbh_mistral(ttl_message_pair, temperature=None, max_new_tokens=10)
        reply = self.generate_basic("say '***the LLM is available!***'", temperature=0, max_new_tokens=10)
        print(f"{reply=}")

        if DEBUGGER=="True": print("leave LLM.check_available_gpu")

    def imitate_chat_template(self, ttl_message_pair: list, continue_final_message: bool):
        prompt = self.chat_template["prefix"]
        template_dialog = self.chat_template["user"] + self.chat_template["assistant"] + self.chat_template["suffix_assistant"]
    
        for message_pair in ttl_message_pair:
            prompt += template_dialog.format(
                text_user=message_pair["user"],
                text_assistant=message_pair["assistant"]
            )
        
        # remove the special token in assistant's message for ending
        if continue_final_message is True:
            prompt = prompt[:-len(self.chat_template["suffix_assistant"])]

        return prompt

    # def imitate_chat_template(self, ttl_message_pair):
    #     """
    #     Var:
    #         ttl_message_pair: list[dict]
    #             {
    #                 "user": str,
    #                 "assistant": str
    #             }
    #     Return:
    #         prompt: str
    #     """
    #     if DEBUGGER=="True": print("enter LLM.imitate_chat_template")

    #     prompt = "<s>"
    #     for message_pair in ttl_message_pair:
    #         prompt += f"[INST] {message_pair['user']} [/INST] {message_pair['assistant']} </s>"
    #     prompt = prompt[:-5]    # remove the last "</s>"

    #     if DEBUGGER=="True": print("leave LLM.imitate_chat_template")
    #     return prompt

    # def generate_bbh_mistral(self, ttl_message_pair, temperature, max_new_tokens):
    #     if DEBUGGER=="True": print("enter LLM.generate_bbh_mistral")
    #     do_sample = temperature != None

    #     prompt = self.imitate_chat_template(ttl_message_pair)
    #     inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
    #     len_input = len(inputs['input_ids'][0])

    #     outputs = self.model.generate(**inputs, do_sample=do_sample, temperature=temperature, max_new_tokens=max_new_tokens, pad_token_id=self.tokenizer.eos_token_id)
    #     outputs_new_tokens = outputs[0][len_input:]
    #     reply = self.tokenizer.decode(outputs_new_tokens, skip_special_tokens=True) # special_tokens 指 </s>

    #     if DEBUGGER=="True": print("leave LLM.generate_bbh_mistral")
    #     return reply

    def generate(self, ttl_prompt_full: list, temperature, max_new_tokens):
        if DEBUGGER=="True": print("enter LLM.generate")
        params_sampling = SamplingParams(temperature=temperature, max_tokens=max_new_tokens)

        outputs = self.model.generate(ttl_prompt_full, params_sampling)
        reply = []
        for output in outputs:
            text = output.outputs[0].text.strip()
            reply.append(text)
        return reply
    
    def generate_basic(self, prompt_user, temperature, max_new_tokens):
        prompt_full = f"<s>[INST] {prompt_user} [/INST]"
        reply = self.generate(prompt_full, temperature, max_new_tokens)
        return reply
    
    def generate_bbh_mistral(self, all_ttl_message_pair, temperature, max_new_tokens):
        ttl_prompt_full = []
        for ttl_message_pair in all_ttl_message_pair:
            prompt_full = self.imitate_chat_template(ttl_message_pair, continue_final_message=True)
            # print(f"{prompt_full=}")
            ttl_prompt_full.append(prompt_full)
        reply = self.generate(ttl_prompt_full, temperature, max_new_tokens)
        return reply

class NoneLLM:
    full_name_model = None
