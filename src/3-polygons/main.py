import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from pypalettes import load_cmap
from pyfonts import load_font

from src.utils import CustomLegend

split_factor = 5

counties = gpd.read_file("data/US-counties/ne_10m_admin_2_counties.shp")
counties = counties[["NAME_ALT", "geometry", "ADM2_CODE"]]
rates = pd.read_csv("data/unemployment-rate.csv")
rates["id"] = rates["id"].apply(lambda x: f"USA-{x:05d}")
data = counties.merge(rates, how="inner", left_on="ADM2_CODE", right_on="id").drop(
    columns="id"
)
data["quartile"] = pd.qcut(data["rate"], q=split_factor, labels=False)

states = gpd.read_file("data/US-states/ne_10m_admin_1_states_provinces.shp")
states = states[states["geonunit"] == "United States of America"]
states = states[["gn_name", "geometry"]]
data_grouped = data.groupby(by="state").agg({"rate": "mean"}).reset_index()
data_grouped = data_grouped.merge(
    states, how="inner", left_on="state", right_on="gn_name"
).drop(columns="gn_name")
data_grouped = gpd.GeoDataFrame(data_grouped, geometry="geometry")
data_grouped["quartile"] = pd.qcut(data_grouped["rate"], q=split_factor, labels=False)

cmap = load_cmap(
    "Coconut", keep=[True, True, False, True, True, True][::-1], reverse=True
)
colors = cmap.colors
background_color = "#eeeeee"
text_color = "#3a3939"


fontlight = load_font(
    "https://github.com/coreyhu/Urbanist/blob/main/fonts/ttf/Urbanist-Light.ttf?raw=true"
)
fontbold = load_font(
    "https://github.com/coreyhu/Urbanist/blob/main/fonts/ttf/Urbanist-Bold.ttf?raw=true"
)
fontitalic = load_font(
    "https://github.com/coreyhu/Urbanist/blob/main/fonts/ttf/Urbanist-LightItalic.ttf?raw=true"
)

quartile_ranges = [
    (data["rate"].quantile(0), data["rate"].quantile(0.2)),
    (data["rate"].quantile(0.2), data["rate"].quantile(0.4)),
    (data["rate"].quantile(0.4), data["rate"].quantile(0.6)),
    (data["rate"].quantile(0.6), data["rate"].quantile(0.8)),
    (data["rate"].quantile(0.8), data["rate"].quantile(1)),
]

map_params = dict(cmap=cmap, edgecolor="white")

fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(15, 10))
fig.set_facecolor(background_color)

data.plot(column="quartile", ax=ax1, linewidth=0.15, **map_params)
data_grouped.plot(column="quartile", ax=ax2, linewidth=0.3, **map_params)

for ax, group in zip([ax1, ax2], ["counties", "states (average across counties)"]):
    ax.set_xlim(-126, -68)
    ax.set_ylim(24, 50)
    ax.set_axis_off()

    ax.text(
        x=0.06,
        y=0.98,
        s=f"{group}",
        transform=ax.transAxes,
        font=fontitalic,
        size=13,
        color=text_color,
    )

fig.text(
    x=0.02,
    y=0.88,
    s="By county VS by state",
    ha="left",
    size=60,
    font=fontlight,
    color=text_color,
)
fig.text(
    x=0.02,
    y=0.96,
    s="Unemployment rates (in %) in the United States",
    ha="left",
    size=20,
    font=fontitalic,
    color=text_color,
)
text = """
When measuring metrics across geographical areas, the level of detail is key.
Striking the right balance between granularity and readability is essential—too
much detail can overwhelm, while too little can obscure important insights.
"""
fig.text(
    x=0.02,
    y=0.87,
    s=text,
    ha="left",
    va="top",
    size=16,
    font=fontlight,
    color=text_color,
)
fig.text(
    x=0.02,
    y=0.32,
    s="#30daymapchallenge 2024",
    font=fontbold,
    ha="left",
    size=12,
    color=text_color,
)
fig.text(
    x=0.02,
    y=0.30,
    s="Polygons - Joseph Barbier",
    font=fontlight,
    ha="left",
    size=12,
    color=text_color,
)
fig.text(
    x=0.02,
    y=0.28,
    s="Data",
    font=fontbold,
    ha="left",
    size=12,
    color=text_color,
)
fig.text(
    x=0.045,
    y=0.28,
    s=": Bureau of Labor Statistics",
    font=fontlight,
    ha="left",
    size=12,
    color=text_color,
)

legend_elements = [
    CustomLegend(
        color=colors[i],
        label=f"{quartile_ranges[i][0]:.2f} - {quartile_ranges[i][1]:.1f}",
    ).set_label_below(ax, 0.325 + i * 0.13, 1.22, color=text_color, font=fontbold)
    for i in range(split_factor)
]

fig.legend(
    handles=legend_elements,
    bbox_to_anchor=(0.95, 0.86),
    prop=fontbold,
    handlelength=4,
    fancybox=False,
    frameon=False,
    handleheight=3,
    labelspacing=0.8,
    ncol=len(legend_elements),
    labels=[""] * len(legend_elements),
)

plt.tight_layout()
plt.savefig("src/3-polygons/polygons.png", dpi=500, bbox_inches="tight")
plt.close()
