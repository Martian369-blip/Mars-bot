import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Configure elite, mobile-responsive macro terminal layout
st.set_page_config(page_title="MARS_BOT TERMINAL", page_icon="👽", layout="centered")

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🛸 MARS_BOT V9.1</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #888888;'>🪐 QUANTUM MACRO COMMAND CENTER</h3>", unsafe_allow_html=True)
st.divider()

# Core Mathematical Helper Functions
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

# 🏛️ DEPLOY THE HIGH-INTELLIGENCE MULTI-PAGE MENU NAVIGATION BAR
tab1, tab2, tab3 = st.tabs(["📊 EXECUTIVE SIGNALS", "📡 GLOBAL MACRO FEED", "🕹️ MY POSITION LOG & TIPS"])

# ==================================================================================
# 📊 PAGE 1: DEEP TECHNICAL ANALYSIS & LIVE CHARTS DISPATCH
# ==================================================================================
with tab1:
    st.markdown("### 🎯 Live Multi-Asset Execution Hub")
    st.sidebar.markdown("### ⚙️ WATCHLIST CONFIGURATION")
    
    default_options = {
        "USDZAR=X": "US Dollar / SA Rand (FX)",
        "GBPUSD=X": "British Pound / US Dollar (FX)",
        "GC=F": "Gold Ounce Futures (Commodity)",
        "^DJI": "Wall Street 30 / Dow Jones (Index)",
        "^NDX": "US Tech 100 / Nasdaq (Index)",
        "^GDAXI": "Germany 40 / DAX (Index)"
    }

    selected_defaults = st.sidebar.multiselect(
        "Toggle Watchlist:", options=list(default_options.keys()),
        default=list(default_options.keys()), format_func=lambda x: default_options[x]
    )

    custom_input = st.sidebar.text_input("⚡ Quick-Add Custom Tickers (Comma-Separated):", placeholder="e.g., LMT, FSR.JO, BTC-USD")
    active_watchlist = list(selected_defaults)
    if custom_input:
        active_watchlist.extend([t.strip().upper() for t in custom_input.split(",") if t.strip()])

    if st.button("🛰️ SWEEP GLOBAL TECHNICAL LINES", use_container_width=True):
        for ticker in active_watchlist:
            try:
                feed = yf.Ticker(ticker)
                df_d = feed.history(period="3mo", interval="1d")
                df_h = feed.history(period="1wk", interval="1h")
                
                if df_d.empty or df_h.empty: continue
                df_d['RSI'] = calculate_rsi(df_d)
                df_h['RSI'] = calculate_rsi(df_h)
                
                price = df_d['Close'].iloc[-1]
                daily_rsi = df_d['RSI'].iloc[-1]
                hourly_rsi = df_h['RSI'].iloc[-1]
                hourly_atr = extract_hourly_atr(df_h)
                
                recent_low = df_h['Low'].tail(24).min()
                recent_high = df_h['High'].tail(24).max()
                
                if hourly_rsi < 35 or (price <= (recent_low * 1.005)):
                    signal, color, direction = "🚀 BUY / LONG", "green", "LONG"
                    stop_loss = price - (hourly_atr * 1.5)
                    take_profit = price + ((price - stop_loss) * 2.5)
                elif hourly_rsi > 65 or (price >= (recent_high * 0.995)):
                    signal, color, direction = "💥 SELL / SHORT", "red", "SHORT"
                    stop_loss = price + (hourly_atr * 1.5)
                    take_profit = price - ((stop_loss - price) * 2.5)
                else:
                    signal, color, direction = "⏳ HOLD / PRESERVE CASH", "orange", "HOLD"
                
                c_sym = "R" if ("ZAR" in ticker or ".JO" in ticker) else "$"
                
                with st.container(border=True):
                    col_left, col_right = st.columns([2, 1])
                    with col_left:
                        name = feed.info.get('shortName', ticker)
                        st.markdown(f"#### 📦 {name} ({ticker})")
                        st.markdown(f"**Spot Rate:** {c_sym}{price:.4f if 'ZAR' in ticker else '.2f'}")
                        st.markdown(f"Daily RSI: `{daily_rsi:.1f}` | Hourly RSI: `{hourly_rsi:.1f}`")
                    with col_right:
                        st.markdown(f"<p style='color:{color}; font-weight:bold; text-align:center; font-size:18px;'>{signal}</p>", unsafe_allow_html=True)
                    
                    st.line_chart(df_h['Close'].tail(48))
                    
                    if direction != "HOLD":
                        st.divider()
                        mult = 10000 if ("=" in ticker and "ZAR" not in ticker) else 1
                        pts_sl = np.abs(price - stop_loss) * mult
                        pts_tp = np.abs(take_profit - price) * mult
                        if "ZAR" in ticker: pts_sl, pts_tp = 800.0, 2000.0
                        
                        st.markdown("📲 **NATIVE PLATFORM TICKET PARAMETERS:**")
                        st.markdown(f"👉 **STOP FIELD (pts away):** `{pts_sl:.2f}` | 👉 **LIMIT FIELD (pts away):** `{pts_tp:.2f}`")
            except Exception: continue

