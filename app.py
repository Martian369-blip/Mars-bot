
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Configure streamlined mobile-first layout
st.set_page_config(page_title="MARS_BOT GLOBAL", page_icon="👽", layout="centered")

st.markdown("<h1 style='text-align: center;'>🛸 MARS_BOT V8.0</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>🌐 DYNAMIC SOVEREIGN GRID</h3>", unsafe_allow_html=True)
st.divider()

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

# 🏛️ 1. INTERACTIVE ASSET CONTROL PANEL (SIDEBAR FOR MOBILE POPUP)
st.sidebar.header("🕹️ MARS_BOT CONTROL HUB")
st.sidebar.markdown("Use this panel to dynamically alter the matrix watchlist.")

# Pre-loaded high-velocity baseline options
default_options = {
    "USDZAR=X": "US Dollar / SA Rand (FX)",
    "GBPUSD=X": "British Pound / US Dollar (FX)",
    "GC=F": "Gold Ounce Futures (Commodity)",
    "^DJI": "Wall Street 30 / Dow Jones (Index)",
    "^NDX": "US Tech 100 / Nasdaq (Index)",
    "^GDAXI": "Germany 40 / DAX (Index)"
}

selected_defaults = st.sidebar.multiselect(
    "Toggle Baseline Watchlist:",
    options=list(default_options.keys()),
    default=list(default_options.keys()),
    format_func=lambda x: default_options[x]
)

# 🚀 THE MAGIC FIELD: Raw ticker input string for absolute market customization
custom_ticker_input = st.sidebar.text_input(
    "⚡ Add Custom Tickers (Comma-Separated):",
    placeholder="e.g., LMT, FSR.JO, BTC-USD, CL=F"
).strip()

# Compile the dynamic watchlist array in real-time
active_watchlist = list(selected_defaults)
if custom_ticker_input:
    custom_tickers = [t.strip().upper() for t in custom_ticker_input.split(",") if t.strip()]
    for ct in custom_tickers:
        if ct not in active_watchlist:
            active_watchlist.append(ct)

target_rrr = 2.5

# 🏛️ 2. PRODUCTION MULTI-ASSET SCANNING CORE
if st.button("🛰️ SCAN CUSTOM MARKET MATRIX", use_container_width=True):
    if not active_watchlist:
        st.warning("⚠️ Watchlist empty. Please select or input tickers in the sidebar panel.")
    else:
        st.toast("🛸 Mars_bot processing customized liquidity nodes...")
        
        for ticker in active_watchlist:
            try:
                feed = yf.Ticker(ticker)
                df_d = feed.history(period="3mo", interval="1d")
                df_h = feed.history(period="1wk", interval="1h")
                
                if df_d.empty or df_h.empty:
                    st.error(f"❌ Invalid symbol format or empty feed for string: {ticker}")
                    continue
                    
                df_d['RSI'] = calculate_rsi(df_d)
                df_h['RSI'] = calculate_rsi(df_h)
                
                price = df_d['Close'].iloc[-1]
                daily_rsi = df_d['RSI'].iloc[-1]
                hourly_rsi = df_h['RSI'].iloc[-1]
                hourly_atr = extract_hourly_atr(df_h)
                
                recent_low = df_h['Low'].tail(24).min()
                recent_high = df_h['High'].tail(24).max()
                
                # Dynamic Algorithmic Filter Rules
                if hourly_rsi < 35 or (price <= (recent_low * 1.005)):
                    signal = "🚀 EXECUTE BUY (GO LONG)"
                    color = "green"
                    stop_loss = price - (hourly_atr * 1.5)
                    take_profit = price + ((price - stop_loss) * target_rrr)
                    direction = "LONG"
                elif hourly_rsi > 65 or (price >= (recent_high * 0.995)):
                    signal = "💥 EXECUTE SELL SHORT (GO SHORT)"
                    color = "red"
                    stop_loss = price + (hourly_atr * 1.5)
                    take_profit = price - ((stop_loss - price) * target_rrr)
                    direction = "SHORT"
                else:
                    signal = "⏳ HOLD POSITION / PRESERVE CASH"
                    color = "orange"
                    direction = "HOLD"
                    
                # Clean Currency String Separation Layer
                c = "R" if ("ZAR" in ticker or ".JO" in ticker) else "$"
                
                with st.container(border=True):
                    col1, col2 = st.columns()
                    with col1:
                        # Fetch the formal security name automatically from yfinance database metadata
                        asset_info_name = feed.info.get('shortName', ticker)
                        st.markdown(f"#### 📦 {asset_info_name} ({ticker})")
                        
                        if "ZAR" in ticker or ".JO" in ticker:
                            st.markdown(f"**Spot Price:** R{price:.4f if 'ZAR' in ticker else '.2f'}")
                        elif "-" in ticker: # Crypto asset formatting string detection
                            st.markdown(f"**Spot Price:** ${price:.2f}")
                        else:
                            st.markdown(f"**Spot Price:** ${price:.2f}")
                        st.markdown(f"Daily RSI: `{daily_rsi:.1f}` | Hourly RSI: `{hourly_rsi:.1f}`")
                    with col2:
                        st.markdown(f"<p style='color:{color}; font-weight:bold; text-align:center; padding-top:10px;'>{signal}</p>", unsafe_allow_html=True)
                    
                    if direction != "HOLD":
                        st.divider()
                        if "ZAR" in ticker:
                            print("🇿🇦 Enforcing structural 800/2000 point ratio template...")
                            pts_sl, pts_tp = 800.0, 2000.0
                        else:
                            # Auto-adjust multiplier based on asset class string indicators
                            mult = 10000 if ("=" in ticker and "ZAR" not in ticker) else 1
                            pts_sl = np.abs(price - stop_loss) * mult
                            pts_tp = np.abs(take_profit - price) * mult
                            
                        st.markdown("📲 **NATIVE IG TICKET PARAMETERS:**")
                        st.markdown(f"👉 **STOP FIELD (pts away):** `{pts_sl:.2f}`")
                        st.markdown(f"👉 **LIMIT FIELD (pts away):** `{pts_tp:.2f}`")
            except Exception as e:
                st.error(f"❌ Error processing asset string '{ticker}': {str(e)}")
                continue
else:
    st.info("👽 Open the sidebar menu sheet to completely customize your watch list, then tap the button above to run calculations!")
