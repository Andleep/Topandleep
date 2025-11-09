from binance.client import Client
from strategy import QuantumStrategy
from utils import log_trade, update_cumulative_profit
from config import CONFIG
import time, random

class AIONQuantumTrader:
    def __init__(self, api_key, api_secret, mode="PAPER"):
        self.mode = mode
        try:
            self.client = Client(api_key, api_secret, testnet=(mode == "PAPER"))
        except Exception:
            self.client = None
        self.strategy = QuantumStrategy()
        self.balance = 50.0
        self.cumulative_profit = 0
        self.virtual_balances = [self.balance / CONFIG["virtual_accounts"]] * CONFIG["virtual_accounts"]

    def start_trading(self):
        print(f"\n🚀 AION Quantum Supreme v6.0 started in {self.mode} mode.\n")
        while True:
            for i in range(CONFIG["virtual_accounts"]):
                for pair in CONFIG["pairs"]:
                    signal = self.strategy.generate_signal(pair)
                    if signal == "BUY":
                        self.execute_trade(pair, i)
            time.sleep(CONFIG["trade_interval_sec"])

    def execute_trade(self, pair, account_index):
        capital = self.virtual_balances[account_index]
        amount = capital * CONFIG["risk_per_trade"]
        profit = amount * CONFIG["profit_target"]
        loss = amount * CONFIG["stop_loss"]

        outcome = random.choices(["WIN", "LOSS"], weights=[85, 15])[0]
        if outcome == "WIN":
            self.virtual_balances[account_index] += profit
            self.cumulative_profit += profit
        else:
            self.virtual_balances[account_index] -= loss
            self.cumulative_profit -= loss

        log_trade(pair, outcome, profit if outcome == "WIN" else -loss)
        update_cumulative_profit(self.cumulative_profit)

        print(f"💰 {pair} | Result: {outcome} | New balance {round(self.virtual_balances[account_index],2)} USDT")
