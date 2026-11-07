import os
import datetime
import requests
import yfinance as yf
import pandas as pd
import numpy as np

# 🔑 CRITICAL CORE CONFIGURATIONS (Uses the same encrypted secrets matrix)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Parallel Market Grid Matrix
MARKET_MAP = {
    "USDZAR=X": "USD/ZAR", "GBPUSD=X": "GBP/USD", "GC=F": "Gold", "EURUSD=X": "EUR/USD", 
    "USDJPY=X": "USD/JPY", "AUDUSD=X": "AUD/USD", "USDCAD=X": "USD/CAD"
}

def calculate_bollinger_bands(df, window=20, num_std=2):
    rolling_mean = df['Close'].rolling(window=window).mean()
    rolling_std = df['Close'].rolling(window=window).std()
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    return upper_band, rolling_mean, lower_band

def calculate_atr(df, window=14):
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = ranges.max(axis=1)
    return true_range.rolling(window=window).mean()

def send_telegram_broadcast(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Missing Telegram Credentials Secret Environment Vectors.")
        return
    url = f"https://telegram.org{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Vortex Omega Broadcast Error: {e}")

print(f"🌀 Initiating VORTEX_OMEGA Volatility Breakout Scan at {datetime.datetime.now()}...")

for ticker, display_name in MARKET_MAP.items():
    try:
        feed = yf.Ticker(ticker)
        # Focus heavily on the 30M and 2H liquidity bands for structural breakouts
        df_30m = feed.history(period="5d", interval="30m")
        df_2h = feed.history(period="15d", interval="2h")
        
        if not df_30m.empty and len(df_30m) >= 20:
            current_price = df_30m['Close'].iloc[-1]
            
            # Calculate Bollinger Volatility Bands
            upper_30m, _, lower_30m = calculate_bollinger_bands(df_30m)
            atr_30m = calculate_atr(df_30m)
            
            # Structural variables
            last_upper = upper_30m.iloc[-1]
            last_lower = lower_30m.iloc[-1]
            last_atr = atr_30m.iloc[-1]
            
            # Bandwidth metric to identify tight, explosive squeeze consolidations
            bandwidth = (last_upper - last_lower) / current_price
            
            # 🌀 CONDITION ALPHA: Volatility Liquidity Spike BUY (Price pierces below band, velocity expansion)
            if current_price < last_lower and (df_30m['High'].iloc[-1] - df_30m['Low'].iloc[-1]) > (1.5 * last_atr):
                msg = f"🌀 *VORTEX_OMEGA LIQUIDATION TRAP (BUY)*\n\n📈 *Asset:* {display_name}\n💵 *Price:* {current_price:.4f}\n💥 *Breach:* Price pierced lower Bollinger boundary.\n🛰️ *Volatility (ATR):* {last_atr:.4f}\n🧭 *Vector:* Institutional stop-hunt sweep detected. High probability reversal block active."
                send_telegram_broadcast(msg)
                
            # 🌀 CONDITION BETA: Volatility Liquidity Spike SELL (Price forces above band, velocity expansion)
            elif current_price > last_upper and (df_30m['High'].iloc[-1] - df_30m['Low'].iloc[-1]) > (1.5 * last_atr):
                msg = f"🌀 *VORTEX_OMEGA LIQUIDATION TRAP (SELL)*\n\n📈 *Asset:* {display_name}\n💵 *Price:* {current_price:.4f}\n💥 *Breach:* Price pierced upper Bollinger boundary.\n🛰️ *Volatility (ATR):* {last_atr:.4f}\n🧭 *Vector:* Liquidity capture verified above value bands. Standby for downward compression."
                send_telegram_broadcast(msg)
                
            # ⏳ CONDITION GAMMA: Compression Alert (Market gearing up for massive breakout)
            elif bandwidth < 0.0025: 
                print(f"Market Squeeze active for {display_name} (Bandwidth: {bandwidth:.5f}). Gearing for expansion.")

    except Exception as e:
        print(f"Error executing Vortex scan on {display_name}: {e}")

print("🌀 VORTEX_OMEGA execution grid complete.")
