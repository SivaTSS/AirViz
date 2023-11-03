
import streamlit as st
import pandas as pd

@st.cache_data
def load_data(filepath):
    if "parquet" in filepath:
        data = pd.read_parquet(filepath)
    elif "csv" in filepath:
        data = pd.read_csv(filepath)
    else:
        raise Exception("file format not supported")
    return data

mapbox_layout = {
    "style": "carto-positron",
    "center": {"lat": 38.0902, "lon": -95.7129},
    "zoom": 2.6,
}


params = [
    "Carbon monoxide",
    "Sulfur dioxide",
    "Nitrogen dioxide (NO2)",
    "Ozone",
    "PM10 Total 0-10um STP",
    "PM10-2.5 - Local Conditions",
    "PM2.5 - Local Conditions",
    "Acceptable PM2.5 AQI & Speciation Mass",
    "Lead (TSP) STP",
    "Barometric pressure",
    "Relative Humidity ",
    "Dew Point",
    "Outdoor Temperature",
    "Wind Direction - Resultant",
    "Wind Speed - Resultant",
]