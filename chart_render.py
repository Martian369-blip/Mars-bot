import plotly.graph_objects as go

def generate_candlestick_chart(plot_df):
    """
    Institutional Candlestick Core Engine V2.
    Overlays live terminal execution lines and structural color-coded 
    quant matrix signal bands directly across the candlestick vector array.
    """
    fig = go.Figure()
    
    # 🕯️ Neon color schema layout configurations
    increasing_color = '#00E676'  # High-visibility neon green
    decreasing_color = '#FF1744'  # High-visibility neon red
    
    # Extract live session parameters from data vectors
    if not plot_df.empty:
        live_spot_price = plot_df['Close'].iloc[-1]
        start_time = plot_df.index[0]
        end_time = plot_df.index[-1]
    else:
        live_spot_price = 0.0
        start_time = None
        end_time = None

    # 1. 🕯️ Inject primary candlestick telemetry stream trace
    fig.add_trace(go.Candlestick(
        x=plot_df.index,
        open=plot_df['Open'],
        high=plot_df['High'],
        low=plot_df['Low'],
        close=plot_df['Close'],
        name="Price Matrix",
        increasing_line_color=increasing_color,
        decreasing_line_color=decreasing_color,
        increasing_fillcolor=increasing_color,
        decreasing_fillcolor=decreasing_color,
        line_width=1.5
    ))
    
    # 2. ⚡ Inject live spot price horizontal trace marker line
    if live_spot_price > 0:
        fig.add_shape(
            type="line",
            x0=start_time,
            x1=end_time,
            y0=live_spot_price,
            y1=live_spot_price,
            line=dict(
                color="#00E5FF",      # Cyber neon cyan tracker line
                width=1.5,
                dash="dashdot"         # Institutional tracing dash structure
            )
        )
        
        # Add dynamic live floating HUD value label block on the price side
        fig.add_annotation(
            x=end_time,
            y=live_spot_price,
            text=f" LIVE: {live_spot_price:.4f}",
            showarrow=False,
            xanchor="left",
            yanchor="middle",
            font=dict(color="#00E5FF", size=10, family="monospace"),
            bgcolor="rgba(17, 9, 36, 0.85)",
            bordercolor="#00E5FF",
            borderwidth=1,
            borderpad=3
        )

    # 🌌 Premium workspace layout optimization
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',   # Complete alpha transparent blend
        plot_bgcolor='rgba(0,0,0,0)',    # Seamless alignment with page theme
        xaxis_rangeslider_visible=False, # Erase messy range sliders
        height=380,                     # Expanded high-density viewing frame
        margin=dict(l=10, r=80, t=10, b=10), # Extra right margin padding for HUD labels
        showlegend=False,
        
        # 🧭 Deep-purple coordinate plane axis styling
        xaxis=dict(
            gridcolor='#1A103C',         # Muted grid accent tint
            showgrid=True,
            linecolor='#2D1B6B',
            tickfont=dict(color='#90A4AE', size=10, family='monospace')
        ),
        yaxis=dict(
            gridcolor='#1A103C',         # Muted grid accent tint
            showgrid=True,
            linecolor='#2D1B6B',
            side='right',                # Institutional right-side value tracker layout
            tickfont=dict(color='#90A4AE', size=10, family='monospace')
        )
    )
    
    return fig
