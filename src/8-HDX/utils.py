import pandas as pd
import geopandas as gpd
import streamlit as st


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
    df = df.sample(1000000, random_state=1)

    avg_sci = df.groupby("name_end", as_index=False)["SCI"].median()
    counties = counties.merge(avg_sci, how="inner", left_on="NAME", right_on="name_end")

    return df, counties
