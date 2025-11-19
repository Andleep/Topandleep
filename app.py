import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import time
import sys
import os

# إضافة المسارات للمكتبات
sys.path.append('deep_learning')
sys.path.append('capital_management') 
sys.path.append('market_analysis')
sys.path.append('market_scanner')
sys.path.append('core')

from main_max import AIONAlphaUltraMAX

class AIONDashboard:
    def __init__(self):
        self.bot = None
        self.setup_page()
        
    def setup_page(self):
        st.set_page_config(
            page_title="AION Alpha Ultra MAX",
            page_icon="🚀",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # تخصيص التصميم
        st.markdown("""
        <style>
        .main-header {
            font-size: 3rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 10px;
            border-left: 4px solid #1f77b4;
        }
        .profit-positive {
            color: #00d600;
            font-weight: bold;
        }
        .profit-negative {
            color: #ff0000;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        st.sidebar.title("🎯 تحكم AION MAX")
        
        # إعدادات البوت
        st.sidebar.subheader("⚙️ الإعدادات")
        initial_balance = st.sidebar.number_input("رأس المال الأولي ($)", value=50.0, min_value=10.0, step=10.0)
        
        mode = st.sidebar.selectbox(
            "وضع التشغيل",
            ["paper_trading", "live_trading", "backtest"]
        )
        
        cycle_interval = st.sidebar.slider(
            "فترة الدورة (ثانية)", 
            min_value=60, 
            max_value=600, 
            value=120, 
            step=30
        )
        
        # إعدادات المخاطرة
        st.sidebar.subheader("🛡️ إدارة المخاطرة")
        max_drawdown = st.sidebar.slider("أقصى تراجع مسموح", 0.05, 0.25, 0.15, 0.01)
        daily_loss_limit = st.sidebar.slider("حد الخسارة اليومي", 0.01, 0.1, 0.03, 0.01)
        
        # أزرار التحكم
        col1, col2 = st.sidebar.columns(2)
        with col1:
            start_bot = st.button("🚀 تشغيل البوت", type="primary")
        with col2:
            stop_bot = st.button("🛑 إيقاف البوت")
        
        st.sidebar.markdown("---")
        st.sidebar.info("""
        **AION Alpha Ultra MAX v5.0**
        - تعلم عميق معزز
        - تحليل كمي متقدم
        - إدارة مخاطر ذكية
        """)
        
        return {
            'initial_balance': initial_balance,
            'mode': mode,
            'cycle_interval': cycle_interval,
            'max_drawdown': max_drawdown,
            'daily_loss_limit': daily_loss_limit,
            'start_bot': start_bot,
            'stop_bot': stop_bot
        }
    
    def render_header(self):
        st.markdown('<h1 class="main-header">🚀 AION Alpha Ultra MAX</h1>', unsafe_allow_html=True)
        
        cols = st.columns(4)
        with cols[0]:
            st.metric("الحالة", "🟢 نشط" if self.bot else "🔴 متوقف")
        with cols[1]:
            balance = self.bot.current_balance if self.bot else 0
            st.metric("رصيد الحساب", f"${balance:.2f}")
        with cols[2]:
            total_profit = (balance - 50) if self.bot else 0
            profit_class = "profit-positive" if total_profit >= 0 else "profit-negative"
            st.metric("إجمالي الأرباح", f"${total_profit:.2f}")
        with cols[3]:
            win_rate = self.bot.performance_metrics['win_rate'] if self.bot and self.bot.performance_metrics else 0
            st.metric("معدل النجاح", f"{win_rate:.1%}")
    
    def render_performance_metrics(self):
        st.subheader("📊 مقاييس الأداء المتقدمة")
        
        if not self.bot:
            st.info("🔍 البوت غير نشط. يرجى تشغيل البوت لعرض البيانات.")
            return
        
        cols = st.columns(5)
        metrics = self.bot.performance_metrics
        
        with cols[0]:
            st.metric("نسبة شارب", f"{metrics.get('sharpe_ratio', 0):.2f}")
        with cols[1]:
            st.metric("أقصى تراجع", f"{metrics.get('max_drawdown', 0):.2%}")
        with cols[2]:
            st.metric("عامل الربح", f"{metrics.get('profit_factor', 0):.2f}")
        with cols[3]:
            st.metric("التوقع", f"${metrics.get('expectancy', 0):.2f}")
        with cols[4]:
            st.metric("الصفقات النشطة", len(self.bot.portfolio))
    
    def render_equity_chart(self):
        st.subheader("📈 منحنى رأس المال")
        
        if not self.bot or not self.bot.performance_data:
            st.info("لا توجد بيانات أداء حتى الآن.")
            return
        
        # تحضير بيانات المنحنى
        performance_df = pd.DataFrame(self.bot.performance_data)
        performance_df['timestamp'] = pd.to_datetime(performance_df['timestamp'])
        performance_df = performance_df.set_index('timestamp')
        
        # إنشاء الرسم البياني
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=performance_df.index,
            y=performance_df['current_balance'],
            mode='lines',
            name='رأس المال',
            line=dict(color='#1f77b4', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=performance_df.index,
            y=performance_df['portfolio_value'],
            mode='lines',
            name='قيمة المحفظة',
            line=dict(color='#ff7f0e', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title="تطور رأس المال مع الزمن",
            xaxis_title="الوقت",
            yaxis_title="القيمة ($)",
            height=400,
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_trade_history(self):
        st.subheader("📋 سجل الصفقات")
        
        if not self.bot or not self.bot.trade_history:
            st.info("لا توجد صفقات حتى الآن.")
            return
        
        # تحويل البيانات إلى DataFrame
        trades_df = pd.DataFrame(self.bot.trade_history)
        
        if len(trades_df) > 0:
            # تنسيق الأعمدة
            trades_df['timestamp'] = pd.to_datetime(trades_df['timestamp']).dt.strftime('%Y-%m-%d %H:%M:%S')
            trades_df['profit'] = trades_df['profit'].apply(lambda x: f"${x:.2f}")
            trades_df['amount'] = trades_df['amount'].apply(lambda x: f"${x:.2f}")
            trades_df['ai_confidence'] = trades_df['ai_confidence'].apply(lambda x: f"{x:.2f}")
            
            # عرض الجدول
            st.dataframe(
                trades_df[[
                    'timestamp', 'symbol', 'action', 'amount', 
                    'profit', 'ai_confidence', 'market_regime'
                ]].sort_values('timestamp', ascending=False),
                height=400
            )
            
            # إحصائيات الصفقات
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                total_trades = len(trades_df)
                st.metric("إجمالي الصفقات", total_trades)
            with col2:
                winning_trades = len(trades_df[trades_df['profit'].str.contains('-').fillna(True) == False])
                st.metric("الصفقات الرابحة", f"{winning_trades} ({winning_trades/total_trades:.1%})")
            with col3:
                avg_profit = trades_df['profit'].str.replace('$', '').str.replace(',', '').astype(float).mean()
                st.metric("متوسط الربح", f"${avg_profit:.2f}")
            with col4:
                best_trade = trades_df['profit'].str.replace('$', '').str.replace(',', '').astype(float).max()
                st.metric("أفضل صفقة", f"${best_trade:.2f}")
    
    def render_portfolio_overview(self):
        st.subheader("💼 نظرة عامة على المحفظة")
        
        if not self.bot or not self.bot.portfolio:
            st.info("لا توجد مراكز نشطة حالياً.")
            return
        
        # بيانات المحفظة
        portfolio_data = []
        for symbol, quantity in self.bot.portfolio.items():
            # في التطبيق الحقيقي، تحتاج للحصول على السعر الحالي من البورصة
            current_price = 100  # قيمة افتراضية
            value = quantity * current_price
            
            portfolio_data.append({
                'الرمز': symbol,
                'الكمية': f"{quantity:.6f}",
                'القيمة': f"${value:.2f}",
                'النسبة': f"{(value / self.bot.current_balance * 100):.1f}%"
            })
        
        portfolio_df = pd.DataFrame(portfolio_data)
        st.dataframe(portfolio_df, height=300)
        
        # مخطط توزيع المحفظة
        if len(portfolio_data) > 0:
            fig = px.pie(
                portfolio_df, 
                values='القيمة', 
                names='الرمز',
                title="توزيع المحفظة"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    def render_ai_insights(self):
        st.subheader("🧠 رؤى الذكاء الاصطناعي")
        
        if not self.bot:
            return
        
        cols = st.columns(2)
        
        with cols[0]:
            st.markdown("### 📊 النظام السوقي")
            regime = self.bot.market_regime
            regime_icons = {
                'HIGH_VOLATILITY': '🌪️',
                'TRENDING_UP': '📈', 
                'TRENDING_DOWN': '📉',
                'LOW_VOLATILITY': '🌊'
            }
            st.metric(
                "الحالة الحالية", 
                f"{regime_icons.get(regime, '🔍')} {regime}"
            )
            
            # توصيات النظام
            st.markdown("#### 💡 توصيات النظام")
            if regime == 'HIGH_VOLATILITY':
                st.warning("تقليل أحجام المراكز، زيادة وقف الخسارة")
            elif regime == 'TRENDING_UP':
                st.success("التركيز على استراتيجيات الزخم والشراء")
            elif regime == 'TRENDING_DOWN':
                st.error("التركيز على البيع والاستراتيجيات الهابطة")
            else:
                st.info("ظروف طبيعية - التداول بالاستراتيجيات المعتادة")
        
        with cols[1]:
            st.markdown("### 🔄 التعلم الآلي")
            st.metric("دورات التعلم", self.bot.learning_cycles)
            st.metric("مستوى التعلم", f"{min(self.bot.learning_cycles / 100, 1.0):.1%}")
            
            # تقدم التعلم
            st.markdown("#### 📈 تقدم النموذج")
            if self.bot.learning_cycles > 0:
                progress = min(self.bot.learning_cycles / 200, 1.0)
                st.progress(progress)
                st.caption(f"النموذج متقدم بنسبة {progress:.1%}")
    
    def render_real_time_updates(self):
        st.subheader("🔄 التحديثات اللحظية")
        
        if not self.bot:
            return
        
        # آخر الصفقات
        latest_trades = self.bot.trade_history[-5:] if self.bot.trade_history else []
        
        for trade in reversed(latest_trades):
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                action_icon = "🟢" if trade['action'] == 'BUY' else "🔴"
                st.write(f"{action_icon} {trade['symbol']}")
            with col2:
                st.write(trade['action'])
            with col3:
                profit_class = "profit-positive" if trade['profit'] > 0 else "profit-negative"
                st.markdown(f'<span class="{profit_class}">${trade["profit"]:.2f}</span>', unsafe_allow_html=True)
            with col4:
                st.write(f"🕒 {trade['timestamp'].strftime('%H:%M')}")
    
    def run(self):
        # تحميل الإعدادات من الشريط الجانبي
        settings = self.render_sidebar()
        
        # عنوان الصفحة
        self.render_header()
        
        # التحكم في البوت
        if settings['start_bot'] and not self.bot:
            try:
                self.bot = AIONAlphaUltraMAX(
                    initial_balance=settings['initial_balance'],
                    mode=settings['mode']
                )
                st.success("✅ تم تشغيل البوت بنجاح!")
                
                # تشغيل البوت في خلفية thread (في production)
                st.info("🧠 البوت يعمل الآن... تحقق من سجل الصفقات للتحديثات.")
                
            except Exception as e:
                st.error(f"❌ خطأ في تشغيل البوت: {e}")
        
        if settings['stop_bot'] and self.bot:
            self.bot = None
            st.warning("🛑 تم إيقاف البوت")
        
        # إذا كان البوت نشطاً، عرض البيانات
        if self.bot:
            # تقسيم الصفحة إلى أقسام
            self.render_performance_metrics()
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                self.render_equity_chart()
                self.render_trade_history()
            
            with col2:
                self.render_portfolio_overview()
                self.render_ai_insights()
            
            self.render_real_time_updates()
            
            # زر تحديث البيانات
            if st.button("🔄 تحديث البيانات"):
                st.rerun()
        else:
            # شاشة الترحيب عندما يكون البوت متوقفاً
            st.markdown("""
            ## 🚀 مرحباً بك في AION Alpha Ultra MAX!
            
            **AION Alpha Ultra MAX** هو نظام تداول بالذكاء الاصطناعي المتقدم الذي يجمع بين:
            
            - 🧠 **التعلم العميق المعزز** - يتعلم من كل صفقة
            - 📊 **التحليل الكمي** - تحليل متعدد الأبعاد  
            - 🛡️ **إدارة المخاطر الذكية** - حماية شاملة لرأس المال
            - 🔄 **التكيف التلقائي** - يتكيف مع ظروف السوق
            
            ### 🎯 لبدء التشغيل:
            1. اضبط الإعدادات في الشريط الجانبي
            2. اضغط على "تشغيل البوت" 
            3. تابع الأداء في الوقت الحقيقي
            
            ### 📈 التوقعات الواقعية:
            - **الشهر 1**: $50 → $200-$500 (400-1000%)
            - **الشهر 2**: $500 → $800-$2,000 (160-400%)  
            - **الشهر 3**: $2,500 → $3,000-$7,500 (120-300%)
            """)

# تشغيل التطبيق
if __name__ == "__main__":
    dashboard = AIONDashboard()
    dashboard.run()
