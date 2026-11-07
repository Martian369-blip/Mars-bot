import streamlit as st
import pandas as pd
import datetime

def render_journal_tab(ig_display_name, price, h1_rsi, save_callback, clear_callback):
    """Complete institutional quantitative ledger dashboard workstation module."""
    st.markdown("### 🕹️ Persistent Quant Ledger Session")
    
    # Calculate rows using dict-safe checking logic keys
    total_trades = len(st.session_state["journal_db"])
    buys_count = len(st.session_state["journal_db"][st.session_state["journal_db"]["Action"].str.contains("BUY", na=False)]) if total_trades > 0 else 0
    sells_count = total_trades - buys_count
    
    st.markdown(f"""
        <div class='cyber-card' style='border-left-color: #9C27B0;'>
            <h4 style='text-align:center; color:#FFFFFF; margin-top:0px; font-family:monospace; font-size:12px; letter-spacing:1px;'>📊 TERMINAL PERFORMANCE AGGREGATIONS</h4>
            <div style='display: flex; justify-content: space-around; text-align: center; margin-top:10px;'>
                <div>
                    <p style='color:#90A4AE; font-size:9px; margin:0;'>TOTAL ENTRIES</p>
                    <h3 style='color:#FFFFFF; margin:5px 0 0 0; font-family:monospace;'>{total_trades}</h3>
                </div>
                <div style='border-left: 1px solid #1F1140; border-right: 1px solid #1F1140; padding: 0 20px;'>
                    <p style='color:#4CAF50; font-size:9px; margin:0;'>LONG POSITIONS</p>
                    <h3 style='color:#4CAF50; margin:5px 0 0 0; font-family:monospace;'>{buys_count}</h3>
                </div>
                <div>
                    <p style='color:#E53935; font-size:9px; margin:0;'>SHORT POSITIONS</p>
                    <h3 style='color:#E53935; margin:5px 0 0 0; font-family:monospace;'>{sells_count}</h3>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        log_action = st.selectbox("EXECUTE STRATEGY ACTION:", ["BUY / LONG", "SELL / SHORT"])
    with col_l2:
        log_price = st.number_input("VERIFY ENTRY PRICE VALUE:", value=float(price), format="%.4f")
        
    if st.button("🚀 TRANSMIT RECORD TO CLOUD VAULT"):
        new_row = pd.DataFrame([{
            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), 
            "Asset": ig_display_name, 
            "Action": log_action, 
            "Price": log_price, 
            "Matrix RSI": round(float(h1_rsi), 1), 
            "Status": "LIVE UNREALIZED"
        }])
        save_callback(new_row)
        st.success("🛰️ Sequence captured securely into terminal storage!")
        st.rerun()
        
    st.divider()
    st.markdown("#### 📦 CLOUD SECURED LEDGER ROWS:")
    if st.session_state["journal_db"].empty:
        st.info("⏳ Core ledger database is currently clean and awaiting transmissions.")
    else:
        st.dataframe(st.session_state["journal_db"], use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⚠️ ERASE GLOBAL STORAGE HISTORY"):
            clear_callback()
            st.rerun()
