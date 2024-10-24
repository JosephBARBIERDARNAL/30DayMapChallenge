import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from matplotlib.patches import FancyBboxPatch
import pandas as pd
import geopandas as gpd
from pypalettes import load_cmap
from pyfonts import load_font
import h3pandas

gdf = gpd.read_file("data/french-counties.geojson")
gdf = gdf.h3.polyfill_resample(resolution=5)

df = pd.read_csv("data/french-population.csv")
df = df.merge(gdf, how="inner", left_on="Département", right_on="nom")
data = gpd.GeoDataFrame(df, geometry="geometry")

points = {
    "Bordeaux": (-0.582983, 44.840595),
    "Paris": (2.344851, 48.854240),
    "Lyon": (4.843147, 45.759170),
    "Marseille": (5.368366, 43.306943),
}

n_cat = 10
cmap = load_cmap("Exter", cmap_type="continuous")
lightfont = load_font(
    "https://github.com/googlefonts/dynapuff/blob/main/fonts/ttf/DynaPuff-Regular.ttf?raw=true"
)
mediumfont = load_font(
    "https://github.com/googlefonts/dynapuff/blob/main/fonts/ttf/DynaPuff-Bold.ttf?raw=true"
)

bins = [0, 30, 60, 90, 120, 150, 180, 250, 1000, 7000, 9200]
data["Densité_quantiles"] = pd.cut(
    data["Densité"], bins=bins, labels=False, include_lowest=True
)

fig, ax = plt.subplots()
ax.set_axis_off()

data.plot(
    ax=ax, column="Densité_quantiles", edgecolor="white", linewidth=0.01, cmap=cmap
)

labels = [f"{bins[i]:.0f} - {bins[i+1]:.0f}" for i in range(len(bins) - 1)][::-1]
value_ranges = list(range(len(labels)))[::-1]

rectangle_width = 0.8
rectangle_height = 0.5
legend_x = 9
legend_y_start = 49.5
legend_y_step = 0.62

for i in range(len(labels)):
    value = (i + 0.5) / len(labels)
    color = cmap(1 - value)

    ax.add_patch(
        FancyBboxPatch(
            (legend_x, legend_y_start - i * legend_y_step),
            rectangle_width,
            rectangle_height,
            boxstyle="round,pad=0.05",
            color=color,
            linewidth=0.6,
        )
    )

    ax.text(
        legend_x + 1,
        legend_y_start - i * legend_y_step + 0.25,
        labels[i],
        fontsize=9,
        va="center",
        ha="left",
        font=lightfont,
    )

for city, location in points.items():
    ax.scatter(location[0], location[1], color="white", s=12, ec="black")
    text = ax.text(
        location[0],
        location[1] + 0.18,
        s=f"{city}",
        color="white",
        font=lightfont,
        size=8,
    )
    text.set_path_effects(
        [path_effects.Stroke(linewidth=2, foreground="black"), path_effects.Normal()]
    )

fig.text(x=0.5, y=1, s="Population density", size=25, ha="center", font=mediumfont)
fig.text(
    x=0.5,
    y=0.96,
    s="Number of inhabitants per square kilometre in France in 2018",
    size=8,
    color="grey",
    ha="center",
    font=mediumfont,
)

fig.text(
    x=0.21,
    y=0.17 - 0.06,
    s="#30daymapchallenge 2024",
    font=mediumfont,
    ha="left",
    size=6,
)
fig.text(
    x=0.21,
    y=0.145 - 0.06,
    s="Hexagons - Joseph Barbier",
    font=lightfont,
    ha="left",
    size=6,
)
fig.text(x=0.21, y=0.12 - 0.06, s="Data: INSEE", font=lightfont, ha="left", size=6)

plt.tight_layout()
plt.savefig("src/4-hexagons/hexagons.png", dpi=500, bbox_inches="tight")
# plt.close()
