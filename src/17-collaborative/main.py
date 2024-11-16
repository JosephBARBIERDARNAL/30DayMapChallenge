import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

newyork = gpd.read_file("data/new-york-city-boroughs.geojson")
df = pd.read_csv("data/taxi_data.csv")

# keep only inside NY itself
df = df[(df["pickup_lat"] > 40.5) & (df["pickup_lat"] < 40.9)]
df = df[(df["pickup_lon"] > -74.3) & (df["pickup_lon"] < -73.7)]
df = df[(df["dropoff_lat"] > 40.5) & (df["dropoff_lat"] < 40.9)]
df = df[(df["dropoff_lon"] > -74.3) & (df["dropoff_lon"] < -73.7)]
df = df.sample(3000)


fig, ax = plt.subplots()
ax.axis("off")
ax.set_xlim(-74.3, -73.7)
ax.set_ylim(40.45, 40.95)

# background map
newyork.plot(ax=ax, color="#fef9e6", edgecolor="black", lw=0.5)

# draw lines
for i, row in df.iterrows():
    pickup_y, pickup_x = row["pickup_lat"], row["pickup_lon"]
    dropoff_y, dropoff_x = row["dropoff_lat"], row["dropoff_lon"]
    weight = row["total_amount"] / df["total_amount"].max()
    ax.plot(
        [pickup_x, dropoff_x],
        [pickup_y, dropoff_y],
        lw=weight,
        color="#252525",
        alpha=0.3,
    )

plt.tight_layout()
plt.savefig("src/17-collaborative/collaborative.png", dpi=500, bbox_inches="tight")
