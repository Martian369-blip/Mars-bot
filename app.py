import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import datetime
import os
import engine as eng
import news_panel as np_view
import journal_panel as jp_view
import layout_config as lc

# Initialize premium terminal view window layout
st.set_page_config(page_title="MARS_BOT V16.0", page_icon="👽", layout="centered", initial_sidebar_state="collapsed")
lc.load_ig_style()

# 🕹️ OPTION 3: PERMANENT FILE JOURNAL PERSISTENCE ENGINE LAYER
PERSISTENT_FILE = "ledger_vault.csv"

def load_persistent_ledger():
    """Hydrates master shared database history directly from hidden local disk vault."""
    if os.path.exists(PERSISTENT_FILE):
        try:
            return pd.read_csv(PERSISTENT_FILE)
        except Exception:
            pass
    return pd.DataFrame(columns=["Timestamp", "Asset", "Action", "Price", "Matrix RSI", "Status"])

def save_persistent_ledger(df):
    """Saves updated user ledger inputs safely to local workspace block."""
    df.to_csv(PERSISTENT_FILE, index=False)

# Maintain system data session cores across sidebar tab navigation switches
if "journal_db" not in st.session_state:
    st.session_state.journal_db = load_persistent_ledger()
if "live_balance" not in st.session_state:
    st.session_state.live_balance = 500.0
if "cached_target_asset" not in st.session_state:
    st.session_state.cached_target_asset = "USDZAR=X"
if "cached_display_name" not in st.session_state:
    st.session_state.cached_display_name = "USD/ZAR"
if "price" not in st.session_state:
    st.session_state.price = 0.0
if "direction" not in st.session_state:
    st.session_state.direction = "HOLD / STANDBY"
if "color" not in st.session_state:
    st.session_state.color = "#757575"
if "m15_rsi" not in st.session_state:
    st.session_state.m15_rsi = 50.0
if "h1_rsi" not in st.session_state:
    st.session_state.h1_rsi = 50.0
if "h4_rsi" not in st.session_state:
    st.session_state.h4_rsi = 50.0

# 📅 MULTI-NATION TRADING SECTOR CLOCK TICKER GRID (WITH PULSING STYLE OVERLAYS)
current_hour_sa = datetime.datetime.now().hour
london_status = "<span style='color:#4CAF50;'>● OPEN</span>" if (9 <= current_hour_sa <= 17) else "<span style='color:#E53935;'>○ CLOSED</span>"
newyork_status = "<span style='color:#4CAF50;'>● OPEN</span>" if (15 <= current_hour_sa <= 22) else "<span style='color:#E53935;'>○ CLOSED</span>"
jse_status = "<span style='color:#4CAF50;'>● OPEN</span>" if (9 <= current_hour_sa <= 17) else "<span style='color:#E53935;'>○ CLOSED</span>"

st.markdown(
    f"<div style='background-color:#120A26; border:1px solid #1F1140; padding:8px; border-radius:4px; text-align:center; font-size:10px; font-family:monospace; letter-spacing:1px; color:#90A4AE; margin-bottom:20px;'> "
    f"LON: {london_status} | NYC: {newyork_status} | JSE: {jse_status}"
    f"</div>", 
    unsafe_allow_html=True
)

st.markdown("<h2 style='text-align: center; color: #FFFFFF !important; margin-bottom: 25px; font-weight: 900; letter-spacing: 2px;'>🛸 MARS_BOT <span style='color:#4CAF50;'>V16.0</span></h2>", unsafe_allow_html=True)

ig_name_map = {
    "USDZAR=X": "USD/ZAR", "GBPUSD=X": "GBP/USD", "GC=F": "Gold", "EURUSD=X": "EUR/USD", 
    "USDJPY=X": "USD/JPY", "AUDUSD=X": "AUD/USD", "USDCAD=X": "USD/CAD", "CL=F": "Oil - Crude"
}
display_options = list(ig_name_map.values())

# Clean horizontal search grid row
col_search, col_trigger = st.columns([0.75, 0.25])
with col_search:
    chosen_display = st.selectbox("🔍 SELECT MARKET WORKSPACE:", options=display_options, label_visibility="collapsed")

reverse_map = {v: k for k, v in ig_name_map.items()}
selected_ticker = reverse_map.get(chosen_display, "USDZAR=X")

with col_trigger:
    search_activated = st.button("🛰️ SCAN")

# 🚀 OPTION 2: MULTI-TIMEFRAME CONVERGENCE MATRIX PIPELINE FETCH
if search_activated or st.session_state.price == 0.0:
    st.session_state.cached_target_asset = selected_ticker
    st.session_state.cached_display_name = chosen_display
    try:
        ticker_feed = yf.Ticker(st.session_state.cached_target_asset)
        
        # Pull discrete interval tracks
        df_15m = ticker_feed.history(period="5d", interval="15m")
        df_1h = ticker_feed.history(period="30d", interval="1h")
        df_4h = ticker_feed.history(period="60d", interval="4h")
        
        # Safe fallback checks
        if df_15m.empty: df_15m = df_1h.copy()
        if df_4h.empty: df_4h = df_1h.copy()
        
        if not df_1h.empty:
            # Process calculations across each matrix layer independently
            rsi_15m = eng.calculate_rsi(df_15m).iloc[-1]
            rsi_1h = eng.calculate_rsi(df_1h).iloc[-1]
            rsi_4h = eng.calculate_rsi(df_4h).iloc[-1]
            
            st.session_state.price = df_1h['Close'].iloc[-1]
            st.session_state.m15_rsi = rsi_15m
            st.session_state.h1_rsi = rsi_1h
            st.session_state.h4_rsi = rsi_4h
            
            # 🔥 MULTI-TIMEFRAME ALIGNMENT CRITERIA (REQUIRES OVERLAPPING CONCURRENCE)
            bullish_alignment = (rsi_15m < 40) and (rsi_1h < 45) and (rsi_4h < 50)
            bearish_alignment = (rsi_15m > 60) and (rsi_1h > 55) and (rsi_4h > 50)
            
            if bullish_alignment:
                st.session_state.direction, st.session_state.color = "🚀 CONVERGENT BUY", "#4CAF50"
            elif bearish_alignment:
                st.session_state.direction, st.session_state.color = "💥 CONVERGENT SELL", "#E53935"
            else:
                st.session_state.direction, st.session_state.color = "⏳ HOLD / STANDBY", "#757575"
    except Exception as e:
        pass

