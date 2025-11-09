from utils import save_json
from config import SIM_PATH
import random
import os

class Simulator:
    def __init__(self):
        os.makedirs(SIM_PATH, exist_ok=True)

    def run_simulation(self, days=30, initial_balance=50):
        balance = initial_balance
        results = []
        for day in range(days):
            profit = balance * random.uniform(-0.02, 0.08)  # خسارة أو ربح يومي
            balance += profit
            results.append({"day": day+1, "profit": round(profit,2), "balance": round(balance,2)})
        save_json(results, f"{SIM_PATH}/sim_{initial_balance}.json")
        return results
