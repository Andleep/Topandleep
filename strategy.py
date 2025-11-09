import random
from utils import load_json, save_json
from config import STRATEGY_PATH

class StrategyManager:
    def __init__(self):
        self.stats = load_json(STRATEGY_PATH)

    def select_strategy(self):
        # اختيار استراتيجية بشكل عشوائي (تطوير لاحق: تعلم ذاتي)
        return random.choice(["scalping", "momentum", "mean_reversion"])

    def update_strategy(self, strategy, profit):
        if strategy not in self.stats:
            self.stats[strategy] = {"trades": 0, "profit": 0}
        self.stats[strategy]["trades"] += 1
        self.stats[strategy]["profit"] += profit
        save_json(self.stats, STRATEGY_PATH)
