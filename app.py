import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import os

# Custom layout and calculation safety fallbacks if internal modules are missing
class EngineFallback:
    @staticmethod
    def calculate_rsi(df, window=14):
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / (loss + 1e-9)
        return 100 - (100 / (1 + rs))

try:
    import engine as eng
except ImportError:
    eng = EngineFallback

try:
    import layout_config as lc
    has_layout_style = True
except ImportError:
    has_layout_style = False

try:
    import chart_render as cr
    has_chart_engine = True
except ImportError:
    has_chart_engine = False

# Initialize premium terminal view window layout
st.set_page_config(page_title="MARS_BOT V16.0", page_icon="👽", layout="centered", initial_sidebar_state="collapsed")

if has_layout_style:
    try: lc.load_ig_style()
    except Exception: pass

PERSISTENT_FILE = "ledger_vault.csv"

def load_persistent_ledger():
    if os.path.exists(PERSISTENT_FILE):
        try:
            df = pd.read_csv(PERSISTENT_FILE)
            if not df.empty: return df
        except Exception: pass
    return pd.DataFrame(columns=["Timestamp", "Asset", "Action", "Price", "Matrix RSI", "Status"])

def save_persistent_ledger(df):
    df.to_csv(PERSISTENT_FILE, index=False)

# Robust Session Matrix Memory Initializations
if "journal_db" not in st.session_state: st.session_state["journal_db"] = load_persistent_ledger()
if "cached_target_asset" not in st.session_state: st.session_state["cached_target_asset"] = ""
if "cached_display_name" not in st.session_state: st.session_state["cached_display_name"] = ""
if "price" not in st.session_state: st.session_state["price"] = 0.0
if "direction" not in st.session_state: st.session_state["direction"] = "⏳ INITIALIZING SYSTEM"
if "color" not in st.session_state: st.session_state["color"] = "#757575"
if "m15_rsi" not in st.session_state: st.session_state["m15_rsi"] = 50.0
if "h1_rsi" not in st.session_state: st.session_state["h1_rsi"] = 50.0
if "h4_rsi" not in st.session_state: st.session_state["h4_rsi"] = 50.0

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
        msg = f"🚨 MACRO CRITICAL ALERT: {active_threat.upper()} TARGET IN {time_str}! EXPECT FLUID LIQUIDATION SHOCKS!"
        st.markdown(f"<div style='background-color:#7F0000; border:2px solid #FF3D00; padding:12px; border-radius:4px; text-align:center; margin-bottom:15px;'><span style='color:#FFFFFF; font-family:monospace; font-weight:bold; font-size:11px;'>{msg}</span></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='background-color:#120A26; border:1px solid #1F1140; padding:8px; border-radius:4px; text-align:center; margin-bottom:15px; font-size:10px; font-family:monospace; color:#4CAF50;'>🛰️ SATELLITE MACRO RADAR: GLOBAL GEOPOLITICAL FLOW MATRIX CLEAR. NO IMMEDIATE VOLATILITY BLOCKS ENCOUNTERED.</div>", unsafe_allow_html=True)

process_macro_volatility_gauge()

st.markdown("<h2 style='text-align: center; color: #FFFFFF !important; margin-bottom: 25px; font-weight: 900;'>🛸 MARS_BOT <span style='color:#4CAF50;'>V16.0</span></h2>", unsafe_allow_html=True)

