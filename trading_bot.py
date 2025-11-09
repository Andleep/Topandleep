from strategy import StrategyManager
from utils import load_json, save_json
from config import LOG_PATH, POSITION_SIZE_PERCENT, BASE_CURRENCY
import random
import os

class TradingBot:
    def __init__(self, balance=50):
        self.balance = balance
        self.strategy_manager = StrategyManager()
        self.trade_log = load_json(LOG_PATH)
        if not self.trade_log:
            self.trade_log = []

    def execute_trade(self):
        strategy = self.strategy_manager.select_strategy()
        position_size = self.balance * (POSITION_SIZE_PERCENT/100)
        profit = position_size * random.uniform(-0.02, 0.08)  # خسارة أو ربح
        self.balance += profit
        trade = {"strategy": strategy, "position_size": position_size, "profit": round(profit,2), "balance": round(self.balance,2)}
        self.trade_log.append(trade)
        save_json(self.trade_log, LOG_PATH)
        self.strategy_manager.update_strategy(strategy, profit)
        return trade
