import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
from pypalettes import load_cmap
from pyfonts import load_font

with rasterio.open("data/GRAY_50M_SR_OB/GRAY_50M_SR_OB.tif") as src:
    raster_data = src.read(1)

text_color = "#000000"
cmap1 = load_cmap("bee_eater", cmap_type="continuous")
cmap1 = load_cmap("Beach", cmap_type="continuous")
cmap2 = load_cmap("blaziken", cmap_type="continuous", reverse=True)
cmap3 = load_cmap("bobcats", cmap_type="continuous", reverse=True)
cmap4 = load_cmap("bryce", cmap_type="continuous", reverse=True)
font = load_font(
    "https://github.com/BornaIz/markazitext/blob/master/fonts/ttf/MarkaziText-Regular.ttf?raw=true"
)

fig, mainax = plt.subplots(figsize=(9.7, 5))
mainax.axis("off")

ax1 = mainax.inset_axes([0, 0, 0.5, 0.5])
ax2 = mainax.inset_axes([0.5, 0.5, 0.5, 0.5])
ax3 = mainax.inset_axes([0.5, 0, 0.5, 0.5])
ax4 = mainax.inset_axes([0, 0.5, 0.5, 0.5])

ax1.set_xlim(-180, 0)
ax1.set_ylim(-90, 0)

ax2.set_xlim(0, 180)
ax2.set_ylim(0, 90)

ax3.set_xlim(0, 180)
ax3.set_ylim(-90, 0)

ax4.set_xlim(-180, 0)
ax4.set_ylim(0, 90)

show(raster_data, transform=src.transform, cmap=cmap1, ax=ax1)
show(raster_data, transform=src.transform, cmap=cmap2, ax=ax2)
show(raster_data, transform=src.transform, cmap=cmap3, ax=ax3)
show(raster_data, transform=src.transform, cmap=cmap4, ax=ax4)

for ax in [ax1, ax2, ax3, ax4]:
    ax.axis("off")

text_prop = dict(size=11, color=text_color, ha="left", font=font)
fig.text(x=0.05, y=0.18, s="#30daymapchallenge 2024", **text_prop)
fig.text(x=0.05, y=0.15, s="Raster - Joseph Barbier", **text_prop)

plt.tight_layout()
plt.savefig("src/6-raster/raster.png", dpi=800, bbox_inches="tight")
