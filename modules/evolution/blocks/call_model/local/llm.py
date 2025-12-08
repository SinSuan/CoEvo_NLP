from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer
from modules.utils.get_config import get_folder_project

from modules.utils.get_config import get_config
CONFIG = get_config()
DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]

class LLM:
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
        path_model = str(folder_project / "model" / full_name_model)

        # load model
        tokenizer = AutoTokenizer.from_pretrained(path_model)
        # tokenizer.pad_token_id = tokenizer.eos_token_id
        self.tokenizer = tokenizer
        self.model = AutoModelForCausalLM.from_pretrained(path_model, device_map=f"cuda:{gpu}")

        self.check_available_gpu()

        if DEBUGGER=="True": print("leave LLM.__init__")

    def imitate_chat_template(self, ttl_message_pair):
        """
        Var:
            ttl_message_pair: list[dict]
                {
                    "user": str,
                    "assistant": str
                }
        Return:
            prompt: str
        """
        if DEBUGGER=="True": print("enter LLM.imitate_chat_template")

        prompt = "<s>"
        for message_pair in ttl_message_pair:
            prompt += f"[INST] {message_pair['user']} [/INST] {message_pair['assistant']} </s>"
        prompt = prompt[:-5]    # remove the last "</s>"

        if DEBUGGER=="True": print("leave LLM.imitate_chat_template")
        return prompt

    def generate_bbh_mistral(self, ttl_message_pair, temperature, max_new_tokens):
        if DEBUGGER=="True": print("enter LLM.generate_bbh_mistral")
        do_sample = temperature != None

        prompt = self.imitate_chat_template(ttl_message_pair)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        len_input = len(inputs['input_ids'][0])

        outputs = self.model.generate(**inputs, do_sample=do_sample, temperature=temperature, max_new_tokens=max_new_tokens, pad_token_id=self.tokenizer.eos_token_id)
        outputs_new_tokens = outputs[0][len_input:]
        reply = self.tokenizer.decode(outputs_new_tokens, skip_special_tokens=True) # special_tokens 指 </s>

        if DEBUGGER=="True": print("leave LLM.generate_bbh_mistral")
        return reply

    def check_available_gpu(self):
        if DEBUGGER=="True": print("enter LLM.check_available_gpu")

        ttl_message_pair = [
            {
                "user": "say '***the LLM is available!***'",
                "assistant": ""
            }
        ]
        reply = self.generate_bbh_mistral(ttl_message_pair, temperature=None, max_new_tokens=10)
        print(f"{reply=}")

        if DEBUGGER=="True": print("leave LLM.check_available_gpu")

    def generate(self, prompt, temperature, max_new_tokens):
        if DEBUGGER=="True": print("enter LLM.generate")
        do_sample = temperature != 0

        inputs = f"<s>[INST] {prompt} [/INST]"
        inputs = self.tokenizer(inputs, return_tensors="pt").to(self.model.device)
        len_input = len(inputs['input_ids'][0])

        outputs = self.model.generate(**inputs, do_sample=do_sample, temperature=temperature, max_new_tokens=max_new_tokens, pad_token_id=self.tokenizer.eos_token_id)
        outputs_new_tokens = outputs[0][len_input:]
        reply = self.tokenizer.decode(outputs_new_tokens, skip_special_tokens=True)
        return reply
    
    def generate2(self, prompt, temperature, max_new_tokens):
        if DEBUGGER=="True": print("enter LLM.generate")
        do_sample = temperature != 0

        inputs = prompt
        self.tokenizer.pad_token = self.tokenizer.eos_token
        inputs = self.tokenizer(inputs, return_tensors="pt", padding=True).to(self.model.device)
        len_input = len(inputs['input_ids'][0])

        outputs = self.model.generate(**inputs, do_sample=do_sample, temperature=temperature, max_new_tokens=max_new_tokens, pad_token_id=self.tokenizer.eos_token_id)
        # outputs_new_tokens = outputs[0][len_input:]
        # reply = self.tokenizer.decode(outputs_new_tokens, skip_special_tokens=True)
        # return reply
        reply = self.tokenizer.decode(outputs, skip_special_tokens=True)
        return reply
        

class NoneLLM:
    full_name_model = None
