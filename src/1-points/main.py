import folium
import pandas as pd
from branca.element import Figure

df = pd.read_csv("data/earthquakes.csv")
df.sort_values(by="Magnitude", ascending=True, inplace=True)

color1, color2, color3 = "#881C00FF", "#F4E3C7FF", "#1BB6AFFF"

fig = Figure(width="100%", height="100%")
m = folium.Map(location=[20, 0], zoom_start=3, tiles="cartodb positron")
fig.add_child(m)

title_html = """
<div style="position: fixed; 
            top: 20px; 
            left: 50%; 
            transform: translateX(-50%);
            z-index: 1000;
            background-color: rgba(0,0,0,0.7);
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            font-family: Arial;
            text-align: center;">
    <h1 style="margin:0;">Global Seismic Activity (2015 and 2024)</h1>
    <p style="margin:5px 0 0 0;font-size:20px;">Data from Pakistan Meteorological Department</p>
</div>
"""
m.get_root().html.add_child(folium.Element(title_html))

legend_html = f"""
<div style="position: fixed; 
            top: 20px; 
            right: 20px; 
            z-index: 1000;
            background-color: rgba(0,0,0,0.7);
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-family: Arial;">
    <h4 style="margin:0 0 10px 0;">Magnitude Scale</h4>
    <div style="margin-bottom:5px;">
        <span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:{color1};margin-right:5px;"></span>
        Major (≥ 7.0)
    </div>
    <div style="margin-bottom:5px;">
        <span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:{color2};margin-right:5px;"></span>
        Moderate (5.0-6.9)
    </div>
    <div>
        <span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:{color3};margin-right:5px;"></span>
        Minor (< 5.0)
    </div>
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

for idx, row in df.iterrows():
    tooltip_text = f"""
<center><h1><b>{row['Region']}</b></h1></center>
<h3><b>Magnitude:</b> {row['Magnitude']}</h3>
<h3><b>Depth:</b> {row['Depth (km)']} km</h3>
<h3><b>Year:</b> {row['Date'][-4:]}</h3>
    """

    color = (
        color3 if row["Magnitude"] < 5 else color2 if row["Magnitude"] < 7 else color1
    )
    radius = row["Magnitude"] ** 2 / 3

    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=radius,
        fill_color=color,
        color="black",
        fill_opacity=0.7,
        weight=1,
        tooltip=folium.Tooltip(tooltip_text, sticky=True),
        popup=folium.Popup(tooltip_text, max_width=300),
    ).add_to(m)

m.save("src/1-points/index.html")
m.save("docs/earthquakes.html")
