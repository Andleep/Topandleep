from flask import Flask, render_template, request, jsonify
from hybrid_bot_engine import AIONHybridBot
import os
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

app = Flask(__name__)
bot = AIONHybridBot()

@app.route('/')
def dashboard():
    stats = bot.get_performance_stats()
    trades = bot.get_recent_trades()
    progress = bot.get_progress_data()
    
    return render_template(
        "dashboard.html",
        stats=stats,
        trades=trades,
        progress=progress,
        balance=bot.balance
    )

@app.route('/start', methods=['POST'])
def start_bot():
    data = request.json
    api_key = data.get('api_key') or os.getenv('BINANCE_API_KEY')
    api_secret = data.get('api_secret') or os.getenv('BINANCE_API_SECRET')
    mode = data.get('mode', 'DEMO')
    
    if bot.set_keys(api_key, api_secret, mode):
        result = bot.start_trading()
        return jsonify({
            "status": result,
            "mode": mode,
            "target": f"${bot.target_balance}",
            "timeline": f"{bot.days_remaining} يوم"
        })
    else:
        return jsonify({"error": "❌ فشل في تعيين المفاتيح"}), 400

@app.route('/stop', methods=['POST'])
def stop_bot():
    result = bot.stop_trading()
    return jsonify({"status": result})

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    start_date = data.get('start_date', '2024-01-01')
    end_date = data.get('end_date', '2024-01-31')
    
    result = bot.run_advanced_simulation(start_date, end_date)
    return jsonify(result)

@app.route('/stats')
def get_stats():
    return jsonify(bot.get_performance_stats())

@app.route('/progress')
def get_progress():
    return jsonify(bot.get_progress_data())

@app.route('/trades')
def get_trades():
    return jsonify(bot.get_recent_trades())

@app.route('/live-trades')
def get_live_trades():
    return jsonify(bot.get_live_trades())

@app.route('/balance-history')
def get_balance_history():
    return jsonify(bot.get_balance_history())

@app.route('/intelligence')
def get_intelligence():
    stats = bot.get_performance_stats()
    return jsonify(stats['adaptive_intelligence'])

@app.route('/test-connection', methods=['POST'])
def test_connection():
    """اختبار الاتصال بـ Binance"""
    try:
        data = request.json
        api_key = data.get('api_key')
        api_secret = data.get('api_secret')
        mode = data.get('mode', 'DEMO')
        
        # اختبار الاتصال
        from binance.client import Client
        client = Client(api_key, api_secret, testnet=(mode=='DEMO'))
        
        # جلب معلومات الحساب
        account_info = client.get_account()
        
        return jsonify({
            "status": "success",
            "message": "✅ الاتصال بنجاح بـ Binance Testnet",
            "can_trade": account_info.get('canTrade', False),
            "balances": len(account_info.get('balances', [])),
            "server_time": client.get_server_time()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"❌ فشل الاتصال: {str(e)}"
        }), 400

@app.route('/debug-info')
def get_debug_info():
    """معلومات التصحيح"""
    debug_info = {
        "bot_running": bot.running,
        "client_connected": bot.client is not None,
        "total_trades": len(bot.trades),
        "live_trades": len(bot.live_trades),
        "last_trade_time": bot.trades[-1]['timestamp'] if bot.trades else "لا توجد صفقات",
        "current_balance": bot.balance,
        "api_keys_set": bot.api_key is not None and bot.api_secret is not None
    }
    return jsonify(debug_info)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=True)
