import json
from pathlib import Path
from time import time
from typing import Union
import requests

from modules.execution.blocks.utils import time_now
from modules.utils.get_config import get_config, get_folder_project
from modules.utils.tools import list_direct_files
CONFIG = get_config()
DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]
JUPYTER = CONFIG["DEBUGGER"]["JUPYTER"]

# URL = CONFIG["breeze"]["lab"]
# SUGGEST_SYSTEM_PROMPT = CONFIG["breeze"]["SUGGEST_SYSTEM_PROMPT"]

def create_unique_file_name(stem:str):
    version = 0
    
    path = Path(f"{stem}_{version:04d}.json")
    while path.exists():
        path = Path(f"{stem}_{version:04d}.json")
        version += 1
    return path

def create_unique_folder_name(stem:str):
    version = 0
    
    path = Path(f"{stem}_{version:04d}")
    while path.exists():
        path = Path(f"{stem}_{version:04d}")
        version += 1
    return path

class RecordStream:
    def __init__(self, folder_record, new=True):
        if new is True:
            folder_record = create_unique_folder_name(folder_record)

        folder_record = Path(folder_record)
        if new is True:
            folder_record.mkdir(parents=True, exist_ok=False)
        elif folder_record.exists() is False:
            raise FileNotFoundError(f"⚠️ 資料夾不存在：{folder_record}")
        self.folder_record = folder_record

    def clean(self):
        for file in self.folder_record.iterdir():
            file.unlink()

    def record(self, data:Union[dict, str]):
        t = time_now()
        # file = self.folder_record / f"{t}.json"
        path = f"{self.folder_record}/{t}"
        path_unique = create_unique_file_name(path)
        
        with open(path_unique, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    def concat(self):
        reply = ""
        ttl_file, _ = list_direct_files(self.folder_record)
        for file in ttl_file[1:-1]:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
            token = data["token"]["text"]
            reply += token
        return reply


class CallTGI:
    """ call tgi to:
        1. tokenize     return the tokenized prompt
        2. count_token  return the number of tokens in the prompt
        3. generate     return the generated text
    """

    def __init__(self, full_name_model:str) -> None:
        """
        Var
            full_name_model: str
                the full name of the model

            host: str
                the host url of the tgi
                prefix: "http://"
        
        Attribute
            host: str
                the host url of the tgi
                prefix: "http://"

            headers: dict
                the headers of the request
        """
        if DEBUGGER=="True": print(f"\tenter CallTGI.__init__")

        self.full_name_model = full_name_model
        self.num_token_prefix = self.get_num_token_prefix()

        self.host = CONFIG["URL"]["lab"]

        self.headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        }

        if DEBUGGER=="True": print(f"\tleave CallTGI.__init__")

    def get_num_token_prefix(self):
        """
        Var:
            full_name_model: str
                the full name of the model

        ------
        Return:
            int
        """
        switcher = {
            "llama": 35,
            "mistral": 8
        }

        full_name_model_lower = self.full_name_model.lower()

        num_token_prefix = 0
        for model, num in switcher.items():
            if model in full_name_model_lower:
                num_token_prefix = num
                break
        return num_token_prefix

    def tokenize(self, prompt):
        if DEBUGGER=="True": print(f"\tenter CallTGI.tokenize")

        url = f"{self.host}/tokenize"
        parameter = {
            "max_new_tokens": 0,
            "apply_chat_template": True
        }
        data = {
            "inputs": prompt,
            "parameters": parameter
        }
        data = json.dumps(data)
        
        response = requests.post(url, data=data, headers=self.headers)

        if DEBUGGER=="True": print(f"\tleave CallTGI.tokenize")
        return response

    def count_token(self, prompt):
        """ count the number of tokens in the prompt
        """
        if DEBUGGER=="True": print(f"\tenter CallTGI.count_token")

        try:
            response = self.tokenize(prompt)
            response = response.json()
            num_token = len(response)
        except Exception as e:
            raise ValueError(f"Except in CallTGI.count_token: fail to count toke\n{e}")

        if DEBUGGER=="True": print(f"\tleave CallTGI.count_token")
        return num_token

    def naive_propmt(self, user_prompt):
        prompt = f"<s> [INST] {user_prompt} [/INST]"
        return prompt

    def naive_prompt_breeze(self, user_prompt):
        prompt = f"<s> {SUGGEST_SYSTEM_PROMPT} [INST] {user_prompt} [/INST]"
        return prompt

    def imitate_chat_template(self, ttl_message_pair):
        prompt = "<s>"
        for message_pair in ttl_message_pair:
            prompt += f"[INST] {message_pair['user']} [/INST] {message_pair['assistant']} </s>"
        prompt = prompt[:-5]    # remove the last "</s>"
        return prompt

    def generate(self, user_prompt, temperature=None, max_new_tokens=1000):
        """ for breeze or mistrial
        """
        if DEBUGGER=="True": print(f"\tenter CallTGI.generate")
        url = f"{self.host}/generate"

        # prompt = self.naive_prompt_breeze(user_prompt)
        prompt = self.naive_propmt(user_prompt)
        num_token_input = self.count_token(prompt)
        max_new_tokens = min(max_new_tokens, 8192-num_token_input)

        parameter = {
            "do_sample": temperature is not None,
            "max_new_tokens": max_new_tokens,
            "temperature": temperature
        }
        
        data = {
            "inputs": prompt,
            "parameters": parameter
        }
        data = json.dumps(data)
        # response = requests.post(url, data=data, headers=self.headers)
        # return response
        try:
            response = requests.post(url, headers=self.headers, data=data)
            j_result = response.json()
            if "generated_text" in j_result.keys():
                r = j_result['generated_text']
            else:
                r = j_result
        except Exception as e:
            print(f"{prompt=}")
            print(f"Except in api_breeze =\n{e}")
            raise e
        return r

    def generate_bbh_mistral(self, ttl_message_pair, temperature, max_new_tokens):
        """ for breeze or mistrial
        Var:
            ttl_message_pair: list[dict]
                {
                    'user': f"Q: {pair['question']}\nA: ",
                    'assistant': f"{os_prompt}\n{pair['cot_answer']}"
                }
        """
        url = f"{self.host}/generate"

        prompt = self.imitate_chat_template(ttl_message_pair)

        # print(prompt)
        # print(f"{prompt=}")
        parameter = {
            "do_sample": temperature is not None,
            "max_new_tokens": max_new_tokens,
            "temperature": temperature
        }

        data = {
            "inputs": prompt,
            "parameters": parameter
        }
        data = json.dumps(data)
        # response = requests.post(url, data=data, headers=self.headers)
        # return response
        try:
            response = requests.post(url, headers=self.headers, json=data, stream=True)
            j_result = response.json()
            # print(f"{j_result=}")
            if "generated_text" in j_result.keys():
                r = j_result['generated_text']
            else:
                r = j_result
        except Exception as e:
            print(f"{prompt=}")
            print(f"Except in generate_bbh_mistral =\n{e}")
            raise e
        return r

    def generate_stream(self, ttl_message_pair, temperature, max_new_tokens):
        url = f"{self.host}/generate_stream"
        
        folder_project = get_folder_project()
        folder_record = folder_project / "data/record/temporary/generate_stream"
        t = time_now()
        recorder = RecordStream( folder_record/f"{t}" , new=True)
        
        recorder.clean()

        prompt = self.imitate_chat_template(ttl_message_pair)
        recorder.record(prompt)    # 紀錄 input

        parameter = {
            "do_sample": temperature is not None,
            "max_new_tokens": max_new_tokens,
            "temperature": temperature
        }

        data = {
            "inputs": prompt,
            "parameters": parameter
        }
        # data = json.dumps(data)
        try:
            with requests.post(url, headers=self.headers, json=data, stream=True, timeout=30) as response:
                for line in response.iter_lines():
                    if line:
                        json_str = line.decode("utf-8").replace("data: ", "")
                        try:
                            token_data = json.loads(json_str)
                            recorder.record(token_data)
                        except json.JSONDecodeError as e:
                            raise ValueError(f"⚠️ JSON 解析錯誤：{e}，內容：{json_str}")
        except requests.exceptions.Timeout:
            raise TimeoutError("⏳ 請求超時（30 秒）！")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"❌ 請求錯誤：{e}")

        r = recorder.concat()
        recorder.record(r)    # 紀錄 output
        return r
        
    def test(self, prompt, temperature, max_new_tokens):
        url = f"{self.host}/generate_stream"
        
        folder_project = get_folder_project()
        folder_record = folder_project / "data/record/temporary/generate_stream"
        t = time_now()
        recorder = RecordStream( folder_record/f"{t}" , new=True)
        
        recorder.clean()

        # prompt = self.imitate_chat_template(ttl_message_pair)
        recorder.record(prompt)    # 紀錄 input

        parameter = {
            "do_sample": temperature is not None,
            "max_new_tokens": max_new_tokens,
            "temperature": temperature
        }

        data = {
            "inputs": prompt,
            "parameters": parameter
        }
        # data = json.dumps(data)
        try:
            with requests.post(url, headers=self.headers, json=data, stream=True, timeout=30) as response:
                for line in response.iter_lines():
                    if line:
                        json_str = line.decode("utf-8").replace("data: ", "")
                        try:
                            token_data = json.loads(json_str)
                            recorder.record(token_data)
                        except json.JSONDecodeError as e:
                            raise ValueError(f"⚠️ JSON 解析錯誤：{e}，內容：{json_str}")
        except requests.exceptions.Timeout:
            raise TimeoutError("⏳ 請求超時（30 秒）！")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"❌ 請求錯誤：{e}")

        r = recorder.concat()
        recorder.record(r)    # 紀錄 output
        return r

    def chat(self, user_prompt, temperature, max_new_tokens):
        """ main function of this class
        """
        if DEBUGGER=="True": print(f"\tenter CallTGI.chat")
        url = f"{self.host}/v1/chat/completions"

        num_token_input = self.count_token(user_prompt)
        max_new_tokens = min(max_new_tokens, 8192-(num_token_input+self.num_token_prefix))
        if DEBUGGER=="True": print(f"\t{max_new_tokens=}")
        parameter = {
            "do_sample": temperature is not None,
            "max_tokens": max_new_tokens,
            "temperature": temperature
        }
        data = {
            "model": self.full_name_model,
            "messages": [
                {"role": "user", "content": user_prompt}
            ]
        }
        data.update(parameter)
        data = json.dumps(data)

        try:
            response = requests.post(url, data=data, headers=self.headers)
            j_result = response.json()
            if "choices" in j_result:
                r = j_result["choices"][0]["message"]["content"]
            else:
                r = j_result
        except Exception as e:
            print(f"{user_prompt=}")
            print(f"Except in api_breeze =\n{e}")
            raise e
        return r

    def chat_bbh(self, messages, temperature, max_new_tokens):
        """ 
        Var:
            ttl_qa_pair: list[dict]
                dict is of the form:
                    {
                        "system": task_description,
                        "qa_pair": list[dict]
                            dict is of the form:
                                {
                                    "user": "Q: ...\nA: {os_prompt}\n",
                                    "assistant": "... . So the answer is {answer}."
                                }
                    }
        """
        if DEBUGGER=="True": print(f"\tenter CallTGI.chat")
        url = f"{self.host}/v1/chat/completions"

        parameter = {
            "do_sample": temperature is not None,
            "max_tokens": max_new_tokens,
            "temperature": temperature
        }

        data = {
            "model": self.full_name_model,
            "messages": messages,
            "instruction_template":"Mistral"
        }
        data.update(parameter)
        data = json.dumps(data)

        try:
            response = requests.post(url, data=data, headers=self.headers)
            j_result = response.json()
            if "choices" in j_result:
                r = j_result["choices"][0]["message"]["content"]
            else:
                r = j_result
        except Exception as e:
            print(f"Except in api_breeze =\n{e}")
            raise e
        return r

class NoneTGI:
    full_name_model = None
