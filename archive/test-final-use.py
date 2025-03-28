import matplotlib.pyplot as plt
import numpy as np

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
    
    Returns:
    --------
    fig, ax : tuple
        Figure and axis objects
    """
    # Create the figure and polar subplot
    fig = plt.figure(figsize=(10, 6))
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
    ax.annotate('80', 
                xy=(current_theta, 0.6),  # Arrow tip (at current value)
                xytext=(min_theta + theta_range/2, 0),  # Arrow base (at center)
                arrowprops=dict(arrowstyle="wedge, tail_width=1.2",
                               color='black', 
                               lw=1,
                               shrinkA=0),
                bbox=dict(boxstyle='circle', facecolor='black', edgecolor='black', linewidth=2.0),
                )

    # Customize the plot appearance
    ax.grid(False)
    ax.set_yticks([])  # Remove radial ticks
    ax.set_theta_direction('clockwise')  # Clockwise direction
    ax.set_rlim(0, 0.9)  # Set radius limits
    
    # Add the legend at the top
    ax.legend(handles=legend_patches, loc='upper center', bbox_to_anchor=(0.5, 1.15),
              ncol=3, frameon=False, fontsize=10)
    # # Add solar icon above the title
    # ax.text(min_theta + theta_range/2, 0.6, '☀️', fontsize=30, ha='center', va='center', transform=ax.transAxes)
    
    ax.set_title('Overall Clean Power 2030 Progress', fontsize=20, pad=60)

    # Hide all unnecessary spines and tick labels
    ax.spines['polar'].set_visible(False)
    ax.set_xticklabels([])

    plt.tight_layout()
    
    return fig, ax

# Example usage:
if __name__ == "__main__":
    # Create chart with default values
    fig, ax = create_gauge_chart()
    plt.show()
    
    # Or with custom values
    # fig, ax = create_gauge_chart(existing_capacity=25, target_capacity=120, capacity_on_track=45)
    # plt.show()