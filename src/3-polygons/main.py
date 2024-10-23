import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Point, Polygon
from scipy.spatial import Voronoi, voronoi_plot_2d

# Load a GeoDataFrame for country or region boundaries and lakes
world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
lakes = gpd.read_file(
    gpd.datasets.get_path("naturalearth_lowres")
)  # You may replace this with an actual lake dataset

# Select a specific country (e.g., Finland) or region with many lakes
country = world[world["name"] == "Finland"]

# Generate random points as an example (Replace with actual lake centroids or points of interest)
# For example, we use lakes' centroids in Finland, but here we simulate points for demonstration.
# Extract the bounding box of the country as scalar values
minx, miny, maxx, maxy = country.total_bounds

# Generate random points within the country's bounding box
num_points = 20
points = np.random.rand(num_points, 2)
points[:, 0] = points[:, 0] * (maxx - minx) + minx
points[:, 1] = points[:, 1] * (maxy - miny) + miny


# Compute Voronoi diagram
vor = Voronoi(points)


# Function to create polygons from Voronoi regions
def voronoi_polygons(vor, region):
    lines = []
    for r in vor.regions:
        if not -1 in r and len(r) > 0:
            polygon = [vor.vertices[i] for i in r]
            lines.append(Polygon(polygon))
    return gpd.GeoDataFrame(geometry=lines)


# Generate Voronoi polygons
vor_polygons = voronoi_polygons(vor, country)

# Clip Voronoi polygons to country boundaries
country_shape = country.unary_union
clipped_vor = gpd.clip(vor_polygons, country_shape)

# Plot the map
fig, ax = plt.subplots(figsize=(10, 10))
country.boundary.plot(ax=ax, color="black")  # Plot the country boundary
clipped_vor.plot(ax=ax, cmap="coolwarm", edgecolor="white")  # Plot Voronoi polygons
plt.title("Voronoi Diagram of Lakes in Finland", fontsize=15)


plt.tight_layout()
plt.savefig("src/3-polygons/polygons.png", dpi=500, bbox_inches="tight")
