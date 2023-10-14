import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import json

@st.cache_data
def load_data():
    data = pd.read_csv("dataset/annual_conc_by_monitor_2022/annual_conc_by_monitor_2022.csv")
    return data

st.sidebar.title("EDA Options")

df = load_data()
df.dropna()
st.title("Air Quality Dataset")
st.write("""
The Air Quality dataset is a collection of pollutant data that offers critical insights on concentration of pollutants.

""")

# age_range = st.sidebar.slider("Select Age Range", min_value=int(df['Age'].min()), max_value=int(df['Age'].max()), value=(int(data['Age'].min()), int(data['Age'].max())))
# gender = st.sidebar.radio("Select Gender", ["All", "Male", "Female"])
    
# st.header("Data Visualization")
# filtered_data = df.copy()
# filtered_data = filtered_data[(filtered_data['Age'] >= age_range[0]) & (filtered_data['Age'] <= age_range[1])]
# if gender != "All":
#     filtered_data = filtered_data[filtered_data['Sex'] == ("F" if gender == "Female" else "M")]

st.header("Location of the air quality monitors")
fig = px.scatter_mapbox(
    df,  
    lat="Latitude",  
    lon="Longitude", 
    zoom=3  
)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig, use_container_width=True)


st.header("Statewise- Concentration of Ozone")

with open('geojson/USA_state.geojson', 'r') as geojson_file:
    geojson_data = json.load(geojson_file)

col="99th Percentile" 

custom_agg= lambda x: x.max()
fig = px.choropleth_mapbox(
    df.loc[df["Parameter Name"]=="Ozone"].groupby("State Name")[col].agg(**{col: custom_agg}).reset_index(),
    geojson=geojson_data,
    locations='State Name',
    featureidkey="properties.shapeName",  
    color=col,
    color_continuous_scale='magma',  
    mapbox_style="carto-positron",
    center={"lat": 37.0902, "lon": -95.7129},
    zoom=3,
)

st.plotly_chart(fig, use_container_width=True)