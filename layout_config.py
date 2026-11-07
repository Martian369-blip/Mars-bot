import streamlit as st

def load_ig_style():
    st.markdown("""
    <style>
        .stApp { background-color: #12161A; color: #ECEFF1; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        h1, h2, h3, h4, h5, h6 { color: #FFFFFF !important; font-weight: 600 !important; }
        div[data-testid="stContainer"] { border: 1px solid #23292F !important; background-color: #1C2127 !important; border-radius: 6px; padding: 18px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }
        .stButton>button { background-color: #1C2127 !important; color: #00A4E4 !important; border: 1px solid #00A4E4 !important; border-radius: 4px; font-size: 14px; width: 100%; height: 45px; font-weight: bold; transition: all 0.3s ease; }
        .stButton>button:hover { background-color: #00A4E4 !important; color: #FFFFFF !important; box-shadow: 0 0 10px rgba(0,164,228,0.4); }
        .stTextInput>div>div>input { background-color: #161A1E !important; color: #FFFFFF !important; border: 1px solid #2A323A !important; border-radius: 4px; text-align: center; font-size: 16px; height: 45px; }
        .stTextInput>div>div>input:focus { border-color: #00A4E4 !important; }
        .stSelectbox>div>div>div { background-color: #161A1E !important; color: #FFFFFF !important; border: 1px solid #2A323A !important; }
        .stNumberInput>div>div>input { background-color: #161A1E !important; color: #FFFFFF !important; border: 1px solid #2A323A !important; }
        section[data-testid="stSidebar"] { background-color: #161A1E !important; border-right: 1px solid #23292F !important; }
        section[data-testid="stSidebar"] .stRadio>div { color: #ECEFF1 !important; }
    </style>
    """, unsafe_allow_html=True)
