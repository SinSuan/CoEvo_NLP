""" other functions
"""
from pathlib import Path
from datetime import datetime
import pytz

from modules.utils.get_config import get_config
CONFIG = get_config()
# DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]
DEBUGGER = "False"    # 可以單獨關掉這個檔案的 DEBUGGER

def list_direct_files(directory):
    """ 列出資料夾下所有直屬文件名。
    Var
        directory: str
            目標資料夾的路徑。

    Returns
        ttl_file: list
        ttl_dir: list
    """
    if DEBUGGER=="True": print("enter list_direct_files")

    directory = Path(directory)
    try:
        # 使用 os.listdir 獲取資料夾中的所有項目
        ttl_item = list(directory.iterdir())
        # 過濾出文件項目
        ttl_file = [item for item in ttl_item if item.is_file()]
        ttl_file = sorted(ttl_file)
        ttl_dir = [item for item in ttl_item if item.is_dir()]
        ttl_dir = sorted(ttl_dir)
    except Exception as e:
        # print(f"An error occurred: {e}")
        # ttl_file = []
        # ttl_dir = []
        raise ValueError(e)
    
    if DEBUGGER=="True": print("leave list_direct_files")
    return ttl_file, ttl_dir

def get_unique_file(directory):
    """ 取得 "唯一" 的文件名
    """
    if DEBUGGER=="True": print("enter get_unique_file")

    ttl_file, ttl_dir = list_direct_files(directory)
    if ttl_dir != [] or len(ttl_file) > 1:
        raise ValueError(f"directory {directory} has more than one file")

    if len(ttl_file) == 0:
        raise FileNotFoundError(f"directory {directory} has no file")

    path = ttl_file[0]

    if DEBUGGER=="True": print("leave get_unique_file")
    return path

def split_by_parent(population):
    """ 為 population_contr 寫的函數
    當 parent 有兩個的時候，依照 pair_new 落於的區間，將 populaiton 分為三個部分
    """
    split_population = {
        "low": [],
        "mid": [],
        "high": [],
        "known": [],
    }
    for pair in population:
        pair.pop("data_sick")
        score_child = pair["train_score"]
        if "info" not in pair:
            split_population["known"].append(pair)
        else:
            score_better = pair["info"]["parent"]["p_better"]["train_score"]
            score_normal = pair["info"]["parent"]["p_normal"]["train_score"]
            if score_child < score_normal:
                split_population["low"].append(pair)
            if score_child > score_better:
                split_population["high"].append(pair)
            else:
                split_population["mid"].append(pair)
    
    return split_population

def time_now():
    """ 取得台灣現在的時間，格式為 YYYY_MMDD_HHMM
    """

    # Define the timezone for Taiwan
    taiwan_tz = pytz.timezone('Asia/Taipei')

    # Get the current time in Taiwan timezone
    taiwan_time = datetime.now(taiwan_tz)

    time_formatted = taiwan_time.strftime('%Y_%m%d_%H%M')

    return time_formatted
