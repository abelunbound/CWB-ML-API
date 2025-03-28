import dash
from dash import dcc, html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import math

# Initialize the Dash app
app = dash.Dash(__name__)

# Create the gauge chart function with capacity segments and custom needle
def create_capacity_gauge():
    # Define the capacity values
    max_capacity = 50  # Maximum reading (50GW)
    existing_capacity = 10  # Existing capacity (10GW)
    capacity_on_track = 20  # Capacity on track (20GW)
    total_existing_and_on_track = existing_capacity + capacity_on_track  # This equals 30GW
    current_value = total_existing_and_on_track  # The value to point at (30GW)
    
    # Calculate angles for the custom needle
    def get_angle(value, min_val=0, max_val=max_capacity):
        # Convert value to angle (0 to 180 degrees, where 0 is min and 180 is max)
        angle = 180 * (value - min_val) / (max_val - min_val)
        return angle

    # Create the gauge chart
    fig = go.Figure()

    # Create the gauge chart segments using a pie chart
    # Existing capacity (green)
    fig.add_trace(go.Pie(
        values=[existing_capacity, capacity_on_track, max_capacity - total_existing_and_on_track, max_capacity * 2],  # Last value creates the empty lower half
        rotation=90,
        hole=0.6,
        direction="clockwise",
        marker=dict(
            colors=["#1a9850", "#91cf60", "#e0e0e0", "rgba(0,0,0,0)"]  # Green, Light green, Grey, Transparent
        ),
        textinfo="none",
        showlegend=False,
        domain=dict(x=[0, 1], y=[0, 1]),
        hoverinfo="none"
    ))

    # Calculate the needle path
    needle_angle = get_angle(current_value)
    needle_angle_rad = math.radians(90 - needle_angle)
    
    # Center point coordinates
    center_x = 0.5
    center_y = 0.5
    
    # Needle length and width parameters
    needle_length = 0.35  # Length of the needle from center
    base_width = 0.02     # Width of the needle at the base
    
    # Calculate the needle tip position
    tip_x = center_x + needle_length * math.cos(needle_angle_rad)
    tip_y = center_y + needle_length * math.sin(needle_angle_rad)
    
    # Calculate points for the base of the needle (circle)
    base_radius = 0.03
    fig.add_shape(
        type="circle",
        x0=center_x - base_radius, 
        y0=center_y - base_radius,
        x1=center_x + base_radius, 
        y1=center_y + base_radius,
        fillcolor="#1e3048",
        line_color="#1e3048"
    )
    
    # Calculate points for the tapered needle
    # Calculate perpendicular direction for the base of the needle
    perp_angle_rad = needle_angle_rad + math.pi/2
    
    # Calculate the base corners of the needle
    base_left_x = center_x + base_width * math.cos(perp_angle_rad)
    base_left_y = center_y + base_width * math.sin(perp_angle_rad)
    
    base_right_x = center_x - base_width * math.cos(perp_angle_rad)
    base_right_y = center_y - base_width * math.sin(perp_angle_rad)
    
    # Add the needle shape
    fig.add_shape(
        type="path",
        path=f"M {base_left_x} {base_left_y} L {tip_x} {tip_y} L {base_right_x} {base_right_y} Z",
        fillcolor="#1e3048",
        line_color="#1e3048"
    )
    
    # Add tick marks and labels
    tick_values = [0, existing_capacity, total_existing_and_on_track, max_capacity]
    tick_labels = ["0", f"{existing_capacity} GW", f"{total_existing_and_on_track} GW", f"{max_capacity} GW"]
    
    for i, (value, label) in enumerate(zip(tick_values, tick_labels)):
        tick_angle = get_angle(value)
        tick_angle_rad = math.radians(90 - tick_angle)
        
        # Outer tick position
        outer_radius = 0.45
        tick_outer_x = center_x + outer_radius * math.cos(tick_angle_rad)
        tick_outer_y = center_y + outer_radius * math.sin(tick_angle_rad)
        
        # Inner tick position
        inner_radius = 0.4
        tick_inner_x = center_x + inner_radius * math.cos(tick_angle_rad)
        tick_inner_y = center_y + inner_radius * math.sin(tick_angle_rad)
        
        # Add tick mark
        fig.add_shape(
            type="line",
            x0=tick_inner_x,
            y0=tick_inner_y,
            x1=tick_outer_x,
            y1=tick_outer_y,
            line=dict(color="#2c3e50", width=2)
        )
        
        # Label position
        label_radius = 0.49
        label_x = center_x + label_radius * math.cos(tick_angle_rad)
        label_y = center_y + label_radius * math.sin(tick_angle_rad)
        
        # Add label
        fig.add_annotation(
            x=label_x,
            y=label_y,
            text=label,
            showarrow=False,
            font=dict(color="#2c3e50", size=12),
            xanchor="center" if tick_angle == 90 else "left" if tick_angle < 90 else "right",
            yanchor="middle"
        )
    
    # Add gauge title
    fig.add_annotation(
        x=0.5,
        y=0.7,
        text="Energy Capacity",
        showarrow=False,
        font=dict(color="#2c3e50", size=24),
        xanchor="center",
        yanchor="middle"
    )
    
    # Add current value display
    fig.add_annotation(
        x=0.5,
        y=0.4,
        text=f"{current_value} GW",
        showarrow=False,
        font=dict(color="#2c3e50", size=28, family="Arial Black"),
        xanchor="center",
        yanchor="middle"
    )
    
    # Update layout for a professional look
    fig.update_layout(
        showlegend=False,
        paper_bgcolor="white",
        plot_bgcolor="white",
        height=450,
        width=700,
        margin=dict(l=40, r=40, t=80, b=40),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-0.2, 1.2]
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-0.1, 1.1]
        ),
        title={
            "text": "Energy Capacity Progress",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 26, "color": "#2c3e50"}
        }
    )
    
    return fig

