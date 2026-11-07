import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime
import engine as eng
import news_panel as np_view
import journal_panel as jp_view
import layout_config as lc

st.set_page_config(page_title="MARS_BOT V15.5", page_icon="👽", layout="centered", initial_sidebar_state="collapsed")
lc.load_ig_style()

# 🛸 INITIALIZE MASTER GLOBAL SESSION CORES TO PREVENT DATA VANISHING
if "journal_db" not in st.session_state:
    st.session_state.journal_db = pd.DataFrame(columns=["Asset", "Action", "Cash In (R)", "Cash Out (R)", "Net P&L (ZAR)", "Entry Price", "Win/Loss %", "Status"])
if "live_balance" not in st.session_state:
    st.session_state.live_balance = 500.0
if "cached_target_asset" not in st.session_state:
    st.session_state.cached_target_asset = "USDZAR=X"
if "cached_display_name" not in st.session_state:
    st.session_state.cached_display_name = "USD/ZAR"
if "price" not in st.session_state:
    st.session_state.price = 16.5170
if "direction" not in st.session_state:
    st.session_state.direction = "⏳ HOLD / PRESERVE CASH"
if "color" not in st.session_state:
    st.session_state.color = "#FFB300"
if "hourly_rsi" not in st.session_state:
    st.session_state.hourly_rsi = 50.0
if "hourly_atr" not in st.session_state:
    st.session_state.hourly_atr = 0.015
if "candle_pattern_alert" not in st.session_state:
    st.session_state.candle_pattern_alert = "⏳ AWAITING FRESH SATELLITE SCAN..."
if "stop_loss" not in st.session_state:
    st.session_state.stop_loss = 0.0
if "take_profit" not in st.session_state:
    st.session_state.take_profit = 0.0

# 📅 MULTI-NATION TRADING SECTOR CLOCK TICKER GRID
current_hour_sa = datetime.datetime.now().hour
london_status = "🟢 OPEN" if (9 <= current_hour_sa <= 17) else "🔴 CLOSED"
newyork_status = "🟢 OPEN" if (15 <= current_hour_sa <= 22) else "🔴 CLOSED"
jse_status = "🟢 OPEN" if (9 <= current_hour_sa <= 17) else "🔴 CLOSED"

st.markdown(
    f"<div style='background-color:#161A1E; border:1px solid #23292F; padding:8px; border-radius:4px; text-align:center; font-size:11px; letter-spacing:0.5px; color:#90A4AE; margin-bottom:15px;'> "
    f"🇬🇧 LONDON: <b style='color:#FFFFFF;'>{london_status}</b> | "
    f"🇺🇸 NEW YORK: <b style='color:#FFFFFF;'>{newyork_status}</b> | "
    f"🇿🇦 JOHANNESBURG JSE: <b style='color:#FFFFFF;'>{jse_status}</b>"
    f"</div>", 
    unsafe_allow_html=True
)

st.markdown("<h2 style='text-align: center; color: #00A4E4 !important; margin-bottom: 5px;'>🛸 MARS_BOT V15.5</h2>", unsafe_allow_html=True)

ig_name_map = {
    "USDZAR=X": "USD/ZAR", "GBPUSD=X": "GBP/USD", "GC=F": "Gold", "EURUSD=X": "EUR/USD", 
    "USDJPY=X": "USD/JPY", "AUDUSD=X": "AUD/USD", "USDCAD=X": "USD/CAD", "CL=F": "Oil - Crude"
}
display_options = list(ig_name_map.values())

col_search, col_trigger = st.columns([0.75, 0.25])
with col_search:
    chosen_display = st.selectbox("🔍 SELECT MARKET WORKSPACE:", options=display_options, label_visibility="collapsed")

reverse_map = {v: k for k, v in ig_name_map.items()}
selected_ticker = reverse_map.get(chosen_display, "USDZAR=X")

with col_trigger:
    search_activated = st.button("🛰️ SCAN")

# 📥 DATA FETCH LAYER - RUNS ON CLICK & STORES SECURELY IN SESSION CACHE
if search_activated or st.session_state.price == 16.5170:
    st.session_state.cached_target_asset = selected_ticker
    st.session_state.cached_display_name = chosen_display
    
    try:
        ticker_feed = yf.Ticker(st.session_state.cached_target_asset)
        daily_df = ticker_feed.history(period="3mo", interval="1d")
        hourly_df = ticker_feed.history(period="1mo", interval="1h")
        
        if hourly_df.empty and not daily_df.empty:
            hourly_df = daily_df.copy()
            
        if not daily_df.empty and not hourly_df.empty:
            daily_df['RSI'] = eng.calculate_rsi(daily_df)
            hourly_df['RSI'] = eng.calculate_rsi(hourly_df)
            
            st.session_state.price = daily_df['Close'].iloc[-1]
            st.session_state.hourly_rsi = hourly_df['RSI'].iloc[-1]
            st.session_state.hourly_atr = eng.extract_hourly_atr(hourly_df)
            st.session_state.candle_pattern_alert = eng.scan_candlestick_patterns(hourly_df)
            
            recent_low = hourly_df['Low'].tail(24).min()
            recent_high = hourly_df['High'].tail(24).max()
            
            if st.session_state.hourly_rsi < 35 or (st.session_state.price <= (recent_low * 1.005)):
                st.session_state.direction = "🚀 BUY / LONG"
                st.session_state.color = "#4CAF50"
                st.session_state.stop_loss = st.session_state.price - (st.session_state.hourly_atr * 1.5)
                st.session_state.take_profit = st.session_state.price + ((st.session_state.price - st.session_state.stop_loss) * 2.5)
            elif st.session_state.hourly_rsi > 65 or (st.session_state.price >= (recent_high * 0.995)):
                st.session_state.direction = "💥 SELL / SHORT"
                st.session_state.color = "#E53935"
                st.session_state.stop_loss = st.session_state.price + (st.session_state.hourly_atr * 1.5)
                st.session_state.take_profit = st.session_state.price - ((st.session_state.stop_loss - st.session_state.price) * 2.5)
            else:
                st.session_state.direction = "⏳ HOLD / PRESERVE CASH"
                st.session_state.color = "#FFB300"
                st.session_state.stop_loss = st.session_state.price
                st.session_state.take_profit = st.session_state.price
    except Exception as e:
        pass

