import pandas as pd
import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt

newyork = gpd.read_file("data/new-york-city-boroughs.geojson")
df = pd.read_csv("data/taxi_data.csv")

# keep only inside NY itself
df = df[(df["pickup_lat"] > 40.5) & (df["pickup_lat"] < 40.9)]
df = df[(df["pickup_lon"] > -74.3) & (df["pickup_lon"] < -73.7)]
df = df[(df["dropoff_lat"] > 40.5) & (df["dropoff_lat"] < 40.9)]
df = df[(df["dropoff_lon"] > -74.3) & (df["dropoff_lon"] < -73.7)]
# df = df.sample(15000)

fig, ax = plt.subplots()
ax.axis("off")


# background map
newyork.plot(ax=ax, color="#e6e3ff", edgecolor="black", lw=0.5)

sns.kdeplot(
    x=df["dropoff_lon"], y=df["dropoff_lat"], cmap="Reds", fill=True, alpha=0.5, ax=ax
)

plt.tight_layout()
plt.savefig("src/17-collaborative/collaborative2.png", dpi=500, bbox_inches="tight")
