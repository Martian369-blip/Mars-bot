import streamlit as st
import engine as eng

def render_news_tab(target_asset, ig_display_name):
    st.markdown(f"#### 📰 Market Intelligence Wire Stream: <span style='color:#00A4E4;'>{ig_display_name}</span>", unsafe_allow_html=True)
    st.divider()
    
    live_news = eng.fetch_specialized_news(target_asset)
    if not live_news:
        st.warning("📡 Sweeping global networks... Displaying baseline sovereign intelligence feeds:")
        st.markdown("##### 🦅 Federal Reserve Enforces Measured Approach Over Late-Autumn Sessions")
        st.write("Institutional dollar desks verify that robust labor metrics give central bankers massive scope to hold baseline borrowing yields steady.")
    else:
        for article in live_news:
            with st.container():
                st.markdown(f"<h5 style='margin-bottom:5px; color:#00A4E4;'>🛰️ {article['title']}</h5>", unsafe_allow_html=True)
                st.caption(f"📅 Wire Time: {article['pubDate']} | Macro Intelligence Node")
                st.markdown(f"[Launch Source Feed Link]({article['link']})")
