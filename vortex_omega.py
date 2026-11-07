import os
import datetime
import requests
import yfinance as yf
import pandas as pd
import numpy as np

# 🔑 CRITICAL CORE CONFIGURATIONS
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

ACCOUNT_EQUITY = 1000.0
RISK_PERCENT = 0.01

MARKET_MAP = {
    "USDZAR=X": "USD/ZAR", "GBPUSD=X": "GBP/USD", "GC=F": "Gold", "EURUSD=X": "EUR/USD", 
    "USDJPY=X": "USD/JPY", "AUDUSD=X": "AUD/USD", "USDCAD=X": "USD/CAD"
}

def calculate_bollinger_bands(df, window=20, num_std=2):
    rolling_mean = df['Close'].rolling(window=window).mean()
    rolling_std = df['Close'].rolling(window=window).std()
    return rolling_mean + (rolling_std * num_std), rolling_mean, rolling_mean - (rolling_std * num_std)

def calculate_atr(df, window=14):
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    return ranges.max(axis=1).rolling(window=window).mean()

def calculate_position_size(market_key, stop_distance, is_zar, risk_multiplier=1.0):
    cash_risk = ACCOUNT_EQUITY * RISK_PERCENT * risk_multiplier
    if stop_distance <= 0: return 0.01
    if is_zar or "GC=F" not in market_key:
        units = cash_risk / stop_distance
        return max(0.01, round(units / 100000, 2))
    else:
        return max(0.01, round(cash_risk / (stop_distance * 100), 2))

def send_telegram_broadcast(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID: return
    url = f"https://telegram.org{TELEGRAM_BOT_TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}, timeout=10)
    except Exception: pass

print(f"🌀 Initiating VORTEX_OMEGA Adaptive Risk Execution Scan...")

for market_key, display_name in MARKET_MAP.items():
    try:
        feed = yf.Ticker(market_key)
        df_30m = feed.history(period="5d", interval="30m")
        
        if not df_30m.empty and len(df_30m) >= 20:
            current_price = df_30m['Close'].iloc[-1]
            upper_30m, _, lower_30m = calculate_bollinger_bands(df_30m)
            atr_30m = calculate_atr(df_30m)
            
            last_upper = upper_30m.iloc[-1]
            last_lower = lower_30m.iloc[-1]
            last_atr = atr_30m.iloc[-1]
            is_zar_pair = "USDZAR" in display_name
            
            # Weekend Gap Calculation Matrix
            prev_close = df_30m['Close'].iloc[-2]
            gap_amt = np.abs(current_price - prev_close)
            is_gap_volatile = gap_amt > (last_atr * 1.0)
            
            risk_mult = 0.5 if is_gap_volatile else 1.0
            gap_warning = "⚠️ *HIGH-RISK WEEKEND LIQUIDATION GAP DETECTED! RISK MITIGATION ACTIVE (LOTS SLICED 50%).*\n\n" if is_gap_volatile else ""
            
            # 🌀 CONDITION ALPHA: Volatility Liquidity Spike BUY
            if current_price < last_lower and (df_30m['High'].iloc[-1] - df_30m['Low'].iloc[-1]) > (1.5 * last_atr):
                stop_distance = last_atr * (2.5 if is_gap_volatile else 2.0)
                sl = current_price - stop_distance
                tp1 = current_price + (stop_distance * 1.5)
                tp2 = current_price + (stop_distance * 3.0)
                rec_lot = calculate_position_size(market_key, stop_distance, is_zar_pair, risk_mult)
                
                msg = f"🌀 *VORTEX_OMEGA LIQUIDATION TRAP (BUY)*\n\n" \
                      f"{gap_warning}" \
                      f"📈 *Asset:* {display_name}\n" \
                      f"💵 *Entry Price:* {current_price:.4f}\n" \
                      f"🛰️ *Volatility (ATR):* {last_atr:.4f}\n\n" \
                      f"🛡️ *RISK MANAGEMENT MATRIX ({int(RISK_PERCENT*100*risk_mult)}% RISK):*\n" \
                      f"🔴 *Stop-Loss:* {sl:.4f}\n" \
                      f"🟢 *Take-Profit 1 (1.5R):* {tp1:.4f}\n" \
                      f"🟢 *Take-Profit 2 (3.0R):* {tp2:.4f}\n" \
                      f"📊 *Recommended Lot Size:* `{rec_lot}` Lots\n\n" \
                      f"Compass *Vector:* Institutional stop-hunt sweep verified. Protective parameters live."
                send_telegram_broadcast(msg)
                
            # 🌀 CONDITION BETA: Volatility Liquidity Spike SELL
            elif current_price > last_upper and (df_30m['High'].iloc[-1] - df_30m['Low'].iloc[-1]) > (1.5 * last_atr):
                stop_distance = last_atr * (2.5 if is_gap_volatile else 2.0)
                sl = current_price + stop_distance
                tp1 = current_price - (stop_distance * 1.5)
                tp2 = current_price - (stop_loss_distance * 3.0) if 'stop_loss_distance' in locals() else current_price - (stop_distance * 3.0)
                rec_lot = calculate_position_size(market_key, stop_distance, is_zar_pair, risk_mult)
                
                msg = f"🌀 *VORTEX_OMEGA LIQUIDATION TRAP (SELL)*\n\n" \
                      f"{gap_warning}" \
                      f"📈 *Asset:* {display_name}\n" \
                      f"💵 *Entry Price:* {current_price:.4f}\n" \
                      f"🛰️ *Volatility (ATR):* {last_atr:.4f}\n\n" \
                      f"🛡️ *RISK MANAGEMENT MATRIX ({int(RISK_PERCENT*100*risk_mult)}% RISK):*\n" \
                      f"🔴 *Stop-Loss:* {sl:.4f}\n" \
                      f"🟢 *Take-Profit 1 (1.5R):* {tp1:.4f}\n" \
                      f"🟢 *Take-Profit 2 (3.0R):* {tp2:.4f}\n" \
                      f"📊 *Recommended Lot Size:* `{rec_lot}` Lots\n\n" \
                      f"🧭 *Vector:* Liquidity capture verified above value bands. Protective parameters live."
                send_telegram_broadcast(msg)

    except Exception as e:
        print(f"Error executing Vortex scan on {display_name}: {e}")
