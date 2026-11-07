import streamlit as st

def load_ig_style():
    """
    Sovereign Cyberpunk CSS Overhaul Engine for MARS_BOT V16.0
    Implements glassmorphism, responsive data grids, and active glowing input focus levels.
    """
    st.markdown("""
        <style>
            /* 🛸 Global App Workspace Skin & Viewport Optimization */
            [data-testid="stAppViewContainer"] { 
                background-color: #0C0F12 !important; 
            }
            [data-testid="stHeader"] { 
                background: rgba(0,0,0,0) !important; 
            }
            
            /* 🔍 Premium Glassmorphic Dropdown Navigation Menu */
            div[data-baseweb="select"] {
                background-color: #161A1E !important;
                border: 1px solid #23292F !important;
                border-radius: 6px !important;
                transition: all 0.3s ease-in-out;
            }
            div[data-baseweb="select"]:focus-within {
                border-color: #00A4E4 !important;
                box-shadow: 0 0 12px rgba(0, 164, 228, 0.3) !important;
            }
            
            /* 🛰️ Tactile Neon Blue Satellite Scan Command Button */
            button[data-testid="baseButton-secondary"] {
                background-color: #00A4E4 !important;
                color: #FFFFFF !important;
                border: none !important;
                border-radius: 6px !important;
                width: 100% !important;
                font-weight: bold !important;
                letter-spacing: 0.5px !important;
                box-shadow: 0 4px 12px rgba(0, 164, 228, 0.2) !important;
                transition: all 0.2s ease-in-out;
            }
            button[data-testid="baseButton-secondary"]:hover {
                background-color: #00B4FA !important;
                transform: translateY(-1px) !important;
                box-shadow: 0 6px 16px rgba(0, 164, 228, 0.4) !important;
            }
            
            /* 📊 Custom Cyberpunk Sidebar Navigation Console Overrides */
            [data-testid="stSidebar"] {
                background-color: #090B0D !important;
                border-right: 1px solid #161A1E !important;
            }
            div[data-testid="stSidebarUserContent"] {
                padding-top: 2rem !important;
            }
            
            /* 🕯️ Plotly Graphic Viewport Wrapper Borders */
            div.stPlotlyChart {
                background-color: #111519 !important;
                border: 1px solid #1E2329 !important;
                border-radius: 8px !important;
                padding: 10px !important;
            }
        </style>
    """, unsafe_allow_html=True)
