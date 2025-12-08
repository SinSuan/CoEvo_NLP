class Terminator:
    def __init__(self, target_score, target_iteration):
        self.target_score = target_score
        self.target_iteration = target_iteration
        self.idx_iteration = 0  # 因為 framework 會先儲存最初的狀態，所以從 0 開始
    
    def is_terminated(self, score):
        achieve_score = score >= self.target_score
        achieve_iteration = self.idx_iteration > self.target_iteration
        is_terminated = achieve_score or achieve_iteration
        return is_terminated