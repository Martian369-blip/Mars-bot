import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import engine as eng  # 🛰️ Link directly into your custom computation file module

# 🏛️ 1. CYBERPUNK TERMINAL SKINNING ENGINE
st.set_page_config(page_title="MARS_BOT V11.6", page_icon="👽", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    h1, h2, h3, h4, h5, h6 { color: #00FF00 !important; font-family: 'Courier New', monospace; }
    div[data-testid="stContainer"] { border: 1px solid #00FF00 !important; background-color: #050505 !important; border-radius: 4px; padding: 15px; margin-bottom: 15px; }
    .stButton>button { background-color: #000000 !important; color: #00FF00 !important; border: 1px solid #00FF00 !important; font-family: 'Courier New', monospace; width: 100%; height: 45px; font-weight: bold; }
    .stButton>button:hover { background-color: #00FF00 !important; color: #000000 !important; }
    .stTextInput>div>div>input { background-color: #050505 !important; color: #00FF00 !important; border: 1px solid #00FF00 !important; font-family: 'Courier New', monospace; text-align: center; font-size: 18px; }
    .stSelectbox>div>div>div { background-color: #050505 !important; color: #00FF00 !important; border: 1px solid #00FF00 !important; }
    .stNumberInput>div>div>input { background-color: #050505 !important; color: #00FF00 !important; border: 1px solid #00FF00 !important; }
    section[data-testid="stSidebar"] { background-color: #000000 !important; border-right: 1px solid #00FF00 !important; }
    section[data-testid="stSidebar"] .stRadio>div { color: #00FF00 !important; font-family: 'Courier New', monospace; }
</style>
""", unsafe_allow_html=True)

# Initialize Session State tracking database layers for the ledger book system
if "journal_db" not in st.session_state:
    st.session_state.journal_db = pd.DataFrame(columns=["Asset", "Action", "Size", "Entry Price", "Profit/Loss (ZAR)", "Status"])
if "live_balance" not in st.session_state:
    st.session_state.live_balance = 500.0

# ==================================================================================
# 🕹️ PERSISTENT TOP-CENTERED SEARCH HUB (RUNS GLOBAL ON ALL PAGES)
# ==================================================================================
st.markdown("<h1 style='text-align: center;'>🛸 MARS_BOT V11.6</h1>", unsafe_allow_html=True)

col_search, col_trigger = st.columns()
with col_search:
    target_asset = st.text_input("🔍 SEARCH ASSET SYMBOL:", value="GBPUSD=X", label_visibility="collapsed").strip().upper()
with col_trigger:
    search_activated = st.button("🛰️ SCAN")

# LEFT-SIDE THREE-BAR HAMBURGER MENU NAVIGATION DRAWER
st.sidebar.markdown("### ☰ CORE CONSOLE")
page_select = st.sidebar.radio(
    "NAVIGATION PANEL:",
    ["📊 EXECUTIVE SIGNALS", "📡 SPECIALIZED NEWS", "🕹️ WORKSPACE JOURNAL"]
)
st.sidebar.divider()
st.sidebar.caption("👽 Active Core Framework. Click top-left arrow on mobile layout to open/close menu.")

# 🏛️ GLOBAL VARIABLE INITIALIZATION
price, daily_rsi, hourly_rsi, hourly_atr, direction, color, stop_loss, take_profit = 0.0, 50.0, 50.0, 0.001, "HOLD", "#FFFF00", 0.0, 0.0
asset_name = target_asset
daily_df = pd.DataFrame()
hourly_df = pd.DataFrame()

try:
    ticker_feed = yf.Ticker(target_asset)
    daily_df = ticker_feed.history(period="3mo", interval="1d")
    hourly_df = ticker_feed.history(period="1mo", interval="1h")
    asset_name = ticker_feed.info.get('shortName', target_asset)
    
    if hourly_df.empty and not daily_df.empty:
        hourly_df = daily_df.copy()
    
    if not daily_df.empty and not hourly_df.empty:
        daily_df['RSI'] = eng.calculate_rsi(daily_df)
        hourly_df['RSI'] = eng.calculate_rsi(hourly_df)
        
        price = daily_df['Close'].iloc[-1]
        daily_rsi = daily_df['RSI'].iloc[-1]
        hourly_rsi = hourly_df['RSI'].iloc[-1]
        hourly_atr = eng.extract_hourly_atr(hourly_df)
        
        recent_low = hourly_df['Low'].tail(24).min()
        recent_high = hourly_df['High'].tail(24).max()
        
        if hourly_rsi < 35 or (price <= (recent_low * 1.005)):
            direction, color = "🚀 BUY / LONG", "#00FF00"
            stop_loss = price - (hourly_atr * 1.5)
            take_profit = price + ((price - stop_loss) * 2.5)
        elif hourly_rsi > 65 or (price >= (recent_high * 0.995)):
            direction, color = "💥 SELL / SHORT", "#FF0000"
            stop_loss = price + (hourly_atr * 1.5)
            take_profit = price - ((stop_loss - price) * 2.5)
        else:
            direction, color = "⏳ HOLD / PRESERVE CASH", "#FFFF00"
            stop_loss, take_profit = price, price
except Exception as e:
    st.sidebar.error(f"Telemetry Core Sync Warning: {str(e)}")

# ==================================================================================
# 📊 NAVIGATION ROW 1: EXECUTIVE SIGNALS Panel View
# ==================================================================================
if page_select == "📊 EXECUTIVE SIGNALS":
    st.markdown(f"### 🎯 Live Sovereign Matrix Sheet: {target_asset}")
    
    if daily_df.empty or hourly_df.empty:
        st.error(f"❌ Empty market node feedback. Verify symbol format: '{target_asset}'")
    else:
        c_sym = "R" if ("ZAR" in target_asset or ".JO" in target_asset) else "$"
        formatted_price = f"{price:.4f}" if "ZAR" in target_asset else (f"{price:.5f}" if "=" in target_asset else f"{price:.2f}")
        
        with st.container():
            st.markdown(f"<h3 style='text-align: center; margin: 0px;'>📦 {asset_name}</h3>", unsafe_allow_html=True)
            st.divider()
            
            col_a, col_b, col_c = st.columns(3)
            with col_a: st.markdown(f"**Spot Rate:**\n### {c_sym}{formatted_price}")
            with col_b: st.markdown(f"**Live Signal:**\n<h3 style='color:{color}; margin-top:5px;'>{direction}</h3>", unsafe_allow_html=True)
            with col_c: st.markdown(f"**Hourly RSI:**\n### `{hourly_rsi:.1f}`")
            
            if direction != "⏳ HOLD / PRESERVE CASH":
                st.divider()
                mult = 10000 if ("=" in target_asset and "ZAR" not in target_asset) else 1
                pts_sl = np.abs(price - stop_loss) * mult
                pts_tp = np.abs(take_profit - price) * mult
                if "ZAR" in target_asset: pts_sl, pts_tp = 800.0, 2000.0
                
                st.markdown("### 📲 NATIVE IG TICKET CODES (ENTRY PROTECTIONS):")
                col_sl, col_tp = st.columns(2)
                with col_sl:
                    st.markdown(f"<div style='border:1px solid #FF0000; padding:10px; border-radius:4px; text-align:center;'><span style='color:#FF0000; font-weight:bold;'>🛑 STOP-LOSS:</span><br><code>{pts_sl:.1f} pts</code></div>", unsafe_allow_html=True)
                with col_tp:
                    st.markdown(f"<div style='border:1px solid #00FF00; padding:10px; border-radius:4px; text-align:center;'><span style='color:#00FF00; font-weight:bold;'>🎯 TAKE-PROFIT:</span><br><code>{pts_tp:.1f} pts</code></div>", unsafe_allow_html=True)
            
            st.divider()
            st.markdown("#### 🕯️ Real-Time Intraday Candlestick Trend")
            fig_sig = go.Figure()
            fig_sig.add_trace(go.Candlestick(
                x=hourly_df.tail(48).index, open=hourly_df.tail(48)['Open'], high=hourly_df.tail(48)['High'],
                low=hourly_df.tail(48)['Low'], close=hourly_df.tail(48)['Close'], name="Market"
            ))
            fig_sig.update_layout(template="plotly_dark", paper_bgcolor='#000000', plot_bgcolor='#050505', xaxis_rangeslider_visible=False, height=350, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig_sig, use_container_width=True)

# ==================================================================================
# 📡 NAVIGATION ROW 2: LIVE SPECIALIZED WIRE STREAM NEWS DESK
# ==================================================================================
elif page_select == "📡 SPECIALIZED NEWS":
    st.markdown(f"### 📰 Mars_bot Custom Research Desk: {target_asset}")
    st.divider()
    
    live_news = eng.fetch_specialized_news(target_asset)
    if not live_news:
        st.warning("📡 Sweeping global networks... Displaying baseline sovereign intelligence feeds:")
        st.markdown("##### 🦅 Federal Reserve Enforces Measured Approach Over Late-Autumn Sessions")
        st.write("Institutional dollar desks verify that robust labor metrics give central bankers massive scope to hold baseline borrowing yields steady.")
    else:
        for article in live_news:
            with st.container():
                st.markdown(f"##### 🛰️ {article['title']}")
                st.caption(f"Published Line: {article['pubDate']} | Type: Dynamic Intelligence Node")
                st.markdown(f"[Launch Source Feed Link]({article['link']})")

# ==================================================================================
# 🕹️ NAVIGATION ROW 3: WORKSPACE JOURNAL (ICHIMOKU CURVES & CASHFLOW LEDGER BOOK)
# ==================================================================================
elif page_select == "🕹️ WORKSPACE JOURNAL":
    st.markdown("### 🕹️ Quantitative Analytics & Ledger Command")
    st.divider()
    
    st.markdown(f"#### 🇯🇵 Live Ichimoku Technical Analysis Matrix: {target_asset}")
    if hourly_df.empty:
        st.error("❌ Node memory link un-established. Scan a valid symbol to display charts.")
    else:
        chart_df = eng.compute_ichimoku(hourly_df.tail(60))
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=chart_df.index, open=chart_df['Open'], high=chart_df['High'],
            low=chart_df['Low'], close=chart_df['Close'], name="Candles"
        ))
        fig.add_trace(go.Scatter(x=chart_df.index, y=chart_df['tenkan_sen'], line=dict(color='#00FFFF', width=1), name="Tenkan-sen"))
