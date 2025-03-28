import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use Agg backend for non-interactive plotting
import numpy as np
import base64
from io import BytesIO
from PIL import Image  # Added for image manipulation

def create_gauge_chart(existing_capacity=40, target_capacity=100, capacity_on_track=30):
    """
    Create a dial gauge chart showing capacity metrics.
    
    Parameters:
    -----------
    existing_capacity : int
        Current installed capacity value (default: 40)
    target_capacity : int
        Target capacity value (default: 100)
    capacity_on_track : int
        Additional capacity that is on track (default: 30)
    title : str
        Chart title (default: "Clean Power Progress")
    
    Returns:
    --------
    encoded_image : str
        Base64 encoded image
    """
    # Create the figure and polar subplot
    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_subplot(projection="polar")

    # Define the gauge and segment parameters
    capacity_on_track_segment = existing_capacity + capacity_on_track

    gauge_min = 0
    gauge_max = target_capacity
    gauge_range = gauge_max - gauge_min

    # Define segment boundaries
    segment_bounds = [gauge_min, existing_capacity, capacity_on_track_segment, target_capacity]
    segment_colors = ['#4575b4', '#74add1', 'lightgray']

    # Convert to radians for polar plot
    min_theta = np.pi  # Left (180 degrees)
    max_theta = 2*np.pi   # Right (360 degrees/0 degrees)
    theta_range = max_theta - min_theta

    # Current value for the dial
    current_value = capacity_on_track_segment
    
    # Calculate current angle
    current_theta = min_theta + (current_value - gauge_min) / gauge_range * theta_range

    # Create the colored segments and prepare for legend
    legend_patches = []
    legend_labels = ["Installed Capacity", "Capacity on Track", "Shortfall by 2030"]
    
    for i in range(len(segment_bounds) - 1):
        # Convert segment boundaries to angles
        start_theta = min_theta + (segment_bounds[i] - gauge_min) / gauge_range * theta_range
        end_theta = min_theta + (segment_bounds[i+1] - gauge_min) / gauge_range * theta_range
        
        # Generate points for the segment
        theta = np.linspace(start_theta, end_theta, 100)
        r = np.ones_like(theta) * 0.9  # Radius of the gauge
        
        # Plot the segment
        ax.fill_between(theta, 0.7, r, color=segment_colors[i], alpha=0.8)
        
        # Create patch for legend
        from matplotlib.patches import Patch
        legend_patches.append(Patch(facecolor=segment_colors[i], alpha=0.8, label=legend_labels[i]))
        
    # Add ticks only at segment boundaries
    for value in segment_bounds:
        tick_theta = min_theta + (value - gauge_min) / gauge_range * theta_range
        
        # Add tick labels at segment boundaries with bold font
        # Add "GW" beside 0 and 100
        if value == 0 or value == target_capacity:
            label_text = f'{value} GW'
        else:
            label_text = f'{value}'
            
        ax.text(tick_theta, 0.99, label_text, ha='center', va='center', 
                fontsize=12, fontweight='bold')

    # Add the arrow annotation
    ax.annotate(f'{current_value}', 
                xy=(current_theta, 0.6),  # Arrow tip (at current value)
                xytext=(min_theta + theta_range/2, 0),  # Arrow base (at center)
                arrowprops=dict(arrowstyle="wedge, tail_width=0.9",
                               color='black', 
                               lw=1,
                               shrinkA=0),
                bbox=dict(boxstyle='circle', facecolor='black', edgecolor='black', linewidth=4.0),
                )

    # Customize the plot appearance
    ax.grid(False)
    ax.set_yticks([])  # Remove radial ticks
    ax.set_theta_direction('clockwise')  # Clockwise direction
    ax.set_rlim(0, 0.9)  # Set radius limits
    
    # # Add the legend at the top
    ax.legend(handles=legend_patches, loc='upper center', bbox_to_anchor=(0.5, 1.15),
              ncol=3, frameon=False, fontsize=10)

    # ax.set_title(title, fontsize=18, pad=40)

    # Hide all unnecessary spines and tick labels
    ax.spines['polar'].set_visible(False)
    ax.set_xticklabels([])

    plt.tight_layout()
    
    # Convert the figure to a PNG image with proper cropping
    buf = BytesIO()
    # Set bbox_inches='tight' to remove extra white space around the plot
    # Set pad_inches=0 to remove padding around the figure
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1, dpi=300)
    buf.seek(0)
    
    # Since we're using an image, we can directly crop it to just the top half
    from PIL import Image
    img = Image.open(buf)
    width, height = img.size
    # Keep only the top 60% of the image (this can be adjusted)
    cropped_img = img.crop((0, 0, width, int(height * 0.6)))
    
    # Save cropped image to a new buffer
    cropped_buf = BytesIO()
    cropped_img.save(cropped_buf, format='PNG')
    cropped_buf.seek(0)
    
    plt.close(fig)  # Close the figure to free memory
    
    # Encode the cropped image to base64 string
    img_data = base64.b64encode(cropped_buf.getvalue()).decode('utf-8')
    return f'data:image/png;base64,{img_data}'

# Initialize the Dash app with Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # Needed for deployment

# App layout
app.layout = html.Div([
    dbc.Container([
        html.H1("Clean Energy Progress Dashboard", className="text-center my-4"),
        
        dbc.Row([
            # First gauge card
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H4("Clean Power Delivery Progress", className="text-center")),
                    dbc.CardBody([
                        html.Div([
                            html.Img(src=create_gauge_chart(40, 100, 30), 
                                     style={'width': '100%'})
                        ]),
                        html.P("Current solar deployment and projected capacity by 2030", 
                               className="text-center text-muted mt-3")
                    ])
                ], className="h-100 shadow", style={'border-radius': '10px'})
            ], md=6, className="mb-4"),
            
            # Second gauge card
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H4("Onshore Wind delivery progress", className="text-center")),
                    dbc.CardBody([
                        html.Div([
                            html.Img(src=create_gauge_chart(60, 120, 25), 
                                     style={'width': '100%'})
                        ]),
                        html.P("Current wind deployment and projected capacity by 2030", 
                               className="text-center text-muted mt-3")
                    ])
                ], className="h-100 shadow", style={'border-radius': '10px'})
            ], md=6, className="mb-4")
        ]),
        
        # Additional information row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("About This Dashboard", className="card-title"),
                        html.P([
                            "This dashboard visualizes the progress towards clean energy goals for 2030. ",
                            "The gauge charts show installed capacity (dark blue), capacity on track (light blue), ",
                            "and the remaining capacity needed to reach targets (light gray)."
                        ]),
                        html.P([
                            "Data is based on current deployment rates and projected installations. ",
                            "Updates are made quarterly based on the latest industry reports."
                        ])
                    ])
                ], className="shadow-sm")
            ], md=12)
        ], className="mt-3")
    ], fluid=True)
])

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)