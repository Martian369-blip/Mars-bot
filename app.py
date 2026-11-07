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

# PERSISTENT JOURNAL VAULT CONSTANTS
PERSISTENT_FILE = "ledger_vault.csv"

def load_persistent_ledger():
    if os.path.exists(PERSISTENT_FILE):
        try: 
            return pd.read_csv(PERSISTENT_FILE)
        except Exception: 
            pass
    return pd.DataFrame(columns=["Timestamp", "Asset", "Action", "Price", "Matrix RSI", "Status"])

def save_persistent_ledger(df):
    df.to_csv(PERSISTENT_FILE, index=False)

# Secure active session memory cores
if "journal_db" not in st.session_state:
    st.session_state.journal_db = load_persistent_ledger()
if "cached_target_asset" not in st.session_state:
    st.session_state.cached_target_asset = "USDZAR=X"
if "cached_display_name" not in st.session_state:
    st.session_state.cached_display_name = "USD/ZAR"
if "price" not in st.session_state: 
    st.session_state.price = 16.5170
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

# 🛰️ OPTION 1: HIGH-IMPACT AUTOMATED MACRO ECONOMIC VOLATILITY RADAR
def process_macro_volatility_gauge():
    current_time = datetime.datetime.now()
    macro_calendar = [
        {"event": "🇺🇸 US Core CPI Inflation Print", "date": datetime.date(2026, 11, 12), "hour": 15, "minute": 30},
        {"event": "🇿🇦 SARB Interest Rate Decision", "date": datetime.date(2026, 11, 19), "hour": 15, "minute": 0},
        {"event": "🇺🇸 Federal Reserve FOMC Decision", "date": datetime.date(2026, 12, 16), "hour": 21, "minute": 0},
    ]
    active_threat = None
    time_str = ""
    for item in macro_calendar:
        event_datetime = datetime.datetime.combine(item["date"], datetime.time(item["hour"], item["minute"]))
        if event_datetime > current_time:
            time_delta = event_datetime - current_time
            if time_delta.total_seconds() <= 86400:
                active_threat = item["event"]
                hours, remainder = divmod(int(time_delta.total_seconds()), 3600)
                minutes, _ = divmod(remainder, 60)
                time_str = f"{hours}h {minutes}m"
                break
    if active_threat:
        st.markdown(f"<div style='background-color:#7F0000; border:2px solid #FF3D00; padding:12px; border-radius:4px; text-align:center; margin-bottom:15px;'><span style='color:#FFFFFF; font-family:monospace; font-weight:bold; font-size:11px;'>🚨 MACRO CRITICAL ALERT: {active_threat.upper()} TARGET IN {time_str}! EXPECT FLUID LIQUIDATION SHOCKS!</span></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='background-color:#120A26; border:1px solid #1F1140; padding:8px; border-radius:4px; text-align:center; margin-bottom:15px; font-size:10px; font-family:monospace; color:#4CAF50;'>🛰️ SATELLITE MACRO RADAR: GLOBAL GEOPOLITICAL FLOW MATRIX CLEAR. NO IMMEDIATE VOLATILITY BLOCKS ENCOUNTERED.</div>", unsafe_allow_html=True)

process_macro_volatility_gauge()

# 📅 MULTI-NATION CLOCK TICKS
current_hour_sa = datetime.datetime.now().hour
london_status = "<span style='color:#4CAF50;'>● OPEN</span>" if (9 <= current_hour_sa <= 17) else "<span style='color:#E53935;'>○ CLOSED</span>"
newyork_status = "<span style='color:#4CAF50;'>● OPEN</span>" if (15 <= current_hour_sa <= 22) else "<span style='color:#E53935;'>○ CLOSED</span>"
st.markdown(f"<div style='background-color:#120A26; border:1px solid #1F1140; padding:8px; border-radius:4px; text-align:center; font-size:10px; font-family:monospace; color:#90A4AE; margin-bottom:20px;'>LON: {london_status} | NYC: {newyork_status}</div>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #FFFFFF !important; margin-bottom: 25px; font-weight: 900;'>🛸 MARS_BOT <span style='color:#4CAF50;'>V16.0</span></h2>", unsafe_allow_html=True)

ig_name_map = {
    "USDZAR=X": "USD/ZAR", "GBPUSD=X": "GBP/USD", "GC=F": "Gold", "EURUSD=X": "EUR/USD", 
    "USDJPY=X": "USD/JPY", "AUDUSD=X": "AUD/USD", "USDCAD=X": "USD/CAD"
}
display_options = list(ig_name_map.values())

col_search, col_trigger = st.columns([0.75, 0.25])
with col_search:
    chosen_display = st.selectbox("🔍 MARKET WORKSPACE:", options=display_options, label_visibility="collapsed")

reverse_map = {v: k for k, v in ig_name_map.items()}
selected_ticker = reverse_map.get(chosen_display, "USDZAR=X")

