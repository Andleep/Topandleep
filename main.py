from trading_bot import AIONQuantumTrader
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
MODE = os.getenv("MODE", "PAPER")  # PAPER = تجريبي, REAL = حقيقي

if __name__ == "__main__":
    bot = AIONQuantumTrader(api_key=API_KEY, api_secret=API_SECRET, mode=MODE)
    bot.start_trading()
