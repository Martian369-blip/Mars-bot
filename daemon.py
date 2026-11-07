import os
import datetime
import requests
import yfinance as yf
import pandas as pd

# 🔑 CRITICAL CORE CONFIGURATIONS
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
PERSISTENT_FILE = "ledger_vault.csv"

MARKET_MAP = {
    "USDZAR=X": "USD/ZAR", "GBPUSD=X": "GBP/USD", "GC=F": "Gold", "EURUSD=X": "EUR/USD", 
    "USDJPY=X": "USD/JPY", "AUDUSD=X": "AUD/USD", "USDCAD=X": "USD/CAD"
}

def calculate_rsi(df, period=14):
    if len(df) < period:
        return pd.Series([50.0] * len(df))
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def send_telegram_broadcast(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Missing Telegram Credentials Secret Environment Vectors.")
        return
    url = f"https://telegram.org{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Telegram Broadcast Error: {e}")

print(f"🛰️ Triggering simultaneous 7-market matrix scan at {datetime.datetime.now()}...")

for ticker, display_name in MARKET_MAP.items():
    try:
        feed = yf.Ticker(ticker)
        df_15m = feed.history(period="5d", interval="15m")
        df_1h = feed.history(period="30d", interval="1h")
        df_4h = feed.history(period="60d", interval="4h")
        
        if not df_1h.empty:
            current_price = df_1h['Close'].iloc[-1]
            rsi_15m = calculate_rsi(df_15m).iloc[-1] if not df_15m.empty else 50.0
            rsi_1h = calculate_rsi(df_1h).iloc[-1]
            rsi_4h = calculate_rsi(df_4h).iloc[-1] if not df_4h.empty else 50.0
            
            # Convergent BUY Signals Check
            if rsi_15m < 40 and rsi_1h < 45 and rsi_4h < 50:
                msg = f"🚀 *MARS_BOT CONVERGENT BUY SIGNAL*\n\n📈 *Asset:* {display_name}\n💵 *Price:* {current_price:.4f}\n🧭 *H1 RSI:* {rsi_1h:.1f}\n🛰️ *Status:* Telemetry confirms liquidity exhaustion. Standby for vector acceleration."
                send_telegram_broadcast(msg)
                
            # Convergent SELL Signals Check
            elif rsi_15m > 60 and rsi_1h > 55 and rsi_4h > 50:
                msg = f"💥 *MARS_BOT CONVERGENT SELL SIGNAL*\n\n📈 *Asset:* {display_name}\n💵 *Price:* {current_price:.4f}\n🧭 *H1 RSI:* {rsi_1h:.1f}\n🛰️ *Status:* Matrix overbought saturation detected. Fluid liquidation threat active."
                send_telegram_broadcast(msg)
                
    except Exception as e:
        print(f"Error scanning market {display_name}: {e}")

print("🛰️ Simultaneous matrix analysis calculation completed.")
