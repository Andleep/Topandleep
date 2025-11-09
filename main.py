from trading_bot import TradingBot
from simulator import Simulator
from flask import Flask, render_template
from config import TRADING_MODE

app = Flask(__name__)
bot = TradingBot()
sim = Simulator()

@app.route("/")
def dashboard():
    trades = bot.trade_log
    return render_template("dashboard.html", trades=trades, balance=round(bot.balance,2))

@app.route("/simulate")
def simulate():
    results = sim.run_simulation()
    return render_template("dashboard.html", trades=results, balance=results[-1]["balance"])

if __name__ == "__main__":
    print(f"🚀 AION Quantum Supreme v9 is running in {TRADING_MODE} mode!")
    app.run(host="0.0.0.0", port=5000)
