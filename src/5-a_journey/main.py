import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from drawarrow import fig_arrow
from pyfonts import load_font

start_point = (44.828687, -0.564033)
end_point = (44.795688, -0.618150)

north = max(start_point[0], end_point[0]) + 0.002
south = min(start_point[0], end_point[0]) - 0.002
east = max(start_point[1], end_point[1]) + 0.002
west = min(start_point[1], end_point[1]) - 0.002

zoom_out_factor = 0.04
north += zoom_out_factor
south -= zoom_out_factor
east += zoom_out_factor
west -= zoom_out_factor

G = ox.graph_from_bbox(north, south, east, west, network_type="walk")

start_node = ox.nearest_nodes(G, start_point[1], start_point[0])
end_node = ox.nearest_nodes(G, end_point[1], end_point[0])

route = nx.shortest_path(G, start_node, end_node, weight="length")
route_coordinates = [[G.nodes[node]["y"], G.nodes[node]["x"]] for node in route]
route_lat = [coord[0] for coord in route_coordinates]
route_lon = [coord[1] for coord in route_coordinates]

font = load_font(
    "https://github.com/Outfitio/Outfit-Fonts/blob/main/fonts/ttf/Outfit-Medium.ttf?raw=true"
)
fontlight = load_font(
    "https://github.com/Outfitio/Outfit-Fonts/blob/main/fonts/ttf/Outfit-Light.ttf?raw=true"
)
fontbold = load_font(
    "https://github.com/Outfitio/Outfit-Fonts/blob/main/fonts/ttf/Outfit-Bold.ttf?raw=true"
)

fig, ax = plt.subplots(figsize=(12, 8))

ox.plot_graph(
    G, ax=ax, node_size=0, edge_color="#6a6969", edge_linewidth=0.5, show=False
)

ax.plot(route_lon, route_lat, color="#fc003f", linewidth=3)

ax.scatter(start_point[1], start_point[0], c="#fc003f", s=100, label="Start", zorder=5)
ax.scatter(end_point[1], end_point[0], c="#fc003f", s=100, label="End", zorder=5)
fig.text(
    x=0.5,
    y=0.98,
    s="My daily commute* of 5.7 km in Bordeaux during college",
    fontsize=17,
    ha="center",
    font=font,
)
fig.text(
    x=0.26,
    y=0.01,
    s="*Exceptions: COVID, weekends, public holidays, rain and when I didn't want to.",
    fontsize=8,
    ha="left",
    font=fontlight,
)
fig.text(
    x=0.75, y=0.017, s="#30daymapchallenge 2024", font=fontbold, size=8, ha="right"
)
fig.text(x=0.75, y=0, s="A Journey - Joseph Barbier", font=fontbold, size=8, ha="right")

bboxprops = dict(boxstyle="round", facecolor="white", alpha=0.7)
text_style = dict(
    transform=ax.transAxes,
    fontsize=14,
    verticalalignment="top",
    bbox=bboxprops,
    font=fontbold,
)
ax.text(0.5, 0.25, s="This was my campus", **text_style)
ax.text(0.1, 0.85, s="Where I used to live", **text_style)

arrow_style = dict(color="black", fill_head=False, width=2, radius=-0.3)
fig_arrow(tail_position=(0.49, 0.25), head_position=(0.40, 0.35), **arrow_style)
fig_arrow(tail_position=(0.45, 0.82), head_position=(0.595, 0.65), **arrow_style)

plt.tight_layout()
plt.savefig("src/5-a_journey/a_journey.png", dpi=500, bbox_inches="tight")
