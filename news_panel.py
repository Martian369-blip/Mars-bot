import streamlit as st
import yfinance as yf

def render_news_tab(target_asset, ig_display_name):
    """Multi-layer autonomous intelligence stream with structural fallbacks."""
    st.markdown(f"#### 📡 Active Intel Stream: <span style='color:#4CAF50;'>{ig_display_name}</span>", unsafe_allow_html=True)
    
    try:
        n_ticker = yf.Ticker(target_asset)
        news_list = n_ticker.news
        
        valid_news_found = False
        
        if news_list and isinstance(news_list, list):
            for item in news_list[:5]:
                # Dynamic structural lookup key checking
                title = item.get("title") or item.get("content", {}).get("title")
                publisher = item.get("publisher") or item.get("source") or "GLOBAL FEED"
                link = item.get("link") or item.get("url") or "#"
                
                if title and title != "No Title Available":
                    valid_news_found = True
                    st.markdown(f"""
                        <div class='cyber-card'>
                            <h5 style='margin:0; color:#4CAF50; font-family:monospace;'>📰 {str(publisher).upper()}</h5>
                            <p style='color:#FFFFFF; font-size:13px; font-weight:bold; margin:8px 0;'>{title}</p>
                            <a href='{link}' target='_blank' style='color:#90A4AE; font-size:11px; text-decoration:none; font-family:monospace;'>🔗 DECRYPT WIRE FEED →</a>
                        </div>
                    """, unsafe_allow_html=True)
                    
        # 🚀 AUTOMATIC HIGH-SIGNAL MACRO FEED FALLBACK IF TICKER NEWS IS BARREN
        if not valid_news_found:
            fallback_feed = yf.Ticker("SPY").news
            if fallback_feed:
                st.markdown("<p style='font-size:10px; font-family:monospace; color:#FFB300; margin-bottom:15px;'>🛰️ SPECIFIC FX NODE BARREN — DIVERTING SATELLITE TO GLOBAL MACRO LIQUIDITY WIRE</p>", unsafe_allow_html=True)
                for item in fallback_feed[:4]:
                    title = item.get("title") or "Macro Liquidity Movement Block Detected"
                    publisher = item.get("publisher") or "MARKET WIRE"
                    link = item.get("link") or "#"
                    st.markdown(f"""
                        <div class='cyber-card'>
                            <h5 style='margin:0; color:#FFB300; font-family:monospace;'>📰 {str(publisher).upper()}</h5>
                            <p style='color:#FFFFFF; font-size:13px; font-weight:bold; margin:8px 0;'>{title}</p>
                            <a href='{link}' target='_blank' style='color:#90A4AE; font-size:11px; text-decoration:none; font-family:monospace;'>🔗 DECRYPT WIRE FEED →</a>
                        </div>
                    """, unsafe_allow_html=True)
    except Exception:
        st.error("❌ Intelligence stream fetch interrupted.")
