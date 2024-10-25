import prettymaps as pm
import matplotlib.pyplot as plt

plot = pm.plot(query=(-33.884788, 151.200655), preset="heerhugowaard", radius=6000)

plt.tight_layout()
plt.savefig("src/7-vintage_style/vintage_style.png", dpi=500, bbox_inches="tight")
