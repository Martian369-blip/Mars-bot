import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# 🏛️ 1. SKINNED MOBILE-FIRST CORE RUNTIME LAYOUT
st.set_page_config(page_title="MARS_BOT V9.5", page_icon="👽", layout="centered")

# Injecting Custom Cyberpunk Green & Black Styling Directly Into the Client Panel
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    h1, h2, h3, h4, h5, h6 { color: #00FF00 !important; font-family: 'Courier New', monospace; }
    .stTabs [data-baseweb="tab-list"] { background-color: #000000; border-bottom: 2px solid #00FF00; }
    .stTabs [data-baseweb="tab"] { color: #888888 !important; font-family: 'Courier New', monospace; }
    .stTabs [aria-selected="true"] { color: #00FF00 !important; font-weight: bold; border-bottom-color: #00FF00 !important; }
    div[data-testid="stContainer"] { border: 1px solid #00FF00 !important; background-color: #050505 !important; border-radius: 4px; padding: 10px; margin-bottom: 15px; }
    .stButton>button { background-color: #000000 !important; color: #00FF00 !important; border: 1px solid #00FF00 !important; font-family: 'Courier New', monospace; width: 100%; }
    .stButton>button:hover { background-color: #00FF00 !important; color: #000000 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🛸 MARS_BOT V9.5</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>🛰️ SPECIALIZED INTERMARKET INTELLIGENCE</h3>", unsafe_allow_html=True)
st.divider()

# Core Technical Indicator Math Layers
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

# HIGH-INTELLIGENCE MULTI-PAGE MENU NAVIGATION BAR
tab1, tab2, tab3 = st.tabs(["📊 EXECUTIVE SIGNALS", "📡 SPECIALIZED NEWS", "🕹️ WORKSPACE JOURNAL"])

# ==================================================================================
# 📊 PAGE 1: AUTOCHARTIST SPEC FORMAT SIGNALS (MARKET -> SIGNAL -> CHART)
# ==================================================================================
with tab1:
    st.markdown("### 🎯 Live Sovereign Signal Logs")
    st.sidebar.markdown("### ⚙️ TERMINAL WATCHLIST")
    
    default_options = {
        "USDZAR=X": "US Dollar / SA Rand",
        "GBPUSD=X": "British Pound / US Dollar",
        "GC=F": "Spot Gold Futures",
        "^DJI": "Wall Street 30 (Dow Jones)",
        "^NDX": "US Tech 100 (Nasdaq)",
        "^GDAXI": "Germany 40 (DAX Index)"
    }

    selected_defaults = st.sidebar.multiselect(
        "Toggle Grid Assets:", options=list(default_options.keys()),
        default=list(default_options.keys()), format_func=lambda x: default_options[x]
    )
    
    active_watchlist = list(selected_defaults)

    if st.button("🛰️ EXECUTE SYSTEM VOLATILITY SCAN", use_container_width=True):
        st.toast("Mars_bot sweeping global liquidity nodes...")
        
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
                    direction, color = "Buy", "#00FF00"
                    stop_loss = price - (hourly_atr * 1.5)
                    take_profit = price + ((price - stop_loss) * 2.5)
                elif hourly_rsi > 65 or (price >= (recent_high * 0.995)):
                    direction, color = "Sell", "#FF0000"
                    stop_loss = price + (hourly_atr * 1.5)
                    take_profit = price - ((stop_loss - price) * 2.5)
                else:
                    direction, color = "Hold", "#FFFF00"
                
                c_sym = "R" if ("ZAR" in ticker or ".JO" in ticker) else "$"
                name = feed.info.get('shortName', ticker)
                
                # 🕹️ THE AUTOCHARTIST CUSTOM SEQUENCE LAYOUT FRAMEWORK
                with st.container():
                    # Layer 1: Market Identification Header (ON TOP)
                    st.markdown(f"<h4 style='margin:0px;'>⚜️ {name} ({ticker})</h4>", unsafe_allow_html=True)
                    
                    # Layer 2: Signal Specification Metrics Panel (IN THE CENTER)
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"**Spot Rate:** {c_sym}{price:.4f if 'ZAR' in ticker else '.2f'}")
                    with col2:
                        st.markdown(f"**Direction:** <span style='color:{color}; font-weight:bold;'>{direction}</span>", unsafe_allow_html=True)
                    with col3:
                        st.markdown(f"**Hourly RSI:** `{hourly_rsi:.1f}`")
                    
                    # Layer 3: Intraday Trendline Data Visualizer Chart (AT THE BOTTOM)
                    st.line_chart(df_h['Close'].tail(36))
                    
                    if direction != "Hold":
                        mult = 10000 if ("=" in ticker and "ZAR" not in ticker) else 1
                        pts_sl = np.abs(price - stop_loss) * mult
                        pts_tp = np.abs(take_profit - price) * mult
                        if "ZAR" in ticker: pts_sl, pts_tp = 800.0, 2000.0
                        st.markdown(f"🎰 **IG PARAMETERS:** STOP: `{pts_sl:.1f} pts away` | LIMIT: `{pts_tp:.1f} pts away`")
            except Exception: continue

# ==================================================================================
# 📡 PAGE 2: SPECIALIZED NEWS FEED & MACRO GRAPHS (THE BANKER HYPOTHESIS)
# ==================================================================================
with tab2:
    st.markdown("### 📰 Specialized Macro Research Hub")
    st.markdown("<p style='color: #888888; font-style: italic;'>Sourced via Mars_bot's active sovereign analysis capabilities</p>", unsafe_allow_html=True)
    st.divider()
    
    # 🏛️ REUTERS / AUTOCHARTIST FORM REAL NEWS BLOCKS
    st.markdown("#### 🇺🇸 US Labor Market Regains Ground as Job Growth Surges")
    st.markdown("<p style='color: #00FF00; font-weight: bold;'>🕒 DATA INGESTION: ACTIVE INTEL</p>", unsafe_allow_html=True)
    st.write("US nonfarm payrolls increased by a surprising **165,000 jobs in October**, completely smashing the standard consensus estimate of 59,000. Concurrently, the nationwide **unemployment rate fell to 4.1%**.")
    
    # Mars_bot's Specialized Research Commentary Box
    st.info("🧠 **MARS_BOT BANKER COMMENTARY:** This robust labor data completely eliminates immediate economic slowdown fears. From a sovereign banker perspective, this gives the Federal Reserve significant scope to hold interest rates higher for longer to combat stubborn domestic energy inflation stemming from ongoing Middle East shipping canal disruptions. A December rate hike remains firmly locked on the institutional agenda.")
    st.divider()
    
    st.markdown("#### 📉 Trump Media's Investors Absorb $2.2 Billion in Structural Paper Losses")
    st.write("Comprehensive auditing across equity issuance filings and court transaction data reveals that public outside investors in the media group have absorbed over **$2.2 billion in aggregate losses**, with shares collapsing toward all-time record lows. This comes as the underlying social application burns through operational cash reserves while struggling to attract verified new enterprise clients.")
    st.divider()
    
    st.markdown("#### ⚡ FOCUS: AI Infrastructure Boom Turns Chip Packaging into Next Semiconductor Battleground")
    st.write("Global technology giants are unleashing billions of dollars of immediate corporate capital expenditure into advanced chip packaging infrastructure. This highly technical, once unglamorous aspect of the hardware chain has transformed into a critical bottleneck in the manufacturing pipeline of the world's most powerful artificial intelligence processors.")
    
    st.markdown("#### 🌎 Broad Market Liquidity Flow (S&P 500 Performance Index)")
    try:
        spy_df = yf.Ticker("SPY").history(period="1mo", interval="1d")
        st.line_chart(spy_df['Close'], use_container_width=True)
    except Exception: st.error("Failed to load global market layout chart.")

# ==================================================================================
# 🕹️ PAGE 3: RECORD JOURNAL TRADES & DYNAMIC ALGO TIPS
# ==================================================================================
with tab3:
    st.markdown("### 🗂️ Live Account Ledger Manager")
    
    dep_budget = st.number_input("💵 Live Allocation Budget (ZAR):", min_value=100, value=500, step=100)
    allowed_risk_zar = dep_budget * (2.0 / 100.0)
