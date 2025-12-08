import numpy as np

from modules.utils.get_config import get_config
CONFIG = get_config()
DEBUGGER = CONFIG["DEBUGGER"]["DEBUGGER"]

# for selectors.py
def get_weight(ttl_score):
    """ GA 抽樣使用輪盤法 (Roulette Wheel Selection)
    """
    ttl_weight = np.array(ttl_score, dtype=float)
    if np.sum(ttl_weight!=0)<=1:
        ttl_weight[ttl_weight==0]=0.01  # 權重 0 的話會抽不到

    ttl_weight = ttl_weight/np.sum(ttl_weight)
    return ttl_weight
