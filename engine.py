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

def fetch_specialized_news(query_ticker):
    try:
        clean_q = query_ticker.replace("=X", "").replace("^", "")
        url = f"https://google.com{clean_q}+finance+market&hl=en-US&gl=US&ceid=US:en"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
        root = ET.fromstring(xml_data)
        articles = []
        for item in root.findall('.//item')[:4]:
            articles.append({
                "title": item.find('title').text,
                "link": item.find('link').text,
                "pubDate": item.find('pubDate').text
            })
        return articles
    except Exception:
        return []
