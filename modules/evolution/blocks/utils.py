from modules.utils.get_config import get_config
CONFIG = get_config()
DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]


def prompt_in_list(prompt, population):
    """
    Var
        prompt: str
            the prompt to be check whether or not the in population

        population: List[Dict]
            list of "{'prompt': prompt, ...}"
    """
    if DEBUGGER=="True": print("enter prompt_in_list")

    # 預設不在
    in_list = False
    # 然後檢查
    for pair in population:
        if pair['prompt'] == prompt:
            in_list = True
            break

    if DEBUGGER=="True": print("exit prompt_in_list")
    return in_list

def sort_by_key(dictionary, key:str="train_score"):
    """ sort dictionary by key in descending order
    """
    dictionary_sorted = sorted(dictionary, key=lambda x: x[key], reverse=True)
    return dictionary_sorted
