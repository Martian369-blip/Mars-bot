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

st.set_page_config(page_title="MARS_BOT V14.0", page_icon="👽", layout="centered", initial_sidebar_state="collapsed")
lc.load_ig_style()

if "journal_db" not in st.session_state:
    st.session_state.journal_db = pd.DataFrame(columns=["Asset", "Action", "Cash In (R)", "Cash Out (R)", "Net P&L (ZAR)", "Entry Price", "Win/Loss %", "Status"])
if "live_balance" not in st.session_state:
    st.session_state.live_balance = 500.0

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

st.markdown("<h2 style='text-align: center; color: #00A4E4 !important; margin-bottom: 5px;'>🛸 MARS_BOT V14.0</h2>", unsafe_allow_html=True)

# ==================== THE COMPREHENSIVE GLOBAL MARKET CATALOG ====================
ig_name_map = {
    # 🇿🇦 South African Rand Exotic Vectors (ZAR Crosses)
    "USDZAR=X": "USD/ZAR (US Dollar)",
    "EURZAR=X": "EUR/ZAR (Euro)",
    "GBPZAR=X": "GBP/ZAR (British Pound)",
    "AUDZAR=X": "AUD/ZAR (Aussie Dollar)",
    "JPYZAR=X": "JPY/ZAR (Japanese Yen)",
    "CADZAR=X": "CAD/ZAR (Canadian Dollar)",
    "CHFZAR=X": "CHF/ZAR (Swiss Franc)",
    "NZDZAR=X": "NZD/ZAR (Kiwi Dollar)",
    
    # 🌍 Global Forex Majors & Liquid Crosses
    "GBPUSD=X": "GBP/USD (Cable)",
    "EURUSD=X": "EUR/USD (Fiber)",
    "USDJPY=X": "USD/JPY (Ninja)",
    "AUDUSD=X": "AUD/USD (Aussie)",
    "USDCAD=X": "USD/CAD (Loonie)",
    "USDCHF=X": "USD/CHF (Swissie)",
    "NZDUSD=X": "NZD/USD (Kiwi)",
    "EURGBP=X": "EUR/GBP (Chunnel)",
    "EURJPY=X": "EUR/JPY",
    "GBPJPY=X": "GBP/JPY (Guppy)",
    
    # 🛢️ Global Hard & Soft Commodities Suite
    "GC=F":     "Gold (Ounce Futures)",
    "SI=F":     "Silver (Ounce Futures)",
    "PL=F":     "Platinum (Ounce Futures)",
    "PA=F":     "Palladium (Ounce Futures)",
    "CL=F":     "Crude Oil (WTI Futures)",
    "BZ=F":     "Brent Crude Oil Futures",
    "NG=F":     "Natural Gas Futures",
    "HG=F":     "Copper Futures",
    "CC=F":     "Cocoa Futures",
    "KC=F":     "Coffee Futures",
    
    # 🇿🇦 Johannesburg Stock Exchange (JSE Blue-Chip Heavyweights)
    "SOL.JO":   "Sasol Ltd (JSE:SOL)",
    "FSR.JO":   "FirstRand Ltd (JSE:FSR)",
    "SBK.JO":   "Standard Bank Group (JSE:SBK)",
    "ANG.JO":   "Anglogold Ashanti (JSE:ANG)",
    "IMP.JO":   "Impala Platinum (JSE:IMP)",
    "NPN.JO":   "Naspers Ltd (JSE:NPN)",
    "PRX.JO":   "Prosus NV (JSE:PRX)",
    "BTI.JO":   "British American Tobacco (JSE:BTI)",
    "AGL.JO":   "Anglo American plc (JSE:AGL)",
    "GFI.JO":   "Gold Fields Ltd (JSE:GFI)",
    "SLM.JO":   "Sanlam Ltd (JSE:SLM)",
    "ABG.JO":   "Absa Group Ltd (JSE:ABG)",
    "NED.JO":   "Nedbank Group (JSE:NED)",
    "MTN.JO":   "MTN Group Ltd (JSE:MTN)",
    "VOD.JO":   "Vodacom Group (JSE:VOD)",
    
    # 🇺🇸 Wall Street Blue-Chips & Tech Giants
    "AAPL":     "Apple Inc. (NASDAQ)",
    "NVDA":     "NVIDIA Corporation (NASDAQ)",
    "TSLA":     "Tesla Motors Inc. (NASDAQ)",
    "MSFT":     "Microsoft Corp. (NASDAQ)",
    "AMZN":     "Amazon.com Inc. (NASDAQ)",
    "META":     "Meta Platforms (NASDAQ)",
    "GOOGL":    "Alphabet Inc. (NASDAQ)",
    "AMD":      "Advanced Micro Devices (NASDAQ)",
    "NFLX":     "Netflix Inc. (NASDAQ)",
    
    # 🪙 Decentralized Digital Assets (Crypto Vectors)
    "BTC-USD":  "Bitcoin / US Dollar",
    "ETH-USD":  "Ethereum / US Dollar",
    "SOL-USD":  "Solana / US Dollar",
    "BNB-USD":  "Binance Coin / US Dollar",
    "XRP-USD":  "Ripple / US Dollar",
    
    # 📉 Macro Stock Market Indices
    "^GSPC":    "S&P 500 Index (US Market)",
    "^NDX":     "NASDAQ 100 (US Tech)",
    "^DJI":     "Dow Jones Industrial 30",
    "^FTSE":    "FTSE 100 Index (London)",
    "^GDAXI":   "DAX Performance Index (Germany)",
    "^N225":    "Nikkei 225 Index (Japan)",
    "^J203.JO": "JSE All Share Index (South Africa)"
}
display_options = list(ig_name_map.values())