with col_trigger:
    search_activated = st.button("🛰️ SCAN")

# 📥 GLOBAL HIGH-SPEED TELEMETRY FETCH PIPELINE
if search_activated or st.session_state.price == 16.5170 or st.session_state.cached_target_asset != selected_ticker:
    st.session_state.cached_target_asset = selected_ticker
    st.session_state.cached_display_name = chosen_display
    try:
        ticker_feed = yf.Ticker(st.session_state.cached_target_asset)
        df_15m = ticker_feed.history(period="5d", interval="15m")
        df_1h = ticker_feed.history(period="30d", interval="1h")
        df_4h = ticker_feed.history(period="60d", interval="4h")
        
        if not df_1h.empty:
            rsi_15m = eng.calculate_rsi(df_15m).iloc[-1] if not df_15m.empty else 50.0
            rsi_1h = eng.calculate_rsi(df_1h).iloc[-1]
            rsi_4h = eng.calculate_rsi(df_4h).iloc[-1] if not df_4h.empty else 50.0
            
            st.session_state.price = df_1h['Close'].iloc[-1]
            st.session_state.m15_rsi = rsi_15m
            st.session_state.h1_rsi = rsi_1h
            st.session_state.h4_rsi = rsi_4h
            
            if rsi_15m < 40 and rsi_1h < 45 and rsi_4h < 50:
                st.session_state.direction, st.session_state.color = "🚀 CONVERGENT BUY", "#4CAF50"
            elif rsi_15m > 60 and rsi_1h > 55 and rsi_4h > 50:
                st.session_state.direction, st.session_state.color = "💥 CONVERGENT SELL", "#E53935"
            else:
                st.session_state.direction, st.session_state.color = "⏳ HOLD / STANDBY", "#757575"
    except Exception: 
        pass

# 🧭 SIDEBAR MATRIX CONSOLE RADIO COMMAND PANEL
st.sidebar.markdown("<h3 style='color:#4CAF50 !important; font-weight:900;'>☰ MAIN CORE</h3>", unsafe_allow_html=True)
page_select = st.sidebar.radio("CHOOSE MODULE SHEET:", ["📊 TERMINAL SIGNALS", "📡 SATELLITE NEWS", "🕹️ LEDGER JOURNAL"])
st.sidebar.divider()
st.sidebar.caption("👽 V16.0 Flight Deck Multi-Module Schema.")

# Load active dataset from root states
target_asset = st.session_state.cached_target_asset
ig_display_name = st.session_state.cached_display_name
price = st.session_state.price
m15_rsi = st.session_state.m15_rsi
h1_rsi = st.session_state.h1_rsi
h4_rsi = st.session_state.h4_rsi
direction = st.session_state.direction
color = st.session_state.color

# ==================================================================================
# SWITCHBOARD ROUTING MODULES
# ==================================================================================
if page_select == "📊 TERMINAL SIGNALS":
    st.markdown(f"#### 📡 Telemetry Feed Workspace: <span style='color:#4CAF50;'>{ig_display_name}</span>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class='cyber-card'>
            <h3 style='text-align:center; color:#FFFFFF; margin-top:0px; font-family:monospace;'>⚡ {ig_display_name} MULTI-MATRIX</h3>
            <hr style='border-color:#1F1140; margin:15px 0;'>
            <div style='display: flex; justify-content: space-between; text-align: center;'>
                <div style='flex: 1;'>
                    <p style='color:#90A4AE; font-size:10px; margin-bottom:5px; font-weight:bold;'>SPOT VALUE</p>
                    <h2 class='matrix-num' style='margin:0; font-size:24px;'>{"R " if "ZAR" in target_asset else "$ "}{price:.4f}</h2>
                </div>
                <div style='flex: 1; border-left: 1px solid #1F1140; border-right: 1px solid #1F1140;'>
                    <p style='color:#90A4AE; font-size:10px; margin-bottom:5px; font-weight:bold;'>CONVERGENCE</p>
                    <h2 style='color:{color}; margin:0; font-size:18px;'>{direction}</h2>
                </div>
                <div style='flex: 1;'>
                    <p style='color:#90A4AE; font-size:10px; margin-bottom:5px; font-weight:bold;'>H1 RSI</p>
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
    
    st.markdown("<p style='font-size:11px; font-weight:bold; color:#90A4AE; margin-bottom:12px; font-family:monospace;'>🕯️ REAL-TIME TELEMETRY CANDLESTICK GRID ARRAY</p>", unsafe_allow_html=True)
    
    # 🕯️ SAFE RESTRUCTURED PLOT LAYER WITH PROPER INDENTATION
    try:
        t_feed = yf.Ticker(target_asset)
        h_df = t_feed.history(period="1mo", interval="1h")
        if not h_df.empty:
            plot_df = h_df.tail(48)
            fig_sig = go.Figure()
            fig_sig.add_trace(
                go.Candlestick(
