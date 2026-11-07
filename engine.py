import pandas as pd
import numpy as np

def calculate_rsi(df, periods=14):
    """Calculates Relative Strength Index securely over data rows."""
    if len(df) < periods:
        return pd.Series(50.0, index=df.index)
    close_delta = df['Close'].diff()
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    ma_up = up.ewm(com=periods - 1, adjust=False).mean()
    ma_down = down.ewm(com=periods - 1, adjust=False).mean()
    rsi = ma_up / ma_down
    rsi = 100 - (100 / (1 + rsi))
    return rsi.fillna(50.0)

def extract_hourly_atr(df, period=14):
    """Extracts Average True Range calculation from pricing feed."""
    if len(df) < period:
        return 0.015
    high_low = df['High'] - df['Low']
    high_cp = np.abs(df['High'] - df['Close'].shift())
    low_cp = np.abs(df['Low'] - df['Close'].shift())
    df_tr = pd.concat([high_low, high_cp, low_cp], axis=1)
    true_range = np.max(df_tr, axis=1)
    atr = true_range.rolling(window=period).mean()
    return float(atr.iloc[-1]) if not pd.isna(atr.iloc[-1]) else 0.015

def scan_candlestick_patterns(df):
    """Scans for significant market pivot structural markers."""
    if len(df) < 3:
        return "⏳ SCANNING MATRIX SYNC..."
    c_close = df['Close'].iloc[-1]
    c_open = df['Open'].iloc[-1]
    p_close = df['Close'].iloc[-2]
    p_open = df['Open'].iloc[-2]
    
    # Simple Bullish / Bearish engulfing matrix check
    if c_close > c_open and p_close < p_open and c_close >= p_open and c_open <= p_close:
        return "🔥 ALIGNED DIRECTIONAL CONCURRENCE: BULLISH ENGULFING MARKER"
    if c_close < c_open and p_close > p_open and c_close <= p_open and c_open >= p_close:
        return "💥 ALIGNED DIRECTIONAL CONCURRENCE: BEARISH ENGULFING MARKER"
    return "⏳ BALANCED TELEMETRY STATED STRUCTURE"
