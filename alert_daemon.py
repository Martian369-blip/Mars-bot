import time
import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import yfinance as yf
import engine as eng  # Reusing your core terminal math engine

# ==========================================
# 🔐 SECURE DISCRETE TELEMETRY CREDENTIALS
# ==========================================
SMTP_SERVER = "://gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"  # Use Google App Password
RECEIVER_EMAIL = "your_destination@gmail.com"

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
                return f"🚨 CRITICAL EVENT PROXIMITY: {item['event']} in {hours}h {minutes}m!"
    return "🛰️ RADAR CLEAR: No high-impact volatility blocks in 24h threat horizon."

def transmit_signal_email(display_name, direction, price, h1_rsi, macro_alert, rsi_warning):
    """Dispatches a premium multi-matrix technical briefing HTML dispatch email."""
    subject = f"🛸 MARS_BOT SIGNAL VECTOR FLIP: {display_name} -> {direction}"
    
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    
    color_hex = "#4CAF50" if "BUY" in direction else "#E53935"
    
    html = f"""
    <html>
        <body style="background-color: #0B0518; color: #FFFFFF; font-family: monospace; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: #120A26; border: 2px solid #1F1140; padding: 20px; border-radius: 8px;">
                <h2 style="color: #FFFFFF; text-align: center; border-bottom: 1px solid #1F1140; padding-bottom: 10px;">🛸 MARS_BOT VECTOR FLIP</h2>
                
                <p style="font-size: 14px; text-align: center; color: #90A4AE;">
                    Autonomous surveillance core has intercepted a strategy convergence matrix cross matching point.
                </p>
                
                <div style="background-color: rgba(0,0,0,0.3); border-left: 4px solid {color_hex}; padding: 15px; margin: 20px 0;">
                    <p style="margin: 5px 0; font-size: 16px;"><b>MARKET:</b> <span style="color: #00E5FF;">{display_name}</span></p>
                    <p style="margin: 5px 0; font-size: 16px;"><b>CONVERGENCE:</b> <span style="color: {color_hex}; font-weight: bold;">{direction}</span></p>
                    <p style="margin: 5px 0; font-size: 16px;"><b>SPOT PRICE:</b> <span>{price:.4f}</span></p>
                    <p style="margin: 5px 0; font-size: 16px;"><b>1H RSI VALUE:</b> <span style="color: #FFB300;">{h1_rsi:.1f}</span></p>
                </div>
                
                {f'<div style="background-color: #7F0000; color: #FFFFFF; padding: 10px; border-radius: 4px; font-weight: bold; text-align: center; margin-bottom: 15px;">⚠️ {rsi_warning}</div>' if rsi_warning else ''}
                
                <div style="background-color: #160D2F; border: 1px solid #2A1B4E; padding: 12px; border-radius: 4px; font-size: 11px; color: #CFD8DC;">
                    <b>📡 SATELLITE MACRO GAUGE:</b><br>{macro_alert}
                </div>
                
                <p style="font-size: 10px; color: #607D8B; text-align: center; margin-top: 25px; border-top: 1px solid #1F1140; padding-top: 15px;">
                    Sovereign Quantum Terminal Execution Layer • Secure Session Channel
                </p>
            </div>
        </body>
    </html>
    """
    
    msg.attach(MIMEText(html, "html"))
    
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print(f"🛰️ Alert transmission complete for {display_name}!")
    except Exception as e:
        print(f"❌ Mail pipeline dispatch dropped: {e}")

def run_telemetry_loop():
    """Simultaneously audits the background watchlist array matrix."""
    print("🛸 MARS_BOT Background Watcher Vector Array Running...")
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
                        rsi_warning = "CRITICAL EXHAUSTION: Asset is profoundly oversold under technical boundaries!"
                    elif h1_rsi >= 70:
                        rsi_warning = "CRITICAL SATURATION: Asset is profoundly overbought under technical boundaries!"
                    
                    # 3. Check for Convergence State Changes to prevent spam
                    last_dir = SIGNAL_STATE_CACHE[ticker]
                    if current_dir != last_dir:
                        # Only fire emails for valid transaction setups, skipping hold transitions
                        if "HOLD" not in current_dir:
                            transmit_signal_email(display_name, current_dir, price, h1_rsi, macro_alert, rsi_warning)
                        
                        # Sync state register cache memory keys
                        SIGNAL_STATE_CACHE[ticker] = current_dir
                        
            except Exception as e:
                print(f"⚠️ Tracking pass paused on ticker {display_name}: {e}")
                
        # Audit frequency interval throttle delay (e.g., scan the matrix arrays every 5 minutes)
        time.sleep(300)

if __name__ == "__main__":
    run_telemetry_loop()
