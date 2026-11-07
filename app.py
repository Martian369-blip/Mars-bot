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

# Initialize premium terminal view window layout
st.set_page_config(page_title="MARS_BOT V16.0", page_icon="👽", layout="centered", initial_sidebar_state="collapsed")

# Execute our newly skinned premium external styling file
lc.load_ig_style()

# Maintain system data session cores across sidebar tab navigation switches
if "journal_db" not in st.session_state:
    st.session_state.journal_db = pd.DataFrame(columns=["Asset", "Action", "Cash In (R)", "Cash Out (R)", "Net P&L (ZAR)", "Entry Price", "Win/Loss %", "Status"])
if "live_balance" not in st.session_state:
    st.session_state.live_balance = 500.0
if "cached_target_asset" not in st.session_state:
    st.session_state.cached_target_asset = "USDZAR=X"
if "cached_display_name" not in st.session_state:
    st.session_state.cached_display_name = "USD/ZAR"
if "price" not in st.session_state:
    st.session_state.price = 0.0
if "direction" not in st.session_state:
    st.session_state.direction = "HOLD"
if "color" not in st.session_state:
    st.session_state.color = "#FFB300"
if "hourly_rsi" not in st.session_state:
    st.session_state.hourly_rsi = 50.0

# 📅 MULTI-NATION TRADING SECTOR CLOCK TICKER GRID (WITH PULSING STYLE OVERLAYS)
current_hour_sa = datetime.datetime.now().hour
london_status = "<span style='color:#4CAF50;'>● OPEN</span>" if (9 <= current_hour_sa <= 17) else "<span style='color:#E53935;'>○ CLOSED</span>"
newyork_status = "<span style='color:#4CAF50;'>● OPEN</span>" if (15 <= current_hour_sa <= 22) else "<span style='color:#E53935;'>○ CLOSED</span>"
jse_status = "<span style='color:#4CAF50;'>● OPEN</span>" if (9 <= current_hour_sa <= 17) else "<span style='color:#E53935;'>○ CLOSED</span>"

st.markdown(
    f"<div style='background-color:#12161B; border:1px solid #1E252D; padding:8px; border-radius:4px; text-align:center; font-size:10px; font-family:monospace; letter-spacing:1px; color:#90A4AE; margin-bottom:20px;'> "
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

# Persistent memory data sync pipeline loop
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
                st.session_state.direction, st.session_state.color = "BUY / LONG", "#4CAF50"
            elif st.session_state.hourly_rsi > 65 or (st.session_state.price >= (recent_high * 0.995)):
                st.session_state.direction, st.session_state.color = "SELL / SHORT", "#E53935"
            else:
                st.session_state.direction, st.session_state.color = "HOLD / STANDBY", "#757575"
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
hourly_rsi = st.session_state.hourly_rsi
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
        c_sym = "R " if ("ZAR" in target_asset or ".JO" in target_asset) else "$ "
        formatted_price = f"{price:.4f}" if "ZAR" in target_asset else (f"{price:.5f}" if "=" in target_asset else f"{price:.2f}")
        
        # 🚀 High-Density Emerald Glowing Data Container Grid Wrapper Block
        st.markdown(f"""
            <div class='cyber-card'>
                <h3 style='text-align:center; color:#FFFFFF; margin-top:0px; font-weight:800; font-family:monospace; letter-spacing:1px;'>⚡ {ig_display_name} CORE SUMMARY</h3>
                <hr style='border-color:#1E252D; margin:15px 0;'>
                <div style='display: flex; justify-content: space-between; text-align: center;'>
                    <div style='flex: 1;'>
                        <p style='color:#90A4AE; font-size:10px; margin-bottom:5px; font-weight:bold; letter-spacing:1px;'>SPOT VALUE</p>
                        <h2 class='matrix-num' style='margin:0; font-size:24px;'>{c_sym}{formatted_price}</h2>
                    </div>
                    <div style='flex: 1; border-left: 1px solid #1E252D; border-right: 1px solid #1E252D;'>
                        <p style='color:#90A4AE; font-size:10px; margin-bottom:5px; font-weight:bold; letter-spacing:1px;'>SYS SIGNAL</p>
                        <h2 style='color:{color}; margin:0; font-weight:bold; font-size:20px;'>{direction}</h2>
                    </div>
                    <div style='flex: 1;'>
                        <p style='color:#90A4AE; font-size:10px; margin-bottom:5px; font-weight:bold; letter-spacing:1px;'>MATRIX RSI</p>
                        <h2 class='matrix-num' style='margin:0; font-size:24px;'>{hourly_rsi:.1f}</h2>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<p style='font-size:11px; font-weight:bold; letter-spacing:1px; color:#90A4AE; margin-bottom:12px; font-family:monospace;'>🕯️ REAL-TIME TELEMETRY CANDLESTICK GRID ARRAY</p>", unsafe_allow_html=True)
        
        # Polished Emerald Technical Candlestick Execution Configuration Layer
        fig_sig = go.Figure()
        fig_sig.add_trace(go.Candlestick(
            x=hourly_df.tail(48).index, open=hourly_df.tail(48)['Open'], high=hourly_df.tail(48)['High'],
            low=hourly_df.tail(48)['Low'], close=hourly_df.tail(48)['Close'], name="Market",
            increasing_line_color='#4CAF50', decreasing_line_color='#B71C1C',
            increasing_fillcolor='#1B5E20', decreasing_fillcolor='#7F0000'
        ))
        fig_sig.update_layout(
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#12161B',
            xaxis_rangeslider_visible=False, height=330, margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(gridcolor='#1E252D', tickfont=dict(family='monospace', size=10)),
            yaxis=dict(gridcolor='#1E252D', tickfont=dict(family='monospace', size=10))
        )
        st.plotly_chart(fig_sig, use_container_width=True)

elif page_select == "📡 SATELLITE NEWS":
    np_view.render_news_tab(target_asset, ig_display_name)

elif page_select == "🕹️ LEDGER JOURNAL":
    jp_view.render_journal_tab(target_asset, ig_display_name, price)
