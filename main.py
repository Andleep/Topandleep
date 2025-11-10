from flask import Flask, render_template, request, jsonify
from bot import AIONBot

app = Flask(__name__)
bot = AIONBot()

@app.route("/")
def dashboard():
    return render_template("dashboard.html", balance=bot.balance, trades=bot.trades)

@app.route("/start_trading", methods=["POST"])
def start_trading():
    bot.start_trading()
    return jsonify({"status": "started"})

@app.route("/stop_trading", methods=["POST"])
def stop_trading():
    bot.stop_trading()
    return jsonify({"status": "stopped"})

@app.route("/simulate", methods=["POST"])
def simulate():
    bot.run_simulation()
    return jsonify({"status": "simulation_done", "trades": bot.trades})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
