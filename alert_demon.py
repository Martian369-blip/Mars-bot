import time
import datetime
import os
import requests
import yfinance as yf
import engine as eng  # Reusing your core terminal math engine

# ==========================================
# 🔐 AUTHENTICATED TELEGRAM COCKPIT CHANNELS
# ==========================================
TELEGRAM_BOT_TOKEN = "7334795790:AAFFw9K5KofA0eX3781m_X6g-Zk4wM9_qmo"
TELEGRAM_CHAT_ID = "-4516766467"

# Watchlist array scanning space
MARKET_WATCHLIST = {
    "USDZAR=X": "USD/ZAR",
    "GBPUSD=X": "GBP/USD",
    "GC=F": "Gold",
    "EURUSD=X": "EUR/USD",
    "USDJPY=X": "USD/JPY",
    "AUDUSD=X": "AUD/USD",
    "USDCAD=X": "USD/CAD"
}

# Persistent execution state memory matrix
SIGNAL_STATE_CACHE = {ticker: "⏳ HOLD / STANDBY" for ticker in MARKET_WATCHLIST}

def check_macro_radar():
    """Evaluates multi-matrix proximity metrics for upcoming global macro hazards."""
    current_time = datetime.datetime.now()
    macro_calendar = [
        {"event": "🇺🇸 US Core CPI Inflation Print", "date": datetime.date(2026, 11, 12), "hour": 15, "minute": 30},
        {"event": "🇿🇦 SARB Interest Rate Decision", "date": datetime.date(2026, 11, 19), "hour": 15, "minute": 0},
        {"event": "🇺🇸 Federal Reserve FOMC Decision", "date": datetime.date(2026, 12, 16), "hour": 21, "minute": 0},
    ]
    for item in macro_calendar:
        event_dt = datetime.datetime.combine(item["date"], datetime.time(item["hour"], item["minute"]))
        if event_dt > current_time:
            delta = event_dt - current_time
            if delta.total_seconds() <= 86400:  # Within 24-hour threat radius
                hours, remainder = divmod(int(delta.total_seconds()), 3600)
                minutes, _ = divmod(remainder, 60)
                return f"🚨 *CRITICAL MACRO HAZARD PROXIMITY*:\n`{item['event']} in {hours}h {minutes}m!`"
    return "🛰️ *RADAR CLEAR*:\n`No high-impact volatility blocks inside 24h horizon.`"

def transmit_telegram_signal(display_name, direction, price, h1_rsi, macro_alert, rsi_warning):
    """Dispatches a clean, formatted Markdown message block directly to your Telegram chat."""
    signal_emoji = "🟢" if "BUY" in direction else "🔴"
    
    # Construct a high-signal markdown block string format
    message_text = (
        f"🛸 *MARS_BOT STRATEGY FLIP VECTOR DETECTED*\n"
        f"───────────────────────\n"
        f"📈 *MARKET:* `{display_name}`\n"
        f"{signal_emoji} *CONVERGENCE:* *{direction}*\n"
        f"⚡ *SPOT PRICE:* `{price:.4f}`\n"
        f"🧭 *1H RSI MATRIX:* `{h1_rsi:.1f}`\n"
        f"───────────────────────\n"
    )
    
    if rsi_warning:
        message_text += f"⚠️ *BOUNDARIES EXHAUSTION WARNING*:\n`{rsi_warning}`\n\n"
        
    message_text += f"📡 *SATELLITE MACRO RADAR FEED*:\n{macro_alert}"

    url = f"https://telegram.org{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message_text,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"🛰️ Telegram broadcast matrix dispatched for {display_name}!")
        else:
            print(f"❌ API rejection block encountered: {response.text}")
    except Exception as e:
        print(f"❌ Connection pipeline dropped to Telegram gateway: {e}")

def run_telemetry_loop():
    """Simultaneously audits the background watchlist array matrix."""
    print("🛸 MARS_BOT Background Watcher Vector Array Running over Telegram Matrix...")
    while True:
        macro_alert = check_macro_radar()
        
        for ticker, display_name in MARKET_WATCHLIST.items():
            try:
                t_feed = yf.Ticker(ticker)
                df_15m = t_feed.history(period="2d", interval="15m")
                df_1h = t_feed.history(period="15d", interval="1h")
                df_4h = t_feed.history(period="30d", interval="4h")
                
                if not df_1h.empty:
                    price = df_1h['Close'].iloc[-1]
                    m15_rsi = eng.calculate_rsi(df_15m).iloc[-1] if not df_15m.empty else 50.0
                    h1_rsi = eng.calculate_rsi(df_1h).iloc[-1]
                    h4_rsi = eng.calculate_rsi(df_4h).iloc[-1] if not df_4h.empty else 50.0
                    
                    # 1. Evaluate Technical Convergence Strategy Vectors
                    if m15_rsi < 40 and h1_rsi < 45 and h4_rsi < 50:
                        current_dir = "🚀 CONVERGENT BUY"
                    elif m15_rsi > 60 and h1_rsi > 55 and h4_rsi > 50:
                        current_dir = "💥 CONVERGENT SELL"
                    else:
                        current_dir = "⏳ HOLD / STANDBY"
                    
                    # 2. Check for RSI Exhaustion Levels (Overbought/Oversold extremes)
                    rsi_warning = None
                    if h1_rsi <= 30:
                        rsi_warning = "Asset is deeply oversold beneath technical boundaries!"
                    elif h1_rsi >= 70:
                        rsi_warning = "Asset is deeply overbought above technical boundaries!"
                    
                    # 3. Check for Convergence State Changes to prevent spam
                    last_dir = SIGNAL_STATE_CACHE[ticker]
                    if current_dir != last_dir:
                        # Only fire updates for valid entry executions, skipping standby returns
                        if "HOLD" not in current_dir:
                            transmit_telegram_signal(display_name, current_dir, price, h1_rsi, macro_alert, rsi_warning)
                        
                        # Sync state register cache memory keys
                        SIGNAL_STATE_CACHE[ticker] = current_dir
                        
            except Exception as e:
                print(f"⚠️ Tracking pass paused on ticker {display_name}: {e}")
                
        # Frequency interval throttle loop delay (Audit watchlist variables every 5 minutes)
        time.sleep(300)

if __name__ == "__main__":
    run_telemetry_loop()
