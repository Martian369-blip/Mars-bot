import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# Configure streamlined mobile-first layout
st.set_page_config(page_title="MARS_BOT", page_icon="👽", layout="centered")

st.markdown("<h1 style='text-align: center;'>🛸 MARS_BOT V7.7</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>📡 MASTER SOVEREIGN GRID</h3>", unsafe_allow_html=True)
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

# The Comprehensive Watchlist Array
watchlists = {
    "USDZAR=X":  {"name": "US Dollar / SA Rand", "type": "FX_ZAR"},
    "GBPUSD=X":  {"name": "British Pound / US Dollar", "type": "FX"}, 
    "GC=F":      {"name": "Gold Ounce Futures", "type": "COMMODITY"},
    "^DJI":      {"name": "Wall Street 30 (Dow Jones)", "type": "INDEX"},
    "^NDX":      {"name": "US Tech 100 (Nasdaq 100)", "type": "INDEX"},
    "^GDAXI":    {"name": "Germany 40 (DAX Index)", "type": "INDEX"}
}

target_rrr = 2.5

if st.button("🔄 REFRESH LIVE MARKET MATRIX", use_container_width=True):
    st.toast("🛸 Mars_bot sweeping global liquidity nodes...")
    
    for ticker, asset in watchlists.items():
        try:
            feed = yf.Ticker(ticker)
            df_d = feed.history(period="3mo", interval="1d")
            df_h = feed.history(period="1wk", interval="1h")
            
            if df_d.empty or df_h.empty:
                continue
                
            df_d['RSI'] = calculate_rsi(df_d)
            df_h['RSI'] = calculate_rsi(df_h)
            
            price = df_d['Close'].iloc[-1]
            daily_rsi = df_d['RSI'].iloc[-1]
            hourly_rsi = df_h['RSI'].iloc[-1]
            hourly_atr = extract_hourly_atr(df_h)
            
            recent_low = df_h['Low'].tail(24).min()
            recent_high = df_h['High'].tail(24).max()
            
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
                
            c = "R" if "ZAR" in ticker else "$"
            
            with st.container(border=True):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"#### 📦 {asset['name']}")
                    if asset["type"] == "FX_ZAR":
                        st.markdown(f"**Spot Rate:** R{price:.4f}")
                    elif asset["type"] == "FX":
                        st.markdown(f"**Spot Rate:** ${price:.5f}")
                    else:
                        st.markdown(f"**Spot Price:** ${price:.2f}")
                    st.markdown(f"Daily RSI: `{daily_rsi:.1f}` | Hourly RSI: `{hourly_rsi:.1f}`")
                with col2:
                    st.markdown(f"<p style='color:{color}; font-weight:bold; text-align:center;'>{signal}</p>", unsafe_allow_html=True)
                
                if direction != "HOLD":
                    st.divider()
                    if asset["type"] == "FX_ZAR":
                        pts_sl, pts_tp = 800.0, 2000.0
                    else:
                        mult = 10000 if asset["type"] == "FX" else 1
                        pts_sl = np.abs(price - stop_loss) * mult
                        pts_tp = np.abs(take_profit - price) * mult
                        
                    st.markdown("📲 **NATIVE IG TICKET PARAMETERS:**")
                    st.markdown(f"👉 **STOP FIELD (pts away):** `{pts_sl:.2f}`")
                    st.markdown(f"👉 **LIMIT FIELD (pts away):** `{pts_tp:.2f}`")
        except Exception:
            continue
else:
    st.info("👽 Tap the button above to run the multi-asset calculations and print your target point dispatches!")
