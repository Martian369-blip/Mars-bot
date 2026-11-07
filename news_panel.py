import streamlit as st
import pandas as pd
import datetime

def render_journal_tab(ig_display_name, price, h1_rsi, save_callback, clear_callback):
    """Autonomous ledger vault data management panel."""
    st.markdown("### 🕹️ Persistent Quant Ledger Session")
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        log_action = st.selectbox("ACTION:", ["BUY / LONG", "SELL / SHORT"])
    with col_l2:
        log_price = st.number_input("ENTRY PRICE VALUE:", value=float(price), format="%.4f")
        
    if st.button("🚀 TRANSMIT RECORD TO CLOUD VAULT"):
        new_row = pd.DataFrame([{
            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), 
            "Asset": ig_display_name, 
            "Action": log_action, 
            "Price": log_price, 
            "Matrix RSI": h1_rsi, 
            "Status": "LIVE UNREALIZED"
        }])
        save_callback(new_row)
        st.success("🛰️ Sequence captured securely into terminal storage!")
        st.rerun()
        
    st.divider()
    st.markdown("#### 📦 CLOUD SECURED LEDGER ROWS:")
    if st.session_state.journal_db.empty:
        st.info("⏳ Core ledger database is currently clean and awaiting transmissions.")
    else:
        st.dataframe(st.session_state.journal_db, use_container_width=True)
        if st.button("⚠️ ERASE GLOBAL STORAGE HISTORY"):
            clear_callback()
            st.rerun()
