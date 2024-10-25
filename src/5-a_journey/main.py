import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
from pyfonts import load_font
from highlight_text import fig_text
from drawarrow import fig_arrow

states = gpd.read_file("data/US-states/ne_10m_admin_1_states_provinces.shp")
states = states[states["geonunit"] == "United States of America"]
states = states[["gn_name", "geometry"]]
df = pd.read_csv("data/oregon-trail.csv")

fontlight = load_font(
    "https://github.com/SorkinType/Merriweather/blob/master/fonts/ttf/Merriweather-Light.ttf?raw=true"
)
fontbold = load_font(
    "https://github.com/SorkinType/Merriweather/blob/master/fonts/ttf/Merriweather-Bold.ttf?raw=true"
)

background_color = "#323131"
text_color = "#f9e9e9"
red = "#b90303"

fig, ax = plt.subplots(figsize=(10, 10))
fig.set_facecolor(background_color)

ax.set_xlim(-125, -66)
ax.set_ylim(25, 50)
ax.set_axis_off()

states.plot(ax=ax, color="white", edgecolor="black", linewidth=0.5)
ax.plot(
    df["longitude"],
    df["latitude"],
    color=red,
    linewidth=4,
)
ax.scatter(
    df[df["name"].isin(["Oregon City", "Independence"])]["longitude"],
    df[df["name"].isin(["Oregon City", "Independence"])]["latitude"],
    color=red,
    linewidth=4,
)

arrow_style = dict(color=red, width=1.5, fill_head=False, zorder=10)
# fig_arrow(tail_position=(0.32, 0.6), head_position=(0.26, 0.63), **arrow_style)
# fig_arrow(tail_position=(0.5, 0.52), head_position=(0.45, 0.54), **arrow_style)

fig.text(
    x=0.5,
    y=0.9,
    s="The Oregon Trail",
    color=text_color,
    size=30,
    ha="center",
    font=fontlight,
)
text = """
The Oregon Trail, spanning <2,170 miles>, connected the Missouri River to Oregon’s
valleys and guided <400,000 emigrants> westward between 1846 and 1869. Originally
laid by fur traders from 1811 to 1840 and cleared for wagons by 1836, it expanded
from Independence, Missouri, to the Willamette Valley.
"""
fig_text(
    x=0.5,
    y=0.88,
    s=text,
    color=text_color,
    size=16,
    ha="center",
    va="top",
    font=fontlight,
    highlight_textprops=[{"font": fontbold}] * 2,
)
fig.text(
    x=0.1,
    y=0.27,
    s="#30daymapchallenge 2024",
    font=fontlight,
    size=7,
    ha="left",
    color=text_color,
)
fig.text(
    x=0.1,
    y=0.255,
    s="A Journey - Joseph Barbier",
    font=fontlight,
    size=7,
    ha="left",
    color=text_color,
)

text_prop = dict(color=red, font=fontbold, size=8)
ax.text(
    x=df[df["name"] == "Oregon City"]["longitude"].values[0] - 0.5,
    y=df[df["name"] == "Oregon City"]["latitude"].values[0] - 1.2,
    s="Oregon City",
    **text_prop
)
ax.text(
    x=df[df["name"] == "Independence"]["longitude"].values[0] - 1,
    y=df[df["name"] == "Independence"]["latitude"].values[0] + 1.2,
    s="Independence",
    **text_prop
)

plt.tight_layout()
plt.savefig("src/5-a_journey/a_journey.png", dpi=500, bbox_inches="tight")
