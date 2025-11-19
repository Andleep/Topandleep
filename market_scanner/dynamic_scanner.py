import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class DynamicMarketScanner:
    def __init__(self):
        self.scan_history = []
        self.symbol_metrics = {}
    
    def comprehensive_scan(self, top_n=20):
        """مسح سوق شامل مع مقاييس متقدمة"""
        try:
            # في التطبيق الحقيقي، ستجلب البيانات من Binance
            # هنا نستخدم بيانات محاكاة
            symbols = self.get_top_symbols(top_n)
            market_analysis = {}
            
            for symbol in symbols:
                analysis = self.analyze_symbol(symbol)
                if analysis:
                    market_analysis[symbol] = analysis
            
            return market_analysis
            
        except Exception as e:
            print(f"❌ Market scan error: {e}")
            return self.get_fallback_symbols()
    
    def get_top_symbols(self, top_n=20):
        """الحصول على أفضل الرموز للتداول"""
        # رموز رئيسية في Binance
        major_symbols = [
            'BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'ADAUSDT',
            'XRPUSDT', 'DOTUSDT', 'DOGEUSDT', 'MATICUSDT', 'LTCUSDT',
            'AVAXUSDT', 'LINKUSDT', 'ATOMUSDT', 'UNIUSDT', 'XLMUSDT'
        ]
        
        return major_symbols[:top_n]
    
    def analyze_symbol(self, symbol):
        """تحليل رمز مفصل"""
        try:
            # محاكاة بيانات السوق
            current_price = np.random.uniform(10, 50000)
            volume_24h = np.random.uniform(1000000, 50000000)
            price_change_24h = np.random.uniform(-0.1, 0.1)
            
            # حساب المؤشرات الفنية
            indicators = self.calculate_technical_indicators(symbol)
            
            analysis = {
                'symbol': symbol,
                'current_price': current_price,
                'volume_24h': volume_24h,
                'price_change_24h': price_change_24h,
                'liquidity_score': min(volume_24h / 1000000, 1.0),
                'volatility_score': np.random.uniform(0.1, 0.3),
                'trend_strength': np.random.uniform(0, 1),
                'momentum_score': np.random.uniform(0, 1),
                'support_resistance_score': np.random.uniform(0, 1),
                'overall_score': np.random.uniform(0.5, 0.9),
                'indicators': indicators
            }
            
            return analysis
            
        except Exception as e:
            print(f"❌ Symbol analysis error for {symbol}: {e}")
            return None
    
    def calculate_technical_indicators(self, symbol):
        """حساب المؤشرات الفنية"""
        return {
            'rsi': np.random.uniform(30, 70),
            'macd': np.random.uniform(-0.1, 0.1),
            'bollinger_position': np.random.uniform(0.2, 0.8),
            'stochastic': np.random.uniform(20, 80),
            'atr': np.random.uniform(0.5, 5.0)
        }
    
    def select_top_symbols(self, market_analysis, top_n=8, min_volume=1000000, max_volatility=0.15):
        """اختيار أفضل الرموز بناءً على معايير متعددة"""
        if not market_analysis:
            return self.get_fallback_symbols()[:top_n]
        
        scored_symbols = []
        
        for symbol, analysis in market_analysis.items():
            if analysis['volume_24h'] < min_volume:
                continue
            
            if analysis['volatility_score'] > max_volatility:
                continue
            
            # حساب النقاط
            volume_score = min(analysis['volume_24h'] / 5000000, 1.0)
            volatility_score = 1 - (analysis['volatility_score'] / max_volatility)
            trend_score = analysis['trend_strength']
            momentum_score = analysis['momentum_score']
            
            total_score = (
                volume_score * 0.25 +
                volatility_score * 0.20 + 
                trend_score * 0.25 +
                momentum_score * 0.30
            )
            
            scored_symbols.append((symbol, total_score, analysis))
        
        # ترتيب حسب النقاط
        scored_symbols.sort(key=lambda x: x[1], reverse=True)
        
        return [symbol for symbol, score, analysis in scored_symbols[:top_n]]
    
    def get_fallback_symbols(self):
        """رموز احتياطية في حالة فشل المسح"""
        return ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'ADAUSDT', 'DOTUSDT', 'LINKUSDT', 'MATICUSDT']
