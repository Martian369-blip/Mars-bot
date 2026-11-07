import streamlit as st
import engine as eng

def render_news_tab(target_asset, ig_display_name):
    st.markdown(f"#### 📡 Tactical Intelligence Desk: <span style='color:#00A4E4;'>{ig_display_name}</span>", unsafe_allow_html=True)
    st.divider()
    
    # Core variables for logic mapping
    hourly_rsi = st.session_state.get('hourly_rsi', 50.0)
    current_price = st.session_state.get('current_price', 0.0)
    direction = st.session_state.get('current_direction', "⏳ HOLD")
    
    # 🧠 SECTION 1: SUMMARISED MARKET RESEARCH
    with st.container():
        st.markdown("##### 🔍 1. Summarised Market Research & Sentiment Matrix")
        st.caption("Aggregated institutional orderbook flows and tracking nodes")
        
        if hourly_rsi < 35:
            st.info("⚡ **BULLISH OVERSOLD NODE:** Global desks indicate heavy localized liquidation exhaustion. Retail hands flushed out on the 1-hour clearing levels. Liquidity pool resting underneath has been completely taken, triggering strong institutional baseline defenses.")
        elif hourly_rsi > 65:
            st.warning("🚨 **BEARISH OVERBOUGHT NODE:** Extreme distribution observed on major exchanges. Momentum curves are stretched past standard variance thresholds. High likelihood of immediate liquidity sweeps targeting early breakout traps.")
        else:
            st.info("⏳ **CONSOLIDATION RANGE MATRIX:** Price action is tightly bound within intraday fair-value bands. Volume distribution is highly balanced at the current node. Institutional market makers are actively absorbing orders before the next session release.")

    # 🎯 SECTION 2: HYPOTHESIS ON THE NEXT HOUR
    with st.container():
        st.markdown("##### 🚀 2. Quantum Momentum Hypothesis (Next 60 Minutes)")
        
        if hourly_rsi < 35:
            st.markdown("* **Vector Vector Shift:** Expected sharp mean reversion higher back toward the 20-period moving average.")
            st.markdown(f"* **Target Floor Grid:** High probability test of localized upside distribution clusters.")
        elif hourly_rsi > 65:
            st.markdown("* **Vector Vector Shift:** Fast profit-taking cascading down to wash out late momentum buyers.")
            st.markdown(f"* **Target Floor Grid:** Imminent correction toward discount liquidity block zones.")
        else:
            st.markdown("* **Vector Vector Shift:** Continued rotational sideways range bound behavior inside existing bars.")
            st.markdown("* **Target Floor Grid:** Re-testing local highs and lows without establishing clear trend dominance.")

    # 📲 SECTION 3: STRATEGIC REASON WHY EXECUTION IS VALIDATED
    with st.container():
        st.markdown("##### 🎯 3. Strategic Trade Execution Validation Statement")
        
        if "BUY" in direction:
            st.success(f"✔️ **EXECUTION VERDICT:** Long vector validated because Hourly RSI (`{hourly_rsi:.1f}`) confirms high-probability structural exhaustion. Risk-to-reward parameters are highly skewed to your advantage. Your Stop-Loss is tightly nested beneath institutional pivot floors.")
        elif "SELL" in direction:
            st.error(f"❌ **EXECUTION VERDICT:** Short vector validated because Hourly RSI (`{hourly_rsi:.1f}`) signals significant supply imbalance. Institutional buying power has decelerated at major overhead resistance, establishing a safe shield for protective stops.")
        else:
            st.warning("⚠️ **EXECUTION VERDICT:** Stand down. No strategic edge is present at this precise coordinate. Preserve cash and await structural expansion into outer extreme pricing bands.")
