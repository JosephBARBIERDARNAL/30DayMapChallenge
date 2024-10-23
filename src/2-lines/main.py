from ridge_map import RidgeMap
import matplotlib.pyplot as plt
from pyfonts import load_font
from pypalettes import load_cmap
from highlight_text import fig_text

font = load_font(
    "https://github.com/googlefonts/imperial-script/blob/master/fonts/ttf/ImperialScript-Regular.ttf?raw=true"
)
font2 = load_font(
    "https://github.com/googlefonts/lexend/blob/main/fonts/lexend/ttf/Lexend-Medium.ttf?raw=true"
)
boldfont2 = load_font(
    "https://github.com/googlefonts/lexend/blob/main/fonts/lexend/ttf/Lexend-Bold.ttf?raw=true"
)
cmap = load_cmap("Starfish", cmap_type="continuous")
background_color = "#f6f6f6"

location = (-1.476030, 41.697286, 2.973862, 43.746855)
rm = RidgeMap(location, font=font)
values = rm.get_elevation_data(num_lines=300)

ratio = (location[3] - location[1]) / (location[2] - location[0])
fig, ax = plt.subplots(dpi=300, figsize=(10, 10 * ratio))
fig.set_facecolor(background_color)
rm.plot_map(
    values=rm.preprocess(
        values=values, vertical_ratio=200, water_ntile=10, lake_flatness=1
    ),
    linewidth=0.6,
    label="",
    line_color=cmap,
    background_color=background_color,
    kind="elevation",
    ax=ax,
)

text_style = dict(
    font=font2,
    color="black",
    transform=ax.transAxes,
    verticalalignment="bottom",
    zorder=len(values) + 10,
    bbox=dict(facecolor=background_color, alpha=0.7, edgecolor="none", pad=1),
)
to_annotate = {
    "Andorra": (1.574387, 42.558644),
    "Pau": (-0.378921, 43.299260),
    "Toulouse": (1.441998, 43.617840),
    "Huesca": (-0.420474, 42.149922),
    "Aneto (11,168 ft)": (0.656798, 42.627154),
}
for city, loc in to_annotate.items():
    city_location = (
        (loc[0] - rm.longs[0]) / (rm.longs[1] - rm.longs[0]),
        (loc[1] - rm.lats[0]) / (rm.lats[1] - rm.lats[0]),
    )

    ax.text(
        city_location[0] + 0.007,
        city_location[1] - 0.04,
        f"{city}",
        size=8,
        **text_style,
    )

    if "Aneto" in city:
        ax.text(
            city_location[0] + 0.007,
            city_location[1] - 0.07,
            "Highest mountain in the Pyrenees",
            size=6,
            **text_style,
        )

    ax.plot(
        *city_location,
        "o",
        color="black",
        transform=ax.transAxes,
        ms=2,
        zorder=len(values) + 10,
    )

fig_text(x=0.16, y=0.12, s="#30daymapchallenge 2024", font=boldfont2, size=7, ha="left")
fig_text(x=0.16, y=0.09, s="Lines - Joseph Barbier", font=font2, size=7, ha="left")
fig_text(
    s="<A Mountain range straddling the border of France and Spain>\nThe Pyrenees",
    y=0.86,
    x=0.16,
    size=26,
    font=font,
    highlight_textprops=[{"font": font2, "size": 8}],
)

plt.savefig("src/2-lines/lines.png", dpi=500, bbox_inches="tight")
plt.close()
