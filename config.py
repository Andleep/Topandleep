# وضع التداول
TRADING_MODE = "PAPER"  # PAPER للتجريبي، REAL للحساب الحقيقي

# العملة الأساسية وحجم الصفقة
BASE_CURRENCY = "USDT"
POSITION_SIZE_PERCENT = 5  # نسبة كل صفقة من الرصيد

# التعلم الذاتي
LEARNING_RATE = 0.1  # سرعة تعلم البوت
MAX_CONCURRENT_TRADES = 3  # أقصى عدد صفقات متزامنة

# المحاكاة
SIMULATION_DAYS = 30  # عدد أيام المحاكاة الافتراضية

# مسارات الملفات
LOG_PATH = "logs/trade_history.json"
STRATEGY_PATH = "logs/strategy_stats.json"
SIM_PATH = "logs/sim_results/"

# واجهة
PORT = 5000