# Define the app layout
app.layout = html.Div(
    style={
        "maxWidth": "900px",
        "margin": "0 auto",
        "padding": "20px",
        "backgroundColor": "#f8f9fa",
        "borderRadius": "10px",
        "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)"
    },
    children=[
        html.H1(
            "Energy Capacity Tracker",
            style={"textAlign": "center", "color": "#2c3e50", "marginBottom": "20px"}
        ),
        html.Div(
            dcc.Graph(
                id="capacity-gauge-chart",
                figure=create_capacity_gauge(),
                config={"displayModeBar": False}
            ),
            style={"backgroundColor": "white", "padding": "15px", "borderRadius": "5px"}
        ),
        html.Div(
            [
                html.Div([
                    html.Div(style={"backgroundColor": "#1a9850", "width": "20px", "height": "20px", "display": "inline-block", "marginRight": "10px"}),
                    html.Span("Existing Capacity: 10 GW", style={"color": "#2c3e50"})
                ], style={"marginBottom": "10px"}),
                html.Div([
                    html.Div(style={"backgroundColor": "#91cf60", "width": "20px", "height": "20px", "display": "inline-block", "marginRight": "10px"}),
                    html.Span("Capacity on Track: 20 GW", style={"color": "#2c3e50"})
                ], style={"marginBottom": "10px"}),
                html.Div([
                    html.Div(style={"backgroundColor": "#e0e0e0", "width": "20px", "height": "20px", "display": "inline-block", "marginRight": "10px"}),
                    html.Span("Delivery Gap: 20 GW", style={"color": "#2c3e50"})
                ]),
                html.H4(
                    "Current Progress: 30 GW / 50 GW (60%)", 
                    style={"color": "#2c3e50", "textAlign": "center", "marginTop": "20px"}
                ),
                html.P(
                    "Last update: March 9, 2025",
                    style={"color": "#7f8c8d", "textAlign": "center", "fontSize": "0.9em"}
                )
            ],
            style={"marginTop": "20px", "textAlign": "center"}
        )
    ]
)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)