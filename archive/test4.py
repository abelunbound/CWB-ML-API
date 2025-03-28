import dash
from dash import dcc, html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import math

# Initialize the Dash app
app = dash.Dash(__name__)

# Create the gauge chart function with custom needle
def create_gauge():
    # Create subplot with 1 row and 2 columns (we'll only use the first column for now)
    fig = make_subplots(
        rows=1, 
        cols=2,
        specs=[[{"type": "indicator"}, {"type": "indicator"}]],
        horizontal_spacing=0.1
    )
    
    # Define color scales for the gauges
    colors1 = ["#1a9850", "#91cf60", "#d9ef8b", "#fee08b", "#fc8d59", "#d73027"]
    
    # The current value should have the needle pointing at it
    current_value = 270
    max_value = 500
    
    # Add the first gauge (without needle - we'll add a custom one)
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=current_value,
            number={"suffix": "°", "font": {"size": 24, "color": "#2c3e50"}},
            title={"text": "Temperature", "font": {"size": 24, "color": "#2c3e50"}},
            gauge={
                "axis": {"range": [None, max_value], "tickwidth": 1, "tickcolor": "#2c3e50"},
                "bar": {"color": "rgba(0,0,0,0)"},  # Make the default bar transparent
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor": "#ccc",
                "steps": [
                    {"range": [0, 100], "color": colors1[0]},
                    {"range": [100, 200], "color": colors1[1]},
                    {"range": [200, 300], "color": colors1[2]},
                    {"range": [300, 400], "color": colors1[3]},
                    {"range": [400, 500], "color": colors1[4]}
                ],
                "threshold": {
                    "line": {"color": "rgba(0,0,0,0)"},  # Make the threshold line invisible
                    "thickness": 0,
                    "value": current_value
                }
            }
        ),
        row=1, col=1
    )
    
    # Calculate positions for the custom needle
    # The gauge in Plotly is positioned in the first column
    gauge_center_x = 0.25  # Center x-position of the gauge
    gauge_center_y = 0.5   # Center y-position of the gauge (middle of the chart)
    
    # Find the exact position for the value 270 on the gauge
    # The gauge typically goes from about 0.05 to 0.45 in x-coordinates
    gauge_start_x = 0.05
    gauge_end_x = 0.45
    gauge_width = gauge_end_x - gauge_start_x
    
    # Calculate the position for value 270 (54% of 500)
    value_position_x = gauge_start_x + ((current_value / max_value) * gauge_width)
    
    # The pointer will go from the center to this position
    # For a half-circle gauge, we need to calculate the y-position as well
    # We'll use a radius to determine how far up from the center the point is
    gauge_radius = 0.2
    
    # Calculate the tip position of the needle to directly point at the 270 mark
    # For a value of 270/500, this should be at about x=0.266 on the gauge arc
    needle_length = gauge_radius * 0.85  # Make the needle about 85% of the gauge radius
    
    # We'll use the percentage directly to find the position on the arc
    percent_of_gauge = current_value / max_value
    
    # For a semicircular gauge, the angle goes from 180° (left) to 0° (right)
    # Convert to radians and use standard trig functions
    arc_angle_rad = math.pi * (1 - percent_of_gauge)
    
    # Calculate the tip position using this angle
    tip_x = gauge_center_x + needle_length * math.cos(arc_angle_rad)
    tip_y = gauge_center_y - needle_length * math.sin(arc_angle_rad)  # Negative because y increases downward in browser coordinates
    
    # Calculate points for the base of the needle (to create a tapered shape)
    base_width = 0.015  # Width of the base of the needle
    
    # Fix the base points on the center line
    base_left_x = gauge_center_x + base_width
    base_left_y = gauge_center_y
    
    base_right_x = gauge_center_x - base_width
    base_right_y = gauge_center_y
    
    # Add the needle shape (triangular path)
    fig.add_shape(
        type="path",
        path=f"M {base_left_x} {base_left_y} L {tip_x} {tip_y} L {base_right_x} {base_right_y} Z",
        fillcolor="#1e3048",  # Dark blue/black color similar to the reference
        line_color="#1e3048",
        line_width=1,
        layer="above"
    )
    
    # Add the circular base of the needle - positioned exactly at the center
    base_radius = 0.015
    fig.add_shape(
        type="circle",
        x0=gauge_center_x - base_radius,
        y0=gauge_center_y - base_radius,
        x1=gauge_center_x + base_radius,
        y1=gauge_center_y + base_radius,
        fillcolor="#1e3048",
        line_color="#1e3048",
        layer="above"
    )
    
    # Update layout for a professional look
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font={"color": "#2c3e50", "family": "Arial"},
        height=450,
        margin=dict(l=40, r=40, t=80, b=40),
        title={
            "text": "Gauge Chart Dashboard",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 28, "color": "#2c3e50"}
        }
    )
    
    return fig

# Define the app layout
app.layout = html.Div(
    style={
        "maxWidth": "1000px",
        "margin": "0 auto",
        "padding": "20px",
        "backgroundColor": "#f8f9fa",
        "borderRadius": "10px",
        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)"
    },
    children=[
        html.H1(
            "Gauge System Monitor",
            style={"textAlign": "center", "color": "#2c3e50", "marginBottom": "20px"}
        ),
        html.Div(
            dcc.Graph(
                id="gauge-chart",
                figure=create_gauge(),
                config={"displayModeBar": False}
            ),
            style={"backgroundColor": "white", "padding": "15px", "borderRadius": "5px"}
        ),
        html.Div(
            [
                html.H4("System Status: Normal", style={"color": "#27ae60", "textAlign": "center"}),
                html.P(
                    "Last update: March 9, 2025 - 08:42 AM",
                    style={"color": "#7f8c8d", "textAlign": "center", "fontSize": "0.9em"}
                )
            ],
            style={"marginTop": "20px"}
        )
    ]
)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, port=8051)