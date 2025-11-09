# simulator/backtest.py
from utils.trading import TradingBot
import random

class Backtester:
    def __init__(self, bot: TradingBot):
        self.bot = bot

    def run(self):
        # محاكاة بسيطة على 100 صفقة
        for _ in range(100):
            self.bot.run_live_trade()
