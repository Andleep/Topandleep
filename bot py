import json
import os
from binance.client import Client
from datetime import datetime

class AIONBot:
    def __init__(self):
        self.load_config()
        self.client = Client(self.api_key, self.api_secret, testnet=True)  # حساب تجريبي
        self.balance = self.start_balance
        self.trades = []
        self.mode = 'PAPER'  # PAPER = تجريبي، LIVE = حقيقي
        self.load_learning()

    def load_config(self):
        # ضع هنا مفاتيح حسابك التجريبي
        self.api_key = "YOUR_TESTNET_API_KEY"
        self.api_secret = "YOUR_TESTNET_API_SECRET"
        self.start_balance = 50

    def load_learning(self):
        if os.path.exists("learning.json"):
            with open("learning.json", "r") as f:
                self.learning = json.load(f)
        else:
            self.learning = {}

    def save_learning(self):
        with open("learning.json", "w") as f:
            json.dump(self.learning, f)

    def get_dashboard_data(self):
        return {
            "balance": self.balance,
            "trades": self.trades,
            "learning": self.learning
        }

    def execute_trade(self):
        # مثال تنفيذي للتداول
        trade = {
            "strategy": "scalping",
            "position_size": 2.5,
            "profit": 0.1,
            "balance": round(self.balance + 0.1, 2),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.balance = trade["balance"]
        self.trades.append(trade)
        self.update_learning(trade)

    def run_simulation(self):
        # مثال للمحاكاة التاريخية
        for i in range(10):
            trade = {
                "strategy": "momentum",
                "position_size": 2.5,
                "profit": 0.15,
                "balance": round(self.balance + 0.15, 2),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.balance = trade["balance"]
            self.trades.append(trade)
            self.update_learning(trade)

    def toggle_mode(self):
        if self.mode == 'PAPER':
            self.mode = 'LIVE'
        else:
            self.mode = 'PAPER'

    def update_learning(self, trade):
        strategy = trade["strategy"]
        if strategy not in self.learning:
            self.learning[strategy] = {"trades": 0, "profit": 0}
        self.learning[strategy]["trades"] += 1
        self.learning[strategy]["profit"] += trade["profit"]
        self.save_learning()