# 🧭 SIDEBAR CONSOLE COMMAND ROUTER PANEL
st.sidebar.markdown("<h3 style='color:#4CAF50 !important; font-weight:900; letter-spacing:1px;'>☰ MAIN CORE</h3>", unsafe_allow_html=True)
page_select = st.sidebar.radio("CHOOSE MODULE SHEET:", ["📊 TERMINAL SIGNALS", "📡 SATELLITE NEWS", "🕹️ LEDGER JOURNAL"])
st.sidebar.divider()
st.sidebar.caption("👽 Core Apex Emerald Multi-Module Layout Architecture.")

# Extract memory cached parameters directly into current local tab frame
target_asset = st.session_state.cached_target_asset
ig_display_name = st.session_state.cached_display_name
price = st.session_state.price
m15_rsi = st.session_state.m15_rsi
h1_rsi = st.session_state.h1_rsi
h4_rsi = st.session_state.h4_rsi
direction = st.session_state.direction
color = st.session_state.color

# ==================================================================================
# SWITCHBOARD ROUTING LAYER
# ==================================================================================
if page_select == "📊 TERMINAL SIGNALS":
    st.markdown(f"#### 📡 Telemetry Feed Workspace: <span style='color:#4CAF50;'>{ig_display_name}</span>", unsafe_allow_html=True)
    
    ticker_feed = yf.Ticker(target_asset)
    hourly_df = ticker_feed.history(period="1mo", interval="1h")
    
    if hourly_df.empty:
        st.warning("🔄 Connecting to core telemetry stream grid...")
    else:
        c_sym = "R " if ("ZAR" in target_asset or ".JO" in target_asset) else "$"
        formatted_price = f"{price:.4f}" if "ZAR" in target_asset else (f"{price:.5f}" if "=" in target_asset else f"{price:.2f}")
        
        # 🚀 High-Density Emerald Glowing Data Container Grid Wrapper Block
        st.markdown(f"""
            <div class='cyber-card'>
                <h3 style='text-align:center; color:#FFFFFF; margin-top:0px; font-weight:800; font-family:monospace; letter-spacing:1px;'>⚡ {ig_display_name} MULTI-MATRIX</h3>
                <hr style='border-color:#1F1140; margin:15px 0;'>
                <div style='display: flex; justify-content: space-between; text-align: center;'>
                    <div style='flex: 1;'>
                        <p style='color:#90A4AE; font-size:10px; margin-bottom:5px; font-weight:bold; letter-spacing:1px;'>SPOT VALUE</p>
                        <h2 class='matrix-num' style='margin:0; font-size:24px;'>{c_sym}{formatted_price}</h2>
                    </div>
                    <div style='flex: 1; border-left: 1px solid #1F1140; border-right: 1px solid #1F1140;'>
                        <p style='color:#90A4AE; font-size:10px; margin-bottom:5px; font-weight:bold; letter-spacing:1px;'>CONVERGENCE SIGNAL</p>
                        <h2 style='color:{color}; margin:0; font-weight:bold; font-size:18px;'>{direction}</h2>
                    </div>
                    <div style='flex: 1;'>
                        <p style='color:#90A4AE; font-size:10px; margin-bottom:5px; font-weight:bold; letter-spacing:1px;'>H1 MATRIX RSI</p>
                        <h2 class='matrix-num' style='margin:0; font-size:24px;'>{h1_rsi:.1f}</h2>
                    </div>
                </div>
                <hr style='border-color:#1F1140; margin:15px 0;'>
                <div style='display: flex; justify-content: space-around; text-align: center; font-family:monospace; font-size:11px; color:#CFD8DC;'>
                    <div>15M RSI: <b style='color:#4CAF50;'>{m15_rsi:.1f}</b></div>
                    <div>1H RSI: <b style='color:#4CAF50;'>{h1_rsi:.1f}</b></div>
                    <div>4H RSI: <b style='color:#4CAF50;'>{h4_rsi:.1f}</b></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<p style='font-size:11px; font-weight:bold; letter-spacing:1px; color:#90A4AE; margin-bottom:12px; font-family:monospace;'>🕯️ REAL-TIME TELEMETRY CANDLESTICK GRID ARRAY</p>", unsafe_allow_html=True)
        
        plot_df = hourly_df.tail(48)
        fig_sig = go.Figure()
        fig_sig.add_trace(go.Candlestick(
            x=plot_df.index, open=plot_df['Open'], high=plot_df['High'],
            low=plot_df['Low'], close=plot_df['Close'], name="Market",
            increasing_line_color='#4CAF50', decreasing_line_color='#B71C1C',
            increasing_fillcolor='#1B5E20', decreasing_fillcolor='#7F0000'
        ))
        
