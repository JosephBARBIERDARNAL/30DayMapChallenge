import pyvista as pv
from pyvista import examples
from pypalettes import load_cmap

# Load and prepare the Earth topography data
land = examples.download_topo_land().triangulate().decimate(0.98)
land.point_data["Elevation"] = land.points[:, 2]

# Initialize the plotter with transparent background
p = pv.Plotter()
cmap = load_cmap("Coconut", cmap_type="continuous")
p.add_mesh(land, cmap=cmap, show_scalar_bar=False)  # Disable scalar bar

# Set the background to be fully transparent
# p.background_color = (245, 40, 145, 0)
p.set_background(color="#080c14")

# Export the plot to an HTML file with transparency
p.export_html("../barbierjoseph.com/public/img/a_new_tool.html")
# p.save_graphic("src/13-a_new_tool/a_new_tool.svg")
