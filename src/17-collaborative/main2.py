import pandas as pd
import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt
from pypalettes import load_cmap

newyork = gpd.read_file("data/new-york-city-boroughs.geojson")
df = pd.read_csv("data/taxi_data.csv")

# keep only inside NY itself
df = df[(df["pickup_lat"] > 40.5) & (df["pickup_lat"] < 40.9)]
df = df[(df["pickup_lon"] > -74.3) & (df["pickup_lon"] < -73.7)]
df = df[(df["dropoff_lat"] > 40.5) & (df["dropoff_lat"] < 40.9)]
df = df[(df["dropoff_lon"] > -74.3) & (df["dropoff_lon"] < -73.7)]
# df = df.sample(15000)

cmap = load_cmap("Coconut", cmap_type="continuous")

fig, (ax1, ax2) = plt.subplots(ncols=2)
ax1.axis("off")
ax2.axis("off")

newyork.plot(ax=ax1, color="#f3f3f3", edgecolor="black", lw=0.5)
newyork.plot(ax=ax2, color="#f3f3f3", edgecolor="black", lw=0.5)

sns.kdeplot(
    x=df["dropoff_lon"], y=df["dropoff_lat"], cmap=cmap, fill=True, alpha=0.7, ax=ax1
)
sns.kdeplot(
    x=df["pickup_lon"], y=df["pickup_lat"], cmap=cmap, fill=True, alpha=0.7, ax=ax2
)

plt.tight_layout()
plt.savefig("src/17-collaborative/collaborative2.png", dpi=500, bbox_inches="tight")
