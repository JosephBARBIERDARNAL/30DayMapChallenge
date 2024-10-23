import matplotlib.pyplot as plt
from pypalettes import load_cmap
import pandas as pd
import numpy as np

# Load the earthquake data
df = pd.read_csv("data/earthquakes.csv")
x = df["Longitude"]
y = df["Latitude"]
z = df["Depth (km)"]

# Load the colormap
cmap = load_cmap("Coconut", cmap_type="continuous")

# Create a 3D plot
fig, ax = plt.subplots(subplot_kw=dict(projection="3d"))

# Set width and depth of bars
dx = dy = 1  # You can adjust these values as needed
dz = z

# Normalize the z values for color mapping
norm = plt.Normalize(z.min(), z.max())
colors = cmap(norm(z))

# Create the 3D bar chart
ax.bar3d(x, y, np.zeros_like(z), dx, dy, dz, color=colors)
ax.view_init(elev=40, azim=20)


# Set labels
ax.set_xlabel("")
ax.set_ylabel("")
ax.set_zlabel("")

# Save the plot
plt.savefig("src/18-3d/3d.png", dpi=500, bbox_inches="tight")
plt.close()
