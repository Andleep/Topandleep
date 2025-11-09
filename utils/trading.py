# utils/trading.py
import random

class TradingBot:
    def __init__(self, balance, trade_percent, max_positions):
        self.balance = balance
        self.trade_percent = trade_percent
        self.max_positions = max_positions
        self.trades = []
        self.mode = "PAPER"
        self.learned_strategies = []

    def run_live_trade(self):
        # هذه نسخة مبسطة، لاحقًا ستربط بباينانس مباشرة
        trade_amount = self.balance * self.trade_percent / 100
        profit = trade_amount * random.uniform(-0.02, 0.08)  # ربح/خسارة عشوائي
        self.balance += profit
        self.trades.append({
            "strategy": random.choice(["scalping", "momentum", "mean_reversion"]),
            "position_size": trade_amount,
            "profit": profit,
            "balance": self.balance
        })
        self.learned_strategies.append("تعلم من الصفقة الأخيرة")

    def learning_progress(self):
        return len(self.learned_strategies)
