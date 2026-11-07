import streamlit as st
import yfinance as yf

def render_news_tab(target_asset, ig_display_name):
    """Autonomous satellite intelligence stream parser block."""
    st.markdown(f"#### 📡 Active Intel Stream: <span style='color:#4CAF50;'>{ig_display_name}</span>", unsafe_allow_html=True)
    try:
        n_ticker = yf.Ticker(target_asset)
        news_list = n_ticker.news
        if news_list:
            for item in news_list[:5]:
                title = item.get("title", "No Title Available")
                publisher = item.get("publisher", "Global Feed")
                link = item.get("link", "#")
                st.markdown(f"""
                    <div class='cyber-card'>
                        <h5 style='margin:0; color:#4CAF50; font-family:monospace;'>📰 {publisher.upper()}</h5>
                        <p style='color:#FFFFFF; font-size:13px; font-weight:bold; margin:8px 0;'>{title}</p>
                        <a href='{link}' target='_blank' style='color:#90A4AE; font-size:11px; text-decoration:none; font-family:monospace;'>🔗 DECRYPT WIRE FEED →</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("⏳ Scanning frequencies... No active news briefs caught in this sector.")
    except Exception:
        st.error("❌ Intelligence stream fetch interrupted.")