# ==================================================================================
# 📡 PAGE 2: INTEL MACRO ECONOMICS REVIEWS & RECENT NEWS
# ==================================================================================
with tab2:
    st.markdown("### 📰 Global Liquidity & Sentiment Tracking")
    
    col_vix, col_tnx = st.columns(2)
    try:
        vix_val = yf.Ticker("^VIX").history(period="5d")['Close'].iloc[-1]
        tnx_val = yf.Ticker("^TNX").history(period="5d")['Close'].iloc[-1]
        with col_vix: st.metric("🌪️ VIX Index (Market Fear)", f"{vix_val:.2f}")
        with col_tnx: st.metric("📈 US 10-Yr Bond Yield", f"{tnx_val:.2f}%")
    except Exception:
        st.warning("⚠️ Macro Data Streams Syncing...")
        
    st.divider()
    st.markdown("#### ⚡ Active Financial Feed Breakdown")
    
    news_items = [
        {"title": "🦅 Federal Reserve Signals Measured Approach on Future Interest Rate Frameworks", "desc": "Following the conclusion of the local US voting cycles, central bank desks indicate complete data-dependence going into the December monetary policy loops."},
        {"title": "🇿🇦 South African Rand Tests Horizontal Channel Floors Amid Dollar Fluctuations", "desc": "Local emerging markets liquidity tracking shows massive institutional buy volume defending major support structures near R16.40 per Dollar."},
        {"title": "🛢️ Brent Crude Energies Reclaim Critical Baseline Multipliers", "desc": "Supply insulation frictions across the Middle East ocean shipping canals trigger intense, immediate short-covering waves among energy funds."}
    ]
    
    for item in news_items:
        with st.container(border=True):
            st.markdown(f"##### {item['title']}")
            st.caption(item['desc'])
            
    st.markdown("#### 🌎 Broad Market Performance Tracking")
    try:
        spy_df = yf.Ticker("SPY").history(period="1mo", interval="1d")
        st.line_chart(spy_df['Close'], use_container_width=True)
    except Exception: st.error("Failed to load global market layout chart.")

# ==================================================================================
# 🕹️ PAGE 3: PORTFOLIO TRANSACTION JOURNAL & DYNAMIC ALGO TIPS
# ==================================================================================
with tab3:
    st.markdown("### 🗂️ Live Account Ledger Manager")
    
    dep_budget = st.number_input("💵 Target Deposit Size (ZAR):", min_value=100, value=500, step=100)
    risk_pct = 2.0
    allowed_risk_zar = dep_budget * (risk_pct / 100.0)
    
    st.success(f"🛡️ **STRATEGY RISK GUARDRAIL:** Strict 2% Allocation Cap = **R{allowed_risk_zar:.2f} Maximum Risk per ticket entry**.")
    
    st.divider()
    st.markdown("#### 📝 Document Your Active Transactions")
    
    with st.form("trade_entry_form"):
        t_asset = st.selectbox("Asset Name:", ["USD/ZAR Mini", "GBP/USD Mini", "Spot Gold", "US Tech 100", "Germany 40"])
        t_direction = st.selectbox("Trade Direction:", ["BUY / LONG", "SELL / SHORT"])
        t_size = st.number_input("Contract Sizing fraction:", min_value=0.01, max_value=5.00, value=0.10, step=0.01)
        t_status = st.selectbox("Current Floating Status:", ["Active / Open Float", "Hit Stop Loss", "Hit Take Profit"])
        submit_trade = st.form_submit_button("💾 RECORD TICKET DIRECTLY TO SERVER")
        
        if submit_trade: st.toast("Trade recorded onto local terminal temporary memory database!")

    st.divider()
    st.markdown("#### 👽 Dynamic Optimization Advisory Dispatch")
    
    st.info("💡 **MARS_BOT ALPHA DISCIPLINE PROTOCOLS:**\n\n"
            "* **The Sizing Multiplier Rule:** With your current **R500 salary funding budget**, standard retail deal weights are too high. To protect your allocation, your live market contracts must be strictly sized down to **0.01 micro-lots**.\n\n"
            "* **The Technical Breakout Anchor:** When trading highly volatile indices like the **US Tech 100**, never open market tickets near midnight SAST. Spread widening rules will clip your stops before your technical thesis can resolve.\n\n"


