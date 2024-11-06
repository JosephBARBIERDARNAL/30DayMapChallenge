import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go


@st.cache_data(show_spinner=False)
def load_data():
    counties = gpd.read_file("data/US-counties/ne_10m_admin_2_counties.shp")
    counties = counties[["NAME", "geometry", "CODE_LOCAL"]]
    counties["CODE_LOCAL"] = counties["CODE_LOCAL"].astype(int)
    counties["centroid"] = counties["geometry"].centroid

    # data source: https://data.humdata.org/dataset/social-connectedness-index
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
    df = df.sample(10000, random_state=1)

    avg_sci = df.groupby("name_end", as_index=False)["SCI"].median()
    counties = counties.merge(avg_sci, how="inner", left_on="NAME", right_on="name_end")

    return df, counties


st.markdown("# County connection")

df, counties = load_data()

county = st.selectbox("County", options=df["name_end"])

if county:
    subset = df[df["name_end"] == county]

    # Create an empty figure
    fig = go.Figure()

    # Plot all counties in a base layer
    fig.add_trace(
        go.Choropleth(
            geojson=counties.set_index("NAME")["geometry"].__geo_interface__,
            locations=counties["NAME"],
            z=counties["SCI"],
            colorscale="Reds",
            marker_line_color="black",
            marker_line_width=0.1,
            showscale=False,
            hoverinfo="location+z",
        )
    )

    # Plot connections for the selected county
    for i, row in subset.iterrows():
        x_start, y_start = row["centroid_start"].coords[0]
        x_end, y_end = row["centroid_end"].coords[0]
        fig.add_trace(
            go.Scattergeo(
                lon=[x_start, x_end],
                lat=[y_start, y_end],
                mode="lines",
                line=dict(width=3, color="black"),
                opacity=0.4,
                showlegend=False,
            )
        )

    # Update layout to make it look like a map
    fig.update_geos(
        projection_type="albers usa",
        showcountries=True,
        countrycolor="black",
        showland=True,
        landcolor="lightgray",
        lakecolor="lightblue",
    )

    fig.update_layout(
        title_text=f"Connections for {county}",
        height=600,
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
    )

    st.plotly_chart(fig)