# 🔥 FIX UPGRADE: Added proportional width ratio lists to resolve the layout crash
col_search, col_trigger = st.columns([3, 1])
with col_search:
    chosen_display = st.selectbox("🔍 SELECT MARKET WORKSPACE:", options=display_options, label_visibility="collapsed")

reverse_map = {v: k for k, v in ig_name_map.items()}
target_asset = reverse_map.get(chosen_display, "GBPUSD=X")
ig_display_name = chosen_display

with col_trigger:
    search_activated = st.button("🛰️ SCAN")

st.sidebar.markdown("<h3 style='color:#00A4E4 !important;'>☰ IG CONSOLE</h3>", unsafe_allow_html=True)
page_select = st.sidebar.radio("NAVIGATION PANEL:", ["📊 EXECUTIVE SIGNALS", "📡 SPECIALIZED NEWS", "🕹️ WORKSPACE JOURNAL"])
st.sidebar.divider()
st.sidebar.caption("👽 V14.0 Quantum Core Multi-Module Mesh.")

price, hourly_rsi, direction, color, stop_loss, take_profit = 0.0, 50.0, "HOLD", "#E53935", 0.0, 0.0
daily_df, hourly_df = pd.DataFrame(), pd.DataFrame()
candle_pattern_alert = "⏳ SCANNING MATRIX..."

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
        hourly_rsi = hourly_df['RSI'].iloc[-1]
        hourly_atr = eng.extract_hourly_atr(hourly_df)
        
        candle_pattern_alert = eng.scan_candlestick_patterns(hourly_df)
        
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
    
    if "ALIGNED" in candle_pattern_alert or "DETECTED" in candle_pattern_alert:
        st.warning(f"⚠️ **{candle_pattern_alert}**")
    else:
        st.info(f"👀 **Structure Matrix Status:** {candle_pattern_alert}")
        
    if daily_df.empty or hourly_df.empty:
        st.error(f"❌ Empty market node feedback.")
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
            st.markdown("<p style='font-size:13px; font-weight:bold; letter-spacing:0.5px; color:#90A4AE;'>🕯️ REAL-TIME DEALING CANDLESTICK GRAPH</p>", unsafe_allow_html=True)
            fig_sig = go.Figure()
            fig_sig.add_trace(go.Candlestick(
                x=hourly_df.tail(48).index, open=hourly_df.tail(48)['Open'], high=hourly_df.tail(48)['High'],
                low=hourly_df.tail(48)['Low'], close=hourly_df.tail(48)['Close'], name="Market",
                increasing_line_color='#4CAF50', decreasing_line_color='#E53935'
            ))
            fig_sig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#161A1E', xaxis_rangeslider_visible=False, height=350, margin=dict(l=10, r=10, t=10, b=10))
            st.plotly_chart(fig_sig, use_container_width=True)

elif page_select == "📡 SPECIALIZED NEWS":
    np_view.render_news_tab(target_asset, ig_display_name)
    try:
        import macro_tracker; macro_tracker.render_macro_schedule_panel()
    except Exception: pass

elif page_select == "🕹️ WORKSPACE JOURNAL":
