import prettymaps as pm
import matplotlib.pyplot as plt

plot = pm.plot(query=(44.846030, -0.566520), preset="heerhugowaard", radius=1600)

text_args = dict(
    transform=plt.gcf().transFigure, size=12, weight="bold", ha="center", font="Arial"
)
plt.text(x=0.5, y=0.935, s="#30DayMapChallenge", **text_args)
plt.text(x=0.5, y=0.92, s="Vintage style - Joseph Barbier", **text_args)
plt.text(
    x=0.32,
    y=0.06,
    s="The Garonne River crossing Bordeaux, France",
    transform=plt.gcf().transFigure,
    size=17,
    ha="center",
    font="Arial",
)
plt.savefig("src/7-vintage_style/vintage_style.png", dpi=500)
