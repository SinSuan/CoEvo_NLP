from datetime import datetime
import pytz
import ray

from modules.evolution.blocks.call_model.local.llm import LLM


def time_now():
    """ 取得台灣現在的時間，格式為 YYYY_MMDD_HHMM
    """

    # Define the timezone for Taiwan
    taiwan_tz = pytz.timezone('Asia/Taipei')

    # Get the current time in Taiwan timezone
    taiwan_time = datetime.now(taiwan_tz)

    time_formatted = taiwan_time.strftime('%Y_%m%d_%H%M')

    return time_formatted


@ray.remote
def load_model(full_name_model:str, gpu:int):
    return LLM(full_name_model, gpu)
