from flask import Flask, render_template, request, redirect, url_for
from bot import AIONBot
import os

app = Flask(__name__)

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

bot = AIONBot(API_KEY, API_SECRET, mode="PAPER")

@app.route("/")
def dashboard():
    return render_template("dashboard.html", bot=bot)

@app.route("/execute_trade")
def execute_trade():
    bot.trade()
    return redirect(url_for("dashboard"))

@app.route("/run_simulation")
def run_simulation():
    bot.run_simulation()
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
