import streamlit as st
import pandas as pd
import numpy as np

def render_journal_tab(target_asset, ig_display_name, price):
    st.markdown("#### 🕹️ Quantitative Ledger Desk & Cashflow Command")
    st.divider()

    # 🧾 AUTOMATED BALANCE HEADERS RIGHT AT THE TOP
    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1: st.metric("💵 Total Capital Funds (ZAR)", f"R{st.session_state.live_balance:.2f}")
    with col_b2: st.metric("🛡️ Strict 2% Position Limit", f"R{(st.session_state.live_balance * 0.02):.2f}")
    with col_b3: st.metric("🛸 Funding Milestone Target", "R1000.00", f"{((st.session_state.live_balance / 1000.0) * 100):.1f}% Met")
        
    st.divider()
    
    # 🎛️ TWO INDEPENDENT WORKSPACE COLUMNS
    col_entry, col_summary = st.columns([1.2, 1.0])
    
    with col_entry:
        st.markdown("<p style='font-size:12px; font-weight:bold; color:#90A4AE; letter-spacing:0.5px;'>📝 RECORD RAW SETTLEMENT ENTRY:</p>", unsafe_allow_html=True)
        with st.form("ledger_input_form_v2"):
            form_asset = st.text_input("Asset Row:", value=ig_display_name)
            form_dir = st.selectbox("Execution Vector:", ["LONG BUY", "SHORT SELL"])
            
            # Manual cash flow inputs
            form_cashin = st.number_input("Manual Cash Inflow (ZAR profit):", min_value=0.0, value=0.0, step=10.0)
            form_cashout = st.number_input("Manual Cash Outflow (ZAR loss):", min_value=0.0, value=0.0, step=10.0)
            
            form_entry = st.number_input("Execution Entry Floor Price:", value=float(price) if price > 0 else 1.3355, format="%.5f")
            form_status = st.selectbox("Current State:", ["CLOSED SETTLED", "ACTIVE OPEN POSITION"])
            
            submit_btn = st.form_submit_button("💾 DISPATCH TRANSACTION TO ACTIVE LEDGER")
            
            if submit_btn:
                # Automated computation of net profit or loss
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
                st.toast("Cashflows successfully computed and added to master logs!")
                st.rerun()

    with col_summary:
        st.markdown("<p style='font-size:12px; font-weight:bold; color:#90A4AE; letter-spacing:0.5px;'>📊 AUTOMATED BALANCES & RUNTIME PERFORMANCE SUMMARY:</p>", unsafe_allow_html=True)
        
        if st.session_state.journal_db.empty:
            st.info("No transaction sequences logged on the master spreadsheet database for this operational tracking cycle.")
        else:
            # Complete automated calculations
            total_cashin = st.session_state.journal_db["Cash In (R)"].sum()
            total_cashout = st.session_state.journal_db["Cash Out (R)"].sum()
            daily_net_change = total_cashin - total_cashout
            
            win_rows = st.session_state.journal_db[st.session_state.journal_db["Net P&L (ZAR)"] > 0]
            total_trades = len(st.session_state.journal_db)
            win_ratio = (len(win_rows) / total_trades * 100) if total_trades > 0 else 0.0
            
            with st.container():
                st.markdown(f"**Net Change for Session:** `R{daily_net_change:+.2f}`")
                st.markdown(f"**Gross Accumulated Cash Inflows:** `R{total_cashin:.2f}`")
                st.markdown(f"**Gross Accumulated Cash Outflows:** `R{total_cashout:.2f}`")
                st.markdown(f"**Win Rate Multiplier:** `{win_ratio:.1f}%` successful settlements")
                st.divider()
                
                # 👽 MATHEMATICAL SPEED ANALYSIS STATEMENT RUNNER
                if daily_net_change > 0:
                    st.success(f"🚀 **VELOCITY OUTCOME:** Income velocity is compounding efficiently. The ledger is expanding at **{win_ratio:.1f}% win efficiency**. Risk management frameworks are safely containing downside outliers.")
                elif daily_net_change < 0:
                    st.error(f"📉 **VELOCITY OUTCOME:** Cashflow velocity indicates net draw down pressure. Current loss vectors outpace inflows. Re-align execution profiles to preserve capital parameters.")
                else:
                    st.warning("⏳ **VELOCITY OUTCOME:** Neutral equilibrium reached. Inflows match outflows down to the integer. Capital structure has stayed perfectly flat.")

    # MASTER SPREADSHEET LEDGER CONTAINER
    if not st.session_state.journal_db.empty:
        st.divider()
        st.markdown("##### 📁 Master Transaction Sequence Table Database")
        st.dataframe(st.session_state.journal_db, use_container_width=True)
        if st.button("🗑️ PURGE MASTER LEDGER DATA RECORDS"):
            st.session_state.journal_db = pd.DataFrame(columns=["Asset", "Action", "Cash In (R)", "Cash Out (R)", "Net P&L (ZAR)", "Entry Price", "Win/Loss %", "Status"])
            st.session_state.live_balance = 500.0
            st.rerun()
