import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import geopandas as gpd
import wikipedia as wp
from pypalettes import load_cmap
from pyfonts import load_font

html = (
    wp.page("List_of_Chinese_administrative_divisions_by_population")
    .html()
    .encode("UTF-8")
)
df = pd.read_html(html)[1]
df = df.drop(columns="Unnamed: 4").iloc[1:]

world = gpd.read_file("data/countries.geojson")
china = gpd.read_file("data/china.json")

map_province_names = {
    "Xinjiang Uygur": "Xinjiang",
    "Ningxia Hui": "Ningxia",
    "Nei Mongol": "Inner Mongolia",
    "Xizang": "Tibet",
}
china = china.replace(map_province_names)

china = china.merge(df, how="left", left_on="NAME_1", right_on="Division")
china = china[["NAME_1", "Division", "Total", "Urban", "Rural", "geometry"]]
china["centroid"] = china["geometry"].centroid

font = load_font(
    "https://github.com/coreyhu/Urbanist/blob/main/fonts/ttf/Urbanist-Medium.ttf?raw=true"
)
boldfont = load_font(
    "https://github.com/coreyhu/Urbanist/blob/main/fonts/ttf/Urbanist-ExtraBold.ttf?raw=true"
)

cmap = load_cmap("YlGnBu", cmap_type="continuous")
cmap = load_cmap("X28", cmap_type="continuous", reverse=True)
color_world = "#e5e4e4"
edgecolor_world = color_world
lw_world = 0
sea_color = "#ffffff"
edgecolor_china = "#515151"
lw_china = 0.5

fig, ax = plt.subplots()
ax.set_facecolor(sea_color)

world.plot(
    ax=ax, color=color_world, alpha=0.7, edgecolor=edgecolor_world, linewidth=lw_world
)
china.plot(
    column="Total", ax=ax, edgecolor=edgecolor_china, linewidth=lw_china, cmap=cmap
)

bins = [0, 30, 60, 90, 120, 150, 180, 250, 1000, 7000, 9200]
bins = pd.cut(china["Total"], bins=6, retbins=True)[1]
labels = [
    f"{bins[i]/1_000_000:.0f} - {bins[i+1]/1_000_000:.0f}" for i in range(len(bins) - 1)
][::-1]
value_ranges = list(range(len(labels)))[::-1]

rectangle_scale = 2
rectangle_width = 0.8 * rectangle_scale
rectangle_height = 0.5 * rectangle_scale
legend_x = 68
legend_y_start = 57
legend_y_step = 2.2

for i in range(len(labels)):
    value = (i + 0.5) / len(labels)
    color = cmap(1 - value)

    ax.add_patch(
        FancyBboxPatch(
            (legend_x, legend_y_start - i * legend_y_step),
            rectangle_width,
            rectangle_height,
            facecolor=color,
            edgecolor="black",
            linewidth=0.6,
        )
    )

    ax.text(
        legend_x + 2.5,
        legend_y_start - i * legend_y_step + 0.25,
        s=f"{labels[i]}M",
        fontsize=6,
        va="center",
        ha="left",
        font=font,
    )

ax.set_xlim(65, 155)
ax.set_ylim(10, 60)
ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
ax.tick_params(
    which="both", bottom=False, left=False, labelbottom=False, labelleft=False
)

province_to_annotate = {
    "Xinjiang": {"location": (0, 0), "rotation": 0},
    "Tibet": {"location": (0, 1), "rotation": 0},
    "Qinghai": {"location": (0, 1), "rotation": 0},
    "Jilin": {"location": (0, 1), "rotation": 0},
    "Yunnan": {"location": (0, 0), "rotation": 0},
    "Guangdong": {"location": (2, -0.7), "rotation": 15},
    "Sichuan": {"location": (0, 1), "rotation": 0},
    "Hubei": {"location": (0, 1), "rotation": 0},
    "Heilongjiang": {"location": (0, 0), "rotation": 0},
    "Hainan": {"location": (1, -1.5), "rotation": 0},
    "Inner Mongolia": {"location": (-3, -1.2), "rotation": 24},
}
for province in province_to_annotate:
    province_data = china.loc[china["NAME_1"] == province]
    centroid = province_data["centroid"].values[0]
    value = province_data["Total"].values[0]
    x, y = centroid.coords[0]
    rotation = 0
    if province in province_to_annotate.keys():
        x += province_to_annotate[province]["location"][0]
        y += province_to_annotate[province]["location"][1]
    if province in province_to_annotate.keys():
        rotation += province_to_annotate[province]["rotation"]
    ax.text(
        x=x,
        y=y,
        s=f"{province.upper()}",
        fontsize=4.5,
        ha="center",
        va="top",
        rotation=rotation,
        font=font,
    )
    y_adj = -0.9
    if "mongol" in province.lower():
        y_adj = +0.2
    ax.text(
        x=x,
        y=y + y_adj,
        s=f"{value/1e6:.1f}M",
        fontsize=5,
        ha="center",
        va="top",
        weight="bold",
        rotation=rotation,
        font=boldfont,
    )


fig.text(
    x=0.97, y=0.4, s="China's population", size=18, ha="right", va="top", font=font
)
fig.text(
    x=0.97,
    y=0.34,
    s="95% of the population lives on less than 50% of the total surface area.",
    size=5,
    ha="right",
    va="top",
    color="grey",
    font=font,
)

fig.text(x=0.97, y=0.1, s="#30daymapchallenge 2024", font=boldfont, size=5, ha="right")
fig.text(x=0.97, y=0.08, s="Joseph Barbier", font=font, size=5, ha="right")


plt.tight_layout()
plt.savefig("src/16-choropleth/choropleth.png", dpi=500, bbox_inches="tight")
