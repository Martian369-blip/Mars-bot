import os
import datetime
import requests
import yfinance as yf
import pandas as pd
import numpy as np

# 🔑 CRITICAL CORE CONFIGURATIONS
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Institutional Risk Management Model Baselines
ACCOUNT_EQUITY = 1000.0  # Change to your exact account size
RISK_PERCENT = 0.01      # Risking strictly 1% of account equity per trade vector

MARKET_MAP = {
    "USDZAR=X": "USD/ZAR", "GBPUSD=X": "GBP/USD", "GC=F": "Gold", "EURUSD=X": "EUR/USD", 
    "USDJPY=X": "USD/JPY", "AUDUSD=X": "AUD/USD", "USDCAD=X": "USD/CAD"
}

def calculate_rsi(df, period=14):
    if len(df) < period: return pd.Series([50.0] * len(df))
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_atr(df, window=14):
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    return ranges.max(axis=1).rolling(window=window).mean()

def calculate_position_size(market_key, stop_distance, is_zar, risk_multiplier=1.0):
    cash_risk = ACCOUNT_EQUITY * RISK_PERCENT * risk_multiplier
    if stop_distance <= 0: return 0.01
    
    if is_zar:
        units = cash_risk / stop_distance
        return max(0.01, round(units / 100000, 2))
    elif "GC=F" in market_key:
        lots = cash_risk / (stop_distance * 100)
        return max(0.01, round(lots, 2))
    else:
        units = cash_risk / stop_distance
        return max(0.01, round(units / 100000, 2))

def send_telegram_broadcast(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID: return
    url = f"https://telegram.org{TELEGRAM_BOT_TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}, timeout=10)
    except Exception: pass

print(f"🛰️ Triggering ultimate gap-mitigated matrix scan...")

for market_key, display_name in MARKET_MAP.items():
    try:
        feed = yf.Ticker(market_key)
        df_15m = feed.history(period="5d", interval="15m")
        df_1h = feed.history(period="30d", interval="1h")
        df_4h = feed.history(period="60d", interval="4h")
        
        if not df_1h.empty and len(df_1h) >= 20:
            current_price = df_1h['Close'].iloc[-1]
            rsi_15m = calculate_rsi(df_15m).iloc[-1] if not df_15m.empty else 50.0
            rsi_1h = calculate_rsi(df_1h).iloc[-1]
            rsi_4h = calculate_rsi(df_4h).iloc[-1] if not df_4h.empty else 50.0
            
            atr_series = calculate_atr(df_1h)
            current_atr = atr_series.iloc[-1]
            
            # Check for Sunday Weekend Opening Gaps
            prev_close = df_1h['Close'].iloc[-2]
            gap_amt = np.abs(current_price - prev_close)
            is_gap_volatile = gap_amt > (current_atr * 1.0)
            
            risk_mult = 0.5 if is_gap_volatile else 1.0
            gap_warning = "⚠️ *HIGH-RISK WEEKEND LIQUIDATION GAP DETECTED! RISK MITIGATION ACTIVE (LOTS SLICED 50%).*\n\n" if is_gap_volatile else ""
            
            # Risk bracket boundaries adjusted dynamically for volatile open sessions
            stop_loss_distance = current_atr * (2.0 if is_gap_volatile else 1.5)
            is_zar_pair = "USDZAR" in display_name
            
            # 🚀 CONVERGENT BUY
            if rsi_15m < 40 and rsi_1h < 45 and rsi_4h < 50:
                sl = current_price - stop_loss_distance
                tp1 = current_price + (stop_loss_distance * 1.5)
                tp2 = current_price + (stop_loss_distance * 3.0)
                rec_lot = calculate_position_size(market_key, stop_loss_distance, is_zar_pair, risk_mult)
                
                msg = f"🚀 *MARS_BOT CONVERGENT BUY SIGNAL*\n\n" \
                      f"{gap_warning}" \
                      f"📈 *Asset:* {display_name}\n" \
                      f"💵 *Entry Price:* {current_price:.4f}\n" \
                      f"🧭 *H1 RSI:* {rsi_1h:.1f}\n\n" \
                      f"🛡️ *RISK MANAGEMENT MATRIX ({int(RISK_PERCENT*100*risk_mult)}% RISK):*\n" \
                      f"🔴 *Stop-Loss:* {sl:.4f}\n" \
                      f"🟢 *Take-Profit 1 (1.5R):* {tp1:.4f}\n" \
                      f"🟢 *Take-Profit 2 (3.0R):* {tp2:.4f}\n" \
                      f"📊 *Recommended Lot Size:* `{rec_lot}` Lots\n\n" \
                      f"🛰 *Status:* Momentum convergence verified. Adaptive execution live."
                send_telegram_broadcast(msg)
                
            # 💥 CONVERGENT SELL
            elif rsi_15m > 60 and rsi_1h > 55 and rsi_4h > 50:
                sl = current_price + stop_loss_distance
                tp1 = current_price - (stop_loss_distance * 1.5)
                tp2 = current_price - (stop_loss_distance * 3.0)
                rec_lot = calculate_position_size(market_key, stop_loss_distance, is_zar_pair, risk_mult)
                
                msg = f"💥 *MARS_BOT CONVERGENT SELL SIGNAL*\n\n" \
                      f"{gap_warning}" \
                      f"📈 *Asset:* {display_name}\n" \
                      f"💵 *Entry Price:* {current_price:.4f}\n" \
                      f"🧭 *H1 RSI:* {rsi_1h:.1f}\n\n" \
                      f"🛡️ *RISK MANAGEMENT MATRIX ({int(RISK_PERCENT*100*risk_mult)}% RISK):*\n" \
                      f"🔴 *Stop-Loss:* {sl:.4f}\n" \
                      f"🟢 *Take-Profit 1 (1.5R):* {tp1:.4f}\n" \
                      f"🟢 *Take-Profit 2 (3.0R):* {tp2:.4f}\n" \
                      f"📊 *Recommended Lot Size:* `{rec_lot}` Lots\n\n" \
                      f"🛰️ *Status:* Saturation confirmed. Adaptive execution live."
                send_telegram_broadcast(msg)
                
    except Exception as e:
        print(f"Error executing scan on {display_name}: {e}")
