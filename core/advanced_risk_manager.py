import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class AdvancedRiskManager:
    def __init__(self, initial_balance):
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.daily_trades = {}
        self.risk_metrics = {
            'max_daily_loss': 0.03,  # 3%
            'max_position_size': 0.15,  # 15%
            'max_portfolio_risk': 0.25,  # 25%
            'max_consecutive_losses': 3
        }
        self.trade_history = []
    
    def approve_trade(self, symbol, action, market_data, current_balance, portfolio):
        """الموافقة على الصفقة بعد فحص المخاطر"""
        risk_check = {
            'approved': True,
            'risk_score': 0.0,
            'warnings': [],
            'adjustments': {}
        }
        
        # 1. فحص التوازن
        if current_balance < 10:
            risk_check['approved'] = False
            risk_check['warnings'].append("رصيد غير كافي")
            return risk_check
        
        # 2. فحص اليومي
        daily_check = self.check_daily_limits(symbol, action)
        if not daily_check['approved']:
            risk_check['approved'] = False
            risk_check['warnings'].extend(daily_check['warnings'])
        
        # 3. فحص التركيز
        concentration_check = self.check_portfolio_concentration(symbol, portfolio, current_balance)
        if not concentration_check['approved']:
            risk_check['approved'] = False
            risk_check['warnings'].extend(concentration_check['warnings'])
        
        # 4. فحص السوق
        market_check = self.check_market_conditions(symbol, market_data)
        risk_check['warnings'].extend(market_check['warnings'])
        risk_check['risk_score'] += market_check['risk_score']
        
        # 5. حساب درجة المخاطرة النهائية
        risk_check['risk_score'] = self.calculate_overall_risk_score(
            risk_check, daily_check, concentration_check, market_check
        )
        
        # إذا كانت درجة المخاطرة عالية جداً، رفض الصفقة
        if risk_check['risk_score'] > 0.8:
            risk_check['approved'] = False
            risk_check['warnings'].append("درجة المخاطرة عالية جداً")
        
        return risk_check
    
    def check_daily_limits(self, symbol, action):
        """فحص الحدود اليومية"""
        today = datetime.now().date()
        today_str = today.isoformat()
        
        if today_str not in self.daily_trades:
            self.daily_trades[today_str] = {
                'trades_count': 0,
                'total_volume': 0,
                'net_profit': 0
            }
        
        daily_data = self.daily_trades[today_str]
        check = {'approved': True, 'warnings': []}
        
        # فحص عدد الصفقات
        if daily_data['trades_count'] >= 50:
            check['approved'] = False
            check['warnings'].append("تم الوصول للحد اليومي للصفقات")
        
        # فحص الخسارة اليومية
        if daily_data['net_profit'] < -self.initial_balance * self.risk_metrics['max_daily_loss']:
            check['approved'] = False
            check['warnings'].append("تم الوصول للحد الأقصى للخسارة اليومية")
        
        return check
    
    def check_portfolio_concentration(self, symbol, portfolio, current_balance):
        """فحص تركيز المحفظة"""
        check = {'approved': True, 'warnings': []}
        
        # حساب قيمة المحفظة الإجمالية
        portfolio_value = current_balance  # + قيمة المراكز (مبسطة)
        
        # فحص التركيز على رمز واحد
        if symbol in portfolio:
            position_size = portfolio[symbol] * 100  # قيمة افتراضية
            concentration = position_size / portfolio_value
            
            if concentration > self.risk_metrics['max_position_size']:
                check['approved'] = False
                check['warnings'].append(f"التركيز على {symbol} превысил الحد المسموح")
        
        # فحص تنويع المحفظة
        if len(portfolio) > 10:
            check['warnings'].append("المحفظة متنوعة بشكل كبير")
        
        return check
    
    def check_market_conditions(self, symbol, market_data):
        """فحص ظروف السوق"""
        check = {'risk_score': 0.0, 'warnings': []}
        
        if symbol not in market_data:
            check['risk_score'] += 0.3
            check['warnings'].append("بيانات سوق غير كافية")
            return check
        
        data = market_data[symbol]
        
        # فحص التقلب
        if 'volatility_score' in data and data['volatility_score'] > 0.2:
            check['risk_score'] += 0.2
            check['warnings'].append("تقلب السوق مرتفع")
        
        # فحص السيولة
        if 'liquidity_score' in data and data['liquidity_score'] < 0.3:
            check['risk_score'] += 0.3
            check['warnings'].append("سيولة منخفضة")
        
        return check
    
    def calculate_overall_risk_score(self, risk_check, daily_check, concentration_check, market_check):
        """حساب درجة المخاطرة الإجمالية"""
        base_score = market_check['risk_score']
        
        # إضافة نقاط للتحذيرات
        warning_penalty = len(risk_check['warnings']) * 0.1
        total_score = base_score + warning_penalty
        
        return min(total_score, 1.0)
    
    def update_after_trade(self, symbol, action, amount, profit):
        """تحديث البيانات بعد الصفقة"""
        today = datetime.now().date()
        today_str = today.isoformat()
        
        if today_str not in self.daily_trades:
            self.daily_trades[today_str] = {
                'trades_count': 0,
                'total_volume': 0,
                'net_profit': 0
            }
        
        daily_data = self.daily_trades[today_str]
        daily_data['trades_count'] += 1
        daily_data['total_volume'] += amount
        daily_data['net_profit'] += profit
        
        # تسجيل الصفقة
        trade_record = {
            'timestamp': datetime.now(),
            'symbol': symbol,
            'action': action,
            'amount': amount,
            'profit': profit
        }
        self.trade_history.append(trade_record)
