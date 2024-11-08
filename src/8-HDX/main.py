import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patheffects as pe
from pypalettes import add_cmap
from pyfonts import load_font

italy = gpd.read_file("data/italy.geojson")

df = pd.read_csv("data/consumer-price-indices_ita.csv")
df = df.loc[df["Item"] == "Food price inflation"]
df = df.drop(
    columns=[
        "Note",
        "Iso3",
        "Area",
        # "Value",
        "Year Code",
        "Item",
        "Item Code",
        "Months Code",
        "Element",
        "Element Code",
        "Unit",
        "Area Code (M49)",
        "Area Code",
        "Flag",
    ]
)
df["StartDate"] = pd.to_datetime(df["StartDate"])
df = df.sort_values("StartDate")

font = load_font(
    "https://github.com/coreyhu/Urbanist/blob/main/fonts/ttf/Urbanist-Medium.ttf?raw=true"
)
boldfont = load_font(
    "https://github.com/coreyhu/Urbanist/blob/main/fonts/ttf/Urbanist-ExtraBold.ttf?raw=true"
)

green = "#008C45"
white = "#F4F9FF"
red = "#CD212A"
cmap = add_cmap(colors=[green, white, red], name="ItalyFlag", cmap_type="continuous")

fig, ax = plt.subplots(dpi=500)
fig.set_facecolor("#fff8f8")

text_args = dict(
    va="top",
    ha="left",
    transform=fig.transFigure,
)


def update(date):

    ax.clear()
    ax.axis("off")
    ax.set_xlim(2, 19)

    subset = df[df["StartDate"] <= date]
    value = df.loc[df["StartDate"] == date, "Value"].values[0]
    color = cmap((value - df["Value"].min()) / (df["Value"].max() - df["Value"].min()))
    print(date)

    italy.plot(ax=ax, color=color, edgecolor="black", linewidth=0.2)

    lineax = ax.inset_axes(bounds=[0, 0.1, 0.6, 0.22], transform=ax.transAxes)
    lineax.set_ylim(df["Value"].min(), df["Value"].max() * 1.05)
    lineax.axis("off")

    lineax.scatter(
        subset["StartDate"],
        subset["Value"],
        c=subset["Value"],
        cmap=cmap,
        s=7,
        zorder=5,
    )

    y_axis_values = [0, 4, 8, 12]
    lineax.hlines(
        y=y_axis_values,
        xmin=df["StartDate"].min(),
        xmax=df["StartDate"].max(),
        color="black",
        linewidth=0.3,
        zorder=1,
        alpha=0.4,
    )
    for y_value in y_axis_values:
        lineax.text(
            x=df["StartDate"].min() - pd.Timedelta(weeks=90),
            y=y_value,
            s=f"{y_value:.0f}%",
            font=font,
            size=5,
            va="center",
            ha="left",
        )

    ax.text(
        x=0.24,
        y=0.6,
        s=f"Italy inflation - {str(date)[:4]}",
        size=12,
        font=font,
        **text_args,
    )
    ax.text(
        x=0.24,
        y=0.55,
        s=f"{value:.1f}%",
        size=16,
        color=color,
        path_effects=[pe.Stroke(linewidth=1, foreground="black"), pe.Normal()],
        font=boldfont,
        **text_args,
    )
    ax.text(
        x=0.6, y=0.7, s=f"#30DayMapChallenge - HDX", size=5, font=boldfont, **text_args
    )
    ax.text(x=0.6, y=0.7, s=f"\nJoseph Barbier", size=5, font=font, **text_args)


anim = FuncAnimation(fig, update, frames=df["StartDate"])
anim.save("src/8-HDX/hdx.gif", fps=15)
