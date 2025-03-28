import matplotlib.pyplot as plt
import numpy as np
# from matplotlib.patches import Wedge
# from matplotlib.patches import Circle

# Create the figure and polar subplot
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(projection="polar")

# Define the gauge parameters
gauge_min = 0
gauge_max = 100
gauge_range = gauge_max - gauge_min

# Define segment boundaries (in percentage)
segment_bounds = [0, 40, 70, 100]  # Three segments
segment_colors = ['#4575b4', '#74add1', 'lightgray']
segment_labels = ['Low', 'Medium', 'High']

# Convert to radians for polar plot (0 to 180 degrees)
# Note: In polar coordinates, 0 is to the right, pi/2 is up
# min_theta = np.pi/2
# max_theta = 3 * np.pi/2
# theta_range = max_theta - min_theta

# # Convert to radians for polar plot
# min_theta = -np.pi/2  # Bottom (-90 degrees)
# max_theta = np.pi/2   # Top (90 degrees)
# theta_range = max_theta - min_theta

# Convert to radians for polar plot
min_theta = np.pi  # Left (180 degrees)
max_theta = 2*np.pi   # Right (360 degrees/0 degrees)
theta_range = max_theta - min_theta

# Current value for the dial
current_value = 40 # Example value in the medium range

# Calculate current angle
current_theta = min_theta + (current_value - gauge_min) / gauge_range * theta_range

# Create the colored segments
for i in range(len(segment_bounds) - 1):
    # Convert segment boundaries to angles
    start_theta = min_theta + (segment_bounds[i] - gauge_min) / gauge_range * theta_range
    end_theta = min_theta + (segment_bounds[i+1] - gauge_min) / gauge_range * theta_range
    
    # Generate points for the segment
    theta = np.linspace(start_theta, end_theta, 100)
    r = np.ones_like(theta) * 0.9  # Radius of the gauge
    
    # Plot the segment
    ax.fill_between(theta, 0.7, r, color=segment_colors[i], alpha=0.8)
    
    # # Add segment label
    # mid_theta = (start_theta + end_theta) / 2
    # x = 0.8 * np.cos(mid_theta)
    # y = 0.8 * np.sin(mid_theta)
    # ax.text(mid_theta, 0.8, segment_labels[i], ha='center', va='center', fontsize=12)

# # Create the gauge outline
# theta = np.linspace(min_theta, max_theta, 100)
# r = np.ones_like(theta) * 0.9
# ax.plot(theta, r, 'k-', lw=2)

# # Add ticks
# for percent in range(0, 101, 10):
#     tick_theta = min_theta + (percent - gauge_min) / gauge_range * theta_range
#     tick_r_inner = 0.9
#     tick_r_outer = 1.0
#     ax.plot([tick_theta, tick_theta], [tick_r_inner, tick_r_outer], 'k-', lw=2)
    
#     # Add tick labels every 20 units
#     if percent % 20 == 0:
#         x = 1.05 * np.cos(tick_theta)
#         y = 1.05 * np.sin(tick_theta)
#         ax.text(tick_theta, 1.1, f'{percent}', ha='center', va='center', fontsize=10)

# Add the arrow annotation
ax.annotate('80', 
            xy=(current_theta, 0.6),  # Arrow tip (at current value)
            xytext=(min_theta + theta_range/2, 0),  # Arrow base (at center)
            arrowprops=dict(arrowstyle="wedge, tail_width=1.5",
                           color='black', 
                           lw=2,
                           shrinkA=0),
            bbox=dict(boxstyle='circle', facecolor='black', edgecolor='black', linewidth=15.0),

            )

# # Add a circle at the center with the current value
# circle = Circle((0, 0), 0.2, transform=ax.transData._b, color='white', zorder=10)
# ax.add_patch(circle)
# ax.text(0, 0, f'{current_value}', ha='center', va='center', fontsize=15, 
#         bbox=dict(boxstyle='circle', facecolor='white', edgecolor='black'),
#         color='black')

# Customize the plot appearance
ax.grid(False)
ax.set_yticks([])  # Remove radial ticks
ax.set_theta_zero_location('E')  # Set 0 degrees to the right
ax.set_theta_direction('clockwise')  # Clockwise direction
ax.set_rlim(0, 0.9)  # Set radius limits
ax.set_title('Dial Gauge Chart', fontsize=16, pad=20)

# Hide all unnecessary spines and tick labels
ax.spines['polar'].set_visible(False)
ax.set_xticklabels([])

plt.tight_layout()
plt.show()