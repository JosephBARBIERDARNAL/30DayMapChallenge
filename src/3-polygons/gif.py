from gifing import Gif
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from pypalettes import load_cmap
from pyfonts import load_font

path = "https://raw.githubusercontent.com/holtzy/The-Python-Graph-Gallery/master/static/data/us-counties-employmentrate.geojson"
uscounties = gpd.read_file(path)
uscounties.head()

path = "https://raw.githubusercontent.com/holtzy/The-Python-Graph-Gallery/master/static/data/us-states-employmentrate.geojson"
usstates = gpd.read_file(path)
usstates.head()

group = ["counties", "states"]

cmap = load_cmap(
    "Coconut", keep=[True, True, False, True, True, True][::-1], reverse=True
)

fontlight = load_font(
    "https://github.com/coreyhu/Urbanist/blob/main/fonts/ttf/Urbanist-Light.ttf?raw=true"
)
fontbold = load_font(
    "https://github.com/coreyhu/Urbanist/blob/main/fonts/ttf/Urbanist-Bold.ttf?raw=true"
)
fontitalic = load_font(
    "https://github.com/coreyhu/Urbanist/blob/main/fonts/ttf/Urbanist-LightItalic.ttf?raw=true"
)

x = 0

###############################################

fig, axs = plt.subplots(
    dpi=300, figsize=(10, 10), sharex=True, gridspec_kw={"hspace": 0.01}
)

usstates.plot(ax=axs, edgecolor="#e1e1e1")

axs.set_xlim(-126, -68)
axs.set_ylim(24, 50)


x += 1
plt.savefig(f"src/3-polygons/gif/{x}.png", dpi=300, bbox_inches="tight")

###############################################

fig, axs = plt.subplots(
    nrows=2, dpi=300, figsize=(10, 15), sharex=True, gridspec_kw={"hspace": 0.01}
)

usstates.plot(ax=axs[0], edgecolor="#e1e1e1")
usstates.plot(ax=axs[1], edgecolor="#e1e1e1")

for i in range(2):
    ax = axs[i]

    ax.set_xlim(-126, -68)
    ax.set_ylim(24, 50)


x += 1
plt.savefig(f"src/3-polygons/gif/{x}.png", dpi=300, bbox_inches="tight")

###############################################

fig, axs = plt.subplots(
    nrows=2, dpi=300, figsize=(10, 15), sharex=True, gridspec_kw={"hspace": 0.01}
)

uscounties.plot(ax=axs[0], edgecolor="#e1e1e1")
usstates.plot(ax=axs[1], edgecolor="#e1e1e1")

for i in range(2):
    ax = axs[i]

    ax.set_xlim(-126, -68)
    ax.set_ylim(24, 50)


x += 1
plt.savefig(f"src/3-polygons/gif/{x}.png", dpi=300, bbox_inches="tight")

###############################################

fig, axs = plt.subplots(
    nrows=2, dpi=300, figsize=(10, 15), sharex=True, gridspec_kw={"hspace": 0.01}
)

uscounties.plot(ax=axs[0], edgecolor="#e1e1e1")
usstates.plot(ax=axs[1], edgecolor="#e1e1e1")

for i in range(2):
    ax = axs[i]

    ax.set_xlim(-126, -68)
    ax.set_ylim(24, 50)
    ax.set_axis_off()


x += 1
plt.savefig(f"src/3-polygons/gif/{x}.png", dpi=300, bbox_inches="tight")

###############################################

fig, axs = plt.subplots(
    nrows=2, dpi=300, figsize=(10, 15), sharex=True, gridspec_kw={"hspace": 0.01}
)

map_args = dict(column="quartile", cmap=cmap)
uscounties.plot(ax=axs[0], **map_args)
usstates.plot(ax=axs[1], edgecolor="#e1e1e1")

for i in range(2):
    ax = axs[i]

    ax.set_xlim(-126, -68)
    ax.set_ylim(24, 50)
    ax.set_axis_off()


x += 1
plt.savefig(f"src/3-polygons/gif/{x}.png", dpi=300, bbox_inches="tight")

###############################################

fig, axs = plt.subplots(
    nrows=2, dpi=300, figsize=(10, 15), sharex=True, gridspec_kw={"hspace": 0.01}
)

map_args = dict(column="quartile", cmap=cmap)
uscounties.plot(ax=axs[0], **map_args)
usstates.plot(ax=axs[1], **map_args)

