from flask import Flask, render_template, jsonify, request
from trading_bot import TradingBot
from simulator import Simulator
from config import PORT, TRADING_MODE

app = Flask(__name__)
bot = TradingBot(balance=50)
sim = Simulator()

# الوضع الحالي: تجريبي أو حقيقي
current_mode = TRADING_MODE

@app.route('/')
def dashboard():
    trades = bot.trade_log
    balance = round(bot.balance,2)
    return render_template('dashboard.html', trades=trades, balance=balance, mode=current_mode)

@app.route('/execute_trade', methods=['POST'])
def execute_trade():
    trade = bot.execute_trade()
    return jsonify(trade)

@app.route('/run_simulation', methods=['POST'])
def run_simulation():
    days = int(request.json.get("days",30))
    initial_balance = float(request.json.get("balance",50))
    results = sim.run_simulation(days=days, initial_balance=initial_balance)
    return jsonify(results)

@app.route('/set_mode', methods=['POST'])
def set_mode():
    global current_mode
    mode = request.json.get("mode","PAPER")
    current_mode = mode
    return jsonify({"status":"ok","mode":current_mode})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
