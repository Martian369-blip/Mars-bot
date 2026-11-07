import streamlit as st

def load_ig_style():
    """
    Sovereign Apex Emerald-Ultramarine Stark Contrast Overhaul
    Injects high-contrast solid white presentation backdrops into the technical grid frames.
    """
    st.markdown("""
        <style>
            /* 🛸 1. RICH ULTRAMARINE COBALT OUTER VOID SKIN */
            html, body, [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"] { 
                background-color: #0B0518 !important; 
            }
            [data-testid="stHeader"] { 
                background: rgba(0,0,0,0) !important; 
            }
            
            /* 🟢 Monospace Matrix Telemetry Data Text Tweaks */
            .matrix-num {
                font-family: "Courier New", Courier, monospace !important;
                font-weight: bold !important;
                color: #2E7D32 !important; /* Slightly darker green to retain crisp readability on white */
            }
            
            /* 🔍 Glassmorphic Deep Workspace Menu Options */
            div[data-baseweb="select"] {
                background-color: #120A26 !important;
                border: 1px solid #1F1140 !important;
                border-radius: 4px !important;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            }
            div[data-baseweb="select"]:focus-within {
                border-color: #4CAF50 !important;
                box-shadow: 0 0 14px rgba(76, 175, 80, 0.25) !important;
            }
            
            /* 🛰️ Tactile Neon Emerald Scan Command Selector Switch */
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
            
            /* 📊 Heavy Ultramarine Sidebar Console Options Panel */
            [data-testid="stSidebar"] {
                background-color: #070310 !important;
                border-right: 1px solid #140C2B !important;
            }
            
            /* 🕯️ FIXED: THE STARK WHITE DISK CHARTS BACKGROUND LAYER */
            div.stPlotlyChart {
                background-color: #FFFFFF !important;
                border: 1px solid #E0E4E8 !important;
                border-radius: 6px !important;
                padding: 12px !important;
                box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4) !important;
            }
            
            /* 🚀 FIXED: THE STARK WHITE DATA CARD PRESENTATION DECK BLOCK */
            .cyber-card {
                background: #FFFFFF;
                border-left: 4px solid #2E7D32;
                border-top: 1px solid #E0E4E8;
                border-right: 1px solid #E0E4E8;
                border-bottom: 1px solid #E0E4E8;
                border-radius: 4px;
                padding: 18px;
                margin-bottom: 20px;
                box-shadow: 0 12px 40px rgba(0, 0, 0, 0.35);
            }
            
            /* Adjust internal text elements inside white modules for clear readability */
            .cyber-card h3 { color: #0B0518 !important; }
            .cyber-card p { color: #546E7A !important; }
            .cyber-card hr { border-color: #ECEFF1 !important; }
        </style>
    """, unsafe_allow_html=True)
