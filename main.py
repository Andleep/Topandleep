from trading_bot import AIONQuantumTrader
import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
MODE = os.getenv("MODE", "PAPER")  # PAPER = تجريبي, REAL = حقيقي

bot = AIONQuantumTrader(api_key=API_KEY, api_secret=API_SECRET, mode=MODE)

# تشغيل البوت في الخلفية
import threading
threading.Thread(target=bot.start_trading, daemon=True).start()

# إنشاء خادم ويب صغير لتوافق Render
app = Flask(__name__)

@app.route("/")
def home():
    return "🚀 AION Quantum Supreme v6.0 is running!"

if __name__ == "__main__":
    # Render يحدد PORT عبر متغير البيئة
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
