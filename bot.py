import time
from binance.client import Client
from binance.enums import *

class AIONBot:
    def __init__(self):
        self.balance = 50.0  # الرصيد المبدئي
        self.trades = []  # سجل الصفقات
        self.trading = False
        self.client = Client(api_key="fUPhEYky7xhJGJKlzG2djaWfcwQCUEIs7jIWiySLdd0e9bnJeUA9pfg2XKbjnv7y", api_secret="fSYeBIPnL6GzMchmLF6GB8dUNWjYCdxCnv8R9GpVEk4AixeD6d3gLRJrJSQOCaeO", testnet=True)

    def start_trading(self):
        self.trading = True
        # تشغيل حلقة التداول المباشر في الخلفية
        import threading
        threading.Thread(target=self._trading_loop, daemon=True).start()

    def stop_trading(self):
        self.trading = False

    def _trading_loop(self):
        while self.trading:
            # مثال على تداول وهمي لحساب الرصيد
            trade = {"strategy": "scalping", "position_size": 2.5, "profit": 0.1, "balance": self.balance + 0.1}
            self.trades.append(trade)
            self.balance += 0.1
            time.sleep(2)  # تأخير 2 ثانية بين كل صفقة

    def run_simulation(self):
        self.trades = []
        for i in range(10):
            trade = {"strategy": "simulation", "position_size": 2.0, "profit": 0.2, "balance": self.balance + 0.2}
            self.trades.append(trade)
            self.balance += 0.2
