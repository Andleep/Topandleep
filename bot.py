import os
import time
import math
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException

class AIONBot:
    def __init__(self, api_key, api_secret, mode="PAPER"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.mode = mode.upper()
        
        # ✅ نستخدم Binance Testnet بدل المنصة الحقيقية
        self.client = Client(api_key, api_secret, testnet=True)
        self.client.API_URL = 'https://testnet.binance.vision/api'
        
        self.balance = 50.0
        self.trades = []
        self.strategy_list = ["scalping", "momentum", "mean_reversion"]
        self.position_size = 2.5

    def fetch_price(self, symbol="BTCUSDT"):
        try:
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            return float(ticker['price'])
        except Exception as e:
            print("❌ Error fetching price:", e)
            return None

    def trade(self, symbol="BTCUSDT"):
        strategy = self.choose_strategy()
        price = self.fetch_price(symbol)
        if not price:
            return
        
        position = self.position_size
        profit = round((price * 0.001) * (1 if math.sin(time.time()) > 0 else -1), 3)
        self.balance += profit
        self.balance = round(self.balance, 2)
        
        trade_data = {
            "strategy": strategy,
            "position_size": position,
            "profit": profit,
            "balance": self.balance
        }
        self.trades.append(trade_data)
        print(f"✅ Executed {strategy} trade | Profit: {profit} | Balance: {self.balance}")

    def choose_strategy(self):
        import random
        return random.choice(self.strategy_list)

    def run_simulation(self, symbol="BTCUSDT", steps=10):
        print("🚀 Starting AI simulation...")
        for _ in range(steps):
            self.trade(symbol)
            time.sleep(1)
        print("✅ Simulation finished.")
