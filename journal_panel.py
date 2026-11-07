import streamlit as st
import pandas as pd
import numpy as np

def render_journal_tab(target_asset, ig_display_name, price):
    st.markdown("#### 🕹️ Quantitative Ledger Desk & Reconciliation Center")
    st.divider()

    # 🧾 AUTOMATED & MANUAL BALANCE RECONCILIATION HEADERS
    st.markdown("<p style='font-size:12px; font-weight:bold; color:#90A4AE; letter-spacing:0.5px;'>🏦 APP RECONCILIATION CONTROL LAYER:</p>", unsafe_allow_html=True)
    
    # Let the user manually set their absolute capital funds directly on screen
    manual_balance = st.number_input("💵 Sync Live Trading App Balance (ZAR):", min_value=1.0, value=float(st.session_state.live_balance), step=50.0)
    st.session_state.live_balance = manual_balance

    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1: st.metric("💵 Verified Capital Funds", f"R{st.session_state.live_balance:.2f}")
    with col_b2: st.metric("🛡️ Strict 2% Position Limit", f"R{(st.session_state.live_balance * 0.02):.2f}")
    with col_b3: st.metric("🛸 Funding Milestone Target", "R1000.00", f"{((st.session_state.live_balance / 1000.0) * 100):.1f}% Met")
        
    st.divider()
    
    col_entry, col_summary = st.columns([1.2, 1.0])
    
    with col_entry:
        st.markdown("<p style='font-size:12px; font-weight:bold; color:#90A4AE; letter-spacing:0.5px;'>📝 DISPATCH RECENT TRANSACTION:</p>", unsafe_allow_html=True)
        with st.form("ledger_input_form_v3"):
            form_asset = st.text_input("Asset Row:", value=ig_display_name)
            form_dir = st.selectbox("Execution Vector:", ["LONG BUY", "SHORT SELL"])
            
            # Manual cash flow boxes requested by user
            form_cashin = st.number_input("Manual Cash Inflow (ZAR Gross Profit):", min_value=0.0, value=0.0, step=10.0)
            form_cashout = st.number_input("Manual Cash Outflow (ZAR Gross Loss):", min_value=0.0, value=0.0, step=10.0)
            
            form_entry = st.number_input("Execution Entry Floor Price:", value=float(price) if price > 0 else 1.3355, format="%.5f")
            form_status = st.selectbox("Current State:", ["CLOSED SETTLED", "ACTIVE OPEN POSITION"])
            
            submit_btn = st.form_submit_button("AFFECT SPREADSHEET CASHFLOWS")
            
            if submit_btn:
                # Automated computation of net profit/loss and tracking percentages
                net_pnl = form_cashin - form_cashout
                pct_calc = (net_pnl / st.session_state.live_balance) * 100 if st.session_state.live_balance > 0 else 0.0
                
                new_row = {
                    "Asset": form_asset,
                    "Action": form_dir,
                    "Cash In (R)": form_cashin,
                    "Cash Out (R)": form_cashout,
                    "Net P&L (ZAR)": net_pnl,
                    "Entry Price": form_entry,
                    "Win/Loss %": round(pct_calc, 2),
                    "Status": form_status
                }
                
                st.session_state.journal_db = pd.concat([st.session_state.journal_db, pd.DataFrame([new_row])], ignore_index=True)
                st.session_state.live_balance += net_pnl
                st.toast("Cashflows successfully computed and added to logs!")
                st.rerun()

    with col_summary:
        st.markdown("<p style='font-size:12px; font-weight:bold; color:#90A4AE; letter-spacing:0.5px;'>📊 AUTOMATED HARMONIZED BALANCES:</p>", unsafe_allow_html=True)
        
        if st.session_state.journal_db.empty:
            st.info("No active ledger rows recorded.")
        else:
            total_cashin = st.session_state.journal_db["Cash In (R)"].sum()
            total_cashout = st.session_state.journal_db["Cash Out (R)"].sum()
            daily_net_change = total_cashin - total_cashout
            
            win_rows = st.session_state.journal_db[st.session_state.journal_db["Net P&L (ZAR)"] > 0]
            total_trades = len(st.session_state.journal_db)
            win_ratio = (len(win_rows) / total_trades * 100) if total_trades > 0 else 0.0
            
            with st.container():
                st.markdown(f"**Automated Summary for Day:** `R{daily_net_change:+.2f}`")
                st.markdown(f"**Gross Inflows:** `R{total_cashin:.2f}` | **Gross Outflows:** `R{total_cashout:.2f}`")
                st.markdown(f"**Win Efficiency Multiplier:** `{win_ratio:.1f}%` successful settlements")
                st.divider()
                
                if daily_net_change > 0:
                    st.success(f"🚀 **VELOCITY:** Net income compounding effectively. Capital base expanding at **{win_ratio:.1f}% efficiency**. Speed of cash generation outpaces losses.")
                elif daily_net_change < 0:
                    st.error(f"📉 **VELOCITY:** Drawdown momentum present. Speed of leakage outpaces inflows. Review execution parameters to defend remaining funds.")
                else:
                    st.warning("⏳ **VELOCITY:** Station equilibrium. Income generation matches loss parameters perfectly. Flat session profile.")

    if not st.session_state.journal_db.empty:
        st.divider()
        st.markdown("##### 📁 Master Transaction Sequence Table Database")
        st.dataframe(st.session_state.journal_db, use_container_width=True)
        if st.button("🗑️ PURGE MASTER LEDGER DATA RECORDS"):
            st.session_state.journal_db = pd.DataFrame(columns=["Asset", "Action", "Cash In (R)", "Cash Out (R)", "Net P&L (ZAR)", "Entry Price", "Win/Loss %", "Status"])
            st.session_state.live_balance = 500.0
            st.rerun()
