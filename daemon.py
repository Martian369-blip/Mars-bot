import time
import datetime
import os
import requests
import yfinance as yf
import pandas as pd

# 🔑 CRITICAL CORE CONFIGURATIONS (Set these in your hosting dashboard or paste directly)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID_HERE")
PERSISTENT_FILE = "ledger_vault.csv"

# The 7 Global Markets to track simultaneously
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
    url = f"https://telegram.org{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Telegram Daemon Send Error: {e}")

def log_vector_to_ledger(asset, action, price, rsi, status):
    new_row = pd.DataFrame([{
        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Asset": asset,
        "Action": action,
        "Price": price,
        "Matrix RSI": round(float(rsi), 1),
        "Status": status
    }])
    if os.path.exists(PERSISTENT_FILE):
        try:
            df = pd.read_csv(PERSISTENT_FILE)
            df = pd.concat([df, new_row], axis=0, ignore_index=True)
            df.to_csv(PERSISTENT_FILE, index=False)
        except Exception:
            new_row.to_csv(PERSISTENT_FILE, index=False)
    else:
        new_row.to_csv(PERSISTENT_FILE, index=False)

print("🛸 MARS_BOT BACKGROUND DAEMON ONLINE & STREAMING METRIC ARRAYS...")
send_telegram_broadcast("🛸 *MARS_BOT V16.0 DAEMON DEPLOYED:* Background pipeline secured and monitoring all 7 global macro markets simultaneously.")

while True:
    print(f"🛰️ Executing simultaneous matrix scan at {datetime.datetime.now()}...")
    
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
                
                # Check for Convergent BUY Signals across all timeframes
                if rsi_15m < 40 and rsi_1h < 45 and rsi_4h < 50:
                    msg = f"🚀 *MARS_BOT CONVERGENT BUY SIGNAL*\n\n📈 *Asset:* {display_name}\n💵 *Price:* {current_price:.4f}\n🧭 *H1 RSI:* {rsi_1h:.1f}\n🛰️ *Status:* Telemetry confirms liquidity exhaustion. Standby for vector acceleration."
                    send_telegram_broadcast(msg)
                    log_vector_to_ledger(display_name, "🚀 BUY / LONG", current_price, rsi_1h, "🎯 FILLED")
                    
                # Check for Convergent SELL Signals across all timeframes
                elif rsi_15m > 60 and rsi_1h > 55 and rsi_4h > 50:
                    msg = f"💥 *MARS_BOT CONVERGENT SELL SIGNAL*\n\n📈 *Asset:* {display_name}\n💵 *Price:* {current_price:.4f}\n🧭 *H1 RSI:* {rsi_1h:.1f}\n🛰️ *Status:* Matrix overbought saturation detected. Fluid liquidation threat active."
                    send_telegram_broadcast(msg)
                    log_vector_to_ledger(display_name, "💥 SELL / SHORT", current_price, rsi_1h, "🎯 FILLED")
                    
        except Exception as e:
            print(f"Error scanning market {display_name}: {e}")
            
    # Interval cooldown delay: Sleep exactly 15 minutes (900 seconds) before recalculating metrics
    time.sleep(900)
