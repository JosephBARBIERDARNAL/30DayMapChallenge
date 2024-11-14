import matplotlib.pyplot as plt
import geopandas as gpd
import cartopy.crs as ccrs

proj = ccrs.Gnomonic()
proj = ccrs.EckertI()
# proj = ccrs.InterruptedGoodeHomolosine()

world = gpd.read_file("data/countries.geojson")
world = world.to_crs(proj.proj4_init)

background_color = "#fffdf3"

fig, ax = plt.subplots(figsize=(12, 6), subplot_kw={"projection": proj})
fig.set_facecolor(background_color)

world.plot(ax=ax, color="lightgrey", edgecolor="black", lw=0.2)
ax.gridlines(draw_labels=True, color="grey", linestyle="--", lw=0.5)


plt.tight_layout()
plt.savefig("src/26-map_projections/map_projections.png", dpi=500, bbox_inches="tight")
