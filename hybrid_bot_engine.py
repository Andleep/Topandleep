import threading
import time
import json
import os
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from binance.client import Client
from indicators import compute_indicators

class AIONHybridBot:
    def __init__(self):
        # 🎯 إعدادات الهدف
        self.initial_balance = 50.0
        self.balance = 50.0
        self.target_balance = 5000.0
        self.days_remaining = 90
        self.start_date = datetime.now()
        
        # 📈 تتبع التاريخ للأداء
        self.balance_history = [{"timestamp": datetime.now().isoformat(), "balance": 50.0}]
        self.performance_history = []
        
        # 🧠 مؤشر الذكاء التكيفي
        self.adaptive_intelligence = {
            "score": 50,  # من 0 إلى 100
            "learning_rate": 0,
            "pattern_recognition": 0,
            "risk_adjustment": 0,
            "market_adaptation": 0
        }
        
        # ⚡ نظام التضاعف الذكي
        self.compounding_factor = 1.08
        self.risk_level = 0.005
        self.trade_size = 2.5
        
        # 📊 المؤشرات الفنية
        self.client = None
        self.running = False
        self.trades = []
        self.live_trades = []  # الصفقات الحية
        
        self.performance = {
            "daily": 0, "weekly": 0, "monthly": 0,
            "total_profit": 0, "win_rate": 0,
            "successful_trades": 0, "total_trades": 0,
            "current_streak": 0
        }
        
        # 🧠 الذاكرة الهجينة
        self.memory = []
        self.strategy_weights = {"momentum": 0.4, "mean_reversion": 0.35, "scalping": 0.25}
        
        self.load_state()
    
    def set_keys(self, api_key, api_secret, mode="DEMO"):
        if api_key and api_secret:
            try:
                self.client = Client(api_key, api_secret, testnet=(mode=="DEMO"))
                return True
            except Exception as e:
                print(f"Error setting keys: {e}")
                return False
        return False
    
    def start_trading(self):
        if not self.running:
            self.running = True
            threading.Thread(target=self.hybrid_trade_loop, daemon=True).start()
            return "✅ بدأ التداول بنجاح"
        return "⚠️ البوت يعمل بالفعل"
    
    def stop_trading(self):
        if self.running:
            self.running = False
            # إغلاق جميع الصفقات الحية
            self.close_all_live_trades()
            return "🛑 تم إيقاف التداول"
        return "ℹ️ البوت متوقف بالفعل"
    
    def close_all_live_trades(self):
        """إغلاق جميع الصفقات الحية وتحديث الأرباح"""
        for trade in self.live_trades:
            trade['status'] = 'CLOSED'
            trade['close_time'] = datetime.now().isoformat()
            # حساب الربح النهائي (محاكاة)
            if trade['profit'] is None:
                trade['profit'] = round(trade['amount'] * 0.015, 2)  # 1.5% ربح
                self.balance += trade['profit']
        self.live_trades = []
    
    def hybrid_trade_loop(self):
        symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT"]
        trade_count = 0
        
        while self.running:
            try:
                for symbol in symbols:
                    if not self.running:
                        break
                    
                    # 📊 جلب بيانات حقيقية من Binance
                    df = self.get_realtime_data(symbol)
                    if df is None or len(df) < 50:
                        continue
                    
                    # 🧠 تحليل بالإشارات الحقيقية
                    signal = self.advanced_signal_analysis(df, symbol)
                    if signal and self.can_enter_trade():
                        trade = self.execute_hybrid_trade(symbol, signal)
                        if trade:
                            self.update_performance(trade)
                            self.adaptive_learning(trade)
                            self.update_intelligence_score()
                            trade_count += 1
                    
                    time.sleep(3)  # انتظار بين الرموز
                
                # 📈 تحديث التاريخ كل 5 صفقات
                if trade_count % 5 == 0:
                    self.update_balance_history()
                
                time.sleep(10)  # دورة كاملة
                
            except Exception as e:
                print(f"Error in trade loop: {e}")
                time.sleep(30)
    
    def update_balance_history(self):
        """تحديث تاريخ الرصيد للرسم البياني"""
        self.balance_history.append({
            "timestamp": datetime.now().isoformat(),
            "balance": round(self.balance, 2)
        })
        # الحفاظ على آخر 100 نقطة فقط
        if len(self.balance_history) > 100:
            self.balance_history.pop(0)
        self.save_state()
    
    def update_intelligence_score(self):
        """تحديث مؤشر الذكاء التكيفي"""
        recent_trades = self.memory[-30:] if len(self.memory) >= 30 else self.memory
        
        if not recent_trades:
            return
        
        # 1. معدل التعلم (سرعة تحسين الأداء)
        win_rate = sum(1 for t in recent_trades if t.get('profit', 0) > 0) / len(recent_trades)
        learning_rate = min(win_rate * 100, 100)
        
        # 2. التعرف على الأنماط (اتساق القرارات)
        pattern_score = self.calculate_pattern_recognition(recent_trades)
        
        # 3. تعديل المخاطر (كفاءة إدارة المخاطر)
        risk_score = self.calculate_risk_adjustment_score()
        
        # 4. التكيف مع السوق (مرونة الاستراتيجيات)
        market_score = self.calculate_market_adaptation()
        
        # 🧠 حساب النتيجة النهائية
        total_score = (
            learning_rate * 0.3 +
            pattern_score * 0.25 +
            risk_score * 0.25 +
            market_score * 0.2
        )
        
        self.adaptive_intelligence = {
            "score": round(total_score, 1),
            "learning_rate": round(learning_rate, 1),
            "pattern_recognition": round(pattern_score, 1),
            "risk_adjustment": round(risk_score, 1),
            "market_adaptation": round(market_score, 1)
        }
    
    def calculate_pattern_recognition(self, recent_trades):
        """حساب درجة التعرف على الأنماط"""
        if len(recent_trades) < 10:
            return 50
        
        # تحليل اتساق القرارات
        successful_patterns = 0
        total_patterns = 0
        
        for i in range(1, len(recent_trades)):
            current = recent_trades[i]
            previous = recent_trades[i-1]
            
            if (current.get('profit', 0) > 0 and 
                current.get('strategy') == previous.get('strategy') and
                previous.get('profit', 0) > 0):
                successful_patterns += 1
            total_patterns += 1
        
        return (successful_patterns / total_patterns * 100) if total_patterns > 0 else 50
    
    def calculate_risk_adjustment_score(self):
        """حساب درجة تعديل المخاطر"""
        # تحسين المخاطرة بناء على الأداء
        recent_profits = [t.get('profit', 0) for t in self.memory[-20:] if len(self.memory) >= 20]
        if not recent_profits:
            return 50
        
        avg_profit = np.mean(recent_profits)
        profit_std = np.std(recent_profits)
        
        if profit_std == 0:
            return 70
        
        # نسبة Sharpe مبسطة
        sharpe_ratio = avg_profit / profit_std if profit_std > 0 else 0
        risk_score = min(max(sharpe_ratio * 50 + 50, 0), 100)
        
        return risk_score
    
    def calculate_market_adaptation(self):
        """حساب درجة التكيف مع السوق"""
        # تحليل مرونة تغيير الاستراتيجيات
        strategy_changes = 0
        total_opportunities = 0
        
        for i in range(1, len(self.memory)):
            current_strategy = self.memory[i].get('strategy')
            previous_strategy = self.memory[i-1].get('strategy')
            
            if current_strategy != previous_strategy:
                strategy_changes += 1
                if self.memory[i].get('profit', 0) > self.memory[i-1].get('profit', 0):
                    strategy_changes += 1  # مكافأة التغيير الناجح
            
            total_opportunities += 1
        
        adaptation_score = (strategy_changes / total_opportunities * 100) if total_opportunities > 0 else 50
        return min(adaptation_score, 100)
    
    def get_realtime_data(self, symbol, interval='1m', limit=100):
        """جلب بيانات حقيقية من Binance"""
        try:
            if self.client:
                klines = self.client.get_klines(
                    symbol=symbol, 
                    interval=interval, 
                    limit=limit
                )
                df = pd.DataFrame(klines, columns=[
                    'open_time', 'open', 'high', 'low', 'close', 'volume',
                    'close_time', 'quote_asset_volume', 'number_of_trades',
                    'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
                ])
                df['close'] = df['close'].astype(float)
                return df
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
        return None
    
    def advanced_signal_analysis(self, df, symbol):
        """تحليل إشارات حقيقي باستخدام المؤشرات الفنية"""
        try:
            indicators = compute_indicators(df)
            if indicators is None:
                return None
            
            current_rsi = indicators['rsi'].iloc[-1] if 'rsi' in indicators else 50
            macd_diff = indicators['macd_diff'].iloc[-1] if 'macd_diff' in indicators else 0
            current_close = df['close'].iloc[-1]
            
            # 🎯 إشارات هجينة - الجمع بين القواعد
            signals = []
            
            # إشارة 1: RSI تشبع شراء/بيع
            if current_rsi < 30 and macd_diff > 0:
                signals.append({"type": "BUY", "strategy": "mean_reversion", "confidence": 0.85})
            elif current_rsi > 70 and macd_diff < 0:
                signals.append({"type": "SELL", "strategy": "mean_reversion", "confidence": 0.80})
            
            # إشارة 2: اتجاه MACD
            if macd_diff > 0 and current_rsi < 60:
                signals.append({"type": "BUY", "strategy": "momentum", "confidence": 0.75})
            elif macd_diff < 0 and current_rsi > 40:
                signals.append({"type": "SELL", "strategy": "momentum", "confidence": 0.70})
            
            # اختيار أفضل إشارة
            if signals:
                best_signal = max(signals, key=lambda x: x['confidence'])
                return best_signal
                
        except Exception as e:
            print(f"Signal analysis error for {symbol}: {e}")
        
        return None
    
    def execute_hybrid_trade(self, symbol, signal):
        """تنفيذ صفقة مهجنة ذكية"""
        try:
            # 📈 حساب حجم الصفقة مع التضاعف الذكي
            trade_amount = self.balance * self.risk_level
            trade_amount = max(trade_amount, 1.0)  # حد أدنى $1
            
            # 🧠 محاكاة ربح واقعي بناء على الإشارة
            base_profit = self.calculate_realistic_profit(signal)
            compounded_profit = base_profit * self.compounding_factor
            
            # 🛡️ تطبيق إدارة المخاطر
            max_loss = -trade_amount * 0.1  # خسارة محدودة 10%
            final_profit = max(compounded_profit, max_loss)
            
            trade = {
                "symbol": symbol,
                "type": signal["type"],
                "strategy": signal["strategy"],
                "amount": round(trade_amount, 2),
                "profit": round(final_profit, 2),
                "confidence": signal["confidence"],
                "timestamp": datetime.now().isoformat(),
                "status": "OPEN",
                "balance_before": round(self.balance, 2)
            }
            
            # 💰 تحديث الرصيد
            self.balance += final_profit
            trade["balance_after"] = round(self.balance, 2)
            
            # ➕ إضافة إلى الصفقات الحية
            self.live_trades.append(trade)
            self.trades.append(trade)
            
            return trade
            
        except Exception as e:
            print(f"Trade execution error: {e}")
            return None
    
    def calculate_realistic_profit(self, signal):
        """حساب ربح واقعي بناء على قوة الإشارة"""
        base_return = 0.02  # 2% عائد أساسي
        
        # تعديل حسب قوة الإشارة
        confidence_boost = (signal['confidence'] - 0.5) * 0.04  # ±2%
        strategy_boost = 0.01 if signal['strategy'] == 'mean_reversion' else 0.005
        
        total_return = base_return + confidence_boost + strategy_boost
        
        # تطبيق تقلبات واقعية
        volatility = np.random.normal(0, 0.015)  # تقلبات ±1.5%
        final_return = total_return + volatility
        
        # حساب الربح بالدولار
        trade_value = self.balance * self.risk_level
        profit = trade_value * final_return
        
        return profit
    
    def adaptive_learning(self, trade):
        """تعلم تكيفي من الصفقات"""
        self.memory.append(trade)
        if len(self.memory) > 200:
            self.memory.pop(0)
        
        # تحديث أوزان الاستراتيجيات
        if trade['profit'] > 0:
            self.strategy_weights[trade['strategy']] *= 1.01
        else:
            self.strategy_weights[trade['strategy']] *= 0.99
        
        # تطبيع الأوزان
        total = sum(self.strategy_weights.values())
        for strategy in self.strategy_weights:
            self.strategy_weights[strategy] /= total
        
        # تحديث عامل التضاعف
        self.update_compounding_factor()
        
        self.save_state()
    
    def update_compounding_factor(self):
        """تحديث عامل التضاعف بناء على الأداء"""
        recent_trades = self.memory[-30:] if len(self.memory) >= 30 else self.memory
        if recent_trades:
            win_rate = sum(1 for t in recent_trades if t['profit'] > 0) / len(recent_trades)
            
            if win_rate > 0.75:
                self.compounding_factor = 1.12
            elif win_rate > 0.65:
                self.compounding_factor = 1.09
            elif win_rate > 0.55:
                self.compounding_factor = 1.06
            else:
                self.compounding_factor = 1.03
    
    def update_performance(self, trade):
        """تحديث إحصائيات الأداء"""
        self.performance["total_trades"] += 1
        self.performance["total_profit"] += trade['profit']
        
        if trade['profit'] > 0:
            self.performance["successful_trades"] += 1
            self.performance["current_streak"] = max(0, self.performance["current_streak"]) + 1
        else:
            self.performance["current_streak"] = min(0, self.performance["current_streak"]) - 1
        
        self.performance["daily"] += trade['profit']
        self.performance["win_rate"] = (
            self.performance["successful_trades"] / 
            self.performance["total_trades"] * 100 
            if self.performance["total_trades"] > 0 else 0
        )
    
    def can_enter_trade(self):
        """التحقق من إمكانية الدخول في صفقة"""
        open_trades = sum(1 for t in self.live_trades if t.get('status') == 'OPEN')
        return open_trades < 3 and self.balance > 10
    
    def get_progress_data(self):
        """بيانات التقدم نحو الهدف"""
        progress = ((self.balance - self.initial_balance) / 
                   (self.target_balance - self.initial_balance)) * 100
        
        days_passed = (datetime.now() - self.start_date).days
        days_remaining = max(0, self.days_remaining - days_passed)
        
        required_daily = (
            (self.target_balance / self.balance) ** (1/days_remaining) - 1
        ) * 100 if days_remaining > 0 else 0
        
        return {
            "progress_percent": round(min(progress, 100), 2),
            "days_remaining": days_remaining,
            "required_daily": round(required_daily, 2),
            "current_balance": round(self.balance, 2),
            "target_balance": self.target_balance,
            "initial_balance": self.initial_balance
        }
    
    def get_performance_stats(self):
        """إحصائيات الأداء الشاملة"""
        progress = self.get_progress_data()
        
        return {
            **self.performance,
            **progress,
            "compounding_factor": round(self.compounding_factor, 3),
            "risk_level": f"{self.risk_level * 100}%",
            "strategy_weights": self.strategy_weights,
            "adaptive_intelligence": self.adaptive_intelligence,
            "live_trades_count": len([t for t in self.live_trades if t.get('status') == 'OPEN'])
        }
    
    def get_recent_trades(self, limit=15):
        """آخر الصفقات"""
        return self.trades[-limit:] if self.trades else []
    
    def get_live_trades(self):
        """الصفقات الحية"""
        return [t for t in self.live_trades if t.get('status') == 'OPEN']
    
    def get_balance_history(self):
        """تاريخ الرصيد للرسم البياني"""
        return self.balance_history
    
    def load_state(self):
        """تحميل الحالة المحفوظة"""
        try:
            if os.path.exists('hybrid_state.json'):
                with open('hybrid_state.json', 'r') as f:
                    data = json.load(f)
                    self.balance = data.get('balance', self.balance)
                    self.trades = data.get('trades', [])
                    self.memory = data.get('memory', [])
                    self.performance = data.get('performance', self.performance)
                    self.balance_history = data.get('balance_history', self.balance_history)
                    self.adaptive_intelligence = data.get('adaptive_intelligence', self.adaptive_intelligence)
        except Exception as e:
            print(f"Load state error: {e}")
    
    def save_state(self):
        """حفظ الحالة الحالية"""
        try:
            data = {
                'balance': self.balance,
                'trades': self.trades,
                'memory': self.memory,
                'performance': self.performance,
                'balance_history': self.balance_history,
                'adaptive_intelligence': self.adaptive_intelligence,
                'last_update': datetime.now().isoformat()
            }
            with open('hybrid_state.json', 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"Save state error: {e}")