# 🧭 SIDEBAR NAVIGATION PANEL
st.sidebar.markdown("<h3 style='color:#00A4E4 !important;'>☰ IG CONSOLE</h3>", unsafe_allow_html=True)
page_select = st.sidebar.radio("NAVIGATION PANEL:", ["📊 EXECUTIVE SIGNALS", "📡 SPECIALIZED NEWS", "🕹️ WORKSPACE JOURNAL"])
st.sidebar.divider()
st.sidebar.caption("👽 V15.5 Core Apex Multi-Module Architecture.")

# Persistent state variable routing
target_asset = st.session_state.cached_target_asset
ig_display_name = st.session_state.cached_display_name
price = st.session_state.price
hourly_rsi = st.session_state.hourly_rsi
hourly_atr = st.session_state.hourly_atr
direction = st.session_state.direction
color = st.session_state.color
stop_loss = st.session_state.stop_loss
take_profit = st.session_state.take_profit
candle_pattern_alert = st.session_state.candle_pattern_alert

# ==================================================================================
# SWITCHBOARD ROUTING LAYER
# ==================================================================================
if page_select == "📊 EXECUTIVE SIGNALS":
    st.markdown(f"#### 🎯 Live Sovereign Matrix Sheet: <span style='color:#00A4E4;'>{ig_display_name}</span>", unsafe_allow_html=True)
    st.info(f"👀 **Structure Matrix Status:** {candle_pattern_alert}")
    
    ticker_feed = yf.Ticker(target_asset)
    hourly_df = ticker_feed.history(period="1mo", interval="1h")
    daily_df = ticker_feed.history(period="3mo", interval="1d")
    
    if daily_df.empty or hourly_df.empty:
        st.warning("🔄 Fetching live data parameters...")
    else:
        c_sym = "R" if ("ZAR" in target_asset or ".JO" in target_asset) else "$"
        formatted_price = f"{price:.4f}" if "ZAR" in target_asset else (f"{price:.5f}" if "=" in target_asset else f"{price:.2f}")
        
        with st.container():
            st.markdown(f"<h3 style='text-align: center; margin: 0px; color:#FFFFFF;'>📦 {ig_display_name}</h3>", unsafe_allow_html=True)
            st.divider()
            
            col_a, col_b, col_c = st.columns(3)
            with col_a: st.markdown(f"**Spot Rate:**\n### {c_sym}{formatted_price}")
            with col_b: st.markdown(f"**Live Signal:**\n<h3 style='color:{color}; margin-top:5px;'>{direction}</h3>", unsafe_allow_html=True)
            with col_c: st.markdown(f"**Hourly RSI:**\n### `{hourly_rsi:.1f}`")
            
            st.divider()
            st.markdown("<p style='font-size:12px; font-weight:bold; color:#90A4AE; letter-spacing:0.5px;'>📊 MARKET RANGE & VOLATILITY GAUGES:</p>", unsafe_allow_html=True)
            col_v1, col_v2 = st.columns(2)
            
            pip_multiplier = 10000 if ("=" in target_asset and "ZAR" not in target_asset) else 1
            atr_pips = hourly_atr * pip_multiplier
            
            day_high = daily_df['High'].iloc[-1]
            day_low = daily_df['Low'].iloc[-1]
            total_range = day_high - day_low
            current_range_exhaustion = ((price - day_low) / total_range * 100) if total_range > 0 else 50.0
            
            with col_v1:
                st.markdown(f"<div style='background-color:#161A1E; border:1px solid #23292F; padding:10px; border-radius:4px; text-align:center;'>⚡ <span style='color:#90A4AE; font-size:11px;'>HOURLY ATR EXPRESSION</span><br><b style='font-size:18px; color:#FFFFFF;'>{atr_pips:.1f} <span style='font-size:12px; color:#00A4E4;'>pips</span></b></div>", unsafe_allow_html=True)
            with col_v2:
                st.markdown(f"<div style='background-color:#161A1E; border:1px solid #23292F; padding:10px; border-radius:4px; text-align:center;'>🎯 <span style='color:#90A4AE; font-size:11px;'>DAILY RANGE EXHAUSTION</span><br><b style='font-size:18px; color:#FFFFFF;'>{current_range_exhaustion:.1f}% <span style='font-size:12px; color:#FFB300;'>filled</span></b></div>", unsafe_allow_html=True)
            
            st.divider()
            st.markdown("<p style='font-size:13px; font-weight:bold; letter-spacing:0.5px; color:#90A4AE;'>🕯️ REAL-TIME DEALING CANDLESTICK GRAPH WITH TARGET BARRIERS</p>", unsafe_allow_html=True)
            
            plot_df = hourly_df.tail(48)
            fig_sig = go.Figure()
            fig_sig.add_trace(go.Candlestick(
                x=plot_df.index, open=plot_df['Open'], high=plot_df['High'],
