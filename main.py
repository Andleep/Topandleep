from flask import Flask, render_template, request, redirect
from bot import AIONBot

app = Flask(__name__)
bot = AIONBot()  # تهيئة البوت

@app.route('/')
def dashboard():
    data = bot.get_dashboard_data()
    return render_template('dashboard.html', data=data)

@app.route('/execute_trade', methods=['POST'])
def execute_trade():
    bot.execute_trade()
    return redirect('/')

@app.route('/run_simulation', methods=['POST'])
def run_simulation():
    bot.run_simulation()
    return redirect('/')

@app.route('/toggle_mode', methods=['POST'])
def toggle_mode():
    bot.toggle_mode()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
