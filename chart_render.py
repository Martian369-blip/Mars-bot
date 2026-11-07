import plotly.graph_objects as go

def generate_candlestick_chart(plot_df):
    """
    Autonomous Graphic Telemetry Render Pipeline
    Generates a mathematically perfect, fully closed dark matrix candlestick chart.
    """
    fig = go.Figure()
    
    # Fully enclosed trace calculation matrix
    fig.add_trace(
        go.Candlestick(
            x=plot_df.index,
            open=plot_df['Open'],
            high=plot_df['High'],
            low=plot_df['Low'],
            close=plot_df['Close'],
            name="Market",
            increasing_line_color='#4CAF50',
            decreasing_line_color='#B71C1C',
            increasing_fillcolor='#1B5E20',
            decreasing_fillcolor='#7F0000'
        )
    )
    
    # Saturated space matrix display constraints
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='#110924',
        xaxis_rangeslider_visible=False,
        height=340,
        margin=dict(l=10, r=10, t=15, b=10),
        xaxis=dict(gridcolor='#1E1435', showgrid=True),
        yaxis=dict(gridcolor='#1E1435', showgrid=True)
    )
    
    return fig
