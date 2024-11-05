import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from pypalettes import load_cmap

counties = gpd.read_file("data/US-counties/ne_10m_admin_2_counties.shp")
counties = counties[["NAME", "geometry", "CODE_LOCAL"]]
counties["CODE_LOCAL"] = counties["CODE_LOCAL"].astype(int)
counties["centroid"] = counties["geometry"].centroid

# https://data.humdata.org/dataset/social-connectedness-index
df = pd.read_csv("data/county_county.tsv", sep="\t")
df = df.rename(columns={"user_loc": "start", "fr_loc": "end", "scaled_sci": "SCI"})
df = df.merge(counties, how="inner", left_on="start", right_on="CODE_LOCAL").drop(
    columns=["geometry", "CODE_LOCAL"]
)
df = df.rename(columns={"NAME": "name_start", "centroid": "centroid_start"})
df = df.merge(counties, how="inner", left_on="end", right_on="CODE_LOCAL").drop(
    columns=["geometry", "CODE_LOCAL"]
)
df = df.rename(columns={"NAME": "name_end", "centroid": "centroid_end"})
df = df.sample(100000, random_state=1)

avg_sci = df.groupby("name_end", as_index=False)["SCI"].median()
counties = counties.merge(avg_sci, how="inner", left_on="NAME", right_on="name_end")

cmap = load_cmap("Coconut", cmap_type="continuous")

fig, ax = plt.subplots()
ax.set_xlim(-180, -60)
ax.set_ylim(17, 72)
ax.axis("off")

counties.plot(ax=ax, column="SCI", edgecolor="black", linewidth=0.1, cmap=cmap)

for i, row in df.iterrows():
    x_start, y_start = row["centroid_start"].coords[0]
    x_end, y_end = row["centroid_end"].coords[0]
    ax.plot([x_start, x_end], [y_start, y_end], color="#0ab8db", linewidth=0.01)

for i, row in counties.iterrows():
    x, y = row["centroid"].coords[0]
    ax.scatter(x, y, color="black", s=0.5)

plt.tight_layout()
plt.savefig("src/8-HDX/hdx.png", dpi=500, bbox_inches="tight")
