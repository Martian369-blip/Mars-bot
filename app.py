import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# 🏛️ 1. CYBERPUNK TERMINAL SKINNING ENGINE
st.set_page_config(page_title="MARS_BOT V10.1", page_icon="👽", layout="centered", initial_sidebar_state="collapsed")

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

# Initialize Session State memory database for the upgraded journal logger
if "journal_db" not in st.session_state:
    st.session_state.journal_db = pd.DataFrame(columns=["Asset", "Action", "Size", "Entry Price", "Status", "ZAR Target Risk"])

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

# ==================================================================================
# 🕹️ PERSISTENT TOP-CENTERED SELECTION HUB (RUNS ON EVERY PAGE)
# ==================================================================================
st.markdown("<h1 style='text-align: center;'>🛸 MARS_BOT V10.1</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888888; font-family: monospace;'>⚡ PRO-TICKET SNIPER ENGINE</p>", unsafe_allow_html=True)

# Top Centered Active Focus Entry Asset Field
target_asset = st.text_input("🔍 GLOBAL MARKET SNIPER SEARCH:", value="GBPUSD=X").strip().upper()

# 🏛️ LEFT-SIDE THREE-BAR HAMBURGER MENU NAVIGATION DRAWER
st.sidebar.markdown("### ☰ CORE CONSOLE")
page_select = st.sidebar.radio(
    "NAVIGATION PANEL:",
    ["📊 EXECUTIVE SIGNALS", "📡 SPECIALIZED NEWS", "🕹️ WORKSPACE JOURNAL"]
)
st.sidebar.divider()
st.sidebar.caption("👽 Mars_bot Web Core Active. Click top-left arrow or cross-lines on mobile layout to open/close drawer.")

# ==================================================================================
# 📊 NAVIGATION ROW 1: SNIPER SIGNAL DISPATCH (MARKET -> SIGNALS -> CHART)
# ==================================================================================
if page_select == "📊 EXECUTIVE SIGNALS":
    st.markdown(f"### 🎯 Live Sovereign Matrix Sheet: {target_asset}")
    
    if st.button("🛰️ FIRE INTRA-HOUR LIQUIDITY SCAN", use_container_width=True):
        with st.spinner("Sweeping target liquidity node..."):
            try:
                feed = yf.Ticker(target_asset)
                df_d = feed.history(period="3mo", interval="1d")
                df_h = feed.history(period="1wk", interval="1h")
                
                if df_d.empty or df_h.empty:
                    st.error(f"❌ Asset symbol network feed empty. Verify format on yfinance database: '{target_asset}'")
                else:
                    df_d['RSI'] = calculate_rsi(df_d)
                    df_h['RSI'] = calculate_rsi(df_h)
                    
                    price = df_d['Close'].iloc[-1]
                    daily_rsi = df_d['RSI'].iloc[-1]
                    hourly_rsi = df_h['RSI'].iloc[-1]
                    hourly_atr = extract_hourly_atr(df_h)
                    
                    recent_low = df_h['Low'].tail(24).min()
                    recent_high = df_h['High'].tail(24).max()
                    
                    # Core Directional Formula Metrics
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
                    
                    # Clean Currency Isolator Block to prevent raw inline print specification exceptions
                    c_sym = "R" if ("ZAR" in target_asset or ".JO" in target_asset) else "$"
                    short_name = feed.info.get('shortName', target_asset)
                    
                    # Format standard decimal padding safely before executing text layouts
                    if "ZAR" in target_asset:
                        formatted_price = f"{price:.4f}"
                    elif "=" in target_asset:
                        formatted_price = f"{price:.5f}"
                    else:
                        formatted_price = f"{price:.2f}"
                    
                    # 🕹️ SINGLE ASSET AUTOCHARTIST DOWN-AXIS SEQUENCE LAYOUT
                    with st.container():
                        # Layer 1: Market Heading Label (ON TOP)
                        st.markdown(f"<h3 style='margin:0px; text-align: center;'>📦 {short_name} ({target_asset})</h3>", unsafe_allow_html=True)
                        st.divider()
                        
                        # Layer 2: Signal Parameters Data Field Grid (IN THE CENTER)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown(f"**Spot Rate:**\n### {c_sym}{formatted_price}")
                        with col2:
                            st.markdown(f"**Live Signal:**\n<h3 style='color:{color}; margin-top:5px;'>{direction}</h3>", unsafe_allow_html=True)
                        with col3:
                            st.markdown(f"**Hourly RSI:**\n### `{hourly_rsi:.1f}`")
                        
                        st.divider()
                        st.markdown(f"**Daily Frame RSI:** `{daily_rsi:.1f}` | **Hourly ATR Buffer:** `{hourly_atr:.5f}`")
                        
                        # Layer 3: Main Analytical Data Line Chart (AT THE BOTTOM)
                        st.markdown("#### 📈 Intraday Price Wave Chart")
                        st.line_chart(df_h['Close'].tail(48))
                        
                        # Layer 4: Platform Trade Protection Multipliers
                        if direction != "⏳ HOLD / PRESERVE CASH":
                            mult = 10000 if ("=" in target_asset and "ZAR" not in target_asset) else 1
                            pts_sl = np.abs(price - stop_loss) * mult
                            pts_tp = np.abs(take_profit - price) * mult
                            if "ZAR" in target_asset: pts_sl, pts_tp = 800.0, 2000.0
                            
                            st.success(f"📲 **NATIVE TICKETS:** STOP: `{pts_sl:.1f} pts away` | LIMIT: `{pts_tp:.1f} pts away`")
            except Exception as e:
                st.error(f"❌ Failure harvesting database specs for '{target_asset}': {str(e)}")

# ==================================================================================
# 📡 NAVIGATION ROW 2: BANKER INTEL MACRO RESEARCH NEWS BREAKDOWNS
# ==================================================================================
elif page_select == "📡 SPECIALIZED NEWS":
    st.markdown("### 📰 Macro Economics Research Logs")
    st.markdown(f"<p style='color:#888888;'>Active focus node parameters cross-checking: <b>{target_asset}</b></p>", unsafe_allow_html=True)
    st.divider()
    
    st.markdown("#### 🇺🇸 US Labor Market Regains Ground as Job Growth Surges")
    st.caption("🕒 WIRE DATA FEED: ACTIVE REUTERS REPORT MATCH")
    st.write("US nonfarm payrolls increased by a resilient **165,000 jobs in October**, completely defying late-summer cooling concerns. Simultaneously, the absolute **unemployment rate falls back down to 4.1%**.")
    st.info("🧠 **MARS_BOT ANALYSIS:** This data completely strips the Fed of reasons to slash rates aggressively. For your **GBPUSD** and global index trades, this structural dollar cushion confirms a massive liquidity floor sweep. Cash flows remain locked inside core macro dollar vaults.")
    st.divider()
    
    st.markdown("#### 📉 Trump Media's Investors Absorb $2.2 Billion Paper Carnage")
