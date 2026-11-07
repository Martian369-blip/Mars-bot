import streamlit as st

def load_ig_style():
    """
    Sovereign Apex Emerald Cyber Matrix Layout Overhaul - Premium Hue Variance
    Configured with deep space foundation hues for high-contrast element separation.
    """
    st.markdown("""
        <style>
            /* 🛸 MAXIMUM DEPTH SPACE HUD BACKGROUND OVERRIDES */
            html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"] { 
                background-color: #060B11 !important; /* Change this specific hex to alter the master background */
            }
            [data-testid="stHeader"] { 
                background: rgba(0,0,0,0) !important; 
            }
            
            /* 🟢 High-Density Monospace Telemetry Typography */
            h1, h2, h3, h4, h5, h6, p, div, span, label {
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
                letter-spacing: 0.5px !important;
            }
            .matrix-num {
                font-family: "Courier New", Courier, monospace !important;
                font-weight: bold !important;
                color: #4CAF50 !important;
                text-shadow: 0 0 10px rgba(76, 175, 80, 0.35) !important;
            }
            
            /* 🔍 Glassmorphic Active Dropdown Menu Grid */
            div[data-baseweb="select"] {
                background-color: #0E151E !important;
                border: 1px solid #1A2430 !important;
                border-radius: 4px !important;
                transition: all 0.3s ease-in-out;
            }
            div[data-baseweb="select"]:focus-within {
                border-color: #4CAF50 !important;
                box-shadow: 0 0 14px rgba(76, 175, 80, 0.25) !important;
            }
            
            /* 🛰️ Tactile Neon Emerald Scan Trigger Command */
            button[data-testid="baseButton-secondary"] {
                background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%) !important;
                color: #FFFFFF !important;
                border: none !important;
                border-radius: 4px !important;
                width: 100% !important;
                font-weight: 800 !important;
                letter-spacing: 1px !important;
                box-shadow: 0 4px 14px rgba(76, 175, 80, 0.2) !important;
                transition: all 0.2s ease-in-out;
            }
            button[data-testid="baseButton-secondary"]:hover {
                transform: translateY(-1px) !important;
                box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4) !important;
            }
            
            /* 📊 Cyberpunk Console Sidebar Menu Overrides */
            [data-testid="stSidebar"] {
                background-color: #03060A !important;
                border-right: 1px solid #0E151E !important;
            }
            
            /* 🕯️ Graphic Viewport Container Frames */
            div.stPlotlyChart {
                background-color: #0B1017 !important;
                border: 1px solid #16202C !important;
                border-radius: 6px !important;
                padding: 12px !important;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6) !important;
            }
            
            /* 🚀 Premium Telemetry Matrix Data Card Block */
            .cyber-card {
                background: #0B1017;
                border-left: 3px solid #4CAF50;
                border-top: 1px solid #16202C;
                border-right: 1px solid #16202C;
                border-bottom: 1px solid #16202C;
                border-radius: 4px;
                padding: 18px;
                margin-bottom: 20px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            }
        </style>
    """, unsafe_allow_html=True)
