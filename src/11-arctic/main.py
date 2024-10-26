import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import cartopy.crs as ccrs
from pyfonts import load_font

world = gpd.read_file("data/countries.geojson")
df = pd.read_csv("data/arctic_ice_extent.csv")

projection = ccrs.NearsidePerspective(central_latitude=90, central_longitude=-50)
world_projected = world.to_crs(projection.proj4_init)

font = load_font(
    "https://github.com/BornaIz/markazitext/blob/master/fonts/ttf/MarkaziText-Regular.ttf?raw=true"
)

land_color = "#2a5518"
sea_color = "#b7e7fb"
axis_color = "#777777"
line_color = "#000000"
text_color = "#ffffff"

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={"projection": projection})
fig.set_facecolor(sea_color)

zoomx = 0.6
zoomy = 0.6
xlims = (-5476336.097965347, 5476336.097965347)
ylims = (-5476336.097965347, 5476336.097965347)
ax.set_xlim(xlims[0] * zoomx, xlims[1] * zoomx)
ax.set_ylim(ylims[0] * zoomy, ylims[1] * zoomy)
ax.axis("off")

world_projected.plot(ax=ax, color=land_color, edgecolor=land_color)

axline = ax.inset_axes(bounds=(0.3, 0.46, 0.32, 0.17), transform=fig.transFigure)
axline.axis("off")
axline.plot(df["year"], df["extent"], color=line_color, linewidth=0.8)
axline.plot(
    [df["year"].min(), df["year"].max()], [3.2] * 2, color=axis_color, linewidth=0.4
)
axline.plot(
    [df["year"].min(), df["year"].min()],
    [3.2, df["extent"].max()],
    color=axis_color,
    linewidth=0.4,
)

for year in range(1980, 2021, 10):
    axline.text(
        x=year, y=2.8, s=f"{year}", size=10, ha="center", color=axis_color, font=font
    )
for value in range(4, 8):
    axline.text(
        x=df["year"].min() - 2,
        y=value,
        s=f"{value}",
        size=10,
        ha="center",
        color=axis_color,
        font=font,
    )
    axline.hlines(
        y=value,
        xmin=df["year"].min(),
        xmax=df["year"].max(),
        color=axis_color,
        alpha=0.8,
        linewidth=0.2,
        linestyles="dashed",
    )
axline.text(
    x=df["year"].min() + 1.2,
    y=4.1,
    s="sea ice extent, in million square km",
    color=axis_color,
    size=8,
    font=font,
)

fig.text(
    x=0.88,
    y=0.82,
    s="Arctic Sea Ice Extent: the decline",
    color=text_color,
    size=30,
    ha="right",
    font=font,
)
s = """
Over the last 40 years, the extent of Arctic sea ice has been almost halved.
The main consequence is the accelerated warming of the region, which disrupts
ecosystems and amplifies global climate change impacts.
"""
fig.text(
    x=0.88, y=0.82, s=s, color=text_color, size=14, ha="right", va="top", font=font
)

s = """
As the amount of ice tends
to reach its lowest value
in September, the measurement
here is the lowest annual ice
extent in September.
"""
fig.text(
    x=0.53, y=0.37, s=s, size=7.5, ha="center", va="top", color=text_color, font=font
)

s = """
According to NASA, sea
ice extent is the total
area covered by grid
cells that have an ice
concentration of at
least 15%.
"""
fig.text(
    x=0.55, y=0.3, s=s, size=7.5, ha="center", va="top", color=text_color, font=font
)

fig.text(x=0.76, y=0.43, s="Data: NASA", color=text_color, size=11, font=font)
fig.text(
    x=0.14, y=0.45, s="#30daymapchallenge\n2024", color=text_color, size=10, font=font
)
fig.text(
    x=0.14, y=0.4, s="Arctic\nJoseph Barbier", color=text_color, size=10, font=font
)

plt.savefig("src/11-arctic/arctic.png", dpi=500, bbox_inches="tight")
