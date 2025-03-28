import dash
from dash import dcc, html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Initialize the Dash app
app = dash.Dash(__name__)

# Create the dual gauge chart function
def create_dual_gauge():
    # Create subplot with 1 row and 2 columns
    fig = make_subplots(
        rows=1, 
        cols=2,
        specs=[[{"type": "indicator"}, {"type": "indicator"}]],
        horizontal_spacing=0.1
    )
    
    # Define color scales for the gauges
    colors1 = ["#1a9850", "#91cf60", "#d9ef8b", "#fee08b", "#fc8d59", "#d73027"]
    colors2 = ["#4575b4", "#74add1", "#abd9e9", "#e0f3f8", "#fee090", "#fdae61"]
    
    # Add the first gauge
    fig.add_trace(
        go.Indicator(
            mode="gauge+number+delta",
            value=30,
            title={"text": "Temperature", "font": {"size": 24, "color": "#2c3e50"}},
            delta={"reference": 20, "increasing": {"color": "#d73027"}},
            gauge={
                "axis": {"range": [None, 50], "tickwidth": 1, "tickcolor": "#2c3e50"},
                "bar": {"color": "rgba(0,0,0,0)"},
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor": "#ccc",
                "steps": [
                    {"range": [0, 10], "color": colors1[0]},
                    {"range": [10, 30], "color": colors1[1]},
                    {"range": [30, 50], "color": colors1[2]},
                    # {"range": [300, 400], "color": colors1[3]},
                    # {"range": [400, 500], "color": colors1[4]}
                ],
                # "threshold": {
                #     "line": {"color": "#d62728", "width": 4},
                #     "thickness": 1,
                #     "value": 450
                # }
            }
        ),
        row=1, col=1
    )
    
    # Add the second gauge
    fig.add_trace(
        go.Indicator(
            mode="gauge+number+delta",
            value=78,
            title={"text": "Pressure", "font": {"size": 24, "color": "#2c3e50"}},
            delta={"reference": 80, "decreasing": {"color": "#4575b4"}},
            gauge={
                "axis": {"range": [None, 100], "tickwidth": 1, "tickcolor": "#2c3e50"},
                "bar": {"color": "#2c3e50"},
                "bgcolor": "white",
                "borderwidth": 2,
                "bordercolor": "#ccc",
                "steps": [
                    {"range": [0, 20], "color": colors2[0]},
                    {"range": [20, 40], "color": colors2[1]},
                    {"range": [40, 60], "color": colors2[2]},
                    {"range": [60, 80], "color": colors2[3]},
                    {"range": [80, 100], "color": colors2[4]}
                ],
                "threshold": {
                    "line": {"color": "#4575b4", "width": 4},
                    "thickness": 0.75,
                    "value": 90
                }
            }
        ),
        row=1, col=2
    )
    
    # Update layout for a professional look
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font={"color": "#2c3e50", "family": "Arial"},
        height=450,
        margin=dict(l=40, r=40, t=80, b=40),
        title={
            "text": "Dual Gauge Chart Dashboard",
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
            "Dual Gauge System Monitor",
            style={"textAlign": "center", "color": "#2c3e50", "marginBottom": "20px"}
        ),
        html.Div(
            dcc.Graph(
                id="dual-gauge-chart",
                figure=create_dual_gauge(),
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
    app.run_server(debug=True, port=8050)