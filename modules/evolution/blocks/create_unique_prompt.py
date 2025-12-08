"""
generate an unique prompt from population and population_temp
"""

from copy import deepcopy
import re
# from modules.evolution.blocks.call_model.llm import CallTGI
from modules.evolution.blocks.call_model.local.llm import LLM
from modules.evolution.blocks.utils import prompt_in_list
from modules.utils.get_config import get_config
CONFIG = get_config()
DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]

def prompt_is_bad(match_all):
    return match_all == [] or match_all[-1].strip() == "and"

def create_prompt(prompt_4_create_new_os_prompt, llm: LLM, temperature):
    """ call model 並 用正則表達抓 <prompt>[/PROMPT]間的字
    Var
        temperature:
            EvoPrompt 論文的溫度設 0.5
    """
    if DEBUGGER=="True": print("enter generate_prompt")

    num_try = 0
    reply = ""
    match_all = []
    # while match_all==[] or match_all[-1]==" and ":
    while prompt_is_bad(match_all) is True:
        num_try += 1
        print(f"**fail to generate prompt**\n{num_try=}\t{reply=}")
        # 沒有 special token: <prompt>, </prompt>
        # 有時候會生出 " and " 這樣的 prompt
        # reply = llm.chat(prompt_4_create_new_os_prompt, temperature, 1000)
        # reply = llm.generate_bbh_mistral(prompt_4_create_new_os_prompt, temperature, 1000)
        response = llm.generate_bbh_mistral([prompt_4_create_new_os_prompt], temperature, 1000)
        reply = response[0]
        # reply = llm.generate_stream(prompt_4_create_new_os_prompt, temperature, 1000)
        match_all = re.findall(r'<prompt>(.*?)</prompt>', reply, re.DOTALL)
        if prompt_is_bad(match_all) is True:    # for gemma-3-1b-it
            # match_all = re.findall(r'Worse Prompt:(.*?)</prompt>', reply, re.DOTALL)
            match_all = re.findall(r'“(.*?)”', reply, re.DOTALL)

    new_prompt = match_all[-1].strip()

    if DEBUGGER=="True": print("leave generate_prompt")
    return new_prompt, reply

def create_unique_prompt(population_current, prompt_4_create_new_os_prompt, llm):
    """ 用來確保 new_prompt 不在 population 裡
    Var
        temperature:
            EvoPrompt 論文的溫度設 0.5
        
        for_debug:
            用來 debug 的參數

    """
    if DEBUGGER=="True": print("enter generate_unique_prompt")
    # 嘗試生出新的 prompt
    num_prompt = len(population_current)
    # print(population_current)

    # 溫度設最高之後給 pop 裡的每個參數各一次機會
    # temperature 升到 1.0 都有重複，old pop 跟 new pop 裡的每個 prompt 都生過一次，最後再試一次（類似鴿籠原理）
    num_try = num_prompt + 1

    temperature = 1

    population_history = []
    new_prompt, reply = create_prompt(prompt_4_create_new_os_prompt, llm, temperature)
    population_history.append(new_prompt)
    is_exist = prompt_in_list(new_prompt, population_current)
    # while num_try > 0 and is_exist is True:
    while is_exist is True:
        print(f"【try to generate unique prompt】, {num_try=}")
        new_prompt, reply = create_prompt(prompt_4_create_new_os_prompt, llm, temperature)
        population_history.append(new_prompt)
        is_exist = prompt_in_list(new_prompt, population_current)
        num_try -= 1

    # 如果經過 num_try 次還是重複，就 raise error
    if prompt_in_list(new_prompt, population_current) is True:
        population_current = deepcopy(population_current)
        population_current = [pair['prompt'] for pair in population_current]
        print(f"{population_current=}\n")
        print(f"{population_history=}\n")
        print(f"{prompt_4_create_new_os_prompt=}\n")
        # raise Exception("can't generate unique prompt")
        new_prompt, reply = None, None

    if DEBUGGER=="True": print("leave generate_unique_prompt")
    return new_prompt, reply