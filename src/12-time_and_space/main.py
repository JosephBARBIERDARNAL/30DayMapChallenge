import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import geopandas as gpd
import cartopy.crs as ccrs
from pyfonts import load_font

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

map_color = "#585858"
alpha_before = 0.4
size_before = 10
size_after = 20
color_scatter = "#e73939"

fig, ax = plt.subplots(dpi=500, subplot_kw={"projection": proj})
ax.axis("off")


def update(year):
    ax.clear()
    ax.axis("off")
    world.plot(ax=ax, color=map_color)

    before = df[df["Year"] <= year]
    current = df[df["Year"] == year]

    ax.scatter(
        before["Longitude2"],
        before["Latitude2"],
        color=color_scatter,
        s=size_before,
        alpha=alpha_before,
    )
    ax.scatter(
        current["Longitude2"], current["Latitude2"], color=color_scatter, s=size_after
    )

    ax.text(
        x=0.5, y=0.9, s=f"Year: {year}", size=25, ha="center", transform=ax.transAxes
    )


ani = FuncAnimation(fig, update, frames=df["Year"].unique())
ani.save("src/12-time_and_space/time_and_space.gif", fps=5)
