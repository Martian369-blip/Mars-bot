import plotly.graph_objects as go

def generate_candlestick_chart(plot_df):
    """
    Sovereign Dark-Matrix Candlestick Core Engine.
    Generates high-density, custom-styled financial charts matching
    the terminal's signature cyber-purple aesthetic framework.
    """
    fig = go.Figure()
    
    # 🕯️ Neon color schema layout configurations
    increasing_color = '#00E676'  # High-visibility neon green
    decreasing_color = '#FF1744'  # High-visibility neon red
    
    # Inject primary candlestick telemetry stream data array
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
    
    # 🌌 Premium workspace layout optimization
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',   # Complete alpha transparent blend
        plot_bgcolor='rgba(0,0,0,0)',    # Seamless alignment with page theme
        xaxis_rangeslider_visible=False, # Erase messy range sliders
        height=380,                     # Expanded high-density viewing frame
        margin=dict(l=10, r=10, t=10, b=10),
        
        # 🧭 Deep-purple coordinate plane axis styling
        xaxis=dict(
            gridcolor='#1A103C',         # Custom grid lines matching layout style
            showgrid=True,
            linecolor='#2D1B6B',
            tickfont=dict(color='#90A4AE', size=10, family='monospace')
        ),
        yaxis=dict(
            gridcolor='#1A103C',         # Custom grid lines matching layout style
            showgrid=True,
            linecolor='#2D1B6B',
            side='right',                # Institutional right-side value tracker layout
            tickfont=dict(color='#90A4AE', size=10, family='monospace')
        )
    )
    
    return fig