ig_name_map = {
    "USDZAR=X": "USD/ZAR (US Dollar)",
    "EURZAR=X": "EUR/ZAR (Euro)",
    "GBPZAR=X": "GBP/ZAR (British Pound)",
    "AUDZAR=X": "AUD/ZAR (Aussie Dollar)",
    "JPYZAR=X": "JPY/ZAR (Japanese Yen)",
    "CADZAR=X": "CAD/ZAR (Canadian Dollar)",
    "CHFZAR=X": "CHF/ZAR (Swiss Franc)",
    "NZDZAR=X": "NZD/ZAR (Kiwi Dollar)",
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
    "AAPL":     "Apple Inc. (NASDAQ)",
    "NVDA":     "NVIDIA Corporation (NASDAQ)",
    "TSLA":     "Tesla Motors Inc. (NASDAQ)",
    "MSFT":     "Microsoft Corp. (NASDAQ)",
    "AMZN":     "Amazon.com Inc. (NASDAQ)",
    "META":     "Meta Platforms (NASDAQ)",
    "GOOGL":    "Alphabet Inc. (NASDAQ)",
    "AMD":      "Advanced Micro Devices (NASDAQ)",
    "NFLX":     "Netflix Inc. (NASDAQ)",
    "BTC-USD":  "Bitcoin / US Dollar",
    "ETH-USD":  "Ethereum / US Dollar",
    "SOL-USD":  "Solana / US Dollar",
    "BNB-USD":  "Binance Coin / US Dollar",
    "XRP-USD":  "Ripple / US Dollar",
    "^GSPC":    "S&P 500 Index (US Market)",
    "^NDX":     "NASDAQ 100 (US Tech)",
    "^DJI":     "Dow Jones Industrial 30",
    "^FTSE":    "FTSE 100 Index (London)",
    "^GDAXI":   "DAX Performance Index (Germany)",
    "^N225":    "Nikkei 225 Index (Japan)",
    "^J203.JO": "JSE All Share Index (South Africa)"
}

display_options = list(ig_name_map.values())

col_search, col_trigger = st.columns([0.75, 0.25])
with col_search:
    chosen_display = st.selectbox("🔍 MARKET:", options=display_options, label_visibility="collapsed")
reverse_map = {v: k for k, v in ig_name_map.items()}
selected_ticker = reverse_map.get(chosen_display, "USDZAR=X")
with col_trigger:
    search_activated = st.button("🛰️ SCAN")

# AUTO-SCAN DEPLOYMENT: Automatically pulls live analytics immediately on initial page mount
if search_activated or st.session_state["cached_target_asset"] == "":
    st.session_state["cached_target_asset"] = selected_ticker
    st.session_state["cached_display_name"] = chosen_display
    try:
        with st.spinner("Fetching Live Market Telemetry Vectors..."):
            ticker_feed = yf.Ticker(st.session_state["cached_target_asset"])
            df_15m = ticker_feed.history(period="5d", interval="15m")
            df_1h = ticker_feed.history(period="30d", interval="1h")
            df_4h = ticker_feed.history(period="60d", interval="4h")
            
            if not df_1h.empty:
                st.session_state["price"] = float(df_1h['Close'].iloc[-1])
                st.session_state["m15_rsi"] = float(eng.calculate_rsi(df_15m).iloc[-1]) if not df_15m.empty else 50.0
                st.session_state["h1_rsi"] = float(eng.calculate_rsi(df_1h).iloc[-1])
                st.session_state["h4_rsi"] = float(eng.calculate_rsi(df_4h).iloc[-1]) if not df_4h.empty else 50.0
                
                if st.session_state["m15_rsi"] < 40 and st.session_state["h1_rsi"] < 45 and st.session_state["h4_rsi"] < 50:
                    st.session_state["direction"], st.session_state["color"] = "🚀 CONVERGENT BUY", "#4CAF50"
                elif st.session_state["m15_rsi"] > 60 and st.session_state["h1_rsi"] > 55 and st.session_state["h4_rsi"] > 50:
                    st.session_state["direction"], st.session_state["color"] = "💥 CONVERGENT SELL", "#E53935"
                else:
                    st.session_state["direction"], st.session_state["color"] = "⏳ HOLD / STANDBY", "#757575"
    except Exception as e:
        st.sidebar.error(f"Feed Error: {str(e)}")

st.sidebar.markdown("<h3 style='color:#4CAF50 !important; font-weight:900;'>☰ MAIN CORE</h3>", unsafe_allow_html=True)

navigation_sheets = ["📊  TERMINAL SIGNALS", "📡  SATELLITE NEWS", "🕹️  LEDGER JOURNAL"]
page_select = st.sidebar.radio("CHOOSE MODULE SHEET:", options=navigation_sheets)
current_active_index = navigation_sheets.index(page_select)

if current_active_index == 0:
    st.markdown(f"#### 📡 Telemetry Feed Workspace: <span style='color:#4CAF50;'>{st.session_state['cached_display_name']}</span>", unsafe_allow_html=True)
    
    is_zar_denominated = "ZAR" in st.session_state['cached_target_asset'] or ".JO" in st.session_state['cached_target_asset']
    currency_prefix = "R " if is_zar_denominated else "$ "
    
    spot_str = f"{currency_prefix}{st.session_state['price']:.4f}"