for i in range(2):
    ax = axs[i]

    ax.set_xlim(-126, -68)
    ax.set_ylim(24, 50)
    ax.set_axis_off()


x += 1
plt.savefig(f"src/3-polygons/gif/{x}.png", dpi=300, bbox_inches="tight")

###############################################

fig, axs = plt.subplots(
    nrows=2, dpi=300, figsize=(10, 15), sharex=True, gridspec_kw={"hspace": 0.01}
)

map_args = dict(column="quartile", cmap=cmap)
uscounties.plot(ax=axs[0], **map_args)
usstates.plot(ax=axs[1], **map_args)

for i in range(2):
    ax = axs[i]
    ax.set_xlim(-126, -68)
    ax.set_ylim(24, 50)
    ax.set_axis_off()
    ax.text(
        x=0.06,
        y=0.97,
        s=f"{group[i]}",
        transform=ax.transAxes,
        font=fontitalic,
        size=13,
        color="#585757",
    )

fig.text(x=0.14, y=0.867, s="By county VS by state", ha="left", size=50, font=fontbold)
fig.text(
    x=0.14,
    y=0.91,
    s="Unemployment rates (in %) in the United States",
    ha="left",
    size=20,
    font=fontlight,
    color="#282828",
)

x += 1
plt.savefig(f"src/3-polygons/gif/{x}.png", dpi=300, bbox_inches="tight")

###############################################

quartile_ranges = [
    (uscounties["rate"].quantile(0), uscounties["rate"].quantile(0.2)),
    (uscounties["rate"].quantile(0.2), uscounties["rate"].quantile(0.4)),
    (uscounties["rate"].quantile(0.4), uscounties["rate"].quantile(0.6)),
    (uscounties["rate"].quantile(0.6), uscounties["rate"].quantile(0.8)),
    (uscounties["rate"].quantile(0.8), uscounties["rate"].quantile(1)),
]
legend_elements = [
    Patch(
        facecolor=cmap.colors[i],
        edgecolor="none",
    )
    for i in range(5)
]

fig, axs = plt.subplots(
    nrows=2, dpi=300, figsize=(10, 15), sharex=True, gridspec_kw={"hspace": 0.01}
)

map_args = dict(column="quartile", cmap=cmap)
uscounties.plot(ax=axs[0], **map_args)
usstates.plot(ax=axs[1], **map_args)

for i in range(2):
    ax = axs[i]
    ax.set_xlim(-126, -68)
    ax.set_ylim(24, 50)
    ax.set_axis_off()
    ax.text(
        x=0.06,
        y=0.97,
        s=f"{group[i]}",
        transform=ax.transAxes,
        font=fontitalic,
        size=13,
        color="#585757",
    )

fig.text(x=0.14, y=0.867, s="By county VS by state", ha="left", size=50, font=fontbold)
fig.text(
    x=0.14,
    y=0.91,
    s="Unemployment rates (in %) in the United States",
    ha="left",
    size=20,
    font=fontlight,
    color="#282828",
)

for i, element in enumerate(legend_elements):
    axs[1].text(
        0.12 + i * 0.122,
        1.12,
        f"{quartile_ranges[i][0]:.1f} - {quartile_ranges[i][1]:.1f}",
        size=13,
        horizontalalignment="center",
        verticalalignment="top",
        transform=axs[1].transAxes,
        font=fontbold,
    )

fig.legend(
    handles=legend_elements,
    bbox_to_anchor=(0.65, 0.54),
    prop=fontbold,
    handlelength=4,
    fancybox=False,
    frameon=False,
    handleheight=3,
    labelspacing=0.8,
    ncol=len(legend_elements),
    labels=[""] * len(legend_elements),
)

x += 1
plt.savefig(f"src/3-polygons/gif/{x}.png", dpi=300, bbox_inches="tight")

###############################################
###############################################
###############################################
###############################################

file_path = [f"src/3-polygons/gif/{str(i)}.png" for i in range(1, x + 1)]
gif = Gif(file_path, frame_duration=1000, n_repeat_last_frame=4)
gif.set_background_color("white")
gif.set_size((1000, 1500), scale=2)
gif.set_labels(
    [
        "Simple map of the USA",
        "Dual map of the USA",
        "Maps with counties and states",
        "Remove borders around axes",
        "Apply colors to the counties map",
        "Apply colors to the states map",
        "Add a title and subtitle",
        "Include a legend",
    ],
    loc="bottom right",
    font="Eatingpasta",
    font_size=80,
    box_color="#f0ebd7",
)
gif.make()
