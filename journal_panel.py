import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def render_journal_tab(target_asset, ig_display_name, price):
    st.markdown("#### 🕹️ Quantitative Ledger Desk & Risk Control Engine")
    st.divider()

    # 🧾 1. APP RECONCILIATION LAYER (MANUAL CAPITAL OVERRIDE RIGHT AT TOP)
    st.markdown("<p style='font-size:12px; font-weight:bold; color:#90A4AE; letter-spacing:0.5px;'>🏦 APP RECONCILIATION CONTROL LAYER:</p>", unsafe_allow_html=True)
    
    manual_balance = st.number_input("💵 Sync Live Trading App Balance (ZAR):", min_value=1.0, value=float(st.session_state.live_balance), step=50.0)
    st.session_state.live_balance = manual_balance

    risk_allowance_2pct = st.session_state.live_balance * 0.02

    col_b1, col_b2, col_b3 = st.columns(3)
    with col_b1: st.metric("💵 Verified Capital Funds", f"R{st.session_state.live_balance:.2f}")
    with col_b2: st.metric("🛡️ Strict 2% Position Limit", f"R{risk_allowance_2pct:.2f}")
    with col_b3: st.metric("🛸 Funding Milestone Target", "R1000.00", f"{((st.session_state.live_balance / 1000.0) * 100):.1f}% Met")
        
    st.divider()
    
    # 🎛️ TWO-COLUMN ACTION WORKSPACE
    col_entry, col_summary = st.columns([1.2, 1.0])
    
    with col_entry:
        st.markdown("<p style='font-size:12px; font-weight:bold; color:#90A4AE; letter-spacing:0.5px;'>📝 RISK ESTIMATION & TRANSACTION TICKET:</p>", unsafe_allow_html=True)
        
        # 🧮 UPGRADE 1: DYNAMIC POSITION SIZE CALCULATOR INSIDE ENTRY PANEL
        with st.expander("🧮 LIVE IG CONTRACT LOT SIZE CALCULATOR", expanded=True):
            stop_distance_pts = st.number_input("Stop Loss Distance (In Points / Pips):", min_value=1.0, value=20.0, step=1.0)
            point_value_zar = st.number_input("ZAR Value Per Point (1 standard lot value):", min_value=0.1, value=10.0, step=0.5)
            
            # Mathematical calculation of contract fraction size needed to equal max 2% loss
            max_recommended_lots = risk_allowance_2pct / (stop_distance_pts * point_value_zar) if (stop_distance_pts * point_value_zar) > 0 else 0.01
            st.info(f"🛸 **Recommended Execution Size:** `{max_recommended_lots:.3f} Lots` to limit risk strictly to R{risk_allowance_2pct:.2f}.")

        with st.form("ledger_input_form_v4"):
            form_asset = st.text_input("Asset Row:", value=ig_display_name)
            form_dir = st.selectbox("Execution Vector:", ["LONG BUY", "SHORT SELL"])
            
            form_cashin = st.number_input("Manual Cash Inflow (ZAR Gross Profit):", min_value=0.0, value=0.0, step=10.0)
            form_cashout = st.number_input("Manual Cash Outflow (ZAR Gross Loss):", min_value=0.0, value=0.0, step=10.0)
            
            form_entry = st.number_input("Execution Entry Floor Price:", value=float(price) if price > 0 else 1.3355, format="%.5f")
            form_status = st.selectbox("Current State:", ["CLOSED SETTLED", "ACTIVE OPEN POSITION"])
            
            submit_btn = st.form_submit_button("AFFECT SPREADSHEET CASHFLOWS")
            
            if submit_btn:
                # 🛡️ UPGRADE 2: RULE BREAKER GUARDRAIL PROTOCOL BLOCK
                if form_cashout > risk_allowance_2pct:
                    st.error(f"🚨 **RISK PARAMETERS VIOLATED:** Your input loss of R{form_cashout:.2f} breaks your strict 2% protective allowance limit of R{risk_allowance_2pct:.2f}! Trade rejected by rule breaker guardrail.")
                else:
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
        st.markdown("<p style='font-size:12px; font-weight:bold; color:#90A4AE; letter-spacing:0.5px;'>📊 HARMONIZED ANALYTICS SUMMARY:</p>", unsafe_allow_html=True)
        
        if st.session_state.journal_db.empty:
            st.info("No active ledger rows recorded. Enter transactions on left vector form to boot curves.")
        else:
            total_cashin = st.session_state.journal_db["Cash In (R)"].sum()
            total_cashout = st.session_state.journal_db["Cash Out (R)"].sum()
            daily_net_change = total_cashin - total_cashout
            
            win_rows = st.session_state.journal_db[st.session_state.journal_db["Net P&L (ZAR)"] > 0]
            loss_rows = st.session_state.journal_db[st.session_state.journal_db["Net P&L (ZAR)"] < 0]
            total_trades = len(st.session_state.journal_db)
            win_ratio = (len(win_rows) / total_trades * 100) if total_trades > 0 else 0.0
            
            # 📈 UPGRADE 3: ADVANCED PERFORMANCE METRICS PANEL BLOCK
            avg_win = win_rows["Net P&L (ZAR)"].mean() if not win_rows.empty else 0.0
            avg_loss = abs(loss_rows["Net P&L (ZAR)"].mean()) if not loss_rows.empty else 0.0
            profit_factor = total_cashin / total_cashout if total_cashout > 0 else total_cashin
            
            with st.container():
                st.markdown(f"**Session Net Outcome:** `R{daily_net_change:+.2f}`")
                st.markdown(f"**Win Efficiency Multiplier:** `{win_ratio:.1f}%` successful settlements")
                st.markdown(f"**System Profit Factor:** `{profit_factor:.2f}x` factor performance")
                st.markdown(f"**Avg Win / Loss Size:** `R{avg_win:.2f}` / `R{avg_loss:.2f}`")
                st.divider()
                
                if daily_net_change > 0:
                    st.success(f"🚀 **VELOCITY:** Net income compounding effectively. Capital base expanding at **{win_ratio:.1f}% efficiency**. Speed of cash generation outpaces leakage.")
                elif daily_net_change < 0:
                    st.error(f"📉 **VELOCITY:** Drawdown momentum present. Speed of leakage outpaces inflows. Review execution parameters to defend remaining funds.")
                else:
                    st.warning("⏳ **VELOCITY:** Station equilibrium. Inflows match outflows down to the integer. Flat session profile.")

    # 📈 UPGRADE 3 PART B: ROLLING EQUITY CURVE CHART PLOTTER
    if not st.session_state.journal_db.empty:
        st.divider()
        st.markdown("<p style='font-size:13px; font-weight:bold; letter-spacing:0.5px; color:#90A4AE;'>📈 CONTINUOUS SESSION EQUITY CURVE TRACKING GRAPH</p>", unsafe_allow_html=True)
        
        # Calculate rolling wealth curve starting from base balance minus recent pnl sum up increments
        starting_capital_node = st.session_state.live_balance - st.session_state.journal_db["Net P&L (ZAR)"].sum()
        pnl_array = st.session_state.journal_db["Net P&L (ZAR)"].tolist()
        equity_curve_points = [starting_capital_node]
        for trade_return in pnl_array:
            equity_curve_points.append(equity_curve_points[-1] + trade_return)
            
        fig_equity = go.Figure()
        fig_equity.add_trace(go.Scatter(
            x=list(range(len(equity_curve_points))), 
            y=equity_curve_points, 
            mode='lines+markers',
            name='Capital (ZAR)',
            line=dict(color='#00A4E4', width=2),
            marker=dict(size=6, color='#FFFFFF', line=dict(color='#00A4E4', width=1.5))
        ))
        fig_equity.update_layout(
            template="plotly_dark", 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='#161A1E', 
            height=260, 
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(title="Transaction Event Count Sequence", showgrid=False),
            yaxis=dict(title="Account Balance Value (R)", showgrid=True, gridcolor='#23292F')
        )
        st.plotly_chart(fig_equity, use_container_width=True)

        st.divider()
        st.markdown("##### 📁 Master Transaction Sequence Table Database")
        st.dataframe(st.session_state.journal_db, use_container_width=True)
        if st.button("🗑️ PURGE MASTER LEDGER DATA RECORDS"):
            st.session_state.journal_db = pd.DataFrame(columns=["Asset", "Action", "Cash In (R)", "Cash Out (R)", "Net P&L (ZAR)", "Entry Price", "Win/Loss %", "Status"])
            st.session_state.live_balance = 500.0
            st.rerun()
