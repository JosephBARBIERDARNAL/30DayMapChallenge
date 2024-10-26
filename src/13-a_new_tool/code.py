import pyvista as pv
from pyvista import examples
from pypalettes import load_cmap

land = examples.download_topo_land().triangulate().decimate(0.98)
land.point_data["Elevation"] = land.points[:, 2]

p = pv.Plotter()
cmap = load_cmap("Coconut", cmap_type="continuous")
p.add_mesh(land, scalars="Elevation", cmap=cmap)

p.export_html("src/13-a_new_tool/a_new_tool.html")
p.save_graphic("src/13-a_new_tool/a_new_tool.svg")
