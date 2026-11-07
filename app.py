import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import engine as eng
import news_panel as np_view
import journal_panel as jp_view  # 🕹️ Import your premium automated cash ledger file
import layout_config as lc

st.set_page_config(page_title="MARS_BOT V12.6", page_icon="👽", layout="centered", initial_sidebar_state="collapsed")
lc.load_ig_style()

# Automated initialization using the updated structured keys
if "journal_db" not in st.session_state:
    st.session_state.journal_db = pd.DataFrame(columns=["Asset", "Action", "Cash In (R)", "Cash Out (R)", "Net P&L (ZAR)", "Entry Price", "Win/Loss %", "Status"])
if "live_balance" not in st.session_state:
    st.session_state.live_balance = 500.0

st.markdown("<h2 style='text-align: center; color: #00A4E4 !important; margin-bottom: 5px;'>🛸 MARS_BOT V12.6</h2>", unsafe_allow_html=True)

col_search, col_trigger = st.columns([4, 1])
with col_search:
    user_input = st.text_input("🔍 SEARCH ASSET SYMBOL:", value="GBPUSD=X", label_visibility="collapsed").strip().upper()

ig_name_map = {
    "EURUSD=X": "EUR/USD", "USDJPY=X": "USD/JPY", "AUDUSD=X": "AUD/USD", "GBPUSD=X": "GBP/USD",
    "EURJPY=X": "EUR/JPY", "USDCAD=X": "USD/CAD", "USDCHF=X": "USD/CHF", "EURGBP=X": "EUR/GBP",
    "USDZAR=X": "USD/ZAR", "GBPZAR=X": "GBP/ZAR", "GC=F": "Gold", "CL=F": "Oil - US Crude"
}

reverse_map = {v.upper(): k for k, v in ig_name_map.items()}
target_asset = reverse_map.get(user_input, user_input)
ig_display_name = ig_name_map.get(target_asset, target_asset)

with col_trigger:
    search_activated = st.button("🛰️ SCAN")

st.sidebar.markdown("<h3 style='color:#00A4E4 !important;'>☰ IG CONSOLE</h3>", unsafe_allow_html=True)
page_select = st.sidebar.radio(
    "NAVIGATION PANEL:",
    ["📊 EXECUTIVE SIGNALS", "📡 SPECIALIZED NEWS", "🕹️ WORKSPACE JOURNAL"]
)
st.sidebar.divider()
st.sidebar.caption("👽 Active IG Core Multi-Module Mesh Protocol.")

price, daily_rsi, hourly_rsi, hourly_atr, direction, color, stop_loss, take_profit = 0.0, 50.0, 50.0, 0.001, "HOLD", "#E53935", 0.0, 0.0
daily_df, hourly_df = pd.DataFrame(), pd.DataFrame()

try:
    ticker_feed = yf.Ticker(target_asset)
    daily_df = ticker_feed.history(period="3mo", interval="1d")
    hourly_df = ticker_feed.history(period="1mo", interval="1h")
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
            direction, color = "🚀 BUY / LONG", "#4CAF50"
            stop_loss = price - (hourly_atr * 1.5)
            take_profit = price + ((price - stop_loss) * 2.5)
        elif hourly_rsi > 65 or (price >= (recent_high * 0.995)):
            direction, color = "💥 SELL / SHORT", "#E53935"
            stop_loss = price + (hourly_atr * 1.5)
            take_profit = price - ((stop_loss - price) * 2.5)
        else:
            direction, color = "⏳ HOLD / PRESERVE CASH", "#FFB300"
            stop_loss, take_profit = price, price
            
        # Push variables to state memory so news modules can reference them instantly
        st.session_state['hourly_rsi'] = hourly_rsi
        st.session_state['current_price'] = price
        st.session_state['current_direction'] = direction
except Exception as e:
    st.sidebar.error(f"Telemetry Core Sync Warning: {str(e)}")

# ==================================================================================
# SWITCHBOARD ROUTING LAYER
# ==================================================================================
if page_select == "📊 EXECUTIVE SIGNALS":
    st.markdown(f"#### 🎯 Live Sovereign Matrix Sheet: <span style='color:#00A4E4;'>{ig_display_name}</span>", unsafe_allow_html=True)
    if daily_df.empty or hourly_df.empty:
        st.error(f"❌ Empty market node feedback. Verify symbol format: '{target_asset}'")
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
            if direction != "⏳ HOLD / PRESERVE CASH":
                st.divider()
                mult = 10000 if ("=" in target_asset and "ZAR" not in target_asset) else 1
                pts_sl = np.abs(price - stop_loss) * mult
                pts_tp = np.abs(take_profit - price) * mult
                if "ZAR" in target_asset: pts_sl, pts_tp = 800.0, 2000.0
                st.markdown("<p style='font-size:13px; font-weight:bold; letter-spacing:0.5px; color:#90A4AE; text-transform:uppercase;'>📲 NATIVE IG DEAL TICKET LIMITS:</p>", unsafe_allow_html=True)
                col_sl, col_tp = st.columns(2)
                with col_sl:
                    st.markdown(f"<div style='border: 1.5px solid #E53935; background-color:#261C1E; padding:12px; border-radius:4px; text-align:center;'><span style='color:#E53935; font-size:11px; font-weight:bold; letter-spacing:0.5px;'>🛑 IG STOP PRICE DISTANCE</span><br><span style='font-size:22px; font-weight:bold; color:#FFFFFF;'>{pts_sl:.1f} <span style='font-size:13px; color:#E53935;'>pts</span></span></div>", unsafe_allow_html=True)
                with col_tp:
                    st.markdown(f"<div style='border: 1.5px solid #4CAF50; background-color:#1B241C; padding:12px; border-radius:4px; text-align:center;'><span style='color:#4CAF50; font-size:11px; font-weight:bold; letter-spacing:0.5px;'>🎯 IG LIMIT PROFIT DISTANCE</span><br><span style='font-size:22px; font-weight:bold; color:#FFFFFF;'>{pts_tp:.1f} <span style='font-size:13px; color:#4CAF50;'>pts</span></span></div>", unsafe_allow_html=True)
            st.divider()
            st.markdown("<p style='font-size:13px; font-weight:bold; letter-spacing:0.5px; color:#90A4AE;'>🕯️ REAL-TIME DEALING CANDLESTICK GRAPH</p>", unsafe_allow_html=True)
            fig_sig = go.Figure()
            fig_sig.add_trace(go.Candlestick(
                x=hourly_df.tail(48).index, open=hourly_df.tail(48)['Open'], high=hourly_df.tail(48)['High'],
                low=hourly_df.tail(48)['Low'], close=hourly_df.tail(48)['Close'], name="Market",
                increasing_line_color='#4CAF50', decreasing_line_color='#E53935',
                increasing_fillcolor='#4CAF50', decreasing_fillcolor='#E53935'
            ))
            fig_sig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#161A1E', xaxis_rangeslider_visible=False, height=350, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig_sig, use_container_width=True)

elif page_select == "📡 SPECIALIZED NEWS":
    np_view.render_news_tab(target_asset, ig_display_name)

elif page_select == "🕹️ WORKSPACE JOURNAL":
    jp_view.render_journal_tab(target_asset, ig_display_name, price)
