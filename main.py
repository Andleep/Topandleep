# main.py
from flask import Flask, render_template, request, redirect
from config import *
from utils.trading import TradingBot
from simulator.backtest import Backtester

app = Flask(__name__)
bot = TradingBot(balance=INITIAL_BALANCE, trade_percent=TRADE_PERCENT, max_positions=MAX_POSITIONS)

@app.route("/")
def dashboard():
    return render_template("dashboard.html",
                           balance=bot.balance,
                           trades=bot.trades,
                           mode=MODE,
                           learning_progress=bot.learning_progress())

@app.route("/execute_trade")
def execute_trade():
    bot.run_live_trade()
    return redirect("/")

@app.route("/run_simulation")
def run_simulation():
    sim = Backtester(bot)
    sim.run()
    return redirect("/")

@app.route("/toggle_mode")
def toggle_mode():
    global MODE
    MODE = "REAL" if MODE == "PAPER" else "PAPER"
    bot.mode = MODE
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
