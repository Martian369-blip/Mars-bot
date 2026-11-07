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

# Initialize premium terminal window configurations
st.set_page_config(page_title="MARS_BOT V16.0", page_icon="👽", layout="centered", initial_sidebar_state="collapsed")

# 🔥 EXECUTING YOUR EXTERNAL DESIGN FILE DIRECTLY FROM STORAGE HOOK
lc.load_ig_style()

# Initialize master global session memory cores to prevent any sub-page data loss
if "journal_db" not in st.session_state:
    st.session_state.journal_db = pd.DataFrame(columns=["Asset", "Action", "Cash In (R)", "Cash Out (R)", "Net P&L (ZAR)", "Entry Price", "Win/Loss %", "Status"])
if "live_balance" not in st.session_state:
    st.session_state.live_balance = 500.0
if "cached_target_asset" not in st.session_state:
    st.session_state.cached_target_asset = "GBPUSD=X"
if "cached_display_name" not in st.session_state:
    st.session_state.cached_display_name = "GBP/USD"
if "price" not in st.session_state:
    st.session_state.price = 0.0
if "direction" not in st.session_state:
    st.session_state.direction = "HOLD"
if "color" not in st.session_state:
    st.session_state.color = "#FFB300"
if "hourly_rsi" not in st.session_state:
    st.session_state.hourly_rsi = 50.0

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

st.markdown("<h2 style='text-align: center; color: #00A4E4 !important; margin-bottom: 20px; font-weight: 800; letter-spacing: 1px;'>🛸 MARS_BOT V16.0</h2>", unsafe_allow_html=True)

ig_name_map = {
    "GBPUSD=X": "GBP/USD", "USDZAR=X": "USD/ZAR", "GC=F": "Gold", "EURUSD=X": "EUR/USD", 
    "USDJPY=X": "USD/JPY", "AUDUSD=X": "AUD/USD", "USDCAD=X": "USD/CAD", "CL=F": "Oil - Crude"
}
display_options = list(ig_name_map.values())

# Clean proportional grid alignment row
col_search, col_trigger = st.columns([3, 1])
with col_search:
    chosen_display = st.selectbox("🔍 SELECT MARKET WORKSPACE:", options=display_options, label_visibility="collapsed")

reverse_map = {v: k for k, v in ig_name_map.items()}
selected_ticker = reverse_map.get(chosen_display, "GBPUSD=X")

with col_trigger:
    search_activated = st.button("🛰️ SCAN")

# Data fetch layer handling pipeline with persistent caching fallbacks
if search_activated or st.session_state.price == 0.0:
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
            
            recent_low = hourly_df['Low'].tail(24).min()
            recent_high = hourly_df['High'].tail(24).max()
            if st.session_state.hourly_rsi < 35 or (st.session_state.price <= (recent_low * 1.005)):
                st.session_state.direction, st.session_state.color = "🚀 BUY / LONG", "#4CAF50"
            elif st.session_state.hourly_rsi > 65 or (st.session_state.price >= (recent_high * 0.995)):
                st.session_state.direction, st.session_state.color = "💥 SELL / SHORT", "#E53935"
            else:
                st.session_state.direction, st.session_state.color = "⏳ HOLD / PRESERVE CASH", "#FFB300"
    except Exception as e:
        pass

# 🧭 SIDEBAR MATRIX CONSOLE NAVIGATION PANEL
st.sidebar.markdown("<h3 style='color:#00A4E4 !important; font-weight:800; letter-spacing:0.5px;'>☰ IG CONSOLE</h3>", unsafe_allow_html=True)
page_select = st.sidebar.radio("NAVIGATION PANEL:", ["📊 EXECUTIVE SIGNALS", "📡 SPECIALIZED NEWS", "🕹️ WORKSPACE JOURNAL"])
st.sidebar.divider()
st.sidebar.caption("👽 V16.0 Sovereign Cyberpunk Skin Interface Grid.")

# Map state memory copies cleanly to current panel scopes
target_asset = st.session_state.cached_target_asset
ig_display_name = st.session_state.cached_display_name
price = st.session_state.price
hourly_rsi = st.session_state.hourly_rsi
direction = st.session_state.direction
color = st.session_state.color

# ==================================================================================
# SWITCHBOARD ROUTING LAYER
# ==================================================================================
if page_select == "📊 EXECUTIVE SIGNALS":
    st.markdown(f"#### 🎯 Live Sovereign Matrix Sheet: <span style='color:#00A4E4;'>{ig_display_name}</span>", unsafe_allow_html=True)
    
    ticker_feed = yf.Ticker(target_asset)
    hourly_df = ticker_feed.history(period="1mo", interval="1h")
    
    if hourly_df.empty:
        st.warning("🔄 Waiting for core matrix satellite stream...")
    else:
        c_sym = "R" if ("ZAR" in target_asset or ".JO" in target_asset) else "$"
        formatted_price = f"{price:.4f}" if "ZAR" in target_asset else (f"{price:.5f}" if "=" in target_asset else f"{price:.2f}")
        
        # Premium stylized sheet dashboard row block
        st.markdown(f"""
            <div style='background-color:#111519; border:1px solid #1E2329; border-radius:8px; padding:20px; margin-bottom:20px;'>
                <h3 style='text-align:center; color:#FFFFFF; margin-top:0px; font-weight:700;'>📦 {ig_display_name}</h3>
                <hr style='border-color:#1E2329; margin:15px 0;'>
                <div style='display: flex; justify-content: space-between; text-align: center;'>
                    <div style='flex: 1;'>
                        <p style='color:#90A4AE; font-size:12px; margin-bottom:5px; font-weight:bold;'>SPOT RATE</p>
                        <h2 style='color:#FFFFFF; margin:0; font-weight:800;'>{c_sym}{formatted_price}</h2>
                    </div>
                    <div style='flex: 1; border-left: 1px solid #1E2329; border-right: 1px solid #1E2329;'>
                        <p style='color:#90A4AE; font-size:12px; margin-bottom:5px; font-weight:bold;'>LIVE SIGNAL</p>
                        <h2 style='color:{color}; margin:0; font-weight:800;'>{direction}</h2>
                    </div>
                    <div style='flex: 1;'>
                        <p style='color:#90A4AE; font-size:12px; margin-bottom:5px; font-weight:bold;'>HOURLY RSI</p>
                        <h2 style='color:#FFFFFF; margin:0; font-weight:800;'>{hourly_rsi:.1f}</h2>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<p style='font-size:13px; font-weight:bold; letter-spacing:0.5px; color:#90A4AE; margin-bottom:10px;'>🕯️ REAL-TIME DEALING CANDLESTICK GRAPH</p>", unsafe_allow_html=True)
        
        fig_sig = go.Figure()
        fig_sig.add_trace(go.Candlestick(
            x=hourly_df.tail(48).index, open=hourly_df.tail(48)['Open'], high=hourly_df.tail(48)['High'],
            low=hourly_df.tail(48)['Low'], close=hourly_df.tail(48)['Close'], name="Market",
            increasing_line_color='#4CAF50', decreasing_line_color='#E53935'
        ))
        fig_sig.update_layout(
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#111519',
            xaxis_rangeslider_visible=False, height=340, margin=dict(l=10, r=10, t=10, b=10)
        )
        st.plotly_chart(fig_sig, use_container_width=True)

elif page_select == "📡 SPECIALIZED NEWS":
    np_view.render_news_tab(target_asset, ig_display_name)

elif page_select == "🕹️ WORKSPACE JOURNAL":
    jp_view.render_journal_tab(target_asset, ig_display_name, price)
