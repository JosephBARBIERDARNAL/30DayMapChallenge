import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
from pypalettes import load_cmap
from pyfonts import load_font

with rasterio.open("data/GRAY_50M_SR_OB/GRAY_50M_SR_OB.tif") as src:
    raster_data = src.read(1)

text_color = "#c0bfbf"
cmap = load_cmap("Sunset", cmap_type="continuous")
font = load_font(
    "https://github.com/BornaIz/markazitext/blob/master/fonts/ttf/MarkaziText-Regular.ttf?raw=true"
)

fig, ax = plt.subplots()
ax.set_axis_off()
ax.set_xlim(50, 180)
ax.set_ylim(-50, 50)
show(raster_data, transform=src.transform, cmap=cmap, ax=ax)

fig.text(x=0.1, y=0.3, s="Asia & Oceania", font=font, size=18, color=text_color)

text_prop = dict(size=7, color=text_color, ha="left", font=font)
fig.text(x=0.05, y=0.07, s="#30daymapchallenge 2024", **text_prop)
fig.text(x=0.05, y=0.05, s="Raster - Joseph Barbier", **text_prop)

plt.tight_layout()
plt.savefig("src/6-raster/raster.png", dpi=500, bbox_inches="tight")
