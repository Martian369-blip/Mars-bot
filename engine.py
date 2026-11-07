import yfinance as yf
import pandas as pd
import numpy as np
import urllib.request
import xml.etree.ElementTree as ET

def calculate_rsi(df, window=14):
    if len(df) < window: 
        return pd.Series(50.0, index=df.index)
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50.0)

def extract_hourly_atr(df_hourly, window=14):
    if len(df_hourly) < window: 
        return df_hourly['Close'].iloc[-1] * 0.002 if not df_hourly.empty else 0.01
    high_low = df_hourly['High'] - df_hourly['Low']
    high_close = np.abs(df_hourly['High'] - df_hourly['Close'].shift())
    low_close = np.abs(df_hourly['Low'] - df_hourly['Close'].shift())
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = true_range.rolling(window).mean().iloc[-1]
    return atr if not pd.isna(atr) else df_hourly['Close'].iloc[-1] * 0.002

def compute_ichimoku(df):
    if len(df) < 52:
        df['tenkan_sen'] = df['Close']
        df['kijun_sen'] = df['Close']
        df['senkou_span_a'] = df['Close']
        df['senkou_span_b'] = df['Close']
        return df
    high_9 = df['High'].rolling(window=9).max()
    low_9 = df['Low'].rolling(window=9).min()
    df['tenkan_sen'] = (high_9 + low_9) / 2
    high_26 = df['High'].rolling(window=26).max()
    low_26 = df['Low'].rolling(window=26).min()
    df['kijun_sen'] = (high_26 + low_26) / 2
    df['senkou_span_a'] = ((df['tenkan_sen'] + df['kijun_sen']) / 2).shift(26)
    high_52 = df['High'].rolling(window=52).max()
    low_52 = df['Low'].rolling(window=52).min()
    df['senkou_span_b'] = ((high_52 + low_52) / 2).shift(26)
    return df

def scan_candlestick_patterns(df):
    """
    🔍 UPGRADE 1: Automated Candlestick Pattern Core Scanner Matrix
    Parses the last 2 completed bars to trace immediate structural setups.
    """
    if len(df) < 3:
        return "⏳ SCANNING STRATOSPHERE..."
    
    # Grab data nodes from the last 2 rows
    c1_open, c1_high, c1_low, c1_close = df['Open'].iloc[-2], df['High'].iloc[-2], df['Low'].iloc[-2], df['Close'].iloc[-2]
    c2_open, c2_high, c2_low, c2_close = df['Open'].iloc[-1], df['High'].iloc[-1], df['Low'].iloc[-1], df['Close'].iloc[-1]
    
    # Mathematical measurements of body sizes
    body1 = c1_close - c1_open
    body2 = c2_close - c2_open
    
    # Check 1: Bullish Engulfing
    if body1 < 0 and body2 > 0 and c2_close >= c1_open and c2_open <= c1_close:
        return "🚀 ALIGNMENT: BULLISH ENGULFING BLOCK DETECTED"
        
    # Check 2: Bearish Engulfing
    if body1 > 0 and body2 < 0 and c2_close <= c1_open and c2_open >= c1_close:
        return "💥 ALIGNMENT: BEARISH ENGULFING DISTRIBUTION DETECTED"
        
    # Check 3: Hammer / Pin Bar setup
    c2_range = c2_high - c2_low
    c2_body_abs = abs(body2)
    lower_wick = (c2_open - c2_low) if body2 > 0 else (c2_close - c2_low)
    
    if c2_range > 0 and (lower_wick / c2_range) >= 0.6 and c2_body_abs <= (c2_range * 0.3):
        return "🔨 ALIGNMENT: REVERSAL PIN BAR / HAMMER FOUND ON THE FLOOR"
        
    return "⏳ NO IMPERATIVE CANDLE REVERSALS CONFIRMED"

def fetch_specialized_news(query_ticker):
    try:
        ticker_map = {
            "GC=F": "Gold commodity finance market",
            "USDZAR=X": "South African Rand currency market",
            "GBPUSD=X": "Pound Sterling currency market",
            "EURUSD=X": "Euro Dollar currency market"
        }
        search_phrase = ticker_map.get(query_ticker, f"{query_ticker} financial market")
        encoded_phrase = urllib.parse.quote(search_phrase)
        url = f"https://google.com{encoded_phrase}&hl=en-US&gl=US&ceid=US:en"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=7) as response:
            xml_data = response.read()
        root = ET.fromstring(xml_data)
        articles = []
        for item in root.findall('.//item')[:5]:
            title_text = item.find('title').text
            if " - " in title_text:
                title_text = title_text.rsplit(" - ", 1)[0]
            articles.append({
                "title": title_text,
                "link": item.find('link').text,
                "pubDate": item.find('pubDate').text
            })
        return articles
    except Exception:
        return []
