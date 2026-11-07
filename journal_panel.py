import streamlit as st
import pandas as pd
import datetime

def render_journal_tab(ig_display_name, price, h1_rsi, save_callback, clear_callback):
    """Institutional quantitative ledger matrix with complete cashflow logging tracks."""
    st.markdown("### 🕹️ Persistent Quant Ledger Session")
    
    # 📊 Live Dashboard Scoreboard Aggregations
    total_trades = len(st.session_state.get("journal_db", pd.DataFrame()))
    
    # Load separate cashflow ledger database if not set
    if "cashflow_db" not in st.session_state:
        if os.path.exists("cashflow_vault.csv"):
            try: st.session_state["cashflow_db"] = pd.read_csv("cashflow_vault.csv")
            except Exception: st.session_state["cashflow_db"] = pd.DataFrame(columns=["Timestamp", "Type", "Amount", "Currency", "Status"])
        else:
            st.session_state["cashflow_db"] = pd.DataFrame(columns=["Timestamp", "Type", "Amount", "Currency", "Status"])

    # Render Dual Sub-Workspace Channels
    sub_tab1, sub_tab2 = st.tabs(["📊 TRADE LEDGER ROWS", "💸 CASHFLOW TRANSACTIONS"])
    
    with sub_tab1:
        st.markdown("<p style='font-size:11px; font-family:monospace; color:#90A4AE;'>TRANSMIT SYSTEM TRADE POSITIONS</p>", unsafe_allow_html=True)
        col_l1, col_l2 = st.columns(2)
        with col_l1:
            log_action = st.selectbox("EXECUTE STRATEGY ACTION:", ["BUY / LONG", "SELL / SHORT"], key="trade_action_sel")
        with col_l2:
            log_price = st.number_input("VERIFY ENTRY PRICE VALUE:", value=float(price), format="%.4f", key="trade_price_input")
            
        if st.button("🚀 TRANSMIT TRADE TO CODES PACK", key="btn_submit_trade"):
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
        if st.session_state["journal_db"].empty:
            st.info("⏳ Trade position matrix database is currently clear.")
        else:
            st.dataframe(st.session_state["journal_db"], use_container_width=True)
            if st.button("⚠️ ERASE POSITION JOURNAL ROW DATA", key="btn_clear_trades"):
                clear_callback()
                st.rerun()
                
    with sub_tab2:
        st.markdown("<p style='font-size:11px; font-family:monospace; color:#90A4AE;'>LOG DISCRETE SYSTEM DEPOSITS & CAPITAL WITHDRAWALS</p>", unsafe_allow_html=True)
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            cf_type = st.selectbox("CASHFLOW TYPE MATRIX:", ["DEPOSIT (+)", "WITHDRAWAL (-)"])
        with col_c2:
            cf_amount = st.number_input("CAPITAL QUANTITY VALUE:", min_value=0.0, value=100.0, step=50.0)
            
        if st.button("💸 TRANSMIT CASHFLOW TO SHIELDS VAULT", key="btn_submit_cf"):
            cf_sign = 1.0 if "DEPOSIT" in cf_type else -1.0
            new_cf_row = pd.DataFrame([{
                "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Type": cf_type,
                "Amount": cf_amount * cf_sign,
                "Currency": "ZAR" if "ZAR" in ig_display_name else "USD",
                "Status": "SETTLED LIQUID"
            }])
            st.session_state["cashflow_db"] = pd.concat([st.session_state["cashflow_db"], new_cf_row], ignore_index=True)
            st.session_state["cashflow_db"].to_csv("cashflow_vault.csv", index=False)
            st.success("💸 Cashflow token ledger update deployed successfully!")
            st.rerun()
            
        st.divider()
        st.markdown("#### 💳 SECURED ACCOUNT CASHFLOW BALANCE SYSTEM:")
        if st.session_state["cashflow_db"].empty:
            st.info("⏳ Capital transaction streams are currently clean.")
        else:
            st.dataframe(st.session_state["cashflow_db"], use_container_width=True)
            if st.button("⚠️ WIPEOUT GLOBAL TRANSACTION CASHFLOW CACHE", key="btn_clear_cf"):
                st.session_state["cashflow_db"] = pd.DataFrame(columns=["Timestamp", "Type", "Amount", "Currency", "Status"])
                st.session_state["cashflow_db"].to_csv("cashflow_vault.csv", index=False)
                st.rerun()
