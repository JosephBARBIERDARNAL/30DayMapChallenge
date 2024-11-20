import matplotlib.pyplot as plt
import geopandas as gpd
import cartopy.crs as ccrs
from pypalettes import load_cmap
from pyfonts import load_font
from drawarrow import fig_arrow

proj = ccrs.Mercator()

world = gpd.read_file("data/countries.geojson")
world = world.to_crs(proj.proj4_init)
world = world[~world["name"].isin(["Antarctica"])]

world["useImperial"] = world["name"].apply(
    lambda x: (
        "true"
        if x in ["United States of America", "Liberia", "Myanmar"]
        else "false"
        if x not in "United Kingdom"
        else "both"
    )
)


font = load_font(
    "https://github.com/BornaIz/markazitext/blob/master/fonts/ttf/MarkaziText-Regular.ttf?raw=true"
)

cmap = load_cmap(
    "Sunset",
    keep=[
        False,
        False,
        True,
        False,
        True,
        False,
        True,
    ],
)
background_color = "#171b2b"
text_color = "#fff"

fig, ax = plt.subplots(figsize=(12, 6), subplot_kw={"projection": proj})
fig.set_facecolor(background_color)
ax.axis("off")

world.plot(ax=ax, column="useImperial", edgecolor="#000000", lw=0.15, cmap=cmap)

fig.text(
    x=0.83,
    y=1.08,
    s="Metric vs Imperial System",
    size=30,
    ha="right",
    font=font,
    va="top",
    color=text_color,
)
description = """
Most countries worldwide have adopted and primarily use the metric
system, which is based on seven base units like the meter and kilogram.\n
However, a few countries still primarily rely on the Imperial system,
creating added confusion in international trade and standardization.
"""
fig.text(
    x=0.83,
    y=1.035,
    s=description,
    size=12,
    ha="right",
    font=font,
    va="top",
    color=text_color,
)

fig.text(
    x=0.23,
    y=0.2,
    s="Use the metric system\n\nUse the imperial system\n\nUse both (???)",
    ha="left",
    font=font,
    size=12,
    color=text_color,
)

ax.add_patch(
    plt.Rectangle(
        (0.08, 0.277),
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
        (0.08, 0.227),
        0.02,
        0.025,
        facecolor=cmap.colors[2],
        lw=0.5,
        edgecolor="black",
        transform=ax.transAxes,
    )
)
ax.add_patch(
    plt.Rectangle(
        (0.08, 0.18),
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
    s="#30DayMapChallenge\nConflict - Joseph Barbier",
    font=font,
    ha="right",
    size=8,
    color=text_color,
)

fig.text(x=0.295, y=0.485, s="USA", color="black", font=font, size=12)
fig.text(x=0.45, y=0.53, s="UK", color=cmap.colors[0], font=font, size=12)
fig_arrow(
    (0.46, 0.55),
    (0.487, 0.595),
    color=cmap.colors[0],
    radius=-0.4,
    head_length=4,
    head_width=2,
    width=0.8,
)
fig.text(x=0.47, y=0.25, s="Liberia", color=cmap.colors[2], font=font, size=12)
fig_arrow(
    (0.48, 0.27),
    (0.48, 0.34),
    color=cmap.colors[2],
    radius=-0.3,
    head_length=4,
    head_width=2,
    width=0.8,
)
fig.text(x=0.64, y=0.25, s="Myanmar", color=cmap.colors[2], font=font, size=12)
fig_arrow(
    (0.66, 0.27),
    (0.679, 0.4),
    color=cmap.colors[2],
    radius=-0.2,
    head_length=4,
    head_width=2,
    width=0.8,
)

plt.tight_layout()
plt.savefig("src/21-conflict/conflict.png", dpi=500, bbox_inches="tight")
