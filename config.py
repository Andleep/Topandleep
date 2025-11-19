import os
from binance.client import Client
import logging

class BinanceConfig:
    def __init__(self):
        self.api_key = os.getenv('BINANCE_API_KEY', '')
        self.api_secret = os.getenv('BINANCE_SECRET_KEY', '')
        self.testnet = os.getenv('TESTNET', 'true').lower() == 'true'
        self.trading_mode = os.getenv('TRADING_MODE', 'paper_trading')
        
        # إعدادات إضافية
        self.log_level = logging.INFO
        
    def get_client(self):
        """إنشاء عميل Binance"""
        try:
            if self.testnet:
                client = Client(
                    self.api_key, 
                    self.api_secret,
                    testnet=True
                )
                print("🔗 Connected to Binance Testnet")
            else:
                client = Client(self.api_key, self.api_secret)
                print("🔗 Connected to Binance Live")
            
            # اختبار الاتصال
            client.get_account()
            return client
            
        except Exception as e:
            print(f"❌ Binance connection failed: {e}")
            print("💡 Using simulation mode only")
            return None
    
    def validate_connection(self):
        """التحقق من صحة الاتصال"""
        try:
            client = self.get_client()
            if client:
                # جلب معلومات الحساب
                account_info = client.get_account()
                balances = account_info['balances']
                
                print("✅ Binance connection validated")
                print(f"📊 Account has {len(balances)} balances")
                return True
            return False
        except Exception as e:
            print(f"❌ Binance validation failed: {e}")
            return False

# إنشاء كائن الإعدادات العالمي
binance_config = BinanceConfig()
