from flask import Flask, render_template, request, redirect
from bot import AIONBot

app = Flask(__name__)
bot = AIONBot()  # تهيئة البوت

@app.route("/")
def dashboard():
    return render_template("dashboard.html",
                           balance=bot.balance,
                           trades=bot.trades,
                           learning_rate=bot.learning_rate,
                           strategies=bot.strategy_performance)

@app.route("/start")
def start_trading():
    bot.start_trading()
    return redirect("/")

@app.route("/stop")
def stop_trading():
    bot.stop_trading()
    return redirect("/")

@app.route("/simulate")
def run_simulation():
    start_date = request.args.get("start_date", None)
    end_date = request.args.get("end_date", None)
    bot.run_simulation(start_date, end_date)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
