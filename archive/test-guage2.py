import dash
from dash import dcc, html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Initialize the Dash app
app = dash.Dash(__name__)

# Create the gauge chart function with capacity segments
def create_capacity_gauge():
    # Create subplot with 1 row and 1 column (single gauge)
    fig = make_subplots(
        rows=1, 
        cols=1,
        specs=[[{"type": "indicator"}]],
    )
    
    # Define the capacity values
    max_capacity = 50  # Maximum reading (50GW)
    existing_capacity = 10  # Existing capacity (10GW)
    capacity_on_track = 20  # Capacity on track (20GW)
    total_existing_and_on_track = existing_capacity + capacity_on_track  # This equals 30GW
    
    # Add the gauge
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=total_existing_and_on_track,  # Show the total of existing + on track (30GW)
            number={"suffix": " GW", "font": {"size": 26, "color": "#2c3e50"}},
            title={"text": "Energy Capacity", "font": {"size": 28, "color": "#2c3e50"}},
            gauge={
                "axis": {
                    "range": [None, max_capacity], 
                    "tickwidth": 1, 
                    "tickcolor": "#2c3e50",
                    "tickvals": [0, 10, 30, 50],  # Custom tick values to highlight the segments
                    "ticktext": ["0", "10 GW<br>Existing", "30 GW<br>On Track", "50 GW<br>Target"]
                },
                "bar": {"color": "rgba(0,0,0,0)"},  # Make the bar transparent
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor": "#ccc",
                "steps": [
                    # Existing capacity (green)
                    {"range": [0, existing_capacity], "color": "#1a9850"},
                    # Capacity on track (light green)
                    {"range": [existing_capacity, total_existing_and_on_track], "color": "#91cf60"},
                    # Delivery gap (grey)
                    {"range": [total_existing_and_on_track, max_capacity], "color": "#e0e0e0"}
                ],
                "threshold": {
                    "line": {"color": "#2c3e50", "width": 4},
                    "thickness": 0.75,
                    "value": total_existing_and_on_track  # This places the needle exactly at 30GW
                }
            }
        ),
        row=1, col=1
    )
    
    # Update layout for a professional look
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font={"color": "#2c3e50", "family": "Arial"},
        height=500,
        margin=dict(l=40, r=40, t=120, b=40),
        title={
            "text": "Energy Capacity Progress",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 32, "color": "#2c3e50"}
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