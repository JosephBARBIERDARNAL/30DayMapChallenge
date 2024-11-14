import matplotlib.pyplot as plt
import geopandas as gpd
import cartopy.crs as ccrs
from pypalettes import load_cmap
from pyfonts import load_font

proj = ccrs.Mercator()

world = gpd.read_file("data/countries.geojson")
world = world.to_crs(proj.proj4_init)
world = world[~world["name"].isin(["Antarctica"])]

world["hasamazingfood"] = world["name"].apply(
    lambda x: (
        True if x in ["France", "Italy", "Morocco", "South Korea", "Japan"] else False
    )
)


font = load_font(
    "https://github.com/BornaIz/markazitext/blob/master/fonts/ttf/MarkaziText-Regular.ttf?raw=true"
)

cmap = load_cmap("Acadia", keep=[False, False, True, False, True, False])
background_color = "#fffdf3"

fig, ax = plt.subplots(figsize=(12, 6), subplot_kw={"projection": proj})
fig.set_facecolor(background_color)
ax.axis("off")

world.plot(ax=ax, column="hasamazingfood", edgecolor="black", lw=0.2, cmap=cmap)

fig.text(
    x=0.5,
    y=1.07,
    s="An exhaustive (and objective) list of",
    size=20,
    ha="center",
    font=font,
    color="#cfcdcd",
    va="top",
)
fig.text(
    x=0.5,
    y=1.03,
    s="Countries with the best food in the world",
    size=30,
    ha="center",
    font=font,
    va="top",
)

fig.text(x=0.25, y=0.2, s="Has amazing food\n\nHas food", ha="left", font=font, size=12)

ax.add_patch(
    plt.Rectangle(
        (0.11, 0.227),
        0.02,
        0.025,
        facecolor=cmap.colors[1],
        lw=0.5,
        edgecolor="black",
        transform=ax.transAxes,
    )
)
ax.add_patch(
    plt.Rectangle(
        (0.11, 0.18),
        0.02,
        0.025,
        facecolor=cmap.colors[0],
        lw=0.5,
        edgecolor="black",
        transform=ax.transAxes,
    )
)

fig.text(
    x=0.75,
    y=0.1,
    s="#30DayMapChallenge\nA world map - Joseph Barbier",
    font=font,
    ha="right",
    size=8,
)

plt.tight_layout()
plt.savefig("src/14-a_world_map/a_world_map.png", dpi=500, bbox_inches="tight")
