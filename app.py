  import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 🏛️ 1. CYBERPUNK TERMINAL SKINNING ENGINE
st.set_page_config(page_title="MARS_BOT V11.0", page_icon="👽", layout="centered", initial_sidebar_state="collapsed")

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

# Core Mathematical Indicators Engine
def calculate_rsi(df, window=14):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50.0)

def extract_hourly_atr(df_hourly, window=14):
    high_low = df_hourly['High'] - df_hourly['Low']
    high_close = np.abs(df_hourly['High'] - df_hourly['Close'].shift())
    low_close = np.abs(df_hourly['Low'] - df_hourly['Close'].shift())
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = true_range.rolling(window).mean().iloc[-1]
    return atr if not pd.isna(atr) else df_hourly['Close'].iloc[-1] * 0.002

def compute_ichimoku(df):
    # Conversion Line (Tenkan-sen): (9-period high + 9-period low)/2
    high_9 = df['High'].rolling(window=9).max()
    low_9 = df['Low'].rolling(window=9).min()
    df['tenkan_sen'] = (high_9 + low_9) / 2
    
    # Base Line (Kijun-sen): (26-period high + 26-period low)/2
    high_26 = df['High'].rolling(window=26).max()
    low_26 = df['Low'].rolling(window=26).min()
    df['kijun_sen'] = (high_26 + low_26) / 2
    
    # Leading Span A (Senkou Span A): (Conversion Line + Base Line)/2 shifted 26 periods forward
    df['senkou_span_a'] = ((df['tenkan_sen'] + df['kijun_sen']) / 2).shift(26)
    
    # Leading Span B (Senkou Span B): (52-period high + 52-period low)/2 shifted 26 periods forward
    high_52 = df['High'].rolling(window=52).max()
    low_52 = df['Low'].rolling(window=52).min()
    df['senkou_span_b'] = ((high_52 + low_52) / 2).shift(26)
    
    return df

# ==================================================================================
# 🕹️ PERSISTENT TOP-CENTERED SEARCH CONFIGURATION MODULE (RUNS GLOBAL)
# ==================================================================================
st.markdown("<h1 style='text-align: center;'>🛸 MARS_BOT V11.0</h1>", unsafe_allow_html=True)

# Unified Global Entry Tracker Layout with an explicit execution button next to it
col_search, col_trigger = st.columns([4, 1])
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

# Fetch asset market data safely at top-level loop to synchronize pages
try:
    ticker_feed = yf.Ticker(target_asset)
    daily_df = ticker_feed.history(period="3mo", interval="1d")
    hourly_df = ticker_feed.history(period="1wk", interval="1h")
    asset_name = ticker_feed.info.get('shortName', target_asset)
except Exception:
    daily_df, hourly_df, asset_name = pd.DataFrame(), pd.DataFrame(), target_asset

# ==================================================================================
# 📊 NAVIGATION ROW 1: EXECUTIVE SIGNALS (STOP/LIMIT PLACED BEFORE THE CHART)
# ==================================================================================
if page_select == "📊 EXECUTIVE SIGNALS":
    st.markdown(f"### 🎯 Live Sovereign Matrix Sheet: {target_asset}")
    
    if daily_df.empty or hourly_df.empty:
        st.error(f"❌ Empty market node feedback. Verify format on database rules: '{target_asset}'")
    else:
        daily_df['RSI'] = calculate_rsi(daily_df)
        hourly_df['RSI'] = calculate_rsi(hourly_df)
        
        price = daily_df['Close'].iloc[-1]
        daily_rsi = daily_df['RSI'].iloc[-1]
        hourly_rsi = hourly_df['RSI'].iloc[-1]
        hourly_atr = extract_hourly_atr(hourly_df)
        
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
            
        c_sym = "R" if ("ZAR" in target_asset or ".JO" in target_asset) else "$"
        formatted_price = f"{price:.4f}" if "ZAR" in target_asset else (f"{price:.5f}" if "=" in target_asset else f"{price:.2f}")
        
        with st.container():
            st.markdown(f"<h3 style='text-align: center; margin: 0px;'>📦 {asset_name}</h3>", unsafe_allow_html=True)
            st.divider()
            
            # Displays main numerical state configurations
            col_a, col_b, col_c = st.columns(3)
            with col_a: st.markdown(f"**Spot Rate:**\n### {c_sym}{formatted_price}")
            with col_b: st.markdown(f"**Live Signal:**\n<h3 style='color:{color}; margin-top:5px;'>{direction}</h3>", unsafe_allow_html=True)
            with col_c: st.markdown(f"**Hourly RSI:**\n### `{hourly_rsi:.1f}`")
            
            # CRITICAL DESIGN ITEM: Stop Loss and Take Profit calculated and displayed BEFORE the chart
            if direction != "⏳ HOLD / PRESERVE CASH":
                st.divider()
                mult = 10000 if ("=" in target_asset and "ZAR" not in target_asset) else 1
                pts_sl = np.abs(price - stop_loss) * mult
                pts_tp = np.abs(take_profit - price) * mult
                if "ZAR" in target_asset: pts_sl, pts_tp = 800.0, 2000.0
                
                st.markdown("### 📲 NATIVE IG TICKET CODES (ENTRY PROTECTIONS):")
                col_sl, col_tp = st.columns(2)
                with col_sl:
                    st.markdown(f"<div style='border: 1px solid #FF0000; padding:10px; border-radius:4px; text-align:center;'><span style='color:#FF0000; font-weight:bold;'>🛑 STOP-LOSS FIELD:</span><br><code style='font-size:18px;'>{pts_sl:.1f} pts away</code></div>", unsafe_allow_html=True)
                with col_tp:
                    st.markdown(f"<div style='border: 1px solid #00FF00; padding:10px; border-radius:4px; text-align:center;'><span style='color:#00FF00; font-weight:bold;'>🎯 TAKE-PROFIT FIELD:</span><br><code style='font-size:18px;'>{pts_tp:.1f} pts away</code></div>", unsafe_allow_html=True)
            
            st.divider()
            st.markdown("#### 📈 Intraday Price Wave Chart")
            st.line_chart(hourly_df['Close'].tail(48))

# ==================================================================================
# 📡 NAVIGATION ROW 2: TICKER-DYNAMIC SPECIALIZED MACRO ECONOMICS NEWS TERMINAL
# ==================================================================================
elif page_select == "📡 SPECIALIZED NEWS":
    st.markdown(f"### 📰 Mars_bot Custom Research Desk: {target_asset}")
    st.divider()
    
    if not ticker_feed.news:
        st.warning(f"📡 Sweeping global networks... No localized headline logs returned for target string: '{target_asset}' right now. Displaying baseline sovereign intelligence feeds:")
        news_list = [
            {"title": "🦅 Federal Reserve Enforces Data-Dependence Over Late-Autumn Sessions", "summary": "Institutional dollar desks verify that robust labor metrics (165K payrolls) give central bankers room to hold interest rates steady to absorb supply anomalies."},
