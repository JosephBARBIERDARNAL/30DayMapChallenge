import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import geopandas as gpd
import cartopy.crs as ccrs
from pyfonts import load_font
from pypalettes import load_cmap

fontlight = load_font(
    "https://github.com/coreyhu/Urbanist/blob/main/fonts/ttf/Urbanist-Light.ttf?raw=true"
)
fontbold = load_font(
    "https://github.com/coreyhu/Urbanist/blob/main/fonts/ttf/Urbanist-Bold.ttf?raw=true"
)

cmap = load_cmap("OrYel", cmap_type="continuous")

df = pd.read_csv("data/earthquakes-large.csv")
df = df.drop(
    columns=[
        "Depth Error",
        "Depth Seismic Stations",
        "Magnitude Error",
        "Magnitude Seismic Stations",
        "Azimuthal Gap",
        "Horizontal Distance",
        "Horizontal Error",
        "Root Mean Square",
    ]
)
df = df[df["Type"].isin(["Earthquake", "Nuclear Explosion"])]
df["Year"] = df["Date"].str[-4:].astype(int)

proj = ccrs.Mercator()

world = gpd.read_file("data/countries.geojson")
world = world.to_crs(proj.proj4_init)

pc = ccrs.PlateCarree()
new_coords = proj.transform_points(pc, df["Longitude"].values, df["Latitude"].values)
df["Longitude2"] = new_coords[:, 0]
df["Latitude2"] = new_coords[:, 1]

map_color = "#907676"
color_scatter = "#bb0303"

fig, ax = plt.subplots(dpi=500, subplot_kw={"projection": proj})
ax.axis("off")


def update(year):
    ax.clear()
    ax.axis("off")
    world.plot(ax=ax, color=map_color)

    subset = df[df["Year"] <= year]

    ax.scatter(
        subset["Longitude2"],
        subset["Latitude2"],
        c=subset["Magnitude"],
        cmap=cmap,
        edgecolor="black",
        linewidth=0.4,
        alpha=0.7,
        s=12,
    )

    ax.text(
        x=0.5,
        y=1.02,
        s=f"Watch earthquakes trace the tectonic plates throughout time",
        size=12,
        ha="center",
        transform=ax.transAxes,
        font=fontlight,
    )

    ax.text(
        x=0.2,
        y=0.14,
        s=f"Year: {year}",
        size=8,
        ha="center",
        transform=ax.transAxes,
        font=fontbold,
    )

    ax.text(
        x=0.85,
        y=0.06,
        s=f"#30DayMapChallenge 2024",
        size=5,
        ha="right",
        transform=ax.transAxes,
        font=fontlight,
        color="white",
    )

    ax.text(
        x=0.85,
        y=0.04,
        s=f"Time and space - Joseph Barbier",
        size=5,
        ha="right",
        transform=ax.transAxes,
        font=fontlight,
        color="white",
    )


ani = FuncAnimation(fig, update, frames=df["Year"].unique())
ani.save("src/12-time_and_space/time_and_space.gif", fps=8)
